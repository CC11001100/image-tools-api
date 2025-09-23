import os
import uuid
import requests
import json
from typing import Optional
from PIL import Image
import io
import base64
from ..utils.logger import logger

class AITextToImageService:
    def __init__(self):
        self.output_dir = "public/generated"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 这里可以配置不同的AI服务
        # 例如：Stable Diffusion、DALL-E、Midjourney等
        self.api_endpoints = {
            "stable_diffusion": "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
            "huggingface": "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
        }
    
    def enhance_prompt_by_style(self, prompt: str, style: str) -> str:
        """根据风格增强提示词"""
        style_enhancers = {
            "realistic": f"{prompt}, photorealistic, high quality, detailed, professional photography",
            "anime": f"{prompt}, anime style, manga, japanese animation, colorful, detailed",
            "artistic": f"{prompt}, artistic, painting, fine art, masterpiece, detailed",
            "cartoon": f"{prompt}, cartoon style, illustration, colorful, fun, animated",
            "oil_painting": f"{prompt}, oil painting, classical art, brush strokes, artistic",
            "watercolor": f"{prompt}, watercolor painting, soft colors, artistic, flowing"
        }
        
        return style_enhancers.get(style, prompt)
    
    async def generate_with_dummy_service(self, prompt: str, **kwargs) -> str:
        """使用虚拟服务生成图片（用于演示）"""
        # 这是一个演示方法，创建一个带有提示词的简单图片
        from PIL import Image, ImageDraw, ImageFont
        
        width = kwargs.get('width', 512)
        height = kwargs.get('height', 512)
        
        # 创建渐变背景
        image = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(image)
        
        # 创建简单的渐变背景
        for y in range(height):
            ratio = y / height
            r = int(100 * (1 - ratio) + 200 * ratio)
            g = int(150 * (1 - ratio) + 100 * ratio)
            b = int(200 * (1 - ratio) + 150 * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # 添加文字说明
        try:
            font = ImageFont.load_default()
        except:
            font = None
        
        # 添加提示词文本
        text_lines = [
            "AI生成图片演示",
            f"提示词: {prompt[:30]}...",
            "这是演示版本",
            "请配置真实AI服务"
        ]
        
        y_offset = height // 4
        for line in text_lines:
            bbox = draw.textbbox((0, 0), line, font=font) if font else (0, 0, 100, 20)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            draw.text((x, y_offset), line, fill=(255, 255, 255), font=font)
            y_offset += 30
        
        # 保存图片
        filename = f"ai_image_{uuid.uuid4().hex}.png"
        filepath = os.path.join(self.output_dir, filename)
        image.save(filepath, "PNG")
        
        return f"/generated/{filename}"
    
    async def generate_with_huggingface(self, prompt: str, **kwargs) -> str:
        """使用HuggingFace API生成图片"""
        try:
            # 这里需要HuggingFace API密钥
            api_key = os.getenv("HUGGINGFACE_API_KEY")
            if not api_key:
                logger.warning("未配置HuggingFace API密钥，使用演示服务")
                return await self.generate_with_dummy_service(prompt, **kwargs)
            
            headers = {"Authorization": f"Bearer {api_key}"}
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "width": kwargs.get('width', 512),
                    "height": kwargs.get('height', 512),
                    "num_inference_steps": kwargs.get('num_inference_steps', 20),
                    "guidance_scale": kwargs.get('guidance_scale', 7.5),
                }
            }
            
            if kwargs.get('seed'):
                payload["parameters"]["seed"] = kwargs['seed']
            
            response = requests.post(
                self.api_endpoints["huggingface"],
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                # 保存生成的图片
                filename = f"ai_image_{uuid.uuid4().hex}.png"
                filepath = os.path.join(self.output_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                return f"/generated/{filename}"
            else:
                logger.error(f"HuggingFace API错误: {response.status_code}")
                return await self.generate_with_dummy_service(prompt, **kwargs)
                
        except Exception as e:
            logger.error(f"HuggingFace生成失败: {str(e)}")
            return await self.generate_with_dummy_service(prompt, **kwargs)
    
    async def generate_with_stability_ai(self, prompt: str, **kwargs) -> str:
        """使用Stability AI生成图片"""
        try:
            api_key = os.getenv("STABILITY_API_KEY")
            if not api_key:
                logger.warning("未配置Stability AI API密钥，使用演示服务")
                return await self.generate_with_dummy_service(prompt, **kwargs)
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "text_prompts": [
                    {
                        "text": prompt,
                        "weight": 1
                    }
                ],
                "cfg_scale": kwargs.get('guidance_scale', 7.5),
                "height": kwargs.get('height', 512),
                "width": kwargs.get('width', 512),
                "samples": 1,
                "steps": kwargs.get('num_inference_steps', 20),
            }
            
            if kwargs.get('negative_prompt'):
                payload["text_prompts"].append({
                    "text": kwargs['negative_prompt'],
                    "weight": -1
                })
            
            if kwargs.get('seed'):
                payload["seed"] = kwargs['seed']
            
            response = requests.post(
                self.api_endpoints["stable_diffusion"],
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                # 解码base64图片
                image_data = base64.b64decode(data["artifacts"][0]["base64"])
                
                filename = f"ai_image_{uuid.uuid4().hex}.png"
                filepath = os.path.join(self.output_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(image_data)
                
                return f"/generated/{filename}"
            else:
                logger.error(f"Stability AI错误: {response.status_code}")
                return await self.generate_with_dummy_service(prompt, **kwargs)
                
        except Exception as e:
            logger.error(f"Stability AI生成失败: {str(e)}")
            return await self.generate_with_dummy_service(prompt, **kwargs)
    
    async def generate_image(self, prompt: str, negative_prompt: str = "",
                           width: int = 512, height: int = 512,
                           num_inference_steps: int = 20, guidance_scale: float = 7.5,
                           seed: Optional[int] = None, style: str = "realistic") -> str:
        """生成AI图片"""
        
        # 根据风格增强提示词
        enhanced_prompt = self.enhance_prompt_by_style(prompt, style)
        
        kwargs = {
            'width': width,
            'height': height,
            'num_inference_steps': num_inference_steps,
            'guidance_scale': guidance_scale,
            'seed': seed,
            'negative_prompt': negative_prompt
        }
        
        # 尝试不同的AI服务
        # 优先级：Stability AI > HuggingFace > 演示服务
        
        # 首先尝试Stability AI
        if os.getenv("STABILITY_API_KEY"):
            try:
                return await self.generate_with_stability_ai(enhanced_prompt, **kwargs)
            except Exception as e:
                logger.error(f"Stability AI失败，尝试其他服务: {str(e)}")
        
        # 然后尝试HuggingFace
        if os.getenv("HUGGINGFACE_API_KEY"):
            try:
                return await self.generate_with_huggingface(enhanced_prompt, **kwargs)
            except Exception as e:
                logger.error(f"HuggingFace失败，使用演示服务: {str(e)}")
        
        # 最后使用演示服务
        return await self.generate_with_dummy_service(enhanced_prompt, **kwargs) 