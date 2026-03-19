#!/usr/bin/env python3
"""
Security verification script for nutstore-sync
运行安全检查，确保代码符合安全最佳实践
"""

import ast
import sys
import re
from pathlib import Path


def check_hardcoded_credentials(file_path: str) -> list:
    """检查硬编码凭证"""
    issues = []
    content = Path(file_path).read_text(encoding='utf-8')
    
    # 检查常见的凭证模式
    patterns = [
        (r'password\s*=\s*["\'][^"\']+["\']', "可能的硬编码密码"),
        (r'api_key\s*=\s*["\'][^"\']+["\']', "可能的硬编码 API Key"),
        (r'secret\s*=\s*["\'][^"\']+["\']', "可能的硬编码 Secret"),
        (r'token\s*=\s*["\'][^"\']+["\']', "可能的硬编码 Token"),
        (r'username\s*=\s*["\'][^@"\']+@[^"\']+["\']', "可能的硬编码邮箱"),
    ]
    
    for pattern, desc in patterns:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            # 排除配置文件示例和注释
            line = content[:match.start()].count('\n') + 1
            line_content = content.split('\n')[line-1].strip()
            if not line_content.startswith('#') and 'example' not in line_content.lower():
                issues.append(f"行 {line}: {desc}")
    
    return issues


def check_dangerous_functions(file_path: str) -> list:
    """检查危险函数使用"""
    issues = []
    content = Path(file_path).read_text(encoding='utf-8')
    
    dangerous = [
        ('eval(', "使用 eval() 可能导致代码注入"),
        ('exec(', "使用 exec() 可能导致代码注入"),
        ('subprocess.call', "使用 subprocess 可能存在命令注入风险"),
        ('os.system', "使用 os.system() 可能存在命令注入风险"),
        ('pickle.loads', "pickle 反序列化可能导致 RCE"),
        ('yaml.load', "yaml.load 不安全，应使用 yaml.safe_load"),
    ]
    
    for func, desc in dangerous:
        if func in content:
            lines = [i+1 for i, line in enumerate(content.split('\n')) if func in line]
            for line in lines:
                issues.append(f"行 {line}: {desc}")
    
    return issues


def check_path_traversal(file_path: str) -> list:
    """检查路径遍历防护"""
    issues = []
    content = Path(file_path).read_text(encoding='utf-8')
    
    # 检查是否有路径清理
    if 'lstrip' not in content and 'pathlib' not in content:
        issues.append("未检测到路径清理，可能存在路径遍历风险")
    
    # 检查是否有 .. 处理
    if "'..'" in content or '".."' in content:
        issues.append("代码中包含 .. 路径，需确认是否有防护")
    
    return issues


def check_ssl_verification(file_path: str) -> list:
    """检查 SSL 验证设置"""
    issues = []
    content = Path(file_path).read_text(encoding='utf-8')
    
    if 'ssl._create_unverified_context' in content:
        # 检查是否有详细注释说明
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'ssl._create_unverified_context' in line:
                # 检查前3行是否有注释说明
                prev_lines = '\n'.join(lines[max(0, i-3):i])
                if '坚果云' in prev_lines or '证书' in prev_lines or '兼容' in prev_lines:
                    # 有注释说明，不报告问题
                    pass
                else:
                    issues.append("检测到 SSL 验证禁用，请确保有注释说明原因")
    
    if 'verify=False' in content:
        issues.append("检测到 verify=False，可能存在中间人攻击风险")
    
    return issues


def check_sensitive_data_logging(file_path: str) -> list:
    """检查敏感数据是否被记录"""
    issues = []
    content = Path(file_path).read_text(encoding='utf-8')
    
    # 检查是否有打印凭证的代码
    patterns = [
        (r'print.*password', "可能打印密码"),
        (r'print.*secret', "可能打印密钥"),
        (r'print.*token', "可能打印 Token"),
        (r'print.*auth', "可能打印认证信息"),
        (r'logging.*password', "日志中可能记录密码"),
    ]
    
    for pattern, desc in patterns:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            line = content[:match.start()].count('\n') + 1
            issues.append(f"行 {line}: {desc}")
    
    return issues


def check_input_validation(file_path: str) -> list:
    """检查输入验证"""
    issues = []
    content = Path(file_path).read_text(encoding='utf-8')
    
    # 检查是否有配置验证
    if 'ConfigError' not in content:
        issues.append("未检测到配置错误处理")
    
    # 检查是否有输入验证（检查多种验证方式）
    validation_patterns = [
        'validate',
        'required_fields',
        'missing_fields',
        'if.*not in',
        'if.*exists',
    ]
    has_validation = any(p.lower() in content.lower() for p in validation_patterns)
    
    if not has_validation:
        issues.append("未检测到输入验证逻辑")
    
    return issues


def check_file_permissions(file_path: str) -> list:
    """检查文件权限处理"""
    issues = []
    content = Path(file_path).read_text(encoding='utf-8')
    
    # 检查是否有权限设置
    if 'chmod' in content:
        issues.append("代码中包含 chmod，需确认权限设置是否合理")
    
    return issues


def run_security_check(file_path: str) -> dict:
    """运行完整的安全检查"""
    print("=" * 60)
    print("nutstore-sync 安全检查")
    print("=" * 60)
    
    checks = {
        "硬编码凭证": check_hardcoded_credentials(file_path),
        "危险函数": check_dangerous_functions(file_path),
        "路径遍历": check_path_traversal(file_path),
        "SSL验证": check_ssl_verification(file_path),
        "敏感数据日志": check_sensitive_data_logging(file_path),
        "输入验证": check_input_validation(file_path),
        "文件权限": check_file_permissions(file_path),
    }
    
    total_issues = 0
    for category, issues in checks.items():
        print(f"\n【{category}】")
        if issues:
            for issue in issues:
                print(f"  ⚠️  {issue}")
            total_issues += len(issues)
        else:
            print("  ✅ 通过")
    
    print("\n" + "=" * 60)
    print(f"检查完成，发现问题: {total_issues}")
    print("=" * 60)
    
    return checks


def main():
    """主函数"""
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = Path(__file__).parent / "nutstore_sync.py"
    
    if not Path(file_path).exists():
        print(f"错误: 文件不存在 {file_path}")
        sys.exit(1)
    
    checks = run_security_check(str(file_path))
    
    # 统计结果
    total_issues = sum(len(issues) for issues in checks.values())
    
    if total_issues == 0:
        print("\n🎉 安全检查通过！未发现明显安全问题。")
        sys.exit(0)
    else:
        print(f"\n⚠️  发现 {total_issues} 个潜在安全问题，请检查并修复。")
        sys.exit(1)


if __name__ == "__main__":
    main()
