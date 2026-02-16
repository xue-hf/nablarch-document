.. _performance_log:

性能日志的输出
==================================================

.. contents:: 目录
  :depth: 3
  :local:

性能日志输出任意处理范围的执行时间和内存使用量，
用于开发时的性能调优。
应用程序在源代码上调用框架提供的API，指定测量对象的处理范围来输出。

性能日志的输出策略
--------------------------------------------------
性能日志由于获取堆大小等原因可能会影响性能。
因此假设在开发时使用，以DEBUG级别输出。

.. list-table:: 性能日志的输出策略
   :header-rows: 1
   :class: white-space-normal
   :widths: 15,15

   * - 日志级别
     - 日志记录器名称

   * - DEBUG
     - PERFORMANCE

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

  availableLoggersNamesOrder=PER,ROO

  # 应用程序日志的设置
  loggers.ROO.nameRegex=.*
  loggers.ROO.level=INFO
  loggers.ROO.writerNames=appLog

  # 性能日志的设置
  loggers.PER.nameRegex=PERFORMANCE
  loggers.PER.level=DEBUG
  loggers.PER.writerNames=appLog

app-log.properties的设置示例
 .. code-block:: properties

  # PerformanceLogFormatter
  #performanceLogFormatter.className=
  #performanceLogFormatter.targetPoints=
  #performanceLogFormatter.datePattern=
  performanceLogFormatter.format=\n\tpoint = [$point$] result = [$result$]\
                                 \n\tstart_time = [$startTime$] end_time = [$endTime$]\
                                 \n\texecution_time = [$executionTime$]\
                                 \n\tmax_memory = [$maxMemory$]\
                                 \n\tstart_free_memory = [$startFreeMemory$] start_used_memory = [$startUsedMemory$]\
                                 \n\tend_free_memory = [$endFreeMemory$] end_used_memory = [$endUsedMemory$]

使用方法
--------------------------------------------------

.. _performance_log-logging:

输出性能日志
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
性能日志使用 :java:extdoc:`PerformanceLogUtil <nablarch.core.log.app.PerformanceLogUtil>` 来输出。
:java:extdoc:`PerformanceLogUtil <nablarch.core.log.app.PerformanceLogUtil>` 提供了
处理开始时调用的 :java:extdoc:`PerformanceLogUtil#start <nablarch.core.log.app.PerformanceLogUtil.start(java.lang.String)>` 和
结束时调用的 :java:extdoc:`PerformanceLogUtil#end <nablarch.core.log.app.PerformanceLogUtil.end(java.lang.String,java.lang.String,java.lang.Object...)>` 。
:java:extdoc:`PerformanceLogUtil <nablarch.core.log.app.PerformanceLogUtil>` 在
:java:extdoc:`PerformanceLogUtil#end <nablarch.core.log.app.PerformanceLogUtil.end(java.lang.String,java.lang.String,java.lang.Object...)>`
被调用时，会一并输出 :java:extdoc:`PerformanceLogUtil#start <nablarch.core.log.app.PerformanceLogUtil.start(java.lang.String)>`
获取的日期时间、内存使用量。

:java:extdoc:`PerformanceLogUtil <nablarch.core.log.app.PerformanceLogUtil>` 的使用示例如下。

.. code-block:: java

 // start方法中，指定用于识别测量对象的点。
 // 为防止误设置导致的无效输出，
 // 如果此点名称未在配置文件中定义，则不会输出日志。
 String point = "UserSearchAction#doUSERS00101";
 PerformanceLogUtil.start(point);

 // 执行搜索
 UserSearchService searchService = new UserSearchService();
 SqlResultSet searchResult = searchService.selectByCondition(condition);

 // end方法中，可以指定点、表示处理结果的字符串、日志输出的可选信息。
 // 以下未指定日志输出的可选信息。
 PerformanceLogUtil.end(point, String.valueOf(searchResult.size()));

.. important::
 :java:extdoc:`PerformanceLogUtil <nablarch.core.log.app.PerformanceLogUtil>` 以
 :ref:`执行时ID <log-execution_id>` ＋点名称唯一识别测量对象。
 因此，请注意在递归调用中使用 :java:extdoc:`PerformanceLogUtil <nablarch.core.log.app.PerformanceLogUtil>`
 将无法进行测量。

.. _performance_log-setting:

性能日志的设置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
性能日志的设置是在 :ref:`log-app_log_setting` 中说明的属性文件中进行的。

记述规则
 \

 performanceLogFormatter.className
  实现 :java:extdoc:`PerformanceLogFormatter <nablarch.core.log.app.PerformanceLogFormatter>` 的类。
  在替换时指定。

 performanceLogFormatter.format
  性能日志各个项目的格式。

  格式中可指定的占位符
   :识别测量对象的ID: $point$
   :表示处理结果的字符串: $result$
   :处理开始日期时间: $startTime$
   :处理结束日期时间: $endTime$
   :处理执行时间(结束日期时间 - 开始日期时间): $executionTime$
   :处理开始时的堆大小: $maxMemory$
   :处理开始时的空闲堆大小: $startFreeMemory$
   :处理开始时的使用堆大小: $startUsedMemory$
   :处理结束时的空闲堆大小: $endFreeMemory$
   :处理结束时的使用堆大小: $endUsedMemory$

  默认格式
   .. code-block:: bash

    \n\tpoint = [$point$] result = [$result$]
    \n\tstart_time = [$startTime$] end_time = [$endTime$]
    \n\texecution_time = [$executionTime$]
    \n\tmax_memory = [$maxMemory$]
    \n\tstart_free_memory = [$startFreeMemory$] start_used_memory = [$startUsedMemory$]
    \n\tend_free_memory = [$endFreeMemory$] end_used_memory = [$endUsedMemory$]

 performanceLogFormatter.datePattern
  开始日期时间和结束日期时间使用的日期时间模式。
  模式中指定 :java:extdoc:`SimpleDateFormat <java.text.SimpleDateFormat>` 规定的语法。
  默认是"yyyy-MM-dd HH:mm:ss.SSS"。

 performanceLogFormatter.targetPoints
  作为输出对象的点名称。
  指定多个时用逗号分隔。
  性能日志为防止误设置导致的无效输出，根据此设置进行输出。

记述示例
 .. code-block:: properties

  performanceLogFormatter.className=nablarch.core.log.app.PerformanceLogFormatter
  performanceLogFormatter.targetPoints=UserSearchAction#doUSERS00101
  performanceLogFormatter.datePattern=yyyy-MM-dd HH:mm:ss.SSS
  performanceLogFormatter.format=point:$point$ result:$result$ exe_time:$executionTime$ms

.. _performance_log-json_setting:

作为JSON格式的结构化日志输出
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
通过 :ref:`log-json_log_setting` 设置可以将日志输出为JSON格式，
但 :java:extdoc:`PerformanceLogFormatter <nablarch.core.log.app.PerformanceLogFormatter>` 中
性能日志的各个项目作为字符串输出到message的值中。
要将性能日志的各个项目也作为JSON的值输出，
请使用 :java:extdoc:`PerformanceJsonLogFormatter <nablarch.core.log.app.PerformanceJsonLogFormatter>` 。
设置是在 :ref:`log-app_log_setting` 中说明的属性文件中进行的。

记述规则
 :java:extdoc:`PerformanceJsonLogFormatter <nablarch.core.log.app.PerformanceJsonLogFormatter>` 使用时
 指定的属性如下。
 
 performanceLogFormatter.className ``必需``
  JSON格式输出日志时，
  指定 :java:extdoc:`PerformanceJsonLogFormatter <nablarch.core.log.app.PerformanceJsonLogFormatter>` 。

 performanceLogFormatter.targets
  性能日志的输出项目。用逗号分隔指定。

  可指定的输出项目
   :识别测量对象的ID: point
   :表示处理结果的字符串: result
   :处理开始日期时间: startTime
   :处理结束日期时间: endTime
   :处理执行时间(结束日期时间 - 开始日期时间): executionTime
   :处理开始时的堆大小: maxMemory
   :处理开始时的空闲堆大小: startFreeMemory
   :处理开始时的使用堆大小: startUsedMemory
   :处理结束时的空闲堆大小: endFreeMemory
   :处理结束时的使用堆大小: endUsedMemory

  默认所有输出项目都是对象。

 performanceLogFormatter.datePattern
  开始日期时间和结束日期时间使用的日期时间模式。
  模式中指定 :java:extdoc:`SimpleDateFormat <java.text.SimpleDateFormat>` 规定的语法。
  默认是"yyyy-MM-dd HH:mm:ss.SSS"。

 performanceLogFormatter.targetPoints
  作为输出对象的点名称。
  指定多个时用逗号分隔。
  性能日志为防止误设置导致的无效输出，根据此设置进行输出。

 performanceLogFormatter.structuredMessagePrefix
  为了能够识别格式化后的消息字符串已格式化为JSON格式，在消息开头附加的标记字符串。
  当消息开头的标记字符串与 :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` 中设置的标记字符串一致时， :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` 会将消息作为JSON数据处理。
  默认是 ``"$JSON$"`` 。
  更改时，请使用LogWriter的 ``structuredMessagePrefix`` 属性将相同值也设置到 :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` （关于LogWriter的属性请参考 :ref:`log-basic_setting` ）。

记述示例
 .. code-block:: properties

  performanceLogFormatter.className=nablarch.core.log.app.PerformanceJsonLogFormatter
  performanceLogFormatter.structuredMessagePrefix=$JSON$
  performanceLogFormatter.targetPoints=UserSearchAction#doUSERS00101
  performanceLogFormatter.datePattern=yyyy-MM-dd'T'HH:mm:ss.SSS'Z'
  performanceLogFormatter.targets=point,result,executionTime
