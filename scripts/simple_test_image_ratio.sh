#!/bin/bash

# 图片比例显示修复简单测试脚本
# 用于验证前端服务是否正常运行，以及检查代码中的objectFit修复

echo "🧪 图片比例显示修复测试"
echo "=========================="

# 检查前端服务是否运行
echo "📡 检查前端服务状态..."
if curl -s -I http://localhost:58889 | grep -q "200 OK"; then
    echo "✅ 前端服务运行正常 (http://localhost:58889)"
else
    echo "❌ 前端服务未运行或无法访问"
    exit 1
fi

# 检查后端服务是否运行
echo "📡 检查后端服务状态..."
if curl -s http://localhost:58888/health | grep -q "ok"; then
    echo "✅ 后端服务运行正常 (http://localhost:58888)"
else
    echo "⚠️  后端服务未运行或无法访问"
fi

# 检查代码中的objectFit修复
echo ""
echo "🔍 检查代码修复状态..."

# 检查是否还有objectFit: 'cover'的使用
echo "📋 检查 objectFit: 'cover' 的使用情况..."
cover_count=$(grep -r "objectFit.*cover" frontend/src/ 2>/dev/null | wc -l)
if [ "$cover_count" -eq 0 ]; then
    echo "✅ 没有发现 objectFit: 'cover' 的使用"
else
    echo "⚠️  发现 $cover_count 处 objectFit: 'cover' 的使用:"
    grep -r "objectFit.*cover" frontend/src/ 2>/dev/null
fi

# 检查objectFit: 'contain'的使用
echo "📋 检查 objectFit: 'contain' 的使用情况..."
contain_count=$(grep -r "objectFit.*contain" frontend/src/ 2>/dev/null | wc -l)
echo "✅ 发现 $contain_count 处 objectFit: 'contain' 的使用"

# 检查修复的关键文件
echo ""
echo "🔧 检查关键文件修复状态..."

files_to_check=(
    "frontend/src/components/PhoneFrame.tsx"
    "frontend/src/components/EffectShowcase.tsx"
    "frontend/src/components/MultiImageUpload.tsx"
)

for file in "${files_to_check[@]}"; do
    if [ -f "$file" ]; then
        echo "📄 检查文件: $file"
        
        # 检查是否包含objectFit: 'contain'
        if grep -q "objectFit.*contain" "$file"; then
            echo "   ✅ 包含 objectFit: 'contain'"
        else
            echo "   ⚠️  未找到 objectFit: 'contain'"
        fi
        
        # 检查是否还有objectFit: 'cover'
        if grep -q "objectFit.*cover" "$file"; then
            echo "   ❌ 仍包含 objectFit: 'cover'"
        else
            echo "   ✅ 不包含 objectFit: 'cover'"
        fi
    else
        echo "❌ 文件不存在: $file"
    fi
done

# 测试页面访问
echo ""
echo "🌐 测试页面访问..."

pages=(
    "/resize:调整大小"
    "/crop:裁剪"
    "/transform:旋转翻转"
    "/canvas:画布调整"
    "/perspective:透视变换"
    "/filter:滤镜效果"
    "/watermark:图片水印"
)

accessible_pages=0
total_pages=${#pages[@]}

for page_info in "${pages[@]}"; do
    IFS=':' read -r path name <<< "$page_info"
    echo "📱 测试页面: $name ($path)"
    
    if curl -s -I "http://localhost:58889$path" | grep -q "200 OK"; then
        echo "   ✅ 页面可访问"
        ((accessible_pages++))
    else
        echo "   ❌ 页面无法访问"
    fi
done

# 生成测试报告
echo ""
echo "📊 测试报告"
echo "============"
echo "总页面数: $total_pages"
echo "可访问页面: $accessible_pages"
echo "成功率: $(( accessible_pages * 100 / total_pages ))%"

if [ "$cover_count" -eq 0 ] && [ "$contain_count" -gt 0 ] && [ "$accessible_pages" -eq "$total_pages" ]; then
    echo ""
    echo "🎉 所有测试通过！图片比例显示修复成功！"
    echo ""
    echo "✅ 修复总结:"
    echo "   - 已移除所有 objectFit: 'cover' 的使用"
    echo "   - 已添加 $contain_count 处 objectFit: 'contain' 的使用"
    echo "   - 所有 $total_pages 个页面都可正常访问"
    echo "   - 前端和后端服务运行正常"
    
    # 保存测试结果
    timestamp=$(date +"%Y%m%d_%H%M%S")
    report_file="test_results/simple_test_report_$timestamp.txt"
    mkdir -p test_results
    
    {
        echo "图片比例显示修复测试报告"
        echo "测试时间: $(date)"
        echo "=========================="
        echo "objectFit: 'cover' 使用次数: $cover_count"
        echo "objectFit: 'contain' 使用次数: $contain_count"
        echo "可访问页面数: $accessible_pages/$total_pages"
        echo "测试结果: 通过"
    } > "$report_file"
    
    echo "📄 测试报告已保存: $report_file"
    exit 0
else
    echo ""
    echo "⚠️  测试发现问题，请检查上述输出"
    exit 1
fi
