# Nablarch 文档中文翻译状态

## 总体进度

| 指标 | 数量 |
|------|------|
| 总文件数 | 334 |
| 已翻译 | 262 |
| 未翻译 | 72 |
| **进度** | **78.4%** |

---

## 各模块翻译状态

| 模块 | 文件数 | 已翻译 | 未翻译 | 进度 |
|------|--------|--------|--------|------|
| about_nablarch | 7 | 5 | 2 | 71.4% |
| application_framework | 219 | 203 | 16 | 92.7% |
| biz_samples | 16 | 1 | 15 | 6.3% |
| development_tools | 55 | 55 | 0 | **100%** |
| inquiry | 1 | 0 | 1 | 0% |
| releases | 1 | 0 | 1 | 0% |
| terms_of_use | 1 | 0 | 1 | 0% |

---

## 已完成的模块

以下模块已 100% 翻译完成：

- ✅ **Development Tools** (55/55 文件)
  - Java Static Analysis
  - Testing Framework (单元测试指南、测试框架指南、测试工具)
  - Toolbox (JSP静态分析、SQL执行器、OpenAPI生成器)
  
- ✅ **Adaptors** (16/16 文件)
  - Doma适配器
  - Jakarta RESTful Web Services适配器
  - JSR310适配器
  - Lettuce适配器 (Redis存储、Redis健康检查)
  - 日志适配器 (SLF4J、JBoss Logging)
  - 邮件发送适配器 (FreeMarker、Thymeleaf、Velocity)
  - Micrometer适配器
  - 路由适配器
  - SLF4J适配器
  - Web Thymeleaf适配器
  - IBM MQ适配器

---

## 主要已完成子模块

| 子模块 | 文件数 | 状态 |
|--------|--------|------|
| **Handlers** | 74 | ✅ 100% 完成 |
| **Web** | 44 | ✅ 100% 完成 |
| **Batch** (JSR352 + Nablarch) | 29 | ✅ 100% 完成 |
| **Libraries** | 49 | ✅ 100% 完成 |
| **Web Service** (REST + HTTP Messaging) | 22 | ✅ 100% 完成 |
| **Nablarch Core** | 5 | ✅ 100% 完成 |
| **Adaptors** | 16 | ✅ 100% 完成 |

---

## 剩余未翻译文件 (72个)

### About Nablarch (2个)
- `about_nablarch/versionup_policy.rst` ⭐ 高优先级

### Application Framework - Blank Project (17个)
- `blank_project/FirstStep.rst`
- `blank_project/FirstStepContainer.rst`
- `blank_project/ModifySettings.rst`
- `blank_project/CustomizeDB.rst`
- `blank_project/maven.rst`
- `blank_project/addin_gsp.rst`
- `blank_project/beforeFirstStep.rst`
- `blank_project/MavenModuleStructures/index.rst`
- `blank_project/firstStep_appendix/ResiBatchReboot.rst`
- `blank_project/firstStep_appendix/firststep_complement.rst`
- `blank_project/setup_blankProject/setup_Java21.rst`
- `blank_project/setup_blankProject/setup_Jbatch.rst`
- `blank_project/setup_blankProject/setup_NablarchBatch.rst`
- `blank_project/setup_blankProject/setup_NablarchBatch_Dbless.rst`
- `blank_project/setup_blankProject/setup_Web.rst`
- `blank_project/setup_blankProject/setup_WebService.rst`
- `blank_project/setup_containerBlankProject/setup_ContainerBatch.rst`
- `blank_project/setup_containerBlankProject/setup_ContainerBatch_Dbless.rst`
- `blank_project/setup_containerBlankProject/setup_ContainerWeb.rst`
- `blank_project/setup_containerBlankProject/setup_ContainerWebService.rst`

### Application Framework - Messaging (12个)
- `messaging/db/index.rst`
- `messaging/db/application_design.rst`
- `messaging/db/architecture.rst`
- `messaging/db/feature_details.rst`
- `messaging/db/feature_details/error_processing.rst`
- `messaging/db/feature_details/multiple_process.rst`
- `messaging/db/getting_started.rst`
- `messaging/db/getting_started/table_queue.rst`
- `messaging/mom/index.rst`
- `messaging/mom/application_design.rst`
- `messaging/mom/architecture.rst`
- `messaging/mom/feature_details.rst`
- `messaging/mom/getting_started.rst`
- `messaging/index.rst`

### Application Framework - Cloud Native (6个)
- `cloud_native/index.rst`
- `cloud_native/containerize/index.rst`
- `cloud_native/distributed_tracing/index.rst`
- `cloud_native/distributed_tracing/aws_distributed_tracing.rst`
- `cloud_native/distributed_tracing/azure_distributed_tracing.rst`

### Application Framework - Setting Guide (7个)
- `setting_guide/index.rst`
- `setting_guide/configuration/index.rst`
- `setting_guide/ManagingEnvironmentalConfiguration/index.rst`
- `setting_guide/CustomizingConfigurations/index.rst`
- `setting_guide/CustomizingConfigurations/config_key_naming.rst`
- `setting_guide/CustomizingConfigurations/CustomizeMessageIDAndMessage.rst`
- `setting_guide/CustomizingConfigurations/CustomizeAvailableCharacters.rst`
- `setting_guide/CustomizingConfigurations/CustomizeSystemTableName.rst`

### Biz Samples (13个)
- `biz_samples/01/0101_PBKDF2PasswordEncryptor.rst`
- `biz_samples/04/index.rst`
- `biz_samples/04/0402_ExtendedFieldType.rst`
- `biz_samples/13/index.rst`
- 以及其他9个文件

### Others (3个)
- `inquiry/index.rst`
- `releases/index.rst`
- `terms_of_use/index.rst`

---

## 建议翻译优先级

| 优先级 | 模块 | 文件数 | 理由 |
|--------|------|--------|------|
| 🔴 高 | **Blank Project** | 17 | 项目初始设置指南，新用户必需 |
| 🟡 中 | **Messaging** | 12 | 消息处理功能 |
| 🟡 中 | **Cloud Native** | 6 | 云原生支持 |
| 🟢 低 | **Setting Guide** | 7 | 配置指南 |
| 🟢 低 | **Biz Samples** | 13 | 业务示例 |
| 🟢 低 | **Others** | 3 | 其他页面 |

---

## 术语表

术语对照表请参考 `.kimi/skills/nablarch-translation/terms/TERMINOLOGY.md`

---

## 更新历史

| 日期 | 更新内容 |
|------|----------|
| 2025-02-16 | 完成 Adaptors 模块翻译 (16个文件)，整体进度达到 78.4% |
| 2025-02-16 | 完成 Development Tools 模块翻译 (55个文件) |
| 2025-02-16 | 完成 Testing Framework 模块翻译 (47个文件) |
| 2025-02-12 | 完成 Libraries 模块翻译 (49个文件) |
| 2025-02-11 | 完成 Batch 模块翻译 (29个文件) |
| 2025-02-11 | 完成 Web 模块翻译 (44个文件) |
| 2025-02-09 | 完成 Handlers 模块翻译 (74个文件) |
| 2025-02-08 | 初始化翻译项目，建立术语表 |

---

## 翻译规范

1. **准确性**：技术术语准确，符合中文技术文档习惯
2. **一致性**：同一术语全文统一翻译
3. **可读性**：语句通顺，符合中文表达习惯
4. **保留英文**：专有名词、Java类名保留英文
5. **无日文假名**：翻译后的文件不应包含日文假名（平假名/片假名）
