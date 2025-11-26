.. _`batch-functional_comparison`:

Jakarta Batch 与 Nablarch Batch 应用程序的功能对比
----------------------------------------------------------------------------------------------------
本章节展示了以下的功能对比。

* :doc:`jsr352/index`
* :doc:`nablarch_batch/index`

.. list-table:: 功能对比（◎：根据 Jakarta Batch 规范定义　○：支出　△：部分支持　×：不支持　－：除外）
  :header-rows: 1
  :class: something-special-class
  :widths: 30 35 35

  * - 功能
    - Jakarta Batchに準拠 [#jsr]_
    - Nablarchバッチ

  * - 启动时设置任意参数
    - ◎
    - ○ |br| :ref:`前往文档 <main-option_parameter>`

  * - 防止同一Batch应用重复启动
    - ○ |br| :java:extdoc:`Javadocへ <nablarch.fw.batch.ee.listener.job.DuplicateJobRunningCheckListener>`
    - ○ |br| :ref:`前往文档 <duplicate_process_check_handler>`

  * - 从外部安全地停止正在运行的批处理应用程序。
    - ◎
    - ○ |br| :ref:`前往文档 <process_stop_handler>`

  * - 指定单次执行中处理的最大记录数。
    - × |br| [#jsr_max]_
    - ○ |br| :ref:`前往文档 <data_read_handler-max_count>`

  * - 以指定记录数为单位进行commit
    - ◎
    - ○ |br| :ref:`前往文档 <loop_handler-commit_interval>`

  * - 故障恢复
    - ◎
    - △ |br| [#resumable]_

  * - 多线程处理业务逻辑
    - ◎
    - ○ |br| :ref:`前往文档 <multi_thread_execution_handler>`

  * - 忽略指定异常继续执行处理 |br|
      (回滚后可继续处理)
    - ◎
    - × |br| [#skip_exception]_

  * - 发生特定异常时重试处理
    - ◎
    - △ |br| [#retry_exception]_

  * - 根据Batch应用程序的执行结果 |br| 可切换下一执行的处理流程
    - ◎
    - × |br| [#branch_batch]_

  * - 定期监控输入数据源 |br| 并执行Batch处理
    - × [#resident_batch]_
    - ○ |br| :ref:`前往文档 <nablarch_batch-resident_batch>`


.. [#jsr]
  ◎ 处遵循 Jakarta Batch 所规定的规范。
  详细内容请参阅 `Jakarta Batch(外部サイト、英語) <https://jakarta.ee/specifications/batch/>`_ 的规范文档。

.. [#jsr_max]
  可通过为 :java:extdoc:`ItemReader <jakarta.batch.api.chunk.ItemReader>` 的实现类添加一个用于指定单次执行时最大读取记录数的属性等方式进行对应。

.. [#resumable]
  通过使用 :java:extdoc:`ResumeDataReader (支持断点续传的读取器)<nablarch.fw.reader.ResumeDataReader>` 可实现从故障发生点重新执行。
  但该功能仅适用于以文件作为输入源的情况；若输入数据非文件形式，则需由应用程序侧自行设计与实现相应功能。

.. [#skip_exception]
  若需忽略特定异常并继续处理，应添加相应的handler进行对应。

.. [#retry_exception]
  通过 :ref:`retry_handler` 可对可重试异常执行重试，但无法像 Jakarta Batch 那样对发生异常的单条数据进行简单重试。
  此外，:ref:`retry_handler` 无法灵活指定需重试的异常类型。

  若 :ref:`retry_handler` 无法满足需求（例如需要对发生异常的数据进行简单重试，或需灵活指定异常类型），则应通过自定义处理器进行应对。

.. [#branch_batch]
  通过作业调度器等进行应对。例如，需根据退出代码切换下一个执行的作业等。

.. [#resident_batch]
  Jakarta Batch 的Batch应用无法实现定期监控输入数据源的Batch功能。
  因此，当需要此类Batch应用时，应使用 :ref:`Nablarch Batch应用的常驻Batch <nablarch_batch-resident_batch>` 来实现。

.. |br| raw:: html

  <br />

