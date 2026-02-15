.. _repository:

系统仓库
==================================================

.. contents:: 目录
  :depth: 3
  :local:

提供管理实现应用程序时各处使用的对象、设置值等的功能。

本功能可以进行以下操作。

* 可以在外部文件中定义可能因环境而异的逻辑（生成的类或属性值）。
* 可以基于外部文件的定义构建对象间的关联。（具有DI容器功能）

功能概述
--------------------------------------------------
可以通过DI容器构建对象
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
使用DI容器功能，可以基于 :ref:`xml <repository-root_node>` 中定义的组件定义或
:ref:`添加注解的类 <repository-inject-annotation-component>` 构建对象。
构建的对象为 **单例** 。

DI容器功能可以进行以下操作。

* :ref:`可以进行setter注入。 <repository-definition_bean>`
* :ref:`可以使用字符串、数值、布尔值。 <repository-property_type>`
* :ref:`可以注入List和Map。 <repository-map_list>`
* :ref:`可以向类型和名称匹配的setter自动注入。 <repository-autowired>`
* :ref:`可以进行工厂注入。 <repository-factory_injection>`
* :ref:`可以构建添加注解的类的对象。 <repository-inject-annotation-component>`
* :ref:`可以管理环境依赖值。 <repository-environment_configuration>`

应用程序不直接访问DI容器，而是通过系统仓库访问。
详细参见 :ref:`repository-use_system_repository` 。

可以进行对象初始化
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
对象构建后可以执行任意初始化处理。

根据对象的依赖关系，可能会产生初始化顺序的约束，
因此本功能可以指定对象的初始化顺序。

详细参见 :ref:`repository-initialize_object` 。

模块列表
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core</artifactId>
  </dependency>
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-repository</artifactId>
  </dependency>

使用方法
--------------------------------------------------

.. _repository-root_node:

在xml中定义根节点
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
组件设置文件(xml)的根节点为 `component-configuration` 。
正确设置 `schemaLocation` 后，可以在IDE中引用各元素或属性的文档，或有效利用补全功能。

.. code-block:: xml

  <component-configuration xmlns="http://tis.co.jp/nablarch/component-configuration"
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://tis.co.jp/nablarch/component-configuration /component-configuration.xsd">

  </component-configuration>

xml中组件定义方法的详细内容参见以下。

* :ref:`repository-definition_bean`
* :ref:`repository-override_bean`
* :ref:`repository-property_type`
* :ref:`repository-map_list`
* :ref:`repository-autowired`
* :ref:`repository-environment_configuration`
* :ref:`repository-user_environment_configuration`
* :ref:`repository-factory_injection`
* :ref:`repository-initialize_object`
* :ref:`repository-split_xml`

.. _repository-definition_bean:

设置Java Beans对象
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Java Beans对象使用component元素定义。

* class属性设置DI容器管理的类的FQCN。
* 使用name属性可以设置任意名称。
* 使用property子元素可以进行setter注入。
* 可以在property的子元素中定义component。
* 使用property的ref属性可以setter注入其他定义的component。


以下展示示例。

.. code-block:: xml

  <!-- 使用component元素设置Java Beans对象 -->
  <component name="sample" class="sample.SampleBean" />

  <component name="component" class="sample.SampleComponent">
    <!--
     使用property元素进行setter注入
     此示例中，名称为sample的component定义的对象被注入
     -->
    <property name="sample" ref="sample" />

    <!-- 不使用ref属性，也可以在property的子元素中定义component -->
    <property name="obj">
      <component class="sample.SampleObject" />
    </property>

    <!-- setter注入字面量值 -->
    <property name="limit" value="100" />
  </component>


.. important::

  生成的实例为单例。因此，注意以下事项。

  - 实例为单例，因此不是每次获取都生成（非原型）。
  - 应用程序结束前实例不会被销毁。
  
  误解这一点可能会导致严重的问题，因此特别需要注意。
  例如，如果误以为生成的实例是原型，可能会在某个请求中将用户A的输入值设置到组件中，
  在另一个用户B的请求中使用该值，导致严重的故障。
  
  如果要在应用程序中故意更改、共享组件的状态，该组件必须是线程安全的。


.. tip::

  对象按component元素单位生成实例。例如，如果在两处定义component如下，会生成不同的实例。

  .. code-block:: xml

    <!-- SampleBean的2个实例注册到仓库中 -->
    <component name="sample1" class="sample.SampleBean" />
    <component name="sample2" class="sample.SampleBean" />

.. tip::

  嵌套定义的component也在仓库的全局区域中保持，因此可以通过名称获取对象。
  对象获取方法参见 :ref:`repository-get_object` 。

  

.. tip::
   不对static属性(static setter方法)进行注入。
   注入目标的属性为static时，DI容器构建时会抛出异常。
   
.. _repository-override_bean:

覆盖Java Beans对象的设置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
通过component标签的name属性注册相同名称的对象，可以覆盖之前读取的对象设置。
此功能可在测试时将生产环境用对象替换为测试用对象（模拟）。

覆盖对象时，只需注册相同名称的对象，自动优先后读取的对象。

以下展示示例。

.. code-block:: xml

  <component name="sample" class="sample.SampleBean">
    <property name="prop" value="message" />
  </component>

  <!-- 使用相同名称定义组件进行覆盖 -->
  <component name="sample" class="sample.MockSampleBean" />

.. important::

  如上面的示例设置不同类时，覆盖前的property设置将全部废弃。
  这是因为即使实现了相同接口，也不一定有相同的property。

  但是，设置相同类时，覆盖前的property设置将全部继承到覆盖后的类。
  因此，无法删除覆盖后设置中特定property的设置。
  例如，进行如下覆盖设置时，覆盖后的设置中不存在property元素，
  但由于继承了覆盖前的prop值，因此prop为设置了message的状态。

  .. code-block:: xml

    <component name="sample" class="sample.SampleBean">
      <property name="prop" value="message" />
    </component>

    <!--
    虽然未设置property，但继承了覆盖前的prop值
     -->
    <component name="sample" class="sample.SampleBean" />

.. _repository-property_type:

使用字符串、数值、布尔值作为设置值
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
属性类型为以下类型时，可以使用字面量表示简易设置值。

* java.lang.String
* java.lang.String[]
* java.lang.Integer(int)
* java.lang.Integer[](int[])
* java.lang.Long(long)
* java.lang.Boolean(boolean)

以下展示设置示例。

java.lang.String
  向java.lang.String型设置值时，在value属性中用字面量描述要设置的值。

  此示例中，向str属性设置文本。

  .. code-block:: xml

    <property name="str" value="sample text" />

java.lang.String[]
  向java.lang.String[]型设置值时，在value属性中用逗号(,)分隔设置值。
  逗号分隔的值成为数组的一个元素。

  此示例中，向array属性设置列表值。

  .. code-block:: xml

    <property name="array" value="a,b,c,d,e" />

java.lang.Integer(int)
  向java.lang.Integer型及int型设置值时，在value属性中描述要设置的值。
  可设置的值为 Integer#valueOf 可转换的值。

  此示例中，向Integer(int)型的num属性设置数值。

  .. code-block:: xml

    <property name="num" value="12345" />

java.lang.Integer[](int[])
  与java.lang.String[]相同，在value属性中用逗号(,)分隔设置值。
  各元素可设置的值为 Integer#valueOf 可转换的值。

java.lang.Long(long)
  与java.lang.Integer(int)相同，在value属性中描述要设置的值。
  可设置的值为 Long#valueOf 可转换的值。

java.lang.Boolean(boolean)
  向java.lang.Boolean型设置值时，在value属性中用字面量描述要设置的值。
  可设置的值为 Boolean#valueOf 可转换的值。

  此示例中，向Boolean(boolean)型的bool属性设置布尔值。

  .. code-block:: xml

    <property name="bool" value="true" />

.. _repository-map_list:

使用List和Map作为设置值
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
使用list元素或map元素进行组件设置，可以对接受List或Map的property进行setter注入。

使用list元素的List设置
  list元素可以设置字符串或任意Java Beans对象。

  此示例中，向SampleBean的stringList属性设置字符串List。

  .. code-block:: xml

    <component class="sample.SampleBean">
      <property name="stringList">
        <list>
          <value>string1</value>
          <value>string2</value>
          <value>string3</value>
        </list>
      </property>
    </component>

  list元素也可以设置任意名称，property元素可以通过名称引用。
  此示例与上面的示例设置相同。

  .. code-block:: xml

    <list name="strList">
      <value>string1</value>
      <value>string2</value>
      <value>string3</value>
    </list>

    <component class="sample.ListSample">
      <!-- 设置名称为strList的List -->
      <property name="stringList" ref="strList" />
    </component>

  此示例中，向handlers属性设置Java Beans对象List。

  .. code-block:: xml

    <component name="sampleHandler3" class="sample.SampleHandler3" />

    <component class="sample.ListSample">
      <property name="handlers">
        <list>
          <component class="sample.SampleHandler1" />
          <component class="sample.SampleHandler2" />
          <component-ref name="sampleHandler3" />
        </list>
      </property>
    </component>

使用map元素的Map设置
  此示例中，向map属性设置Map值。

  .. code-block:: xml

    <property name="map">
      <map>
        <entry key="key1" value="1" />
        <entry key="key2" value="2" />
        <entry key="key3" value="3" />
      </map>
    </property>

  map也可以设置任意名称，property元素可以通过名称引用。

  .. code-block:: xml

      <map name="map">
        <entry key="key1" value="1" />
        <entry key="key2" value="2" />
        <entry key="key3" value="3" />
      </map>

    <component class="sample.ListSample">
      <!-- 设置名称为map的Map -->
    <property name="map" ref="map">
    </component>

  使用value-component元素可以将任意Bean也设置为Map的值。

  .. code-block:: xml

    <property name="settings">
      <map>
        <entry key="sample1">
          <value-component class="sample.SampleBean1" />
        </entry>
        <entry key="sample2">
          <value-component class="sample.SampleBean2" />
        </entry>
      </map>
    </property>

.. important::
  定义多个name属性相同的map或list时，先定义的有效。
  这与 :ref:`bean的覆盖 <repository-override_bean>` 行为不同，请注意。

  如果希望按环境更改map或list的信息，通过更改各环境读取的文件来对应。
  

.. _repository-autowired:

自动注入组件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
即使省略组件的property标签定义，也提供自动注入组件的功能。
此功能通过使用component元素的autowireType属性，可以指定自动注入类型。

.. important::

  使用自动注入功能存在以下问题，因此建议autowireType属性显式指定 None 。

  * 最终生成的对象状态无法从组件设置文件(xml)读取。
  * 省略可选项目的属性定义时，可能会自动注入未预料的对象。
  * 使用基于类型的自动注入时，如果在衍生开发中增加了相同类型对象的设置，
    需要property定义，因此可维护性差。

autowireType属性可指定的类型如下。

ByType
  DI容器上该属性类型只有1个时，自动注入该组件。
  默认使用此类型。

ByName
  存在与属性名匹配的组件时，自动注入该组件。
  另外，属性与组件类型不匹配时会报错。

None
  不进行自动注入。

默认(ByType)设置自动注入的示例如下。

创建注入目标的类
  创建注入目标的接口及实现类。
  此示例中创建了接口，但创建接口不是必需的。

  .. code-block:: java

    public interface SampleComponent {
    }

    public class BasicSampleComponent implements SampleComponent {
    }

创建使用注入目标对象的类
  创建使用上述类进行处理的类。
  此类通过setter注入接收上述类。

  .. code-block:: java

    public class SampleClient {
      private SampleComponent component;

      public void setSampleComponent(SampleComponent component) {
        this.component = component;
      }
    }

在组件设置文件中定义组件
  此示例中， SampleClient 未定义 sampleComponent property，但 SampleComponent 的实现类设置只有1个，
  因此 sampleComponent property自动设置 BasicSampleComponent 。

  .. code-block:: xml

    <component name="sampleComponent" class="sample.BasicSampleComponent" />

    <component name="sampleClient" class="sample.SampleClient" />


  上述设置与如下显式定义property时行为相同。

  .. code-block:: xml

    <component name="sampleComponent" class="sample.BasicSampleComponent" />

    <component name="sampleClient" class="sample.SampleClient">
      <property name="sampleComponent" ref="sampleComponent" />
    </component>

.. _repository-split_xml:

分割组件设置文件(xml)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
将所有定义定义在一个组件设置文件中会导致xml过大，可维护性差。
因此，提供了可以将xml文件分割为多个文件的功能。

分割xml文件时，按功能单位等一定粒度分割文件比较好。
分割的xml文件可以通过import元素读取。

以下展示示例。

此示例中，加载3个xml文件。

.. code-block:: xml

  <import file="library/database.xml" />
  <import file="library/validation.xml" />
  <import file="handler/multipart.xml" />

.. _repository-environment_configuration:

设置依赖值
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
在测试环境或生产环境中不同的值（数据库连接信息或目录路径等）可以在环境设置文件中管理。

环境设置文件如下以简单的key-value形式描述。
详细描述规则参见 :ref:`repository-environment_configuration_file_rule` 。

.. code-block:: bash

  database.url = jdbc:h2:mem:sample
  database.user = sa
  database.password = sa

.. important::

  环境设置值的键值重复时，后定义的有效，请注意。

以下展示示例。

环境依赖值
  .. code-block:: bash

    database.url = jdbc:h2:mem:sample
    database.user = sa
    database.password = sa

.. _repository-user_environment_configuration:

从组件设置文件引用环境依赖值
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
可以从组件设置文件(xml)读取环境设置文件，作为Java Beans对象的设置值使用。

对DI容器管理的对象设置（注入）环境依赖值时，
在组件设置文件中用 ${ 和 } 包围环境依赖值的键值来描述。

另外，此写法不能在环境设置文件中使用。（环境设置文件内不能引用其他环境依赖值。）

以下展示示例。

环境设置文件
  .. code-block:: bash

    database.url = jdbc:h2:mem:sample
    database.user = sa
    database.password = sa

组件设置文件
  读取环境设置文件时，使用config-file元素。
  如此示例可以通过文件名指定读取，也可以批量读取特定目录下的文件。

  上述环境设置文件的名称为database.properties时， JdbcDataSource 的 url 设置相应值。

  .. code-block:: xml

    <!-- 读取database.properties文件 -->
    <config-file file="database.properties" />

    <component class="org.h2.jdbcx.JdbcDataSource">
      <property name="url" value="${database.url}" />
    </component>

  环境设置文件有config文件和properties文件两种，config文件按Nablarch的独自规格解析，
  properties文件由java.util.Properties解析。由于config文件是Nablarch的独自规格，
  因此环境设置文件推荐使用properties文件。

  环境设置文件规格参见 :ref:`repository-environment_configuration_file_rule` 。

.. important::

  在组件设置文件中记载环境设置文件中未定义的环境依赖值键时，会抛出ConfigurationLoadException。

.. _repository-overwrite_environment_configuration:

使用系统属性覆盖环境依赖值
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
环境依赖值可以通过系统属性( java.lang.System#getProperties() 可获取的值)覆盖。
系统属性优先于环境设置文件中设置的值，因此可以通过vm选项轻松覆盖设置值。

例如，只想更改特定Batch应用程序的设置值时，可以使用系统属性覆盖环境依赖值。

以下展示示例。

环境设置文件

  .. code-block:: bash

    message=将被覆盖的消息

使用系统属性覆盖值
  通过java命令的 -D 选项设置系统属性，可以覆盖环境设置文件的值。
  此示例中， message 的值为覆盖后的消息。

  java -Dmessage=覆盖后的消息

.. _repository-overwrite_environment_configuration_by_os_env_var:

使用OS环境变量覆盖环境依赖值
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
按照以下说明设置，可以通过OS环境变量覆盖环境依赖值。

启用OS环境变量覆盖的设置方法
  覆盖环境依赖值的机制由实现 ExternalizedComponentDefinitionLoader 接口的类实现。
  
  此实现类通过 java.util.ServiceLoader 加载。
  未设置服务提供者时，默认使用 SystemPropertyExternalizedLoader 。
  此类是通过系统属性覆盖的类，前一节说明的系统属性覆盖由此类实现。
  
  使用OS环境变量覆盖环境依赖值时，实现类使用 OsEnvironmentVariableExternalizedLoader 。
  
  具体设置如下进行。
  
  #. 在类路径根目录下创建 META-INF/services 目录
  #. 在上述创建的目录中，创建名为 nablarch.core.repository.di.config.externalize.ExternalizedComponentDefinitionLoader 的文本文件
  #. 在文件中换行分隔列举要使用的实现类的完全限定名
  
  例如，使用 OsEnvironmentVariableExternalizedLoader 时， nablarch.core.repository.di.config.externalize.ExternalizedComponentDefinitionLoader 的内容如下描述。
  
  .. code-block:: text
  
    nablarch.core.repository.di.config.externalize.OsEnvironmentVariableExternalizedLoader
  
  
  组合多个实现类时，可以如下换行分隔列举。
  
  .. code-block:: text
  
    nablarch.core.repository.di.config.externalize.OsEnvironmentVariableExternalizedLoader
    nablarch.core.repository.di.config.externalize.SystemPropertyExternalizedLoader
  
  指定多个实现类时，从上往下依次进行覆盖。
  因此，如果用各种方法覆盖相同名称的环境依赖值，最下面描述的类的覆盖最终采用。
  上述示例中，系统属性设置的值比OS环境变量设置的值优先。

.. _repository-overwrite_environment_configuration_by_os_env_var_naming_rule:

关于OS环境变量的名称
  Linux中，OS环境变量的名称不能使用 . 或 - 。
  因此，如果有 example.error-message 这样名称的环境依赖值，无法使用原样名称定义用于覆盖的OS环境变量。

  Nablarch为回避此问题，按以下方式转换环境依赖值名称后搜索OS环境变量。

  #. 将 . 和 - 替换为 _
  #. 将字母转换为大写

  即， example.error-message 这样名称的环境依赖值，可以通过定义 EXAMPLE_ERROR_MESSAGE 名称的OS环境变量来覆盖。
  
  Windows中OS环境变量可以使用 . 或 - ，但上述转换处理与运行时OS无关都会执行。
  因此， example.error-message 用于覆盖的OS环境变量，Windows中也必须定义为 EXAMPLE_ERROR_MESSAGE 名称。


.. _repository-factory_injection:

注入工厂类生成的对象
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
如果是实现为Java Beans的类，可以使用setter注入设置值生成对象。
但是，有时想将供应商提供或OSS等未实现为Java Beans的对象管理在系统仓库中。

这种情况下，创建工厂类并通过工厂类生成对象，可以将这些类管理在系统仓库中。

以下展示步骤。

创建工厂类
  工厂类实现 ComponentFactory 接口创建。

  实现示例
    .. code-block:: java

      public class SampleComponentFactory implements ComponentFactory<SampleComponent> {
        // 生成对象的设置值
        private String configValue;

        public void setConfigValue(String configValue) {
          this.configValue = configValue;
        }

        public SampleComponent createObject() {
          // 生成对象。
          // 此示例中，使用setter注入到此类的值生成对象。
          return new SampleComponent(configValue);
        }
      }

在组件设置文件中设置工厂类
  与普通组件相同设置工厂类，
  自动设置工厂类生成的对象。

  .. code-block:: xml

    <!-- 工厂类定义 -->
    <component name="sampleComponent" class="sample.SampleComponentFactory">
      <property name="configValue" value="设置值" />
    </component>

    <!-- 设置工厂类生成对象的类 -->
    <component class="sample.SampleBean">
      <!-- sampleObject属性设置工厂类生成的对象 -->
      <property name="sampleObject" ref="sampleComponent" />
    </component>

.. important::

  Nablarch不支持工厂类的嵌套。
  即，不能在工厂类的属性中指定其他工厂类。

  .. code-block:: xml

      <component name="sampleComponent" class="sample.SampleComponentFactory">
        <!-- 工厂类嵌套 -->
        <property name="property">
          <component class="sample.OtherSampleComponentFactory">
        </property>
      </component>

  这种情况下，在1个工厂类内构建嵌套工厂类构建的对象，
  或创建生成嵌套工厂类构建对象的Creator/Builder/Provider等类，
  作为组件注入来对应。

.. _repository-inject-annotation-component:

构建添加注解的类的对象
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SystemRepositoryComponent 
添加到类后，无需 在XML中设置 即可成为DI容器的管理对象。

.. important::

  本功能在类路径下资源由独自文件系统管理的一部分Web应用服务器中无法使用。

  例如，Jboss或Wildfly中，类路径下资源由称为vfs的虚拟文件系统管理，
  因此无法搜索 SystemRepositoryComponent 注解注释的类。

  使用此类Web应用服务器时，组件定义请照旧 在XML中定义 。

使用方法
**********

创建确定收集目标包的类。
  SystemRepositoryComponent 添加的
  类的收集由实现 ExternalizedComponentDefinitionLoader 接口的类执行。
  此类为 AnnotationComponentDefinitionLoader 抽象类，持有返回收集目标基点包的抽象方法
  getBasePackage 。

  根据各项目的包名覆盖上述抽象方法，以便按项目包名进行收集。

  .. code-block:: java

    public class ExampleComponentDefinitionLoader extends AnnotationComponentDefinitionLoader {
        @Override
        protected String getBasePackage() {
            return "com.example";
        }
    }

将创建的类设置为服务提供者。
  为使 java.util.ServiceLoader 加载，与 启用OS环境变量覆盖的设置方法 相同
  创建 nablarch.core.repository.di.config.externalize.ExternalizedComponentDefinitionLoader 文件并记载上述类的完全限定名。

在要DI容器管理的类中添加注解。
  添加 SystemRepositoryComponent 后由DI容器管理。

  .. code-block:: java

    @SystemRepositoryComponent
    public class ExampleAction {

使用构造函数注入
****************************************

SystemRepositoryComponent 添加的类构建时满足以下条件则执行构造函数注入。

* 只定义了1个构造函数
* 构造函数有参数

满足条件时，按以下规格注入。

* ConfigValue 添加的参数注入设置值
* ComponentRef 添加的参数注入DI容器注册的组件
* 上述任一注解都未添加时

  * DI容器上参数类型匹配的组件只有1个时，自动注入该组件
  * DI容器上参数类型匹配的组件不存在或存在多个时，不注入任何内容

注入设置值
  构造函数参数添加 ConfigValue 
  后，注入注解 value 中设置的值。
  可用设置值的类型参见 使用字符串、数值、布尔值作为设置值 。

  与 从组件设置文件引用环境依赖值 时相同
  可以用 ${ 和 } 包围环境依赖值键值来描述。

  .. code-block:: java

    @SystemRepositoryComponent
    public class ExampleService {

        private final String errorMessageId;

        public ExampleService(@ConfigValue("${example.service.errorMessageId}") String errorMessageId) {
            this.errorMessageId = errorMessageId;
        }

注入组件
  构造函数参数添加 ComponentRef 
  后，注入注解 value 中设置名称的组件。

  以下示例中注入以 lettuceRedisClientProvider 名称定义的组件。

  .. code-block:: java

    @SystemRepositoryComponent
    public class ExampleService {

      private LettuceRedisClient client;

      public ExampleService(@ComponentRef("lettuceRedisClientProvider") LettuceRedisClient client) {
          this.client = client;
      }

.. tip::

  构造函数注入由 ConstructorInjectionComponentCreator 类实现。
  通过覆盖 AnnotationComponentDefinitionLoader 的 newComponentCreator 
  ，可以替换为添加注解的类对象构建时执行任意处理的 ComponentCreator 实现。

  .. code-block:: java

    public class ExampleComponentDefinitionLoader extends AnnotationComponentDefinitionLoader {
      @Override
      protected String getBasePackage() {
          return "com.example";
      }

      @Override
      protected ComponentCreator newComponentCreator() {
        // 更改为任意ComponentCreator实现类。
        return new ExampleComponentCreator();
      }
    }

在DI容器中管理Action类
****************************************

在Action类中添加注解后可在DI容器中管理。
Nablarch提供的分派handler（ 路由适配器 、 请求分派handler 、
HTTP请求分派handler ）中
分派目标的类在分派handler内实例化。
因此，要将Action类注册到DI容器时，需要将分派目标的类改为从系统仓库获取的 DelegateFactory 。
替换通过 DispatchHandler#setDelegateFactory 如下设置。

  .. code-block:: xml

    <component name="packageMapping" class="nablarch.integration.router.RoutesMapping">
      <!-- 从系统仓库获取分派目标的DelegateFactory -->
      <property name="delegateFactory">
          <component class="nablarch.fw.handler.SystemRepositoryDelegateFactory"/>
      </property>
      <!-- 其他属性省略 -->
    </component>

.. _repository-initialize_object:

执行对象初始化处理
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
要执行对象初始化处理，需要以下步骤。

#. 实现 Initializable 接口。
#. 在组件设置文件中设置初始化目标列表。

以下展示详细步骤。

实现Initializable接口
  在 initialize 中执行初始化处理。

  .. code-block:: java

    public class SampleComponent implements Initializable {
      public void initialize() {
        // 基于注入属性的值等执行初始化处理
      }
    }

在组件设置文件中设置初始化目标列表
  向 BasicApplicationInitializer 设置初始化目标对象。

  需要注意初始化目标对象的初始化顺序时，将希望先初始化的对象设置得更靠上。
  以下设置示例中，按以下顺序进行初始化。
  
  #. sampleObject1
  #. sampleObject2
  #. sampleObject3

  .. important::
    
    BasicApplicationInitializer 的组件名必须设为 initializer 。

  .. code-block:: xml

    <!-- 初始化目标对象设置 -->
    <component name="sampleObject1" class="sample.SampleComponent1" />
    <component name="sampleObject2" class="sample.SampleComponent2" />
    <component name="sampleObject3" class="sample.SampleComponent3" />

    <component name="initializer"
        class="nablarch.core.repository.initialization.BasicApplicationInitializer">

      <!-- initializeList属性中用list元素列举初始化目标对象 -->
      <property name="initializeList">
        <list>
          <component-ref name="sampleObject1" />
          <component-ref name="sampleObject2" />
          <component-ref name="sampleObject3" />
        </list>
      </property>

    </component>

.. _repository-dispose_object:

执行对象废弃处理
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
要执行对象废弃处理，需要以下步骤。

#. 实现 Disposable 接口。
#. 在组件设置文件中设置废弃目标列表。

以下展示详细步骤。

实现Disposable接口
  在 dispose 中执行废弃处理。

  .. code-block:: java

    public class SampleComponent implements Disposable {
      public void dispose() throws Exception{
        // 执行资源释放等废弃处理
      }
    }

在组件设置文件中设置废弃目标列表
  向 BasicApplicationDisposer 设置废弃目标对象。

  需要注意废弃目标对象的废弃顺序时，将希望先废弃的对象设置得更靠 下 。
  以下设置示例中，按以下顺序进行废弃处理。
  
  #. sampleObject1
  #. sampleObject2
  #. sampleObject3

  .. important::
    
    BasicApplicationDisposer 的组件名必须设为 disposer 。

  .. code-block:: xml

    <!-- 废弃目标对象设置 -->
    <component name="sampleObject1" class="sample.SampleComponent1" />
    <component name="sampleObject2" class="sample.SampleComponent2" />
    <component name="sampleObject3" class="sample.SampleComponent3" />

    <component name="disposer"
        class="nablarch.core.repository.disposal.BasicApplicationDisposer">

      <!-- disposableList属性中用list元素列举废弃目标对象 -->
      <property name="disposableList">
        <list>
          <component-ref name="sampleObject3" />
          <component-ref name="sampleObject2" />
          <component-ref name="sampleObject1" />
        </list>
      </property>

    </component>

  BasicApplicationDisposer 提供了 addDisposable 方法，可以在组件生成后添加任意 Disposable 。

  此 addDisposable 添加的 Disposable ，预计按实例生成顺序添加。
  这种情况下，废弃处理最好按与实例生成相反的顺序进行（例如：JDBC的 Connection, Statement, ResultSet）。
  
  因此， BasicApplicationDisposer 中按与 disposableList 设置顺序相反的顺序调用废弃处理。

将Closeable对象设置到废弃目标列表
  java.io.Closeable 实现的组件，可以使用 DisposableAdaptor 如下轻松设置到废弃目标列表。

  .. code-block:: xml

    <!-- 实现 java.io.Closeable 的组件 -->
    <component name="closeableComponent" class="sample.CloseableComponent" />

    <component name="disposer"
        class="nablarch.core.repository.disposal.BasicApplicationDisposer">

      <property name="disposableList">
        <list>
          <component class="nablarch.core.repository.disposal.DisposableAdaptor">
            <!-- DisposableAdaptor 的 target 属性中，设置实现 Closeable 的组件 -->
            <property name="target" ref="closeableComponent" />
          </component>
        </list>
      </property>

    </component>


.. _repository-use_system_repository:

将DI容器信息设置到系统仓库
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
将DI容器信息加载到系统仓库后，可以从应用程序内所有位置访问DI容器上的对象。

以下展示加载组件设置文件并设置到系统仓库的示例。

此示例中，基于 web-boot.xml 构建的DI容器信息设置到系统仓库。

.. code-block:: java

  XmlComponentDefinitionLoader loader
      = new XmlComponentDefinitionLoader("web-boot.xml");
  SystemRepository.load(new DiContainer(loader));

.. important::

  将DI容器信息注册到系统仓库的处理，由Nablarch提供的以下类执行。
  因此，基本不需要单独实现。

  * ServletContextListener的实现类
  * 独立型应用程序的启动类

.. _repository-get_object:

从系统仓库获取对象
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
从系统仓库上获取对象时，使用 SystemRepository 类。

另外，需要事先将DI容器信息设置到系统仓库。
详细参见 将DI容器信息设置到系统仓库 。

如下，可以指定component元素(包含list或map元素)中设置的name属性值来获取对象。

组件定义
  .. code-block:: xml

    <component name="sampleComponent" class="sample.SampleComponent" />

    <component name="component" class="sample.Component" >
      <property name="component2">
        <component name="component2" class="sample.Component2" />
      </property>
    </component>

获取示例
  .. code-block:: java

    // 使用SystemRepository#get获取。
    SampleComponent sample = SystemRepository.get("sampleComponent");

    // 嵌套的component，将父名称与自身名称用.连接获取。
    Component2 component2 = SystemRepository.get("component.component2");

.. _repository-environment_configuration_file_rule:

环境设置文件的描述规则
--------------------------------------------------
环境设置文件有config文件和properties文件两种，这里说明各环境设置文件的描述规则。

properties文件规格
  基于Java的Properties规格解析。

config文件规格
  以下说明config文件规格。

  设置值的描述格式
    设置值用 = 分隔键和值来描述。

    .. code-block:: bash
    
      key1=value1
      key2=value2

  注释的描述
    注释仅支持使用 # 的行注释。
    行中存在 # 时，其以后作为注释处理。

    .. code-block:: bash

      # 这是注释
      key = value   # 这是注释

  跨多行的设置值描述
    行末描述 \ ，可以跨多行描述设置值。

    以下示例中，设置值的组合如下。

    * key -> value
    * key2 -> value,value2
    * key3 -> abcdefg

    .. code-block:: bash

      key = value
      key2 = value,\
      value2
      key3 = abcd\    # 这里可以定义注释
      efg

  保留字的转义
    以下保留字作为一般字符处理时，使用 \ 转义。

    * #
    * =
    * \

    以下示例中，设置值的组合如下。

    * key -> a=a
    * key2 -> #不是注释
    * key3 -> text

    .. code-block:: bash

      key = a\=a
      key2 = \#不是注释
      key3 = text

.. tip::

  关于半角空格，config文件不支持仅半角空格的值，但properties文件中可以设置数值引用字符来处理。

  .. code-block:: bash

    key = \u0020

.. tip::

  关于值为空时的行为，config文件中值为空时键不会被读取，但properties文件中作为空字符串处理。
  因此，从组件设置文件引用环境依赖值时行为不同，需要注意。

  定义如下组件设置和环境设置文件时的行为如下。
  
  * 环境设置文件为config文件时 config.value 不存在因此抛出异常。
  * 环境设置文件为properties文件时，组件的 property 设置为空字符串。

  .. code-block:: xml

    <property name="property" value="${config.value}" />

  .. code-block:: bash

    # 值为空的设置值
    config.value=
