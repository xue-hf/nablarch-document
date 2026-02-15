.. _`batch-functional_comparison`:

遵循Jakarta Batch的Batch应用与Nablarch Batch应用的功能比较
----------------------------------------------------------------------------------------------------
本章介绍以下功能的比较。

* :doc:`jsr352/index`
* :doc:`nablarch_batch/index`

.. list-table:: 功能比较（◎：Jakarta Batch规范中定义的　○：提供　△：部分提供　×：未提供　－：不适用）
  :header-rows: 1
  :class: something-special-class
  :widths: 30 35 35

  * - 功能
    - 遵循Jakarta Batch [#jsr]_
    - Nablarch Batch

  * - 启动时可设置任意参数
    - ◎
    - ○ |br| :ref:`前往说明书 <main-option_parameter>`

  * - 可防止同一Batch应用同时执行
    - ○ |br| :java:extdoc:`前往Javadoc <nablarch.fw.batch.ee.listener.job.DuplicateJobRunningCheckListener>`
    - ○ |br| :ref:`前往说明书 <duplicate_process_check_handler>`

  * - 可从外部安全停止执行中的Batch应用
    - ◎
    - ○ |br| :ref:`前往说明书 <process_stop_handler>`

  * - 可指定单次执行处理的最大件数
    - × |br| [#jsr_max]_
    - ○ |br| :ref:`前往说明书 <data_read_handler-max_count>`

  * - 可按指定件数单位进行提交
    - ◎
    - ○ |br| :ref:`前往说明书 <loop_handler-commit_interval>`

  * - 可从故障发生点重新执行
    - ◎
    - △ |br| [#resumable]_

  * - 可将业务处理在多线程中并行执行
    - ◎
    - ○ |br| :ref:`前往说明书 <multi_thread_execution_handler>`

  * - 可忽略特定异常继续处理 |br|
      (可在回滚后继续处理)
    - ◎
    - × |br| [#skip_exception]_

  * - 特定异常发生时可重试处理
    - ◎
    - △ |br| [#retry_exception]_

  * - 可根据Batch应用的结果 |br| 切换下次执行的处理
    - ◎
    - × |br| [#branch_batch]_

  * - 可按一定间隔监视输入数据源 |br| 并执行Batch
    - × [#resident_batch]_
    - ○ |br| :ref:`前往说明书 <nablarch_batch-resident_batch>`


.. [#jsr]
  ◎的部分遵循Jakarta Batch规定的规范。
  详情请参考 `Jakarta Batch(外部网站，英文) <https://jakarta.ee/specifications/batch/>`_ 的Specification。

.. [#jsr_max]
  可通过在 :java:extdoc:`ItemReader <jakarta.batch.api.chunk.ItemReader>` 的实现类中设置可指定单次执行读取最大件数的属性等方式来应对。

.. [#resumable]
  使用 :java:extdoc:`ResumeDataReader (带恢复功能的读取)<nablarch.fw.reader.ResumeDataReader>` 可实现从故障发生点重新执行。
  但是，此功能仅在以文件为输入时使用。以其他数据为输入时，需要在应用侧进行设计和实现。

.. [#skip_exception]
  如需忽略特定异常继续处理，可通过添加handler来应对。

.. [#retry_exception]
  :ref:`retry_handler` 可在发生可重试异常时进行重试，但无法像Jakarta Batch那样对发生异常的数据进行简单重试。
  此外，:ref:`retry_handler` 无法灵活指定重试对象的异常。

  如果 :ref:`retry_handler` 无法满足需求(需要对发生异常的数据进行简单重试或灵活指定异常)时，可通过添加handler来应对。

.. [#branch_batch]
  可通过Job Scheduler等方式应对。例如，需要根据结束代码切换下次执行的Job等。

.. [#resident_batch]
  遵循Jakarta Batch的Batch应用无法实现按一定间隔监视输入数据源的Batch处理。
  因此，当需要此类Batch应用时，请使用 :ref:`Nablarch Batch应用的常驻Batch  <nablarch_batch-resident_batch>` 来实现。

.. |br| raw:: html

  <br />
