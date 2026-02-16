.. _webspheremq_adaptor:

IBM MQ适配器
==================================================

.. contents:: 目录
  :depth: 3
  :local:

提供用于在 :ref:`Nablarch的MOM消息功能 <mom_messaging>` 中使用 `IBM MQ(外部网站，英语) <https://www.ibm.com/docs/en/ibm-mq/9.3?topic=mq-about>`_ 的适配器。

IBM MQ的规格及构建步骤等请参阅IBM公司的官方网站及手册。

模块列表
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-wmq-adaptor</artifactId>
  </dependency>

.. important::

  测试中使用的是IBM MQ 9.3的库。
  要更改版本时，请在项目侧进行测试确认无问题。

使用本适配器的设置
--------------------------------------------------
本适配器通过以下步骤定义组件即可启用。

1. 在组件配置文件中添加 ``nablarch.integration.messaging.wmq.provider.WmqMessagingProvider`` 的定义。
2. 将 ``1`` 中设置的 ``WmqMessagingProvider`` 设置到 :ref:`messaging_context_handler` 。
3. ``1`` 中设置的 ``WmqMessagingProvider`` 需要初始化，因此需要设置到初始化对象的列表中。


以下显示设置示例。

.. code-block:: xml

  <!-- IBM MQ适配器用的提供程序实现 -->
  <component name="wmqMessagingProvider"
      class="nablarch.integration.messaging.wmq.provider.WmqMessagingProvider">
    <!-- 设置值请参阅Javadoc -->
  </component>

  <!--
  消息上下文管理处理程序

  将上述定义的WmqMessagingProvider设置到messagingProvider属性。
  -->
  <component class="nablarch.fw.messaging.handler.MessagingContextHandler">
    <property name="messagingProvider" ref="wmqMessagingProvider" />
  </component>

  <component name="initializer"
      class="nablarch.core.repository.initialization.BasicApplicationInitializer">
    <property name="initializeList">
      <list>
        <!-- WmqMessagingProvider需要初始化 -->
        <component-ref name="wmqMessagingProvider" />
      </list>
    </property>
  </component>

使用分布式事务
--------------------------------------------------
本适配器包含将IBM MQ作为事务管理器实现分布式事务的功能。

此功能用于在与外部系统进行消息收发时防止遗漏接收或重复接收。

使用分布式事务的步骤如下。

1. 定义支持分布式事务的数据源(实现 :java:extdoc:`javax.sql.XADataSource` 的类)。

2. 定义生成分布式事务对应数据库连接的工厂类。 |br|
   (定义 ``nablarch.integration.messaging.wmq.xa.WmqXADbConnectionFactoryForXADataSource`` 。)

3. 将 ``2`` 中定义的工厂类设置到 :ref:`database_connection_management_handler` 。

4. 定义生成分布式事务用事务对象的工厂类。 |br|
   (定义 ``nablarch.integration.messaging.wmq.xa.WmqXATransactionFactory`` 。)

5. 将 ``4`` 中定义的工厂类设置到 :ref:`transaction_management_handler` 。

以下显示设置示例。

.. code-block:: xml

  <!--
  XA用数据源的设置
  设置使用的数据库产品的JDBC实现中的XA用数据源。

  此示例为Oracle数据库的设置。
  -->
  <component name="xaDataSource" class="oracle.jdbc.xa.client.OracleXADataSource">
    <!-- 对属性的设置省略 -->
  </component>

  <!-- XA用数据库连接生成类的设置-->
  <component name="xaConnectionFactory"
      class="nablarch.integration.messaging.wmq.xa.WmqXADbConnectionFactoryForXADataSource">

    <!-- 向xaDataSource属性设置XA用数据源。-->
    <property name="xaDataSource" ref="xaDataSource" />

    <!-- 上述以外的属性省略 -->
  </component>

  <!-- 分布式事务用DB连接处理程序的设置 -->
  <component class="nablarch.common.handler.DbConnectionManagementHandler">
    <!-- DB连接工厂中，设置上述定义的XA用数据库连接生成类。 -->
    <property name="connectionFactory" ref="xaConnectionFactory" />

    <!-- 上述以外的属性省略 -->
  </component>

  <!-- XA用事务控制对象生成类的设置 -->
  <component name="xaTransactionFactory"
      class="nablarch.integration.messaging.wmq.xa.WmqXATransactionFactory" />

  <!-- 分布式事务用事务处理程序的设置 -->
  <component class="nablarch.common.handler.TransactionManagementHandler">
    <!-- 事务工厂中，设置上述定义的
    XA用事务控制对象生成类。
    -->
    <property name="transactionFactory" ref="xaTransactionFactory" />

    <!-- 上述以外的属性省略 -->
  </component>

.. important::

  使用分布式事务需要对IBM MQ进行XA资源管理器设置以及对数据库授予权限等。
  详细的设置方法和所需权限等请参阅使用产品的手册。

.. |br| raw:: html

  <br />
