.. _transaction:

事务管理
============================
.. contents:: 目录
  :depth: 3
  :local:

提供对需要事务控制的资源（数据库、消息队列等）进行事务管理的功能。

功能概述
--------------------------
可以对各种资源进行事务控制
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
可以对数据库、消息队列等需要事务控制的资源进行事务管理。

关于数据库事务控制的详细内容，请参考以下文档：

* :ref:`transaction-database`
* :ref:`transaction-timeout`

当出现针对新资源的事务控制需求时，通过实现本功能定义的接口可以轻松实现。
详细内容请参考 :ref:`transaction_addResource` 。

模块列表
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-transaction</artifactId>
  </dependency>

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-jdbc</artifactId>
  </dependency>

使用方法
--------------------------------------------------

.. _transaction-database:

数据库事务控制
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
通过在组件配置文件中添加使用JDBC的事务控制，可以实现数据库事务控制。
前提是已经进行了数据库连接设置。

数据库连接方法的详细内容请参考 :ref:`database-connect` 。

使用以SQL为单位的细粒度事务时，请参考 :ref:`database-new_transaction` 进行设置和实现。

组件定义示例
  在组件配置文件中定义生成JDBC事务类的工厂类( :java:extdoc:`JdbcTransactionFactory <nablarch.core.db.transaction.JdbcTransactionFactory>` )。

  .. code-block:: xml

    <!-- 将JdbcTransactionFactory配置为组件 -->
    <component class="nablarch.core.db.transaction.JdbcTransactionFactory">

      <!-- 隔离级别 -->
      <property name="isolationLevel" value="READ_COMMITTED" />

      <!-- 事务超时秒数 -->
      <property name="transactionTimeoutSec" value="15" />

    </component>

.. tip::

  基本上不会直接使用上述配置的类。
  需要事务控制时，请使用 :ref:`transaction_management_handler` 。

.. _transaction-timeout:

数据库事务超时应用
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
通过对 :java:extdoc:`JdbcTransactionFactory <nablarch.core.db.transaction.JdbcTransactionFactory>` 设置事务超时秒数，事务超时功能将生效。
如果设置的事务超时秒数为0或以下，则事务超时功能将被禁用。

.. tip::

  对于批处理应用程序等一次性处理大量数据的功能，不要使用事务超时功能，
  而应通过作业调度器的终止延迟监控等方式处理处理延迟。

  这是因为在批处理应用程序中，只要整体处理时间在预期范围内即可，个别事务出现延迟也没有问题。
  例如，即使特定事务因数据库资源不足而耗时1分钟，只要整体处理在预期时间内完成，就会被认为是可接受的。


事务超时检查开始时机
  事务开始时(调用 :java:extdoc:`Transaction#begin() <nablarch.core.transaction.Transaction.begin()>` )开始检查。

  使用多个事务时（例如，在事务内执行其他事务时），
  对每个事务进行超时检查。

事务超时检查时机
  是否超过事务超时秒数在以下时机进行检查：

  SQL执行前
    如果在SQL执行前已超过事务超时秒数，则抛出 :java:extdoc:`TransactionTimeoutException <nablarch.core.transaction.TransactionTimeoutException>` 。

    在SQL执行前进行检查是因为，如果已经超过事务超时秒数，
    访问数据库将造成不必要的资源消耗。

  SQL执行后
    如果在SQL执行后已超过事务超时秒数，则抛出 :java:extdoc:`TransactionTimeoutException <nablarch.core.transaction.TransactionTimeoutException>` 。

    即使在SQL正常执行完毕的情况下也会进行检查，是因为在SQL执行中或结果集转换期间可能会超过事务超时秒数。

  查询超时异常发生时
    当发生表示查询超时的异常时，如果已超过事务超时秒数，则抛出 :java:extdoc:`TransactionTimeoutException <nablarch.core.transaction.TransactionTimeoutException>` 。
    是否属于查询超时异常，使用数据库功能的 :ref:`方言 <database-dialect>` 进行判断。

    执行处理时间较长的SQL语句（单纯的重SQL或等待锁释放的SQL）时，控制权可能无法从数据库返回。
    因此，将事务超时的剩余秒数设置到 `java.sql.Statement#setQueryTimeout` 中，
    当事务超时秒数超时时强制取消执行。

    此外，如果在SQL执行时已经设置了查询超时时间，
    当事务超时的剩余秒数小于已设置的查询超时时间时，
    将使用事务超时的剩余秒数覆盖已设置的查询超时时间。

    下面显示查询超时处理的示例。

    模式1
      | 已设置查询超时时间: 10秒
      | 事务超时的剩余秒数: 15秒
      | SQL执行时设置的查询超时时间: 10秒
      | 查询超时发生时不会成为事务超时，而是抛出SQL执行异常

    模式2
      | 已设置查询超时时间: 10秒
      | 事务超时的剩余秒数: 5秒
      | SQL执行时设置的查询超时时间: 5秒
      | 查询超时发生时将成为事务超时，抛出 :java:extdoc:`TransactionTimeoutException <nablarch.core.transaction.TransactionTimeoutException>` 。

  .. tip::

    由于该功能在数据库访问时进行事务超时检查，
    因此在不访问数据库的逻辑中发生处理延迟时，不会成为事务超时。

    例如，如果在不访问数据库的逻辑中发生无限循环，本功能无法检测事务超时。
    在这种情况下，请使用应用程序服务器的超时功能等方式处理延迟的应用程序线程。

事务超时时间重置时机
  显式开始事务时(调用 :java:extdoc:`Transaction#begin <nablarch.core.transaction.Transaction.begin()>` )时，事务超时时间将被重置。
  请注意，在事务结束时( :java:extdoc:`Transaction#commit <nablarch.core.transaction.Transaction.commit()>` 或 :java:extdoc:`Transaction#rollback <nablarch.core.transaction.Transaction.rollback()>` )，
  事务超时的剩余时间不会重置。

扩展示例
--------------------------------------------------

.. _transaction_addResource:

添加事务控制目标资源
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
添加事务控制目标资源时，需要以下步骤：

例如，将IBM MQ作为分布式事务的事务管理器来控制事务时即属于这种情况。

#. 添加事务实现
#. 添加生成事务的工厂实现
#. :ref:`transaction_management_handler` 实现事务控制

下面显示详细步骤。

添加事务实现
  事务实现 :java:extdoc:`Transaction <nablarch.core.transaction.Transaction>` 接口，
  并实现事务控制目标资源的事务开始、结束处理。

  .. code-block:: java

    public class SampleTransaction implements Transaction {

      private final String resourceName;

      // 接收用于识别事务控制目标资源的资源名。
      // 事务控制时，需要从此资源名获取事务控制目标资源。
      public SampleTransaction(String resourceName) {
        this.resourceName = resourceName;
      }

      @Override
      public void begin() {
        // 实现事务控制目标资源的事务开始处理
      }

      @Override
      public void commit() {
        // 实现事务控制目标资源的事务提交处理
      }

      @Override
      public void rollback() {
        // 实现事务控制目标资源的事务回滚处理
      }
    }

添加生成事务的工厂实现
  创建生成事务的工厂类。
  工厂类实现 :java:extdoc:`TransactionFactory <nablarch.core.transaction.TransactionFactory>` 。

  此示例是生成上述创建的 `SampleTransaction` 的工厂类。

  .. code-block:: java

    public class SampleTransactionFactory implements TransactionFactory {

      @Override
      public Transaction getTransaction(String resourceName) {
        // 生成并返回具有用于识别事务控制目标的资源名的事务对象。
        SampleTransaction transaction = new SampleTransaction(resourceName);
        return transaction;
      }
    }

:ref:`transaction_management_handler` 实现事务控制
  通过使用Nablarch标准处理器中包含的事务控制处理器，可以实现事务控制。

  如下例所示，将添加的工厂类配置到事务控制处理器中。

  .. code-block:: xml

    <!-- 事务控制处理器 -->
    <component class="nablarch.common.handler.TransactionManagementHandler">

      <!-- 事务工厂 -->
      <property name="transactionFactory">
        <component class="sample.SampleTransactionFactory" />
      </property>

   </component>
