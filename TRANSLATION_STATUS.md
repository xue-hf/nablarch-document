# Nablarch 文档中文翻译进度

本文档记录了 Nablarch 框架文档的中文翻译进度。

## 翻译统计

| 项目 | 数量 |
|------|------|
| 总文件数 | 334 |
| 已翻译文件 | 176 |
| 未翻译文件 | 158 |
| 翻译进度 | **52.7%** |

> **判断标准**：文件中没有日文假名（平假名/片假名）即认为已翻译

---

## 分类统计

### 已翻译（按模块）

| 模块 | 已翻译 | 未翻译 | 进度 |
|------|--------|--------|------|
| 处理器 (Handlers) | 65 | 0 | 100% |
| Web 应用 | 23 | 0 | 100% |
| Web 服务 | 17 | 0 | 100% |
| 批处理 (Batch) | 24 | 5 | 82.8% |
| 关于 Nablarch | 4 | 1 | 80% |
| Nablarch 核心 | 1 | 0 | 100% |
| 适配器 (Adaptors) | 1 | 15 | 6.3% |
| 类库 (Libraries) | 33 | 16 | 67.3% |
| 空白项目 (Blank Project) | 1 | 19 | 5% |
| 其他 | 6 | 36 | 14.3% |
| 业务示例 (Biz Samples) | 0 | 15 | 0% |
| 开发工具 (Development Tools) | 0 | 52 | 0% |

---

## 已翻译文件列表（155个）

### 处理器 (Handlers)（65个）

- [x] `application_framework\application_framework\handlers\index.rst`
- [x] `application_framework\application_framework\handlers\batch\dbless_loop_handler.rst`
- [x] `application_framework\application_framework\handlers\batch\index.rst`
- [x] `application_framework\application_framework\handlers\batch\loop_handler.rst`
- [x] `application_framework\application_framework\handlers\batch\process_resident_handler.rst`
- [x] `application_framework\application_framework\handlers\common\ServiceAvailabilityCheckHandler.rst`
- [x] `application_framework\application_framework\handlers\common\database_connection_management_handler.rst`
- [x] `application_framework\application_framework\handlers\common\file_record_writer_dispose_handler.rst`
- [x] `application_framework\application_framework\handlers\common\global_error_handler.rst`
- [x] `application_framework\application_framework\handlers\common\index.rst`
- [x] `application_framework\application_framework\handlers\common\permission_check_handler.rst`
- [x] `application_framework\application_framework\handlers\common\request_handler_entry.rst`
- [x] `application_framework\application_framework\handlers\common\request_path_java_package_mapping.rst`
- [x] `application_framework\application_framework\handlers\common\thread_context_clear_handler.rst`
- [x] `application_framework\application_framework\handlers\common\thread_context_handler.rst`
- [x] `application_framework\application_framework\handlers\common\transaction_management_handler.rst`
- [x] `application_framework\application_framework\handlers\http_messaging\http_messaging_error_handler.rst`
- [x] `application_framework\application_framework\handlers\http_messaging\http_messaging_request_parsing_handler.rst`
- [x] `application_framework\application_framework\handlers\http_messaging\http_messaging_response_building_handler.rst`
- [x] `application_framework\application_framework\handlers\http_messaging\index.rst`
- [x] `application_framework\application_framework\handlers\mom_messaging\index.rst`
- [x] `application_framework\application_framework\handlers\mom_messaging\message_reply_handler.rst`
- [x] `application_framework\application_framework\handlers\mom_messaging\message_resend_handler.rst`
- [x] `application_framework\application_framework\handlers\mom_messaging\messaging_context_handler.rst`
- [x] `application_framework\application_framework\handlers\rest\body_convert_handler.rst`
- [x] `application_framework\application_framework\handlers\rest\cors_preflight_request_handler.rst`
- [x] `application_framework\application_framework\handlers\rest\index.rst`
- [x] `application_framework\application_framework\handlers\rest\jaxrs_access_log_handler.rst`
- [x] `application_framework\application_framework\handlers\rest\jaxrs_bean_validation_handler.rst`
- [x] `application_framework\application_framework\handlers\rest\jaxrs_response_handler.rst`
- [x] `application_framework\application_framework\handlers\standalone\data_read_handler.rst`
- [x] `application_framework\application_framework\handlers\standalone\duplicate_process_check_handler.rst`
- [x] `application_framework\application_framework\handlers\standalone\index.rst`
- [x] `application_framework\application_framework\handlers\standalone\main.rst`
- [x] `application_framework\application_framework\handlers\standalone\multi_thread_execution_handler.rst`
- [x] `application_framework\application_framework\handlers\standalone\process_stop_handler.rst`
- [x] `application_framework\application_framework\handlers\standalone\request_thread_loop_handler.rst`
- [x] `application_framework\application_framework\handlers\standalone\retry_handler.rst`
- [x] `application_framework\application_framework\handlers\standalone\status_code_convert_handler.rst`
- [x] `application_framework\application_framework\handlers\web\HttpErrorHandler.rst`
- [x] `application_framework\application_framework\handlers\web\SessionStoreHandler.rst`
- [x] `application_framework\application_framework\handlers\web\csrf_token_verification_handler.rst`
- [x] `application_framework\application_framework\handlers\web\forwarding_handler.rst`
- [x] `application_framework\application_framework\handlers\web\health_check_endpoint_handler.rst`
- [x] `application_framework\application_framework\handlers\web\hot_deploy_handler.rst`
- [x] `application_framework\application_framework\handlers\web\http_access_log_handler.rst`
- [x] `application_framework\application_framework\handlers\web\http_character_encoding_handler.rst`
- [x] `application_framework\application_framework\handlers\web\http_request_java_package_mapping.rst`
- [x] `application_framework\application_framework\handlers\web\http_response_handler.rst`
- [x] `application_framework\application_framework\handlers\web\http_rewrite_handler.rst`
- [x] `application_framework\application_framework\handlers\web\index.rst`
- [x] `application_framework\application_framework\handlers\web\keitai_access_handler.rst`
- [x] `application_framework\application_framework\handlers\web\multipart_handler.rst`
- [x] `application_framework\application_framework\handlers\web\nablarch_tag_handler.rst`
- [x] `application_framework\application_framework\handlers\web\normalize_handler.rst`
- [x] `application_framework\application_framework\handlers\web\post_resubmit_prevent_handler.rst`
- [x] `application_framework\application_framework\handlers\web\resource_mapping.rst`
- [x] `application_framework\application_framework\handlers\web\secure_handler.rst`
- [x] `application_framework\application_framework\handlers\web\session_concurrent_access_handler.rst`
- [x] `application_framework\application_framework\handlers\web_interceptor\InjectForm.rst`
- [x] `application_framework\application_framework\handlers\web_interceptor\index.rst`
- [x] `application_framework\application_framework\handlers\web_interceptor\on_double_submission.rst`
- [x] `application_framework\application_framework\handlers\web_interceptor\on_error.rst`
- [x] `application_framework\application_framework\handlers\web_interceptor\on_errors.rst`
- [x] `application_framework\application_framework\handlers\web_interceptor\use_token.rst`

### Web 应用（23个）

- [x] `application_framework\application_framework\web\application_design.rst`
- [x] `application_framework\application_framework\web\architecture.rst`
- [x] `application_framework\application_framework\web\feature_details.rst`
- [x] `application_framework\application_framework\web\feature_details\error_message.rst`
- [x] `application_framework\application_framework\web\feature_details\forward_error_page.rst`
- [x] `application_framework\application_framework\web\feature_details\jsp_session.rst`
- [x] `application_framework\application_framework\web\feature_details\nablarch_servlet_context_listener.rst`
- [x] `application_framework\application_framework\web\feature_details\view\other.rst`
- [x] `application_framework\application_framework\web\feature_details\web_front_controller.rst`
- [x] `application_framework\application_framework\web\getting_started\client_create\client_create1.rst`
- [x] `application_framework\application_framework\web\getting_started\client_create\client_create2.rst`
- [x] `application_framework\application_framework\web\getting_started\client_create\client_create3.rst`
- [x] `application_framework\application_framework\web\getting_started\client_create\client_create4.rst`
- [x] `application_framework\application_framework\web\getting_started\client_create\index.rst`
- [x] `application_framework\application_framework\web\getting_started\index.rst`
- [x] `application_framework\application_framework\web\getting_started\popup\index.rst`
- [x] `application_framework\application_framework\web\getting_started\project_bulk_update\index.rst`
- [x] `application_framework\application_framework\web\getting_started\project_delete\index.rst`
- [x] `application_framework\application_framework\web\getting_started\project_download\index.rst`
- [x] `application_framework\application_framework\web\getting_started\project_search\index.rst`
- [x] `application_framework\application_framework\web\getting_started\project_update\index.rst`
- [x] `application_framework\application_framework\web\getting_started\project_upload\index.rst`
- [x] `application_framework\application_framework\web\index.rst`

### Web 服务（17个）

- [x] `application_framework\application_framework\web_service\functional_comparison.rst`
- [x] `application_framework\application_framework\web_service\http_messaging\application_design.rst`
- [x] `application_framework\application_framework\web_service\http_messaging\architecture.rst`
- [x] `application_framework\application_framework\web_service\http_messaging\feature_details.rst`
- [x] `application_framework\application_framework\web_service\http_messaging\getting_started\getting_started.rst`
- [x] `application_framework\application_framework\web_service\http_messaging\getting_started\save\index.rst`
- [x] `application_framework\application_framework\web_service\http_messaging\index.rst`
- [x] `application_framework\application_framework\web_service\index.rst`
- [x] `application_framework\application_framework\web_service\rest\application_design.rst`
- [x] `application_framework\application_framework\web_service\rest\architecture.rst`
- [x] `application_framework\application_framework\web_service\rest\feature_details.rst`
- [x] `application_framework\application_framework\web_service\rest\feature_details\resource_signature.rst`
- [x] `application_framework\application_framework\web_service\rest\getting_started\create\index.rst`
- [x] `application_framework\application_framework\web_service\rest\getting_started\index.rst`
- [x] `application_framework\application_framework\web_service\rest\getting_started\search\index.rst`
- [x] `application_framework\application_framework\web_service\rest\getting_started\update\index.rst`
- [x] `application_framework\application_framework\web_service\rest\index.rst`

### 批处理 (Batch)（24个）

- [x] `application_framework\application_framework\batch\functional_comparison.rst`
- [x] `application_framework\application_framework\batch\index.rst`
- [x] `application_framework\application_framework\batch\jsr352\application_design.rst`
- [x] `application_framework\application_framework\batch\jsr352\architecture.rst`
- [x] `application_framework\application_framework\batch\jsr352\feature_details.rst`
- [x] `application_framework\application_framework\batch\jsr352\feature_details\database_reader.rst`
- [x] `application_framework\application_framework\batch\jsr352\feature_details\operation_policy.rst`
- [x] `application_framework\application_framework\batch\jsr352\feature_details\operator_notice_log.rst`
- [x] `application_framework\application_framework\batch\jsr352\feature_details\pessimistic_lock.rst`
- [x] `application_framework\application_framework\batch\jsr352\feature_details\progress_log.rst`
- [x] `application_framework\application_framework\batch\jsr352\feature_details\run_batch_application.rst`
- [x] `application_framework\application_framework\batch\jsr352\getting_started\batchlet\index.rst`
- [x] `application_framework\application_framework\batch\jsr352\getting_started\chunk\index.rst`
- [x] `application_framework\application_framework\batch\jsr352\getting_started\getting_started.rst`
- [x] `application_framework\application_framework\batch\jsr352\index.rst`
- [x] `application_framework\application_framework\batch\nablarch_batch\application_design.rst`
- [x] `application_framework\application_framework\batch\nablarch_batch\feature_details.rst`
- [x] `application_framework\application_framework\batch\nablarch_batch\feature_details\nablarch_batch_error_process.rst`
- [x] `application_framework\application_framework\batch\nablarch_batch\feature_details\nablarch_batch_multiple_process.rst`
- [x] `application_framework\application_framework\batch\nablarch_batch\feature_details\nablarch_batch_pessimistic_lock.rst`
- [x] `application_framework\application_framework\batch\nablarch_batch\feature_details\nablarch_batch_retention_state.rst`
- [x] `application_framework\application_framework\batch\nablarch_batch\getting_started\getting_started.rst`
- [x] `application_framework\application_framework\batch\nablarch_batch\getting_started\nablarch_batch\index.rst`
- [x] `application_framework\application_framework\batch\nablarch_batch\index.rst`

### 类库 (Libraries)（33个）

- [x] `application_framework\application_framework\libraries\authorization\permission_check.rst`
- [x] `application_framework\application_framework\libraries\authorization\role_check.rst`
- [x] `application_framework\application_framework\libraries\bean_util.rst`
- [x] `application_framework\application_framework\libraries\code.rst`
- [x] `application_framework\application_framework\libraries\data_converter.rst`
- [x] `application_framework\application_framework\libraries\data_io\data_bind.rst`
- [x] `application_framework\application_framework\libraries\data_io\data_format.rst`
- [x] `application_framework\application_framework\libraries\data_io\data_format\format_definition.rst`
- [x] `application_framework\application_framework\libraries\data_io\data_format\multi_format_example.rst`
- [x] `application_framework\application_framework\libraries\data_io\functional_comparison.rst`
- [x] `application_framework\application_framework\libraries\date.rst`
- [x] `application_framework\application_framework\libraries\db_double_submit.rst`
- [x] `application_framework\application_framework\libraries\exclusive_control.rst`
- [x] `application_framework\application_framework\libraries\file_path_management.rst`
- [x] `application_framework\application_framework\libraries\format.rst`
- [x] `application_framework\application_framework\libraries\mail.rst`
- [x] `application_framework\application_framework\libraries\message.rst`
- [x] `application_framework\application_framework\libraries\repository.rst`
- [x] `application_framework\application_framework\libraries\service_availability.rst`
- [x] `application_framework\application_framework\libraries\session_store.rst`
- [x] `application_framework\application_framework\libraries\session_store\create_example.rst`
- [x] `application_framework\application_framework\libraries\session_store\update_example.rst`
- [x] `application_framework\application_framework\libraries\stateless_web_app.rst`
- [x] `application_framework\application_framework\libraries\static_data_cache.rst`
- [x] `application_framework\application_framework\libraries\system_messaging.rst`
- [x] `application_framework\application_framework\libraries\system_messaging\http_system_messaging.rst`
- [x] `application_framework\application_framework\libraries\system_messaging\mom_system_messaging.rst`
- [x] `application_framework\application_framework\libraries\tag.rst`
- [x] `application_framework\application_framework\libraries\transaction.rst`
- [x] `application_framework\application_framework\libraries\utility.rst`
- [x] `application_framework\application_framework\libraries\validation.rst`
- [x] `application_framework\application_framework\libraries\validation\bean_validation.rst`
- [x] `application_framework\application_framework\libraries\validation\functional_comparison.rst`
- [x] `application_framework\application_framework\libraries\validation\nablarch_validation.rst`

### 关于 Nablarch（4个）

- [x] `about_nablarch\concept.rst`
- [x] `about_nablarch\index.rst`
- [x] `about_nablarch\license.rst`
- [x] `about_nablarch\mvn_module.rst`

### Nablarch 核心（1个）

- [x] `application_framework\application_framework\nablarch\architecture.rst`
- [x] `application_framework\application_framework\nablarch\big_picture.rst`
- [x] `application_framework\application_framework\nablarch\index.rst`
- [x] `application_framework\application_framework\nablarch\platform.rst`
- [x] `application_framework\application_framework\nablarch\policy.rst`

### 应用框架（1个）

- [x] `application_framework\application_framework\index.rst`
- [x] `application_framework\index.rst`

### 空白项目 (Blank Project)（1个）

- [x] `application_framework\application_framework\blank_project\index.rst`

### 适配器 (Adaptors)（1个）

- [x] `application_framework\adaptors\index.rst`

---

## 未翻译文件列表（158个）

### 与原文完全相同的文件（44个）

这些文件与 `ja/` 目录下的日文原文完全一致，尚未开始翻译：

**类库 (Libraries)**（10个）

- [ ] `application_framework\application_framework\libraries\data_io\data_format\multi_format_example.rst`
- [ ] `application_framework\application_framework\libraries\database_management.rst`
- [ ] `application_framework\application_framework\libraries\index.rst`
- [ ] `application_framework\application_framework\libraries\permission_check.rst`
- [ ] `application_framework\application_framework\libraries\session_store\create_example.rst`
- [ ] `application_framework\application_framework\libraries\session_store\update_example.rst`
- [ ] `application_framework\application_framework\libraries\tag\tag_reference.rst`
- [ ] `application_framework\application_framework\libraries\validation.rst`
- [ ] `application_framework\application_framework\libraries\validation\functional_comparison.rst`

**空白项目 (Blank Project)**（4个）

- [ ] `application_framework\application_framework\blank_project\FirstStep.rst`
- [ ] `application_framework\application_framework\blank_project\FirstStepContainer.rst`
- [ ] `application_framework\application_framework\blank_project\ModifySettings.rst`
- [ ] `application_framework\application_framework\blank_project\setup_blankProject\setup_Java21.rst`

**处理器 (Handlers)**（2个）

- [ ] `application_framework\application_framework\handlers\common\index.rst`
- [ ] `application_framework\application_framework\handlers\index.rst`

**其他**（28个）
- [ ] 应用框架配置、消息处理、开发工具、业务示例等

### 包含日文假名的文件（135个）

这些文件包含日文假名（如ア、イ、ウ、あ、い、う等），说明仍有日文内容未翻译：

**类库 (Libraries)**（34个）

- [ ] `application_framework\application_framework\libraries\data_io\data_format\format_definition.rst`
- [ ] `application_framework\application_framework\libraries\database\database.rst`
- [ ] `application_framework\application_framework\libraries\database\functional_comparison.rst`
- [ ] `application_framework\application_framework\libraries\database\generator.rst`
- [ ] `application_framework\application_framework\libraries\database\universal_dao.rst`
- [ ] `application_framework\application_framework\libraries\log.rst`
- [ ] `application_framework\application_framework\libraries\log\failure_log.rst`
- [ ] `application_framework\application_framework\libraries\log\http_access_log.rst`
- [ ] `application_framework\application_framework\libraries\log\jaxrs_access_log.rst`
- [ ] `application_framework\application_framework\libraries\log\messaging_log.rst`
- [ ] `application_framework\application_framework\libraries\log\performance_log.rst`
- [ ] `application_framework\application_framework\libraries\log\sql_log.rst`
- [ ] `application_framework\application_framework\libraries\repository.rst`
- [ ] `application_framework\application_framework\libraries\session_store.rst`
- [ ] `application_framework\application_framework\libraries\stateless_web_app.rst`
- [ ] `application_framework\application_framework\libraries\static_data_cache.rst`
- [ ] `application_framework\application_framework\libraries\system_messaging.rst`
- [ ] `application_framework\application_framework\libraries\system_messaging\http_system_messaging.rst`
- [ ] `application_framework\application_framework\libraries\system_messaging\mom_system_messaging.rst`
- [ ] `application_framework\application_framework\libraries\tag.rst`
- [ ] `application_framework\application_framework\libraries\transaction.rst`
- [ ] `application_framework\application_framework\libraries\utility.rst`
- [ ] `application_framework\application_framework\libraries\validation\bean_validation.rst`
- [ ] `application_framework\application_framework\libraries\validation\nablarch_validation.rst`

**空白项目 (Blank Project)**（19个）

- [ ] `application_framework\application_framework\blank_project\CustomizeDB.rst`
- [ ] `application_framework\application_framework\blank_project\MavenModuleStructures\index.rst`
- [ ] `application_framework\application_framework\blank_project\addin_gsp.rst`
- [ ] `application_framework\application_framework\blank_project\beforeFirstStep.rst`
- [ ] `application_framework\application_framework\blank_project\firstStep_appendix\ResiBatchReboot.rst`
- [ ] `application_framework\application_framework\blank_project\firstStep_appendix\firststep_complement.rst`
- [ ] `application_framework\application_framework\blank_project\maven.rst`
- [ ] `application_framework\application_framework\blank_project\setup_blankProject\setup_Jbatch.rst`
- [ ] `application_framework\application_framework\blank_project\setup_blankProject\setup_NablarchBatch.rst`
- [ ] `application_framework\application_framework\blank_project\setup_blankProject\setup_NablarchBatch_Dbless.rst`
- [ ] `application_framework\application_framework\blank_project\setup_blankProject\setup_Web.rst`
- [ ] `application_framework\application_framework\blank_project\setup_blankProject\setup_WebService.rst`
- [ ] `application_framework\application_framework\blank_project\setup_containerBlankProject\setup_ContainerBatch.rst`
- [ ] `application_framework\application_framework\blank_project\setup_containerBlankProject\setup_ContainerBatch_Dbless.rst`
- [ ] `application_framework\application_framework\blank_project\setup_containerBlankProject\setup_ContainerWeb.rst`
- [ ] `application_framework\application_framework\blank_project\setup_containerBlankProject\setup_ContainerWebService.rst`

**适配器 (Adaptors)**（15个）

- [ ] `application_framework\adaptors\doma_adaptor.rst`
- [ ] `application_framework\adaptors\jaxrs_adaptor.rst`
- [ ] `application_framework\adaptors\jsr310_adaptor.rst`
- [ ] `application_framework\adaptors\lettuce_adaptor.rst`
- [ ] `application_framework\adaptors\lettuce_adaptor\redishealthchecker_lettuce_adaptor.rst`
- [ ] `application_framework\adaptors\lettuce_adaptor\redisstore_lettuce_adaptor.rst`
- [ ] `application_framework\adaptors\log_adaptor.rst`
- [ ] `application_framework\adaptors\mail_sender_freemarker_adaptor.rst`
- [ ] `application_framework\adaptors\mail_sender_thymeleaf_adaptor.rst`
- [ ] `application_framework\adaptors\mail_sender_velocity_adaptor.rst`
- [ ] `application_framework\adaptors\micrometer_adaptor.rst`
- [ ] `application_framework\adaptors\router_adaptor.rst`
- [ ] `application_framework\adaptors\slf4j_adaptor.rst`
- [ ] `application_framework\adaptors\web_thymeleaf_adaptor.rst`
- [ ] `application_framework\adaptors\webspheremq_adaptor.rst`

**开发工具 (Development Tools)**（52个）

- [ ] `development_tools\index.rst`
- [ ] `development_tools\java_static_analysis\index.rst`
- [ ] `development_tools\testing_framework\guide\development_guide\05_UnitTestGuide\01_ClassUnitTest\01_entityUnitTest\01_entityUnitTestWithBeanValidation.rst`
- [ ] `development_tools\testing_framework\guide\development_guide\05_UnitTestGuide\01_ClassUnitTest\01_entityUnitTest\02_entityUnitTestWithNablarchValidation.rst`
- [ ] `development_tools\testing_framework\guide\development_guide\05_UnitTestGuide\01_ClassUnitTest\01_entityUnitTest\index.rst`
- [ ] `development_tools\testing_framework\guide\development_guide\05_UnitTestGuide\01_ClassUnitTest\02_componentUnitTest.rst`
- [ ] `development_tools\testing_framework\guide\development_guide\05_UnitTestGuide\01_ClassUnitTest\index.rst`
- [ ] `development_tools\testing_framework\guide\development_guide\05_UnitTestGuide\02_RequestUnitTest\batch.rst`
- [ ] ... 以及其他 45 个开发工具相关文件

**业务示例 (Biz Samples)**（15个）
- [ ] `biz_samples\01\0101_PBKDF2PasswordEncryptor.rst`
- [ ] `biz_samples\01\index.rst`
- [ ] `biz_samples\03\index.rst`
- [ ] ... 以及其他 13 个业务示例文件

---

## 优先级建议

### 高优先级（核心入门文档）

1. `application_framework/application_framework/blank_project/FirstStep.rst` - 入门第一步
2. `application_framework/application_framework/blank_project/FirstStepContainer.rst`
3. `application_framework/application_framework/blank_project/ModifySettings.rst`
4. `application_framework/application_framework/libraries/` 下的核心类库文档
5. `application_framework/application_framework/handlers/` 下剩余的处理器文档（仅剩2个）

### 中优先级（功能模块）

- `application_framework/adaptors/` 下的适配器文档
- `application_framework/application_framework/libraries/` 下剩余的数据库、日志相关文档
- `application_framework/application_framework/messaging/` 下的消息处理文档

### 低优先级（高级/扩展功能）

- `biz_samples/` 下的业务示例
- `development_tools/` 下的开发工具文档

---

## 更新记录

| 日期 | 更新内容 |
|------|----------|
| 2026-02-15 | 自动更新翻译进度，已翻译 155 个文件，进度 46.4% |

---

## 如何贡献翻译

1. 从「未翻译文件列表」中选择要翻译的文件
2. 参考 `ja/` 目录下的对应日文原文进行翻译
3. 将翻译后的文件保存到 `zh_CN/` 目录的对应位置
4. 确保翻译后的文件中**不包含日文假名**（平假名/片假名）
5. 运行检查脚本更新翻译进度
6. 提交 Pull Request

### 翻译规范

- 保持与原文档的 RST 格式一致
- 参考 `.kimi/skills/nablarch-translation/terms/TERMINOLOGY.md` 术语表
- 技术术语首次出现时标注日文或英文
- **确保最终文件中没有日文假名**

---
