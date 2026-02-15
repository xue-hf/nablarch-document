.. _data_read_handler:

数据读取handler
========================================
.. contents:: 目录
  :depth: 3
  :local:

使用 :ref:`DataReader <nablarch_batch-data_reader>` 进行输入数据顺序读取的handler。

本handler使用执行上下文上的 :ref:`DataReader <nablarch_batch-data_reader>` ，逐条读取业务处理的输入数据，
并将其作为参数委托给后续handler处理。
当到达 :ref:`DataReader <nablarch_batch-data_reader>` 的末尾时，不执行后续handler，而是返回表示数据已到达末尾的 :java:extdoc:`NoMoreRecord <nablarch.fw.DataReader.NoMoreRecord>` 。

本handler执行以下处理。

* 使用DataReader读取输入数据
* :ref:`执行时ID <log-execution_id>` 的编号

处理流程如下。

.. image:: ../images/DataReadHandler/flow.png

handler类名
--------------------------------------------------
* :java:extdoc:`nablarch.fw.handler.DataReadHandler`

模块列表
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-standalone</artifactId>
  </dependency>

约束
------------------------------
需要在本handler之前的handler中，向 :java:extdoc:`ExecutionContext <nablarch.fw.ExecutionContext>` 设置 :java:extdoc:`DataReader <nablarch.fw.DataReader>` 。
如果在本handler被调用时 :java:extdoc:`DataReader <nablarch.fw.DataReader>` 未设置，则本handler将作为无处理对象数据而结束处理(返回 :java:extdoc:`NoMoreRecord <nablarch.fw.DataReader.NoMoreRecord>` )。

.. _data_read_handler-max_count:

最大处理件数的设置
--------------------------------------------------
本handler可以设置最大处理件数。处理完最大处理件数的数据后，本handler将返回表示无处理对象记录的 :java:extdoc:`NoMoreRecord <nablarch.fw.DataReader.NoMoreRecord>` 。

此设置值用于将处理大量数据的批处理分批在数日内处理等情况。
使用此设置值，可以将处理最多100万件的批处理，每日仅处理最多10万件，在10天内完成全部处理。

以下显示设置示例。

.. code-block:: xml

  <component class="nablarch.fw.handler.DataReadHandler">
    <!-- 处理件数最多1万条记录 -->
    <property name="maxCount" value="10000" />
  </component>


