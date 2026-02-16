.. _http_access_log:

HTTP访问日志的输出
==================================================

.. contents:: 目录
  :depth: 3
  :local:

HTTP访问日志通过框架提供的handler输出。
应用程序中，通过配置handler来输出HTTP访问日志。

HTTP访问日志输出所需的handler如下。

 :ref:`http_access_log_handler`
  在请求处理开始和结束时进行日志输出。

 :ref:`nablarch_tag_handler`
  在hidden参数解密后进行日志输出。
  关于hidden参数，请参考 :ref:`hidden加密<tag-hidden_encryption>` 。

 :ref:`http_request_java_package_mapping`
  在确定分发目标类后进行日志输出。

通过输出包含请求参数的请求信息，
如果能够满足个别应用程序的审计日志要求，也可以考虑将HTTP访问日志与审计日志兼用。

HTTP访问日志的输出策略
--------------------------------------------------
HTTP访问日志输出到进行应用程序整体日志输出的应用程序日志中。

.. list-table:: HTTP访问日志的输出策略
   :header-rows: 1
   :class: white-space-normal
   :widths: 15,15

   * - 日志级别
     - 日志记录器名称

   * - INFO
     - HTTP_ACCESS

上述输出策略的日志输出配置示例如下。

log.properties的配置示例
 .. code-block:: properties

  writerNames=appLog

  # 应用程序日志的输出目标
  writer.appLog.className=nablarch.core.log.basic.FileLogWriter
  writer.appLog.filePath=/var/log/app/app.log
  writer.appLog.encoding=UTF-8
  writer.appLog.maxFileSize=10000
  writer.appLog.formatter.className=nablarch.core.log.basic.BasicLogFormatter
  writer.appLog.formatter.format=$date$ -$logLevel$- $runtimeLoggerName$ [$executionId$] boot_proc = [$bootProcess$] proc_sys = [$processingSystem$] req_id = [$requestId$] usr_id = [$userId$] $message$$information$$stackTrace$

  availableLoggersNamesOrder=ACC,ROO

  # 应用程序日志的配置
  loggers.ROO.nameRegex=.*
  loggers.ROO.level=INFO
  loggers.ROO.writerNames=appLog

  # HTTP访问日志的配置
  loggers.ACC.nameRegex=HTTP_ACCESS
  loggers.ACC.level=INFO
  loggers.ACC.writerNames=appLog

app-log.properties的配置示例
 .. code-block:: properties

  # HttpAccessLogFormatter
  #httpAccessLogFormatter.className=
  #httpAccessLogFormatter.datePattern=
  #httpAccessLogFormatter.maskingChar=
  #httpAccessLogFormatter.maskingPatterns=
  #httpAccessLogFormatter.parametersSeparator=
  #httpAccessLogFormatter.sessionScopeSeparator=
  #httpAccessLogFormatter.beginOutputEnabled=
  #httpAccessLogFormatter.parametersOutputEnabled=
  #httpAccessLogFormatter.dispatchingClassOutputEnabled=
  #httpAccessLogFormatter.endOutputEnabled=
  httpAccessLogFormatter.beginFormat=@@@@ BEGIN @@@@ rid = [$requestId$] uid = [$userId$] sid = [$sessionId$]\
                                        \n\turl          = [$url$$query$]\
                                        \n\tmethod      = [$method$]\
                                        \n\tport        = [$port$]\
                                        \n\tclient_ip   = [$clientIpAddress$]\
                                        \n\tclient_host = [$clientHost$]
  httpAccessLogFormatter.parametersFormat=@@@@ PARAMETERS @@@@\n\tparameters  = [$parameters$]
  httpAccessLogFormatter.dispatchingClassFormat=@@@@ DISPATCHING CLASS @@@@ class = [$dispatchingClass$]
  httpAccessLogFormatter.endFormat=@@@@ END @@@@ rid = [$requestId$] uid = [$userId$] sid = [$sessionId$] url = [$url$$query$] method = [$method$] status_code = [$statusCode$] content_path = [$contentPath$]\
                                      \n\tstart_time     = [$startTime$]\
                                      \n\tend_time       = [$endTime$]\
                                      \n\texecution_time = [$executionTime$]\
                                      \n\tmax_memory     = [$maxMemory$]\
                                      \n\tfree_memory    = [$freeMemory$]

使用方法
--------------------------------------------------

.. _http_access_log-setting:

HTTP访问日志的配置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
HTTP访问日志的配置在 :ref:`log-app_log_setting` 中说明的属性文件中进行。

记述规则
 \

 httpAccessLogFormatter.className
  实现 :java:extdoc:`HttpAccessLogFormatter <nablarch.fw.web.handler.HttpAccessLogFormatter>` 的类。
  在需要替换时指定。

 .. _http_access_log-prop_begin_format:

 httpAccessLogFormatter.beginFormat
  请求处理开始时日志输出使用的格式。

  格式中可指定的占位符
   :请求ID: $requestId$
   :用户ID: $userId$
   :URL: $url$
   :查询字符串: $query$
   :端口号: $port$
   :HTTP方法: $method$
   :HTTP会话ID: $sessionId$
   :会话存储ID: $sessionStoreId$
   :请求参数: $parameters$
   :会话作用域信息: $sessionScope$
   :客户端终端IP地址: $clientIpAddress$
   :客户端终端主机: $clientHost$
   :HTTP头的User-Agent: $clientUserAgent$

  默认格式
   .. code-block:: bash

    @@@@ BEGIN @@@@ rid = [$requestId$] uid = [$userId$] sid = [$sessionId$]
        \n\turl         = [$url$]
        \n\tmethod      = [$method$]
        \n\tport        = [$port$]
        \n\tclient_ip   = [$clientIpAddress$]
        \n\tclient_host = [$clientHost$]

  .. tip::
   请求参数是 :ref:`hidden加密<tag-hidden_encryption>` 解密前的状态。

  .. important::
   请求ID和用户ID虽然与 :java:extdoc:`BasicLogFormatter <nablarch.core.log.basic.BasicLogFormatter>`
   输出的项目重复，但这是为了提高HTTP访问日志格式的灵活性而设置的。

   输出请求ID、用户ID时，
   由于这些的获取来源是 :java:extdoc:`ThreadContext <nablarch.core.ThreadContext>` ，
   因此handler构成中需要包含 :ref:`thread_context_handler` 。
   特别是用户ID，请参考 :ref:`thread_context_handler-user_id_attribute_setting` ，
   在应用程序中设置会话值。

 httpAccessLogFormatter.parametersFormat
  hidden参数解密后日志输出使用的格式。

  格式中可指定的占位符
   与"请求处理开始时日志输出使用的格式"相同，故省略。

  默认格式
   .. code-block:: bash

    @@@@ PARAMETERS @@@@
        \n\tparameters  = [$parameters$]

 httpAccessLogFormatter.dispatchingClassFormat
  确定分发目标类后日志输出使用的格式。

  格式中可指定的占位符
   :分发目标类: $dispatchingClass$
   :会话存储ID: $sessionStoreId$

  默认格式
   .. code-block:: bash

    @@@@ DISPATCHING CLASS @@@@ class = [$dispatchingClass$]

 .. _http_access_log-prop_end_format:

 httpAccessLogFormatter.endFormat
  请求处理结束时日志输出使用的格式。

  格式中可指定的占位符
   :分发目标类: $dispatchingClass$
   :状态码(内部): $statusCode$
   :状态码(客户端): $responseStatusCode$
   :内容路径: $contentPath$
   :开始日期时间: $startTime$
   :结束日期时间: $endTime$
   :执行时间: $executionTime$
   :最大内存量: $maxMemory$
   :空闲内存量(开始时): $freeMemory$
   :会话存储ID: $sessionStoreId$

  默认格式
   .. code-block:: bash

    @@@@ END @@@@ rid = [$requestId$] uid = [$userId$] sid = [$sessionId$] url = [$url$] status_code = [$statusCode$] content_path = [$contentPath$]
        \n\tstart_time     = [$startTime$]
        \n\tend_time       = [$endTime$]
        \n\texecution_time = [$executionTime$]
        \n\tmax_memory     = [$maxMemory$]
        \n\tfree_memory    = [$freeMemory$]

  .. tip::

    状态码(内部)是指 :ref:`http_access_log_handler` 在返回时点的状态码。
    状态码(客户端)是指 :ref:`http_response_handler` 中返回给客户端的状态码。

    状态码(客户端)在本日志输出时点尚未确定，但使用与 :ref:`http_response_handler` 相同的功能，
    推导出状态码(客户端)并进行日志输出。

    状态码的转换规则请参考 :ref:`http_response_handler-convert_status_code` 。

  .. important::
   ``状态码(客户端)`` 的值，如果在HTTP访问日志handler处理之后发生JSP错误等系统错误，
   可能与实际的内部代码不同。此时，由于会另行输出系统错误作为故障监控日志，
   因此在发生故障监控日志时要考虑到该值可能不正确来验证日志。

 httpAccessLogFormatter.datePattern
  开始日期时间和结束日期时间使用的日期时间模式。
  模式指定 :java:extdoc:`SimpleDateFormat <java.text.SimpleDateFormat>` 规定的语法。
  默认为 ``yyyy-MM-dd HH:mm:ss.SSS`` 。

 httpAccessLogFormatter.maskingPatterns
  用正则表达式指定要掩码的参数名或变量名。
  指定多个时用逗号分隔。
  用于请求参数和会话作用域信息两者的掩码。
  指定的正则表达式不区分大小写。
  例如，指定 ``password`` 时，会匹配 ``password`` ``newPassword`` ``password2`` 等。

 httpAccessLogFormatter.maskingChar
  掩码使用的字符。默认为 ``*`` 。

 httpAccessLogFormatter.parametersSeparator
  请求参数的分隔符。
  默认为 ``\n\t\t`` 。

 httpAccessLogFormatter.sessionScopeSeparator
  会话作用域信息的分隔符。
  默认为 ``\n\t\t`` 。

 httpAccessLogFormatter.beginOutputEnabled
  请求处理开始时的输出是否有效。
  默认为true。
  指定false则请求处理开始时不输出。

 httpAccessLogFormatter.parametersOutputEnabled
  hidden参数解密后的输出是否有效。
  默认为true。
  指定false则hidden参数解密后不输出。

 httpAccessLogFormatter.dispatchingClassOutputEnabled
  确定分发目标类后的输出是否有效。
  默认为true。
  指定false则确定分发目标类后不输出。

 httpAccessLogFormatter.endOutputEnabled
  请求处理结束时的输出是否有效。
  默认为true。
  指定false则请求处理结束时不输出。

记述示例
 .. code-block:: properties

  httpAccessLogFormatter.className=nablarch.fw.web.handler.HttpAccessLogFormatter
  httpAccessLogFormatter.beginFormat=> sid = [$sessionId$] @@@@ BEGIN @@@@\n\turl = [$url$]\n\tmethod = [$method$]
  httpAccessLogFormatter.parametersFormat=> sid = [$sessionId$] @@@@ PARAMETERS @@@@\n\tparameters  = [$parameters$]
  httpAccessLogFormatter.dispatchingClassFormat=> sid = [$sessionId$] @@@@ DISPATCHING CLASS @@@@ class = [$dispatchingClass$]
  httpAccessLogFormatter.endFormat=< sid = [$sessionId$] @@@@ END @@@@ url = [$url$] status_code = [$statusCode$] content_path = [$contentPath$]
  httpAccessLogFormatter.datePattern="yyyy-MM-dd HH:mm:ss.SSS"
  httpAccessLogFormatter.maskingChar=#
  httpAccessLogFormatter.maskingPatterns=password,mobilePhoneNumber
  httpAccessLogFormatter.parametersSeparator=,
  httpAccessLogFormatter.sessionScopeSeparator=,
  httpAccessLogFormatter.beginOutputEnabled=true
  httpAccessLogFormatter.parametersOutputEnabled=true
  httpAccessLogFormatter.dispatchingClassOutputEnabled=true
  httpAccessLogFormatter.endOutputEnabled=true

.. _http_access_log-json_setting:

作为JSON格式的结构化日志输出
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
通过 :ref:`log-json_log_setting` 配置可以将日志以JSON格式输出，
但在 :java:extdoc:`HttpAccessLogFormatter <nablarch.fw.web.handler.HttpAccessLogFormatter>` 中
HTTP访问日志的各项目是作为字符串输出到message的值中的。
要将HTTP访问日志的各项目也作为JSON的值输出，
需要使用 :java:extdoc:`HttpAccessJsonLogFormatter <nablarch.fw.web.handler.HttpAccessJsonLogFormatter>` 。
配置在 :ref:`log-app_log_setting` 中说明的属性文件中进行。

记述规则
 :java:extdoc:`HttpAccessJsonLogFormatter <nablarch.fw.web.handler.HttpAccessJsonLogFormatter>` 使用时
 指定的属性如下。
 
 httpAccessLogFormatter.className ``必需``
  以JSON格式输出日志时，
  指定 :java:extdoc:`HttpAccessJsonLogFormatter <nablarch.fw.web.handler.HttpAccessJsonLogFormatter>` 。

 .. _http_access_log-prop_begin_targets:

 httpAccessLogFormatter.beginTargets
  请求处理开始时的日志输出项目。用逗号分隔指定。

  可指定的输出项目以及默认输出项目
   :标签: label ``默认``
   :请求ID: requestId ``默认``
   :用户ID: userId ``默认``
   :HTTP会话ID: sessionId ``默认``
   :会话存储ID: sessionStoreId
   :URL: url ``默认``
   :端口号: port ``默认``
   :HTTP方法: method ``默认``
   :查询字符串: queryString
   :请求参数: parameters
   :会话作用域信息: sessionScope
   :客户端终端IP地址: clientIpAddress ``默认``
   :客户端终端主机: clientHost ``默认``
   :HTTP头的User-Agent: clientUserAgent

  输出项目的详情，
  与 :ref:`请求处理开始时日志输出使用的格式 <http_access_log-prop_begin_format>` 
  的占位符相同，故省略。

 httpAccessLogFormatter.parametersTargets
  hidden参数解密后的日志输出项目。用逗号分隔指定。
  可指定的输出项目，
  与 :ref:`请求处理开始时的输出项目 <http_access_log-prop_begin_targets>` 相同，故省略。
  默认输出项目为 ``label,parameters`` 。
        
 httpAccessLogFormatter.dispatchingClassTargets
  确定分发目标类后的日志输出项目。用逗号分隔指定。

  可指定的输出项目以及默认输出项目
   :标签: label ``默认``
   :HTTP会话ID: sessionId
   :会话存储ID: sessionStoreId
   :分发目标类: dispatchingClass ``默认``

 httpAccessLogFormatter.endTargets
  请求处理结束时的日志输出项目。用逗号分隔指定。

  可指定的输出项目以及默认输出项目
   :标签: label ``默认``
   :请求ID: requestId ``默认``
   :用户ID: userId ``默认``
   :HTTP会话ID: sessionId ``默认``
   :会话存储ID: sessionStoreId
   :URL: url ``默认``
   :分发目标类: dispatchingClass
   :状态码(内部): statusCode ``默认``
   :状态码(客户端): responseStatusCode
   :内容路径: contentPath ``默认``
   :开始日期时间: startTime ``默认``
   :结束日期时间: endTime ``默认``
   :执行时间: executionTime ``默认``
   :最大内存量: maxMemory ``默认``
   :空闲内存量(开始时): freeMemory ``默认``

  输出项目的详情，
  与 :ref:`请求处理结束时日志输出使用的格式 <http_access_log-prop_end_format>` 
  的占位符相同，故省略。

 httpAccessLogFormatter.datePattern
  开始日期时间和结束日期时间使用的日期时间模式。
  模式指定 :java:extdoc:`SimpleDateFormat <java.text.SimpleDateFormat>` 规定的语法。
  默认为 ``yyyy-MM-dd HH:mm:ss.SSS`` 。

 httpAccessLogFormatter.maskingPatterns
  用正则表达式指定要掩码的参数名或变量名（部分匹配）。
  指定多个时用逗号分隔。
  用于请求参数和会话作用域信息两者的掩码。
  指定的正则表达式不区分大小写。
  例如，指定 ``password`` 时，会匹配 ``password`` ``newPassword`` ``password2`` 等。

 httpAccessLogFormatter.maskingChar
  掩码使用的字符。默认为 ``*`` 。

 httpAccessLogFormatter.beginOutputEnabled
  请求处理开始时的输出是否有效。
  默认为true。
  指定false则请求处理开始时不输出。

 httpAccessLogFormatter.parametersOutputEnabled
  hidden参数解密后的输出是否有效。
  默认为true。
  指定false则hidden参数解密后不输出。

 httpAccessLogFormatter.dispatchingClassOutputEnabled
  确定分发目标类后的输出是否有效。
  默认为true。
  指定false则确定分发目标类后不输出。

 httpAccessLogFormatter.endOutputEnabled
  请求处理结束时的输出是否有效。
  默认为true。
  指定false则请求处理结束时不输出。

 httpAccessLogFormatter.beginLabel
  请求处理开始时日志的label输出的值。
  默认为 ``"HTTP ACCESS BEGIN"``。

 httpAccessLogFormatter.parametersLabel
  hidden参数解密后日志的label输出的值。
  默认为 ``"PARAMETERS"``。

 httpAccessLogFormatter.dispatchingClassLabel
  确定分发目标类后日志的label输出的值。
  默认为 ``"DISPATCHING CLASS"``。

 httpAccessLogFormatter.endLabel
  请求处理结束时日志的label输出的值。
  默认为 ``"HTTP ACCESS END"``。

 httpAccessLogFormatter.structuredMessagePrefix
  为了使格式化后的消息字符串能够被识别为已格式化为JSON格式，而在消息开头附加的标记字符串。
  如果消息开头的标记字符串与 :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` 中设置的标记字符串一致， :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` 会将消息作为JSON数据处理。
  默认为 ``"$JSON$"`` 。
  更改时，请使用LogWriter的 ``structuredMessagePrefix`` 属性为 :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` 也设置相同的值（关于LogWriter的属性请参考 :ref:`log-basic_setting` ）。

记述示例
 .. code-block:: properties

  httpAccessLogFormatter.className=nablarch.fw.web.handler.HttpAccessJsonLogFormatter
  httpAccessLogFormatter.structuredMessagePrefix=$JSON$
  httpAccessLogFormatter.beginTargets=sessionId,url,method
  httpAccessLogFormatter.parametersTargets=sessionId,parameters
  httpAccessLogFormatter.dispatchingClassTargets=sessionId,dispatchingClass
  httpAccessLogFormatter.endTargets=sessionId,url,statusCode,contentPath
  httpAccessLogFormatter.beginLabel=HTTP ACCESS BEGIN
  httpAccessLogFormatter.parametersLabel=PARAMETERS
  httpAccessLogFormatter.dispatchingClassLabel=DISPATCHING CLASS
  httpAccessLogFormatter.endLabel=HTTP ACCESS END

.. _http_access_log-session_store_id:

关于会话存储ID
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在输出中包含会话存储ID时，会输出 :ref:`session_store` 发行的用于识别会话的ID。

该值使用 :ref:`session_store_handler` 在往路中记录的值。
因此要在日志中输出会话存储ID时， :ref:`http_access_log_handler` 必须配置在 :ref:`session_store_handler` 之后。

由于会话存储ID在请求处理开始时的状态即被固定，因此具有以下规格。

* 对于未发行会话存储ID的请求，即使在途中发行了ID，同一请求内输出的会话存储ID也全部为空
* 即使在途中 :java:extdoc:`销毁会话 <nablarch.common.web.session.SessionUtil.invalidate(nablarch.fw.ExecutionContext)>` 或 :java:extdoc:`更改ID <nablarch.common.web.session.SessionUtil.changeId(nablarch.fw.ExecutionContext)>` ，日志中输出的值也不会从请求处理开始时的值发生变化
