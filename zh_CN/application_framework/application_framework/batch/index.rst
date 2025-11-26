.. _batch_application:

Batch应用篇
==================================================
本章节提供了使用Nablarch应用框架开发Batch（批处理）应用所需的信息。

Nablarch的Batch应用框架提供了一下两种批处理应用的框架。

.. toctree::
  :maxdepth: 1

  jsr352/index
  nablarch_batch/index

虽然用任何一个框架都可以构建Batch应用。
但是基于以下原因，推荐使用 :doc:`nablarch_batch/index` 构建Batch应用。

理由
  由于截至2020年，Jakarta Batch的相关资料较少，且难以调配相关领域的专家 [1]_ ，因此建议使用 :doc:nablarch_batch/index 来开发批处理应用程序。

.. tip::

  虽然直到Nablarch 5u15的说明文档我们都在推荐采用符合 Jakarta Batch 标准的批处理应用程序，但是鉴于直到2020年其普及情况较差且学习成本较高，因此方针已经被调整为推荐使用Nablarch Batch构建Batch应用。

.. tip::

  :ref:`jsr352_batch` と :ref:`nablarch_batch` 提供的功能上的区别可以参考 :ref:`batch-functional_comparison` 。


.. toctree::
  :maxdepth: 1
  :hidden:

  functional_comparison

.. [1] 此处指日本业内