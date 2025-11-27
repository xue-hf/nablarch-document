.. _nablarch_batch_error_process:

Nablarch Batch应用的异常处理
============================================================
.. contents:: 目录
  :depth: 3
  :local:

.. _nablarch_batch_error_process-rerun:

使Batch处理可重试
--------------------------------------------------
在 Nablarch Batch 应用中，
除文件输入外，未提供使Batch能够重新运行的功能。

因此，需要在应用的设计与实现上，
为待处理记录设置状态，并在处理成功或者失败的时候更新状态。
关于处理成功或者失败时如何变更状态，请参考 :ref:`loop_handler-callback`

关于输入文件可以使用
:java:extdoc:`ResumeDataReader (带断点续读的读取)<nablarch.fw.reader.ResumeDataReader>`
使得Batch可以从上次故障发生的断点开始继续执行。

.. _nablarch_batch_error_process-continue:

在发生错误时继续进行Batch处理
--------------------------------------------------
在发生错误时继续进行Batch处理的功能只在 :ref:`驻留型Batch<nablarch_batch-resident_batch>` 中支持。
:ref:`每次启动型Batch<nablarch_batch-each_time_batch>` 不支持。

在 :ref:`驻留型Batch<nablarch_batch-resident_batch>` 中，若抛出
:java:extdoc:`TransactionAbnormalEnd<nablarch.fw.results.TransactionAbnormalEnd>`
则处理将由 :ref:`retry_handler` 继续执行。
但是为了确保Batch能够重新运行，需要满足 :ref:`nablarch_batch_error_process-rerun` 中记载的条件
（如记录状态管理、可重入设计等）。

.. tip::
 :ref:`每次启动型Batch<nablarch_batch-each_time_batch>` 送出了
 :java:extdoc:`TransactionAbnormalEnd<nablarch.fw.results.TransactionAbnormalEnd>`
 时，Batch会异常结束。

.. _nablarch_batch_error_process-abnormal_end:

使Batch处理异常终止
--------------------------------------------------
当应用中发生错误时，
有时希望不继续处理，而是直接使Batch异常终止。

在 Nablarch Batch 应用中，通过抛出
:java:extdoc:`ProcessAbnormalEnd<nablarch.fw.launcher.ProcessAbnormalEnd>`
，即可实现批处理的异常终止。
一旦抛出 :java:extdoc:`ProcessAbnormalEnd<nablarch.fw.launcher.ProcessAbnormalEnd>`
，进程终止代码将采用该类中指定的值。

