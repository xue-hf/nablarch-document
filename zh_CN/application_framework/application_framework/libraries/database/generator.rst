.. _generator:

代理键的生成
====================

.. contents:: 目录
  :depth: 3
  :local:

提供为数据库代理键（代理键）的值进行编号的功能。

此功能在 :ref:`universal_dao` 中进行代理键编号（简单的连续编号）时使用。

此外，虽然也可以在 :ref:`universal_dao` 以外使用，
但基于以下理由，建议在应用程序侧进行对应。

理由
  代理键的编号处理由 :ref:`universal_dao` 执行，因此应用程序侧无需直接使用编号功能。
  在除此以外的用途中进行值编号时，预计编号规则较复杂，或需要对编号的值进行编辑。
  此类情况下，无法使用进行简单连续编号的本功能，因此需要在应用程序侧进行设计、实现。
  （虽然本功能也可以实现，但由于需要设计及实现（配置），因此使用本功能没有优势）

  例如，在父键内进行连续编号的情况下，可以通过以下步骤进行值编号。

  1. 创建用于对每个父键进行连续编号的专用表。
  2. 应用程序在父键登记的时机向专用表登记记录。
  3. 在需要编号的时机，通过递增对应父键的已编号值，可以在父键内进行连续编号。

功能概述
-------------
可以使用序列(sequence)进行值编号
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
可以使用在数据库上创建的序列(sequence)对象，进行唯一值的编号。

此外，使用序列(sequence)获取下一个值的SQL语句，
使用数据库访问功能的方言(Dialect)构建。

关于方言(Dialect)功能，请参阅 :ref:`方言(Dialect) <database-dialect>` 。

可以使用表进行值编号
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
可以在表的记录单位管理当前值，进行唯一值的编号。

表的布局预想为以下内容。

================ ===================================================
编号识别名(PK)   用于识别编号目标的值

当前值           当前的值（进行编号后将获取此值加1后的值）
================ ===================================================

.. important::

  必要的记录请预先设置好。
  执行编号时，如果指定编号识别名(PK)对应的记录不存在，
  不会新增记录，而是异常结束（抛出异常）。


.. important::

  使用表进行编号，在处理大量数据的批处理等中往往会成为瓶颈。
  因此，强烈建议不要使用表进行编号，而是使用数据库侧的编号列或序列(sequence)进行编号。

  仅在数据库功能无法使用编号列及序列(sequence)对象的情况下，才使用表进行编号功能。

模块列表
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-idgenerator</artifactId>
  </dependency>
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-idgenerator-jdbc</artifactId>
  </dependency>

使用方法
--------------------------------------------

.. _generator_dao_setting:

为通用DAO配置编号
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
要在 :ref:`universal_dao` 中使用本功能，需要对 :java:extdoc:`BasicDaoContextFactory <nablarch.common.dao.BasicDaoContextFactory>` 进行配置。

此示例中同时配置了序列(sequence)编号和表编号，但不使用的编号配置可以省略。
由于不推荐使用表编号，因此在代理键编号中使用序列(sequence)编号时，只需配置 `sequenceIdGenerator` 即可。

如果不在序列(sequence)编号中使用而使用数据库侧的编号功能（自动编号列），则不需要编号配置本身。

.. code-block:: xml

  <!-- 表编号模块的配置 -->
  <component name="tableIdGenerator" class="nablarch.common.idgenerator.TableIdGenerator">
    <property name="tableName" value="GENERATOR" />
    <property name="idColumnName" value="ID" />
    <property name="noColumnName" value="NO" />
  </component>

  <component name="daoContextFactory" class="nablarch.common.dao.BasicDaoContextFactory">
    <!-- 序列(sequence)编号的配置 -->
    <property name="sequenceIdGenerator">
      <component class="nablarch.common.idgenerator.SequenceIdGenerator"/>
    </property>

    <!-- 表编号的配置 -->
    <property name="tableIdGenerator" ref="tableIdGenerator" />

    <!-- 省略与编号无关的配置 -->
  </component>

  <component name="initializer"
      class="nablarch.core.repository.initialization.BasicApplicationInitializer">
    <property name="initializeList">
      <list>
        <!-- TableIdGenerator需要初始化 -->
        <component-ref name="tableIdGenerator" />
      </list>
    </property>
  </component>

扩展示例
--------------------------------------------------
替换表编号或序列(sequence)编号
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
要将使用表或序列(sequence)的编号实现替换为新的实现时，
可以通过创建实现 :java:extdoc:`IdGenerator <nablarch.common.idgenerator.IdGenerator>` 的类来对应。

按照 `为通用DAO配置编号`_ 创建的类配置在组件配置文件中定义后即可使用。

.. |br| raw:: html

  <br />
