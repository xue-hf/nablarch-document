.. _sql_log:

SQL日志的输出
==================================================

.. contents:: 目录
  :depth: 3
  :local:

SQL日志用于性能调优，输出SQL语句的执行时间和SQL语句。
应用程序通过设置日志输出来输出。

SQL日志的输出策略
--------------------------------------------------
SQL日志可能会导致日志大小增大、磁盘满或影响性能。
因此，SQL日志设想在开发时使用，以DEBUG级别或更低级别输出。

.. list-table:: SQL日志的输出策略
   :header-rows: 1
   :class: white-space-normal
   :widths: 15,15,70

   * - 日志级别
     - 日志记录器名称
     - 输出内容

   * - DEBUG
     - SQL
     - SQL语句、执行时间、件数(检索件数或更新件数等)、事务处理结果(提交或回滚)

   * - TRACE
     - SQL
     - SQL参数(绑定变量的值)

下面显示上述输出策略的日志输出设置示例。

log.properties的设置示例
 .. code-block:: properties

  writerNames=appLog

  # 应用程序日志的输出目的地
  writer.appLog.className=nablarch.core.log.basic.FileLogWriter
  writer.appLog.filePath=/var/log/app/app.log
  writer.appLog.encoding=UTF-8
  writer.appLog.maxFileSize=10000
  writer.appLog.formatter.className=nablarch.core.log.basic.BasicLogFormatter
  writer.appLog.formatter.format=$date$ -$logLevel$- $runtimeLoggerName$ [$executionId$] boot_proc = [$bootProcess$] proc_sys = [$processingSystem$] req_id = [$requestId$] usr_id = [$userId$] $message$$information$$stackTrace$

  availableLoggersNamesOrder=SQL,ROO

  # 应用程序日志的设置
  loggers.ROO.nameRegex=.*
  loggers.ROO.level=INFO
  loggers.ROO.writerNames=appLog

  # SQL日志的设置
  loggers.SQL.nameRegex=SQL
  loggers.SQL.level=TRACE
  loggers.SQL.writerNames=appLog

app-log.properties的设置示例
 .. code-block:: properties

  # SqlLogFormatter
  #sqlLogFormatter.className=
  # SqlPStatement#retrieve的格式
  sqlLogFormatter.startRetrieveFormat=$methodName$\
                                        \n\tSQL = [$sql$]\
                                        \n\tstart_position = [$startPosition$] size = [$size$]\
                                        \n\tquery_timeout = [$queryTimeout$] fetch_size = [$fetchSize$]\
                                        \n\tadditional_info:\
                                        \n\t$additionalInfo$
  sqlLogFormatter.endRetrieveFormat=$methodName$\
                                      \n\texecute_time(ms) = [$executeTime$] retrieve_time(ms) = [$retrieveTime$] count = [$count$]
  # SqlPStatement#execute的格式
  sqlLogFormatter.startExecuteFormat=$methodName$\
                                        \n\tSQL = [$sql$]\
                                        \n\tadditional_info:\
                                        \n\t$additionalInfo$
  sqlLogFormatter.endExecuteFormat=$methodName$\
                                      \n\texecute_time(ms) = [$executeTime$]
  # SqlPStatement#executeQuery的格式
  sqlLogFormatter.startExecuteQueryFormat=$methodName$\
                                            \n\tSQL = [$sql$]\
                                            \n\tadditional_info:\
                                            \n\t$additionalInfo$
  sqlLogFormatter.endExecuteQueryFormat=$methodName$\
                                          \n\texecute_time(ms) = [$executeTime$]
  # SqlPStatement#executeUpdate的格式
  sqlLogFormatter.startExecuteUpdateFormat=$methodName$\
                                              \n\tSQL = [$sql$]\
                                              \n\tadditional_info:\
                                              \n\t$additionalInfo$
  sqlLogFormatter.endExecuteUpdateFormat=$methodName$\
                                          \n\texecute_time(ms) = [$executeTime$] update_count = [$updateCount$]
  # SqlStatement#executeBatch的格式
  sqlLogFormatter.startExecuteBatchFormat=$methodName$\
                                            \n\tSQL = [$sql$]\
                                            \n\tadditional_info:\
                                            \n\t$additionalInfo$
  sqlLogFormatter.endExecuteBatchFormat=$methodName$\
                                          \n\texecute_time(ms) = [$executeTime$] batch_count = [$updateCount$]

使用方法
--------------------------------------------------

.. _sql_log-setting:

SQL日志的设置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SQL日志的设置，在 :ref:`log-app_log_setting` 中说明的属性文件中进行。

记述规则
 \

 sqlLogFormatter.className
  :java:extdoc:`SqlLogFormatter <nablarch.core.db.statement.SqlLogFormatter>` 的实现类。
  替换时指定。

 sqlLogFormatter.startRetrieveFormat
  :java:extdoc:`SqlPStatement#retrieve <nablarch.core.db.statement.SqlPStatement.retrieve()>`
  开始时使用的格式。

  格式中可指定的占位符
   :方法名: $methodName$
   :SQL语句: $sql$
   :获取开始位置: $startPosition$
   :获取最大件数: $size$
   :超时时间: $queryTimeout$
   :获取行数: $fetchSize$
   :附加信息: $additionalInfo$

  默认格式
   .. code-block:: bash

    $methodName$
        \n\tSQL = [$sql$]
        \n\tstart_position = [$startPosition$] size = [$size$]
        \n\tquery_timeout = [$queryTimeout$] fetch_size = [$fetchSize$]
        \n\tadditional_info:
        \n\t$additionalInfo$

 sqlLogFormatter.endRetrieveFormat
  :java:extdoc:`SqlPStatement#retrieve <nablarch.core.db.statement.SqlPStatement.retrieve()>`
  结束时使用的格式。

  格式中可指定的占位符
   :方法名: $methodName$
   :执行时间: $executeTime$
   :数据获取时间: $retrieveTime$
   :检索件数: $count$

  默认格式
   .. code-block:: bash

    $methodName$
        \n\texecute_time(ms) = [$executeTime$] retrieve_time(ms) = [$retrieveTime$] count = [$count$]

 sqlLogFormatter.startExecuteFormat
  :java:extdoc:`SqlPStatement#execute <nablarch.core.db.statement.SqlPStatement.execute()>`
  开始时使用的格式。

  格式中可指定的占位符
   :方法名: $methodName$
   :SQL语句: $sql$
   :附加信息: $additionalInfo$

  默认格式
   .. code-block:: bash

    $methodName$
        \n\tSQL = [$sql$]
        \n\tadditional_info:
        \n\t$additionalInfo$

 sqlLogFormatter.endExecuteFormat
  :java:extdoc:`SqlPStatement#execute <nablarch.core.db.statement.SqlPStatement.execute()>`
  结束时使用的格式。

  格式中可指定的占位符
   :方法名: $methodName$
   :执行时间: $executeTime$

  默认格式
   .. code-block:: bash

    $methodName$
        \n\texecute_time(ms) = [$executeTime$]

 sqlLogFormatter.startExecuteQueryFormat
  :java:extdoc:`SqlPStatement#executeQuery <nablarch.core.db.statement.SqlPStatement.executeQuery()>`
  开始时使用的格式。

  格式中可指定的占位符
   :方法名: $methodName$
   :SQL语句: $sql$
   :附加信息: $additionalInfo$

  默认格式
   .. code-block:: bash

    $methodName$
        \n\tSQL = [$sql$]
        \n\tadditional_info:
        \n\t$additionalInfo$

 sqlLogFormatter.endExecuteQueryFormat
  :java:extdoc:`SqlPStatement#executeQuery <nablarch.core.db.statement.SqlPStatement.executeQuery()>`
  结束时使用的格式。

  格式中可指定的占位符
   :方法名: $methodName$
   :执行时间: $executeTime$

  默认格式
   .. code-block:: bash

    $methodName$
        \n\texecute_time(ms) = [$executeTime$]

 sqlLogFormatter.startExecuteUpdateFormat
  :java:extdoc:`SqlPStatement#executeUpdate <nablarch.core.db.statement.SqlPStatement.executeUpdate()>`
  开始时使用的格式。

  格式中可指定的占位符
   :方法名: $methodName$
   :SQL语句: $sql$
   :附加信息: $additionalInfo$

  默认格式
   .. code-block:: bash

    $methodName$
        \n\tSQL = [$sql$]
        \n\tadditional_info:
        \n\t$additionalInfo$

 sqlLogFormatter.endExecuteUpdateFormat
  :java:extdoc:`SqlPStatement#executeUpdate <nablarch.core.db.statement.SqlPStatement.executeUpdate()>`
  结束时使用的格式。

  格式中可指定的占位符
   :方法名: $methodName$
   :执行时间: $executeTime$
   :更新件数: $updateCount$

  默认格式
   .. code-block:: bash

    $methodName$
        \n\texecute_time(ms) = [$executeTime$] update_count = [$updateCount$]

 sqlLogFormatter.startExecuteBatchFormat
  :java:extdoc:`SqlStatement#executeBatch <nablarch.core.db.statement.SqlStatement.executeBatch()>`
  开始时使用的格式。

  格式中可指定的占位符
   :方法名: $methodName$
   :SQL语句: $sql$
   :附加信息: $additionalInfo$

  默认格式
   .. code-block:: bash

    $methodName$
        \n\tSQL = [$sql$]
        \n\tadditional_info:
        \n\t$additionalInfo$

 sqlLogFormatter.endExecuteBatchFormat
  :java:extdoc:`SqlStatement#executeBatch <nablarch.core.db.statement.SqlStatement.executeBatch()>`
  结束时使用的格式。

  格式中可指定的占位符
   :方法名: $methodName$
   :执行时间: $executeTime$
   :批处理件数: $batchCount$

  默认格式
   .. code-block:: bash

    $methodName$
        \n\texecute_time(ms) = [$executeTime$] batch_count = [$updateCount$]

记述示例
 .. code-block:: properties

  sqlLogFormatter.className=nablarch.core.db.statement.SqlLogFormatter
  sqlLogFormatter.startRetrieveFormat=$methodName$\n\tSQL:$sql$\n\tstart:$startPosition$ size:$size$\n\tadditional_info:\n\t$additionalInfo$
  sqlLogFormatter.endRetrieveFormat=$methodName$\n\texe:$executeTime$ms ret:$retrieveTime$ms count:$count$
  sqlLogFormatter.startExecuteFormat=$methodName$\n\tSQL:$sql$\n\tadditional_info:\n\t$additionalInfo$
  sqlLogFormatter.endExecuteFormat=$methodName$\n\texe:$executeTime$ms
  sqlLogFormatter.startExecuteQueryFormat=$methodName$\n\tSQL:$sql$\n\tadditional_info:\n\t$additionalInfo$
  sqlLogFormatter.endExecuteQueryFormat=$methodName$\n\texe:$executeTime$ms
  sqlLogFormatter.startExecuteUpdateFormat=$methodName$\n\tSQL:$sql$\n\tadditional_info:\n\t$additionalInfo$
  sqlLogFormatter.endExecuteUpdateFormat=$methodName$\n\texe:$executeTime$ms count:$updateCount$
  sqlLogFormatter.startExecuteBatchFormat=$methodName$\n\tSQL:$sql$\n\tadditional_info:\n\t$additionalInfo$
  sqlLogFormatter.endExecuteBatchFormat=$methodName$\n\texe:$executeTime$ms count:$updateCount$

.. _sql_log-json_setting:

作为JSON形式的结构化日志输出
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
通过 :ref:`log-json_log_setting` 设置可以以JSON格式输出日志，
但在 :java:extdoc:`SqlLogFormatter <nablarch.core.db.statement.SqlLogFormatter>` 中
SQL日志的各项作为字符串输出到message的值中。
要将SQL日志的各项也作为JSON值输出，
请使用 :java:extdoc:`SqlJsonLogFormatter <nablarch.core.db.statement.SqlJsonLogFormatter>` 。
设置在 :ref:`log-app_log_setting` 中说明的属性文件中进行。

记述规则
 :java:extdoc:`SqlJsonLogFormatter <nablarch.core.db.statement.SqlJsonLogFormatter>` 使用时
 指定的属性如下。
 
 sqlLogFormatter.className ``必须``
  以JSON格式输出日志时，
  指定 :java:extdoc:`SqlJsonLogFormatter <nablarch.core.db.statement.SqlJsonLogFormatter>` 。

 sqlLogFormatter.startRetrieveTargets
  :java:extdoc:`SqlPStatement#retrieve <nablarch.core.db.statement.SqlPStatement.retrieve()>`
  开始时的日志输出项目。以逗号分隔指定。

  可指定的输出项目
   :方法名: methodName
   :SQL语句: sql
   :获取开始位置: startPosition
   :获取最大件数: size
   :超时时间: queryTimeout
   :获取行数: fetchSize
   :附加信息: additionalInfo
 
  默认以所有输出项目为对象。

 sqlLogFormatter.endRetrieveTargets
  :java:extdoc:`SqlPStatement#retrieve <nablarch.core.db.statement.SqlPStatement.retrieve()>`
  结束时的日志输出项目。以逗号分隔指定。

  可指定的输出项目
   :方法名: methodName
   :执行时间: executeTime
   :数据获取时间: retrieveTime
   :检索件数: count

  默认以所有输出项目为对象。

 sqlLogFormatter.startExecuteTargets
  :java:extdoc:`SqlPStatement#execute <nablarch.core.db.statement.SqlPStatement.execute()>`
  开始时的日志输出项目。以逗号分隔指定。

  可指定的输出项目
   :方法名: methodName
   :SQL语句: sql
   :附加信息: additionalInfo

  默认以所有输出项目为对象。

 sqlLogFormatter.endExecuteTargets
  :java:extdoc:`SqlPStatement#execute <nablarch.core.db.statement.SqlPStatement.execute()>`
  结束时的日志输出项目。以逗号分隔指定。

  可指定的输出项目
   :方法名: methodName
   :执行时间: executeTime

  默认以所有输出项目为对象。

 sqlLogFormatter.startExecuteQueryTargets
  :java:extdoc:`SqlPStatement#executeQuery <nablarch.core.db.statement.SqlPStatement.executeQuery()>`
  开始时的日志输出项目。以逗号分隔指定。

  可指定的输出项目
   :方法名: methodName
   :SQL语句: sql
   :附加信息: additionalInfo

  默认以所有输出项目为对象。

 sqlLogFormatter.endExecuteQueryTargets
  :java:extdoc:`SqlPStatement#executeQuery <nablarch.core.db.statement.SqlPStatement.executeQuery()>`
  结束时的日志输出项目。以逗号分隔指定。

  可指定的输出项目
   :方法名: methodName
   :执行时间: executeTime

  默认以所有输出项目为对象。

 sqlLogFormatter.startExecuteUpdateTargets
  :java:extdoc:`SqlPStatement#executeUpdate <nablarch.core.db.statement.SqlPStatement.executeUpdate()>`
  开始时的日志输出项目。以逗号分隔指定。

  可指定的输出项目
   :方法名: methodName
   :SQL语句: sql
   :附加信息: additionalInfo

  默认以所有输出项目为对象。

 sqlLogFormatter.endExecuteUpdateTargets
  :java:extdoc:`SqlPStatement#executeUpdate <nablarch.core.db.statement.SqlPStatement.executeUpdate()>`
  结束时的日志输出项目。以逗号分隔指定。

  可指定的输出项目
   :方法名: methodName
   :执行时间: executeTime
   :更新件数: updateCount

  默认以所有输出项目为对象。

 sqlLogFormatter.startExecuteBatchTargets
  :java:extdoc:`SqlStatement#executeBatch <nablarch.core.db.statement.SqlStatement.executeBatch()>`
  开始时的日志输出项目。以逗号分隔指定。

  可指定的输出项目
   :方法名: methodName
   :SQL语句: sql
   :附加信息: additionalInfo

  默认以所有输出项目为对象。

 sqlLogFormatter.endExecuteBatchTargets
  :java:extdoc:`SqlStatement#executeBatch <nablarch.core.db.statement.SqlStatement.executeBatch()>`
  结束时的日志输出项目。以逗号分隔指定。

  可指定的输出项目
   :方法名: methodName
   :执行时间: executeTime
   :批处理件数: batchCount

  默认以所有输出项目为对象。

 sqlLogFormatter.structuredMessagePrefix
  为了识别格式化后的消息字符串已被格式化为JSON格式，而在消息开头添加的标记字符串。
  当消息开头的标记字符串与 :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` 中设置的标记字符串一致时， :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` 将消息作为JSON数据处理。
  默认为 ``"$JSON$"`` 。
  更改时，使用LogWriter的 ``structuredMessagePrefix`` 属性将相同的值也设置到 :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` （关于LogWriter的属性请参阅 :ref:`log-basic_setting` ）。

记述示例
 .. code-block:: properties

  sqlLogFormatter.className=nablarch.core.db.statement.SqlJsonLogFormatter
  sqlLogFormatter.structuredMessagePrefix=$JSON$
  sqlLogFormatter.startRetrieveTargets=methodName,sql,startPosition,size,additionalInfo
  sqlLogFormatter.endRetrieveTargets=methodName,executeTime,retrieveTime,count
  sqlLogFormatter.startExecuteTargets=methodName,sql,additionalInfo
  sqlLogFormatter.endExecuteTargets=methodName,executeTime
  sqlLogFormatter.startExecuteQueryTargets=methodName,sql,additionalInfo
  sqlLogFormatter.endExecuteQueryTargets=methodName,executeTime
  sqlLogFormatter.startExecuteUpdateTargets=methodName,sql,additionalInfo
  sqlLogFormatter.endExecuteUpdateTargets=methodName,executeTime,updateCount
  sqlLogFormatter.startExecuteBatchTargets=methodName,sql,additionalInfo
  sqlLogFormatter.endExecuteBatchTargets=methodName,executeTime,batchCount
