#!/usr/bin/env python3
"""
分析接口模式和命名一致性
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app.main import app
import inspect

def analyze_interface_patterns():
    """分析接口模式"""
    print("🔍 分析接口模式和命名一致性")
    print("=" * 80)
    
    # 收集所有接口信息
    interfaces = []
    
    for route in app.routes:
        if hasattr(route, 'path') and hasattr(route, 'methods') and hasattr(route, 'endpoint'):
            path = route.path
            methods = list(route.methods)
            endpoint = route.endpoint
            
            # 只关注POST接口
            if 'POST' in methods and path.startswith('/api/v1/'):
                # 获取函数签名
                sig = inspect.signature(endpoint)
                params = list(sig.parameters.keys())
                
                interfaces.append({
                    'path': path,
                    'endpoint_name': endpoint.__name__,
                    'params': params,
                    'has_file_param': any('file' in p.lower() for p in params),
                    'has_url_param': any('url' in p.lower() for p in params),
                    'has_request_body': any('request' in p.lower() for p in params)
                })
    
    # 分析模式
    print(f"\n📋 接口分析结果:")
    
    file_upload_only = []
    url_only = []
    mixed_interfaces = []
    inconsistent_naming = []
    
    for interface in sorted(interfaces, key=lambda x: x['path']):
        path = interface['path']
        has_file = interface['has_file_param']
        has_url = interface['has_url_param']
        has_request = interface['has_request_body']
        
        # 分类接口
        if has_file and not has_url and not has_request:
            file_upload_only.append(interface)
        elif (has_url or has_request) and not has_file:
            url_only.append(interface)
        elif has_file and (has_url or has_request):
            mixed_interfaces.append(interface)
        
        # 检查命名一致性
        if has_url or has_request:
            if '-by-url' not in path:
                inconsistent_naming.append(interface)
        
        # 打印详细信息
        type_indicators = []
        if has_file:
            type_indicators.append("📁文件")
        if has_url:
            type_indicators.append("🔗URL")
        if has_request:
            type_indicators.append("📝请求体")
        
        type_str = " + ".join(type_indicators) if type_indicators else "❓未知"
        
        print(f"  {path}")
        print(f"    类型: {type_str}")
        print(f"    参数: {', '.join(interface['params'][:5])}{'...' if len(interface['params']) > 5 else ''}")
        
        if '-by-url' not in path and (has_url or has_request):
            print(f"    ⚠️  命名不一致：URL接口但路径无-by-url后缀")
        
        print()
    
    # 生成总结
    print("=" * 80)
    print("📊 模式分析总结")
    print("=" * 80)
    
    print(f"纯文件上传接口: {len(file_upload_only)}")
    print(f"纯URL接口: {len(url_only)}")
    print(f"混合接口: {len(mixed_interfaces)}")
    print(f"命名不一致接口: {len(inconsistent_naming)}")
    
    if inconsistent_naming:
        print(f"\n❌ 命名不一致的接口:")
        for interface in inconsistent_naming:
            print(f"  - {interface['path']} ({interface['endpoint_name']})")
    
    # 检查配对情况
    print(f"\n🔍 配对分析:")
    
    base_interfaces = {}
    url_interfaces = {}
    
    for interface in interfaces:
        path = interface['path']
        if '-by-url' in path:
            base_path = path.replace('-by-url', '')
            url_interfaces[base_path] = interface
        else:
            base_interfaces[path] = interface
    
    missing_pairs = []
    for base_path, base_interface in base_interfaces.items():
        if base_interface['has_file_param'] and base_path not in url_interfaces:
            # 检查是否是特殊情况（如video-to-gif）
            if not (base_interface['has_url_param'] or base_interface['has_request_body']):
                missing_pairs.append(base_path)
    
    if missing_pairs:
        print(f"  缺少URL版本的文件接口: {len(missing_pairs)}")
        for path in missing_pairs:
            print(f"    - {path}")
    else:
        print(f"  ✅ 所有文件接口都有对应的URL版本")
    
    return {
        'total_interfaces': len(interfaces),
        'file_upload_only': len(file_upload_only),
        'url_only': len(url_only),
        'mixed_interfaces': len(mixed_interfaces),
        'inconsistent_naming': len(inconsistent_naming),
        'missing_pairs': len(missing_pairs)
    }

if __name__ == "__main__":
    result = analyze_interface_patterns()
    
    # 返回退出码
    if result['inconsistent_naming'] > 0 or result['missing_pairs'] > 0:
        print(f"\n⚠️  发现 {result['inconsistent_naming']} 个命名不一致和 {result['missing_pairs']} 个缺失配对")
        sys.exit(1)
    else:
        print(f"\n✅ 所有接口命名一致且配对完整")
        sys.exit(0)
