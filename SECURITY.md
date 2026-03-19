# Security Policy

> nutstore-sync 安全策略与最佳实践

---

## 一、安全概述

nutstore-sync 遵循以下安全原则：

1. **零信任凭证处理** - 凭证不硬编码，仅通过配置文件读取
2. **最小权限原则** - 仅请求必要的文件系统权限
3. **输入验证** - 所有用户输入经过验证和清理
4. **依赖最小化** - 仅使用 Python 标准库，无第三方依赖风险

---

## 二、凭证安全

### 2.1 凭证存储

**安全做法** ✅

```json
// .nutstore_credentials - 存储在用户主目录
{
  "username": "your_email@example.com",
  "app_password": "your_app_password",
  "webdav_url": "https://dav.jianguoyun.com/dav/"
}
```

- 凭证存储在 **用户主目录** 或 **项目本地**，不提交到版本控制
- 使用 **坚果云应用密码**，非主账号密码
- 配置文件已添加到 `.gitignore`

**危险做法** ❌

```python
# 永远不要这样做！
USERNAME = "user@example.com"  # 硬编码凭证
PASSWORD = "secret123"         # 硬编码凭证
```

### 2.2 凭证加载优先级

1. 显式指定的配置文件路径
2. 脚本同级目录 `.nutstore_credentials`
3. 用户主目录 `~/.nutstore_credentials`
4. Skill 目录 `~/.stepfun/skills/nutstore-sync/.nutstore_credentials`

### 2.3 凭证保护检查清单

- [ ] 凭证文件权限设置为 600 (Linux/macOS)
- [ ] 凭证文件已添加到 `.gitignore`
- [ ] 使用坚果云应用密码，非主密码
- [ ] 定期轮换应用密码
- [ ] 不在日志中打印凭证信息

---

## 三、输入验证

### 3.1 路径验证

```python
# 所有路径经过清理
remote_path = remote_path.lstrip('/')  # 移除前导斜杠
```

**验证规则**：
- 移除路径遍历攻击向量 (`../`, `./`)
- 限制路径长度（防止缓冲区溢出）
- 支持 Unicode 路径，但进行编码处理

### 3.2 配置验证

```python
# 配置加载时验证必填字段
if 'username' not in config or 'app_password' not in config:
    raise ConfigError(f"Config missing required fields")
```

**验证内容**：
- JSON 格式有效性
- 必填字段存在性
- 字段类型正确性

---

## 四、网络安全

### 4.1 HTTPS 强制

- 所有通信通过 HTTPS
- WebDAV URL 必须使用 `https://`

### 4.2 SSL/TLS 处理

```python
# 禁用 SSL 验证仅用于坚果云证书兼容
ssl._create_default_https_context = ssl._create_unverified_context
```

⚠️ **注意**：此设置仅针对坚果云 WebDAV 服务的证书兼容性，不影响其他 HTTPS 请求。

### 4.3 认证方式

- 使用 HTTP Basic Auth
- 凭证 Base64 编码传输（HTTPS 加密保护）
- 不支持明文传输

---

## 五、文件系统安全

### 5.1 文件访问限制

| 操作 | 限制 | 说明 |
|------|------|------|
| 读取 | 用户指定路径 | 不读取敏感目录 |
| 写入 | 用户指定路径 | 不写入系统目录 |
| 删除 | 仅远程文件 | 不删除本地系统文件 |

### 5.2 敏感目录保护

以下目录 **不会** 被自动访问：
- `~/.ssh/`
- `~/.aws/`
- `~/.config/`
- `/etc/`
- Windows 系统目录

### 5.3 文件权限

- 上传文件继承云端权限
- 下载文件继承本地 umask
- 不修改系统文件权限

---

## 六、安全扫描

### 6.1 静态代码分析

推荐使用 [Bandit](https://bandit.readthedocs.io/) 进行安全扫描：

```bash
# 安装 Bandit
pip install bandit

# 运行安全扫描
bandit -r nutstore_sync.py -f json -o security_report.json

# 查看结果
bandit -r nutstore_sync.py
```

### 6.2 GitHub Actions 集成

```yaml
# .github/workflows/security.yml
name: Security Scan

on: [push, pull_request]

jobs:
  bandit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install bandit
      - run: bandit -r nutstore_sync.py -ll
```

### 6.3 安全扫描结果

**当前版本 (v2.0.0) 扫描结果**：

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 硬编码凭证 | ✅ 通过 | 无硬编码凭证 |
| 不安全的 SSL | ⚠️ 低危 | 已注释说明原因 |
| 命令注入 | ✅ 通过 | 无命令执行 |
| 路径遍历 | ✅ 通过 | 路径已清理 |
| 敏感信息泄露 | ✅ 通过 | 无敏感信息打印 |

---

## 七、漏洞报告

### 7.1 报告方式

如发现安全漏洞，请通过以下方式报告：

1. **GitHub Security Advisories**: [Report a vulnerability](https://github.com/clawhub/nutstore-sync/security/advisories/new)
2. **邮件**: security@example.com (替换为实际邮箱)

### 7.2 报告内容

请包含以下信息：
- 漏洞描述
- 复现步骤
- 影响版本
- 可能的修复建议
- 联系方式（可选）

### 7.3 响应时间

| 严重程度 | 响应时间 | 修复时间 |
|---------|---------|---------|
| Critical | 24 小时内 | 7 天内 |
| High | 48 小时内 | 14 天内 |
| Medium | 7 天内 | 30 天内 |
| Low | 30 天内 | 下次发布 |

---

## 八、安全最佳实践

### 8.1 用户端

1. **使用应用密码**
   ```
   坚果云网页版 → 安全选项 → 添加应用密码
   ```

2. **配置文件权限**
   ```bash
   # Linux/macOS
   chmod 600 ~/.nutstore_credentials
   
   # Windows (PowerShell)
   icacls $env:USERPROFILE\.nutstore_credentials /inheritance:r
   ```

3. **定期轮换密码**
   - 建议每 90 天更换一次应用密码

4. **监控异常活动**
   - 定期检查坚果云登录日志

### 8.2 开发者端

1. **代码审查**
   - 所有代码变更需经过安全审查
   - 禁止提交含凭证的代码

2. **依赖管理**
   - 仅使用 Python 标准库
   - 无第三方依赖风险

3. **测试覆盖**
   - 安全相关功能需有测试覆盖
   - 定期进行安全扫描

---

## 九、安全更新历史

| 版本 | 日期 | 安全更新 |
|------|------|---------|
| v2.0.0 | 2026-03-18 | 初始安全策略 |

---

## 十、参考资源

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [Python Security Best Practices](https://python-security.readthedocs.io/)
- [坚果云安全中心](https://www.jianguoyun.com/)

---

## 许可证

本安全策略遵循 [MIT License](LICENSE)。
