#!/usr/bin/env python3
"""
批量生成所有剩余页面的示例图片并上传到OSS
涵盖: blend, stitch, overlay, mask, noise, pixelate, color, text, annotation, format, gif
"""

import os
import sys
import requests
import tempfile
import asyncio
from pathlib import Path
from typing import List, Dict, Any

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.services.oss_client import oss_client
from app.services.blend_service import BlendService
from app.services.stitch_service_backup import StitchService
from app.services.overlay.main import OverlayService
from app.services.mask_service import MaskService
from app.services.noise_service_backup import NoiseService
from app.services.pixelate_service import PixelateService
from app.services.color_service import ColorService
from app.services.text_service_backup import TextService
from app.services.annotation_service_backup import AnnotationService
from app.services.format_service import FormatService
from app.services.gif_service import GifService

def download_random_image(width=1080, height=1920, seed=None):
    """从picsum.photos下载指定尺寸的随机图片"""
    if seed:
        url = f"https://picsum.photos/seed/{seed}/{width}/{height}"
    else:
        url = f"https://picsum.photos/{width}/{height}"
    
    print(f"📥 下载图片: {url}")
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def upload_to_oss(image_bytes, file_key):
    """上传图片到OSS"""
    try:
        print(f"📤 上传到OSS: {file_key}")
        oss_url = oss_client.upload_bytes(image_bytes, file_key)
        if oss_url:
            print(f"✅ 上传成功: {oss_url}")
            return oss_url
        else:
            print(f"❌ 上传失败: {file_key}")
            return None
    except Exception as e:
        print(f"❌ 上传失败: {file_key} - {e}")
        return None

class BatchExampleGenerator:
    """批量示例生成器"""
    
    def __init__(self):
        self.success_count = 0
        self.total_count = 0
        
    def generate_blend_examples(self):
        """生成blend页面示例"""
        print("\n🎨 生成Blend页面示例...")
        
        examples = [
            {
                'title': '正常混合',
                'name': 'normal',
                'seed1': 'blend-base-001',
                'seed2': 'blend-overlay-001',
                'params': {'blend_mode': 'normal', 'opacity': 0.8, 'quality': 90}
            },
            {
                'title': '正片叠底',
                'name': 'multiply',
                'seed1': 'blend-base-002',
                'seed2': 'blend-overlay-002',
                'params': {'blend_mode': 'multiply', 'opacity': 0.7, 'quality': 90}
            },
            {
                'title': '滤色混合',
                'name': 'screen',
                'seed1': 'blend-base-003',
                'seed2': 'blend-overlay-003',
                'params': {'blend_mode': 'screen', 'opacity': 0.8, 'quality': 90}
            },
            {
                'title': '叠加混合',
                'name': 'overlay',
                'seed1': 'blend-base-004',
                'seed2': 'blend-overlay-004',
                'params': {'blend_mode': 'overlay', 'opacity': 0.9, 'quality': 90}
            }
        ]
        
        for example in examples:
            self.total_count += 1
            try:
                # 下载两张图片
                base_image = download_random_image(seed=example['seed1'])
                overlay_image = download_random_image(seed=example['seed2'])
                
                # 上传原图
                base_key = f"blend/base-{example['name']}.jpg"
                overlay_key = f"blend/overlay-{example['name']}.jpg"
                base_url = upload_to_oss(base_image, base_key)
                overlay_url = upload_to_oss(overlay_image, overlay_key)
                
                if not (base_url and overlay_url):
                    continue
                
                # 处理混合效果
                print(f"🎨 处理混合效果: {example['title']}")
                blended_image = BlendService.blend_images(
                    base_image, overlay_image, **example['params']
                )
                
                # 上传混合结果
                result_key = f"blend/blend-{example['name']}.jpg"
                result_url = upload_to_oss(blended_image, result_key)
                
                if result_url:
                    print(f"✅ Blend示例完成: {example['title']}")
                    self.success_count += 1
                    
            except Exception as e:
                print(f"❌ Blend示例失败: {example['title']} - {e}")
    
    def generate_stitch_examples(self):
        """生成stitch页面示例"""
        print("\n🧩 生成Stitch页面示例...")
        
        examples = [
            {
                'title': '水平拼接',
                'name': 'horizontal',
                'seeds': ['stitch-h1-001', 'stitch-h2-001', 'stitch-h3-001'],
                'params': {'direction': 'horizontal', 'spacing': 10, 'quality': 90}
            },
            {
                'title': '垂直拼接',
                'name': 'vertical',
                'seeds': ['stitch-v1-002', 'stitch-v2-002'],
                'params': {'direction': 'vertical', 'spacing': 5, 'quality': 90}
            },
            {
                'title': '网格拼接',
                'name': 'grid',
                'seeds': ['stitch-g1-003', 'stitch-g2-003', 'stitch-g3-003', 'stitch-g4-003'],
                'params': {'direction': 'grid', 'spacing': 8, 'quality': 90}
            }
        ]
        
        for example in examples:
            self.total_count += 1
            try:
                # 下载多张图片
                images = []
                for i, seed in enumerate(example['seeds']):
                    img_bytes = download_random_image(seed=seed, width=540, height=960)  # 使用较小尺寸便于拼接
                    images.append(img_bytes)
                    
                    # 上传原图
                    orig_key = f"stitch/original-{example['name']}-{i+1}.jpg"
                    upload_to_oss(img_bytes, orig_key)
                
                # 处理拼接效果
                print(f"🧩 处理拼接效果: {example['title']}")
                stitched_image = StitchService.stitch_images(images, **example['params'])
                
                # 上传拼接结果
                result_key = f"stitch/stitch-{example['name']}.jpg"
                result_url = upload_to_oss(stitched_image, result_key)
                
                if result_url:
                    print(f"✅ Stitch示例完成: {example['title']}")
                    self.success_count += 1
                    
            except Exception as e:
                print(f"❌ Stitch示例失败: {example['title']} - {e}")
    
    def generate_overlay_examples(self):
        """生成overlay页面示例"""
        print("\n🔄 生成Overlay页面示例...")
        
        examples = [
            {
                'title': '中心叠加',
                'name': 'center',
                'seed1': 'overlay-base-001',
                'seed2': 'overlay-top-001',
                'params': {'position': 'center', 'opacity': 0.8, 'quality': 90}
            },
            {
                'title': '左上角叠加',
                'name': 'top-left',
                'seed1': 'overlay-base-002',
                'seed2': 'overlay-top-002',
                'params': {'position': 'top-left', 'opacity': 0.9, 'quality': 90}
            },
            {
                'title': '右下角叠加',
                'name': 'bottom-right',
                'seed1': 'overlay-base-003',
                'seed2': 'overlay-top-003',
                'params': {'position': 'bottom-right', 'opacity': 0.7, 'quality': 90}
            }
        ]
        
        for example in examples:
            self.total_count += 1
            try:
                # 下载两张图片
                base_image = download_random_image(seed=example['seed1'])
                overlay_image = download_random_image(seed=example['seed2'], width=540, height=480)  # 叠加图片较小
                
                # 上传原图
                base_key = f"overlay/base-{example['name']}.jpg"
                overlay_key = f"overlay/overlay-{example['name']}.jpg"
                upload_to_oss(base_image, base_key)
                upload_to_oss(overlay_image, overlay_key)
                
                # 处理叠加效果
                print(f"🔄 处理叠加效果: {example['title']}")
                overlaid_image = OverlayService.add_overlay(
                    base_image, overlay_type='gradient', **example['params']
                )
                
                # 上传叠加结果
                result_key = f"overlay/overlay-{example['name']}.jpg"
                result_url = upload_to_oss(overlaid_image, result_key)
                
                if result_url:
                    print(f"✅ Overlay示例完成: {example['title']}")
                    self.success_count += 1
                    
            except Exception as e:
                print(f"❌ Overlay示例失败: {example['title']} - {e}")
    
    def generate_mask_examples(self):
        """生成mask页面示例"""
        print("\n🎭 生成Mask页面示例...")

        examples = [
            {
                'title': '圆形遮罩',
                'name': 'circle',
                'seed': 'mask-circle-001',
                'params': {'mask_type': 'circle', 'feather': 10, 'quality': 90}
            },
            {
                'title': '矩形遮罩',
                'name': 'rectangle',
                'seed': 'mask-rect-002',
                'params': {'mask_type': 'rectangle', 'feather': 5, 'quality': 90}
            },
            {
                'title': '椭圆遮罩',
                'name': 'ellipse',
                'seed': 'mask-ellipse-003',
                'params': {'mask_type': 'ellipse', 'feather': 15, 'quality': 90}
            }
        ]

        for example in examples:
            self.total_count += 1
            try:
                # 下载原图
                original_image = download_random_image(seed=example['seed'])

                # 上传原图
                orig_key = f"mask/original-{example['name']}.jpg"
                upload_to_oss(original_image, orig_key)

                # 处理遮罩效果
                print(f"🎭 处理遮罩效果: {example['title']}")
                masked_image = MaskService.apply_mask(original_image, **example['params'])

                # 上传遮罩结果
                result_key = f"mask/mask-{example['name']}.jpg"
                result_url = upload_to_oss(masked_image, result_key)

                if result_url:
                    print(f"✅ Mask示例完成: {example['title']}")
                    self.success_count += 1

            except Exception as e:
                print(f"❌ Mask示例失败: {example['title']} - {e}")

    def generate_noise_examples(self):
        """生成noise页面示例"""
        print("\n🌪️ 生成Noise页面示例...")

        examples = [
            {
                'title': '高斯噪点',
                'name': 'gaussian',
                'seed': 'noise-gaussian-001',
                'params': {'noise_type': 'gaussian', 'intensity': 0.3, 'quality': 90}
            },
            {
                'title': '椒盐噪点',
                'name': 'salt-pepper',
                'seed': 'noise-salt-002',
                'params': {'noise_type': 'salt_pepper', 'intensity': 0.2, 'quality': 90}
            },
            {
                'title': '泊松噪点',
                'name': 'poisson',
                'seed': 'noise-poisson-003',
                'params': {'noise_type': 'poisson', 'intensity': 0.4, 'quality': 90}
            }
        ]

        for example in examples:
            self.total_count += 1
            try:
                # 下载原图
                original_image = download_random_image(seed=example['seed'])

                # 上传原图
                orig_key = f"noise/original-{example['name']}.jpg"
                upload_to_oss(original_image, orig_key)

                # 处理噪点效果
                print(f"🌪️ 处理噪点效果: {example['title']}")
                noisy_image = NoiseService.add_noise(original_image, **example['params'])

                # 上传噪点结果
                result_key = f"noise/noise-{example['name']}.jpg"
                result_url = upload_to_oss(noisy_image, result_key)

                if result_url:
                    print(f"✅ Noise示例完成: {example['title']}")
                    self.success_count += 1

            except Exception as e:
                print(f"❌ Noise示例失败: {example['title']} - {e}")

    def generate_pixelate_examples(self):
        """生成pixelate页面示例"""
        print("\n🔲 生成Pixelate页面示例...")

        examples = [
            {
                'title': '轻度像素化',
                'name': 'light',
                'seed': 'pixelate-light-001',
                'params': {'pixel_size': 8, 'quality': 90}
            },
            {
                'title': '中度像素化',
                'name': 'medium',
                'seed': 'pixelate-medium-002',
                'params': {'pixel_size': 16, 'quality': 90}
            },
            {
                'title': '重度像素化',
                'name': 'heavy',
                'seed': 'pixelate-heavy-003',
                'params': {'pixel_size': 32, 'quality': 90}
            }
        ]

        for example in examples:
            self.total_count += 1
            try:
                # 下载原图
                original_image = download_random_image(seed=example['seed'])

                # 上传原图
                orig_key = f"pixelate/original-{example['name']}.jpg"
                upload_to_oss(original_image, orig_key)

                # 处理像素化效果
                print(f"🔲 处理像素化效果: {example['title']}")
                pixelated_image = PixelateService.pixelate_full(
                    original_image,
                    pixel_size=example['params']['pixel_size'],
                    quality=example['params']['quality']
                )

                # 上传像素化结果
                result_key = f"pixelate/pixelate-{example['name']}.jpg"
                result_url = upload_to_oss(pixelated_image, result_key)

                if result_url:
                    print(f"✅ Pixelate示例完成: {example['title']}")
                    self.success_count += 1

            except Exception as e:
                print(f"❌ Pixelate示例失败: {example['title']} - {e}")

    def generate_color_examples(self):
        """生成color页面示例"""
        print("\n🎨 生成Color页面示例...")

        examples = [
            {
                'title': '亮度调整',
                'name': 'brightness',
                'seed': 'color-bright-001',
                'params': {'adjustment_type': 'brightness', 'value': 1.3, 'quality': 90}
            },
            {
                'title': '对比度调整',
                'name': 'contrast',
                'seed': 'color-contrast-002',
                'params': {'adjustment_type': 'contrast', 'value': 1.4, 'quality': 90}
            },
            {
                'title': '饱和度调整',
                'name': 'saturation',
                'seed': 'color-sat-003',
                'params': {'adjustment_type': 'saturation', 'value': 1.5, 'quality': 90}
            }
        ]

        for example in examples:
            self.total_count += 1
            try:
                # 下载原图
                original_image = download_random_image(seed=example['seed'])

                # 上传原图
                orig_key = f"color/original-{example['name']}.jpg"
                upload_to_oss(original_image, orig_key)

                # 处理色彩调整
                print(f"🎨 处理色彩调整: {example['title']}")
                # ColorService.adjust_color expects individual parameters, not a dict
                if example['params']['adjustment_type'] == 'brightness':
                    adjusted_image = ColorService.adjust_color(original_image, brightness=example['params']['value']-1.0, quality=example['params']['quality'])
                elif example['params']['adjustment_type'] == 'contrast':
                    adjusted_image = ColorService.adjust_color(original_image, contrast=example['params']['value']-1.0, quality=example['params']['quality'])
                elif example['params']['adjustment_type'] == 'saturation':
                    adjusted_image = ColorService.adjust_color(original_image, saturation=example['params']['value']-1.0, quality=example['params']['quality'])
                else:
                    adjusted_image = ColorService.adjust_color(original_image, quality=example['params']['quality'])

                # 上传调整结果
                result_key = f"color/color-{example['name']}.jpg"
                result_url = upload_to_oss(adjusted_image, result_key)

                if result_url:
                    print(f"✅ Color示例完成: {example['title']}")
                    self.success_count += 1

            except Exception as e:
                print(f"❌ Color示例失败: {example['title']} - {e}")

    def generate_text_examples(self):
        """生成text页面示例"""
        print("\n📝 生成Text页面示例...")

        examples = [
            {
                'title': '简单文字',
                'name': 'simple',
                'seed': 'text-simple-001',
                'params': {'text': 'Hello World', 'font_size': 48, 'color': '#FFFFFF', 'position': 'center', 'quality': 90}
            },
            {
                'title': '带阴影文字',
                'name': 'shadow',
                'seed': 'text-shadow-002',
                'params': {'text': 'Shadow Text', 'font_size': 56, 'color': '#FF6B6B', 'shadow': True, 'position': 'center', 'quality': 90}
            },
            {
                'title': '描边文字',
                'name': 'stroke',
                'seed': 'text-stroke-003',
                'params': {'text': 'Stroke Text', 'font_size': 52, 'color': '#4ECDC4', 'stroke': True, 'stroke_width': 3, 'position': 'center', 'quality': 90}
            }
        ]

        for example in examples:
            self.total_count += 1
            try:
                # 下载原图
                original_image = download_random_image(seed=example['seed'])

                # 上传原图
                orig_key = f"text/original-{example['name']}.jpg"
                upload_to_oss(original_image, orig_key)

                # 处理文字添加
                print(f"📝 处理文字添加: {example['title']}")
                text_image = TextService.add_text(
                    original_image,
                    text=example['params']['text'],
                    position=example['params']['position'],
                    font_size=example['params']['font_size'],
                    font_color=example['params']['color'],
                    quality=example['params']['quality']
                )

                # 上传文字结果
                result_key = f"text/text-{example['name']}.jpg"
                result_url = upload_to_oss(text_image, result_key)

                if result_url:
                    print(f"✅ Text示例完成: {example['title']}")
                    self.success_count += 1

            except Exception as e:
                print(f"❌ Text示例失败: {example['title']} - {e}")

    def generate_annotation_examples(self):
        """生成annotation页面示例"""
        print("\n📍 生成Annotation页面示例...")

        examples = [
            {
                'title': '矩形标注',
                'name': 'rectangle',
                'seed': 'annotation-rect-001',
                'params': {'annotation_type': 'rectangle', 'x': 200, 'y': 300, 'width': 400, 'height': 300, 'color': '#FF0000', 'quality': 90}
            },
            {
                'title': '圆形标注',
                'name': 'circle',
                'seed': 'annotation-circle-002',
                'params': {'annotation_type': 'circle', 'x': 540, 'y': 960, 'radius': 150, 'color': '#00FF00', 'quality': 90}
            },
            {
                'title': '箭头标注',
                'name': 'arrow',
                'seed': 'annotation-arrow-003',
                'params': {'annotation_type': 'arrow', 'start_x': 200, 'start_y': 400, 'end_x': 600, 'end_y': 800, 'color': '#0000FF', 'quality': 90}
            }
        ]

        for example in examples:
            self.total_count += 1
            try:
                # 下载原图
                original_image = download_random_image(seed=example['seed'])

                # 上传原图
                orig_key = f"annotation/original-{example['name']}.jpg"
                upload_to_oss(original_image, orig_key)

                # 处理标注添加
                print(f"📍 处理标注添加: {example['title']}")
                # Convert parameters to the format expected by AnnotationService
                params = example['params'].copy()
                if 'x' in params and 'y' in params:
                    if 'width' in params and 'height' in params:
                        # Rectangle annotation
                        position = f"{params['x']},{params['y']},{params['width']},{params['height']}"
                    elif 'radius' in params:
                        # Circle annotation
                        position = f"{params['x']},{params['y']},{params['radius']}"
                    elif 'start_x' in params:
                        # Arrow annotation
                        position = f"{params['start_x']},{params['start_y']},{params['end_x']},{params['end_y']}"
                    else:
                        position = f"{params['x']},{params['y']}"

                    annotated_image = AnnotationService.add_annotation(
                        original_image,
                        annotation_type=params['annotation_type'],
                        color=params['color'],
                        position=position,
                        quality=params['quality']
                    )
                else:
                    annotated_image = AnnotationService.add_annotation(original_image, **params)

                # 上传标注结果
                result_key = f"annotation/annotation-{example['name']}.jpg"
                result_url = upload_to_oss(annotated_image, result_key)

                if result_url:
                    print(f"✅ Annotation示例完成: {example['title']}")
                    self.success_count += 1

            except Exception as e:
                print(f"❌ Annotation示例失败: {example['title']} - {e}")

    def generate_format_examples(self):
        """生成format页面示例"""
        print("\n🔄 生成Format页面示例...")

        examples = [
            {
                'title': 'JPEG转PNG',
                'name': 'jpg-to-png',
                'seed': 'format-jpg-001',
                'params': {'target_format': 'PNG', 'quality': 90}
            },
            {
                'title': 'PNG转WEBP',
                'name': 'png-to-webp',
                'seed': 'format-png-002',
                'params': {'target_format': 'WEBP', 'quality': 85}
            },
            {
                'title': 'WEBP转JPEG',
                'name': 'webp-to-jpg',
                'seed': 'format-webp-003',
                'params': {'target_format': 'JPEG', 'quality': 90}
            }
        ]

        for example in examples:
            self.total_count += 1
            try:
                # 下载原图
                original_image = download_random_image(seed=example['seed'])

                # 上传原图
                orig_key = f"format/original-{example['name']}.jpg"
                upload_to_oss(original_image, orig_key)

                # 处理格式转换
                print(f"🔄 处理格式转换: {example['title']}")
                converted_image = FormatService.convert_format(original_image, **example['params'])

                # 上传转换结果
                ext = example['params']['target_format'].lower()
                if ext == 'jpeg':
                    ext = 'jpg'
                result_key = f"format/format-{example['name']}.{ext}"
                result_url = upload_to_oss(converted_image, result_key)

                if result_url:
                    print(f"✅ Format示例完成: {example['title']}")
                    self.success_count += 1

            except Exception as e:
                print(f"❌ Format示例失败: {example['title']} - {e}")

    def generate_gif_examples(self):
        """生成gif页面示例"""
        print("\n🎬 生成GIF页面示例...")

        examples = [
            {
                'title': '图片转GIF',
                'name': 'images-to-gif',
                'seeds': ['gif-frame1-001', 'gif-frame2-001', 'gif-frame3-001'],
                'params': {'duration': 500, 'loop': 0, 'quality': 90}
            },
            {
                'title': '快速GIF',
                'name': 'fast-gif',
                'seeds': ['gif-fast1-002', 'gif-fast2-002'],
                'params': {'duration': 200, 'loop': 0, 'quality': 85}
            }
        ]

        for example in examples:
            self.total_count += 1
            try:
                # 下载多张图片作为帧
                frames = []
                for i, seed in enumerate(example['seeds']):
                    frame_bytes = download_random_image(seed=seed, width=540, height=540)  # GIF使用正方形
                    frames.append(frame_bytes)

                    # 上传原始帧
                    frame_key = f"gif/frame-{example['name']}-{i+1}.jpg"
                    upload_to_oss(frame_bytes, frame_key)

                # 处理GIF生成
                print(f"🎬 处理GIF生成: {example['title']}")
                # Convert bytes to PIL Images first
                from PIL import Image
                import io
                pil_frames = []
                for frame_bytes in frames:
                    pil_frames.append(Image.open(io.BytesIO(frame_bytes)))

                gif_bytes = GifService.images_to_gif(
                    pil_frames,
                    duration=example['params']['duration'],
                    loop=example['params']['loop']
                )

                # 上传GIF结果
                result_key = f"gif/gif-{example['name']}.gif"
                result_url = upload_to_oss(gif_bytes, result_key)

                if result_url:
                    print(f"✅ GIF示例完成: {example['title']}")
                    self.success_count += 1

            except Exception as e:
                print(f"❌ GIF示例失败: {example['title']} - {e}")

def main():
    """主函数"""
    print("🚀 开始批量生成所有剩余页面示例图片...")

    generator = BatchExampleGenerator()

    # 生成各页面示例
    generator.generate_blend_examples()
    generator.generate_stitch_examples()
    generator.generate_overlay_examples()
    generator.generate_mask_examples()
    generator.generate_noise_examples()
    generator.generate_pixelate_examples()
    generator.generate_color_examples()
    generator.generate_text_examples()
    generator.generate_annotation_examples()
    generator.generate_format_examples()
    generator.generate_gif_examples()

    # 输出统计信息
    print(f"\n📊 生成完成统计:")
    print(f"   总任务数: {generator.total_count}")
    print(f"   成功数: {generator.success_count}")
    print(f"   失败数: {generator.total_count - generator.success_count}")
    print(f"   成功率: {generator.success_count/generator.total_count*100:.1f}%")

    print("\n🎉 批量示例生成完成！")

if __name__ == "__main__":
    main()
