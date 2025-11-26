.. _`nablarch_Batch_getting_started`:

Getting Started
==========================================
本章を通読することで、Nablarch Batch应用方式のバッチの開発イメージを掴むことができる。

.. tip::
 ExampleはNablarchの機能の使用方法を示した実装例であり、Exampleを改修して本格的なアプリケーションを作成することは想定していない。
 
 本格的なアプリケーションを作成する場合は :ref:`blank_project` から作成すること。


前提条件
  本章は :ref:`example_application` をベースに解説する。
  Exampleアプリケーションの動作環境を事前に構築しておくこと。

  .. tip::
    Exampleアプリケーションに関する以下の事項は、本章节解説しない。
    以下の事項については、 :ref:`example_application` を参照すること。

    - Exampleアプリケーションの環境構築および実行
    - Exampleアプリケーションの設定
    - 使用しているOSSプラグインについて

.. toctree::
  :maxdepth: 1

  nablarch_batch/index

.. tip::
 Nablarch Batch应用では、 :ref:`每次启动型Batch<nablarch_batch-each_time_batch>` と
 :ref:`驻留型Batch<nablarch_batch-resident_batch>` でアプリケーションの実装方法に違いがないため、
 別々にGetting Startedを用意していない。
 :ref:`每次启动型Batch<nablarch_batch-each_time_batch>` と
 :ref:`驻留型Batch<nablarch_batch-resident_batch>` で異なるのは、ハンドラ構成のみである。
