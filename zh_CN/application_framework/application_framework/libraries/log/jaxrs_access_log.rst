.. _jaxrs_access_log:

HTTP访问日志（RESTful Web服务用）的输出
==================================================

.. contents:: 目录
  :depth: 3
  :local:

HTTP访问日志使用框架提供的处理器来输出。
应用程序通过配置处理器来输出HTTP访问日志。

HTTP访问日志输出所需的处理器如下。

 :ref:`jaxrs_access_log_handler`
  进行请求处理开始和结束时的日志输出。

通过输出包含请求参数的请求信息，
当满足个别应用程序的审计日志要求时，也可以考虑将HTTP访问日志和审计日志兼用。

HTTP访问日志（RESTful Web服务用）的输出策略
------------------------------------------------------
HTTP访问日志输出到应用程序整体日志输出的应用程序日志中。

.. list-table:: HTTP访问日志的输出策略
   :header-rows: 1
   :class: white-space-normal
   :widths: 15,15

   * - 日志级别
     - 日志记录器名称

   * - INFO
     - HTTP_ACCESS

上述输出策略的日志输出设置示例如下。

log.properties的设置示例
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

  # 应用程序日志的设置
  loggers.ROO.nameRegex=.*
  loggers.ROO.level=INFO
  loggers.ROO.writerNames=appLog

  # HTTP访问日志的设置
  loggers.ACC.nameRegex=HTTP_ACCESS
  loggers.ACC.level=INFO
  loggers.ACC.writerNames=appLog

app-log.properties的设置示例
 .. code-block:: properties

  # JaxRsAccessLogFormatter
  #jaxRsAccessLogFormatter.className=
  #jaxRsAccessLogFormatter.datePattern=
  #jaxRsAccessLogFormatter.maskingChar=
  #jaxRsAccessLogFormatter.maskingPatterns=
  #jaxRsAccessLogFormatter.bodyLogTargetMatcher=
  #jaxRsAccessLogFormatter.bodyMaskingFilter=
  #jaxRsAccessLogFormatter.bodyMaskingItemNames=
  #jaxRsAccessLogFormatter.parametersSeparator=
  #jaxRsAccessLogFormatter.sessionScopeSeparator=
  #jaxRsAccessLogFormatter.beginOutputEnabled=
  #jaxRsAccessLogFormatter.endOutputEnabled=
  jaxRsAccessLogFormatter.beginFormat=@@@@ BEGIN @@@@ rid = [$requestId$] uid = [$userId$] sid = [$sessionId$]\
                                        \n\turl         = [$url$$query$]\
                                        \n\tmethod      = [$method$]\
                                        \n\tport        = [$port$]\
                                        \n\tclient_ip   = [$clientIpAddress$]\
                                        \n\tclient_host = [$clientHost$]
  jaxRsAccessLogFormatter.endFormat=@@@@ END @@@@ rid = [$requestId$] uid = [$userId$] sid = [$sessionId$] url = [$url$$query$] method = [$method$] status_code = [$statusCode$]\
                                      \n\tstart_time     = [$startTime$]\
                                      \n\tend_time       = [$endTime$]\
                                      \n\texecution_time = [$executionTime$]\
                                      \n\tmax_memory     = [$maxMemory$]\
                                      \n\tfree_memory    = [$freeMemory$]

使用方法
--------------------------------------------------

.. _jaxrs_access_log-setting:

HTTP访问日志（RESTful Web服务用）的设置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
HTTP访问日志的设置是在 :ref:`log-app_log_setting` 中说明的属性文件中进行的。

记述规则
 \

 jaxRsAccessLogFormatter.className
  实现 :java:extdoc:`JaxRsAccessLogFormatter <nablarch.fw.jaxrs.JaxRsAccessLogFormatter>` 的类。
  在替换时指定。

 .. _jaxrs_access_log-prop_begin_format:

 jaxRsAccessLogFormatter.beginFormat
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
   :会话范围信息: $sessionScope$
   :客户端终端IP地址: $clientIpAddress$
   :客户端终端主机: $clientHost$
   :HTTP头的User-Agent: $clientUserAgent$
   :请求体: $requestBody$

  默认格式
   .. code-block:: bash

    @@@@ BEGIN @@@@ rid = [$requestId$] uid = [$userId$] sid = [$sessionId$]
        \n\turl         = [$url$]
        \n\tmethod      = [$method$]
        \n\tport        = [$port$]
        \n\tclient_ip   = [$clientIpAddress$]
        \n\tclient_host = [$clientHost$]

  .. tip::
    占位符 ``$parameters$`` 输出的请求参数不包含请求体。
    要输出请求体时，请使用 ``$requestBody$`` 。

  .. important::
   请求ID和用户ID与 :java:extdoc:`BasicLogFormatter <nablarch.core.log.basic.BasicLogFormatter>`
   输出的项目重复，但这是为了提高HTTP访问日志格式的自由度而设置的。

   输出请求ID、用户ID时，
   由于这些的获取源是 :java:extdoc:`ThreadContext <nablarch.core.ThreadContext>` ，
   因此处理器构成中需要包含 :ref:`thread_context_handler` 。
   特别是用户ID，请参考 :ref:`thread_context_handler-user_id_attribute_setting` 
   在应用程序中设置会话值。

 .. _jaxrs_access_log-prop_end_format:

 jaxRsAccessLogFormatter.endFormat
  请求处理结束时日志输出使用的格式。

  格式中可指定的占位符
   :状态码: $statusCode$
   :开始日期时间: $startTime$
   :结束日期时间: $endTime$
   :执行时间: $executionTime$
   :最大内存量: $maxMemory$
   :空闲内存量(开始时): $freeMemory$
   :会话存储ID: $sessionStoreId$
   :响应体: $responseBody$

  默认格式
   .. code-block:: bash

    @@@@ END @@@@ rid = [$requestId$] uid = [$userId$] sid = [$sessionId$] url = [$url$] status_code = [$statusCode$]
        \n\tstart_time     = [$startTime$]
        \n\tend_time       = [$endTime$]
        \n\texecution_time = [$executionTime$]
        \n\tmax_memory     = [$maxMemory$]
        \n\tfree_memory    = [$freeMemory$]

 jaxRsAccessLogFormatter.datePattern
  开始日期时间和结束日期时间使用的日期时间模式。
  模式中指定 :java:extdoc:`SimpleDateFormat <java.text.SimpleDateFormat>` 规定的语法。
  默认是 ``yyyy-MM-dd HH:mm:ss.SSS`` 。

 jaxRsAccessLogFormatter.maskingPatterns
  用正则表达式指定掩码对象的参数名或变量名。
  指定多个时用逗号分隔。
  用于请求参数和会话范围信息两者的掩码。
  指定的正则表达式不区分大小写。
  例如，指定 ``password`` 时，会匹配 ``password`` ``newPassword`` ``password2`` 等。

 jaxRsAccessLogFormatter.maskingChar
  掩码使用的字符。默认是 ``*`` 。

 jaxRsAccessLogFormatter.bodyLogTargetMatcher
  判定是否输出请求体和响应体的类。
  指定实现 :java:extdoc:`MessageBodyLogTargetMatcher <nablarch.fw.jaxrs.MessageBodyLogTargetMatcher>` 的类名。
  默认是 :java:extdoc:`JaxRsBodyLogTargetMatcher <nablarch.fw.jaxrs.JaxRsBodyLogTargetMatcher>` 。

 jaxRsAccessLogFormatter.bodyMaskingFilter
  对请求体和响应体进行掩码处理的类。
  指定实现 :java:extdoc:`LogContentMaskingFilter <nablarch.fw.jaxrs.LogContentMaskingFilter>` 的类名。
  默认是 :java:extdoc:`JaxRsBodyMaskingFilter <nablarch.fw.jaxrs.JaxRsBodyMaskingFilter>` 。

  .. important::
   RESTful Web服务收发的体格式有多种，但默认的 :java:extdoc:`JaxRsBodyMaskingFilter <nablarch.fw.jaxrs.JaxRsBodyMaskingFilter>` 仅支持JSON格式。

 jaxRsAccessLogFormatter.bodyMaskingItemNames
  对请求体和响应体进行掩码处理时，指定掩码对象的项目名。
  指定多个时用逗号分隔。

 jaxRsAccessLogFormatter.parametersSeparator
  请求参数的分隔符。
  默认是 ``\n\t\t`` 。

 jaxRsAccessLogFormatter.sessionScopeSeparator
  会话范围信息的分隔符。
  默认是 ``\n\t\t`` 。

 jaxRsAccessLogFormatter.beginOutputEnabled
  请求处理开始时的输出是否有效。
  默认是true。
  指定false时不在请求处理开始时输出。

 jaxRsAccessLogFormatter.endOutputEnabled
  请求处理结束时的输出是否有效。
  默认是true。
  指定false时不在请求处理结束时输出。

记述示例
 .. code-block:: properties

  jaxRsAccessLogFormatter.className=nablarch.fw.jaxrs.JaxRsAccessLogFormatter
  jaxRsAccessLogFormatter.beginFormat=> sid = [$sessionId$] @@@@ BEGIN @@@@\n\turl = [$url$]\n\tmethod = [$method$]
  jaxRsAccessLogFormatter.endFormat=< sid = [$sessionId$] @@@@ END @@@@ url = [$url$] status_code = [$statusCode$]
  jaxRsAccessLogFormatter.datePattern="yyyy-MM-dd HH:mm:ss.SSS"
  jaxRsAccessLogFormatter.maskingChar=#
  jaxRsAccessLogFormatter.maskingPatterns=password,mobilePhoneNumber
  jaxRsAccessLogFormatter.bodyLogTargetMatcher=nablarch.fw.jaxrs.JaxRsBodyLogTargetMatcher
  jaxRsAccessLogFormatter.bodyMaskingFilter=nablarch.fw.jaxrs.JaxRsBodyMaskingFilter
  jaxRsAccessLogFormatter.bodyMaskingItemNames=password,mobilePhoneNumber
  jaxRsAccessLogFormatter.parametersSeparator=,
  jaxRsAccessLogFormatter.sessionScopeSeparator=,
  jaxRsAccessLogFormatter.beginOutputEnabled=true
  jaxRsAccessLogFormatter.endOutputEnabled=true

.. _jaxrs_access_log-json_setting:

作为JSON格式的结构化日志输出
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
通过 :ref:`log-json_log_setting` 设置可以将日志输出为JSON格式，
但 :java:extdoc:`JaxRsAccessLogFormatter <nablarch.fw.jaxrs.JaxRsAccessLogFormatter>` 中
HTTP访问日志的各个项目作为字符串输出到message的值中。
要将HTTP访问日志的各个项目也作为JSON的值输出，
请使用 :java:extdoc:`JaxRsAccessJsonLogFormatter <nablarch.fw.jaxrs.JaxRsAccessJsonLogFormatter>` 。
设置是在 :ref:`log-app_log_setting` 中说明的属性文件中进行的。

记述规则
 :java:extdoc:`JaxRsAccessJsonLogFormatter <nablarch.fw.jaxrs.JaxRsAccessJsonLogFormatter>` 使用时
 指定的属性如下。
 
 httpAccessLogFormatter.className ``必需``
  JSON格式输出日志时，
  指定 :java:extdoc:`JaxRsAccessJsonLogFormatter <nablarch.fw.jaxrs.JaxRsAccessJsonLogFormatter>` 。

 .. _jaxrs_access_log-prop_begin_targets:

 jaxRsAccessLogFormatter.beginTargets
  请求处理开始时的日志输出项目。用逗号分隔指定。

  可指定的输出项目和默认输出项目
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
   :会话范围信息: sessionScope
   :客户端终端IP地址: clientIpAddress ``默认``
   :客户端终端主机: clientHost ``默认``
   :HTTP头的User-Agent: clientUserAgent
   :请求体: requestBody

  输出项目的详细说明与
  :ref:`请求处理开始时日志输出使用的格式 <jaxrs_access_log-prop_begin_format>`
  的占位符相同，因此省略。

 jaxRsAccessLogFormatter.endTargets
  请求处理结束时的日志输出项目。用逗号分隔指定。

  可指定的输出项目和默认输出项目
   :标签: label ``默认``
   :请求ID: requestId ``默认``
   :用户ID: userId ``默认``
   :HTTP会话ID: sessionId ``默认``
   :会话存储ID: sessionStoreId
   :URL: url ``默认``
   :状态码: statusCode ``默认``
   :开始日期时间: startTime ``默认``
   :结束日期时间: endTime ``默认``
   :执行时间: executionTime ``默认``
   :最大内存量: maxMemory ``默认``
   :空闲内存量(开始时): freeMemory ``默认``
   :响应体: responseBody

  输出项目的详细说明与
  :ref:`请求处理结束时日志输出使用的格式 <jaxrs_access_log-prop_end_format>`
  的占位符相同，因此省略。

 jaxRsAccessLogFormatter.datePattern
  开始日期时间和结束日期时间使用的日期时间模式。
  模式中指定 :java:extdoc:`SimpleDateFormat <java.text.SimpleDateFormat>` 规定的语法。
  默认是 ``yyyy-MM-dd HH:mm:ss.SSS`` 。

 jaxRsAccessLogFormatter.maskingPatterns
  用正则表达式指定掩码对象的参数名或变量名（部分匹配）。
  指定多个时用逗号分隔。
  用于请求参数和会话范围信息两者的掩码。
  指定的正则表达式不区分大小写。
  例如，指定 ``password`` 时，会匹配 ``password`` ``newPassword`` ``password2`` 等。

 jaxRsAccessLogFormatter.maskingChar
  掩码使用的字符。默认是 ``*`` 。

 jaxRsAccessLogFormatter.beginOutputEnabled
  请求处理开始时的输出是否有效。
  默认是true。
  指定false时不在请求处理开始时输出。

 jaxRsAccessLogFormatter.endOutputEnabled
  请求处理结束时的输出是否有效。
  默认是true。
  指定false时不在请求处理结束时输出。

 jaxRsAccessLogFormatter.beginLabel
  请求处理开始时日志的label输出的值。
  默认是 ``"HTTP ACCESS BEGIN"``。

 jaxRsAccessLogFormatter.endLabel
  请求处理结束时日志的label输出的值。
  默认是 ``"HTTP ACCESS END"``。

 jaxRsAccessLogFormatter.structuredMessagePrefix
  为了能够识别格式化后的消息字符串已格式化为JSON格式，在消息开头附加的标记字符串。
  当消息开头的标记字符串与 :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` 中设置的标记字符串一致时， :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` 会将消息作为JSON数据处理。
  默认是 ``"$JSON$"`` 。
  更改时，请使用LogWriter的 ``structuredMessagePrefix`` 属性将相同值也设置到 :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` （关于LogWriter的属性请参考 :ref:`log-basic_setting` ）。

记述示例
 .. code-block:: properties

  httpAccessLogFormatter.className=nablarch.fw.jaxrs.JaxRsAccessJsonLogFormatter
  httpAccessLogFormatter.structuredMessagePrefix=$JSON$
  httpAccessLogFormatter.beginTargets=sessionId,url,method
  httpAccessLogFormatter.endTargets=sessionId,url,statusCode
  httpAccessLogFormatter.beginLabel=HTTP ACCESS BEGIN
  httpAccessLogFormatter.endLabel=HTTP ACCESS END

.. _jaxrs_access_log-session_store_id:

关于会话存储ID
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

输出中包含会话存储ID时，会输出 :ref:`session_store` 发行的用于识别会话的ID。

此值使用 :ref:`session_store_handler` 去程中记录的值。
因此要在日志中输出会话存储ID时， :ref:`jaxrs_access_log_handler` 必须配置在 :ref:`session_store_handler` 之后。

会话存储ID在请求处理开始时的状态下固定，因此有以下规格：

* 在会话存储ID尚未发行的请求中，即使途中发行了ID，同一请求内输出的会话存储ID也都为空
* 即使途中 :java:extdoc:`销毁会话 <nablarch.common.web.session.SessionUtil.invalidate(nablarch.fw.ExecutionContext)>` 或 :java:extdoc:`更改ID <nablarch.common.web.session.SessionUtil.changeId(nablarch.fw.ExecutionContext)>` ，日志中输出的值也不会从请求处理开始时的值发生变化
