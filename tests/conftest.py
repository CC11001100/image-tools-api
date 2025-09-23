import pytest
import io
from PIL import Image
import numpy as np
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """创建测试客户端"""
    return TestClient(app)


@pytest.fixture
def test_image_bytes():
    """创建测试用的图片字节数据"""
    # 创建一个100x100的红色图片
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes.getvalue()


@pytest.fixture
def test_image_rgba_bytes():
    """创建测试用的RGBA图片字节数据"""
    # 创建一个100x100的半透明蓝色图片
    img = Image.new('RGBA', (100, 100), color=(0, 0, 255, 128))
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes.getvalue()


@pytest.fixture
def test_image_file(test_image_bytes):
    """创建测试用的图片文件对象"""
    return io.BytesIO(test_image_bytes)


@pytest.fixture
def test_large_image_bytes():
    """创建测试用的大图片字节数据"""
    # 创建一个1000x1000的渐变图片
    img_array = np.zeros((1000, 1000, 3), dtype=np.uint8)
    for i in range(1000):
        for j in range(1000):
            img_array[i, j] = [i % 256, j % 256, (i + j) % 256]
    
    img = Image.fromarray(img_array)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes.getvalue() 