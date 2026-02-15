运维人员日志输出
==================================================
.. contents:: 目录
  :depth: 3
  :local:

运维人员日志的输出内容
--------------------------------------------
运维人员日志中，为了让运维人员能够根据日志进行处理，至少需要输出以下内容。

* 发生了什么
* 应该如何处理

如果未输出这些内容，运维人员可能无法判断对发生的事象应如何处理。

添加运维人员日志输出到专用日志文件的设置
----------------------------------------------------------------------
运维人员日志以日志类别名 ``operator`` 输出。
使用此类别名，可以将日志输出到运维人员专用的日志文件中。

以下展示使用 :ref:`log` 时的 ``log.properties`` 设置示例。
如果使用 :ref:`log_adaptor` ，请参考对应适配器的日志库手册等进行设置。

.. code-block:: properties

  # operation log file
  writer.operationLog.className=nablarch.core.log.basic.FileLogWriter
  writer.operationLog.filePath=./log/operation.log
  writer.operationLog.encoding=UTF-8
  writer.operationLog.formatter.className=nablarch.core.log.basic.BasicLogFormatter
  writer.operationLog.formatter.format=$date$ -$logLevel$- $message$

  # logger list
  availableLoggersNamesOrder=SQL,MON,OPERATOR,ROO

  # operation logger setting
  loggers.OPERATOR.nameRegex=operator
  loggers.OPERATOR.level=INFO
  loggers.OPERATOR.writerNames=operationLog

输出运维人员日志
--------------------------------------------------

以下展示输出运维人员日志的实现示例。

要点
  * 使用 :java:extdoc:`OperationLogger#write <nablarch.core.log.operation.OperationLogger.write(nablarch.core.log.basic.LogLevel,java.lang.String,java.lang.Throwable)>`
    输出日志。
  * 如果希望输出运维人员日志的同时使 Batch 处理异常结束，请抛出异常。

实现示例
  .. code-block:: java

    @Named
    @Dependent
    public class SampleBatchlet extends AbstractBatchlet {

        @Override
        public String process() throws Exception {

            try {
                // 省略
            } catch (FileNotFoundException e) {
                // 向运维人员通知输入文件不存在并抛出异常
                OperationLogger.write(
                        LogLevel.ERROR,
                        "文件不存在。请确认是否正确接收。",
                        e);
                throw e;
            }

            // 省略
        }
    }

输出示例
  .. code-block:: bash

    ERROR operator 文件不存在。请确认是否正确接收。
