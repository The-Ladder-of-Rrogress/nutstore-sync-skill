# nutstore-sync

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)

极简坚果云 WebDAV 同步工具，仅依赖 Python 标准库。

[English](#english) | [中文](#中文)

---

## 中文

### 特性

- ✅ **零依赖** - 仅使用 Python 标准库
- ✅ **轻量级** - 单文件 ~3KB
- ✅ **双向同步** - 上传/下载/列表/删除
- ✅ **跨平台** - Windows/macOS/Linux
- ✅ **类型提示** - 完整的类型注解
- ✅ **异常处理** - 清晰的错误分类

### 安装

```bash
# 从 PyPI 安装
pip install nutstore-sync

# 或从源码安装
git clone https://github.com/clawhub/nutstore-sync.git
cd nutstore-sync
pip install -e .
```

### 配置

创建 `.nutstore_credentials`:

```json
{
  "username": "your_email@example.com",
  "app_password": "your_app_password",
  "webdav_url": "https://dav.jianguoyun.com/dav/"
}
```

配置文件搜索路径（按优先级）：
1. 脚本同级目录
2. `~/.nutstore_credentials`
3. `~/.stepfun/skills/nutstore-sync/.nutstore_credentials`

### 命令行使用

```bash
# 测试连接
nutstore-sync test

# 上传文件
nutstore-sync upload local.txt [remote/path/]

# 下载文件
nutstore-sync download remote.txt [local.txt]

# 列出目录
nutstore-sync list [remote/path/]

# 删除文件
nutstore-sync delete remote.txt

# 检查文件是否存在
nutstore-sync exists remote.txt
```

### Python API

```python
from nutstore_sync import NutstoreSync, NutstoreError

client = NutstoreSync()

# 上传文件
client.upload('local.txt', 'remote.txt')

# 下载文件
client.download('remote.txt', 'local.txt')

# 列出目录
items = client.list_dir('remote/path/')
for icon, name in items:
    print(f"{icon} {name}")
```

---

## English

### Features

- ✅ **Zero Dependencies** - Only Python standard library
- ✅ **Lightweight** - Single file ~3KB
- ✅ **Bidirectional Sync** - Upload/Download/List/Delete
- ✅ **Cross-Platform** - Windows/macOS/Linux
- ✅ **Type Hints** - Complete type annotations
- ✅ **Error Handling** - Clear exception hierarchy

### Installation

```bash
pip install nutstore-sync
```

### Configuration

Create `.nutstore_credentials`:

```json
{
  "username": "your_email@example.com",
  "app_password": "your_app_password",
  "webdav_url": "https://dav.jianguoyun.com/dav/"
}
```

### Usage

```bash
# Test connection
nutstore-sync test

# Upload file
nutstore-sync upload local.txt [remote/path/]

# Download file
nutstore-sync download remote.txt [local.txt]

# List directory
nutstore-sync list [remote/path/]
```

### Python API

```python
from nutstore_sync import NutstoreSync

client = NutstoreSync()
client.upload('local.txt', 'remote.txt')
```

---

## 平台适配 / Platform Support

| 平台 / Platform | 支持 / Support | 说明 / Note |
|----------------|----------------|-------------|
| ClawHub | ✅ | 标准 Skill 格式 |
| GitHub | ✅ | 完整开源仓库 |
| PyPI | ✅ | `pip install nutstore-sync` |
| Coze | ✅ | 作为插件使用 |
| SkillHub | ✅ | 标准 skill 格式 |

## 安全性 / Security

🔒 **安全特性**：
- ✅ 零硬编码凭证
- ✅ 凭证文件权限保护
- ✅ 输入验证与清理
- ✅ 仅使用 Python 标准库（无第三方依赖风险）
- ✅ 通过 Bandit 安全扫描
- ✅ 自动化安全检测（GitHub Actions）

📄 **安全文档**：
- [SECURITY.md](SECURITY.md) - 完整安全策略
- [安全扫描脚本](security_check.py) - 本地安全检查

## 文件结构 / File Structure

```
nutstore-sync/
├── nutstore_sync.py          # Core code (~3KB)
├── pyproject.toml            # Package config
├── SKILL.md                  # Skill metadata
├── README.md                 # Documentation
├── LICENSE                   # MIT License
├── .gitignore                # Git ignore
└── .nutstore_credentials.example  # Config example
```

## 更新日志 / Changelog

### v2.0.0
- Refactored to single file structure
- Added complete type annotations
- Added exception hierarchy
- Added delete() and exists() methods
- Added pyproject.toml configuration

## 许可证 / License

MIT License - See [LICENSE](LICENSE)
