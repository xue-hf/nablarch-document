.. _messaging_log:

消息处理日志的输出
==================================================

.. contents:: 目录
  :depth: 3
  :local:

消息处理日志是在 :ref:`system_messaging` 中消息收发时输出的。
应用程序通过设置日志输出来进行输出。

消息处理日志的输出策略
--------------------------------------------------
消息处理日志输出到应用程序整体日志输出的应用程序日志中。

.. list-table:: 消息处理日志的输出策略
   :header-rows: 1
   :class: white-space-normal
   :widths: 50,50

   * - 日志级别
     - 日志记录器名称

   * - INFO
     - MESSAGING

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

  availableLoggersNamesOrder=MESSAGING,ROO

  # 应用程序日志的设置
  loggers.ROO.nameRegex=.*
  loggers.ROO.level=INFO
  loggers.ROO.writerNames=appLog

  # 消息处理日志的设置
  loggers.MESSAGING.nameRegex=MESSAGING
  loggers.MESSAGING.level=INFO
  loggers.MESSAGING.writerNames=appLog

app-log.properties的设置示例
 .. code-block:: properties

  # MessagingLogFormatter
  #messagingLogFormatter.className=
  #messagingLogFormatter.maskingChar=
  #messagingLogFormatter.maskingPatterns=
  # MOM消息处理用格式
  messagingLogFormatter.sentMessageFormat=@@@@ SENT MESSAGE @@@@\
                                            \n\tthread_name    = [$threadName$]\
                                            \n\tmessage_id     = [$messageId$]\
                                            \n\tdestination    = [$destination$]\
                                            \n\tcorrelation_id = [$correlationId$]\
                                            \n\treply_to       = [$replyTo$]\
                                            \n\ttime_to_live   = [$timeToLive$]\
                                            \n\tmessage_body   = [$messageBody$]
  messagingLogFormatter.receivedMessageFormat=@@@@ RECEIVED MESSAGE @@@@\
                                                \n\tthread_name    = [$threadName$]\
                                                \n\tmessage_id     = [$messageId$]\
                                                \n\tdestination    = [$destination$]\
                                                \n\tcorrelation_id = [$correlationId$]\
                                                \n\treply_to       = [$replyTo$]\
                                                \n\tmessage_body   = [$messageBody$]
  # HTTP消息处理用格式
  messagingLogFormatter.httpSentMessageFormat=@@@@ HTTP SENT MESSAGE @@@@\
                                                \n\tthread_name    = [$threadName$]\
                                                \n\tmessage_id     = [$messageId$]\
                                                \n\tdestination    = [$destination$]\
                                                \n\tcorrelation_id = [$correlationId$]\
                                                \n\tmessage_header = [$messageHeader$]\
                                                \n\tmessage_body   = [$messageBody$]
  messagingLogFormatter.httpReceivedMessageFormat=@@@@ HTTP RECEIVED MESSAGE @@@@\
                                                    \n\tthread_name    = [$threadName$]\
                                                    \n\tmessage_id     = [$messageId$]\
                                                    \n\tdestination    = [$destination$]\
                                                    \n\tcorrelation_id = [$correlationId$]\
                                                    \n\tmessage_header = [$messageHeader$]\
                                                    \n\tmessage_body   = [$messageBody$]

使用方法
--------------------------------------------------

.. _messaging_log-setting:

消息处理日志的设置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
消息处理日志的设置是在 :ref:`log-app_log_setting` 中说明的属性文件中进行的。

记述规则
 \

 messagingLogFormatter.className
  实现 :java:extdoc:`MessagingLogFormatter <nablarch.fw.messaging.logging.MessagingLogFormatter>` 的类。
  在替换时指定。

 messagingLogFormatter.maskingPatterns
  用正则表达式指定消息正文的掩码对象字符串。
  正则表达式中指定的第一个捕获部分（括号内的部分）成为掩码对象。

  例如将模式指定为「<password>(.+?)</password>」，
  实际电文中包含「<password>hoge</password>」时，
  输出的字符串将变为「<password>****</password>」。

  指定多个时用逗号分隔。
  指定的正则表达式不区分大小写。

 messagingLogFormatter.maskingChar
  掩码使用的字符。默认是'*'。

 messagingLogFormatter.sentMessageFormat
  MOM发送消息的日志输出使用的格式。

  格式中可指定的占位符
   :线程名: $threadName$
   :消息ID: $messageId$
   :发送目标: $destination$
   :相关消息ID: $correlationId$
   :响应目标: $replyTo$
   :有效期: $timeToLive$
   :消息体的内容: $messageBody$ [#placeholder]_
   :消息体的十六进制转储: $messageBodyHex$ [#placeholder]_
   :消息体的字节长度: $messageBodyLength$

  默认格式
   .. code-block:: bash

    @@@@ SENT MESSAGE @@@@
        \n\tthread_name    = [$threadName$]
        \n\tmessage_id     = [$messageId$]
        \n\tdestination    = [$destination$]
        \n\tcorrelation_id = [$correlationId$]
        \n\treply_to       = [$replyTo$]
        \n\ttime_to_live   = [$timeToLive$]
        \n\tmessage_body   = [$messageBody$]

 messagingLogFormatter.receivedMessageFormat
  MOM接收消息的日志输出使用的格式。

  格式中可指定的占位符
   :线程名: $threadName$
   :消息ID: $messageId$
   :发送目标: $destination$
   :相关消息ID: $correlationId$
   :响应目标: $replyTo$
   :有效期: $timeToLive$
   :消息体的内容: $messageBody$ [#placeholder]_
   :消息体的十六进制转储: $messageBodyHex$ [#placeholder]_
   :消息体的字节长度: $messageBodyLength$

  默认格式
   .. code-block:: bash

    @@@@ RECEIVED MESSAGE @@@@
        \n\tthread_name    = [$threadName$]
        \n\tmessage_id     = [$messageId$]
        \n\tdestination    = [$destination$]
        \n\tcorrelation_id = [$correlationId$]
        \n\treply_to       = [$replyTo$]
        \n\tmessage_body   = [$messageBody$]

 messagingLogFormatter.httpSentMessageFormat
  HTTP发送消息的日志输出使用的格式。

  格式中可指定的占位符
   :线程名: $threadName$
   :消息ID: $messageId$
   :发送目标: $destination$
   :相关消息ID: $correlationId$
   :消息体的内容: $messageBody$ [#placeholder]_
   :消息体的十六进制转储: $messageBodyHex$ [#placeholder]_
   :消息体的字节长度: $messageBodyLength$
   :消息的头部: $messageHeader$

  默认格式
   .. code-block:: bash

    @@@@ HTTP SENT MESSAGE @@@@
        \n\tthread_name    = [$threadName$]
        \n\tmessage_id     = [$messageId$]
        \n\tdestination    = [$destination$]
        \n\tcorrelation_id = [$correlationId$]
        \n\tmessage_header = [$messageHeader$]
        \n\tmessage_body   = [$messageBody$]

 messagingLogFormatter.httpReceivedMessageFormat
  HTTP接收消息的日志输出使用的格式。

  格式中可指定的占位符
   :线程名: $threadName$
   :消息ID: $messageId$
   :发送目标: $destination$
   :相关消息ID: $correlationId$
   :消息体的内容: $messageBody$ [#placeholder]_
   :消息体的十六进制转储: $messageBodyHex$ [#placeholder]_
   :消息体的字节长度: $messageBodyLength$
   :消息的头部: $messageHeader$

  默认格式
   .. code-block:: bash

    @@@@ HTTP RECEIVED MESSAGE @@@@
        \n\tthread_name    = [$threadName$]
        \n\tmessage_id     = [$messageId$]
        \n\tdestination    = [$destination$]
        \n\tcorrelation_id = [$correlationId$]
        \n\tmessage_header = [$messageHeader$]
        \n\tmessage_body   = [$messageBody$]

.. [#placeholder]


  * **$messageBody$:** 以ISO-8859-1固定编码电文的结果输出。
  * **$messageBodyHex$:** 将$messageBody$的内容进行十六进制转储后输出。

记述示例
 .. code-block:: properties

  messagingLogFormatter.className=nablarch.fw.messaging.logging.MessagingLogFormatter
  messagingLogFormatter.maskingChar=#
  messagingLogFormatter.maskingPatterns=<password>(.+?)</password>,<mobilePhoneNumber>(.+?)</mobilePhoneNumber>

  # MOM消息处理用格式
  messagingLogFormatter.sentMessageFormat=@@@@ SENT MESSAGE @@@@\n\tthread_name    = [$threadName$]\n\tmessage_id     = [$messageId$]\n\tdestination    = [$destination$]\n\tcorrelation_id = [$correlationId$]\n\treply_to       = [$replyTo$]\n\ttime_to_live   = [$timeToLive$]\n\tmessage_body   = [$messageBody$]
  messagingLogFormatter.receivedMessageFormat=@@@@ RECEIVED MESSAGE @@@@\n\tthread_name    = [$threadName$]\n\tmessage_id     = [$messageId$]\n\tdestination    = [$destination$]\n\tcorrelation_id = [$correlationId$]\n\treply_to       = [$replyTo$]\n\tmessage_body   = [$messageBody$]

  # HTTP消息处理用格式
  messagingLogFormatter.httpSentMessageFormat=@@@@ HTTP SENT MESSAGE @@@@\n\tthread_name    = [$threadName$]\n\tmessage_id     = [$messageId$]\n\tdestination    = [$destination$]\n\tcorrelation_id = [$correlationId$]\n\tmessage_header = [$messageHeader$]\n\tmessage_body   = [$messageBody$]
  messagingLogFormatter.httpReceivedMessageFormat=@@@@ HTTP RECEIVED MESSAGE @@@@\n\tthread_name    = [$threadName$]\n\tmessage_id     = [$messageId$]\n\tdestination    = [$destination$]\n\tcorrelation_id = [$correlationId$]\n\tmessage_header = [$messageHeader$]\n\tmessage_body   = [$messageBody$]

.. _messaging_log-json_setting:

作为JSON格式的结构化日志输出
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
通过 :ref:`log-json_log_setting` 设置可以将日志输出为JSON格式，
但 :java:extdoc:`MessagingLogFormatter <nablarch.fw.messaging.logging.MessagingLogFormatter>` 中
消息处理日志的各个项目作为字符串输出到message的值中。
要将消息处理日志的各个项目也作为JSON的值输出，
请使用 :java:extdoc:`MessagingJsonLogFormatter <nablarch.fw.messaging.logging.MessagingJsonLogFormatter>` 。
设置是在 :ref:`log-app_log_setting` 中说明的属性文件中进行的。

记述规则
 :java:extdoc:`MessagingJsonLogFormatter <nablarch.fw.messaging.logging.MessagingJsonLogFormatter>` 使用时
 指定的属性如下。
 
 messagingLogFormatter.className ``必需``
  JSON格式输出日志时，
  指定 :java:extdoc:`MessagingJsonLogFormatter <nablarch.fw.messaging.logging.MessagingJsonLogFormatter>` 。

 messagingLogFormatter.maskingPatterns
  用正则表达式指定消息正文的掩码对象字符串。
  正则表达式中指定的第一个捕获部分（括号内的部分）成为掩码对象。

  例如将模式指定为「<password>(.+?)</password>」，
  实际电文中包含「<password>hoge</password>」时，
  输出的字符串将变为「<password>****</password>」。

  指定多个时用逗号分隔。
  指定的正则表达式不区分大小写。

 messagingLogFormatter.maskingChar
  掩码使用的字符。默认是'*'。

 messagingLogFormatter.sentMessageTargets
  MOM发送消息日志的输出项目。用逗号分隔指定。

  可指定的输出项目和默认输出项目
   :标签: label ``默认``
   :线程名: threadName ``默认``
   :消息ID: messageId ``默认``
   :发送目标: destination ``默认``
   :相关消息ID: correlationId ``默认``
   :响应目标: replyTo ``默认``
   :有效期: timeToLive ``默认``
   :消息体的内容: messageBody [#placeholder_json]_ ``默认``
   :消息体的十六进制转储: messageBodyHex [#placeholder_json]_
   :消息体的字节长度: messageBodyLength

 messagingLogFormatter.receivedMessageTargets
  MOM接收消息日志的输出项目。用逗号分隔指定。

  可指定的输出项目和默认输出项目
   :标签: label ``默认``
   :线程名: threadName ``默认``
   :消息ID: messageId ``默认``
   :发送目标: destination ``默认``
   :相关消息ID: correlationId ``默认``
   :响应目标: replyTo ``默认``
   :有效期: timeToLive
   :消息体的内容: messageBody [#placeholder_json]_ ``默认``
   :消息体的十六进制转储: messageBodyHex [#placeholder_json]_
   :消息体的字节长度: messageBodyLength

 messagingLogFormatter.httpSentMessageTargets
  HTTP发送消息日志的输出项目。用逗号分隔指定。

  可指定的输出项目和默认输出项目
   :标签: label ``默认``
   :线程名: threadName ``默认``
   :消息ID: messageId ``默认``
   :发送目标: destination ``默认``
   :相关消息ID: correlationId ``默认``
   :消息体的内容: messageBody [#placeholder_json]_ ``默认``
   :消息体的十六进制转储: messageBodyHex [#placeholder_json]_
   :消息体的字节长度: messageBodyLength
   :消息的头部: messageHeader ``默认``

 messagingLogFormatter.httpReceivedMessageTargets
  HTTP接收消息日志的输出项目。用逗号分隔指定。

  可指定的输出项目和默认输出项目
   :标签: label ``默认``
   :线程名: threadName ``默认``
   :消息ID: messageId ``默认``
   :发送目标: destination ``默认``
   :相关消息ID: correlationId ``默认``
   :消息体的内容: messageBody [#placeholder_json]_ ``默认``
   :消息体的十六进制转储: messageBodyHex [#placeholder_json]_
   :消息体的字节长度: messageBodyLength
   :消息的头部: messageHeader ``默认``

 messagingLogFormatter.sentMessageLabel
  MOM发送消息日志的label输出的值。
  默认是 ``"SENT MESSAGE"``。

 messagingLogFormatter.receivedMessageLabel
  MOM接收消息日志的label输出的值。
  默认是 ``"RECEIVED MESSAGE"``。

 messagingLogFormatter.httpSentMessageLabel
  HTTP发送消息日志的label输出的值。
  默认是 ``"HTTP SENT MESSAGE"``。

 messagingLogFormatter.httpReceivedMessageLabel
  HTTP接收消息日志的label输出的值。
  默认是 ``"HTTP RECEIVED MESSAGE"``。

 messagingLogFormatter.structuredMessagePrefix
  为了能够识别格式化后的消息字符串已格式化为JSON格式，在消息开头附加的标记字符串。
  当消息开头的标记字符串与 :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` 中设置的标记字符串一致时， :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` 会将消息作为JSON数据处理。
  默认是 ``"$JSON$"`` 。
  更改时，请使用LogWriter的 ``structuredMessagePrefix`` 属性将相同值也设置到 :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` （关于LogWriter的属性请参考 :ref:`log-basic_setting` ）。

.. [#placeholder_json]

  * **messageBody:** 以ISO-8859-1固定编码电文的结果输出。
  * **messageBodyHex:** 将messageBody的内容进行十六进制转储后输出。

记述示例
 .. code-block:: properties

  messagingLogFormatter.className=nablarch.fw.messaging.logging.MessagingJsonLogFormatter
  messagingLogFormatter.structuredMessagePrefix=$JSON$

  # MOM消息处理用格式
  messagingLogFormatter.sentMessageTargets=threadName,messageId,destination,correlationId,replyTo,timeToLive,messageBody
  messagingLogFormatter.receivedMessageTargets=threadName,messageId,destination,correlationId,replyTo,messageBody

  # HTTP消息处理用格式
  messagingLogFormatter.httpSentMessageTargets=threadName,messageId,destination,correlationId,messageHeader,messageBody
  messagingLogFormatter.httpReceivedMessageTargets=threadName,messageId,destination,correlationId,messageHeader,messageBody
