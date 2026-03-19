# nutstore-sync 开源发布待办清单

> 任务：nutstore-sync 技能开源发布  
> 优先级：P1  
> 状态：进行中

---

## 一、GitHub 仓库发布 ✅

### 已完成
- [x] 初始化 Git 仓库
- [x] 创建初始提交 (11 files, 1093 insertions)
- [x] 配置 Git 用户信息

### 待完成
- [ ] **创建 GitHub 仓库**
  - 访问 https://github.com/new
  - 仓库名: `nutstore-sync`
  - 描述: `极简坚果云 WebDAV 同步工具 - 免桌面端，纯标准库实现`
  - 选择 Public
  - 不初始化 README（本地已有）
  
- [ ] **推送代码到 GitHub**
  ```bash
  git remote add origin https://github.com/clawhub/nutstore-sync.git
  git branch -M main
  git push -u origin main
  ```

- [ ] **配置 GitHub 仓库**
  - [ ] 添加仓库描述和标签
  - [ ] 启用 Issues
  - [ ] 启用 Discussions（可选）
  - [ ] 配置分支保护规则

---

## 二、PyPI 发布

### 准备工作
- [ ] **注册 PyPI 账号**
  - 访问 https://pypi.org/account/register/
  - 验证邮箱
  - 启用 2FA（推荐）

- [ ] **创建 API Token**
  - Account Settings → API tokens
  - 创建新 token，权限选 "Upload to PyPI"
  - 保存 token 到 `~/.pypirc`:
    ```ini
    [pypi]
    username = __token__
    password = pypi-xxxxxxxx
    ```

### 打包发布
- [ ] **安装构建工具**
  ```bash
  pip install build twine
  ```

- [ ] **构建分发包**
  ```bash
  cd D:\Documents\Agents\StepFun\nutstore-sync-optimized
  python -m build
  ```
  应生成:
  - `dist/nutstore_sync-2.0.0-py3-none-any.whl`
  - `dist/nutstore_sync-2.0.0.tar.gz`

- [ ] **上传到 PyPI**
  ```bash
  python -m twine upload dist/*
  ```

- [ ] **验证安装**
  ```bash
  pip install nutstore-sync
  nutstore-sync test
  ```

---

## 三、ClawHub 提交

### 准备工作
- [ ] **确认 ClawHub 账号**
  - 访问 https://clawhub.com (或对应平台)
  - 登录/注册账号

### 提交 Skill
- [ ] **准备提交材料**
  - 已准备: `SKILL.md` (含元数据)
  - 已准备: `nutstore_sync.py` (核心代码)
  - 已准备: `README.md` (文档)

- [ ] **提交到 ClawHub**
  - 方式1: 通过网页表单提交
  - 方式2: 通过 CLI 工具提交（如有）
  - 填写信息:
    - Name: nutstore-sync
    - Version: 2.0.0
    - Description: 坚果云 WebDAV 同步工具
    - Tags: webdav, sync, nutstore, cloud-storage

---

## 四、SkillHub 提交

### 准备工作
- [ ] **确认 SkillHub 平台地址**
  - 可能是 https://skillhub.com 或类似平台
  - 了解提交规范

### 提交 Skill
- [ ] **按 SkillHub 规范调整**
  - 检查 `SKILL.md` 格式是否符合要求
  - 调整目录结构（如需要）

- [ ] **提交到 SkillHub**
  - 通过平台提供的提交方式上传

---

## 五、文档完善

### README 优化
- [ ] **添加徽章**
  - PyPI 版本徽章
  - 下载量徽章
  - 许可证徽章
  - Python 版本徽章

- [ ] **添加使用示例 GIF/截图**
  - 命令行操作演示
  - Python API 使用示例

### 其他文档
- [ ] **编写使用教程**
  - 详细配置步骤
  - 常见问题 FAQ
  - 故障排除指南

- [ ] **创建 Wiki（可选）**
  - 高级用法
  - 最佳实践
  - 案例分享

---

## 六、社区推广

### 发布渠道
- [ ] **V2EX 发布**
  - 板块: 分享创造 / Python
  - 标题: [开源] nutstore-sync - 极简坚果云同步工具

- [ ] **知乎发布**
  - 文章: 介绍工具特性
  - 回答相关问题

- [ ] **掘金发布**
  - 技术文章分享

- [ ] **GitHub Trending**
  - 优化仓库标签
  - 邀请朋友 star

### 社交媒体
- [ ] **Twitter/X 发布**
- [ ] **即刻分享**
- [ ] **朋友圈/微信群**

---

## 七、后续维护

### 持续迭代
- [ ] **收集用户反馈**
  - 监控 GitHub Issues
  - 回复用户问题

- [ ] **规划 v2.1.0**
  - 支持更多 WebDAV 服务
  - 添加同步目录功能
  - 支持配置文件热重载

- [ ] **定期更新依赖**
  - Python 版本兼容性测试
  - 安全漏洞修复

---

## 快速开始命令

```bash
# 1. GitHub 发布
git remote add origin https://github.com/clawhub/nutstore-sync.git
git branch -M main
git push -u origin main

# 2. PyPI 发布
pip install build twine
python -m build
python -m twine upload dist/*

# 3. 验证安装
pip install nutstore-sync
nutstore-sync test
```

---

## 相关链接

- GitHub: https://github.com/clawhub/nutstore-sync
- PyPI: https://pypi.org/project/nutstore-sync/
- 坚果云: https://www.jianguoyun.com/
- WebDAV 文档: https://docs.python.org/3/library/urllib.request.html
