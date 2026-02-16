架构概述
==============================

.. contents:: 目录
  :depth: 3
  :local:

Nablarch Batch应用程序提供了构建批处理的功能，
用于对存储在数据库或文件中的数据记录逐条重复执行处理。

Nablarch Batch应用程序分为以下两种。

.. _nablarch_batch-each_time_batch:

按需启动批处理
 每日或每月等定期启动进程执行批处理。

.. _nablarch_batch-resident_batch:

常驻Batch
 启动进程后，以固定间隔执行批处理。
 例如，用于定期批量处理在线处理中创建的请求数据。

.. important::
 常驻Batch即使在多线程执行时，由于其他线程会等待执行较慢的线程结束，
 可能会导致请求数据的获取延迟。

 因此，在新开发项目中，建议使用不会出现上述问题的 :ref:`db_messaging` ，而非常驻Batch。

 此外，在现有项目中，虽然可以继续使用常驻Batch，
 但如果可能发生上述问题（或已发生），请考虑迁移到 :ref:`db_messaging` 。

.. _nablarch_batch-structure:

Nablarch Batch应用程序的构成
------------------------------------------------------
Nablarch Batch应用程序作为从java命令直接启动的独立应用程序执行。
以下展示Nablarch Batch应用程序的构成。

.. image:: images/application_structure.png

:ref:`main` (Main)
 Nablarch Batch应用程序的入口主类。
 从java命令直接启动，执行系统仓库和日志的初始化处理，
 并执行handler队列。

.. _nablarch_batch-resolve_action:

通过请求路径指定Action和请求ID
------------------------------------------------------
Nablarch Batch应用程序通过命令行参数(-requestPath)
指定要执行的Action和请求ID。

.. code-block:: properties

  # 格式
  -requestPath=Action的类名/请求ID

  # 指定示例
  -requestPath=com.sample.SampleBatchAction/BATCH0001

请求ID用作各批处理进程的标识符。
当启动多个执行相同业务Action类的进程时，此请求ID将成为标识符。

.. _nablarch_batch-process_flow:

Nablarch Batch应用程序的处理流程
------------------------------------------------------
Nablarch Batch应用程序从读取输入数据到返回处理结果的流程如下所示。

.. image:: images/batch-flow.png
  :scale: 80

1. :ref:`通用启动启动器(Main) <main>` 执行handler队列(handler queue)。
2. :java:extdoc:`DataReader<nablarch.fw.DataReader>` 读取输入数据，
   逐条提供数据记录。
3. 在handler队列中设置的
   :java:extdoc:`DispatchHandler <nablarch.fw.handler.DispatchHandler>` 
   根据命令行参数(-requestPath)指定的请求路径确定应处理的Action类(action class)，
   并将其添加到handler队列的末尾。
4. Action类(action class)使用Form类(form class)和Entity类(entity class)
   逐条执行数据记录的业务逻辑(business logic)。
5. Action类(action class)返回表示处理结果的 :java:extdoc:`Result <nablarch.fw.Result>` 。
6. 重复执行2～5，直到没有待处理的数据。
7. 在handler队列中设置的
   :java:extdoc:`StatusCodeConvertHandler <nablarch.fw.handler.StatusCodeConvertHandler>` 
   将处理结果的状态码转换为进程退出码，
   作为批处理应用程序的处理结果返回进程退出码。

.. _nablarch_batch-handler:

Nablarch Batch应用程序中使用的handler
------------------------------------------------------
Nablarch标准提供了构建批处理应用程序所需的多个handler。
请根据项目需求构建handler队列。（根据需求，可能需要创建项目自定义handler）

各handler的详细信息请参考链接。

执行请求和响应转换的handler
  * :ref:`status_code_convert_handler`
  * :ref:`data_read_handler`

执行批处理运行控制的handler
  * :ref:`duplicate_process_check_handler`
  * :ref:`request_path_java_package_mapping`
  * :ref:`multi_thread_execution_handler`
  * :ref:`loop_handler`
  * :ref:`dbless_loop_handler`
  * :ref:`retry_handler`
  * :ref:`process_resident_handler`
  * :ref:`process_stop_handler`

与数据库相关的handler
  * :ref:`database_connection_management_handler`
  * :ref:`transaction_management_handler`

与错误处理相关的handler
  * :ref:`global_error_handler`

其他
  * :ref:`thread_context_handler`
  * :ref:`thread_context_clear_handler`
  * :ref:`ServiceAvailabilityCheckHandler`
  * :ref:`file_record_writer_dispose_handler`

按需启动批处理的最小handler构成
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
构建按需启动批处理时所需的最小handler队列如下所示。
以此为基础，根据项目需求添加Nablarch标准handler或项目创建的自定义handler。

连接数据库时，构成如下。

.. list-table:: 按需启动批处理（有DB连接）的最小handler构成
   :header-rows: 1
   :class: white-space-normal
   :widths: 4,22,12,22,22,22

   * - No.
     - handler
     - 线程
     - 去程处理
     - 返程处理
     - 异常处理

   * - 1
     - :ref:`status_code_convert_handler`
     - 主线程
     -
     - 将状态码转换为进程退出码。
     -

   * - 2
     - :ref:`global_error_handler`
     - 主线程
     -
     -
     - 出现运行时异常或错误时，输出日志。

   * - 3
     - :ref:`database_connection_management_handler`
       (用于初始化/结束处理)
     - 主线程
     - 获取DB连接。
     - 释放DB连接。
     -

   * - 4
     - :ref:`transaction_management_handler`
       (用于初始化/结束处理)
     - 主线程
     - 开始事务。
     - 提交事务。
     - 回滚事务。

   * - 5
     - :ref:`request_path_java_package_mapping`
     - 主线程
     - 根据命令行参数决定调用的Action。
     -
     -

   * - 6
     - :ref:`multi_thread_execution_handler`
     - 主线程
     - 创建子线程，并行执行后续handler的处理。
     - 等待所有线程正常结束。
     - 等待处理中的线程完成后重新抛出起因异常。

   * - 7
     - :ref:`database_connection_management_handler`
       (用于业务处理)
     - 子线程
     - 获取DB连接。
     - 释放DB连接。
     -

   * - 8
     - :ref:`loop_handler`
     - 子线程
     - 开始业务事务。
     - 按提交间隔提交业务事务。
       此外，如果DataReader上仍有待处理数据，则继续循环。
     - 回滚业务事务。

   * - 9
     - :ref:`data_read_handler`
     - 子线程
     - 使用DataReader读取1条记录，作为后续handler的参数传递。
       同时分配 :ref:`执行时ID<log-execution_id>` 。
     -
     - 输出读取的记录到日志后，重新抛出原异常。

不连接DB时，由于不需要DB连接相关handler，且循环控制handler中不需要事务控制，因此构成如下。

.. list-table:: 按需启动批处理（无DB连接）的最小handler构成
   :header-rows: 1
   :class: white-space-normal
   :widths: 4,22,12,22,22,22

   * - No.
     - handler
     - 线程
     - 去程处理
     - 返程处理
     - 异常处理

   * - 1
     - :ref:`status_code_convert_handler`
     - 主线程
     -
     - 将状态码转换为进程退出码。
     -

   * - 2
     - :ref:`global_error_handler`
     - 主线程
     -
     -
     - 出现运行时异常或错误时，输出日志。

   * - 3
     - :ref:`request_path_java_package_mapping`
     - 主线程
     - 根据命令行参数决定调用的Action。
     -
     -

   * - 4
     - :ref:`multi_thread_execution_handler`
     - 主线程
     - 创建子线程，并行执行后续handler的处理。
     - 等待所有线程正常结束。
     - 等待处理中的线程完成后重新抛出起因异常。

   * - 5
     - :ref:`dbless_loop_handler`
     - 子线程
     -
     - 如果DataReader上仍有待处理数据，则继续循环。
     -

   * - 6
     - :ref:`data_read_handler`
     - 子线程
     - 使用DataReader读取1条记录，作为后续handler的参数传递。
       同时分配 :ref:`执行时ID<log-execution_id>` 。
     -
     - 输出读取的记录到日志后，重新抛出原异常。

常驻Batch的最小handler构成
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
构建常驻Batch时所需的最小handler队列如下所示。
以此为基础，根据项目需求添加Nablarch标准handler或项目创建的自定义handler。

常驻Batch的最小handler构成与按需启动批处理相同，只是在主线程侧添加了以下handler。

* :ref:`thread_context_handler` ( :ref:`process_stop_handler` 所需)
* :ref:`thread_context_clear_handler` 
* :ref:`retry_handler`
* :ref:`process_resident_handler`
* :ref:`process_stop_handler`

.. list-table:: 常驻Batch的最小handler构成
   :header-rows: 1
   :class: white-space-normal
   :widths: 4,22,12,22,22,22

   * - No.
     - handler
     - 线程
     - 去程处理
     - 返程处理
     - 异常处理

   * - 1
     - :ref:`status_code_convert_handler`
     - 主线程
     -
     - 将状态码转换为进程退出码。
     -
     
   * - 2
     - :ref:`thread_context_clear_handler`
     - 主线程
     -
     - 删除 :ref:`thread_context_handler` 在线程本地设置的所有值。
     -

   * - 3
     - :ref:`global_error_handler`
     - 主线程
     -
     -
     - 出现运行时异常或错误时，输出日志。

   * - 4
     - :ref:`thread_context_handler`
     - 主线程
     - 从命令行参数初始化请求ID、用户ID等线程上下文变量。
     -
     -

   * - 5
     - :ref:`retry_handler`
     - 主线程
     -
     -
     - 捕获可重试的运行时异常，且未达到重试上限时重新执行后续handler。

   * - 6
     - :ref:`process_resident_handler`
     - 主线程
     - 按数据监控间隔重复执行后续handler。
     - 继续循环。
     - 输出日志，如果抛出运行时异常则包装为可重试异常后抛出。
       如果抛出错误则直接重新抛出。

   * - 7
     - :ref:`process_stop_handler`
     - 主线程
     - 如果请求表上的处理停止标志为开启，则不执行后续handler的处理，抛出进程停止异常(
       :java:extdoc:`ProcessStop <nablarch.fw.handler.ProcessStopHandler.ProcessStop>`
       )。
     -
     -

   * - 8
     - :ref:`database_connection_management_handler`
       (用于初始化/结束处理)
     - 主线程
     - 获取DB连接。
     - 释放DB连接。
     -

   * - 9
     - :ref:`transaction_management_handler`
       (用于初始化/结束处理)
     - 主线程
     - 开始事务。
     - 提交事务。
     - 回滚事务。

   * - 10
     - :ref:`request_path_java_package_mapping`
     - 主线程
     - 根据命令行参数决定调用的Action。
     -
     -

   * - 11
     - :ref:`multi_thread_execution_handler`
     - 主线程
     - 创建子线程，并行执行后续handler的处理。
     - 等待所有线程正常结束。
     - 等待处理中的线程完成后重新抛出起因异常。

   * - 12
     - :ref:`database_connection_management_handler`
       (用于业务处理)
     - 子线程
     - 获取DB连接。
     - 释放DB连接。
     -

   * - 13
     - :ref:`loop_handler`
     - 子线程
     - 开始业务事务。
     - 按提交间隔提交业务事务。
       此外，如果DataReader上仍有待处理数据，则继续循环。
     - 回滚业务事务。

   * - 14
     - :ref:`data_read_handler`
     - 子线程
     - 使用DataReader读取1条记录，作为后续handler的参数传递。
       同时分配 :ref:`执行时ID<log-execution_id>` 。
     -
     - 输出读取的记录到日志后，重新抛出原异常。

.. _nablarch_batch-data_reader:

Nablarch Batch应用程序中使用的DataReader
------------------------------------------------------
Nablarch标准提供了构建批处理应用程序所需的多个DataReader。
各DataReader的详细信息请参考链接。

* :java:extdoc:`DatabaseRecordReader (数据库读取) <nablarch.fw.reader.DatabaseRecordReader>`
* :java:extdoc:`FileDataReader (文件读取)<nablarch.fw.reader.FileDataReader>`
* :java:extdoc:`ValidatableFileDataReader (带验证功能的文件读取)<nablarch.fw.reader.ValidatableFileDataReader>`
* :java:extdoc:`ResumeDataReader (带恢复功能的读取)<nablarch.fw.reader.ResumeDataReader>`

.. tip::
 如果上述DataReader无法满足项目需求，
 请在项目中创建实现 :java:extdoc:`DataReader <nablarch.fw.DataReader>` 接口的类来应对。

.. important::
 标准提供的 :java:extdoc:`FileDataReader (文件读取)<nablarch.fw.reader.FileDataReader>` 、 :java:extdoc:`ValidatableFileDataReader (带验证功能的文件读取)<nablarch.fw.reader.ValidatableFileDataReader>` 使用 :ref:`data_format` 进行数据访问。如果使用 :ref:`data_bind` 进行数据访问，请勿使用这些DataReader。

.. _nablarch_batch-action:

Nablarch Batch应用程序中使用的Action
---------------------------------------------------------------------------------
Nablarch标准提供了构建批处理应用程序所需的多个Action类。
各Action类的详细信息请参考链接。

* :java:extdoc:`BatchAction (通用批处理Action模板类)<nablarch.fw.action.BatchAction>`
* :java:extdoc:`FileBatchAction (文件输入批处理Action模板类)<nablarch.fw.action.FileBatchAction>`
* :java:extdoc:`NoInputDataBatchAction (不使用输入数据的批处理Action模板类)<nablarch.fw.action.NoInputDataBatchAction>`
* :java:extdoc:`AsyncMessageSendAction (无需响应消息发送用Action类)<nablarch.fw.messaging.action.AsyncMessageSendAction>`

.. important::
 标准提供的 :java:extdoc:`FileBatchAction (文件输入批处理Action模板类)<nablarch.fw.action.FileBatchAction>` 使用 :ref:`data_format` 进行数据访问。如果使用 :ref:`data_bind` 进行数据访问，请使用其他Action类。
