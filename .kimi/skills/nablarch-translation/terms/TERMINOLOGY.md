# Nablarch 文档翻译术语表

本文档记录 Nablarch 框架文档的日文-中文术语对照表。

**使用说明：**
- AI 翻译时优先参考本表
- 发现新术语时自动添加到本表
- 保持术语翻译的一致性

---

## 核心概念

| 日文 | 中文 | 英文 | 备注 |
|------|------|------|------|
| コンセプト | 思想 | Concept | Nablarch のコンセプト → Nablarch 的思想 |
| アーキテクチャ | 架构 | Architecture | |
| ポリシー | 方针/策略 | Policy | |
| プラットフォーム | 平台 | Platform | |
| フレームワーク | 框架 | Framework | |
| ビッグピクチャ | 整体架构 | Big Picture | |

## 应用组件

| 日文 | 中文 | 英文 | 备注 |
|------|------|------|------|
| アプリケーション | 应用 | Application | 也可保留英文 |
| アクションクラス | Action类 | Action Class | 类名保留英文 |
| フォームクラス | Form类 | Form Class | 也可说"表单类" |
| エンティティクラス | Entity类 | Entity Class | 也可说"实体类" |
| 業務ロジック | 业务逻辑 | Business Logic | |
| 責務 | 职责 | Responsibility | |
| 責務配置 | 职责配置 | Responsibility Assignment | |
| コンポーネント | 组件 | Component | |
| モジュール | 模块 | Module | |

## 处理器与拦截器

| 日文 | 中文 | 英文 | 备注 |
|------|------|------|------|
| ハンドラ | handler/处理器 | Handler | 标题用 handler，正文可用"处理器" |
| ハンドラキュー | handler队列 | Handler Queue | 或 handler queue |
| インターセプタ | 拦截器 | Interceptor | 也可保留英文 |
| フィルタ | 过滤器 | Filter | |
| グローバルエラーハンドラ | 全局错误handler | Global Error Handler | |

## 数据处理

| 日文 | 中文 | 英文 | 备注 |
|------|------|------|------|
| バリデーション | 验证 | Validation | 也可说"校验" |
| バリデータ | 验证器 | Validator | |
| 入力値 | 输入值 | Input Value | |
| 入力値のチェック | 输入值校验 | Input Validation | |
| データレコード | 数据记录 | Data Record | |
| マッピング | 映射 | Mapping | |
| 永続化 | 持久化 | Persistence | |
| ファイル入出力 | 文件输入输出 | File I/O | |

## 批处理

| 日文 | 中文 | 英文 | 备注 |
|------|------|------|------|
| バッチ | Batch | Batch | 保留英文 |
| バッチアプリケーション | Batch应用 | Batch Application | |
| バッチ処理 | 批处理 | Batch Processing | |
| データリーダ | DataReader | DataReader | 保留英文 |
| チャンク | Chunk | Chunk | 保留英文 |
| バッチレット | Batchlet | Batchlet | 保留英文 |
| アイテムリーダ | ItemReader | ItemReader | Jakarta Batch 组件 |
| アイテムプロセッサ | ItemProcessor | ItemProcessor | Jakarta Batch 组件 |
| アイテムライタ | ItemWriter | ItemWriter | Jakarta Batch 组件 |
| ステップ | 步骤 | Step | |
| ジョブ | 作业 | Job | |
| ジョブ定義 | 作业定义 | Job Definition | |
| ジョブスケジューラ | 作业调度器 | Job Scheduler | |
| コミット | 提交 | Commit | |
| ロールバック | 回滚 | Rollback | |
| リスナー | 监听器 | Listener | Jakarta Batch 中的监听器 |
| リトライ | 重试 | Retry | |
| スキップ | 跳过 | Skip | 跳过异常数据 |
| 進捗ログ | 进度日志 | Progress Log | |
| 常駐バッチ | 常驻Batch | Resident Batch | 持续运行的批处理 |
| バッチステータス | Batch状态 | Batch Status | |
| 終了ステータス | 结束状态/退出状态 | Exit Status | |

## Web 相关

| 日文 | 中文 | 英文 | 备注 |
|------|------|------|------|
| ウェブアプリケーション | Web应用 | Web Application | |
| Webフロントコントローラ | Web前端控制器 | Web Front Controller | |
| リクエスト | 请求 | Request | |
| レスポンス | 响应 | Response | |
| セッション | 会话 | Session | 或 Session |
| クッキー | Cookie | Cookie | 保留英文 |
| サーブレット | Servlet | Servlet | 保留英文 |
| JSP | JSP | JSP | 保留英文 |
| URIとアクションクラスのマッピング | URI与Action类的映射 | URI-Action Mapping | |

## 数据库

| 日文 | 中文 | 英文 | 备注 |
|------|------|------|------|
| データベース | 数据库 | Database | |
| テーブル | 表/表格 | Table | |
| カラム | 列/字段 | Column | |
| レコード | 记录 | Record | |
| トランザクション | 事务 | Transaction | |
| DAO | DAO | DAO | 保留英文 |
| 排他制御 | 并发控制/排他控制 | Exclusive Control | |
| 悲観的ロック | 悲观锁 | Pessimistic Lock | |
| 楽観的ロック | 乐观锁 | Optimistic Lock | |
| カーソル | 游标 | Cursor | |
| データベース接続 | 数据库连接 | Database Connection | |
| コネクション | 连接 | Connection | |

## 日志与监控

| 日文 | 中文 | 英文 | 备注 |
|------|------|------|------|
| ログ | 日志 | Log | |
| アクセスログ | 访问日志 | Access Log | |
| エラーログ | 错误日志 | Error Log | |
| パフォーマンスログ | 性能日志 | Performance Log | |
| メトリクス | 指标/度量 | Metrics | |
| 運用担当者 | 运维人员/运营人员 | Operator | |
| 運用担当者向けログ | 运维日志 | Operator Log | 给运维人员看的日志 |
| 障害監視 | 故障监控 | Failure Monitoring | |

## 消息处理

| 日文 | 中文 | 英文 | 备注 |
|------|------|------|------|
| メッセージ | 消息 | Message | |
| メッセージング | 消息处理 | Messaging | |
| MOM | MOM | MOM | 保留英文 |
| HTTPメッセージング | HTTP消息处理 | HTTP Messaging | |
| MOMメッセージング | MOM消息处理 | MOM Messaging | |
| 電文 | 电文 | Message | 消息报文 |
| 要求電文 | 请求电文 | Request Message | |
| 応答電文 | 响应电文 | Response Message | |

## 适配器

| 日文 | 中文 | 英文 | 备注 |
|------|------|------|------|
| アダプタ | 适配器 | Adaptor | 或 Adapter |
| Domaアダプタ | Doma适配器 | Doma Adaptor | |
| Lettuceアダプタ | Lettuce适配器 | Lettuce Adaptor | |
| ログアダプタ | 日志适配器 | Log Adaptor | |

## 文档结构词

| 日文 | 中文 | 英文 | 备注 |
|------|------|------|------|
| 目次 | 目录 | Table of Contents | |
| 概要 | 概述/概要 | Overview | |
| 機能概要 | 功能概述 | Functional Overview | |
| 使用方法 | 使用方法 | Usage | |
| 制約 | 约束/限制 | Constraint | |
| 注意事項 | 注意事项 | Notes | |
| ヒント | 提示/建议 | Tip | |
| 警告 | 警告 | Warning | |
| 重要 | 重要 | Important | |

## 开发相关

| 日文 | 中文 | 英文 | 备注 |
|------|------|------|------|
| プロジェクト | 项目 | Project | |
| ブランクプロジェクト | 空白项目 | Blank Project | |
| 設定 | 设置/配置 | Configuration | |
| 環境 | 环境 | Environment | |
| ライブラリ | 库 | Library | 或 library |
| 依存関係 | 依赖关系 | Dependency | |
| システムリポジトリ | 系统仓库 | System Repository | |
| 初期化 | 初始化 | Initialization | |

## 测试相关

| 日文 | 中文 | 英文 | 备注 |
|------|------|------|------|
| テスト | 测试 | Test | |
| 単体テスト | 单元测试 | Unit Test | |
| 結合テスト | 集成测试 | Integration Test | |
| モック | 模拟对象/Mock | Mock | 或 mock |
| スタブ | 桩对象/Stub | Stub | 或 stub |
| テスト容易性 | 可测试性 | Testability | |

## 异常处理

| 日文 | 中文 | 英文 | 备注 |
|------|------|------|------|
| 例外 | 异常 | Exception | |
| エラー | 错误 | Error | |
| 検査例外 | 受检异常 | Checked Exception | |
| 実行時例外 | 运行时异常 | Runtime Exception | |

## 进程与线程

| 日文 | 中文 | 英文 | 备注 |
|------|------|------|------|
| プロセス | 进程 | Process | |
| スレッド | 线程 | Thread | |
| スレッドセーフ | 线程安全 | Thread Safe | |
| マルチスレッド | 多线程 | Multi-thread | |
| マルチプロセス | 多进程 | Multi-process | |
| 多重起動 | 重复启动 | Multiple Launch | |
| 多重起動防止 | 防止重复启动 | Duplicate Launch Prevention | |
| プロセス常駐化 | 进程常驻 | Process Resident | |

---

## 保留不译的词汇

以下词汇通常保留日文原文或英文原文：

- Java 类名（如 `nablarch.fw.web.handler.HttpAccessLogHandler`）
- 注解名称（如 `@Table`, `@Column`, `@Named`, `@Dependent`）
- 专有名词（如 Jakarta EE, Maven, JUnit, H2, CDI）
- 代码中的变量名、方法名
- Jakarta Batch 规范术语（如 ItemReader, ItemProcessor, ItemWriter, Batchlet, Chunk）

---

## 更新记录

| 日期 | 更新内容 | 更新者 |
|------|----------|--------|
| 2026-02-14 | 初始版本，整理核心术语 | AI |
| 2026-02-15 | 添加 Batch 相关术语（ItemReader/ItemProcessor/ItemWriter/Listener/进度日志/运维日志/悲观锁等） | AI |
| 2026-02-15 | 整理术语表，统一格式，删除 JSON 版本 | AI |

---

**维护说明：**
- 本术语表由 AI 自动维护
- 翻译过程中发现的新术语会自动添加
- 用户可通过指令要求更新术语
