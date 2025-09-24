#!/usr/bin/env python3
"""
追踪请求脚本 - 详细追踪-test接口的请求处理过程
"""

import requests
import json
from urllib.parse import urlparse

def trace_test_request():
    """追踪test接口请求"""
    base_url = "http://localhost:58888"
    
    # 测试一个已知存在的正式接口
    print("🔍 测试正式接口:")
    test_formal_url = f"{base_url}/api/v1/watermark-by-url"
    try:
        response = requests.post(test_formal_url, json={"image_url": "test"}, timeout=5)
        print(f"  正式接口状态: {response.status_code}")
        print(f"  响应头: {dict(response.headers)}")
        if response.text:
            print(f"  响应内容: {response.text[:200]}...")
    except Exception as e:
        print(f"  正式接口错误: {e}")
    
    print("\n🔍 测试test接口:")
    test_url = f"{base_url}/api/v1/watermark-by-url-test"
    try:
        response = requests.post(test_url, json={"image_url": "test"}, timeout=5)
        print(f"  Test接口状态: {response.status_code}")
        print(f"  响应头: {dict(response.headers)}")
        if response.text:
            print(f"  响应内容: {response.text[:200]}...")
        
        # 检查是否有重定向
        if response.history:
            print(f"  重定向历史: {[r.url for r in response.history]}")
        
    except Exception as e:
        print(f"  Test接口错误: {e}")
    
    # 测试OPTIONS请求
    print("\n🔍 测试OPTIONS请求:")
    try:
        response = requests.options(test_url, timeout=5)
        print(f"  OPTIONS状态: {response.status_code}")
        print(f"  允许的方法: {response.headers.get('Allow', 'N/A')}")
    except Exception as e:
        print(f"  OPTIONS错误: {e}")
    
    # 测试HEAD请求
    print("\n🔍 测试HEAD请求:")
    try:
        response = requests.head(test_url, timeout=5)
        print(f"  HEAD状态: {response.status_code}")
    except Exception as e:
        print(f"  HEAD错误: {e}")

def check_server_routes():
    """检查服务器路由信息"""
    print("\n🔍 检查服务器路由信息:")
    base_url = "http://localhost:58888"
    
    try:
        # 获取OpenAPI规范
        response = requests.get(f"{base_url}/openapi.json", timeout=5)
        if response.status_code == 200:
            openapi_spec = response.json()
            paths = openapi_spec.get('paths', {})
            
            test_paths = []
            normal_paths = []
            
            for path in paths.keys():
                if 'test' in path.lower():
                    test_paths.append(path)
                else:
                    normal_paths.append(path)
            
            print(f"  OpenAPI中的路径总数: {len(paths)}")
            print(f"  包含'test'的路径: {len(test_paths)}")
            
            if test_paths:
                print("  Test路径列表:")
                for path in sorted(test_paths):
                    print(f"    - {path}")
            else:
                print("  ✅ OpenAPI规范中没有test路径")
                
        else:
            print(f"  无法获取OpenAPI规范: {response.status_code}")
            
    except Exception as e:
        print(f"  检查OpenAPI规范错误: {e}")

def test_url_patterns():
    """测试URL模式匹配"""
    print("\n🔍 测试URL模式匹配:")
    base_url = "http://localhost:58888"
    
    test_patterns = [
        "/api/v1/watermark-by-url-test",
        "/api/v1/watermark-by-url-test/",
        "/api/v1/watermark-by-url-test?param=1",
        "/api/v1/watermark-by-url-test#fragment",
        "/api/v1/WATERMARK-BY-URL-TEST",  # 大写测试
    ]
    
    for pattern in test_patterns:
        print(f"\n  测试模式: {pattern}")
        try:
            response = requests.post(f"{base_url}{pattern}", 
                                   json={"image_url": "test"}, 
                                   timeout=5,
                                   allow_redirects=False)
            print(f"    状态码: {response.status_code}")
            if response.status_code in [301, 302, 307, 308]:
                print(f"    重定向到: {response.headers.get('Location', 'N/A')}")
        except Exception as e:
            print(f"    错误: {e}")

if __name__ == "__main__":
    trace_test_request()
    check_server_routes()
    test_url_patterns()
