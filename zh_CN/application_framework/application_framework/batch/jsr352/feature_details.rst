功能详情
========================================
.. contents:: 目录
  :depth: 3
  :local:

Batch应用的启动方法
--------------------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/run_batch_application

* :ref:`Jakarta Batch应用的启动方法 <jsr352_run_batch_application>`

系统仓库的初始化
--------------------------------------------------
* :ref:`Jakarta Batch应用中系统仓库的初始化 <jsr352_run_batch_init_repository>`

应用到Batch Job的监听器定义方法
--------------------------------------------------
* :ref:`监听器的定义方法 <jsr352-listener_definition>`

输入值的检查
--------------------------------------------------
* :ref:`输入值的检查 <validation>`

数据库访问
--------------------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/database_reader

* :ref:`数据库访问 <database_management>`
* :doc:`feature_details/database_reader`



文件输入输出
--------------------------------------------------
* :ref:`文件输入输出<data_converter>`

排他控制
--------------------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/pessimistic_lock

排他控制虽然提供以下2种方法，
但如 :ref:`推荐使用UniversalDao的理由 <exclusive_control-deprecated>` 中所述，
推荐使用 :ref:`universal_dao` 。

* :ref:`exclusive_control`
* :ref:`universal_dao`

  * :doc:`悲观锁<feature_details/pessimistic_lock>`

Job定义的xml创建方法
--------------------------------------------------
* `请参考Jakarta Batch Specification(外部网站，英文) <https://jakarta.ee/specifications/batch/>`_

MOM消息发送
----------------------------------------
* :ref:`同步响应消息发送<mom_system_messaging-sync_message_send>`

运维设计
----------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/operation_policy
  feature_details/progress_log
  feature_details/operator_notice_log

* :doc:`feature_details/operation_policy`
* :doc:`feature_details/progress_log`
* :doc:`feature_details/operator_notice_log`
