# Nablarch 文档中文翻译进度

本文档记录了 Nablarch 框架文档的中文翻译进度。

## 翻译统计

| 项目 | 数量 |
|------|------|
| 总文件数 | 334 |
| 已翻译文件 | 176 |
| 未翻译文件 | 158 |
| 翻译进度 | **52.7%** |

> **判断标准**：文件中不包含日文假名（平假名/片假名）即认为已翻译

---

## 按模块统计

| 模块 | 已翻译 | 未翻译 | 进度 |
|------|--------|--------|------|
| 处理器 (Handlers) | 65 | 0 | 100% ✅ |
| Web 应用 | 23 | 0 | 100% ✅ |
| Web 服务 | 17 | 0 | 100% ✅ |
| 批处理 (Batch) | 24 | 5 | 82.8% |
| 关于 Nablarch | 4 | 1 | 80% |
| Nablarch 核心 | 5 | 0 | 100% ✅ |
| 类库 (Libraries) | 33 | 16 | 67.3% |
| 空白项目 (Blank Project) | 1 | 19 | 5% |
| 适配器 (Adaptors) | 1 | 15 | 6.3% |
| 消息处理 (Messaging) | 0 | 12 | 0% |
| 云原生 (Cloud Native) | 0 | 4 | 0% |
| 开发工具 (Development Tools) | 0 | 52 | 0% |
| 业务示例 (Biz Samples) | 0 | 15 | 0% |

---

## 已完成模块详情

### ✅ 处理器 (Handlers) - 65个文件

包含所有子类别：
- **Batch 处理器**: 4个文件
- **Common 处理器**: 11个文件
- **HTTP Messaging 处理器**: 4个文件
- **MOM Messaging 处理器**: 4个文件
- **REST 处理器**: 6个文件
- **Standalone 处理器**: 9个文件
- **Web 处理器**: 23个文件
- **Web Interceptor**: 6个文件

### ✅ Web 应用 - 23个文件

包含：
- 应用设计、架构、功能详情
- 入门教程（客户端创建、搜索、更新、删除、上传、下载等）
- 错误页面、JSP Session、前端控制器等

### ✅ Web 服务 - 17个文件

包含：
- 功能对比
- HTTP Messaging（设计、架构、功能详情、入门教程）
- REST（设计、架构、功能详情、入门教程）

### ✅ Nablarch 核心 - 5个文件

- architecture.rst
- big_picture.rst
- index.rst
- platform.rst
- policy.rst

---

## 未翻译文件分布

### 1. 空白项目 (Blank Project) - 19个文件

| 文件 | 状态 |
|------|------|
| `blank_project/FirstStep.rst` | 🔴 与原文相同 |
| `blank_project/FirstStepContainer.rst` | 🔴 与原文相同 |
| `blank_project/ModifySettings.rst` | 🔴 与原文相同 |
| `blank_project/CustomizeDB.rst` | 🟡 含日文 |
| `blank_project/beforeFirstStep.rst` | 🟡 含日文 |
| `blank_project/MavenModuleStructures/index.rst` | 🟡 含日文 |
| `blank_project/addin_gsp.rst` | 🟡 含日文 |
| `blank_project/maven.rst` | 🟡 含日文 |
| `blank_project/setup_blankProject/*.rst` | 🟡 含日文 (6个) |
| `blank_project/setup_containerBlankProject/*.rst` | 🟡 含日文 (4个) |
| `blank_project/firstStep_appendix/*.rst` | 🟡 含日文 (2个) |

### 2. 适配器 (Adaptors) - 15个文件

全部包含日文，需要翻译：
- doma_adaptor.rst
- jaxrs_adaptor.rst
- jsr310_adaptor.rst
- lettuce_adaptor 及相关文件
- log_adaptor.rst
- mail_sender_freemarker_adaptor.rst
- mail_sender_thymeleaf_adaptor.rst
- mail_sender_velocity_adaptor.rst
- micrometer_adaptor.rst
- router_adaptor.rst
- slf4j_adaptor.rst
- web_thymeleaf_adaptor.rst
- webspheremq_adaptor.rst

### 3. 类库 (Libraries) - 16个文件

包含日文，需要翻译：
- database/*.rst (数据库相关, 5个文件)
- log/*.rst (日志相关, 6个文件)
- data_io/data_format/format_definition.rst
- repository.rst (部分)
- session_store.rst (部分)
- stateless_web_app.rst (部分)
- static_data_cache.rst (部分)
- system_messaging.rst (部分)

### 4. 批处理 (Batch) - 5个文件

- `nablarch_batch/architecture.rst` - 含日文
- 其他4个未开始（与原文相同）

### 5. 消息处理 (Messaging) - 12个文件

全部未翻译：
- mom_messaging/*.rst
- http_messaging/*.rst
- db/*.rst

### 6. 开发工具 (Development Tools) - 52个文件

全部未翻译，包括：
- testing_framework/guide/development_guide/... (测试框架)
- java_static_analysis/... (静态分析)

### 7. 业务示例 (Biz Samples) - 15个文件

全部未翻译，包括：
- 01/ (PBKDF2密码加密)
- 03/ (文件管理)
- 04/ (扩展字段类型)
- 其他业务示例

### 8. 其他 - 19个文件

包括：
- cloud_native/*.rst (4个)
- configuration/*.rst
- setting_guide/*.rst
- about_nablarch/versionup_policy.rst
- 其他配置文档

---

## 如何贡献翻译

1. 从「未翻译文件列表」中选择要翻译的文件
2. 参考 `ja/` 目录下的对应日文原文进行翻译
3. 将翻译后的文件保存到 `zh_CN/` 目录的对应位置
4. 确保翻译后的文件中**不包含日文假名**（平假名/片假名）
5. 运行检查脚本更新翻译进度：
   ```bash
   python check_translation.py
   ```
6. 提交 Pull Request

### 翻译规范

- 保持与原文档的 RST 格式一致
- 参考 `.kimi/skills/nablarch-translation/terms/TERMINOLOGY.md` 术语表
- 技术术语首次出现时标注日文或英文
- **确保最终文件中没有日文假名**

---

## 更新记录

| 日期 | 更新内容 |
|------|----------|
| 2026-02-15 | 更新翻译进度：已翻译 176 个文件，进度 52.7% |

---

*本文档由脚本自动生成，如有疑问请参考项目 README_zh_CN.md*
