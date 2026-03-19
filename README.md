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

### 前置条件

使用本技能前，你需要：

| 条件 | 说明 | 零基础教程 |
|------|------|-----------|
| **Python 3.8+** | 本技能使用 Python 编写 | [Python 安装指南](https://www.python.org/downloads/) |
| **坚果云账号 + 应用密码** | 注册账号后开启 WebDAV 并创建应用密码 | [坚果云注册与配置教程](https://www.jianguoyun.com/?p=2064) |

> 💡 **完全零基础？** 跟着这个步骤走：
> 1. 点击上表中的 "Python 安装指南" 安装 Python
> 2. 点击 "坚果云注册与配置教程" 完成：
>    - 注册坚果云账号
>    - 开启 WebDAV 服务
>    - 创建应用密码（⚠️ 不是登录密码！）
> 3. 继续下方的 "安装" 步骤
>
> 📖 **应用密码是什么？**
> 应用密码是坚果云为第三方应用提供的专用密码，与你的登录密码不同。
> 创建后请妥善保存，只显示一次！

### 安装

#### 方式一：通过自然语言安装（Agent 用户推荐）

如果你正在使用 Claude、ChatGPT 或其他 AI Agent，可以直接用自然语言安装：

> **"帮我安装 nutstore-sync 技能，用于坚果云 WebDAV 同步"**

或

> **"请帮我安装这个技能：https://github.com/The-Ladder-of-Rrogress/nutstore-sync-skill"**

Agent 会自动完成：
1. 克隆仓库到技能目录
2. 安装 Python 包（如需要）
3. 创建配置文件模板
4. 验证安装是否成功

#### 方式二：手动安装

```bash
# 从 PyPI 安装
pip install nutstore-sync

# 或从源码安装
git clone https://github.com/The-Ladder-of-Rrogress/nutstore-sync-skill.git
cd nutstore-sync-skill
pip install -e .
```

#### 方式三：作为 Agent Skill 安装

将本技能添加到 Agent 的技能目录：

```bash
# 克隆到 Agent 技能目录
git clone https://github.com/The-Ladder-of-Rrogress/nutstore-sync-skill.git \
  ~/.stepfun/skills/nutstore-sync

# 或使用 SkillHub/ClawHub 安装
# skill install nutstore-sync
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

#### Option 1: Natural Language Install (Recommended for Agent Users)

If you're using Claude, ChatGPT, or other AI Agents, simply ask:

> **"Install the nutstore-sync skill for Nutstore WebDAV sync"**

Or

> **"Please install this skill: https://github.com/The-Ladder-of-Rrogress/nutstore-sync-skill"**

The Agent will automatically:
1. Clone the repository to the skills directory
2. Install Python package (if needed)
3. Create configuration file template
4. Verify installation success

#### Option 2: Manual Install

```bash
pip install nutstore-sync
```

#### Option 3: Install as Agent Skill

```bash
git clone https://github.com/The-Ladder-of-Rrogress/nutstore-sync-skill.git \
  ~/.stepfun/skills/nutstore-sync
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
| **ClawHub** | ✅ | 标准 Skill 格式，支持自然语言安装 |
| **GitHub** | ✅ | 完整开源仓库 |
| **PyPI** | ✅ | `pip install nutstore-sync` |
| **Coze** | ✅ | 作为插件使用 |
| **SkillHub** | ✅ | 标准 skill 格式 |
| **StepFun** | ✅ | 支持 `agent_skill` 加载 |

### Agent 自然语言安装示例

```
用户: "帮我安装 nutstore-sync 技能"
Agent: 自动克隆仓库 → 验证配置 → 测试连接 → 完成安装

用户: "用坚果云同步上传我的笔记"
Agent: 调用 nutstore_sync.upload('notes.md', 'knowledge/notes.md')
```

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
