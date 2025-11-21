#!/bin/bash

# .gitignore管理工具
# 提供验证、清理、优化.gitignore文件的功能

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m'

print_header() {
    echo -e "${PURPLE}$1${NC}"
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
    echo -e "${CYAN}🔍 $1${NC}"
}

# 显示帮助信息
show_help() {
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  validate    验证.gitignore文件"
    echo "  cleanup     清理重复规则"
    echo "  optimize    优化.gitignore文件"
    echo "  status      显示git状态"
    echo "  help        显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 validate   # 验证.gitignore文件"
    echo "  $0 cleanup    # 清理重复规则"
    echo "  $0 optimize   # 完整优化"
}

# 验证.gitignore文件
validate_gitignore() {
    print_header "🔍 验证.gitignore文件"
    
    if [ -f "scripts/validate_gitignore.sh" ]; then
        ./scripts/validate_gitignore.sh
    else
        print_error "验证脚本不存在: scripts/validate_gitignore.sh"
        return 1
    fi
}

# 清理重复规则
cleanup_duplicates() {
    print_header "🧹 清理重复规则"
    
    if [ -f "scripts/cleanup_gitignore_duplicates.py" ]; then
        python scripts/cleanup_gitignore_duplicates.py
    else
        print_error "清理脚本不存在: scripts/cleanup_gitignore_duplicates.py"
        return 1
    fi
}

# 清理被跟踪的忽略文件
cleanup_tracked_files() {
    print_header "🗑️ 清理被跟踪的忽略文件"
    
    if [ -f "scripts/cleanup_ignored_files.sh" ]; then
        ./scripts/cleanup_ignored_files.sh
    else
        print_error "清理脚本不存在: scripts/cleanup_ignored_files.sh"
        return 1
    fi
}

# 优化.gitignore文件
optimize_gitignore() {
    print_header "⚡ 优化.gitignore文件"
    
    echo "执行完整优化流程..."
    echo ""
    
    # 1. 清理重复规则
    print_info "步骤 1: 清理重复规则"
    if cleanup_duplicates; then
        print_success "重复规则清理完成"
    else
        print_warning "重复规则清理失败"
    fi
    
    echo ""
    
    # 2. 验证文件
    print_info "步骤 2: 验证.gitignore文件"
    if validate_gitignore; then
        print_success "验证通过"
    else
        print_warning "验证发现问题"
    fi
    
    echo ""
    
    # 3. 显示git状态
    print_info "步骤 3: 显示git状态"
    show_git_status
    
    echo ""
    print_success "🎉 优化完成！"
}

# 显示git状态
show_git_status() {
    print_header "📊 Git状态"
    
    # 检查是否在git仓库中
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "当前目录不是git仓库"
        return 1
    fi
    
    # 显示修改的文件
    print_info "修改的文件:"
    local modified_files
    modified_files=$(git status --porcelain | grep "^M" | head -10)
    if [ -n "$modified_files" ]; then
        echo "$modified_files" | sed 's/^/  /'
    else
        echo "  无修改文件"
    fi
    
    echo ""
    
    # 显示未跟踪的文件
    print_info "未跟踪的文件:"
    local untracked_files
    untracked_files=$(git ls-files --others --exclude-standard | head -10)
    if [ -n "$untracked_files" ]; then
        echo "$untracked_files" | sed 's/^/  /'
        
        local total_untracked
        total_untracked=$(git ls-files --others --exclude-standard | wc -l)
        if [ "$total_untracked" -gt 10 ]; then
            echo "  ... 还有 $((total_untracked - 10)) 个文件"
        fi
    else
        echo "  无未跟踪文件"
    fi
    
    echo ""
    
    # 显示.gitignore状态
    print_info ".gitignore文件状态:"
    if git status --porcelain | grep -q ".gitignore"; then
        echo "  .gitignore 已修改"
    else
        echo "  .gitignore 无变化"
    fi
}

# 显示.gitignore统计信息
show_statistics() {
    print_header "📈 .gitignore统计信息"
    
    if [ ! -f ".gitignore" ]; then
        print_error ".gitignore文件不存在"
        return 1
    fi
    
    local total_lines
    total_lines=$(wc -l < .gitignore)
    
    local comment_lines
    comment_lines=$(grep -c "^#" .gitignore || echo "0")
    
    local empty_lines
    empty_lines=$(grep -c "^$" .gitignore || echo "0")
    
    local rule_lines
    rule_lines=$((total_lines - comment_lines - empty_lines))
    
    echo "文件统计:"
    echo "  总行数: $total_lines"
    echo "  注释行: $comment_lines"
    echo "  空行: $empty_lines"
    echo "  规则行: $rule_lines"
    
    echo ""
    echo "文件大小: $(du -h .gitignore | cut -f1)"
    echo "最后修改: $(stat -f "%Sm" .gitignore 2>/dev/null || stat -c "%y" .gitignore 2>/dev/null || echo "未知")"
}

# 主函数
main() {
    local action=${1:-help}
    
    case "$action" in
        "validate")
            validate_gitignore
            ;;
        "cleanup")
            cleanup_duplicates
            ;;
        "cleanup-files")
            cleanup_tracked_files
            ;;
        "optimize")
            optimize_gitignore
            ;;
        "status")
            show_git_status
            ;;
        "stats")
            show_statistics
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            print_error "未知选项: $action"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# 运行主函数
main "$@"
