.. _universal_dao:

通用DAO
=====================================================================

.. contents:: 目录
   :depth: 3
   :local:

通用DAO提供使用 `Jakarta Persistence (外部站点，英语) <https://jakarta.ee/specifications/persistence/>`_
注解的简易O/R映射器。

由于通用DAO内部使用 :ref:`database` ，
因此使用通用DAO需要 :ref:`database` 的配置。

.. tip::
 通用DAO定位为简易O/R映射器，
 并不考虑用通用DAO实现所有的数据库访问。
 如果通用DAO无法实现，请直接使用 :ref:`database` 。

 例如，通用DAO无法执行主键以外条件指定的更新/删除，
 因此需要使用 :ref:`database` 。

.. tip::

  通用DAO不提供对通用字段（所有表中定义的登记用户和更新用户等）值的自动设置功能。
  如果要对通用字段自动设置值，可以应用 :ref:`doma_adaptor` ，使用Doma的实体监听器功能。

  如果无论如何都想使用通用DAO，请在通用DAO功能使用前在应用程序中明确设置通用字段。

.. _universal_dao-spec:

功能概述
---------------------------------------------------------------------

.. _universal_dao-execute_crud_sql:

无需编写SQL即可执行简单CRUD
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
只需在Entity上添加Jakarta Persistence注解，无需编写SQL，即可执行以下简单CRUD。
SQL语句根据Jakarta Persistence注解在运行时构建。

* 登记/批量登记
* 指定主键的更新/批量更新
* 指定主键的删除/批量删除
* 指定主键的搜索

Entity可用的Jakarta Persistence注解，请参阅 :ref:`universal_dao_jpa_annotations` 。


.. tip::
   通用DAO的上述CRUD功能中，可以使用\ ``@Table``\ 注解指定模式（schema）\
   （请参阅 :ref:`universal_dao_jpa_annotations` ）。
   但是，:ref:`database` 的 :ref:`database-replace_schema` 功能在通用DAO的上述CRUD功能中无法使用。\
   对于按环境切换模式的用途，请使用 :ref:`database` 而不是通用DAO。
   
.. _universal_dao-bean_mapping:

可以将搜索结果映射到Bean
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
搜索时，与 :ref:`database` 一样，可以创建SQL文件并指定SQL ID进行搜索。
此外，通用DAO中可以将搜索结果映射到Bean（Entity、Form、DTO）后获取。
Bean的属性名与SELECT句名称匹配的项目将被映射。

Bean可用的数据类型，请参阅 :ref:`universal_dao_bean_data_types` 。

模块列表
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-dao</artifactId>
  </dependency>

使用方法
---------------------------------------------------------------------

.. important::
 通用DAO的基本使用方法，请参阅 :java:extdoc:`nablarch.common.dao.UniversalDao` 。

进行使用通用DAO所需的配置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
要使用通用DAO，除了 :ref:`database` 的配置外，
还需要在组件定义中添加 :java:extdoc:`BasicDaoContextFactory <nablarch.common.dao.BasicDaoContextFactory>` 的配置。

.. code-block:: xml

 <!-- 组件名请设置为"daoContextFactory"。 -->
 <component name="daoContextFactory" class="nablarch.common.dao.BasicDaoContextFactory" />

.. _universal_dao-sql_file:

使用任意SQL（SQL文件）进行搜索
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
想用任意SQL搜索时，与数据库访问的 :ref:`database-use_sql_file` 一样，
创建SQL文件并指定SQL ID进行搜索。

.. code-block:: java

 UniversalDao.findAllBySqlFile(User.class, "FIND_BY_NAME");

SQL文件从用于映射搜索结果的Bean推导。
如果上述User.class为sample.entity.User，
则SQL文件路径为类路径下的sample/entity/User.sql。

如果SQL ID包含"#"，则解释为"SQL文件路径#SQL ID"。
以下示例中，SQL文件路径为类路径下的sample/entity/Member.sql，
SQL ID为FIND_BY_NAME。

.. code-block:: java

 UniversalDao.findAllBySqlFile(GoldUser.class, "sample.entity.Member#FIND_BY_NAME");

.. tip::
 包含"#"的指定可以在想按功能单位（Action处理器单位）集中SQL等情况下使用。
 但是，由于指定会变得复杂，因此基本请使用不包含"#"的指定。

.. _universal_dao-join:

获取JOIN多表后的搜索结果
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
在列表搜索等情况下，有时想获取JOIN多个表后的结果。
此类情况下，为了效率，不要分别搜索JOIN对象的数据，
而是创建 **1次即可搜索的SQL** 和 **映射JOIN结果的Bean** 。

.. _universal_dao-lazy_load:

延迟加载搜索结果
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
处理大量搜索结果时，由于内存不足，无法将所有搜索结果展开到内存中。
存在以下情况。

* 在Web中下载大量数据
* 在批处理中处理大量数据

此类情况下，请使用通用DAO的延迟加载。
使用延迟加载后，通用DAO虽然逐条加载，
但内存使用量会根据JDBC的提取大小(fetch size)而变化。
提取大小的详细内容，请参阅数据库供应商提供的手册。

延迟加载只需在搜索时先调用 :java:extdoc:`UniversalDao#defer <nablarch.common.dao.UniversalDao.defer()>` 方法即可使用。
由于延迟加载内部使用服务器端游标，
因此需要调用 :java:extdoc:`DeferredEntityList#close <nablarch.common.dao.DeferredEntityList.close()>` 方法。

.. code-block:: java

 // 使用try-with-resources调用close。
 // DeferredEntityList通过向下转型获取。
 try (DeferredEntityList<User> users
         = (DeferredEntityList<User>) UniversalDao.defer()
                                         .findAllBySqlFile(User.class, "FIND_BY_NAME")) {
     for (User user : users) {
         // 使用user进行处理
     }
 }

.. important::
   根据使用的RDBMS不同，游标打开期间进行事务控制可能会关闭游标。
   因此，如果在使用延迟加载处理大量数据期间进行事务控制，可能会引用已关闭的游标而导致错误，请注意。
   请按照数据库供应商提供的手册调整游标行为，或通过 :ref:`分页<universal_dao-paging>` 等方式避免处理大量数据。

.. _universal_dao-search_with_condition:

指定条件进行搜索
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
通用DAO也提供了像搜索画面那样指定条件的搜索。

.. code-block:: java

 // 获取搜索条件
 ProjectSearchForm condition = context.getRequestScopedVar("form");

 // 指定条件进行搜索
 List<Project> projects = UniversalDao.findAllBySqlFile(
     Project.class, "SEARCH_PROJECT", condition);

.. important::
  搜索条件请指定带有搜索条件的专用Bean，而不是Entity。
  但是，仅访问1个表时，也可以指定Entity。


类型转换
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

通用DAO可以使用 :ref:`@Temporal <universal_dao_jpa_temporal>` 指定 ``java.util.Date`` 及 ``java.util.Calendar`` 类型的值如何映射到数据库。
其他类型无法进行任意映射，因此Entity的属性请根据数据库类型及使用的JDBC驱动规范定义。

此外，通用DAO在将自动生成的SQL发送到DB时使用Jakarta Persistence注解的信息，但在将任意SQL发送到DB时不使用Jakarta Persistence注解的信息。
因此，类型转换如下所示。

:ref:`执行Entity自动生成的SQL时 <universal_dao-execute_crud_sql>`
  向数据库输出时
    * 对于设置了 :ref:`@Temporal <universal_dao_jpa_temporal>` 的属性，转换为@Temporal指定的类型。
    * 上述以外的情况，委托给 :ref:`database` 进行转换。

  从数据库获取时
    * 对于设置了 :ref:`@Temporal <universal_dao_jpa_temporal>` 的属性，从@Temporal指定的类型转换。
    * 上述以外的情况根据Entity的信息转换值。

:ref:`使用任意SQL搜索时 <universal_dao-sql_file>`
  向数据库输出时
    * 委托给 :ref:`database` 进行转换。

  从数据库获取时
    * 执行与Entity自动生成SQL时相同的处理。


.. important::
  如果数据库类型与属性类型不一致，执行时可能会发生类型转换错误。
  此外，SQL执行时可能会进行隐式类型转换，导致性能下降（由于不使用索引）。

  关于数据库与Java数据类型的映射，由于依赖于使用的产品，
  请参阅JDBC驱动手册。

  例如，DB为date型时，大多数数据库中属性类型为 :java:extdoc:`java.sql.Date` 。
  此外，DB为数值型(integer、bigint、number等)时，属性类型为
  `int` (:java:extdoc:`java.lang.Integer`) 或 `long` (:java:extdoc:`java.lang.Long`) 。


.. _universal_dao-paging:

进行分页
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
通用DAO的搜索支持分页。
分页只需在搜索时先调用 :java:extdoc:`UniversalDao#per <nablarch.common.dao.UniversalDao.per(long)>` 方法、:java:extdoc:`UniversalDao#page <nablarch.common.dao.UniversalDao.page(long)>` 方法即可使用。

.. code-block:: java

 EntityList<User> users = UniversalDao.per(3).page(1)
                             .findAllBySqlFile(User.class, "FIND_ALL_USERS");

分页画面显示所需的搜索结果件数等信息，由 :java:extdoc:`Pagination <nablarch.common.dao.Pagination>` 保持。
:java:extdoc:`Pagination <nablarch.common.dao.Pagination>` 可以从 :java:extdoc:`EntityList <nablarch.common.dao.EntityList>` 获取。

.. code-block:: java

 Pagination pagination = users.getPagination();

.. tip::
  分页用的搜索处理，使用 :ref:`数据库访问(JDBC包装器)的范围指定搜索功能 <database-paging>` 执行。

.. tip::
  分页中，在实际的范围指定记录获取处理之前，会发行件数获取SQL。
  如果由于件数获取SQL导致性能下降等情况，请根据需要参考 :ref:`universal_dao-customize_sql_for_counting` 更改件数获取SQL。

.. _universal_dao-generate_surrogate_key:

生成代理键
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. toctree::
  :maxdepth: 1
  :hidden:

  generator

生成代理键时，使用以下注解。

* :ref:`@GeneratedValue <universal_dao_jpa_generated_value>`
* :ref:`@SequenceGenerator <universal_dao_jpa_sequence_generator>`
* :ref:`@TableGenerator <universal_dao_jpa_table_generator>`

通用DAO支持 :java:extdoc:`jakarta.persistence.GenerationType` 的所有策略。

GenerationType.AUTO
 \

 .. code-block:: java

  @Id
  @Column(name = "USER_ID", length = 15)
  @GeneratedValue(strategy = GenerationType.AUTO)
  public Long getId() {
      return id;
  }

 - 根据数据库功能中配置的 :java:extdoc:`Dialect <nablarch.core.db.dialect.Dialect>` 选择编号方法。
   优先级为，IDENTITY→SEQUENCE→TABLE的顺序。
 - 选择SEQUENCE时，序列(sequence)对象名为"<表名>_<编号列名>"。
 - 如果想指定序列(sequence)对象名，请在 :ref:`@SequenceGenerator <universal_dao_jpa_sequence_generator>` 中指定。

GenerationType.IDENTITY
 \

 .. code-block:: java

  @Id
  @Column(name = "USER_ID", length = 15)
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  public Long getId() {
      return id;
  }

GenerationType.SEQUENCE
 \

 .. code-block:: java

  @Id
  @Column(name = "USER_ID", length = 15)
  @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "seq")
  @SequenceGenerator(name = "seq", sequenceName = "USER_ID_SEQ")
  public Long getId() {
      return id;
  }

 - 序列(sequence)对象名在 :ref:`@SequenceGenerator <universal_dao_jpa_sequence_generator>` 中指定。
 - 省略sequenceName属性时，变为"<表名>_<编号列名>"。

GenerationType.TABLE
 \

 .. code-block:: java

  @Id
  @Column(name = "USER_ID", length = 15)
  @GeneratedValue(strategy = GenerationType.TABLE, generator = "table")
  @TableGenerator(name = "table", pkColumnValue = "USER_ID")
  public Long getId() {
      return id;
  }

 - 用于识别记录的值在 :ref:`@TableGenerator <universal_dao_jpa_table_generator>` 中指定。
 - 省略pkColumnValue属性时，变为"<表名>_<编号列名>"。

.. tip::

  使用序列(sequence)及表的代理键编号处理，使用 :ref:`generator` 执行。
  配置值（使用表时的表名和列名配置等），请参阅链接目标。

.. _universal_dao-batch_execute:

执行批处理（批量登记、更新、删除）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
通用DAO中，可以在大量数据批量登记、更新、删除时执行批处理。
通过执行批处理，可以减少应用运行服务器与数据库服务器之间的往返次数，有望提高性能。

批处理使用以下方法。

* :java:extdoc:`batchInsert <nablarch.common.dao.UniversalDao.batchInsert(java.util.List)>`
* :java:extdoc:`batchUpdate <nablarch.common.dao.UniversalDao.batchUpdate(java.util.List)>`
* :java:extdoc:`batchDelete <nablarch.common.dao.UniversalDao.batchDelete(java.util.List)>`

.. important::

  使用 `batchUpdate` 的批量更新处理中不进行并发控制处理。
  如果更新对象Entity与数据库版本不一致，该记录的更新将不会执行而正常结束。

  需要并发控制的更新处理中，请调用非批量更新而是每1条记录的更新处理。

.. _`universal_dao_jpa_optimistic_lock`:

执行乐观锁
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
通用DAO中，更新带有 :ref:`@Version <universal_dao_jpa_version>`
的Entity时，自动执行乐观锁。
乐观锁发生排他错误时，抛出 :java:extdoc:`jakarta.persistence.OptimisticLockException` 。

.. important::
  :ref:`@Version <universal_dao_jpa_version>` 只能指定在数值型的属性上。
  字符串型的属性无法正确动作。

排他错误时的画面迁移，使用 :java:extdoc:`OnError <nablarch.fw.web.interceptor.OnError>` 执行。

.. code-block:: java

 // type属性中指定目标异常，path属性中指定迁移目标路径。
 @OnError(type = OptimisticLockException.class,
          path = "/WEB-INF/view/common/errorPages/userError.jsp")
 public HttpResponse update(HttpRequest request, ExecutionContext context) {

     UniversalDao.update(user); // 省略前后处理。

 }

.. important::
  如 :ref:`universal_dao-batch_execute` 所述，
  批量更新处理(`batchUpdate`)中无法使用乐观锁，请注意。

.. _`universal_dao_jpa_pessimistic_lock`:

执行悲观锁
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
通用DAO中，特别不提供悲观锁功能。

悲观锁通过使用数据库的行锁（select for update）执行。
记载行锁（select for update）的SQL，
使用 :java:extdoc:`UniversalDao#findBySqlFile <nablarch.common.dao.UniversalDao.findBySqlFile(java.lang.Class,java.lang.String,java.lang.Object)>` 方法执行。

并发控制思路
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
并发控制使用的版本列定义在哪个表中，需要根据业务观点决定。

持有版本号的表，按进行并发控制的单位定义，在业务上允许的竞争最大单位中定义。
例如，如果业务上允许以"用户"这样的大单位进行锁定，则在用户表中定义版本号。
但是，请注意单位越大，竞争的可能性越高，会导致更新失败（乐观锁的情况）或处理延迟（悲观锁的情况）。


登记（更新）数据尺寸较大的二进制数据
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
有时想登记（更新）像Oracle的BLOB那样数据尺寸较大的二进制数据。
通用DAO中，必须将数据全部展开到内存后才能登记（更新），
因此请使用数据库提供的功能从文件等直接登记（更新）。

详细内容，请参阅 :ref:`database-binary_column` 。

登记（更新）数据尺寸较大的文本数据
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
有时想登记（更新）像Oracle的CLOB那样数据尺寸较大的文本数据。
通用DAO中，必须将数据全部展开到内存后才能登记（更新），
因此请使用数据库提供的功能从文件等直接登记（更新）。

详细内容，请参阅 :ref:`database-clob_column` 。

.. _universal_dao-transaction:

在与当前事务不同的事务中执行
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
说明在通用DAO中执行与 :ref:`database` 的 :ref:`database-new_transaction` 相同处理的方法。

使用单独事务需要以下步骤。

#. 在组件配置文件中定义 :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>` 。
#. 使用 :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>` ，在新事务中执行通用DAO。

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

    <component name="find-persons-transaction"
        class="nablarch.core.db.transaction.SimpleDbTransactionManager">

      <!-- connectionFactory属性中设置ConnectionFactory实现类 -->
      <property name="connectionFactory" ref="connectionFactory" />

      <!-- transactionFactory属性中设置TransactionFactory实现类 -->
      <property name="transactionFactory" ref="transactionFactory" />

      <!-- 设置用于识别事务的名称 -->
      <property name="dbTransactionName" value="update-login-failed-count-transaction" />

    </component>

实现示例
  使用组件配置文件中配置的 :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>` 执行通用DAO。
  此外，不要直接使用 :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>` ，而是使用控制事务的
  :java:extdoc:`UniversalDao.Transaction <nablarch.common.dao.UniversalDao.Transaction>` 。

  首先，创建继承 :java:extdoc:`UniversalDao.Transaction <nablarch.common.dao.UniversalDao.Transaction>` 的类。

  .. code-block:: java

    private static final class FindPersonsTransaction extends UniversalDao.Transaction {

        // 准备接收结果的容器。
        private EntityList<Person> persons;

        FindPersonsTransaction() {
            // 在super()中指定SimpleDbTransactionManager。
            // 可以指定组件定义中指定的名称或SimpleDbTransactionManager对象。
            // 此示例中指定的是组件定义中指定的名称。
            super("find-persons-transaction");
        }

        // 此方法自动在别的事务中执行。
        // 正常处理结束时事务将提交，
        // 抛出异常或错误时，事务将回滚。
        @Override
        protected void execute() {
            // 在execute方法中实现使用UniversalDao的处理。
            persons = UniversalDao.findAllBySqlFile(Person.class, "FIND_PERSONS");
        }

        // 准备返回结果的getter。
        public EntityList<Person> getPersons() {
            return persons;
        }
    }

  然后，调用继承 :java:extdoc:`UniversalDao.Transaction <nablarch.common.dao.UniversalDao.Transaction>` 的类。

  .. code-block:: java

    // 生成后将在别的事务中执行。
    FindPersonsTransaction findPersonsTransaction = new FindPersonsTransaction();

    // 获取结果。
    EntityList<Person> persons = findPersonsTransaction.getPersons();


扩展示例
---------------------------------------------------------------------

无法从DatabaseMetaData获取信息时的对应
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
根据数据库不同，使用同义词时或由于权限问题，
可能无法从 :java:extdoc:`java.sql.DatabaseMetaData` 获取主键信息。
如果无法获取主键信息，指定主键的搜索将无法正确动作。
此类情况下，请创建继承 :java:extdoc:`DatabaseMetaDataExtractor <nablarch.common.dao.DatabaseMetaDataExtractor>` 的类进行对应。
如何获取主键信息依赖于数据库，请参阅产品手册。

使用创建的类需要进行配置。

.. code-block:: xml

 <!--
 创建sample.dao.CustomDatabaseMetaDataExtractor时的配置示例
 组件名请设置为"databaseMetaDataExtractor"。
 -->
 <component name="databaseMetaDataExtractor" class="sample.dao.CustomDatabaseMetaDataExtractor" />

.. _universal_dao-customize_sql_for_counting:

更改分页处理的件数获取用SQL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:ref:`分页 <universal_dao-paging>` 处理中，在实际的范围指定记录获取处理之前，会发行件数获取SQL。
件数获取SQL默认是将原SQL用 ``SELECT COUNT(*) FROM`` 包裹后的SQL。
如果原SQL包含 ``ORDER BY`` 句等处理负荷较大的SQL，为减轻负荷想去除 ``ORDER BY`` 句等情况时，
可以通过自定义使用的方言(Dialect)，更改件数获取SQL来对应。

.. important::
   件数获取SQL必须与原文SQL具有相同的搜索条件。准备件数获取SQL时，请注意两者的搜索条件不要产生差异。

更改件数获取SQL时，请继承项目中使用的方言(Dialect)，更改 :java:extdoc:`Dialect#convertCountSql(String, Object, StatementFactory) <nablarch.core.db.dialect.Dialect.convertCountSql(java.lang.String,java.lang.Object,nablarch.core.db.statement.StatementFactory)>` 的实现。

实现示例
   以下展示自定义 :java:extdoc:`nablarch.core.db.dialect.H2Dialect` 的示例。
   此示例中，将原SQL与件数获取SQL的映射配置到组件中，更改件数获取SQL。

   .. tip::
      请按项目研讨适当的映射规则。
   
   .. code-block:: java
   
      public class CustomH2Dialect extends H2Dialect {
      
          /**
           * 件数获取SQL的映射
           */
          private Map<String, String> sqlMap;
      
          /**
           * {@inheritDoc}
           *
           * 如果件数获取SQL的映射中存在与{@code sqlId}对应的SQLID，
           * 则将其作为件数获取SQL返回。
           */
          @Override
          public String convertCountSql(String sqlId, Object params, StatementFactory statementFactory) {
      
              if (sqlMap.containsKey(sqlId)) {
                  return statementFactory.getVariableConditionSqlBySqlId(sqlMap.get(sqlId), params);
              }
      
              return convertCountSql(statementFactory.getVariableConditionSqlBySqlId(sqlId, params));
          }
      
          /**
           * 设置件数获取SQL的映射。
           *
           * @param sqlMap 件数获取SQL的映射
           */
          public void setSqlMap(Map<String, String> sqlMap){
              this.sqlMap = sqlMap;
          }
      }

   自定义的方言(Dialect)需要在组件配置文件中配置。
   以下展示将自定义的方言(Dialect)配置到组件配置文件中的示例。
   此示例中，通过 ``<property>`` 元素设置件数获取SQL的映射。
   
   .. code-block:: xml
                   
      <component name="dialect" class="com.nablarch.example.app.db.dialect.CustomH2Dialect">
        <property name="sqlMap">
          <map>
            <entry key="com.nablarch.example.app.entity.Project#SEARCH_PROJECT"
                   value="com.nablarch.example.app.entity.Project#SEARCH_PROJECT_FORCOUNT"/>
          </map>
        </property>
      </component>

.. _`universal_dao_jpa_annotations`:

Entity可用的Jakarta Persistence注解
---------------------------------------------------------------------
Entity可用的Jakarta Persistence注解如下。

* 设置在类上的注解

  * :ref:`@Entity <universal_dao_jpa_entity>`
  * :ref:`@Table <universal_dao_jpa_table>`
  * :ref:`@Access <universal_dao_jpa_access>`
* 设置在getter或字段上的注解

  * :ref:`@Column <universal_dao_jpa_column>`
  * :ref:`@Id <universal_dao_jpa_id>`
  * :ref:`@Version <universal_dao_jpa_version>`
  * :ref:`@Temporal <universal_dao_jpa_temporal>`
  * :ref:`@GeneratedValue <universal_dao_jpa_generated_value>`
  * :ref:`@SequenceGenerator <universal_dao_jpa_sequence_generator>`
  * :ref:`@TableGenerator <universal_dao_jpa_table_generator>`

.. important::
 使用此处未记述的注解及属性将无法动作。

设置在字段上时，请通过@Access明确指定。@Access明确指定时，才引用字段的注解。

即使设置在字段上，UniversalDao中值的获取和设置也通过属性进行，因此getter和setter请务必创建。

字段和属性通过名称关联，如果名称不同，则无法通过属性引用字段的注解。
因此字段名和属性名（get〇〇、set〇〇的〇〇部分）请务必设为相同。

.. tip::
 例如，使用Lombok等生成样板代码的库时，
 通过将注解设置在字段上，可以无需自己创建getter，
 更好地发挥库的优势。

.. _`universal_dao_jpa_entity`:

*jakarta.persistence.Entity*
 设置在对应数据库表的Entity类上的注解。

 设置此注解后，从类名推导表名。
 类名（帕斯卡命名法）转换为蛇形命名法（全部大写）后的值即为表名。

 .. code-block:: bash

  Book类        -> BOOK
  BookAuthor类  -> BOOK_AUTHOR

 .. tip::
  如果无法从类名推导表名，
  请使用后述的 :ref:`@Table <universal_dao_jpa_table>` 明确指定表名。

.. _`universal_dao_jpa_table`:

*jakarta.persistence.Table*
 用于指定表名的注解。

 name属性中指定值时，该值将作为表名使用。
 schema属性中指定值时，将使用指定的模式名作为限定符访问表。
 例如，schema属性中指定work，表名为users_work时，将访问work.users_work。

.. _`universal_dao_jpa_access`:

*jakarta.persistence.Access*
 用于指定注解设置位置的注解。

 仅明确指定在字段上时，才引用字段的注解。

.. _`universal_dao_jpa_column`:

*jakarta.persistence.Column*
 用于指定列名的注解。

 name属性中指定值时，该值将作为列名使用。

 .. tip::
  如果未设置此注解，则从属性名推导列名。
  推导方法与表名的推导方法相同。
  详细内容请参阅 :ref:`@Entity <universal_dao_jpa_entity>` 。

.. _`universal_dao_jpa_id`:

*jakarta.persistence.Id*
 设置在主键上的注解。

 复合主键时，在多个getter或字段上设置此注解。

.. _`universal_dao_jpa_version`:

*jakarta.persistence.Version*
 设置在并发控制使用的版本列上的注解。

 此注解只能指定在数值型的属性上。
 字符串型的属性无法正确动作。

 设置此注解后，
 更新处理时版本列将自动添加到条件中执行乐观锁。

 .. tip::
  此注解在Entity内只能指定1个。

.. _`universal_dao_jpa_temporal`:

*jakarta.persistence.Temporal*
 指定 *java.util.Date* 及 *java.util.Calendar* 类型的值
 如何映射到数据库的注解。

 将Java对象的值转换为value属性中指定的数据库类型后登记到数据库。

.. _`universal_dao_jpa_generated_value`:

*jakarta.persistence.GeneratedValue*
 表示登记自动编号的值的注解。

 strategy属性中设置编号方法。
 设置为AUTO时，按照以下规则选择编号方法。

 * 如果generator属性有对应的Generator配置，则使用该Generator执行编号处理。
 * 如果generator未设置或没有对应的Generator配置，
   则根据数据库功能中配置的 :java:extdoc:`Dialect <nablarch.core.db.dialect.Dialect>` 选择编号方法。
   优先级为，IDENTITY→SEQUENCE→TABLE的顺序。

 generator属性中设置任意名称。

 .. tip::
  使用 :ref:`@GeneratedValue <universal_dao_jpa_generated_value>` 时，
  如果无法获取序列(sequence)编号的序列(sequence)对象名或
  表编号的用于识别记录的值，
  则从表名和自动编号的列名推导这些值。

  .. code-block:: bash

   表名「USER」、编号列名「ID」  -> USER_ID

.. _`universal_dao_jpa_sequence_generator`:

*jakarta.persistence.SequenceGenerator*
 使用序列(sequence)编号时设置的注解。

 name属性中，设置与 :ref:`@GeneratedValue <universal_dao_jpa_generated_value>`
 的generator属性相同的值。

 sequenceName属性中，设置在数据库上创建的序列(sequence)对象名。

 .. tip::
  序列(sequence)编号使用编号功能执行。
  因此，需要另行进行 :ref:`编号用配置 <generator_dao_setting>` 。

.. _`universal_dao_jpa_table_generator`:

*jakarta.persistence.TableGenerator*
 使用表编号时设置的注解。

 name属性中，设置与 :ref:`@GeneratedValue <universal_dao_jpa_generated_value>`
 的generator属性相同的值。

 pkColumnValue属性中，设置用于识别编号表记录的值的。

 .. tip::
  表编号使用编号功能执行。
  因此，需要另行进行 :ref:`编号用配置 <generator_dao_setting>` 。

.. _`universal_dao_bean_data_types`:

Bean可用的数据类型
---------------------------------------------------------------------
映射搜索结果的Bean可用的数据类型如下。

.. important::
 对于此处未记述的数据类型，无法映射搜索结果（将成为运行时异常）。

*java.lang.String*
 \

*java.lang.Short*
 也可以使用基本类型。基本类型时， ``null`` 作为 ``0`` 处理。

*java.lang.Integer*
 也可以使用基本类型。基本类型时， ``null`` 作为 ``0`` 处理。

*java.lang.Long*
 也可以使用基本类型。基本类型时， ``null`` 作为 ``0`` 处理。

*java.math.BigDecimal*
 \

*java.lang.Boolean*
 也可以使用基本类型。基本类型时， ``null`` 作为 ``false`` 处理。
 包装类型(Boolean)时，读取方法名需要从get开始。
 基本类型时，读取方法名从is开始也可以。

*java.util.Date*
 需要使用Jakarta Persistence的 :ref:`@Temporal <universal_dao_jpa_temporal>`
 指定数据库上的数据类型。


*java.sql.Date*
 \

*java.sql.Timestamp*
 \

*java.time.LocalDate*
 \

*java.time.LocalDateTime*
 \

*byte[]*
  像BLOB那样非常大尺寸的数据类型的值，
  请注意不要使用本功能将数据展开到堆上。
  处理非常大尺寸的二进制数据时，
  请直接使用数据库访问，通过Stream引用数据。

  详细内容请参阅 :ref:`database-binary_column` 。
