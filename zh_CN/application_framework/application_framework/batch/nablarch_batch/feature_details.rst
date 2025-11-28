功能详细
========================================
.. contents:: 目录
  :depth: 3
  :local:

Batch 应用的启动方法
--------------------------------------------------
* :ref:`Nablarch Batch应用的启动方法<main-run_application>`

System Repository(系统仓库)初始化
--------------------------------------------------
System Repository是通过在应用启动时加载指定的System Repository配置文件进行的。
相信信息可以参考 :ref:`Nablarch Batch应用的启动方法<main-run_application>` 。

输入值校验
--------------------------------------------------
* :ref:`输入值校验 <validation>`

数据库访问
--------------------------------------------------
* :ref:`数据库访问 <database_management>`
* 默认提供的数据读取器

  * :java:extdoc:`DatabaseRecordReader (数据库读取) <nablarch.fw.reader.DatabaseRecordReader>`

文件输入输出
--------------------------------------------------
* :ref:`文件输入输出<data_converter>`

* 默认提供的数据读取器

  * :java:extdoc:`FileDataReader (文件读取)<nablarch.fw.reader.FileDataReader>`
  * :java:extdoc:`ValidatableFileDataReader (带校验功能的文件读取)<nablarch.fw.reader.ValidatableFileDataReader>`
  * :java:extdoc:`ResumeDataReader (带断点续读的读取)<nablarch.fw.reader.ResumeDataReader>`

数据库锁控制
--------------------------------------------------
.. toctree::
    :maxdepth: 1
    :hidden:

    feature_details/nablarch_batch_pessimistic_lock

关于数据库锁控制，Nablarch提供了以下两种方式，
根据 :ref:`推荐UniversalDao的理由 <exclusive_control-deprecated>` ，
推荐使用 :ref:`universal_dao` 。

* :ref:`exclusive_control`
* :ref:`universal_dao`

  * :ref:`悲观锁<nablarch_batch_pessimistic_lock>`

Batch处理的执行控制
--------------------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/nablarch_batch_error_process
  feature_details/nablarch_batch_retention_state

* :ref:`Batch处理的进程终止代码<status_code_convert_handler-rules>`
* :ref:`Batch处理的异常处理<nablarch_batch_error_process>`
* :ref:`多线程的Batch处理<multi_thread_execution_handler>`
* :ref:`Batch处理的commit间隔控制 <loop_handler-commit_interval>`
* :ref:`单次Batch处理的数据量限制 <data_read_handler-max_count>`
  |br| (例如，需将处理大量数据的批处理任务分摊到数天内完成的情况。)

发送面向消息的中间件消息
----------------------------------------
* :ref:`发送同步消息<mom_system_messaging-sync_message_send>`
* :ref:`发送异步消息<mom_system_messaging-async_message_send>`

在Batch应用的运行过程中保存状态
----------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/nablarch_batch_retention_state

* :ref:`nablarch_batch_retention_state`

驻留型Batch的多Process化
----------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/nablarch_batch_multiple_process
  
* :ref:`nablarch_batch_multiple_process`

.. |br| raw:: html

  <br />
