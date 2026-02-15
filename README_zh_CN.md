# Nablarch 文档（中文版）

[![翻译进度](https://img.shields.io/badge/翻译进度-52.7%25-green)](TRANSLATION_STATUS.md)
[![使用 Skill](https://img.shields.io/badge/使用-Skill-blue)](.kimi/skills/nablarch-translation/SKILL.md)

本项目是 [Nablarch](https://nablarch.github.io/) 框架文档的中文翻译项目。

## 关于 Nablarch

Nablarch 是一个为企业信息系统开发的 Java 应用框架，由日本 TIS 公司开发并开源。它提供了：

- **健壮性（Robustness）**：能够长期稳定运行的企业级框架
- **可测试性（Testability）**：重视测试容易性的设计，提供各种驱动程序、模拟对象和自动化测试框架
- **开箱即用（Ready-to-Use）**：提供经过验证的组件和适配器，使开发者能够快速开始开发

## 文档结构

```
.
├── ja/           # 日文原文文档（原始）
├── en/           # 英文文档
├── zh_CN/        # 中文文档（本翻译项目）
├── _static/      # 静态资源文件
├── _templates/   # Sphinx 模板文件
└── locales/      # 本地化文件
```

## 翻译进度

目前翻译进度：**52.7%**（176/334 文件）

## 文档索引

| 文档 | 说明 |
|------|------|
| [TRANSLATION_STATUS.md](TRANSLATION_STATUS.md) | 详细翻译进度 |
| [TERMINOLOGY.md](.kimi/skills/nablarch-translation/terms/TERMINOLOGY.md) | 术语对照表 |
| [TRANSLATION_GUIDE.md](.kimi/skills/nablarch-translation/guides/TRANSLATION_GUIDE.md) | 翻译指南 |

## 翻译进度

目前翻译进度：**52.7%**（176/334 文件）

详细进度请参考：[TRANSLATION_STATUS.md](TRANSLATION_STATUS.md)

### 已完成的模块

| 模块 | 进度 | 说明 |
|------|------|------|
| ✅ 处理器 (handlers) | 65/65 (100%) | 全部完成 |
| ✅ Web 应用 (web) | 23/23 (100%) | 全部完成 |
| ✅ Web 服务 (web_service) | 17/17 (100%) | 全部完成 |
| ✅ Nablarch 核心 | 5/5 (100%) | 全部完成 |
| 批处理 (batch) | 24/29 (82.8%) | Nablarch Batch 和 JSR352 基本完成 |
| 类库 (libraries) | 33/49 (67.3%) | 核心类库已完成 |
| 关于 Nablarch | 4/5 (80%) | concept, index, license, mvn_module 已完成 |
| 空白项目 (blank_project) | 1/20 (5%) | 仅 index 完成 |
| 适配器 (adaptors) | 1/16 (6.3%) | 仅 index 完成 |
| 消息处理 (messaging) | 0/12 (0%) | 未开始 |
| 云原生 (cloud_native) | 0/4 (0%) | 未开始 |
| 开发工具 (development_tools) | 0/52 (0%) | 未开始 |
| 业务示例 (biz_samples) | 0/15 (0%) | 未开始 |

## 环境准备

本文档使用 [Sphinx](https://www.sphinx-doc.org/) 构建。

### Windows 环境

#### 1. 文档构建环境

安装 Python 3.8.x 及依赖库：

```bash
pip install -r requirements.txt
```

#### 2. textlint 执行环境（可选）

除上述环境外，还需安装：

- Node.js（已在 v20.15.1 版本验证）
- npm 依赖：
  ```bash
  npm install
  ```

#### 3. linkcheck 执行环境

与文档构建环境相同。

### Docker 环境

构建 Docker 镜像：

```bash
docker build -t nablarch-document-build .
```

## 构建文档

### Windows

```bash
# 构建日文文档
make html ja

# 构建英文文档
make html en

# 构建中文文档
make html zh_CN
```

### Docker

```bash
# 构建日文文档
docker run --rm -v <仓库目录(绝对路径)>:/root/document nablarch-document-build \
  /bin/bash -c "cd /root/document; sphinx-build -d _build/.doctrees/ja -b html ja _build/html"

# 构建英文文档
docker run --rm -v <仓库目录(绝对路径)>:/root/document nablarch-document-build \
  /bin/bash -c "cd /root/document; sphinx-build -d _build/.doctrees/en -b html en _build/html/en"

# 构建中文文档
docker run --rm -v <仓库目录(绝对路径)>:/root/document nablarch-document-build \
  /bin/bash -c "cd /root/document; sphinx-build -d _build/.doctrees/zh_CN -b html zh_CN _build/html/zh_CN"
```

构建后的文档将位于 `_build/html/` 目录下。

## textlint 使用方法

### 配置文件

| 文件 | 说明 |
|------|------|
| `.textlintrc` | textlint 配置文件 |
| `.textlint/conf/prh.yml` | 词典文件 |

### 运行 textlint

#### Windows

```bash
# 检查单个文件
./node_modules/.bin/textlint .textlint/test/test.rst

# 检查目录
./node_modules/.bin/textlint ja/development_tools
```

如果已将 `./node_modules/.bin` 添加到 PATH，可直接运行：

```bash
textlint ja/development_tools
```

#### Docker

```bash
# 检查单个文件
docker run --rm -v <仓库目录(绝对路径)>:/root/document nablarch-document-build \
  /bin/bash -c "cd /root/document; ../node_modules/.bin/textlint .textlint/test/test.rst"

# 检查目录
docker run --rm -v <仓库目录(绝对路径)>:/root/document nablarch-document-build \
  /bin/bash -c "cd /root/document; ../node_modules/.bin/textlint ja/development_tools"
```

## linkcheck 使用方法

### Docker

```bash
# 检查日文文档
docker run --rm -v <仓库目录(绝对路径)>:/root/document nablarch-document-build \
  /bin/bash -c "cd /root/document; sphinx-build -d _build/.doctrees/ja -b linkcheck ja _build/linkcheck/ja"

# 检查英文文档
docker run --rm -v <仓库目录(绝对路径)>:/root/document nablarch-document-build \
  /bin/bash -c "cd /root/document; sphinx-build -d _build/.doctrees/en -b linkcheck en _build/linkcheck/en"
```

## 翻译工具

本项目提供了 Kimi Skill 来辅助翻译工作。

### 快速开始

告诉 AI 要翻译的文件：

```
请翻译 ja/application_framework/application_framework/web/architecture.rst
```

AI 会自动：
1. 参考术语表进行翻译
2. 保持 RST 格式不变
3. 确保无日文假名残留
4. 更新术语表（如有新术语）
5. 更新翻译进度

### 批量翻译

```
请批量翻译 application_framework/application_framework/handlers/web/ 下的所有未翻译文件
```

### 更新进度

```
请更新翻译进度文档
```

### 术语表

参考 `.kimi/skills/nablarch-translation/terms/TERMINOLOGY.md` 获取术语对照表。

### 翻译指南

参考 `.kimi/skills/nablarch-translation/guides/TRANSLATION_GUIDE.md` 获取详细的翻译规范。

### 可选脚本

提供了辅助检查脚本（可选）：

```bash
python .kimi/skills/nablarch-translation/scripts/check_translation.py
```

## 参与翻译

我们欢迎社区贡献！如果你想参与翻译：

1. Fork 本仓库
2. 从 [TRANSLATION_STATUS.md](TRANSLATION_STATUS.md) 中选择一个未翻译的文件
3. 参考 `ja/` 目录下的原文进行翻译
4. 将翻译后的文件保存到 `zh_CN/` 目录的对应位置
5. 更新翻译进度文档
6. 提交 Pull Request

### 翻译规范

- 保持与原文档的格式一致（RST 格式）
- 技术术语建议保留英文原文，可在首次出现时标注中文
- 保持代码示例不变，仅翻译注释和说明文字

## 许可证

本项目的文档内容遵循与原始项目相同的许可证。详见 [LICENSE.txt](LICENSE.txt)。

## 相关链接

- [Nablarch 官方网站](https://nablarch.github.io/)
- [Nablarch GitHub](https://github.com/nablarch)
- [日文原文档](https://github.com/nablarch/nablarch-document)

---

*本项目由社区维护，非 Nablarch 官方翻译项目。*
