---
name: nutstore-sync
description: |
  坚果云 WebDAV 同步工具 - 免桌面端，纯标准库实现。
  支持文件上传、下载、目录列表、删除等操作。
  仅依赖 Python 标准库，无需额外安装。
  
  安全特性：
  - 零硬编码凭证，配置文件隔离
  - 输入验证与路径清理
  - 通过 Bandit 安全扫描
  - 自动化 CI/CD 安全检测
version: 2.0.0
author: 阶跃AI+The-Ladder-of-Rrogress
license: MIT
tags: [webdav, sync, nutstore, cloud-storage, jianguoyun, security]
dependencies: []
requirements:
  python: ">=3.8"
  env_vars: []
  binaries: []
  install: []
security:
  verified: true
  scan_tool: bandit
  no_hardcoded_credentials: true
  input_validation: true
  standard_library_only: true
---

# 坚果云 WebDAV 同步

> 体积: ~3KB | 依赖: 仅标准库 | 配置: 本地 JSON

## 功能特性

- ✅ **零依赖** - 仅使用 Python 标准库
- ✅ **轻量级** - 单文件 ~3KB
- ✅ **双向同步** - 上传/下载/列表/删除
- ✅ **跨平台** - Windows/macOS/Linux
- ✅ **类型提示** - 完整的类型注解
- ✅ **异常处理** - 清晰的错误分类

## 配置

创建 `.nutstore_credentials`:

```json
{
  "username": "your_email@example.com",
  "app_password": "your_app_password",
  "webdav_url": "https://dav.jianguoyun.com/dav/"
}
```

配置文件搜索路径（按优先级）：
1. 脚本同级目录: `./.nutstore_credentials`
2. 用户主目录: `~/.nutstore_credentials`
3. Skill 目录: `~/.stepfun/skills/nutstore-sync/.nutstore_credentials`

## 命令行使用

```bash
# 测试连接
python nutstore_sync.py test

# 上传文件
python nutstore_sync.py upload local.txt [remote/path/]

# 下载文件
python nutstore_sync.py download remote.txt [local.txt]

# 列出目录
python nutstore_sync.py list [remote/path/]

# 删除文件
python nutstore_sync.py delete remote.txt

# 检查文件是否存在
python nutstore_sync.py exists remote.txt
```

## Python API

```python
from nutstore_sync import NutstoreSync, NutstoreError

# 初始化（自动搜索配置文件）
client = NutstoreSync()

# 或指定配置文件
client = NutstoreSync("/path/to/config.json")

# 测试连接
try:
    if client.test():
        print("连接成功")
except NutstoreError as e:
    print(f"连接失败: {e}")

# 上传文件
client.upload('local.txt', 'remote.txt')

# 下载文件
client.download('remote.txt', 'local.txt')

# 列出目录
items = client.list_dir('remote/path/')
for icon, name in items:
    print(f"{icon} {name}")

# 删除文件
client.delete('remote.txt')

# 检查文件是否存在
if client.exists('remote.txt'):
    print("文件存在")
```

## 异常处理

```python
from nutstore_sync import NutstoreSync, ConfigError, APIError

try:
    client = NutstoreSync()
    client.upload('file.txt')
except ConfigError as e:
    print(f"配置错误: {e}")
except APIError as e:
    print(f"API错误 (状态码 {e.status_code}): {e}")
except FileNotFoundError as e:
    print(f"本地文件不存在: {e}")
```

## 平台适配

| 平台 | 支持 | 说明 |
|------|------|------|
| ClawHub | ✅ | 标准 Skill 格式 |
| GitHub | ✅ | 完整开源仓库 |
| PyPI | ✅ | `pip install nutstore-sync` |
| Coze | ✅ | 作为插件使用 |
| SkillHub | ✅ | 标准 skill 格式 |

## 文件结构

```
nutstore-sync/
├── nutstore_sync.py          # 核心代码 (~3KB)
├── pyproject.toml            # Python 包配置
├── SKILL.md                  # Skill 元数据
├── README.md                 # 完整文档
├── LICENSE                   # MIT 许可证
├── .gitignore                # Git 忽略配置
└── .nutstore_credentials.example  # 配置示例
```

## 安装

### 从 PyPI 安装

```bash
pip install nutstore-sync
```

### 从源码安装

```bash
git clone https://github.com/clawhub/nutstore-sync.git
cd nutstore-sync
pip install -e .
```

### 直接使用

```bash
# 下载单文件使用
curl -O https://raw.githubusercontent.com/clawhub/nutstore-sync/main/nutstore_sync.py
python nutstore_sync.py test
```

## 更新日志

### v2.0.0
- 重构为单文件结构
- 添加完整的类型注解
- 添加异常类体系 (NutstoreError, ConfigError, APIError)
- 新增 delete() 和 exists() 方法
- 添加 pyproject.toml 包配置
- 优化错误处理和提示信息

## 许可证

MIT License - 详见 [LICENSE](LICENSE)
