.. _log:

日志输出
==================================================

.. contents:: 目录
  :depth: 3
  :local:

提供日志输出功能。

功能概要
--------------------------------------------------

可以替换日志输出功能的实现
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
日志输出由三个处理组成，每个实现都可以替换。

  .. image:: images/log/log-structure.png

根据应用程序的需求，
可以按 :java:extdoc:`LogWriter <nablarch.core.log.basic.LogWriter>` 或
:java:extdoc:`LogFormatter <nablarch.core.log.basic.LogFormatter>`
的单位进行替换，
如果这些无法满足需求，
还可以实现 :java:extdoc:`Logger <nablarch.core.log.Logger>` /
:java:extdoc:`LoggerFactory <nablarch.core.log.LoggerFactory>`
来替换几乎所有的处理。

例如，如果想要使用开源的日志输出库，
可以替换 :java:extdoc:`Logger <nablarch.core.log.Logger>` /
:java:extdoc:`LoggerFactory <nablarch.core.log.LoggerFactory>`。

此外，对于使用实绩较多的开源日志框架，已经提供了专用的Logger/LoggerFactory。

详情请参考 :ref:`log_adaptor`。

本功能与使用实绩较多的log4j的功能比较，请参考 :ref:`log-functional_comparison`。

下面列出日志输出功能默认提供的类。

Logger/LoggerFactory
 * :java:extdoc:`BasicLogger <nablarch.core.log.basic.BasicLogger>`
 * :java:extdoc:`BasicLoggerFactory <nablarch.core.log.basic.BasicLoggerFactory>`

.. _log-log_writers:

LogWriter
 * :java:extdoc:`FileLogWriter (输出到文件。日志轮转。) <nablarch.core.log.basic.FileLogWriter>`
 * :java:extdoc:`SynchronousFileLogWriter (从多个进程输出到单个文件) <nablarch.core.log.basic.SynchronousFileLogWriter>`
 * :java:extdoc:`StandardOutputLogWriter (输出到标准输出) <nablarch.core.log.basic.StandardOutputLogWriter>`
 * :java:extdoc:`LogPublisher (输出到任意监听器) <nablarch.core.log.basic.LogPublisher>`

.. _log-log_formatters:

LogFormatter
 * :java:extdoc:`BasicLogFormatter (通过模式字符串进行格式化) <nablarch.core.log.basic.BasicLogFormatter>`

.. _log-log_policies:

RotatePolicy
 * :java:extdoc:`DateRotatePolicy (按日期时间进行日志轮转) <nablarch.core.log.basic.DateRotatePolicy>`
 * :java:extdoc:`FileSizeRotatePolicy (按文件大小进行日志轮转) <nablarch.core.log.basic.FileSizeRotatePolicy>`
  
.. important::
 :java:extdoc:`SynchronousFileLogWriter <nablarch.core.log.basic.SynchronousFileLogWriter>`
 使用时，请参考 :ref:`log-synchronous_file_log_writer_attention`。

.. tip::
 关于日志输出功能使用的日志级别，请参考 :ref:`log-log_level`。

预先提供了各种日志的输出功能
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
本框架预先提供了应用程序普遍需要的各种日志的输出功能。
根据应用程序的需求，可以通过配置更改日志的格式来使用。
此外，正如 :ref:`log-app_log_setting` 中所述，各种日志的输出功能仅进行格式处理，
日志的输出处理本身使用的是本功能。
从Nablarch提供的原型生成的空白项目中，已经设置了各种日志的格式。
各配置值请参考 :download:`默认设置一览 <../configuration/default_settings.xlsx>`。

.. toctree::
  :hidden:
  :glob:

  log/failure_log
  log/sql_log
  log/performance_log
  log/http_access_log
  log/jaxrs_access_log
  log/messaging_log

.. list-table:: 日志类型
   :header-rows: 1
   :class: white-space-normal
   :widths: 20,80

   * - 日志类型
     - 说明

   * - :ref:`故障通知日志 <failure_log>`
     - 输出故障发生时识别一级排查负责人所需的信息。

   * - :ref:`故障分析日志 <failure_log>`
     - 输出确定故障原因所需的信息。

   * - :ref:`SQL日志 <sql_log>`
     - 对于容易导致严重性能劣化的SQL语句执行，
       为进行性能调优而输出SQL语句的执行时间和SQL语句。

   * - :ref:`性能日志 <performance_log>`
     - 对于任意处理，为进行性能调优而输出执行时间和内存使用量。

   * - :ref:`HTTP访问日志 <http_access_log>`
     - 在Web应用程序中，输出用于把握应用程序执行状况的信息。
       包括应用程序性能测量所需的信息、应用程序负载测量所需的信息的输出。
       此外，为检测应用程序的不当使用，
       也作为输出所有请求及响应信息的审计日志使用。

   * - :ref:`HTTP访问日志（RESTful Web服务用） <jaxrs_access_log>`
     - 在RESTful Web服务应用程序中，输出用于把握应用程序执行状况的信息。
       包括应用程序性能测量所需的信息、应用程序负载测量所需的信息的输出。
       此外，为检测应用程序的不当使用，
       也作为输出所有请求及响应信息的审计日志使用。

   * - :ref:`消息处理日志 <messaging_log>`
     - 在消息处理中，输出用于把握消息收发状况的信息。

.. tip::
 在本框架中，将 :ref:`故障通知日志 <failure_log>` 和 :ref:`故障分析日志 <failure_log>` 合称为故障日志。

模块一览
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core</artifactId>
  </dependency>
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-applog</artifactId>
  </dependency>

  <!-- 仅在使用SQL日志时需要 -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-jdbc</artifactId>
  </dependency>

  <!-- 仅在使用HTTP访问日志时需要 -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web</artifactId>
  </dependency>

  <!-- 仅在使用HTTP访问日志（RESTful Web服务用）时需要 -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-jaxrs</artifactId>
  </dependency>

  <!-- 仅在使用消息处理日志时需要 -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-messaging</artifactId>
  </dependency>

使用方法
--------------------------------------------------

输出日志
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
日志输出使用 :java:extdoc:`Logger <nablarch.core.log.Logger>`。
:java:extdoc:`Logger <nablarch.core.log.Logger>` 从
:java:extdoc:`LoggerManager <nablarch.core.log.LoggerManager>` 获取。

.. code-block:: java

 // 指定类获取Logger。
 // Logger保存在类变量中。
 private static final Logger LOGGER = LoggerManager.get(UserManager.class);

.. code-block:: java

 // 预先检查日志输出是否启用，然后输出日志。
 if (LOGGER.isDebugEnabled()) {
     String message = "userId[" + user.getId() + "],name[" + user.getName() + "]";
     LOGGER.logDebug(message);
 }

在获取 :java:extdoc:`Logger <nablarch.core.log.Logger>` 时指定日志器名称。
日志器名称可以指定字符串或类。
如果指定了类，则指定类的FQCN成为日志器名称。

.. important::
 在应用程序中，对于始终要输出的日志级别，
 由于会降低源代码可读性，不需要预先检查。
 例如，如果生产环境运行时将日志级别设为INFO级别，
 则从FATAL级别到INFO级别不需要预先检查。

.. tip::
 对于日志器名称，如果是SQL日志或监控日志等特定用途的日志输出，
 请指定表示该用途的名称（SQL或MONITOR等），其他情况请指定类的FQCN。

.. _log-basic_setting:

日志输出设置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
日志输出设置在属性文件中进行。

属性文件位置
 使用类路径下的 **log.properties**。
 如果要更改位置，请在系统属性中以 **nablarch.log.filePath** 为键指定文件路径。
 文件路径的指定方法请参考
 :java:extdoc:`FileUtil#getResource <nablarch.core.util.FileUtil.getResource(java.lang.String)>`。

 .. code-block:: bash

  >java -Dnablarch.log.filePath=classpath:nablarch/example/log.properties ...

属性文件记述规则
 属性文件记述规则如下。

 LoggerFactory
  \

  记述规则
   \

   loggerFactory.className
    指定实现LoggerFactory的类的FQCN。
    使用本功能时，请指定 :java:extdoc:`BasicLoggerFactory <nablarch.core.log.basic.BasicLoggerFactory>`。

  记述例
   .. code-block:: properties

    # 通过LoggerFactory决定日志输出使用的实现（本功能或Log4J等）。
    loggerFactory.className=nablarch.core.log.basic.BasicLoggerFactory

 LogWriter
  \

  记述规则
   \

   writerNames
    指定要使用的所有LogWriter的名称。多个时用逗号分隔。

   writer.<名称>.className
    指定实现LogWriter的类的FQCN。

   writer.<名称>.<属性名>
    指定要设置的LogWriter各属性的值。
    可指定的属性请参考使用的LogWriter的Javadoc。

  记述例
   .. code-block:: properties

    # 定义两个名称。
    writerNames=appLog,stdout

    # 设置appLog。
    writer.appLog.className=nablarch.core.log.basic.FileLogWriter
    writer.appLog.filePath=/var/log/app/app.log

    # 设置stdout。
    writer.stdout.className=nablarch.core.log.basic.StandardOutputLogWriter

 日志器设置
  \

  记述规则
   \

   availableLoggersNamesOrder
    指定要使用的所有日志器设置的名称。多个时用逗号分隔。

    .. important::
     请注意availableLoggersNamesOrder属性，记述顺序是有意义的。

     在获取 :java:extdoc:`Logger <nablarch.core.log.Logger>` 时，对于执行日志输出的类指定的日志器名称，
     按照此处记述的顺序进行 :java:extdoc:`Logger <nablarch.core.log.Logger>` 的匹配，
     返回第一个匹配的 :java:extdoc:`Logger <nablarch.core.log.Logger>`。

     例如，如果下面记述例中的availableLoggersNamesOrder记述顺序改为availableLoggersNamesOrder=root,sql，
     则所有日志器获取都会匹配到日志器设置 ``root``。
     结果，即使以日志器名称 ``SQL`` 输出日志，也不会输出到 ``sqlLog``，而是输出到日志器设置 ``root`` 指定的 ``appLog``。

     因此，availableLoggersNamesOrder属性应从指定了更限定性正则表达式的日志器设置开始依次记述。

    .. important::
     availableLoggersNamesOrder和loggers.*中指定的日志器设置名称必须保持一致。
     :java:extdoc:`BasicLoggerFactory <nablarch.core.log.basic.BasicLoggerFactory>` 在初始化处理时会检查是否一致，
     不一致时将抛出异常。
     例如，如果上述设置中的availableLoggersNamesOrder中删除了 ``access``，则会抛出异常。

     此检查是为了防止设置遗漏。
     如果上述设置中的availableLoggersNamesOrder中删除了 ``access``，则必须同时删除loggers.access.*的设置。

   loggers.<名称>.nameRegex
    指定用于与日志器名称匹配的正则表达式。
    正则表达式用于筛选日志器设置的目标日志器。
    匹配时针对获取日志器时指定的日志器名称（即 :java:extdoc:`LoggerManager#get <nablarch.core.log.LoggerManager.get(java.lang.String)>`
    的参数中指定的日志器名称）进行。

   loggers.<名称>.level
    指定 :java:extdoc:`LogLevel <nablarch.core.log.basic.LogLevel>` 的名称。
    输出此处指定级别以上的所有日志。

   loggers.<名称>.writerNames
    指定作为输出目标的LogWriter的名称。
    多个时用逗号分隔。
    向此处指定的所有LogWriter写入日志。

  记述例
   .. code-block:: properties

    # 定义两个日志器设置的名称。
    availableLoggersNamesOrder=sql,root

    # 设置root。
    loggers.root.nameRegex=.*
    loggers.root.level=WARN
    loggers.root.writerNames=appLog

    # 设置sql。
    loggers.sql.nameRegex=SQL
    loggers.sql.level=DEBUG
    loggers.sql.writerNames=sqlLog

属性文件记述例
 属性文件整体的记述例如下。

 .. code-block:: properties

  loggerFactory.className=nablarch.core.log.basic.BasicLoggerFactory

  writerNames=appLog,sqlLog,monitorLog,stdout

  # 应用程序用日志文件设置例
  writer.appLog.className=nablarch.core.log.basic.FileLogWriter
  writer.appLog.filePath=/var/log/app/app.log

  # SQL输出用日志文件设置例
  writer.sqlLog.className=nablarch.core.log.basic.FileLogWriter
  writer.sqlLog.filePath=/var/log/app/sql.log

  # 监控用日志文件设置例
  writer.monitorLog.className=nablarch.core.log.basic.FileLogWriter
  writer.monitorLog.filePath=/var/log/app/monitoring.log

  # 标准输出设置例
  writer.stdout.className=nablarch.core.log.basic.StandardOutputLogWriter

  availableLoggersNamesOrder=sql,monitoring,access,validation,root

  # 将所有日志器名称作为日志输出目标的设置例
  # 针对所有日志器获取，将WARN级别以上输出到appLog。
  loggers.root.nameRegex=.*
  loggers.root.level=WARN
  loggers.root.writerNames=appLog

  # 将特定日志器名称作为日志输出目标的设置例。
  # 针对指定"MONITOR"作为日志器名称的日志器获取，
  # 将ERROR级别以上输出到appLog,monitorLog。
  loggers.monitoring.nameRegex=MONITOR
  loggers.monitoring.level=ERROR
  loggers.monitoring.writerNames=appLog,monitorLog

  # 将特定日志器名称作为日志输出目标的设置例。
  # 针对指定"SQL"作为日志器名称的日志器获取，
  # 将DEBUG级别以上输出到sqlLog。
  loggers.sql.nameRegex=SQL
  loggers.sql.level=DEBUG
  loggers.sql.writerNames=sqlLog

  # 将特定类作为日志输出目标的设置例。
  # 针对指定"app.user.UserManager"作为日志器名称的日志器获取，
  # 将INFO级别以上输出到appLog和stdout。
  loggers.access.nameRegex=app\\.user\\.UserManager
  loggers.access.level=INFO
  loggers.access.writerNames=appLog,stdout

  # 将特定包以下作为日志输出目标的设置例。
  # 针对指定以"nablarch.core.validation"开头的名称作为日志器名称的日志器获取，
  # 将DEBUG级别以上输出到stdout。
  loggers.validation.nameRegex=nablarch\\.core\\.validation\\..*
  loggers.validation.level=DEBUG
  loggers.validation.writerNames=stdout

 .. tip::
  建议在日志器设置中准备一个匹配所有日志输出的日志器设置，并指定在availableLoggersNamesOrder的最后。
  这样即使万一有设置遗漏，也能防止重要日志的输出被遗漏。
  设置例请参考上述记述例中的日志器设置 ``root``。

覆盖日志输出设置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
日志输出设置可以使用系统属性，
以与属性文件相同的键名指定值来覆盖。
这样可以在准备好共用的属性文件后，按进程更改日志输出设置。

以下展示将日志器设置 ``root`` 的日志级别改为INFO时的示例。

.. code-block:: bash

 >java -Dloggers.root.level=INFO ...

.. _log-log_format:

指定日志格式
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
本功能作为可通用使用的 :java:extdoc:`LogFormatter <nablarch.core.log.basic.LogFormatter>`，
提供了 :java:extdoc:`BasicLogFormatter <nablarch.core.log.basic.BasicLogFormatter>`。

:java:extdoc:`BasicLogFormatter <nablarch.core.log.basic.BasicLogFormatter>` 中，
使用占位符指定格式。
可用的占位符请参考
:java:extdoc:`BasicLogFormatter <nablarch.core.log.basic.BasicLogFormatter>`
的Javadoc。

格式设置例如下。
格式在LogWriter的属性中指定。

.. code-block:: properties

 # 指定格式时显式指定BasicLogFormatter。
 writer.appLog.formatter.className=nablarch.core.log.basic.BasicLogFormatter

 # 使用占位符指定格式。
 writer.appLog.formatter.format=$date$ -$logLevel$- $loggerName$ $message$

 # 指定日期时间格式使用的模式。
 # 如果不指定则为"yyyy-MM-dd HH:mm:ss.SSS"。
 writer.appLog.formatter.datePattern=yyyy/MM/dd HH:mm:ss[SSS]

 # 指定日志级别的文字。
 # 如果不指定则为LogLevel枚举类型的名称（FATAL、INFO等）。
 writer.appLog.formatter.label.fatal=F
 writer.appLog.formatter.label.error=E
 writer.appLog.formatter.label.warn=W
 writer.appLog.formatter.label.info=I
 writer.appLog.formatter.label.debug=D
 writer.appLog.formatter.label.trace=T

:java:extdoc:`BasicLogFormatter <nablarch.core.log.basic.BasicLogFormatter>`
中，为识别输出日志的状况，可以输出以下项目。
对这些输出项目进行说明。

* :ref:`启动进程 <log-boot_process>`
* :ref:`处理方式 <log-processing_system>`
* :ref:`执行时ID <log-execution_id>`

.. _log-boot_process:

启动进程
 启动进程是指用于识别启动应用程序的执行环境的名称。
 在启动进程中组合使用服务器名和JOBID等识别字符串作为名称，
 可以识别来自同一服务器多个进程的日志的执行环境。
 启动进程设想按项目以ID体系等规定体系。

 启动进程在系统属性中以 ``nablarch.bootProcess`` 键指定。
 如果没有系统属性指定，启动进程为空。

.. _log-processing_system:

处理方式
 处理方式是指Web、批处理等。
 在需要识别应用程序的处理方式时，按项目规定并使用。

 处理方式在 :ref:`log-basic_setting` 中说明的属性文件中
 以 ``nablarch.processingSystem`` 键指定。
 如果没有属性指定则为空。

.. _log-execution_id:

执行时ID
 执行时ID是指为识别请求ID对应的应用程序各个执行而附加的ID。
 由于对于1个请求ID会发出与执行次数相同的执行时ID，
 请求ID与执行时ID的关系为一对多。

 执行时ID用于在输出多个日志时，将输出的多个日志关联起来。

 执行时ID在各处理方式的 :java:extdoc:`ThreadContext <nablarch.core.ThreadContext>`
 初始化时发出，并设置到 :java:extdoc:`ThreadContext <nablarch.core.ThreadContext>` 中。

 执行时ID的ID体系
  .. code-block:: none

    # 启动进程仅在指定时附加。
    启动进程＋系统日期时间(yyyyMMddHHmmssSSS)＋序列号(4位)

.. important::
 输出请求ID、执行时ID、用户ID时，
 由于这些获取来源是 :java:extdoc:`ThreadContext <nablarch.core.ThreadContext>`，
 因此处理程序构成中需要包含 :ref:`thread_context_handler`。
 特别是关于用户ID，请参考 :ref:`thread_context_handler-user_id_attribute_setting`，
 在应用程序中向会话设置值。

想要在格式中包含换行符和制表符时
 想要在格式中包含换行符和制表符时，请如下所示使用与Java相同的记述。

 .. code-block:: none

  换行符 \n
  制表符   \t

 换行符从Java标准系统属性中包含的 ``line.separator`` 获取。
 因此，如果不更改系统属性的 ``line.separator``，则使用OS的换行符。

 .. tip::
  :java:extdoc:`BasicLogFormatter <nablarch.core.log.basic.BasicLogFormatter>` 中
  无法输出 ``\n`` 和 ``\t`` 这两个字符串。

.. _log-app_log_setting:

各种日志的设置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
各种日志的输出功能仅进行与各种日志用途相符的格式处理，
日志的输出处理本身使用的是本功能。
也就是说，各种日志的输出功能创建的是指定给 :java:extdoc:`Logger <nablarch.core.log.Logger>`
的消息。

因此，使用各种日志的输出功能时，除了 :ref:`log-basic_setting` 之外，还需要各种日志的设置。
各种日志的设置在属性文件中进行。

属性文件位置
 使用类路径下的 **app-log.properties**。
 如果要更改位置，请在系统属性中以 **nablarch.appLog.filePath** 为键指定文件路径。
 文件路径的指定方法请参考
 :java:extdoc:`FileUtil#getResource <nablarch.core.util.FileUtil.getResource(java.lang.String)>`。

 .. code-block:: bash

  >java -Dnablarch.appLog.filePath=file:/var/log/app/app-log.properties ...

属性文件记述规则
 因各种日志而异，请参考以下内容。

 * :ref:`failure_log-setting`
 * :ref:`sql_log-setting`
 * :ref:`performance_log-setting`
 * :ref:`http_access_log-setting`
 * :ref:`jaxrs_access_log-setting`
 * :ref:`messaging_log-setting`

.. _log-rotation:

进行日志文件轮转
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
本功能提供的FileLogWriter按照设置的策略进行日志文件轮转。

轮转策略默认使用按文件大小进行轮转的 :java:extdoc:`FileSizeRotatePolicy <nablarch.core.log.basic.FileSizeRotatePolicy>`。
通过创建 :java:extdoc:`RotatePolicy <nablarch.core.log.basic.RotatePolicy>` 的实现类，可以更改轮转策略。

本功能提供的 :java:extdoc:`RotatePolicy <nablarch.core.log.basic.RotatePolicy>` 实现类如下。
各 :java:extdoc:`RotatePolicy <nablarch.core.log.basic.RotatePolicy>` 的设置请参考各自的Javadoc。

* :java:extdoc:`FileSizeRotatePolicy <nablarch.core.log.basic.FileSizeRotatePolicy>`
* :java:extdoc:`DateRotatePolicy <nablarch.core.log.basic.DateRotatePolicy>`

轮转策略设置例如下。轮转策略在LogWriter的属性中指定。

  .. code-block:: properties

    writerNames=sample
    
    # 在writer的rotatePolicy中指定实现了RotatePolicy的类的FQCN
    writer.sample.rotatePolicy=nablarch.core.log.basic.DateRotatePolicy
    # 更新时间。可选。
    writer.sample.rotateTime=12:00
扩展示例
---------------------------------------------------------------------

.. _log-add_log_writer:

添加LogWriter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
要添加新的LogWriter，需要创建实现 :java:extdoc:`LogWriter <nablarch.core.log.basic.LogWriter>`
接口的类。
此外，如果要创建使用 :java:extdoc:`LogFormatter <nablarch.core.log.basic.LogFormatter>` 的LogWriter，
请继承提供通用处理的 :java:extdoc:`LogWriterSupport <nablarch.core.log.basic.LogWriterSupport>` 来创建。

添加LogFormatter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
要添加新的LogFormatter，需要创建实现 :java:extdoc:`LogFormatter <nablarch.core.log.basic.LogFormatter>`
接口的类。
此外，如果想要通过设置更改表示日志级别的文字，
请使用 :java:extdoc:`LogLevelLabelProvider <nablarch.core.log.basic.LogLevelLabelProvider>`。

随着添加新的LogFormatter，可能会想要增加日志输出时指定的参数，
并让LogFormatter接收增加的参数。
本功能中，为增加日志输出时指定的参数，
在 :java:extdoc:`Logger <nablarch.core.log.Logger>` 接口的日志输出方法中
设置了Object型可变长参数options。

.. code-block:: java

 // Logger#logInfo方法的签名
 public void logInfo(String message, Object... options)
 public void logInfo(String message, Throwable cause, Object... options)

想要增加日志输出时的参数时，请规定并使用options参数。

添加日志输出项目（占位符）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:java:extdoc:`BasicLogFormatter <nablarch.core.log.basic.BasicLogFormatter>` 使用
:java:extdoc:`LogItem <nablarch.core.log.LogItem>` 接口，
获取各占位符对应的输出项目。
因此，如果想要新增占位符，请按以下方式处理。

* 创建实现 :java:extdoc:`LogItem <nablarch.core.log.LogItem>` 的类
* 创建继承 :java:extdoc:`BasicLogFormatter <nablarch.core.log.basic.BasicLogFormatter>` 的类，添加占位符

以下展示从LogFormatter的设置获取启动进程的更改示例。
LogFormatter的设置假设如下。

.. code-block:: properties

 # 指定自定义的LogFormatter。
 writer.appLog.formatter.className=nablarch.core.log.basic.CustomLogFormatter

 # 指定格式。
 writer.appLog.formatter.format=$date$ -$logLevel$- $loggerName$ [$bootProcess$] $message$

 # 在LogFormatter的设置中指定启动进程。
 # 此处指定的启动进程输出到$bootProcess$。
 writer.appLog.formatter.bootProcess=CUSTOM_PROCESS

创建实现 :java:extdoc:`LogItem <nablarch.core.log.LogItem>` 的类
 .. code-block:: java

  // 获取自定义启动进程的类。
  public class CustomBootProcessItem implements LogItem<LogContext> {

      private String bootProcess;

      public CustomBootProcessItem(ObjectSettings settings) {
          // 从LogFormatter的设置获取启动进程。
          bootProcess = settings.getProp("bootProcess");
      }

      @Override
      public String get(LogContext context) {
          // 返回从设置获取的启动进程。
          return bootProcess;
      }
  }

创建继承 :java:extdoc:`BasicLogFormatter <nablarch.core.log.basic.BasicLogFormatter>` 的类，添加占位符
 .. code-block:: java

  public class CustomLogFormatter extends BasicLogFormatter {

      // 覆盖获取格式对象日志输出项目的方法。
      @Override
      protected Map<String, LogItem<LogContext>> getLogItems(ObjectSettings settings) {

          // 以覆盖方式设置启动进程的占位符。
          Map<String, LogItem<LogContext>> logItems = super.getLogItems(settings);
          logItems.put("$bootProcess$", new CustomBootProcessItem(settings));
          return logItems;
      }
  }

不输出日志初始化消息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
本功能中，在各日志器初始化时会向日志输出初始化消息。
在监控对象日志等不需要初始化消息的情况下，需要基于本功能提供的Writer，
创建不输出初始化消息的Writer来对应。

此外，在Web应用程序服务器等中与OSS产品统一日志器等目的使用 :ref:`log_adaptor` 时，
不会输出初始化消息，因此不需要此对应。

对应示例如下。

1. 将基础Writer类的源代码导入（复制）到项目侧。
   例如，如果是输出到文件的日志，请复制 :java:extdoc:`FileLogWriter <nablarch.core.log.basic.FileLogWriter>`。
   
2. 删除输出初始化日志的部分。

   :java:extdoc:`FileLogWriter <nablarch.core.log.basic.FileLogWriter>` 的情况下，
   请像以下修改示例一样删除输出初始化消息的部分。
   
   .. code-block:: java
  
    private void initializeWriter() {
      try {
        out = new BufferedOutputStream(new FileOutputStream(filePath, true), outputBufferSize);
        currentFileSize = new File(filePath).length();
        
        // 删除此处进行的初始化消息输出处理
        
      } catch (IOException e) {
        throw new IllegalArgumentException(String.format("failed to create %s. file name = [%s], encoding = [%s], buffer size =[%s]",
            Writer.class.getName(), filePath, charset.displayName(), outputBufferSize), e);
      }
    }
    
3. 更改为在日志功能初始化后不输出初始化消息。

  覆盖 :java:extdoc:`needsToWrite <nablarch.core.log.basic.LogWriterSupport.needsToWrite(nablarch.core.log.basic.LogContext)>`，
  更改为不输出首次调用的初始化消息。
  
  .. code-block:: java

      /** 定义用于进行首次判定的标志 */
      private boolean suppressionWriting = true;
      
      @Override
      public boolean needsToWrite(final LogContext context) {
        final String message = context.getMessage();
        if (suppressionWriting) {
          // 如果输出目标的日志以"initialized."开头，
          // 则为初始化消息，返回表示非输出目标的"false"。
          if (StringUtil.hasValue(message) && message.startsWith("initialized.")) {
            suppressionWriting = false;
            return false;
          }
        }
        return super.needsToWrite(context);
      }
      
4. 在log.properties中设置创建的类。

  将项目侧创建的Writer的类名设置在log.properties中。
  
  设置示例如下。

  .. code-block:: properties

    writerNames=sample
    
    # 在writer的类名中指定创建的类
    # 类的完全限定名为"sample.CustomFileLogWriter"时的设置示例
    writer.sample.className = sample.CustomFileLogWriter


.. _log-json_log_setting:

以JSON形式的结构化日志输出
--------------------------------------------------------------------------

通过将LogWriter和各种日志使用的格式化器替换为JSON输出用类，可以将日志输出变为JSON形式。

具体来说，通过进行以下修改，可以将日志变为JSON形式。

* :ref:`log-json_set_jsonlogformatter_for_logwriter`
* :ref:`log-json_app_logs`
* :ref:`log-json_for_batch`


.. _log-json_set_jsonlogformatter_for_logwriter:

将LogWriter使用的格式化器更改为JsonLogFormatter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

通过将LogWriter使用的格式化器更改为 :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>`，
可以将日志输出变为JSON形式。

使用方法
 :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` 的设置例如下。
 
 .. code-block:: properties
 
  # 以JSON形式输出日志时指定JsonLogFormatter。
  writer.appLog.formatter.className=nablarch.core.log.basic.JsonLogFormatter
 
  # 指定输出项目。
  writer.appLog.formatter.targets=date,logLevel,message,stackTrace
 
  # 指定日期时间格式使用的模式。
  # 如果不指定则为"yyyy-MM-dd HH:mm:ss.SSS"。
  writer.appLog.formatter.datePattern=yyyy-MM-dd'T'HH:mm:ss.SSS'Z'
 
 :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` 中，
在 ``targets`` 属性中以逗号分隔指定输出项目。
可用的输出项目如下。
此外，默认情况下输出所有项目。
 
 .. list-table:: targets属性可指定的输出项目
   :header-rows: 1
   :class: white-space-normal
   :widths: 20,80
 
   * - 输出项目
     - 说明
 
   * - date
     - 请求此日志输出时的日期时间。
 
   * - logLevel
     - 此日志输出的日志级别。
 
   * - loggerName
     - 此日志输出对应的日志器设置的名称。
 
   * - runtimeLoggerName
     - 执行时，从 :java:extdoc:`LoggerManager <nablarch.core.log.LoggerManager>` 获取日志器时指定的名称。
 
   * - bootProcess
     - 识别启动进程的名称。
 
   * - processingSystem
     - 识别处理方式的名称。
 
   * - requestId
     - 请求此日志输出时的请求ID。
 
   * - executionId
     - 请求此日志输出时的执行时ID。
 
   * - userId
     - 请求此日志输出时的登录用户的用户ID。
 
   * - message
     - 此日志输出的消息。
 
   * - stackTrace
     - 错误信息中指定的异常对象的堆栈跟踪。
 
   * - payload
     - 选项信息中指定的对象。
 
 .. tip::
  ``datePattern`` 和 ``label``（日志级别文字指定）与 :java:extdoc:`BasicLogFormatter <nablarch.core.log.basic.BasicLogFormatter>` 功能相同。
  
 记述例
  .. code-block:: java
  
   // 指定类获取Logger。
   // Logger保存在类变量中。
   private static final Logger LOGGER = LoggerManager.get(UserManager.class);
  
  .. code-block:: java
  
   LOGGER.logInfo("hello");
 
  (输出结果)

  .. code-block:: none

   {"date":"2021-02-04 12:34:56.789","logLevel":"INFO","message":"hello"}

独立添加项目
 如果输出目标包含 ``payload``，则选项信息中指定的Map<String, Object>对象将作为JSON对象输出。
 对象转换规则如下。

 .. list-table:: 可输出的对象
   :header-rows: 1
   :class: white-space-normal
   :widths: 40,60
 
   * - 可输出的Java类
     - JSON输出
 
   * - :java:extdoc:`String <java.lang.String>`
     - 作为JSON字符串输出。

   * - :java:extdoc:`Number <java.lang.Number>` 及其子类 |br|
       （ :java:extdoc:`Integer <java.lang.Integer>` , 
       :java:extdoc:`Long <java.lang.Long>` , 
       :java:extdoc:`Short <java.lang.Short>` , 
       :java:extdoc:`Byte <java.lang.Byte>` , 
       :java:extdoc:`Float <java.lang.Float>` , 
       :java:extdoc:`Double <java.lang.Double>` , 
       :java:extdoc:`BigDecimal <java.math.BigDecimal>` , 
       :java:extdoc:`BigInteger <java.math.BigInteger>` , 
       :java:extdoc:`AtomicInteger <java.util.concurrent.atomic.AtomicInteger>` , 
       :java:extdoc:`AtomicLong <java.util.concurrent.atomic.AtomicLong>` ）
     - 将 ``toString()`` 方法的返回值作为JSON数值输出。
       NaN及无穷大作为JSON字符串输出。

   * - :java:extdoc:`Boolean <java.lang.Boolean>`
     - 作为JSON布尔值（ ``true`` / ``false`` ）输出。
   
   * - :java:extdoc:`Date <java.util.Date>` |br|
       :java:extdoc:`Calendar <java.util.Calendar>`  及其子类 |br|
       :java:extdoc:`LocalDateTime <java.time.LocalDateTime>`
     - 作为JSON字符串输出。默认格式为 ``"yyyy-MM-dd HH:mm:ss.SSS"`` 。
       更改格式时，在 ``datePattern`` 属性中指定。
   
   * - :java:extdoc:`Map <java.util.Map>`  的实现类
     - 作为JSON对象输出。
       如果键不是 :java:extdoc:`String <java.lang.String>` 或值为 ``null``，
       则键及其本身都不会输出。
       要输出值为 ``null`` 的情况，请在属性 ``ignoreNullValueMember`` 中设置 ``false`` 。

   * - :java:extdoc:`List <java.util.List>` 的实现类，以及数组
     - 作为JSON数组输出。
  
   * - ``null``
     - 作为JSON的 ``null`` 输出。
       :java:extdoc:`Map <java.util.Map>` 的值为 ``null`` 时，默认情况下不作为输出目标。

   * - 其他对象
     - 将 ``toString()`` 方法的返回值作为JSON字符串输出。
 
 记述例
  .. code-block:: java
 
   Map<String, Object> structuredArgs = new HashTable<String, Object>();
   structuredArgs.put("key1", "value1");
   structuredArgs.put("key2", 123);
   structuredArgs.put("key3", true);
   structuredArgs.put("key4", null);
   structuredArgs.put("key5", new Date());
   LOGGER.logInfo("addition fields", structuredArgs);
 
  (输出结果)
 
  .. code-block:: none
  
   {"date":"2021-02-04 12:34:56.789","logLevel":"INFO","message":"addition fields","key1":"value1","key2":123,"key3":true,"key5":"2021-02-04 12:34:56.789"}
 
 .. tip::
  使用 :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` 时，
  请不要在选项信息中设置 :java:extdoc:`Map <java.util.Map>` < :java:extdoc:`String <java.lang.String>`
  , :java:extdoc:`Object <java.lang.Object>` >以外的选项信息。
  虽然可以指定多个 :java:extdoc:`Map <java.util.Map>` 对象，
  但如果键重复，其中一个值将被忽略而不输出。

.. _log-json_app_logs:

将各种日志使用的格式化器替换为JSON日志用
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 各种日志以各自的方法格式化消息部分。
 将各格式使用的格式化器替换为JSON用格式化器，各种日志输出的内容也可以作为JSON日志输出。

 各格式化器的具体设置方法，请参考下表各自的链接。

 .. list-table:: 各种日志的JSON版格式化器
  :header-rows: 1
  :class: white-space-normal
  :widths: 30,50
  
  * - 日志类型
    - 对应的格式化器
 
  * - :ref:`故障日志 <failure_log-json_setting>`
    - :java:extdoc:`FailureJsonLogFormatter <nablarch.core.log.app.FailureJsonLogFormatter>`
 
  * - :ref:`SQL日志 <sql_log-json_setting>`
    - :java:extdoc:`SqlJsonLogFormatter <nablarch.core.db.statement.SqlJsonLogFormatter>`
 
  * - :ref:`性能日志 <performance_log-json_setting>`
    - :java:extdoc:`PerformanceJsonLogFormatter <nablarch.core.log.app.PerformanceJsonLogFormatter>`
  
  * - :ref:`HTTP访问日志 <http_access_log-json_setting>`
    - :java:extdoc:`HttpAccessJsonLogFormatter <nablarch.fw.web.handler.HttpAccessJsonLogFormatter>`

  * - :ref:`HTTP访问日志（RESTful Web服务用） <jaxrs_access_log-json_setting>`
    - :java:extdoc:`JaxRsAccessJsonLogFormatter <nablarch.fw.jaxrs.JaxRsAccessJsonLogFormatter>`

  * - :ref:`消息处理日志 <messaging_log-json_setting>`
    - :java:extdoc:`MessagingJsonLogFormatter <nablarch.fw.messaging.logging.MessagingJsonLogFormatter>`

.. _log-json_for_batch:

将Nablarch批处理的日志变为JSON形式
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

要将Nablarch批处理输出的日志变为JSON形式，除了上述格式化器设置外，还需要进行以下修改。

* :ref:`log-json_set_applicationsettingsjsonlogformatter`
* :ref:`log-json_set_launcherjsonlogformatter`
* :ref:`log-json_set_jsoncommitlogger`

以下说明各设置方法。

.. _log-json_set_applicationsettingsjsonlogformatter:

将ApplicationSettingLogFormatter切换为JSON用
******************************************************

:java:extdoc:`ApplicationSettingLogFormatter <nablarch.core.log.app.ApplicationSettingLogFormatter>` 用于将系统设置值输出到日志。
要将其以JSON形式输出，请将格式化器切换为 :java:extdoc:`ApplicationSettingJsonLogFormatter <nablarch.core.log.app.ApplicationSettingJsonLogFormatter>`。
设置在 :ref:`log-app_log_setting` 中说明的属性文件中进行。

记述规则
 :java:extdoc:`ApplicationSettingJsonLogFormatter <nablarch.core.log.app.ApplicationSettingJsonLogFormatter>` 使用时
 可指定的属性如下。
 
 applicationSettingLogFormatter.className ``必需``
  以JSON形式输出日志时，
  指定 :java:extdoc:`ApplicationSettingJsonLogFormatter <nablarch.core.log.app.ApplicationSettingJsonLogFormatter>` 。

 applicationSettingLogFormatter.appSettingTargets
  应用程序设置日志中输出的项目（不含业务日期）。以逗号分隔指定。

  可指定的输出项目及默认输出项目
   :系统设置值: systemSettings ``默认``
   :业务日期: businessDate
 
 applicationSettingLogFormatter.appSettingWithDateTargets
  应用程序设置日志中输出的项目（含业务日期）。以逗号分隔指定。

  可指定的输出项目
   :系统设置: systemSettings
   :业务日期: businessDate

  默认所有输出项目都是目标。

 applicationSettingLogFormatter.systemSettingItems
  要输出的系统设置值的名称列表。以逗号分隔指定。
  默认为空，不输出任何内容。

 applicationSettingLogFormatter.structuredMessagePrefix
  为能够识别格式化后的消息字符串已格式化为JSON形式，在消息开头附加的标记字符串。
  如果消息开头有此标记， :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` 将消息作为JSON数据处理。
  默认为 ``"$JSON$"`` 。

记述例
 .. code-block:: properties

  applicationSettingLogFormatter.className=nablarch.core.log.app.ApplicationSettingJsonLogFormatter
  applicationSettingLogFormatter.structuredMessagePrefix=$JSON$
  applicationSettingLogFormatter.appSettingTargets=systemSettings
  applicationSettingLogFormatter.appSettingWithDateTargets=systemSettings,businessDate
  applicationSettingLogFormatter.systemSettingItems=dbUser,dbUrl,threadCount

.. _log-json_set_launcherjsonlogformatter:

将LauncherLogFormatter切换为JSON用
******************************************************

:java:extdoc:`LauncherLogFormatter <nablarch.fw.launcher.logging.LauncherLogFormatter>` 用于输出批处理开始·结束日志。
要将其以JSON形式输出，请将格式化器切换为 :java:extdoc:`LauncherJsonLogFormatter <nablarch.fw.launcher.logging.LauncherJsonLogFormatter>`。
设置在 :ref:`log-app_log_setting` 中说明的属性文件中进行。

记述规则
 :java:extdoc:`LauncherJsonLogFormatter <nablarch.fw.launcher.logging.LauncherJsonLogFormatter>` 使用时
 可指定的属性如下。
 
 launcherLogFormatter.className ``必需``
  以JSON形式输出日志时，
  指定 :java:extdoc:`LauncherJsonLogFormatter <nablarch.fw.launcher.logging.LauncherJsonLogFormatter>` 。

 launcherLogFormatter.startTargets
  批处理开始日志中输出的项目。以逗号分隔指定。

  可指定的输出项目
   :开始或结束的标签: label
   :命令行选项: commandLineOptions
   :命令行参数: commandLineArguments

  默认所有输出项目都是目标。
 
 launcherLogFormatter.endTargets
  批处理结束日志中输出的项目。以逗号分隔指定。

  可指定的输出项目
   :开始或结束的标签: label
   :退出代码: exitCode
   :处理时间: executeTime

  默认所有输出项目都是目标。
 
 launcherLogFormatter.startLogMsgLabel
  开始日志的label中输出的值。默认为 ``"BATCH BEGIN"``。
 
 launcherLogFormatter.endLogMsgLabel
  结束日志的label中输出的值。默认为 ``"BATCH END"``。

 launcherLogFormatter.structuredMessagePrefix
  为能够识别格式化后的消息字符串已格式化为JSON形式，在消息开头附加的标记字符串。
  如果消息开头有此标记， :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` 将消息作为JSON数据处理。
  默认为 ``"$JSON$"`` 。

记述例
 .. code-block:: properties

  launcherLogFormatter.className=nablarch.fw.launcher.logging.LauncherJsonLogFormatter
  launcherLogFormatter.structuredMessagePrefix=$JSON$
  launcherLogFormatter.startTargets=label,commandLineOptions,commandLineArguments
  launcherLogFormatter.endTargets=label,exitCode,executionTime
  launcherLogFormatter.startLogMsgLabel=BATCH BEGIN
  launcherLogFormatter.endLogMsgLabel=BATCH END


.. _log-json_set_jsoncommitlogger:

将CommitLogger切换为JSON用
******************************************************

:java:extdoc:`CommitLogger <nablarch.core.log.app.CommitLogger>` 用于将提交件数输出到日志。
默认使用 :java:extdoc:`BasicCommitLogger <nablarch.core.log.app.BasicCommitLogger>` 类。

要将其以JSON形式输出，请将 :java:extdoc:`JsonCommitLogger <nablarch.core.log.app.JsonCommitLogger>` 定义为组件。
以下展示组件定义示例。

组件定义示例
 .. code-block:: xml
 
   <component name="commitLogger" class="nablarch.core.log.app.JsonCommitLogger">
     <property name="interval" value="${nablarch.commitLogger.interval}" />
   </component>

组件名称必须以 ``commitLogger`` 定义。

.. _log-synchronous_file_log_writer_attention:

使用SynchronousFileLogWriter时的注意事项
--------------------------------------------------------------------------

.. important::
 :java:extdoc:`SynchronousFileLogWriter <nablarch.core.log.basic.SynchronousFileLogWriter>`
 虽然是专为多进程写入创建的，但仅设想用于 :ref:`故障通知日志 <failure_log>` 等输出频率低的日志输出。
 在日志输出频繁的场面使用 :java:extdoc:`SynchronousFileLogWriter <nablarch.core.log.basic.SynchronousFileLogWriter>` 时，
 可能会发生由于锁获取等待导致的性能劣化或竞争导致的日志丢失，因此请勿将
 :java:extdoc:`SynchronousFileLogWriter <nablarch.core.log.basic.SynchronousFileLogWriter>` 用于应用程序日志或访问日志等输出频率高的日志输出。

 此外，:java:extdoc:`SynchronousFileLogWriter <nablarch.core.log.basic.SynchronousFileLogWriter>`
 有以下限制，使用时请充分考虑。

 * 无法进行日志轮转。
 * 输出的日志内容可能不正确。


:java:extdoc:`SynchronousFileLogWriter <nablarch.core.log.basic.SynchronousFileLogWriter>` 使用
锁文件进行排他控制的同时向文件写入日志。
然后，如果超过锁获取等待时间仍无法获取锁，则强制删除锁文件，
生成自身线程用的锁文件后再输出日志。

如果无法强制删除锁文件，则在未获取锁的状态下强制输出日志。
此外，锁文件生成失败时以及锁获取等待时发生中断的情况下，
也会在未获取锁的状态下强制输出日志。

**请注意，在未获取锁的状态下强制输出日志时，如果多进程日志输出竞争，日志可能无法正常输出。**

发生此类故障时，除了强制输出的日志外，还会向同一日志文件输出故障日志。
默认输出本框架准备的日志，但
通过在 :java:extdoc:`SynchronousFileLogWriter <nablarch.core.log.basic.SynchronousFileLogWriter>`
的属性中设置故障代码，可以以故障通知日志的格式（含故障代码）输出日志。
以故障通知日志的格式输出后，可以用与通常故障通知日志相同的方法监控日志，
因此建议设置故障代码。

故障代码设置的属性名称如下。

failureCodeCreateLockFile
 :故障内容: 无法生成锁文件
 :日志级别: FATAL
 :消息设置示例（{0}中设置锁文件路径）: 锁文件生成失败。可能是锁文件路径错误。锁文件路径=[{0}]。
 :默认输出的日志（不输出故障代码等）: failed to create lock file. perhaps lock file path was invalid. lock file path=[{0}].

failureCodeReleaseLockFile
 :故障内容: 无法释放（删除）生成的锁文件
 :日志级别: FATAL
 :消息设置示例（{0}中设置锁文件路径）: 锁文件删除失败。锁文件路径=[{0}]。
 :默认输出的日志（不输出故障代码等）: failed to delete lock file. lock file path=[{0}].

failureCodeForceDeleteLockFile
 :故障内容: 无法强制删除未释放的锁文件
 :日志级别: FATAL
 :消息设置示例（{0}中设置锁文件路径）: 锁文件强制删除失败。锁文件被非法打开。锁文件路径=[{0}]。
 :默认输出的日志（不输出故障代码等）: failed to delete lock file forcedly. lock file was opened illegally. lock file path=[{0}].

failureCodeInterruptLockWait
 :故障内容: 锁获取等待中线程休眠时发生中断
 :日志级别: FATAL
 :消息设置示例: 锁获取中发生中断。
 :默认输出的日志（不输出故障代码等）: interrupted while waiting for lock retry.

.. important::
 设置故障代码后，虽然会以故障通知日志的格式向同一日志文件输出日志，
 但请注意不会输出故障分析日志。

:java:extdoc:`SynchronousFileLogWriter <nablarch.core.log.basic.SynchronousFileLogWriter>`
设置例如下。

.. code-block:: properties

 writerNames=monitorLog

 # 指定SynchronousFileLogWriter类。
 writer.monitorLog.className=nablarch.core.log.basic.SynchronousFileLogWriter
 # 指定写入目标的文件路径。
 writer.monitorLog.filePath=/var/log/app/monitor.log
 # 指定写入时使用的字符编码。
 writer.monitorLog.encoding=UTF-8
 # 指定输出缓冲区的大小。（单位为千字节。按1000字节换算为1千字节。如果不指定则为8KB）
 writer.monitorLog.outputBufferSize=8
 # 指定日志格式化器的类名。
 writer.monitorLog.formatter.className=nablarch.core.log.basic.BasicLogFormatter
 # 指定LogLevel枚举类型的名称。输出此处指定级别以上的所有日志。
 writer.monitorLog.level=ERROR
 # 指定锁文件的文件名。
 writer.monitorLog.lockFilePath=/var/log/lock/monitor.lock
 # 指定锁获取的重试间隔（毫秒）。
 writer.monitorLog.lockRetryInterval=10
 # 指定锁获取的等待时间（毫秒）。
 writer.monitorLog.lockWaitTime=3000
 # 指定无法生成锁文件时的故障通知代码。
 writer.monitorLog.failureCodeCreateLockFile=MSG00101
 # 指定无法释放（删除）生成的锁文件时的故障通知代码。
 writer.monitorLog.failureCodeReleaseLockFile=MSG00102
 # 指定无法强制删除未释放的锁文件时的故障通知代码。
 writer.monitorLog.failureCodeForceDeleteLockFile=MSG00103
 # 指定锁等待中线程休眠时发生中断情况下的故障通知代码。
 writer.monitorLog.failureCodeInterruptLockWait=MSG00104

.. important::

 maxFileSize属性指定后会发生日志轮转，
 可能导致无法输出日志，因此请勿指定。

.. _log-publisher_usage:

LogPublisher的使用方法
--------------------------------------------------

:java:extdoc:`LogPublisher <nablarch.core.log.basic.LogPublisher>` 提供将输出的日志信息（:java:extdoc:`LogContext <nablarch.core.log.basic.LogContext>`）传递给已注册的 :java:extdoc:`LogListener <nablarch.core.log.basic.LogListener>` 的功能。
想要在程序上对输出的日志信息进行处理时，可以使用此功能。

使用 ``LogPublisher`` 时，首先将 ``LogPublisher`` 设置为 ``LogWriter``。

.. code-block:: properties

  # ...省略

  # 在 writerNames 中添加 LogPublisher 的 writer
  writerNames=monitorFile,appFile,stdout,logPublisher

  # 定义 logPublisher
  writer.logPublisher.className=nablarch.core.log.basic.LogPublisher
  writer.logPublisher.formatter.className=nablarch.core.log.basic.BasicLogFormatter
  # ...省略

  # 在想要处理日志信息的 logger 的 writerNames 中，添加 LogPublisher 的 writer
  # ROO
  loggers.ROO.nameRegex=.*
  loggers.ROO.level=INFO
  loggers.ROO.writerNames=appFile,stdout,logPublisher

  # MON
  loggers.MON.nameRegex=MONITOR
  loggers.MON.level=ERROR
  loggers.MON.writerNames=monitorFile,logPublisher

  # ...省略


接下来，创建要注册到 ``LogWriter`` 的 ``LogListener`` 的实现类。

.. code-block:: java

  package example.micrometer.log;

  import nablarch.core.log.basic.LogContext;
  import nablarch.core.log.basic.LogListener;

  public class CustomLogListener implements LogListener {

      @Override
      public void onWritten(LogContext context) {
          // 使用 LogContext 实现处理
      }
  }

最后，将创建的 ``LogListener`` 实例注册到 ``LogPublisher``。
``LogListener`` 的注册通过 ``LogPublisher`` 的 ``static`` 方法进行。

.. code-block:: java

  LogListener listener = new CustomLogListener();
  LogPublisher.addListener(listener);

通过以上设置，输出到 ``LogPublisher`` 的日志信息将传递给 ``CustomLogListener``。

已注册的 ``LogListener`` 可以通过 :java:extdoc:`removeListener(LogListener) <nablarch.core.log.basic.LogPublisher.removeListener(nablarch.core.log.basic.LogListener)>` 或 :java:extdoc:`removeAllListeners() <nablarch.core.log.basic.LogPublisher.removeAllListeners()>` 删除。

.. _log-log_level:

日志级别的定义
--------------------------------------------------
本功能使用以下日志级别。

.. list-table:: 日志级别的定义
   :header-rows: 1
   :class: white-space-normal
   :widths: 15,85

   * - 日志级别
     - 说明

   * - FATAL
     - 表示发生了使应用程序无法继续运行的严重问题。
       必须监控，需要立即报告和立即处理。

   * - ERROR
     - 表示发生了妨碍应用程序继续运行的问题。
       必须监控，但报告和处理的紧急性不如FATAL级别。

   * - WARN
     - 表示发生了暂时不会产生影响，但放置不管可能会妨碍应用程序继续运行的问题。
       最好监控，但紧急性不如ERROR级别。

   * - INFO
     - 生产环境运行时输出应用程序信息的日志级别。访问日志和统计日志属于此类。

   * - DEBUG
     - 开发时输出调试信息的日志级别。SQL日志和性能日志属于此类。

   * - TRACE
     - 开发时想要输出比调试信息更详细信息时使用的日志级别。

日志级别分为6个阶段，从FATAL到TRACE级别依次降低。
日志输出功能输出设置中指定级别以上的所有日志。
例如，如果设置中指定了WARN级别，则仅输出指定了FATAL级别、ERROR级别、WARN级别的日志。

.. tip::
 生产环境运行时设想以INFO级别输出日志。
 为防止日志文件大小膨胀，请按项目规定日志的输出内容。

.. tip::
 本框架也使用日志输出功能输出日志。
 关于框架输出的日志，请参考 :ref:`log-fw_log_policy`。

.. _log-fw_log_policy:

框架的日志输出方针
--------------------------------------------------
本框架基于以下输出方针进行日志输出。

.. list-table:: 框架的日志输出方针
    :header-rows: 1
    :class: white-space-normal
    :widths: 15,85

    * - 日志级别
      - 输出方针

    * - FATAL/ERROR
      - 输出故障日志时使用FATAL/ERROR级别。

        故障日志是故障监控的对象，也是故障发生时一级排查的起点，
        因此原则上一项故障对应输出一条故障日志。

        因此，执行控制基础设施采用通过单一处理程序（处理异常的处理程序）
        输出故障通知日志的方针。

    * - WARN
      - 故障发生时连锁发生异常等情况，
        无法作为故障日志输出的异常使用WARN级别输出。

        例如，如果业务处理和事务结束处理两处都发生异常，
        则将业务处理的异常输出到故障日志，将事务结束处理的异常以WARN级别输出。

    * - INFO
      - 检测到与应用程序执行状况相关的错误时使用INFO级别输出。

        例如，URL参数篡改错误或授权检查错误发生时，以INFO级别输出。

    * - DEBUG
      - 输出应用程序开发时使用的调试信息。

        应用程序开发时，通过设置DEBUG级别来确保输出开发所需信息。

    * - TRACE
      - 输出框架开发时使用的调试信息。不设想在应用程序开发中使用。

.. _log-functional_comparison:

与log4j的功能比较
--------------------------------------------------
此处展示本功能与 `log4j(外部站点、英语) <https://logging.apache.org/log4j/1.x/>`_ 的功能比较。

.. list-table:: 功能比较（○：提供  △：部分提供  ×：不提供  －：非对象）
  :header-rows: 1
  :class: white-space-normal
  :widths: 50, 25, 25

  * - 功能
    - Nablarch
    - log4j

  * - 可以按日志级别控制日志输出与否
    - ○
      |br|
      :ref:`前往解说书 <log-basic_setting>`
    - ○

  * - 可以按类别（包单位或名称等）控制日志输出与否
    - ○
      |br|
      :ref:`前往解说书 <log-basic_setting>`
    - ○

  * - 可以将1条日志输出到多个输出目标
    - ○
      |br|
      :ref:`前往解说书 <log-basic_setting>`
    - ○

  * - 可以将日志输出到标准输出
    - ○
      |br|
      :ref:`前往解说书 <log-log_writers>`
    - ○

  * - 可以将日志输出到文件
    - ○
      |br|
      :ref:`前往解说书 <log-log_writers>`
    - ○

  * - 可以按文件大小进行日志文件轮转
    - △ [#logrolate]_
      |br|
      :ref:`前往解说书 <log-rotation>`
    - ○

  * - 可以按日期时间进行日志文件轮转
    - △ [#logrolate]_
      |br|
      :ref:`前往解说书 <log-rotation>`
    - ○

  * - 可以通过邮件发送日志
    - × [#extends_or_log4j]_
    - ○

  * - 可以通过Telnet发送日志
    - × [#extends_or_log4j]_
    - ○

  * - 可以通过Syslog发送日志
    - × [#extends_or_log4j]_
    - ○

  * - 可以添加到Windows NT的事件日志
    - × [#extends_or_log4j]_
    - ○

  * - 可以输出日志到数据库
    - × [#extends_or_log4j]_
    - ○

  * - 可以异步输出日志
    - × [#extends_or_log4j]_
    - ○

  * - 可以通过模式字符串指定日志格式
    - ○
      |br|
      :ref:`前往解说书 <log-log_format>`
    - ○

  * - 可以输出故障日志
    - ○
      |br|
      :ref:`前往解说书 <failure_log>`
    - －

  * - 可以输出HTTP访问日志
    - ○
      |br|
      :ref:`前往解说书 <http_access_log>`
    - －

  * - 可以输出SQL日志
    - ○
      |br|
      :ref:`前往解说书 <sql_log>`
    - －

  * - 可以输出性能日志
    - ○
      |br|
      :ref:`前往解说书 <performance_log>`
    - －

  * - 可以输出消息处理日志
    - ○
      |br|
      :ref:`前往解说书 <messaging_log>`
    - －

.. [#logrolate] Nablarch的日志输出不提供文件的世代管理，因此为部分提供。

.. [#extends_or_log4j] 使用 :ref:`log_adaptor` 。
                       或者在项目中创建。创建方法请参考 :ref:`log-add_log_writer` 。

.. |br| raw:: html

  <br />
