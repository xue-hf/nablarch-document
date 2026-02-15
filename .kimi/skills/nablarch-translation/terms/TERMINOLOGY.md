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
| 概念モデル | 概念模型 | Conceptual Model | 架构概念 |

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
| アプリケーションレイヤー | 应用层 | Application Layer | 架构层次 |
| 業務アクション | 业务Action | Business Action | 业务处理Action |
| 業務処理 | 业务处理 | Business Processing | |

## 处理器与拦截器

| 日文 | 中文 | 英文 | 备注 |
|------|------|------|------|
| ハンドラ | handler/处理器 | Handler | 标题用 handler，正文可用"处理器" |
| ハンドラキュー | handler队列 | Handler Queue | 或 handler queue |
| インターセプタ | 拦截器 | Interceptor | 也可保留英文 |
| フィルタ | 过滤器 | Filter | |
| グローバルエラーハンドラ | 全局错误handler | Global Error Handler | |
| 後続ハンドラ | 后续handler | Subsequent Handler | handler链中的下一个 |
| 呼び出し | 调用 | Invocation/Call | 方法调用 |
| コールバック | 回调 | Callback | 事件回调 |
| コールバック処理 | 回调处理 | Callback Processing | 线程回调机制 |
| 委譲先 | 委托目标 | Delegation Target | 委托处理的handler |
| 実行コンテキスト | 执行上下文 | Execution Context | 运行时上下文 |

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
| コンバート/変換 | 转换 | Convert | |
| コンバータ | 转换器 | Converter | |
| コンバータテーブル | 转换器表 | Convertor Table | 类型映射 |
| 型変換 | 类型转换 | Type Conversion | |
| 型パラメータ | 型参数 | Type Parameter | 泛型相关 |
| 具象クラス | 具体类 | Concrete Class | 与抽象类相对 |
| フィールドコンバータ | 字段转换器 | Field Converter | 数据转换 |
| データバインド | 数据绑定 | Data Bind | 数据与Bean映射 |
| データリーダ | DataReader | DataReader | 数据读取接口 |
| データの読み込み | 数据的读取 | Data Reading | 输入处理 |
| データの終端 | 数据末端 | End of Data | 数据结束标记 |
| 処理対象データ | 处理对象数据 | Target Data | 待处理的数据 |
| 処理対象レコード | 处理对象记录 | Target Record | 待处理的记录 |
| 順次読み込み | 顺序读取 | Sequential Reading | 数据读取方式 |
| データ不整合 | 数据不一致 | Data Inconsistency | 数据异常 |
| 階層構造 | 层次结构 | Hierarchical Structure | XML/JSON结构 |
| ルート要素 | 根元素 | Root Element | XML概念 |
| ネストした要素 | 嵌套元素 | Nested Element | XML/JSON结构 |
| 配列要素 | 数组元素 | Array Element | JSON概念 |
| 添字 | 下标 | Index | 数组索引 |
| ファイル入出力 | 文件输入输出 | File I/O | |

## 批处理

| 日文 | 中文 | 英文 | 备注 |
|------|------|------|------|
| バッチ | Batch | Batch | 保留英文 |
| バッチアプリケーション | Batch应用 | Batch Application | |
| バッチ処理 | 批处理 | Batch Processing | |
| チャンク | Chunk | Chunk | 保留英文 |
| バッチレット | Batchlet | Batchlet | 保留英文 |
| アイテムリーダ | ItemReader | ItemReader | Jakarta Batch 组件 |
| アイテムプロセッサ | ItemProcessor | ItemProcessor | Jakarta Batch 组件 |
| アイテムライタ | ItemWriter | ItemWriter | Jakarta Batch 组件 |
| ステップ | 步骤 | Step | |
| ジョブ | 作业 | Job | |
| ジョブ定義 | 作业定义 | Job Definition | |
| ジョブスケジューラ | 作业调度器 | Job Scheduler | |
| リスナー | 监听器 | Listener | Jakarta Batch 中的监听器 |
| スキップ | 跳过 | Skip | 跳过异常数据 |
| 進捗ログ | 进度日志 | Progress Log | |
| 常駐バッチ | 常驻Batch | Resident Batch | 持续运行的批处理 |
| 都度起動バッチ | 按需启动批处理 | On-demand Batch | 与常驻Batch相对 |
| バッチステータス | Batch状态 | Batch Status | |
| 終了ステータス | 结束状态/退出状态 | Exit Status | |
| 一括更新 | 批量更新 | Bulk Update | |
| 一括登録 | 批量注册 | Bulk Insert | |
| 一括処理 | 批量处理 | Bulk Processing | |
| 空回り | 空转 | Idle Running | 批处理等待状态 |

## Web 相关

| 日文 | 中文 | 英文 | 备注 |
|------|------|------|------|
| ウェブアプリケーション | Web应用 | Web Application | |
| Webフロントコントローラ | Web前端控制器 | Web Front Controller | |
| リクエスト | 请求 | Request | |
| レスポンス | 响应 | Response | |
| リクエストボディ | 请求主体 | Request Body | |
| レスポンスボディ | 响应主体 | Response Body | |
| リクエストパス | 请求路径 | Request Path | URL路径 |
| リクエストパターン | 请求模式 | Request Pattern | 路径匹配模式 |
| リクエストID | 请求ID | Request ID | 请求标识 |
| 内部リクエストID | 内部请求ID | Internal Request ID | 转发时的请求ID |
| セッション | 会话 | Session | 或 Session |
| クッキー | Cookie | Cookie | 保留英文 |
| サーブレット | Servlet | Servlet | 保留英文 |
| JSP | JSP | JSP | 保留英文 |
| URIとアクションクラスのマッピング | URI与Action类的映射 | URI-Action Mapping | |
| ポップアップ画面 | 弹出窗口画面 | Popup Window | |
| ダイアログ | 对话框 | Dialog | |
| フォワード | forward/跳转 | Forward | |
| 内部フォワード | 内部转发 | Internal Forward | |
| サーブレットフォワード | Servlet forward | Servlet Forward | |
| リダイレクト | redirect/重定向 | Redirect | |
| ディスパッチ | 分发 | Dispatch | |
| セッションストア | 会话存储 | Session Store | |
| リクエストスコープ | 请求作用域 | Request Scope | |
| ウィンドウスコープ | 窗口作用域 | Window Scope | |
| スティッキーセッション | 粘性会话 | Sticky Session | 负载均衡会话保持 |
| プルダウン | 下拉框 | Dropdown/Pulldown | |
| テキストボックス | 文本框 | Text Box | |
| ボタン | 按钮 | Button | |
| リンク | 链接 | Link | |
| メニュー | 菜单 | Menu | |
| サイドメニュー | 侧边菜单 | Side Menu | |
| ヘッダメニュー | 头部菜单 | Header Menu | |
| 画面 | 画面/页面 | Screen/Page | |
| 画面表示 | 画面显示 | Screen Display | UI显示 |
| 画面遷移 | 页面跳转 | Page Transition | |
| 初期表示 | 初始显示 | Initial Display | |
| 入力項目 | 输入项目 | Input Item | |
| 入力欄 | 输入栏 | Input Field | |
| 入力エラー | 输入错误 | Input Error | |
| エラーメッセージ | 错误消息 | Error Message | |
| エラーページ | 错误页面 | Error Page | 错误显示页面 |
| 完了画面 | 完成画面 | Completion Screen | |
| 確認画面 | 确认画面 | Confirmation Screen | |
| 詳細画面 | 详情画面 | Detail Screen | |
| 一覧画面 | 列表画面 | List Screen | |
| 検索画面 | 搜索画面 | Search Screen | |
| 検索条件 | 搜索条件 | Search Condition | |
| 検索結果 | 搜索结果 | Search Result | |
| ページング | 分页 | Paging | |
| ソート | 排序 | Sort | |
| ソート順 | 排序顺序 | Sort Order | 列表排序 |
| 二重サブミット | 重复提交 | Double Submission | |
| 二重サブミット防止 | 重复提交防止 | Double Submit Prevention | Web防重复提交 |
| トークン | 令牌 | Token | 防重复提交用 |
| 携帯端末 | 手机端 | Mobile | |
| 並行アクセス | 并发访问 | Concurrent Access | |
| スレッド間の処理不整合 | 线程间处理不一致 | Thread Processing Inconsistency | |
| 静的コンテンツ/リソース | 静态内容/资源 | Static Content/Resource | |
| ホットデプロイ | 热部署 | Hot Deploy | |
| リソースマッピング | 资源映射 | Resource Mapping | |
| ベースパッケージ | 基础包 | Base Package | |
| 相対パス | 相对路径 | Relative Path | |
| 絶対パス | 绝对路径 | Absolute Path | |
| ワイルドカード | 通配符 | Wildcard | 模式匹配 |
| 前方一致 | 前方匹配 | Prefix Match | 字符串匹配方式 |
| マッチ | 匹配 | Match | 模式匹配 |
| 書き換え | 重写 | Rewrite | |
| 改ざんチェック | 篡改检查 | Tampering Check | |
| カスタムレスポンスライター | 自定义响应写入器 | Custom Response Writer | |
| コンテンツセキュリティポリシー | Content Security Policy | Content Security Policy | |
| ノーマライズ | 规范化 | Normalization | |
| ノーマライザー | 规范化器 | Normalizer | |
| ホワイトスペース | 空白字符 | Whitespace | |
| 往路処理 | 往路处理 | Outbound Processing | 请求处理流程（去程） |
| 復路処理 | 返回处理 | Return Processing | 请求处理流程（返程） |
| 透過的 | 透明 | Transparent | 对应用透明 |

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
| 排他制御用テーブル | 并发控制用表 | Exclusive Control Table | 版本号管理表 |
| 悲観的ロック | 悲观锁 | Pessimistic Lock | |
| 楽観的ロック | 乐观锁 | Optimistic Lock | |
| カーソル | 游标 | Cursor | |
| データベース接続 | 数据库连接 | Database Connection | |
| コネクション | 连接 | Connection | |
| スキーマ | Schema | Schema | 数据库结构 |
| トランザクションマネージャ | Transaction Manager | Transaction Manager | 事务管理 |
| バージョン番号 | 版本号 | Version Number | 乐观锁用 |
| 複合主キー/複合キー | 复合主键/复合键 | Composite Primary Key | 多字段主键 |
| デッドロック | 死锁 | Deadlock | 数据库死锁 |
| 個別トランザクション | 单独事务 | Separate Transaction | 独立事务 |

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
| ヘルスチェック | 健康检查 | Health Check | |
| エンドポイント | 端点 | Endpoint | |
| サービス閉塞 | 服务闭塞 | Service Unavailable | 服务不可用状态 |
| サービス閉塞中 | 服务闭塞中 | Service Unavailable Status | 服务暂停状态 |
| サービス提供可否チェック | 服务可用性检查 | Service Availability Check | 功能开关检查 |

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
| メッセージ管理 | 消息管理 | Message Management | 错误消息等管理 |
| メッセージレベル | 消息级别 | Message Level | INFO/WARN/ERROR |
| 固定文言 | 固定文本 | Fixed Text | 画面固定文字 |
| 埋め込み文字 | 嵌入字符 | Embedded Character | 消息参数占位 |

## RESTful Web服务

| 日文 | 中文 | 英文 | 备注 |
|------|------|------|------|
| ウェブサービス | Web服务 | Web Service | |
| RESTfulウェブサービス | RESTful Web服务 | RESTful Web Service | |
| パスパラメータ | 路径参数 | Path Parameter | |
| クエリーパラメータ | 查询参数 | Query Parameter | |
| メディアタイプ | 媒体类型 | Media Type | |
| Produces | Produces | Produces | 保留英文 |
| Consumes | Consumes | Consumes | 保留英文 |
| HTTPヘッダ | HTTP头部 | HTTP Header | |
| HTTPメソッド | HTTP方法 | HTTP Method | |
| JSON形式 | JSON格式 | JSON Format | |
| XML形式 | XML格式 | XML Format | |
| CORS | CORS | CORS | 跨域资源共享 |
| プリフライトリクエスト | 预检请求 | Preflight Request | CORS预检 |
| リソースクラス | 资源类 | Resource Class | 或Resource类 |
| Origin | Origin | Origin | CORS相关 |
| Bean Validation | Bean Validation | Bean Validation | 保留英文 |

## 适配器

| 日文 | 中文 | 英文 | 备注 |
|------|------|------|------|
| アダプタ | 适配器 | Adaptor | 或 Adapter |
| Domaアダプタ | Doma适配器 | Doma Adaptor | |
| Lettuceアダプタ | Lettuce适配器 | Lettuce Adaptor | |
| ログアダプタ | 日志适配器 | Log Adaptor | |

## 文件操作

| 日文 | 中文 | 英文 | 备注 |
|------|------|------|------|
| ダウンロード | 下载 | Download | |
| アップロード | 上传 | Upload | |
| ファイル | 文件 | File | |
| ファイル名 | 文件名 | File Name | |
| ファイルパス | 文件路径 | File Path | |
| ファイル形式 | 文件格式 | File Format | |
| フォーマットファイル | 格式文件 | Format File | |
| データフォーマット | 数据格式 | Data Format | |
| CSV形式 | CSV格式 | CSV Format | |
| 一時ファイル | 临时文件 | Temp File | |
| 一時領域 | 临时区域 | Temporary Area | |
| アップロードファイル | 上传文件 | Upload File | 文件处理 |
| アップロードヘルパー | 上传助手 | Upload Helper | 辅助功能 |
| 固定長ファイル | 固定长度文件 | Fixed Length File | 文件格式 |
| マルチレイアウト | 多布局 | Multi-layout | 多种格式 |
| パディング | 填充 | Padding | 数据处理 |
| トリム | 修剪 | Trim | 数据处理 |
| 列区切り | 列分隔符 | Field Separator | CSV格式 |
| 行区切り | 行分隔符 | Line Separator | CSV格式 |
| フィールド囲み文字 | 字段包围字符 | Quote Character | CSV格式 |
| クォートモード | 引用模式 | Quote Mode | CSV格式 |
| ヘッダ行 | 标题行 | Header Row | CSV格式 |
| 区切り文字 | 分隔符 | Delimiter | 数据分隔用 |
| 論理行番号 | 逻辑行号 | Logical Line Number | 行号相关 |

## 数据格式定义

| 日文 | 中文 | 英文 | 备注 |
|------|------|------|------|
| フォーマット定義ファイル | 格式定义文件 | Format Definition File | 核心概念 |
| 汎用データフォーマット | 通用数据格式 | Universal Data Format | |
| レコード識別フィールド | 记录识别字段 | Record Identification Field | 数据识别 |
| パック数値 | 压缩数值 | Packed Decimal | 主机数据类型 |
| ゾーン10進数 | 区域十进制数 | Zoned Decimal | 主机数据类型 |
| ホスト | 主机 | Host/Mainframe | 大型机 |
| フィールドタイプ | 字段类型 | Field Type | 数据类型 |
| データタイプ | 数据类型 | Data Type | 数据类型 |
| 置き換え(寄せ字) | 字符替换(替代字) | Character Replacement | 文字处理 |
| コンテンツ名 | 内容名 | Content Name | XML元素内容 |
| 固定長 | 固定长度 | Fixed Length | 与CSV/TSV并列 |

## 代码管理

| 日文 | 中文 | 英文 | 备注 |
|------|------|------|------|
| コード管理 | 代码管理 | Code Management | 值与名称映射管理 |
| コードパターンテーブル | 代码模式表 | Code Pattern Table | 代码管理用表 |
| コード名称テーブル | 代码名称表 | Code Name Table | 代码管理用表 |
| パターン | 模式 | Pattern | 代码管理中用法 |
| オプション名称 | 选项名称 | Optional Name | 代码管理扩展 |

## 日期与时间

| 日文 | 中文 | 英文 | 备注 |
|------|------|------|------|
| 日付管理 | 日期管理 | Date Management | 系统日期和业务日期管理 |
| システム日時 | 系统日期时间 | System Date Time | OS日期时间 |
| 業務日付 | 业务日期 | Business Date | 业务处理日期 |
| 業務日付プロバイダ | 业务日期提供provider | Business Date Provider | 日期处理 |
| タイムゾーン | 时区 | Time Zone | 国际化相关 |
| フォーマッタ | 格式化器 | Formatter | 日期数值格式化 |
| フォーマットパターン | 格式模式 | Format Pattern | 格式化模板 |
| プレースホルダ | 占位符 | Placeholder | 模板变量 |
| ディレードオンライン処理 | 延迟在线处理 | Deferred Online Processing | 异步处理模式 |

## 邮件

| 日文 | 中文 | 英文 | 备注 |
|------|------|------|------|
| メール送信 | 邮件发送 | Mail Sending | 邮件功能 |
| 定型メール | 定型邮件 | Template Mail | 模板邮件 |
| 添付ファイル | 附件 | Attached File | 邮件附件 |
| 送信先 | 接收方 | Recipient | 邮件接收者 |

## 授权与权限

| 日文 | 中文 | 英文 | 备注 |
|------|------|------|------|
| 認可チェック | 权限检查/授权检查 | Permission Check/Authorization Check | |
| アクセス制御 | 访问控制 | Access Control | 安全相关 |
| 権限データ | 权限数据 | Permission Data | 权限相关 |
| 認可チェック単位 | 授权检查单位 | Permission Unit | 权限粒度 |
| グループ | 组 | Group | 组织单位 |
| システムアカウント | 系统账户 | System Account | 用户相关 |
| グループシステムアカウント | 组系统账户 | Group System Account | 关联表 |
| グループ権限 | 组权限 | Group Authority | 权限相关 |
| システムアカウント権限 | 系统账户权限 | System Account Authority | 权限相关 |
| リクエスト単位 | 请求单位 | Request Unit | 权限粒度 |
| ユーザIDロック状態 | 用户ID锁定状态 | User ID Lock Status | 安全状态 |
| 有効日(From/To) | 有效日期(From/To) | Effective Date (From/To) | 时间范围 |
| ロール | 角色 | Role | 核心概念 |
| ユーザ | 用户 | User | 核心概念 |
| 定数クラス | 常量类 | Constants Class | 编程实践 |
| 許可判定 | 授权判定 | Authorization Decision | 权限判定 |
| Forbidden | Forbidden | Forbidden | 403错误 |
| anyOf | anyOf | Any Of | OR条件 |

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
| 初期化対象リスト | 初始化对象列表 | Initialization List | 配置项 |
| 設定クラス | 设置类 | Setting Class | 配置相关 |
| デフォルトコンフィグレーション | 默认配置 | Default Configuration | 配置相关 |
| ファクトリ | 工厂 | Factory | 工厂类/模式 |
| 実装クラス | 实现类 | Implementation Class | 接口实现 |
| インタフェース | 接口 | Interface | Java接口 |
| 上書き/オーバーライド | 覆盖/重写 | Override | 方法重写 |
| サブクラス | 子类 | Subclass | 继承类 |
| FQCN/完全修飾名 | 完全限定类名 | Fully Qualified Class Name | 完整类名 |
| シグネチャ | 签名 | Signature | 方法标识 |
| EL式 | EL表达式 | EL Expression | JSP表达式 |
| サブパッケージ | 子包 | Sub-package | 包结构 |
| 実行順定義 | 执行顺序定义 | Execution Order Definition | 拦截器配置 |
| アノテーション | 注解 | Annotation | Java注解 |
| プロパティ | 属性 | Property | JavaBeans属性 |
| 属性値 | 属性值 | Attribute Value | 上下文属性值 |
| 論理名 | 逻辑名 | Logical Name | 配置的别名 |
| 拡張子 | 扩展名 | Extension | 文件后缀 |
| scheme | Scheme | Scheme | URI scheme(file/classpath) |
| デフォルト | 默认 | Default | 缺省设置 |
| 任意 | 任意 | Arbitrary | 用户自定义 |
| 除外 | 排除 | Exclude | 排除在外 |
| モジュール一覧 | 模块列表 | Module List | Maven依赖列表 |
| プロパティファイル | 属性文件 | Properties File | 消息定义文件 |
| 定数クラス | 常量类 | Constants Class | 编程实践 |

## 测试相关

| 日文 | 中文 | 英文 | 备注 |
|------|------|------|------|
| テスト | 测试 | Test | |
| 単体テスト | 单元测试 | Unit Test | |
| 結合テスト | 集成测试 | Integration Test | |
| モック | 模拟对象/Mock | Mock | 或 mock |
| スタブ | 桩对象/Stub | Stub | 或 stub |
| テスト容易性 | 可测试性 | Testability | |
| リクエスト単体テスト | 请求单元测试 | Request Unit Test | |

## 异常处理

| 日文 | 中文 | 英文 | 备注 |
|------|------|------|------|
| 例外 | 异常 | Exception | |
| エラー | 错误 | Error | |
| 検査例外 | 受检异常 | Checked Exception | |
| 実行時例外 | 运行时异常 | Runtime Exception | |
| 特定の例外 | 特定异常 | Specific Exception | 指定异常类型 |
| リトライ可能例外/リトライ対象例外 | 可重试异常 | Retryable Exception | 可重试的异常 |
| 致命的な例外 | 致命的异常 | Fatal Exception | 严重异常 |
| 補足した例外 | 捕获的异常 | Caught Exception | 已捕获异常 |
| エラーに応じた処理 | 根据错误的处理 | Error Handling | 错误处理 |
| 再送出 | 重新抛出/再送出 | Rethrow | 异常处理 |
| スタックオーバーフロー | 堆栈溢出 | Stack Overflow | 内存错误 |
| ヒープ不足 | 堆内存不足 | Out Of Memory (Heap) | 内存错误 |

## 进程与线程

| 日文 | 中文 | 英文 | 备注 |
|------|------|------|------|
| プロセス | 进程 | Process | |
| スレッド | 线程 | Thread | |
| スレッドセーフ | 线程安全 | Thread Safe | |
| スレッドセーフな実装 | 线程安全的实现 | Thread-safe Implementation | 并发安全 |
| スレッドアンセーフ | 线程不安全 | Thread-unsafe | 并发相关 |
| マルチスレッド | 多线程 | Multi-thread | |
| マルチプロセス | 多进程 | Multi-process | |
| スレッドローカル | 线程本地 | Thread Local | 线程本地存储区域 |
| 多重起動 | 重复启动 | Multiple Launch | |
| 多重起動防止 | 防止重复启动 | Duplicate Launch Prevention | |
| プロセス常駐化 | 进程常驻 | Process Resident | |
| プロセス多重起動防止ハンドラ | 防止进程重复启动handler | Duplicate Process Check Handler | handler标题 |
| 起動中フラグ | 启动中标志 | Process Active Flag | 进程状态标志 |
| 多重起動防止チェック | 防止重复启动的检查 | Duplicate Launch Check | 功能描述 |
| マルチスレッド実行制御ハンドラ | 多线程执行控制handler | Multi-thread Execution Handler | handler标题 |
| サブスレッド | 子线程 | Sub-thread | 相对父线程而言 |
| 親スレッド | 父线程 | Parent Thread | 相对子线程而言 |
| メインスレッド | 主线程 | Main Thread | 主线程 |
| 割り込み要求 | 中断请求 | Interrupt Request | 线程中断 |
| スレッド数 | 线程数 | Thread Count | 配置项 |
| プロセス停止制御ハンドラ | 进程停止控制handler | Process Stop Handler | handler标题 |
| プロセス停止フラグ | 进程停止标志 | Process Stop Flag | 停止控制标志 |
| プロセス停止可否 | 进程停止可否 | Process Stoppable Check | 是否可停止 |
| リクエストスレッド内ループ制御ハンドラ | 请求线程内循环控制handler | Request Thread Loop Handler | handler标题 |
| チェック間隔 | 检查间隔 | Check Interval | 配置项 |
| 終了コード/プロセス終了コード | 结束代码/退出代码 | Exit Code/Process Exit Code | 进程返回值 |
| ステータスコード | 状态码 | Status Code | 处理结果状态码 |
| 変換ルール | 转换规则 | Conversion Rule | 代码映射规则 |
| ステータスコード→プロセス終了コード変換ハンドラ | 状态码→进程结束代码转换handler | Status Code Convert Handler | handler标题 |
| 停止要求 | 停止请求 | Stop Request | 进程停止信号 |
| 処理の中断 | 处理的中断 | Process Interruption | 中断处理 |
| 復旧時間 | 恢复时间 | Recovery Time | 故障恢复 |
| 最大処理件数 | 最大处理件数 | Max Count | DataReadHandler配置项 |
| 実行結果を集約 | 汇总执行结果 | Aggregate Results | 结果汇总 |
| データリーダをクローズ | 关闭DataReader | Close DataReader | 资源释放 |
| リトライハンドラ | 重试handler | Retry Handler | handler标题 |
| リトライ上限 | 重试上限 | Retry Limit | 重试次数上限 |
| リトライ回数 | 重试次数 | Retry Count | 配置项 |
| リトライ間隔 | 重试间隔 | Retry Interval | 重试等待时间 |
| 実行時ID/実行ID | 执行ID | Execution ID | 线程上下文属性 |
| 匿名ID | 匿名ID | Anonymous ID | 未登录用户ID |
| プロセス正常停止 | 进程正常停止 | Normal Process Stop | 正常停止 |
| 強制停止 | 强制停止 | Force Stop | 强制终止 |

## 国际化

| 日文 | 中文 | 英文 | 备注 |
|------|------|------|------|
| 国際化対応 | 国际化支持 | Internationalization Support | i18n支持 |
| 言語 | 语言 | Language | 国际化相关 |
| 多言語化 | 多语言化 | Multilingualization | 国际化支持 |
| 文字コード | 字符编码 | Character Encoding | 编码相关 |
| 文字セット | 字符集 | Character Set/Charset | 编码相关 |

## JavaBeans/对象

| 日文 | 中文 | 英文 | 备注 |
|------|------|------|------|
| Java Beansオブジェクト | Java Beans对象 | Java Beans Object | 核心概念 |
| Mapオブジェクト | Map对象 | Map Object | 核心概念 |
| レコード | 记录 | Record | Java16标准特性 |

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
| 上記 | 上述/以上 | Above | 前文所述 |
| 以下 | 以下 | Below | 后文所述 |

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
| 2026-02-15 | 添加 Web/RESTful Web服务/HTTP消息处理/文件操作相关术语（弹出窗口/对话框/路径参数/查询参数/批量更新/批量注册/下载/上传等） | AI |
| 2026-02-15 | 添加 RESTful Web服务相关术语（转换器/预检请求/CORS/资源类/Bean Validation等） | AI |
| 2026-02-15 | 从 handlers 和 libraries 已翻译文件中提取新术语：线程上下文/事务管理/权限控制/进程线程/批处理/Web处理/数据绑定/代码管理/日期管理/邮件/授权等（约200个新术语） | AI |
| 2026-02-15 | 整理术语表，删减重复内容，合并相似术语（コンバート/型変換、データバインド、実行ID、複合キー、上書き/オーバーライド等） | AI |

---

**维护说明：**
- 本术语表由 AI 自动维护
- 翻译过程中发现的新术语会自动添加
- 用户可通过指令要求更新术语
