#!/bin/bash

# 验证.gitignore文件的有效性
# 检查是否有应该被忽略但仍被跟踪的文件

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
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
    echo -e "${CYAN}🔍 $1${NC}"
}

# 检查是否在git仓库中
check_git_repo() {
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "当前目录不是git仓库"
        exit 1
    fi
}

# 检查.gitignore文件
check_gitignore_exists() {
    if [ ! -f ".gitignore" ]; then
        print_error ".gitignore文件不存在"
        exit 1
    fi
    print_success ".gitignore文件存在"
}

# 检查被跟踪但应该被忽略的文件
check_tracked_ignored_files() {
    print_info "检查被跟踪但应该被忽略的文件..."
    
    local issues_found=0
    
    # 检查测试文件
    local test_patterns=(
        "test_*.py"
        "test_*.js"
        "*_test.py"
        "*_test.js"
        "complete_*.py"
        "comprehensive_*.py"
        "final_*.py"
        "quick_test.py"
    )
    
    for pattern in "${test_patterns[@]}"; do
        local files
        files=$(git ls-files "$pattern" 2>/dev/null || true)
        if [ -n "$files" ]; then
            print_warning "发现被跟踪的测试文件: $pattern"
            echo "$files" | sed 's/^/  /'
            issues_found=$((issues_found + 1))
        fi
    done
    
    # 检查日志文件
    local log_files
    log_files=$(git ls-files "*.log" 2>/dev/null || true)
    if [ -n "$log_files" ]; then
        print_warning "发现被跟踪的日志文件:"
        echo "$log_files" | sed 's/^/  /'
        issues_found=$((issues_found + 1))
    fi
    
    # 检查临时文件
    local temp_patterns=(
        "*.tmp"
        "*.temp"
        "temp_*"
        "tmp_*"
    )
    
    for pattern in "${temp_patterns[@]}"; do
        local files
        files=$(git ls-files "$pattern" 2>/dev/null || true)
        if [ -n "$files" ]; then
            print_warning "发现被跟踪的临时文件: $pattern"
            echo "$files" | sed 's/^/  /'
            issues_found=$((issues_found + 1))
        fi
    done
    
    # 检查虚拟环境目录
    local venv_dirs
    venv_dirs=$(git ls-files | grep -E "^venv_|^\.venv/" 2>/dev/null || true)
    if [ -n "$venv_dirs" ]; then
        print_warning "发现被跟踪的虚拟环境文件:"
        echo "$venv_dirs" | sed 's/^/  /'
        issues_found=$((issues_found + 1))
    fi
    
    # 检查缓存目录
    local cache_files
    cache_files=$(git ls-files | grep -E "__pycache__|\.pytest_cache|\.cache" 2>/dev/null || true)
    if [ -n "$cache_files" ]; then
        print_warning "发现被跟踪的缓存文件:"
        echo "$cache_files" | sed 's/^/  /'
        issues_found=$((issues_found + 1))
    fi
    
    if [ $issues_found -eq 0 ]; then
        print_success "没有发现被跟踪但应该被忽略的文件"
    else
        print_warning "发现 $issues_found 类问题文件"
    fi
    
    return $issues_found
}

# 检查未被跟踪的文件
check_untracked_files() {
    print_info "检查未被跟踪的文件..."
    
    local untracked_files
    untracked_files=$(git ls-files --others --exclude-standard)
    
    if [ -z "$untracked_files" ]; then
        print_success "没有未被跟踪的文件"
    else
        print_info "未被跟踪的文件:"
        echo "$untracked_files" | head -20 | sed 's/^/  /'
        
        local count
        count=$(echo "$untracked_files" | wc -l)
        if [ "$count" -gt 20 ]; then
            echo "  ... 还有 $((count - 20)) 个文件"
        fi
    fi
}

# 检查.gitignore规则的有效性
test_gitignore_rules() {
    print_info "测试.gitignore规则的有效性..."
    
    local test_files=(
        "test_sample.py"
        "sample_test.js"
        "temp_file.tmp"
        "debug.log"
        "config.secret.json"
    )
    
    for test_file in "${test_files[@]}"; do
        # 创建测试文件
        touch "$test_file"
        
        # 检查是否被忽略
        if git check-ignore "$test_file" >/dev/null 2>&1; then
            print_success "$test_file 被正确忽略"
        else
            print_warning "$test_file 没有被忽略"
        fi
        
        # 删除测试文件
        rm "$test_file"
    done
}

# 分析.gitignore文件内容
analyze_gitignore_content() {
    print_info "分析.gitignore文件内容..."
    
    local total_lines
    total_lines=$(wc -l < .gitignore)
    print_info "总行数: $total_lines"
    
    local comment_lines
    comment_lines=$(grep -c "^#" .gitignore || echo "0")
    print_info "注释行数: $comment_lines"
    
    local empty_lines
    empty_lines=$(grep -c "^$" .gitignore || echo "0")
    print_info "空行数: $empty_lines"
    
    local rule_lines
    rule_lines=$((total_lines - comment_lines - empty_lines))
    print_info "规则行数: $rule_lines"
    
    # 检查重复规则
    local duplicate_rules
    duplicate_rules=$(grep -v "^#" .gitignore | grep -v "^$" | sort | uniq -d)
    if [ -n "$duplicate_rules" ]; then
        print_warning "发现重复规则:"
        echo "$duplicate_rules" | sed 's/^/  /'
    else
        print_success "没有发现重复规则"
    fi
}

# 提供修复建议
provide_suggestions() {
    print_info "修复建议..."
    
    echo "如果发现问题，可以执行以下操作:"
    echo ""
    echo "1. 清理被跟踪但应该被忽略的文件:"
    echo "   ./scripts/cleanup_ignored_files.sh"
    echo ""
    echo "2. 从git索引中移除特定文件:"
    echo "   git rm --cached <文件名>"
    echo ""
    echo "3. 从git索引中移除目录:"
    echo "   git rm -r --cached <目录名>"
    echo ""
    echo "4. 更新.gitignore后重新应用:"
    echo "   git rm -r --cached ."
    echo "   git add ."
    echo ""
    echo "5. 检查特定文件是否被忽略:"
    echo "   git check-ignore <文件名>"
}

# 主函数
main() {
    print_header "🔍 验证.gitignore文件"
    
    # 检查git仓库
    check_git_repo
    
    # 检查.gitignore文件
    check_gitignore_exists
    
    echo ""
    
    # 分析.gitignore内容
    analyze_gitignore_content
    
    echo ""
    
    # 检查被跟踪但应该被忽略的文件
    local issues=0
    if ! check_tracked_ignored_files; then
        issues=1
    fi
    
    echo ""
    
    # 检查未被跟踪的文件
    check_untracked_files
    
    echo ""
    
    # 测试.gitignore规则
    test_gitignore_rules
    
    echo ""
    
    # 提供建议
    if [ $issues -eq 1 ]; then
        provide_suggestions
        echo ""
    fi
    
    # 总结
    print_header "📊 验证结果"
    if [ $issues -eq 0 ]; then
        print_success "🎉 .gitignore配置正确，没有发现问题！"
    else
        print_warning "⚠️  发现一些问题，请参考上述建议进行修复"
    fi
}

# 运行主函数
main "$@"
