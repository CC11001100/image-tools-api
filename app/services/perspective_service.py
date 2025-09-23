from PIL import Image
import cv2
import numpy as np
import io
from typing import List, Tuple, Optional
from ..utils.logger import logger


class PerspectiveService:
    """透视校正服务"""

    @staticmethod
    def process_perspective(
        image_bytes: bytes,
        points: str = None,
        auto_document: bool = False,
        width: Optional[int] = None,
        height: Optional[int] = None,
        quality: int = 90
    ) -> bytes:
        """
        通用透视处理方法

        Args:
            image_bytes: 输入图片的字节数据
            points: 四点坐标字符串，格式：[[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
            auto_document: 是否使用自动文档校正
            width: 输出图像宽度
            height: 输出图像高度
            quality: 输出图像质量 (1-100)

        Returns:
            处理后图片的字节数据
        """
        logger.info(f"执行透视处理: auto_document={auto_document}, points={points}")

        if auto_document:
            return PerspectiveService.auto_correct_document(image_bytes, quality)
        elif points:
            # 解析点坐标字符串
            import json
            try:
                points_list = json.loads(points)
                src_points = [(int(p[0]), int(p[1])) for p in points_list]
                return PerspectiveService.correct_perspective(
                    image_bytes, src_points, width, height, quality
                )
            except (json.JSONDecodeError, ValueError, IndexError) as e:
                raise ValueError(f"无效的点坐标格式: {e}")
        else:
            raise ValueError("必须提供points参数或设置auto_document=True")
    
    @staticmethod
    def correct_perspective(
        image_bytes: bytes,
        src_points: List[Tuple[int, int]],
        width: Optional[int] = None,
        height: Optional[int] = None,
        quality: int = 90
    ) -> bytes:
        """
        透视校正 - 四点透视变换
        
        Args:
            image_bytes: 输入图片的字节数据
            src_points: 源图像四个角点坐标 [(x1,y1), (x2,y2), (x3,y3), (x4,y4)]
            width: 输出图像宽度（默认自动计算）
            height: 输出图像高度（默认自动计算）
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据
        """
        logger.info(f"透视校正: 源点={src_points}")
        
        try:
            # 打开图像
            img = Image.open(io.BytesIO(image_bytes))
            img_array = np.array(img)
            
            # 验证源点数量
            if len(src_points) != 4:
                raise ValueError("需要提供4个源点坐标")
            
            # 转换为numpy数组
            src_pts = np.float32(src_points)
            
            # 如果没有指定输出尺寸，自动计算
            if width is None or height is None:
                # 计算边长
                width_top = np.sqrt(((src_pts[1][0] - src_pts[0][0]) ** 2) + 
                                   ((src_pts[1][1] - src_pts[0][1]) ** 2))
                width_bottom = np.sqrt(((src_pts[3][0] - src_pts[2][0]) ** 2) + 
                                      ((src_pts[3][1] - src_pts[2][1]) ** 2))
                width = int(max(width_top, width_bottom))
                
                height_left = np.sqrt(((src_pts[2][0] - src_pts[0][0]) ** 2) + 
                                     ((src_pts[2][1] - src_pts[0][1]) ** 2))
                height_right = np.sqrt(((src_pts[3][0] - src_pts[1][0]) ** 2) + 
                                      ((src_pts[3][1] - src_pts[1][1]) ** 2))
                height = int(max(height_left, height_right))
            
            # 定义目标点（矩形）
            dst_pts = np.float32([
                [0, 0],
                [width - 1, 0],
                [0, height - 1],
                [width - 1, height - 1]
            ])
            
            # 计算透视变换矩阵
            matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
            
            # 应用透视变换
            if len(img_array.shape) == 3 and img_array.shape[2] == 3:
                # RGB图像
                img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            elif len(img_array.shape) == 3 and img_array.shape[2] == 4:
                # RGBA图像
                img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGRA)
            else:
                # 灰度图像
                img_bgr = img_array
            
            # 执行透视变换
            result = cv2.warpPerspective(img_bgr, matrix, (width, height))
            
            # 转换回RGB/RGBA
            if len(img_array.shape) == 3 and img_array.shape[2] == 3:
                result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
            elif len(img_array.shape) == 3 and img_array.shape[2] == 4:
                result = cv2.cvtColor(result, cv2.COLOR_BGRA2RGBA)
            
            # 转换为PIL图像
            result_img = Image.fromarray(result)
            
            # 保存并返回
            output = io.BytesIO()
            format = img.format if img.format else "JPEG"
            result_img.save(output, format=format, quality=quality)
            
            logger.info("透视校正成功")
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"透视校正失败: {e}")
            raise
    
    @staticmethod
    def auto_correct_document(
        image_bytes: bytes,
        quality: int = 90
    ) -> bytes:
        """
        自动文档透视校正
        
        Args:
            image_bytes: 输入图片的字节数据
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据
        """
        logger.info("自动文档透视校正")
        
        try:
            # 打开图像
            img = Image.open(io.BytesIO(image_bytes))
            img_array = np.array(img)
            
            # 转换为灰度图
            if len(img_array.shape) == 3:
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = img_array
            
            # 边缘检测
            edges = cv2.Canny(gray, 50, 150, apertureSize=3)
            
            # 查找轮廓
            contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            
            # 找到最大的矩形轮廓
            max_area = 0
            best_contour = None
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > max_area:
                    # 近似多边形
                    peri = cv2.arcLength(contour, True)
                    approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
                    
                    # 如果是四边形
                    if len(approx) == 4:
                        max_area = area
                        best_contour = approx
            
            if best_contour is None:
                # 未找到合适的轮廓，返回原图
                logger.warning("未找到文档边缘，返回原图")
                output = io.BytesIO()
                img.save(output, format=img.format or "JPEG", quality=quality)
                return output.getvalue()
            
            # 获取四个角点
            points = best_contour.reshape(4, 2)
            
            # 对点进行排序（左上、右上、左下、右下）
            rect = np.zeros((4, 2), dtype="float32")
            
            # 计算每个点的和
            s = points.sum(axis=1)
            rect[0] = points[np.argmin(s)]  # 左上
            rect[3] = points[np.argmax(s)]  # 右下
            
            # 计算每个点的差
            diff = np.diff(points, axis=1)
            rect[1] = points[np.argmin(diff)]  # 右上
            rect[2] = points[np.argmax(diff)]  # 左下
            
            # 应用透视校正
            src_points = [(int(p[0]), int(p[1])) for p in rect]
            
            return PerspectiveService.correct_perspective(
                image_bytes,
                src_points,
                quality=quality
            )
            
        except Exception as e:
            logger.error(f"自动文档透视校正失败: {e}")
            raise 