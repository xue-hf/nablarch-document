.. _`nablarch_Batch_getting_started`:

Getting Started
==========================================
通过通读本章，可以掌握 Nablarch Batch 应用方式的 Batch 开发思路。

.. tip::
 Example 是展示 Nablarch 功能使用方法的实现示例，不建议通过修改 Example 来开发正式应用。
 
 如需开发正式应用，请从 :ref:`blank_project` 开始。


前提条件
  本章以 :ref:`example_application` 为基础进行说明。
  请事先构建好 Example 应用的运行环境。

  .. tip::
    与Example应用相关的以下事项不会在本章节说明。
    请参考 :ref:`example_application` 。

    - Example应用的运行环境构建与执行
    - Example应用的设置
    - 使用的OSS插件相关

.. toctree::
  :maxdepth: 1

  nablarch_batch/index

.. tip::
 在 Nablarch Batch 应用中，由于 :ref:`每次启动型Batch<nablarch_batch-each_time_batch>` 与
 :ref:`驻留型Batch<nablarch_batch-resident_batch>` 的实现方式并无差异，
 因此未分别为两者提供独立的“Getting Started”。
 :ref:`每次启动型Batch<nablarch_batch-each_time_batch>` 与
 :ref:`驻留型Batch<nablarch_batch-resident_batch>` 的差异只在handler配置上。
