#!/bin/bash

# 清理应该被.gitignore忽略的文件
# 这个脚本会删除项目中应该被忽略但已经被跟踪的文件

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "${BLUE}$1${NC}"
    echo "=================================================="
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}🔍 $1${NC}"
}

# 检查是否在git仓库中
check_git_repo() {
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "当前目录不是git仓库"
        exit 1
    fi
}

# 备份重要文件
backup_important_files() {
    print_info "备份重要文件..."
    
    local backup_dir="backup_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    
    # 备份可能有用的测试报告
    if [ -f "test_report.json" ]; then
        cp "test_report.json" "$backup_dir/"
        print_success "备份 test_report.json"
    fi
    
    if [ -f "image_load_test_report.json" ]; then
        cp "image_load_test_report.json" "$backup_dir/"
        print_success "备份 image_load_test_report.json"
    fi
    
    if [ -f "frontend_config_test_results.json" ]; then
        cp "frontend_config_test_results.json" "$backup_dir/"
        print_success "备份 frontend_config_test_results.json"
    fi
    
    echo "备份目录: $backup_dir"
}

# 删除测试文件
cleanup_test_files() {
    print_info "清理测试文件..."
    
    local test_files=(
        "complete_api_test.py"
        "complete_test.py"
        "comprehensive_all_endpoints_test.py"
        "comprehensive_api_test.py"
        "final_comprehensive_test.py"
        "final_test.py"
        "final_test_report.py"
        "quick_test.py"
        "test_all_api_formats.py"
        "test_all_endpoints.sh"
        "test_api_responses.py"
        "test_api_simple.sh"
        "test_deployment.sh"
        "test_deployment_verification.py"
        "test_enhanced_watermark.py"
        "test_enhanced_watermark_comprehensive.py"
        "test_final_deployment.py"
        "test_final_enhanced_watermark.py"
        "test_final_verification.js"
        "test_production_deployment.py"
        "test_production_final.py"
        "test_resize_api.py"
        "test_resize_api.sh"
        "test_simple_verification.py"
        "test_simple_watermark.py"
        "test_tile_watermark.py"
        "test_prod.py"
        "test_all_image_composition_pages.js"
        "test_footer_implementation.js"
        "test_git_and_final_status.js"
        "test_multi_image_phone_frame.js"
        "test_overlay_functionality.js"
        "test_production_deployment.js"
        "test_qr_size_update.js"
        "test_wechat_qr_update.js"
    )
    
    for file in "${test_files[@]}"; do
        if [ -f "$file" ]; then
            rm "$file"
            print_success "删除 $file"
        fi
    done
}

# 删除测试输出文件
cleanup_test_outputs() {
    print_info "清理测试输出文件..."
    
    local output_files=(
        "watermark_test_output.jpg"
        "test_report.json"
        "test_report.md"
        "frontend_config_test_results.json"
        "image_load_test_report.json"
    )
    
    for file in "${output_files[@]}"; do
        if [ -f "$file" ]; then
            rm "$file"
            print_success "删除 $file"
        fi
    done
}

# 删除虚拟环境目录
cleanup_venv_dirs() {
    print_info "清理虚拟环境目录..."
    
    local venv_dirs=(
        "venv_playwright"
    )
    
    for dir in "${venv_dirs[@]}"; do
        if [ -d "$dir" ]; then
            rm -rf "$dir"
            print_success "删除目录 $dir"
        fi
    done
}

# 删除缓存目录
cleanup_cache_dirs() {
    print_info "清理缓存目录..."
    
    local cache_dirs=(
        ".pytest_cache"
        "__pycache__"
        "*.pyc"
    )
    
    # 删除pytest缓存
    if [ -d ".pytest_cache" ]; then
        rm -rf ".pytest_cache"
        print_success "删除 .pytest_cache"
    fi
    
    # 删除Python缓存
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true
    print_success "删除Python缓存文件"
}

# 更新git索引
update_git_index() {
    print_info "更新git索引..."
    
    # 添加.gitignore的更改
    git add .gitignore
    
    # 从git索引中移除已删除的文件
    git add -u
    
    print_success "git索引已更新"
}

# 显示清理结果
show_cleanup_result() {
    print_info "清理结果..."
    
    echo "当前git状态:"
    git status --porcelain | head -10
    
    echo ""
    echo "剩余的未跟踪文件:"
    git ls-files --others --exclude-standard | head -10
}

# 主函数
main() {
    print_header "🧹 清理.gitignore忽略的文件"
    
    # 检查git仓库
    check_git_repo
    
    # 确认操作
    echo "这个脚本将删除以下类型的文件:"
    echo "  - 测试脚本文件"
    echo "  - 测试输出文件"
    echo "  - 虚拟环境目录"
    echo "  - 缓存目录"
    echo ""
    read -p "确认继续? (y/N): " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_warning "操作已取消"
        exit 0
    fi
    
    # 备份重要文件
    backup_important_files
    
    echo ""
    
    # 执行清理
    cleanup_test_files
    echo ""
    cleanup_test_outputs
    echo ""
    cleanup_venv_dirs
    echo ""
    cleanup_cache_dirs
    echo ""
    
    # 更新git索引
    update_git_index
    echo ""
    
    # 显示结果
    show_cleanup_result
    
    echo ""
    print_success "🎉 清理完成！"
    print_info "建议运行 'git status' 检查更改"
}

# 运行主函数
main "$@"
