.. _database:

数据库访问(JDBC包装器)
=========================================

.. contents:: 目录
  :depth: 3
  :local:

提供使用JDBC执行SQL语句访问数据库的功能。

.. tip::

  如 :ref:`database_management` 所述，建议使用 :ref:`universal_dao` 来执行SQL。

  此外，由于 :ref:`universal_dao` 内部使用此功能的API进行数据库访问，
  因此使用此功能所需的配置是必需的。

.. important::

  此功能依赖于JDBC 3.0，因此使用的JDBC驱动必须实现JDBC 3.0或更高版本。


功能概述
----------------------

.. _database-dialect:

无需关注数据库方言即可使用
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
通过配置与使用数据库产品对应的 :java:extdoc:`Dialect <nablarch.core.db.dialect.Dialect>` ，
可以在不考虑产品间方言差异的情况下实现应用程序。

:java:extdoc:`Dialect <nablarch.core.db.dialect.Dialect>` 提供以下功能。

* 返回是否可以使用identity列的方法(:java:extdoc:`supportsIdentity <nablarch.core.db.dialect.Dialect.supportsIdentity()>` )
* 返回对具有identity(自动编号)列的表是否可以进行batch insert的方法(:java:extdoc:`supportsIdentityWithBatchInsert <nablarch.core.db.dialect.Dialect.supportsIdentityWithBatchInsert()>`)
* 返回是否可以使用序列对象的方法(:java:extdoc:`supportsSequence <nablarch.core.db.dialect.Dialect.supportsSequence()>` )
* 返回在搜索查询的范围指定中是否可以使用offset（或等效功能）的方法(:java:extdoc:`supportsOffset <nablarch.core.db.dialect.Dialect.supportsOffset()>` )
* 判断是否表示唯一约束违反的 :java:extdoc:`SQLException <java.sql.SQLException>` 的方法(:java:extdoc:`isDuplicateException <nablarch.core.db.dialect.Dialect.isDuplicateException(java.sql.SQLException)>` )
* 判断是否属于事务超时目标的  :java:extdoc:`SQLException <java.sql.SQLException>` 的方法(:java:extdoc:`isTransactionTimeoutError <nablarch.core.db.dialect.Dialect.isTransactionTimeoutError(java.sql.SQLException)>` )
* 生成从序列对象获取下一个值的SQL语句的方法(:java:extdoc:`buildSequenceGeneratorSql <nablarch.core.db.dialect.Dialect.buildSequenceGeneratorSql(java.lang.String)>` )
* 返回从 :java:extdoc:`ResultSet <java.sql.ResultSet>` 获取值的 :java:extdoc:`ResultSetConvertor <nablarch.core.db.statement.ResultSetConvertor>` 的方法(:java:extdoc:`getResultSetConvertor <nablarch.core.db.dialect.Dialect.getResultSetConvertor()>` )
* 将搜索查询转换为范围指定（分页用）SQL的方法(:java:extdoc:`convertPaginationSql <nablarch.core.db.dialect.Dialect.convertPaginationSql(java.lang.String,nablarch.core.db.statement.SelectOption)>` )
* 将搜索查询转换为件数获取SQL的方法(:java:extdoc:`convertCountSql(String) <nablarch.core.db.dialect.Dialect.convertCountSql(java.lang.String)>` )
* 将SQLID转换为件数获取SQL的方法(:java:extdoc:`convertCountSql(String, Object, StatementFactory) <nablarch.core.db.dialect.Dialect.convertCountSql(java.lang.String,java.lang.Object,nablarch.core.db.statement.StatementFactory)>` )
* 返回检查 :java:extdoc:`Connection <java.sql.Connection>` 是否已连接到数据库的SQL的方法(:java:extdoc:`getPingSql <nablarch.core.db.dialect.Dialect.getPingSql()>` )

:java:extdoc:`Dialect <nablarch.core.db.dialect.Dialect>` 的配置方法，请参阅 :ref:`database-use_dialect` 。

.. _database-sql_file:

SQL应写在SQL文件中而非逻辑中
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SQL应定义在SQL文件中，原则上不应写在逻辑内。

通过将SQL写在SQL文件中，无需在逻辑中组装SQL，
因为一定会使用 `PreparedStatement` ，所以可以消除SQL注入漏洞。

.. tip::

  如果确实无法定义在SQL文件中，也提供了直接指定SQL执行的API，请使用该API。
  但是，随意使用可能会嵌入SQL注入漏洞，因此需要注意。
  此外，前提是能够在测试或审查中保证不存在SQL注入漏洞。


详细内容请参阅 :ref:`database-use_sql_file` 。

.. _database-bean:

可以将Bean的属性值嵌入到SQL的绑定变量中
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
提供将Bean属性中设置的值自动绑定到 :java:extdoc:`java.sql.PreparedStatement` 的IN参数的功能。

使用此功能后，无需多次调用 :java:extdoc:`java.sql.PreparedStatement` 的值设置方法，
且在IN参数增减时无需修正索引。

详细内容请参阅 :ref:`database-input_bean` 。

可以轻松实现like搜索
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
提供对like搜索自动插入escape子句和对通配符字符进行转义处理的功能。

详细内容请参阅 :ref:`database-like_condition` 。

.. _database-variable_condition:

可以根据运行时Bean对象的状态动态构建SQL语句
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
提供根据Bean对象的状态动态组装执行SQL语句的功能。

例如，可以进行条件和in子句的动态构建等。

详细内容请参阅以下内容。

* :ref:`database-use_variable_condition`
* :ref:`database-in_condition`
* :ref:`database-make_order_by`

可以缓存SQL的查询结果
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
当执行的SQL和从外部获取的条件（绑定变量中设置的值）相等时，
提供不访问数据库而是从缓存返回搜索结果的功能。

详细内容请参阅 :ref:`database-use_cache` 。

模块列表
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-jdbc</artifactId>
  </dependency>

使用方法
--------------------------------------------------

.. _database-connect:

数据库连接配置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
数据库连接配置可以从以下两种方式中选择。

* 使用 :java:extdoc:`javax.sql.DataSource` 生成数据库连接
* 使用注册到应用服务器等的数据源生成数据库连接

如果要使用上述以外的连接方法（例如使用OSS连接池库等），
请参阅 :ref:`database-add_connection_factory` ，添加连接数据库的实现。

连接配置示例
  从 :java:extdoc:`javax.sql.DataSource` 生成数据库连接
    .. code-block:: xml

      <component class="nablarch.core.db.connection.BasicDbConnectionFactoryForDataSource">
        <!-- 配置值的详细内容请参阅Javadoc -->
      </component>

  从应用服务器的数据源生成数据库连接
    .. code-block:: xml

      <component class="nablarch.core.db.connection.BasicDbConnectionFactoryForJndi">
        <!-- 配置值的详细内容请参阅Javadoc -->
      </component>

  :java:extdoc:`BasicDbConnectionFactoryForDataSource<nablarch.core.db.connection.BasicDbConnectionFactoryForDataSource>` 和
  :java:extdoc:`BasicDbConnectionFactoryForJndi <nablarch.core.db.connection.BasicDbConnectionFactoryForJndi>` 的
  配置值，请参阅各自类的Javadoc。

.. tip::

  基本上不会直接使用上述配置的类。
  需要数据库访问时，请使用 :ref:`database_connection_management_handler` 。

  此外，使用数据库时还需要事务管理。
  关于事务管理，请参阅 :ref:`transaction` 。

.. _database-use_dialect:

使用与数据库产品对应的方言(Dialect)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
通过在组件配置文件中配置与数据库产品对应的方言(Dialect)，方言(Dialect)功能将生效。

.. tip::
  如果未配置，将使用 :java:extdoc:`DefaultDialect <nablarch.core.db.dialect.DefaultDialect>` 。
  :java:extdoc:`DefaultDialect <nablarch.core.db.dialect.DefaultDialect>` 原则上所有功能都将被禁用，因此请务必配置与数据库产品对应的方言(Dialect)。

  此外，如果没有与使用数据库产品对应的方言(Dialect)，
  或想使用新版本的新功能时，请参阅 :ref:`database-add_dialect` 创建新的方言(Dialect)。

组件配置示例
  此示例是配置从 :java:extdoc:`javax.sql.DataSource` 获取数据库连接的组件的示例。
  :java:extdoc:`BasicDbConnectionFactoryForJndi <nablarch.core.db.connection.BasicDbConnectionFactoryForJndi>` 的情况下，也与以下示例相同，
  在 :java:extdoc:`dialect <nablarch.core.db.connection.ConnectionFactorySupport.setDialect(nablarch.core.db.dialect.Dialect)>` 属性中配置方言(Dialect)即可。

  .. code-block:: xml

    <component class="nablarch.core.db.connection.BasicDbConnectionFactoryForDataSource">
      <!-- 省略与方言(Dialect)无关的属性 -->

      <!--
      方言(Dialect)配置在dialect属性中。
      此示例中配置的是Oracle数据库用的方言(Dialect)。
      -->
      <property name="dialect">
        <component class="nablarch.core.db.dialect.OracleDialect" />
      </property>
    </component>


.. _database-use_sql_file:

使用文件管理SQL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
如 :ref:`database-sql_file` 所述，此功能中SQL由SQL文件管理。
要处理SQL文件，需要在组件配置文件中进行配置。
详细内容请参阅 :ref:`从SQL文件加载SQL的配置 <database-load_sql>` 。

SQL文件按照以下规则创建。

* 创建在类路径下。
* 一个SQL文件中可以记述多个SQL，但SQLID在文件内必须唯一。
* SQLID与SQLID之间插入空行。（包含空格的行不视为空行）
* SQLID与SQL之间插入 ``=`` 。
* 注释使用 ``--`` 记述。（不支持块注释）
* SQL可以使用换行或空格(tab)等进行格式化。

.. important::

  SQL不要在多个功能间共用，务必为每个功能单独创建。

  如果在多个功能间共用，由于意外的使用方式或SQL变更可能导致意想不到的故障。
  例如，如果在多个功能中使用的SQL语句中添加了排他锁用的 ``for update`` ，
  则在不需要排他锁的功能中获取了锁，导致处理延迟。

以下展示SQL文件示例。

.. code-block:: sql

  -- XXXXX获取SQL
  -- SQL_ID:GET_XXXX_INFO
  GET_XXXX_INFO =
  select
     col1,
     col2
  from
     test_table
  where
     col1 = :col1


  -- XXXXX更新SQL
  -- SQL_ID:UPDATE_XXXX
  update_xxxx =
  update
      test_table
  set
      col2 = :col2
  where
      col1 = :col1

.. _database-load_sql:

从SQL文件加载SQL的配置
  说明从SQL文件加载SQL所需的配置内容。

  要加载SQL，需要像以下示例一样，在 :java:extdoc:`BasicStatementFactory#sqlLoader <nablarch.core.db.statement.BasicStatementFactory.setSqlLoader(nablarch.core.cache.StaticDataLoader)>`
  中配置 :java:extdoc:`BasicSqlLoader <nablarch.core.db.statement.BasicSqlLoader>` 。

  此示例中配置了文件编码和扩展名。如果省略配置，则使用以下配置值。

  :文件编码: utf-8
  :扩展名: sql

  此处定义的 :java:extdoc:`BasicStatementFactory <nablarch.core.db.statement.BasicStatementFactory>` 组件，需要在 :ref:`database-connect`
  中定义的数据库连接获取组件中进行配置。

  配置示例
    .. code-block:: xml

      <component name="statementFactory" class="nablarch.core.db.statement.BasicStatementFactory">
        <property name="sqlLoader">
          <component class="nablarch.core.db.statement.BasicSqlLoader">
            <property name="fileEncoding" value="utf-8"/>
            <property name="extension" value="sql"/>
          </component>
        </property>
      </component>

.. _database-execute_sqlid:

指定SQLID执行SQL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
要根据SQLID执行SQL，需要使用从 :java:extdoc:`DbConnectionContext <nablarch.core.db.connection.DbConnectionContext>` 获取的数据库连接。
此外，需要在 :ref:`database_connection_management_handler` 中将数据库连接注册到 :java:extdoc:`DbConnectionContext <nablarch.core.db.connection.DbConnectionContext>` 。

SQLID与实际执行的SQL之间的映射规则如下。

* SQLID中 ``#`` 之前的部分是SQL文件名。
* SQLID中 ``#`` 之后的部分是SQL文件内的SQLID。

实现示例
  此示例中，SQLID指定为 ``jp.co.tis.sample.action.SampleAction#findUser`` ，因此
  SQL文件为类路径下的 ``jp.co.tis.sample.action.SampleAction.sql`` 。
  SQL文件内的SQLID为 ``findUser`` 。

  * :java:extdoc:`AppDbConnection <nablarch.core.db.connection.AppDbConnection>` 和
    :java:extdoc:`SqlPStatement <nablarch.core.db.statement.SqlPStatement>` 的使用方法，请参阅Javadoc。

  .. code-block:: java

    // 从DbConnectionContext获取数据库连接。
    AppDbConnection connection = DbConnectionContext.getConnection();

    // 根据SQLID生成语句。
    SqlPStatement statement = connection.prepareStatementBySqlId(
        "jp.co.tis.sample.action.SampleAction#findUser");

    // 设置条件。
    statement.setLong(1, userId);

    // 执行搜索处理。
    SqlResultSet result = statement.retrieve();

执行存储过程
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
执行存储过程时，基本上与执行SQL时的实现方式相同。

.. important::

  在执行存储过程时，不支持 :ref:`database-bean` 。
  这是因为如果使用存储过程，逻辑会分散在Java和存储过程之间，
  显著降低可维护性，因此原则上不应使用。

  但是，考虑到在现有资产等中可能必须使用存储过程的情况，
  本功能提供了非常简单的用于执行存储过程的API。

以下展示示例。

* :java:extdoc:`SqlCStatement <nablarch.core.db.statement.SqlCStatement>` 的详细使用方法，请参阅Javadoc。

.. code-block:: java

  // 根据SQLID生成执行存储过程用的语句。
  SqlCStatement statement = connection.prepareCallBySqlId(
      "jp.co.tis.sample.action.SampleAction#execute_sp");

  // 设置IN及OUT参数。
  statement.registerOutParameter(1, Types.CHAR);

  // 执行。
  statement.execute();

  // 获取OUT参数。
  String result = statement.getString(1);

.. _database-paging:

指定搜索范围执行SQL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
在Web系统的列表搜索画面等中，有时会使用分页功能仅显示特定范围的结果。
针对此类用途，本功能提供了可以指定搜索结果范围的功能。

实现示例
  从数据库连接( `connection` )生成语句时，指定搜索对象的范围。
  此示例中指定了以下值，因此将获取从第11条开始的最多10条记录。

  :开始位置: 11
  :获取件数: 10

  .. code-block:: java

    // 从DbConnectionContext获取数据库连接
    AppDbConnection connection = DbConnectionContext.getConnection();

    // 指定SQLID和搜索范围生成语句对象。
    SqlPStatement statement = connection.prepareStatementBySqlId(
        "jp.co.tis.sample.action.SampleAction#findUser", new SelectOption(11, 10));

    // 执行搜索处理
    SqlResultSet result = statement.retrieve();

.. tip::
  指定搜索范围时，会将搜索用SQL重写为获取范围指定的SQL后执行。
  此外，获取范围指定的SQL由 :ref:`方言(Dialect) <database-dialect>` 进行。

.. _database-input_bean:

以Bean对象为输入执行SQL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
如 :ref:`database-bean` 所述，可以以Bean对象为输入执行SQL。

以Bean对象为输入执行SQL时，SQL的IN参数使用命名绑定变量。
命名参数记述为 ``:`` 后接作为输入接收的Bean属性名。

.. important::

  如果IN参数使用JDBC标准的 ``?`` 记述，则无法以Bean对象为输入执行SQL，请注意。

以下展示实现示例。

SQL示例
  IN参数使用命名参数。

  .. code-block:: sql

    insert into user
      (
      id,
      name
      ) values (
      :id,
      :userName
      )

实现示例
  在Bean对象中设置必要的值，然后调用以Bean对象为输入执行SQL的功能。

  * :java:extdoc:`AppDbConnection <nablarch.core.db.connection.AppDbConnection>` 和 :java:extdoc:`ParameterizedSqlPStatement <nablarch.core.db.statement.ParameterizedSqlPStatement>` 的使用方法，请参阅Javadoc。
  * 关于SQLID与执行的SQL的关系，请参阅 :ref:`database-execute_sqlid`

  .. code-block:: java

    // 生成bean并在属性中设置值
    UserEntity entity = new UserEntity();
    entity.setId(1);              // 设置id属性的值
    entity.setUserName("名字"); // 设置userName属性的值

    // 从DbConnectionContext获取数据库连接
    AppDbConnection connection = DbConnectionContext.getConnection();

    // 根据SQLID生成语句
    ParameterizedSqlPStatement statement = connection.prepareParameterizedSqlStatementBySqlId(
        "jp.co.tis.sample.action.SampleAction#insertUser");

    // 将bean属性的值设置到绑定变量中并执行SQL
    // SQL的:id中设置bean的id属性的值。
    // SQL的:userName中设置bean的userName属性的值。
    int result = statement.executeUpdateByObject(entity);

.. tip::

  除了Bean，还可以指定 :java:extdoc:`java.util.Map` 的实现类。
  指定Map时，Map的值会设置到与Map键值匹配的IN参数中。

  此外，指定Bean时，使用 :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` 转换为Map后进行处理。
  如果Bean的属性中存在 :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` 不支持的类型，则该属性无法使用此功能。
  
  如果想增加 :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` 可以复制到Map的类型，请参阅 :ref:`utility-conversion` 进行对应。

.. tip::

  可以将Bean的访问方式从属性更改为字段。
  要更改为字段访问时，需要在properties文件中添加以下配置。

  .. code-block:: properties

     nablarch.dbAccess.isFieldAccess=true

  此外，由于以下原因，不推荐字段访问。

  本框架的其他功能（例如 :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` ）中，从Bean获取值的方法统一使用属性访问。
  如果仅数据库功能更改为字段访问，程序员需要同时意识到字段访问和属性访问，这会导致生产力下降和故障原因。


类型转换
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

数据库访问(JDBC包装器)将与数据库输入输出使用变量的类型转换委托给JDBC驱动。
因此，输入输出使用的变量类型需要根据数据库类型及使用的JDBC驱动规范来定义。

如果需要任意类型转换，则需要对用于与数据库输入输出的变量在应用程序侧进行类型转换。

- 输入使用Bean时，在向Bean属性设置值时进行类型转换；输出使用Bean时，在从属性取出值后进行类型转换。
- 输入使用Map时，在向Map设置值时进行类型转换；输出使用Map时，在取出值后进行类型转换。
- 指定索引设置绑定变量时，将绑定变量要设置的对象转换为适当的类型。从 :java:extdoc:`SqlRow <nablarch.core.db.statement.SqlRow>` 获取值时，在获取后进行类型转换。


.. _database-common_bean:

SQL执行时自动设置通用值
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
提供在数据登记或更新时，对每次都要设置的值在SQL执行前自动设置的功能。
例如，可以使用此功能处理登记日期时间和更新日期时间等项目。

此功能根据属性中设置的注解自动设置值，
因此仅在 :ref:`database-input_bean` 使用时有效。

以下展示使用示例。

组件配置文件
  要使用此功能，需要在组件配置文件中配置自动设置值的类。

  像以下示例一样，对 :java:extdoc:`BasicStatementFactory#updatePreHookObjectHandlerList <nablarch.core.db.statement.BasicStatementFactory.setUpdatePreHookObjectHandlerList(java.util.List)>` ，
  以list形式设置 :java:extdoc:`AutoPropertyHandler <nablarch.core.db.statement.AutoPropertyHandler>` 实现类。
  此外，标准提供的实现类配置在 :java:extdoc:`nablarch.core.db.statement.autoproperty` 包下。

  此处定义的 :java:extdoc:`BasicStatementFactory <nablarch.core.db.statement.BasicStatementFactory>` 组件，需要在 :ref:`database-connect`
  中定义的数据库连接获取组件中进行配置。

  .. code-block:: xml

    <component name="statementFactory"
        class="nablarch.core.db.statement.BasicStatementFactory">

      <property name="updatePreHookObjectHandlerList">
        <list>
          <!-- 以list形式设置nablarch.core.db.statement.AutoPropertyHandler实现类-->
        </list>
      </property>
    </component>

Bean对象(Entity)
  在要自动设置值的属性中配置注解。
  此外，标准提供的注解配置在 :java:extdoc:`nablarch.core.db.statement.autoproperty` 包下。

  .. code-block:: java

    public class UserEntity {
      // 用户ID
      private String id;

      // 登记日期时间
      // 登记时自动设置
      @CurrentDateTime
      private Timestamp createdAt;

      // 更新日期时间
      // 登记·更新时自动设置
      @CurrentDateTime
      private String updatedAt;

      // 访问方法等省略
    }

SQL
  SQL的创建方式与 :ref:`database-input_bean` 相同。

  .. code-block:: sql

    insert into user (
      id,
      createdAt,
      updatedAt
    ) values (
      :id,
      :createdAt,
      :updatedAt
    )

实现示例
  基本上与 :ref:`database-input_bean` 的实现方式相同。
  对于自动设置值的字段，无需在逻辑中向Bean设置值。
  此外，即使明确设置了值，也会在SQL执行前被自动设置值功能覆盖。

  .. code-block:: java

    // 生成bean并在属性中设置值
    // 对于自动设置字段createdAt和updatedAt无需设置值
    UserEntity entity = new UserEntity();
    entity.setId(1);

    // 从DbConnectionContext获取数据库连接
    AppDbConnection connection = DbConnectionContext.getConnection();

    // 根据SQLID生成语句
    ParameterizedSqlPStatement statement = connection.prepareParameterizedSqlStatementBySqlId(
        "jp.co.tis.sample.action.SampleAction#insertUser");

    // 在不设置自动设置字段值的情况下调用。
    // 数据库功能自动设置值。
    int result = statement.executeUpdateByObject(entity);

.. _database-like_condition:

执行like搜索
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
like搜索使用 :ref:`database-input_bean` ，在SQL中按照以下规则记述like搜索用的条件。

前方一致的情况
  在命名参数的末尾记述 ``%`` 。

  例: ``name like :userName%``

后方一致的情况
  在命名参数的开头记述 ``%`` 。

  例: ``name like :%userName``

中间一致的情况
  在命名参数的前后记述 ``%`` 。

  例: ``name like :%userName%``

like搜索时的转义字符及转义目标字符的定义，请参阅 :ref:`database-def_escape_char` 。

以下展示实现示例。

SQL
  按照上述规则定义SQL。

  .. code-block:: sql

    select *
      from user
     where name like :userName%

实现示例
  与 :ref:`database-input_bean` 一样执行SQL即可，like条件用的值重写和转义处理会自动进行。
  此示例的情况下，实际条件变为 ``name like '名%' escape '\'`` 。

  * :java:extdoc:`AppDbConnection <nablarch.core.db.connection.AppDbConnection>` 和 :java:extdoc:`ParameterizedSqlPStatement <nablarch.core.db.statement.ParameterizedSqlPStatement>` 的使用方法，请参阅Javadoc。
  * 关于SQLID与执行的SQL的关系，请参阅 :ref:`database-execute_sqlid`

  .. code-block:: java

    // 生成bean并在属性中设置值
    UserEntity entity = new UserEntity();
    entity.setUserName("名"); // 设置userName属性的值

    // 从DbConnectionContext获取数据库连接
    AppDbConnection connection = DbConnectionContext.getConnection();

    // 根据SQLID生成语句
    ParameterizedSqlPStatement statement = connection.prepareParameterizedSqlStatementBySqlId(
        "jp.co.tis.sample.action.SampleAction#findUserByName");

    // 将bean属性值设置到绑定变量中并执行SQL
    // 此示例的情况下，执行 name like '名%'
    int result = statement.retrieve(bean);


.. _database-def_escape_char:

定义like搜索时的转义字符及转义目标字符
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
转义字符及转义目标字符的定义在组件配置文件中进行。
此外，转义字符自动成为转义目标，无需明确设置为转义目标字符。

如果省略配置，则使用以下值。

:转义字符: ``\``
:转义目标字符: ``%`` 、 ``_``

组件配置示例
  此示例中将 ``\`` 设置为转义字符，将 ``%`` 、 ``％`` 、 ``_`` 、 ``＿`` 这4个字符设置为转义目标字符。

  此处定义的 :java:extdoc:`BasicStatementFactory <nablarch.core.db.statement.BasicStatementFactory>` 组件，需要在 :ref:`database-connect`
  中定义的数据库连接获取组件中进行配置。

  .. code-block:: xml

    <component name="statementFactory" class="nablarch.core.db.statement.BasicStatementFactory">
      <!-- 转义字符的定义 -->
      <property name="likeEscapeChar" value="\" />

      <!-- 转义目标字符的定义(以逗号分隔设置) -->
      <property name="likeEscapeTargetCharList" value="%,％,_,＿" />
    </component>

.. _database-use_variable_condition:

执行带有可变条件的SQL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
执行带有可变条件的SQL时，使用 :ref:`database-input_bean` ，并用以下记法记述条件。

可变条件的记述规则
  可变条件记述为 ``$if(属性名) {SQL语句的条件}`` 。
  根据 ``$if`` 后属性名对应的Bean对象的值，该条件将被排除。
  被排除的条件如下。

  * 数组或 :java:extdoc:`java.util.Collection` 的情况下，属性值为null或大小为0时
  * 上述以外的类型的情况下，属性值为null或空字符串(String对象的情况)时

  此外， ``$if`` 特殊语法有以下限制。

  * 只能用于where子句
  * ``$if`` 内不能使用 ``$if``

  .. important::

    此功能用于如Web应用程序的搜索画面那样，根据用户输入内容搜索条件会变化的情况。
    并非用于将条件仅不同的多个SQL共用的目的。
    随意共用的情况下，变更SQL时可能埋下意想不到的故障原因，因此务必定义多个SQL。


以下展示示例。

SQL
  此SQL中， ``user_name`` 和 ``user_kbn`` 的条件为可变。

  .. code-block:: none

    select
      user_id,
      user_name,
      user_kbn
    from
      user
    where
      $if (userName) {user_name like :userName%}
      and $if (userKbn) {user_kbn in ('1', '2')}
      and birthday = :birthday

实现示例
  由于仅在 `userName` 属性中设置了值，
  因此在可变条件中定义的 ``user_kbn`` 将在运行时从条件中排除。

  .. code-block:: java

    // 生成bean并在属性中设置值
    UserEntity entity = new UserEntity();
    entity.setUserName("名字");

    // 从DbConnectionContext获取数据库连接
    AppDbConnection connection = DbConnectionContext.getConnection();

    // 根据SQLID生成语句
    // 第2个参数中指定带有条件的Bean对象。
    // 根据此Bean对象的状态进行SQL可变条件的组装。
    ParameterizedSqlPStatement statement = connection.prepareParameterizedSqlStatementBySqlId(
        "jp.co.tis.sample.action.SampleAction#insertUser", entity);

    // 将entity属性的值设置到绑定变量中并执行SQL
    SqlResultSet result = statement.retrieve(entity);

.. _database-in_condition:

执行in子句条件数可变的SQL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
执行in子句条件数可变的SQL时，使用 :ref:`database-input_bean` ，并用以下记法记述条件。

in子句的记述规则
  在条件的命名参数末尾附加 ``[]`` 。
  此外，与命名参数对应的Bean对象属性的类型，
  必须是数组或 :java:extdoc:`java.util.Collection` (包含子类型) [#collection]_ 。

  .. tip::

    如果作为in子句条件的属性值为null或大小为0，则务必将该条件定义为可变条件。
    如果没有定义为可变条件而属性值为null，则条件变为 ``xxxx in (null)`` ，
    可能无法正确获取搜索结果。

    ※由于in子句不能使条件表达式（括号内）为空，因此当指定大小为0的数组或null时，
    规格上将条件表达式设为 ``in (null)`` 。

以下展示示例。

SQL
  此SQL中， ``user_kbn`` 的in条件动态构建。
  此外，由于与 ``$if`` 并用，当 `userKbn` 属性为null或大小为0时，将从条件中排除。

  .. code-block:: none

    select
      user_id,
      user_name,
      user_kbn
    from
      user
    where
      $if (userKbn) {user_kbn in (:userKbn[])}

执行示例
  此示例中，由于 `userKbn` 属性中设置了2个元素，
  因此执行的SQL条件变为 ``userKbn in (?, ?)`` 。

  从数据库获取的是 `userKbn` 为 ``1`` 和 ``3`` 的记录。

  .. code-block:: java

    // 生成bean并在属性中设置值
    UserSearchCondition condition = new UserSearchCondition();
    condition.setUserKbn(Arrays.asList("1", "3"));

    // 从DbConnectionContext获取数据库连接
    AppDbConnection connection = DbConnectionContext.getConnection();

    // 根据SQLID生成语句
    // 第2个参数中指定带有条件的Bean对象。
    // 根据此Bean对象的状态进行SQL的in子句组装。
    ParameterizedSqlPStatement statement = connection.prepareParameterizedSqlStatementBySqlId(
        "jp.co.tis.sample.action.SampleAction#searchUser", condition);

    // 将condition属性的值设置到绑定变量中并执行SQL
    SqlResultSet result = statement.retrieve(condition);
    
.. [#collection] 
    如 :ref:`database-input_bean` 所述，属性值使用 :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` 转换为Map后使用。
    因此，如果属性声明为 :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` 不支持的类型，
    则无法向in子句设置条件，请注意。
    
    此外，关于在 :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` 中添加转换目标类型的方法，
    请参阅 :ref:`utility-conversion-add-rule` 。

.. _database-make_order_by:

执行时动态切换order by的排序项目执行SQL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
执行order by的排序项目可变的SQL时，使用 :ref:`database-input_bean` ，并用以下记法记述条件。

order by子句的记述规则
  要使排序项目可变，使用 ``$sort`` 代替order by子句，并如下记述。

  .. code-block:: text

     $sort(属性名) {(情况1)(情况2)···(情况n)}

     属性名: Bean对象保持排序ID的属性名
     情况: 表示order by子句的切换候选项。
             记述用于唯一识别候选项的排序ID和要在order by子句中指定的字符串（以下称为情况主体）。
             对于与任何候选项都不匹配时使用的默认情况，排序ID指定为"default"。

  * 各种情况通过将排序ID和情况主体用半角圆括号括起来表示。
  * 排序ID和情况主体用半角空格分隔。
  * 排序ID中不能使用半角空格。
  * 情况主体中可以使用半角空格。
  * 将括号开始后首次出现的字符串作为排序ID。
  * 将排序ID之后到括号结束之间的部分作为情况主体。
  * 排序ID及情况主体进行修剪处理。

以下展示使用示例。

SQL
  .. code-block:: none

    select
      user_id,
      user_name
    from
      user
    where
      user_name = :userName
    $sort(sortId) {
      (user_id_asc  user_id asc)
      (user_id_desc user_id desc)
      (name_asc     user_name asc)
      (name_desc    user_name desc)
      (default      user_id)
    }

实现示例
  此示例中，由于排序ID设置为 ``name_asc`` ，
  因此order by子句变为 ``order by user_name asc`` 。

  .. code-block:: java

    // 生成bean并在属性中设置值
    UserSearchCondition condition = new UserSearchCondition();
    condition.setUserName("名字");
    condition.setSortId("name_asc");      // 设置排序ID

    // 从DbConnectionContext获取数据库连接
    AppDbConnection connection = DbConnectionContext.getConnection();

    // 根据SQLID生成语句
    // 第2个参数中指定带有条件的Bean对象。
    // 根据此Bean对象的状态进行SQL的order by子句组装。
    ParameterizedSqlPStatement statement = connection.prepareParameterizedSqlStatementBySqlId(
        "jp.co.tis.sample.action.SampleAction#searchUser", condition);

    // 将condition属性的值设置到绑定变量中并执行SQL
    SqlResultSet result = statement.retrieve(condition);

.. _database-binary_column:

访问二进制类型的列
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
说明如何访问blob（根据数据库产品不同，二进制类型的类型也不同）等二进制类型的列。

获取二进制类型的值
  获取二进制类型的值时，从搜索结果对象 :java:extdoc:`SqlRow <nablarch.core.db.statement.SqlRow>` 中以 `byte[]` 形式获取值。

  以下展示示例。

  .. code-block:: java

    SqlResultSet rows = statement.retrieve();

    SqlRow row = rows.get(0);

    // 使用getBytes以二进制形式获取加密列的值
    byte[] encryptedPassword = row.getBytes("password");

  .. important::

    在上述实现示例中，列的内容全部展开到Java的堆上。
    因此，如果读取非常大尺寸的数据，会压迫堆区域，可能导致系统宕机等故障。

    因此，读取大量数据时，请像以下这样使用 :java:extdoc:`Blob <java.sql.Blob>` 对象，避免大量消耗堆。

    .. code-block:: java

      SqlResultSet rows = select.retrieve();

      // 作为Blob获取数据
      Blob pdf = (Blob) rows.get(0).get("PDF");

      try (InputStream input = pdf.getBinaryStream()) {
        // 从InputStream顺序读取数据进行处理。
        // 注意如果一次性读取，全部会展开到堆上
      }

登记·更新二进制类型的值
  登记·更新尺寸较小的二进制值时，使用 :java:extdoc:`SqlPStatement#setByte <nablarch.core.db.statement.SqlPStatement.setBytes(int,byte[])>` 。

  .. code-block:: java

    SqlPStatement statement = getSqlPStatement("UPDATE_PASSWORD");

    statement.setBytes(1, new byte[] {0x30, 0x31, 0x32});
    int updateCount = statement.executeUpdate();

 登记·更新尺寸较大的二进制值时，使用 :java:extdoc:`SqlPStatement#setBinaryStream <nablarch.core.db.statement.SqlPStatement.setBinaryStream(int,java.io.InputStream,int)>`
 ，从表示文件等的 :java:extdoc:`InputStream <java.io.InputStream>` 直接向数据库发送值。

 .. code-block:: java

    final Path pdf = Paths.get("input.pdf");
    try (InputStream input = Files.newInputStream(pdf)) {
        statement.setBinaryStream(1, input, (int) Files.size(pdf));
    }


.. _database-clob_column:

访问位数较大的字符串类型列（例如CLOB）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
说明如何访问像CLOB这样大尺寸的字符串类型列。

获取CLOB类型的值
  获取CLOB类型的值时，从 :java:extdoc:`搜索结果对象 <nablarch.core.db.statement.SqlRow>` 中以字符串类型获取值。

  以下展示示例。

  .. code-block:: java

    SqlResultSet rows = statement.retrieve();
    SqlRow row = rows.get(0);

    // 以String形式获取CLOB的值。
    String mailBody = row.getString("mailBody");

  .. important::

    在上述实现示例中，列的内容全部展开到Java的堆上。
    因此，如果读取非常大尺寸的数据，会压迫堆区域，可能导致系统宕机等故障。

    因此，读取大量数据时，请像以下这样使用 :java:extdoc:`Clob <java.sql.Clob>` 对象，避免大量消耗堆。

    .. code-block:: java

      SqlResultSet rows = select.retrieve();

      // 作为Clog获取数据
      Clob mailBody = (Clob) rows.get(0).get("mailBody");

      try (Reader reader = mailBody.getCharacterStream()) {
        // 从Reader顺序读取数据进行处理。
        // 注意如果将读取的数据全部保持在堆上，会压迫堆。
      }
    
向CLOB类型登记（更新）值
  登记·更新尺寸较小的值时，使用String类型的值通过 :java:extdoc:`SqlPStatement#setString <nablarch.core.db.statement.SqlPStatement.setString(int,java.lang.String)>` 进行设置。

  以下展示示例。

  .. code-block:: java

    statement.setString(1, "值");
    statement.executeUpdate();

  登记·更新尺寸较大的值时，使用 :java:extdoc:`SqlPStatement#setCharacterStream <nablarch.core.db.statement.SqlPStatement.setCharacterStream(int,java.io.Reader,int)>`
  ，经由表示文本文件等的 :java:extdoc:`Reader <java.io.Reader>` 向数据库发送值。

  以下展示示例。

  .. code-block:: java

    Path path = Paths.get(filePath);
    try (Reader reader = Files.newBufferedReader(path, StandardCharsets.UTF_8)) {
      // 使用setCharacterStream登记Reader的值。
      statement.setCharacterStream(1, reader, (int) Files.size(path));
    }


数据库访问时发生的异常种类
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
数据库访问时的异常，大致分为以下4种。

这些异常都是非检查异常，因此无需像 :java:extdoc:`SQLException <java.sql.SQLException>` 那样用 ``try-catch`` 捕获。

数据库访问错误时的异常
  数据库访问时发生的异常，抛出 :java:extdoc:`DbAccessException <nablarch.core.db.DbAccessException>` 。

数据库连接错误时的异常
  如果数据库访问错误时的异常表示数据库连接错误，则抛出 :java:extdoc:`DbConnectionException <nablarch.core.db.connection.exception.DbConnectionException>` 。
  此异常由 :ref:`retry_handler` 处理。(未应用 :ref:`retry_handler` 时，作为运行时异常处理。)

  此外，数据库连接错误的判定使用 :ref:`方言(Dialect) <database-dialect>` 。

SQL执行时的异常
  SQL执行失败时发生的异常，抛出 :java:extdoc:`SqlStatementException <nablarch.core.db.statement.exception.SqlStatementException>` 。

SQL执行时异常为唯一约束违反时的异常
  如果SQL执行时的异常表示唯一约束违反，则抛出 :java:extdoc:`DuplicateStatementException <nablarch.core.db.statement.exception.DuplicateStatementException>` 。

  如果要处理唯一约束违反，请参阅 :ref:`database-duplicated_error` 。

  此外，唯一约束违反的判定使用 :ref:`方言(Dialect) <database-dialect>` 。

.. tip::

  如果想更改数据库访问错误发生时的异常（例如想更细致地划分）等，
  请参阅 :ref:`database-change_exception` 。

.. _database-duplicated_error:

处理唯一约束违反并执行处理
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
需要在唯一约束违反时执行某些处理的情况下，请用 ``try-catch`` 捕获 :java:extdoc:`DuplicateStatementException <nablarch.core.db.statement.exception.DuplicateStatementException>` 并处理。

此外，唯一约束违反的判定使用 :ref:`方言(Dialect) <database-dialect>` 。

.. important::

  根据数据库产品不同，SQL执行时发生异常的情况下，在回滚完成前可能不接受任何SQL，请注意。
  对于此类产品，请考虑是否可以用其他方法替代。

  例如，如果在登记处理中发生唯一约束违反时想执行更新处理，
  不是进行异常处理，而是使用 `merge` 语句来规避此问题。

将处理时间较长的事务作为错误中断处理
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
通过事务管理实现。
详细内容请参阅 :ref:`transaction-timeout` 。

.. _database-new_transaction:

在与当前事务不同的事务中执行SQL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
有时不想使用数据库连接管理处理器和事务控制处理器启动的事务，
而是想使用单独的事务进行数据库访问。

例如，即使业务处理失败也想确保对数据库的更改时，
定义与当前事务不同的事务来访问数据库。

使用单独事务需要以下步骤。

#. 在组件配置文件中定义 :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>` 。
#. 从系统仓库获取 :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>` ，在新事务中执行SQL。
   （也可以不通过系统仓库获取，而是配置 :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>` 后使用）

以下展示使用示例。

组件配置文件
  在组件配置文件中定义 :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>` 。

  * :java:extdoc:`connectionFactory <nablarch.core.db.transaction.SimpleDbTransactionManager.setConnectionFactory(nablarch.core.db.connection.ConnectionFactory)>`
    属性中设置 :java:extdoc:`ConnectionFactory <nablarch.core.db.connection.ConnectionFactory>` 实现类。
    :java:extdoc:`ConnectionFactory <nablarch.core.db.connection.ConnectionFactory>` 实现类的详细内容，请参阅 :ref:`database-connect` 。

  * :java:extdoc:`transactionFactory <nablarch.core.db.transaction.SimpleDbTransactionManager.setTransactionFactory(nablarch.core.transaction.TransactionFactory)>`
    属性中设置 :java:extdoc:`TransactionFactory <nablarch.core.transaction.TransactionFactory>` 实现类。
    :java:extdoc:`TransactionFactory <nablarch.core.transaction.TransactionFactory>` 实现类的详细内容，请参阅 :ref:`transaction-database` 。

  .. code-block:: xml

    <component name="update-login-failed-count-transaction" class="nablarch.core.db.transaction.SimpleDbTransactionManager">
      <!-- connectionFactory属性中设置ConnectionFactory实现类 -->
      <property name="connectionFactory" ref="connectionFactory" />

      <!-- transactionFactory属性中设置TransactionFactory实现类 -->
      <property name="transactionFactory" ref="transactionFactory" />

      <!-- 设置用于识别事务的名称 -->
      <property name="dbTransactionName" value="update-login-failed-count-transaction" />

    </component>

实现示例
  使用组件配置文件中配置的 :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>` 执行SQL。
  此外，不要直接使用 :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>` ，而是使用控制事务的
  :java:extdoc:`SimpleDbTransactionExecutor<nablarch.core.db.transaction.SimpleDbTransactionExecutor>` 。

  .. code-block:: java

    // 从系统仓库获取SimpleDbTransactionManager
    SimpleDbTransactionManager dbTransactionManager =
        SystemRepository.get("update-login-failed-count-transaction");

    // 在构造函数中指定SimpleDbTransactionManager后执行
    SqlResultSet resultSet = new SimpleDbTransactionExecutor<SqlResultSet>(dbTransactionManager) {
      @Override
      public SqlResultSet execute(AppDbConnection connection) {
        SqlPStatement statement = connection.prepareStatementBySqlId(
            "jp.co.tis.sample.action.SampleAction#findUser");
        statement.setLong(1, userId);
        return statement.retrieve();
      }
    }.doTransaction();

.. _database-use_cache:

缓存搜索结果（想在相同SQL相同条件时使用缓存的数据）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
对于更新时间已确定的数据，或频繁访问但不必返回最新数据的情况，
可以通过缓存搜索结果来减轻数据库负载。

此功能可以在以下功能中有效利用。

* 如销售额排行榜那样，结果不必严格最新但被大量引用的数据
* 数据更新时机仅在夜间，白天不更新的数据

约束
  关于LOB类型
    获取LOB(BLOB类型或CLOB类型)的列时，获取的不是实际存储在DB中的数据，而是LOB定位器。
    获取实际值时，需要通过此LOB定位器获取。

    此LOB定位器的有效期限依赖于各RDBMS的实现。
    通常，在 :java:extdoc:`java.sql.ResultSet` 或 :java:extdoc:`java.sql.Connection` 关闭时将无法访问。
    因此，生存期限比 `ResultSet` 或 `Connection` 更长的缓存不能包含BLOB、CLOB类型。

  关于应用的冗余化
    默认提供的缓存保持组件在JVM的堆上保持缓存。
    因此，如果应用采用冗余化配置，搜索结果将在每个应用中缓存。

    因此，由于缓存时机不同，每个应用可能保持不同的缓存。

    如果应用服务器采用冗余化配置，并以轮询方式进行负载均衡，
    则可能每次访问不同的服务器。
    如果各服务器保持不同的缓存，则每次请求可能显示不同的结果，请注意。

.. important::

  此功能旨在当可以省略引用系数据库访问时进行省略，减轻系统负载，
  并非以数据库访问（SQL）高速化为目的。
  因此，不得以SQL高速化为目的使用。此类情况下，请进行SQL调优。

.. important::

  此功能不会监视数据库值的更新来更新缓存。
  因此，在必须始终显示最新数据的功能中不要使用。

以下展示使用示例。

组件配置文件
  按照以下步骤启用搜索结果缓存。

  #. 定义缓存查询结果的组件
  #. 每个SQLID的搜索结果缓存配置
  #. 定义缓存搜索结果的SQL执行组件

  查询结果缓存类的组件定义
    配置默认提供的缓存查询结果的类 :java:extdoc:`InMemoryResultSetCache <nablarch.core.db.cache.InMemoryResultSetCache>` 。

    .. code-block:: xml

      <component name="resultSetCache" class="nablarch.core.db.cache.InMemoryResultSetCache">
        <property name="cacheSize" value="100"/>
        <property name="systemTimeProvider" ref="systemTimeProvider"/>
      </component>

  每个SQLID的缓存配置
    配置每个SQLID的缓存。
    默认提供的 :java:extdoc:`BasicExpirationSetting <nablarch.core.cache.expirable.BasicExpirationSetting>` 可以设置每个SQLID的缓存有效期限。

    有效期限可以使用以下单位。

    :ms: 毫秒
    :sec: 秒
    :min: 分
    :h: 时

    .. code-block:: xml

      <!-- 缓存有效期限配置 -->
        <component name="expirationSetting"
            class="nablarch.core.cache.expirable.BasicExpirationSetting">

          <property name="expiration">
            <map>
              <!-- key中设置SQLID，value中设置有效期限 -->
              <entry key="please.change.me.tutorial.ss11AA.W11AA01Action#SELECT" value="100ms"/>
              <entry key="please.change.me.tutorial.ss11AA.W11AA02Action#SELECT" value="30sec"/>
            </map>
          </property>

        </component>

  缓存搜索结果的SQL执行组件的定义
    要使搜索结果缓存，需要在SQL执行组件的生成类中配置 :java:extdoc:`CacheableStatementFactory <nablarch.core.db.cache.statement.CacheableStatementFactory>` 。
    :java:extdoc:`CacheableStatementFactory <nablarch.core.db.cache.statement.CacheableStatementFactory>` 继承自默认提供的
    :java:extdoc:`BasicStatementFactory <nablarch.core.db.statement.BasicStatementFactory>` ，
    因此基本配置值与 :java:extdoc:`BasicStatementFactory <nablarch.core.db.statement.BasicStatementFactory>` 相同。

    :java:extdoc:`expirationSetting <nablarch.core.db.cache.statement.CacheableStatementFactory.setExpirationSetting(nablarch.core.cache.expirable.ExpirationSetting)>` 及
    :java:extdoc:`resultSetCache <nablarch.core.db.cache.statement.CacheableStatementFactory.setResultSetCache(nablarch.core.db.cache.ResultSetCache)>` 属性中，
    需要设置上述配置的查询结果缓存组件和每个SQLID的缓存配置组件。

    此处定义的 :java:extdoc:`CacheableStatementFactory <nablarch.core.db.cache.statement.CacheableStatementFactory>` 组件，需要在
    :ref:`database-connect` 中定义的数据库连接获取组件中进行配置。

    .. code-block:: xml

      <!-- 配置生成可缓存语句的CacheableStatementFactory -->
      <component name="cacheableStatementFactory"
                 class="nablarch.core.db.cache.CacheableStatementFactory">

        <!-- 有效期限配置 -->
        <property name="expirationSetting" ref="expirationSetting"/>
        <!-- 缓存实现 -->
        <property name="resultSetCache" ref="resultSetCache"/>

      </component>

  实现示例
    使用SQL的数据库访问，无论是否有缓存都不会改变。
    按照以下方式实现即可。

    * :ref:`database-execute_sqlid`
    * :ref:`database-input_bean`

使用`java.sql.Connection`进行处理
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
有时想处理JDBC的原生数据库连接( :java:extdoc:`java.sql.Connection` )。
例如，想使用 :java:extdoc:`java.sql.DatabaseMetaData` 就属于这种情况。

这种情况下，可以从 :java:extdoc:`DbConnectionContext <nablarch.core.db.connection.DbConnectionContext>` 获取的
:java:extdoc:`TransactionManagerConnection <nablarch.core.db.connection.TransactionManagerConnection>` 中获取 :java:extdoc:`java.sql.Connection` 来应对。

.. important::

  使用 :java:extdoc:`java.sql.Connection` 时，需要处理作为检查异常的 :java:extdoc:`java.sql.SQLException` 来控制异常。
  如果此异常控制实现错误，可能会发生故障未被发现或故障时无法调查等问题。
  因此，除非没有必须使用 :java:extdoc:`java.sql.Connection` 无法满足的需求，否则不要使用此功能。

以下展示示例。

.. code-block:: java

  TransactionManagerConnection managerConnection = DbConnectionContext.getTransactionManagerConnection();
  Connection connection = managerConnection.getConnection();
  return connection.getMetaData();
    

.. _database-replace_schema:
  
按环境切换SQL文中的模式(schema)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

当仅想引用特定SQL（表）的其他模式时，通常会在SQL文中明确记述模式
(例: ``SELECT * FROM A_SCHEMA.TABLE1``)，但根据环境不同，想引用的模式名可能不同（请参阅以下示例）。

**TABLE1的引用目标模式**

=================== ==========
环境                模式
=================== ==========
生产环境            A_SCHEMA
测试环境            B_SCHEMA
=================== ==========

在这种情况下，无法在SQL文中明确记述模式名的方法。

.. code-block:: sql

  -- 指定模式名进行SELECT
  SELECT * FROM A_SCHEMA.TABLE1  -- 在生产环境中运行但在测试环境中不运行

  
为此类情况提供按环境切换SQL文中模式的功能。

首先，在SQL文中记述用于替换模式的占位符 ``#SCHEMA#`` \ [#schema]_\ 。


.. code-block:: sql
                
  -- 指定模式名进行SELECT
  SELECT * FROM #SCHEMA#.TABLE1


.. [#schema] 此占位符的字符串是固定的。


为了替换占位符，像以下示例一样配置\
:java:extdoc:`BasicSqlLoader <nablarch.core.db.statement.BasicSqlLoader>` 。

.. code-block:: xml
                
  <component name="statementFactory" class="nablarch.core.db.statement.BasicStatementFactory">
    <property name="sqlLoader">
      <component name="sqlLoader" class="nablarch.core.db.statement.BasicSqlLoader">
        <property name="sqlLoaderCallback">
          <list>
            <!-- 将SQL文中的#SCHEMA#替换为指定值 -->
            <component class="nablarch.core.db.statement.sqlloader.SchemaReplacer">
              <property name="schemaName" value="${nablarch.schemaReplacer.schemaName}"/>
            </component>
          </list>
        </property>
      </component>
    </property>
  </component>

将占位符替换为何种值，
在 :java:extdoc:`SchemaReplacer <nablarch.core.db.statement.sqlloader.SchemaReplacer>`
的属性\ ``schemaName``\ 中进行配置。
上述示例中，将替换后的值设置为环境依赖值 ``nablarch.schemaReplacer.schemaName`` 。\
通过按环境切换此值，\
可以将SQL文中的模式替换为适应该环境的值\
（切换方法的详细内容请参阅 :ref:`how_to_switch_env_values` ）。

.. tip::
   此功能对SQL文中的模式替换是简单的字符串替换处理，\
   不会检查模式是否存在或模式替换后的SQL是否妥当等\
   （在SQL文执行时会报错）。

扩展示例
--------------------------------------------------

.. _database-add_connection_factory:

添加数据库连接方法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
说明添加数据库连接方法的步骤。
例如，使用OSS连接池库等情况时，按照此步骤操作即可。

#. 继承 :java:extdoc:`ConnectionFactorySupport <nablarch.core.db.connection.ConnectionFactorySupport>` ，创建生成数据库连接的类。
#. 将创建的类配置在组件配置文件中。( 请参阅 :ref:`database-connect` )

.. _database-add_dialect:

添加方言(Dialect)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
说明添加方言(Dialect)的步骤。

例如，如果没有与使用数据库产品对应的方言(Dialect)，或想切换特定功能的使用与否时，需要添加方言(Dialect)。

#. 继承 :java:extdoc:`DefaultDialect <nablarch.core.db.dialect.DefaultDialect>` ，创建与数据库产品对应的方言(Dialect)。
#. 将创建的方言(Dialect)配置在组件配置文件中 ( 请参阅 :ref:`database-use_dialect` )

.. _database-change_exception:

切换数据库访问时的异常类
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
说明切换数据库访问时异常类的步骤。

例如，想更改死锁错误的异常类时，按照此步骤操作即可。

#. 创建生成数据库访问错误的 :java:extdoc:`DbAccessExceptionFactory <nablarch.core.db.connection.DbAccessExceptionFactory>` 的实现类。
#. 创建生成SQL执行时错误的 :java:extdoc:`SqlStatementExceptionFactory <nablarch.core.db.statement.SqlStatementExceptionFactory>` 的实现类。
#. 在组件配置文件中定义创建的类。

以下展示详细步骤。

创建 :java:extdoc:`DbAccessExceptionFactory <nablarch.core.db.connection.DbAccessExceptionFactory>` 的实现类
  如果想更改获取数据库连接时及事务控制时(commit或rollback)发生的 :java:extdoc:`DbAccessException <nablarch.core.db.DbAccessException>` ，
  请创建此接口的实现类。

创建 :java:extdoc:`SqlStatementExceptionFactory <nablarch.core.db.statement.SqlStatementExceptionFactory>` 的实现类
  如果想更改SQL执行时发生的 :java:extdoc:`SqlStatementException <nablarch.core.db.statement.exception.SqlStatementException>` ，请创建此接口的实现类。

在组件配置文件中定义
  :java:extdoc:`DbAccessExceptionFactory <nablarch.core.db.connection.DbAccessExceptionFactory>` 的实现类，需要在 :ref:`database-connect`
  中定义的数据库连接获取组件中进行配置。

  .. code-block:: xml

    <component class="sample.SampleDbAccessExceptionFactory" />

  :java:extdoc:`SqlStatementExceptionFactory <nablarch.core.db.statement.SqlStatementExceptionFactory>` 的实现类，需要对 :java:extdoc:`BasicStatementFactory <nablarch.core.db.statement.BasicStatementFactory>` 进行配置。
  此外，:java:extdoc:`BasicStatementFactory <nablarch.core.db.statement.BasicStatementFactory>` 需要在 :ref:`database-connect` 中定义的数据库连接获取组件中进行配置。

  .. code-block:: xml

    <component name="statementFactory" class="nablarch.core.db.statement.BasicStatementFactory">
      <property name="sqlStatementExceptionFactory">
        <component class="sample.SampleStatementExceptionFactory" />
      </property>
    </component>
