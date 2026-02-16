.. _`db_double_submit`:

使用数据库防止重复提交
=====================================================================

.. contents:: 目录
  :depth: 3
  :local:

:ref:`重复提交防止 <tag-double_submission>` 中，服务器端令牌保存在HTTP会话中。
因此，在扩展应用服务器时，需要使用粘性会话或会话复制等。

通过使用将服务器端令牌保存在数据库中的实现，可以在不进行应用服务器特别配置的情况下，
在多个应用服务器之间共享令牌。

.. tip::

  在浏览器关闭等情况下，令牌可能会残留在表上。
  因此，需要定期删除已过期的令牌。

.. important::

  使用HTTP会话的 :ref:`重复提交防止 <tag-double_submission>` 可以用于CSRF防护，
  但本功能由于不识别用户就将令牌存储在数据库中，因此不能用于CSRF防护。
  使用本功能时，CSRF防护请使用 :ref:`csrf_token_verification_handler` 。

功能概述
---------------------------------------------------------------------

可以将服务器端令牌保存在数据库中

模块列表
---------------------------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web-doublesubmit-jdbc</artifactId>
  </dependency>


使用方法
---------------------------------------------------------------------

需要在数据库上创建用于保存令牌的表。

创建表的定义如下所示。

`DOUBLE_SUBMISSION` 表
  ==================== ====================
  列名                 数据类型
  ==================== ====================
  TOKEN(PK)            `java.lang.String`
  CREATED_AT           `java.sql.Timestamp`
  ==================== ====================

表名和列名可以更改。
更改时，需在 :java:extdoc:`DbTokenManager.dbTokenSchema <nablarch.common.web.token.DbTokenManager.setDbTokenSchema(nablarch.common.web.token.DbTokenSchema)>` 中
定义 :java:extdoc:`DbTokenSchema <nablarch.common.web.token.DbTokenSchema>` 的组件。

需要添加2种组件定义。

添加名为 ``tokenManager`` 的组件定义。
这样令牌将由数据库管理。
``tokenManager`` 需要 :ref:`初始化<repository-initialize_object>` 。

.. code-block:: xml
                
  <component name="tokenManager" class="nablarch.common.web.token.DbTokenManager">
    <property name="dbManager">
      <component class="nablarch.core.db.transaction.SimpleDbTransactionManager">
        <property name="dbTransactionName" value="tokenTransaction"/>
      </component>
    </property>
    <!-- 从上述表定义更改表名、列名时才需要以下配置 -->
    <property name="dbTokenSchema">
      <component class="nablarch.common.web.token.DbTokenSchema">
        <property name="tableName" value="DB_TOKEN"/>
        <property name="tokenName" value="VALUE_COL"/>
        <property name="createdAtName" value="CREATED_AT_COL"/>
      </component>
    </property>
  </component>

  <!-- 由于需要初始化，请进行以下配置 -->
  <component name="initializer" class="nablarch.core.repository.initialization.BasicApplicationInitializer">
    <property name="initializeList">
      <list>
        <component-ref name="tokenManager"/>
      </list>
    </property>
  </component>


添加名为 ``tokenGenerator`` 的组件定义。
这样令牌将使用UUID，无需考虑推测和冲突的可能性。

.. code-block:: xml

    <component name="tokenGenerator"
               class="nablarch.common.web.token.UUIDV4TokenGenerator" />

.. important::

  :ref:`测试框架的令牌发行<how_to_set_token_in_request_unit_test>` 不支持令牌的数据库保存。
  因此，自动测试执行时需要替换为 :java:extdoc:`HttpSessionTokenManager <nablarch.common.web.token.HttpSessionTokenManager>` 进行测试。

  .. code-block:: xml

    <!-- 将令牌保存在HTTP会话中 -->
    <component name="tokenManager" class="nablarch.common.web.token.HttpSessionTokenManager"/>
