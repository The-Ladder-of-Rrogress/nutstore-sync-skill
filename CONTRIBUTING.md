# Contributing to Nutstore Sync

感谢您对 nutstore-sync 的兴趣！我们欢迎各种形式的贡献。

## 如何贡献

### 报告问题

如果您发现了 bug 或有功能建议，请通过 [GitHub Issues](https://github.com/clawhub/nutstore-sync/issues) 提交。

提交问题时请包含：
- 问题描述
- 复现步骤
- 预期行为
- 实际行为
- 环境信息（Python 版本、操作系统）

### 提交代码

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开一个 Pull Request

### 代码规范

- 遵循 [PEP 8](https://pep8.org/) 代码风格
- 添加类型注解
- 编写清晰的文档字符串
- 保持单文件结构

### 测试

```bash
# 运行测试
python -m pytest

# 检查代码风格
python -m flake8 nutstore_sync.py
python -m black --check nutstore_sync.py
```

## 开发环境

```bash
# 克隆仓库
git clone https://github.com/clawhub/nutstore-sync.git
cd nutstore-sync

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows

# 安装开发依赖
pip install -e ".[dev]"
```

## 许可证

通过提交代码，您同意您的贡献将在 MIT 许可证下发布。
