.. _doma_adaptor:

Doma适配器
==================================================

.. contents:: 目录
  :depth: 3
  :local:

提供用于使用 `Doma2(外部网站) <https://doma.readthedocs.io/ja/latest/>`_ 进行数据库访问的适配器。

使用Doma进行数据库访问可以获得以下好处。

* 与Nablarch一样，可以在运行时动态构建SQL语句。
* 由于是2waySQL，无需像Nablarch那样重写SQL语句，可以直接在SQL工具等中执行。

此外，通过使用本适配器，可以使用 :java:extdoc:`Transactional<nablarch.integration.doma.Transactional>` 拦截器
仅将指定的Action作为事务管理对象，
从而减少不必要的事务控制处理，有望提高性能。

模块列表
--------------------------------------------------
.. code-block:: xml

  <!-- Doma适配器 -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-doma-adaptor</artifactId>
  </dependency>
  
.. tip::

  使用Doma版本2.62.0进行测试。
  要更改版本时，请在项目侧进行测试确认无问题。

进行使用Doma适配器的设置
--------------------------------------------------
以下显示使用本适配器的步骤。

.. _`doma_dependency`:

依赖关系的设置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
需要参考以下内容设置项目的依赖关系。

详情请参阅 `Doma2中的Maven构建设置(外部网站) <https://doma.readthedocs.io/ja/latest/build/#build-with-maven>`_ 。

.. code-block:: xml

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <configuration>
                    <annotationProcessorPaths>
                        <path>
                            <groupId>org.seasar.doma</groupId>
                            <artifactId>doma-processor</artifactId>
                            <version>2.62.0</version>
                        </path>
                    </annotationProcessorPaths>
                    <!-- 使用Eclipse时，请设置以下参数
                    <compilerArgs>
                        <arg>-Adoma.resources.dir=${project.basedir}/src/main/resources</arg>
                    </compilerArgs>
                    -->
                </configuration>
            </plugin>
        </plugins>
    </build>

根据使用的RDBMS设置Doma的方言和数据源
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
需要根据项目中使用的RDBMS在组件配置文件中定义Doma的方言和数据源。

以下显示使用H2时的设置示例。

要点
 * 定义的方言必须是 ``org.seasar.doma.jdbc.dialect.Dialect`` 的实现类
 * 方言的组件名必须是 ``domaDialect``
 * 数据源的组件名必须是 ``dataSource``

.. code-block:: xml

  <component name="domaDialect" class="org.seasar.doma.jdbc.dialect.H2Dialect"  />
  <component name="dataSource" class="org.h2.jdbcx.JdbcDataSource">
    <!-- 属性省略 -->
  </component>

使用Doma访问数据库
--------------------------------------------------
以下显示使用Doma进行数据库访问的步骤。

创建Dao接口
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
创建用于数据库访问的Dao(Data Access Object)接口。

.. code-block:: java

  @Dao
  public interface ProjectDao {
      // 省略
  }

实现数据库访问处理
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
在业务Action的方法中实现数据库访问处理。

要点
 * 为了将业务Action方法作为事务管理对象，
   需要设置 :java:extdoc:`Transactional<nablarch.integration.doma.Transactional>` 拦截器
 * 使用 :java:extdoc:`DomaDaoRepository#get<nablarch.integration.doma.DomaDaoRepository.get(java.lang.Class)>` 查找Dao的实现类

  .. tip::

    由于Doma通过注解处理在编译时自动生成Dao的实现类，因此在编码时实现类还不存在。
    因此，本适配器提供了 :java:extdoc:`DomaDaoRepository<nablarch.integration.doma.DomaDaoRepository>` 作为查找Dao实现类的功能。

.. code-block:: java

    @Transactional
    public HttpResponse create(final HttpRequest request, final ExecutionContext context) {
        final Project project = SessionUtil.delete(context, "project");

        DomaDaoRepository.get(ProjectDao.class).insert(project);

        return new HttpResponse("redirect://complete");
    }

.. tip::

    从Doma 2.44.0开始，Dao注解的config属性已被弃用，因此从Doma 2.44.0之前介绍的内容更改了实现方法。  
    详情请参阅 :ref:`migration_doma2.44.0` 。

在单独事务中执行
--------------------------------------------------
有时希望使用与 :java:extdoc:`Transactional<nablarch.integration.doma.Transactional>` 拦截器启动的事务不同的事务进行数据库访问。

在这种情况下，使用 :java:extdoc:`DomaConfig#getTransactionManager <nablarch.integration.doma.DomaConfig.getTransactionManager()>` 获取的
`TransactionManager` 在单独事务中进行控制。

以下显示实现示例。

.. code-block:: java

  DomaConfig.singleton()
          .getTransactionManager()
          .requiresNew(() ->
                  DomaDaoRepository.get(ProjectDao.class).insert(project);


在符合Jakarta Batch的批处理应用程序中使用
----------------------------------------------------------------
为了在符合Jakarta Batch的批处理应用程序中使用Doma，
本适配器提供了以下监听器。

* :java:extdoc:`DomaTransactionStepListener<nablarch.integration.doma.batch.ee.listener.DomaTransactionStepListener>`
* :java:extdoc:`DomaTransactionItemWriteListener<nablarch.integration.doma.batch.ee.listener.DomaTransactionItemWriteListener>`

通过在监听器列表中定义这些监听器，
可以在符合Jakarta Batch的批处理应用程序中使用Doma进行数据库访问。

以下显示设置示例。

.. code-block:: xml

  <list name="stepListeners">
    <!-- 其他监听器省略 -->
    <component class="nablarch.integration.doma.batch.ee.listener.DomaTransactionStepListener" />
  </list>

  <list name="itemWriteListeners">
    <!-- 其他监听器省略 -->
    <component class="nablarch.integration.doma.batch.ee.listener.DomaTransactionItemWriteListener" />
  </list>

.. important::

  在 :ref:`Chunk步骤 <jsr352-batch_type_chunk>` 的ItemWriter中对数据库进行批处理更新(批处理insert或批处理update等)时，需要显式指定批处理大小。
  ※请注意Chunk步骤的item-count大小不会成为批处理大小

  如果不这样做，将应用Doma的默认值，因此即使使用批处理更新也可能无法提高性能。

  实现示例
    例如，要每1000件进行批处理insert时，请按以下方式实现Dao的方法。

    .. code-block:: java

      @BatchInsert(batchSize = 1000)
      int[] batchInsert(List<Bonus> bonuses);


在符合Jakarta Batch的批处理应用程序中进行延迟加载
----------------------------------------------------------------
在符合Jakarta Batch的批处理应用程序中读取大量数据时，有时希望使用延迟加载。

在这种情况下，在查找Dao的实现类时使用 :java:extdoc:`DomaDaoRepository#get(java.lang.Class,java.lang.Class)<nablarch.integration.doma.DomaDaoRepository.get(java.lang.Class,java.lang.Class)>` ，
在第2个参数中指定 :java:extdoc:`DomaTransactionNotSupportedConfig<nablarch.integration.doma.DomaTransactionNotSupportedConfig>` 的Class类。

.. important::

  如果使用带1个参数的 :java:extdoc:`DomaDaoRepository#get(java.lang.Class)<nablarch.integration.doma.DomaDaoRepository.get(java.lang.Class)>` ，
  将使用 :java:extdoc:`DomaConfig<nablarch.integration.doma.DomaConfig>` ，
  因此 :java:extdoc:`DomaTransactionItemWriteListener<nablarch.integration.doma.batch.ee.listener.DomaTransactionItemWriteListener>` 提交事务时会关闭流，导致后续记录无法读取。

以下显示实现示例。

Dao接口
  要点
    * 搜索结果以 :java:extdoc:`Stream<java.util.stream.Stream>` 获取。

  .. code-block:: java

    @Dao
    public interface ProjectDao {

        @Select(strategy = SelectType.RETURN)
        Stream<Project> search();
    }

ItemReader类
  要点
     * 在获取Dao的实现类时使用 :java:extdoc:`DomaDaoRepository#get(java.lang.Class,java.lang.Class)<nablarch.integration.doma.DomaDaoRepository.get(java.lang.Class,java.lang.Class)>` ，
       在第2个参数中指定 :java:extdoc:`DomaTransactionNotSupportedConfig<nablarch.integration.doma.DomaTransactionNotSupportedConfig>` 。
     * 在open方法中获取搜索结果的流。
     * 为防止资源释放遗漏，务必在close方法中关闭流。

  .. code-block:: java

    @Dependent
    @Named
    public class ProjectReader extends AbstractItemReader {

        private Iterator<Project> iterator;

        private Stream<Project> stream;

        @Override
        public void open(Serializable checkpoint) throws Exception {
            final ProjectDao dao = DomaDaoRepository.get(ProjectDao.class, DomaTransactionNotSupportedConfig.class);
            stream = dao.search();
            iterator = stream.iterator();
        }

        @Override
        public Object readItem() {
            if (iterator.hasNext()) {
                return iterator.next();
            } else {
                return null;
            }
        }

        @Override
        public void close() throws Exception {
            stream.close();
        }
    }

  .. tip::

    从Doma 2.44.0开始，Dao注解的config属性已被弃用，因此从Doma 2.44.0之前介绍的内容更改了实现方法。  
    详情请参阅 :ref:`migration_doma2.44.0` 。

访问多个数据库
--------------------------------------------------
如果需要访问多个数据库，需要创建新的Config类，
并实现对另一个数据库的访问使用该Config类。

以下显示实现示例。

组件配置文件
  .. code-block:: xml

    <component name="customDomaDialect" class="org.seasar.doma.jdbc.dialect.OracleDialect"  />
    <component name="customDataSource" class="oracle.jdbc.pool.OracleDataSource">
      <!-- 属性省略 -->
    </component>

Config类
  要点
     * 实现Doma提供的Config接口。
     * 具有public可见性且无参数的构造函数。

  .. code-block:: java

    public final class CustomConfig implements Config {

        public CustomConfig() {
            dialect = SystemRepository.get("customDomaDialect");
            localTransactionDataSource =
                    new LocalTransactionDataSource(SystemRepository.get("customDataSource"));
            localTransaction = localTransactionDataSource.getLocalTransaction(getJdbcLogger());
            localTransactionManager = new LocalTransactionManager(localTransaction);
        }

        // 其他字段、方法请参考DomaConfig实现
    }

Dao接口
  .. code-block:: java

    @Dao
    public interface ProjectDao {
        // 省略
    }


业务Action类
  要点
     * 在获取Dao的实现类时，使用 :java:extdoc:`DomaDaoRepository#get(java.lang.Class,java.lang.Class)<nablarch.integration.doma.DomaDaoRepository.get(java.lang.Class,java.lang.Class)>` ，
       在第2个参数中指定创建的Config类。

  .. code-block:: java

    public HttpResponse create(final HttpRequest request, final ExecutionContext context) {
        final Project project = SessionUtil.delete(context, "project");

        CustomConfig.singleton()
                .getTransactionManager()
                .requiresNew(() ->
                        DomaDaoRepository.get(ProjectDao.class, CustomConfig.class).insert(project);

        return new HttpResponse("redirect://complete");
    }

  .. tip::

    从Doma 2.44.0开始，创建Config的SingletonConfig注解的赋予以及Dao注解的config属性已被弃用，
    因此从Doma 2.44.0之前介绍的内容更改了实现方法。  
    详情请参阅 :ref:`migration_doma2.44.0` 。

同时使用Doma和Nablarch的数据库访问
--------------------------------------------------
即使在数据库访问中采用Doma，也可能希望使用 :ref:`Nablarch提供的数据库访问 <database_management>` 。
例如，使用 :ref:`邮件发送库 <mail>` 时就是这种情况。(:ref:`邮件发送请求 <mail-request>` 中使用了 :ref:`database` 。)

为了解决此问题，Nablarch提供了数据库访问处理可以使用与Doma相同的事务(数据库连接)的功能。

使用步骤
  在组件配置文件中添加以下定义。
  这样，Nablarch的数据库访问将自动在Doma的事务控制下执行。
  
  * 在组件配置文件中定义 :java:extdoc:`ConnectionFactoryFromDomaConnection <nablarch.integration.doma.ConnectionFactoryFromDomaConnection>` 。
    组件名设为 ``connectionFactoryFromDoma`` 。
  * 在用于Jakarta Batch的Doma事务控制监听器中设置ConnectionFactoryFromDomaConnection。

  .. code-block:: xml

    <!-- 组件名设为connectionFactoryFromDoma -->
    <component name="connectionFactoryFromDoma"
        class="nablarch.integration.doma.ConnectionFactoryFromDomaConnection">
        
      <!-- 对属性的设置省略 -->
      
    </component>
    
    <!-- 
    在符合Jakarta Batch的批处理应用程序中使用时，
    将上述定义的connectionFactoryFromDoma设置到控制Doma事务的监听器中。
     -->
    <component class="nablarch.integration.doma.batch.ee.listener.DomaTransactionItemWriteListener">
      <property name="connectionFactory" ref="connectionFactoryFromDoma" />
    </component>

    <component class="nablarch.integration.doma.batch.ee.listener.DomaTransactionStepListener">
      <property name="connectionFactory" ref="connectionFactoryFromDoma" />
    </component>

切换日志记录器
--------------------------------------------------
本适配器提供 :java:extdoc:`NablarchJdbcLogger<nablarch.integration.doma.NablarchJdbcLogger>` 作为Doma使用的日志记录器的实现，使用Nablarch的日志记录器。
默认使用 :java:extdoc:`NablarchJdbcLogger<nablarch.integration.doma.NablarchJdbcLogger>` ，但要切换到其他日志记录器时需要在组件定义文件中设置。

以下显示使用 ``org.seasar.doma.jdbc.UtilLoggingJdbcLogger`` 时的设置示例。

要点
 * 定义的日志记录器必须是 ``org.seasar.doma.jdbc.JdbcLogger`` 的实现类
 * 日志记录器的组件名必须是 ``domaJdbcLogger``

.. code-block:: xml

  <component name="domaJdbcLogger" class="org.seasar.doma.jdbc.UtilLoggingJdbcLogger"  />

进行与java.sql.Statement相关的设置
--------------------------------------------------
有时希望在项目范围内设置获取大小、查询超时等与 ``java.sql.Statement`` 相关的项目。

在这种情况下，在组件配置文件中设置 :java:extdoc:`DomaStatementProperties<nablarch.integration.doma.DomaStatementProperties>` 。

可设置的项目包括以下内容。

* 最大行数限制值
* 获取大小
* 查询超时（秒）
* 批处理大小

以下显示设置示例。

要点
 * 组件名必须是 ``domaStatementProperties``

.. code-block:: xml

  <component class="nablarch.integration.doma.DomaStatementProperties" name="domaStatementProperties">
    <!-- 将最大行数限制值设置为1000行 -->
    <property name="maxRows" value="1000" />
    <!-- 将获取大小设置为200行 -->
    <property name="fetchSize" value="200" />
    <!-- 将查询超时设置为30秒 -->
    <property name="queryTimeout" value="30" />
    <!-- 将批处理大小设置为400 -->
    <property name="batchSize" value="400" />
  </component>

.. _`migration_doma2.44.0`:

从Doma 2.44.0之前的实现方法迁移
--------------------------------------------------

`从Doma 2.44.0开始(外部网站，英语) <https://github.com/domaframework/doma/releases/tag/2.44.0>`_ Dao注解的config属性和SingletonConfig注解已被弃用，
因此Nablarch也添加了API并更改了介绍的内容和实现方法。

继续使用Dao注解的config属性和SingletonConfig注解的实现也可以运行，但建议根据Doma的更改迁移实现方法。

此处说明与Doma 2.44.0之前Nablarch介绍的实现方法的对比。

另外，Doma 2.44.0之前介绍的实现方法也将继续执行相同的操作。

使用DomaConfig的基本实现情况
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

以下显示在Dao注解的config属性中使用 :java:extdoc:`DomaConfig<nablarch.integration.doma.DomaConfig>` 的实现示例。

.. code-block:: java

  // Dao的定义
  @Dao(config = DomaConfig.class)  /* 指定config属性 */
  public interface ProjectDao {
      // 省略
  }

  // 使用Dao的实现示例
  @Transactional
  public HttpResponse create(final HttpRequest request, final ExecutionContext context) {
      final Project project = SessionUtil.delete(context, "project");

      DomaDaoRepository.get(ProjectDao.class).insert(project);

      return new HttpResponse("redirect://complete");
  }

这等价于以下实现。

.. code-block:: java

  // Dao的定义
  @Dao  /* 删除config属性的指定 */
  public interface ProjectDao {
      // 省略
  }

  // 使用Dao的实现示例
  @Transactional
  public HttpResponse create(final HttpRequest request, final ExecutionContext context) {
      final Project project = SessionUtil.delete(context, "project");

      DomaDaoRepository.get(ProjectDao.class).insert(project);  /* 无更改 */

      return new HttpResponse("redirect://complete");
  }

对于不使用Dao注解的config属性而使用 :java:extdoc:`DomaDaoRepository#get<nablarch.integration.doma.DomaDaoRepository.get(java.lang.Class)>` 获取Dao实现类的情况，
将使用 :java:extdoc:`DomaConfig<nablarch.integration.doma.DomaConfig>` 构建Dao的实现类。

使用DomaTransactionNotSupportedConfig进行延迟加载的情况
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

以下显示为了在符合Jakarta Batch的批处理应用程序中支持延迟加载而使用 :java:extdoc:`DomaTransactionNotSupportedConfig<nablarch.integration.doma.DomaTransactionNotSupportedConfig>` 的实现示例。

.. code-block:: java

    // Dao的定义
    @Dao(config = DomaTransactionNotSupportedConfig.class)  /* 指定config属性 */
    public interface ProjectDao {

        @Select(strategy = SelectType.RETURN)
        Stream<Project> search();
    }

    // 使用Dao的实现示例
    @Dependent
    @Named
    public class ProjectReader extends AbstractItemReader {

        private Iterator<Project> iterator;

        private Stream<Project> stream;

        @Override
        public void open(Serializable checkpoint) throws Exception {
            /* 在DomaDaoRepository#get中仅指定Dao的接口 */
            final ProjectDao dao = DomaDaoRepository.get(ProjectDao.class);
            stream = dao.search();
            iterator = stream.iterator();
        }

        // 省略
    }

这等价于以下实现。

.. code-block:: java

    // Dao的定义
    @Dao  /* 删除config属性的指定 */
    public interface ProjectDao {

        @Select(strategy = SelectType.RETURN)
        Stream<Project> search();
    }

    // 使用Dao的实现示例
    @Dependent
    @Named
    public class ProjectReader extends AbstractItemReader {

        private Iterator<Project> iterator;

        private Stream<Project> stream;

        @Override
        public void open(Serializable checkpoint) throws Exception {
            /* 在DomaDaoRepository#get的第2参数中指定DomaTransactionNotSupportedConfig.class */
            final ProjectDao dao = DomaDaoRepository.get(ProjectDao.class, DomaTransactionNotSupportedConfig.class);
            stream = dao.search();
            iterator = stream.iterator();
        }

        // 省略
    }

对于不使用Dao注解的config属性而使用 :java:extdoc:`DomaDaoRepository#get(java.lang.Class,java.lang.Class)<nablarch.integration.doma.DomaDaoRepository.get(java.lang.Class,java.lang.Class)>` 调用的情况，
将使用第2参数中指定的Config构建Dao的实现类。

创建自定义Config类的情况
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

以下显示为了访问多个数据库等原因而创建自定义Config类的实现示例。

.. code-block:: java

    // Config类的定义
    @SingletonConfig  /* 赋予SingletonConfig注解 */
    public final class CustomConfig implements Config {

        private CustomConfig() {  /* 构造函数为private */
            // 省略
        }

        // 省略
    }

    // Dao的定义
    @Dao(config = CustomConfig.class)  /* 在config属性中指定创建的Config类 */
    public interface ProjectDao {
        // 省略
    }

    // 使用Dao的实现示例
    public HttpResponse create(final HttpRequest request, final ExecutionContext context) {
        final Project project = SessionUtil.delete(context, "project");

        CustomConfig.singleton()
                .getTransactionManager()
                .requiresNew(() ->
                        /* 在DomaDaoRepository#get中仅指定Dao的接口 */
                        DomaDaoRepository.get(ProjectDao.class);

        return new HttpResponse("redirect://complete");
    }

这等价于以下实现。

.. code-block:: java

    // Config类的定义
    /* 删除SingletonConfig注解 */
    public final class CustomConfig implements Config {

        public CustomConfig() {  /* 更改为public的无参数构造函数 */
            // 省略
        }

        // 省略
    }

    // Dao的定义
    @Dao  /* 删除config属性的指定 */
    public interface ProjectDao {
        // 省略
    }

    // 使用Dao的实现示例
    public HttpResponse create(final HttpRequest request, final ExecutionContext context) {
        final Project project = SessionUtil.delete(context, "project");

        CustomConfig.singleton()
                .getTransactionManager()
                .requiresNew(() ->
                        /* 在DomaDaoRepository#get的第2参数中指定创建的Config的Class类 */
                        DomaDaoRepository.get(ProjectDao.class, CustomConfig.class);

        return new HttpResponse("redirect://complete");
    }

对于不使用Dao注解的config属性而使用 :java:extdoc:`DomaDaoRepository#get(java.lang.Class,java.lang.Class)<nablarch.integration.doma.DomaDaoRepository.get(java.lang.Class,java.lang.Class)>` 调用的情况，
将使用第2参数中指定的Config构建Dao的实现类。
