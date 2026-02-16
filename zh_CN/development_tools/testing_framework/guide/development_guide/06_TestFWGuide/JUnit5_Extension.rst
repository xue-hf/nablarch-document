.. _ntf_junit5_extension:

========================================
 JUnit 5用扩展功能
========================================

.. contents:: 目录
  :depth: 3
  :local:

-----
概要
-----

这里说明在JUnit 5编写的测试中使用自动化测试框架的扩展功能。
使用本扩展功能，可以将参数化测试等JUnit 5提供的便利功能与自动化测试框架组合使用。

.. tip::
  即使引入本扩展功能，也不需要修改JUnit 4编写的现有自动化测试框架的测试。
  JUnit 4编写的测试可以通过使用JUnit Vintage继续在JUnit 5上执行（关于使用JUnit Vintage使自动化测试框架运行的方法，请参考 :ref:`run_ntf_on_junit5_with_vintage_engine` ）。
  因此，可以保持现有测试为JUnit 4代码，仅将新测试改为使用JUnit 5的代码。

----------
前提条件
----------

使用JUnit 5需要满足以下条件。

* maven-surefire-plugin 的 2.22.0 以上

此外，本页面假设您已具备JUnit 5的引入方法和测试用例创建方法等基础知识，因此不记载这些步骤。
关于JUnit 5本身的信息，请参考 `官方用户指南（外部网站、英语） <https://junit.org/junit5/docs/5.11.0/user-guide/>`_ 。

---------------
模块一览
---------------

.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-testing-junit5</artifactId>
    <scope>test</scope>
  </dependency>

.. _ntf_junit5_extension_standard_usages:

---------------
基本使用方法
---------------

自动化测试框架提供实现了 :java:extdoc:`TestSupport <nablarch.test.TestSupport>` 等测试所需功能的类。
传统的JUnit 4中，测试类继承这些自动化测试框架提供的类，从而可以从测试类使用提供类具有的功能。

本扩展功能在扩展功能侧生成自动化测试框架提供类的实例，并提供注入到测试类的机制。
此机制使用JUnit 5的 `Extension (外部网站、英语) <https://junit.org/junit5/docs/5.11.0/user-guide/#extensions>`_ 。

本扩展功能为自动化测试框架提供的每个类准备了 **Extension 类** 和 **组合注解** 。
例如， :java:extdoc:`TestSupport <nablarch.test.TestSupport>` 有 :java:extdoc:`TestSupportExtension <nablarch.test.junit5.extension.TestSupportExtension>` 和 :java:extdoc:`NablarchTest <nablarch.test.junit5.extension.NablarchTest>` 。

.. tip::
  组合注解是JUnit 5提供的功能，可以将多个注解的设置汇总到另一个1个注解中。
  详情请参考 `官方指南的「2.1.1. Meta-Annotations and Composed Annotations」(外部网站、英语) <https://junit.org/junit5/docs/5.11.0/user-guide/#writing-tests-meta-annotations>`_ 。


通过使用这些类按以下方式实现，可以在测试中使用 :java:extdoc:`TestSupport <nablarch.test.TestSupport>` 。

.. code-block:: java

  // 1. 在测试类上设置对应的组合注解
  @NablarchTest
  class YourTest {
      // 2. 将要使用的类声明为测试类的字段
      TestSupport support;

      @Test
      void test() {
          ...
          // 3. 在测试内使用
          Map<String, String> map = support.getMap(sheetName, id);
          ...
      }
  }

在测试类中使用 :java:extdoc:`TestSupport <nablarch.test.TestSupport>` 时，首先在测试类上设置对应的组合注解(:java:extdoc:`NablarchTest <nablarch.test.junit5.extension.NablarchTest>`)。
这样， :java:extdoc:`TestSupportExtension <nablarch.test.junit5.extension.TestSupportExtension>` 将应用于测试类。

接下来，在测试类中声明 :java:extdoc:`TestSupport <nablarch.test.TestSupport>` 类型的实例字段。
此时，实例字段的可见性不限。

扩展功能在测试执行前生成对应的类（这里是 :java:extdoc:`TestSupport <nablarch.test.TestSupport>` ）的实例。
然后，找到可赋值给测试类的字段时，自动注入实例。

.. warning::

  如果作为注入目标的字段不为null，扩展功能将错误终止，因此请勿设置值。

---------------------------------------------
Extension 类和组合注解一览
---------------------------------------------

本扩展功能提供以下Extension类和组合注解。


.. list-table:: 扩展功能提供的Extension类和组合注解一览
   :header-rows: 1

   * - 自动化测试框架提供的类
     - Extension 类
     - 组合注解
   * - :java:extdoc:`TestSupport <nablarch.test.TestSupport>`
     - :java:extdoc:`TestSupportExtension <nablarch.test.junit5.extension.TestSupportExtension>`
     - :java:extdoc:`NablarchTest <nablarch.test.junit5.extension.NablarchTest>`
   * - :java:extdoc:`BatchRequestTestSupport <nablarch.test.core.batch.BatchRequestTestSupport>`
     - :java:extdoc:`BatchRequestTestExtension <nablarch.test.junit5.extension.batch.BatchRequestTestExtension>`
     - :java:extdoc:`BatchRequestTest <nablarch.test.junit5.extension.batch.BatchRequestTest>`
   * - :java:extdoc:`DbAccessTestSupport <nablarch.test.core.db.DbAccessTestSupport>`
     - :java:extdoc:`DbAccessTestExtension <nablarch.test.junit5.extension.db.DbAccessTestExtension>`
     - :java:extdoc:`DbAccessTest <nablarch.test.junit5.extension.db.DbAccessTest>`
   * - :java:extdoc:`EntityTestSupport <nablarch.test.core.db.EntityTestSupport>`
     - :java:extdoc:`EntityTestExtension <nablarch.test.junit5.extension.db.EntityTestExtension>`
     - :java:extdoc:`EntityTest <nablarch.test.junit5.extension.db.EntityTest>`
   * - :java:extdoc:`BasicHttpRequestTestTemplate <nablarch.test.core.http.BasicHttpRequestTestTemplate>`
     - :java:extdoc:`BasicHttpRequestTestExtension <nablarch.test.junit5.extension.http.BasicHttpRequestTestExtension>`
     - :java:extdoc:`BasicHttpRequestTest <nablarch.test.junit5.extension.http.BasicHttpRequestTest>`
   * - :java:extdoc:`HttpRequestTestSupport <nablarch.test.core.http.HttpRequestTestSupport>`
     - :java:extdoc:`HttpRequestTestExtension <nablarch.test.junit5.extension.http.HttpRequestTestExtension>`
     - :java:extdoc:`HttpRequestTest <nablarch.test.junit5.extension.http.HttpRequestTest>`
   * - :java:extdoc:`RestTestSupport <nablarch.test.core.http.RestTestSupport>`
     - :java:extdoc:`RestTestExtension <nablarch.test.junit5.extension.http.RestTestExtension>`
     - :java:extdoc:`RestTest <nablarch.test.junit5.extension.http.RestTest>`
   * - :java:extdoc:`SimpleRestTestSupport <nablarch.test.core.http.SimpleRestTestSupport>`
     - :java:extdoc:`SimpleRestTestExtension <nablarch.test.junit5.extension.http.SimpleRestTestExtension>`
     - :java:extdoc:`SimpleRestTest <nablarch.test.junit5.extension.http.SimpleRestTest>`
   * - :java:extdoc:`IntegrationTestSupport <nablarch.test.core.integration.IntegrationTestSupport>`
     - :java:extdoc:`IntegrationTestExtension <nablarch.test.junit5.extension.integration.IntegrationTestExtension>`
     - :java:extdoc:`IntegrationTest <nablarch.test.junit5.extension.integration.IntegrationTest>`
   * - :java:extdoc:`MessagingReceiveTestSupport <nablarch.test.core.messaging.MessagingReceiveTestSupport>`
     - :java:extdoc:`MessagingReceiveTestExtension <nablarch.test.junit5.extension.messaging.MessagingReceiveTestExtension>`
     - :java:extdoc:`MessagingReceiveTest <nablarch.test.junit5.extension.messaging.MessagingReceiveTest>`
   * - :java:extdoc:`MessagingRequestTestSupport <nablarch.test.core.messaging.MessagingRequestTestSupport>`
     - :java:extdoc:`MessagingRequestTestExtension <nablarch.test.junit5.extension.messaging.MessagingRequestTestExtension>`
     - :java:extdoc:`MessagingRequestTest <nablarch.test.junit5.extension.messaging.MessagingRequestTest>`

BasicHttpRequestTest 使用方法的补充
====================================

除 :java:extdoc:`BasicHttpRequestTestTemplate <nablarch.test.core.http.BasicHttpRequestTestTemplate>` 外，其他都可以在 :ref:`ntf_junit5_extension_standard_usages` 中说明的方法使用。

只有 :java:extdoc:`BasicHttpRequestTestTemplate <nablarch.test.core.http.BasicHttpRequestTestTemplate>` 在使用组合注解 :java:extdoc:`BasicHttpRequestTest <nablarch.test.junit5.extension.http.BasicHttpRequestTest>` 时需要指定参数，因此对此进行补充。

.. code-block:: java

  // 1. 指定 BasicHttpRequestTest 的 baseUri
  @BasicHttpRequestTest(baseUri = "/test/")
  class YourTestClass {
      // 2. BasicHttpRequestTestTemplate 的注入方法与其他相同
      BasicHttpRequestTestTemplate support;

      @Test
      void test() {
          support.execute();
      }
  }

:java:extdoc:`BasicHttpRequestTest <nablarch.test.junit5.extension.http.BasicHttpRequestTest>` 注解需要指定 ``baseUri`` 。
此值对应于 :java:extdoc:`AbstractHttpRequestTestTemplate <nablarch.test.core.http.AbstractHttpRequestTestTemplate>` 的 ``getBaseUri()`` 方法返回的值。

-------------------
添加自定义扩展
-------------------

说明继承自动化测试框架提供的类并添加自定义扩展时的对应方法。

.. tip::
  这里说明的步骤也适用于将JUnit 4编写的现有自定义扩展类用于本扩展功能时。

创建自定义扩展类时，大致按以下步骤对应。

#. 继承自动化测试框架提供的类，创建自定义扩展类
#. 继承继承源类对应的Extension类，创建用于自定义扩展的Extension，实现生成自定义扩展类实例
#. 使用 ``ExtendWith`` 注解将自定义Extension类应用于测试类

创建自定义扩展类
========================

这里以继承 :java:extdoc:`TestSupport <nablarch.test.TestSupport>` 创建类为例说明。

首先，创建继承 :java:extdoc:`TestSupport <nablarch.test.TestSupport>` 的自定义扩展类。

.. code-block:: java

  public class CustomTestSupport extends TestSupport {
      // 实现使测试类的 Class 实例可以传递给 TestSupport 的构造函数
      public CustomTestSupport(Class<?> testClass) {
          super(testClass);
      }

      // 实现自定义的扩展方法
  }

基本上，自动化测试框架提供的类在生成实例时需要传递测试类的 ``Class`` 对象。
因此，自定义扩展类需要在构造函数中定义可以接收测试类 ``Class`` 对象的构造函数。

.. tip::
  :java:extdoc:`SimpleRestTestSupport <nablarch.test.core.http.SimpleRestTestSupport>` 无需在构造函数中传递测试类的 ``Class`` 对象也可以使用。

创建用于自定义扩展的Extension
====================================

接下来，继承扩展源类对应的Extension类，创建用于自定义扩展的Extension。
示例中继承的是 :java:extdoc:`TestSupport <nablarch.test.TestSupport>` ，因此对应的Extension类是 :java:extdoc:`TestSupportExtension <nablarch.test.junit5.extension.TestSupportExtension>` 。

.. tip::
  直接使用继承 :java:extdoc:`AbstractHttpRequestTestTemplate <nablarch.test.core.http.AbstractHttpRequestTestTemplate>` 的自定义扩展类时，作为对应的Extension可以使用 :java:extdoc:`BasicHttpRequestTestExtension <nablarch.test.junit5.extension.http.BasicHttpRequestTestExtension>` 。

.. code-block:: java

  public class CustomTestSupportExtension extends TestSupportExtension {
  
      // 覆盖 createSupport() ，实现返回自定义扩展类实例
      @Override
      protected TestEventDispatcher createSupport(Object testInstance, ExtensionContext context) {
          return new CustomTestSupport(testInstance.getClass());
      }
  }

在用于自定义扩展的Extension中，覆盖 ``createSupport()`` 方法。
然后，实现返回先前创建的自定义扩展类实例。

此外， ``createSupport()`` 方法生成的自定义扩展类实例保存在父类 :java:extdoc:`TestEventDispatcherExtension <nablarch.test.junit5.extension.event.TestEventDispatcherExtension>` 中定义的 ``support`` 这个 :java:extdoc:`TestEventDispatcher <nablarch.test.event.TestEventDispatcher>` 型实例字段中。
此字段为 ``protected`` ，因此可以从子类引用。


使用ExtendWith应用于测试类
====================================

创建的用于自定义扩展的Extension，可以使用 ``ExtendWith`` 注解应用于测试类。
以下显示实现示例。

.. code-block:: java

  ..
  import org.junit.jupiter.api.extension.ExtendWith;
  
  // 1. 使用 ExtendWith 将用于自定义扩展的Extension应用于测试类
  @ExtendWith(CustomTestSupportExtension.class)
  class YourTest {
      // 2. 将自定义扩展类声明为实例变量
      CustomTestSupport support;

      @Test
      void test() {
          // 3. 在测试内使用自定义扩展类
          support.customMethod();
      }
  }

扩展BasicHttpRequestTestTemplate时也需要创建注解
====================================================================

扩展 :java:extdoc:`BasicHttpRequestTestTemplate <nablarch.test.core.http.BasicHttpRequestTestTemplate>` 或 :java:extdoc:`AbstractHttpRequestTestTemplate <nablarch.test.core.http.AbstractHttpRequestTestTemplate>` 时，需要将 ``baseUri`` 传递给自定义扩展类的实例。
``ExtendWith`` 无法传递参数，因此也需要单独创建注解。

以下显示在 :java:extdoc:`BasicHttpRequestTestTemplate <nablarch.test.core.http.BasicHttpRequestTestTemplate>` 中的实现示例。

.. code-block:: java

  public class CustomHttpRequestTestSupport extends BasicHttpRequestTestTemplate {
      private final String baseUri;
     
      // 实现使 baseUri 可以从外部传递
      public CustomHttpRequestTestSupport(Class<?> testClass, String baseUri) {
          super(testClass);
          this.baseUri = baseUri;
      }
  
      @Override
      protected String getBaseUri() {
          return baseUri;
      }
  }

首先，继承 :java:extdoc:`BasicHttpRequestTestTemplate <nablarch.test.core.http.BasicHttpRequestTestTemplate>` 创建自定义扩展类。
此时，在构造函数中实现可以传递测试类和 ``baseUri`` 。

接下来，创建用于自定义扩展类的组合注解。

.. code-block:: java

  import org.junit.jupiter.api.extension.ExtendWith;
  
  import java.lang.annotation.ElementType;
  import java.lang.annotation.Retention;
  import java.lang.annotation.RetentionPolicy;
  import java.lang.annotation.Target;
  
  @Retention(RetentionPolicy.RUNTIME)
  @Target(ElementType.TYPE)
  // 指定此后创建的用于自定义扩展的Extension
  @ExtendWith(CustomHttpRequestTestExtension.class)
  public @interface CustomHttpRequestTest {
      // 声明可以传递 baseUri
      String baseUri();
  }

在组合注解中，声明可以传递 ``baseUri`` 。
``ExtendWith`` 中指定的用于自定义扩展的Extension，按以下方式实现。

.. code-block:: java

  public class CustomHttpRequestTestExtension extends BasicHttpRequestTestExtension {
  
      @Override
      protected TestEventDispatcher createSupport(Object testInstance, ExtensionContext context) {
          // 从测试类获取注解信息
          CustomHttpRequestTest annotation = findAnnotation(testInstance, CustomHttpRequestTest.class);
          // 将 baseUri 信息传递给自定义扩展类的构造函数
          return new CustomHttpRequestTestSupport(testInstance.getClass(), annotation.baseUri());
      }
  }

使用 ``findAnnotation(Object, Class)`` 可以获取测试类上设置的注解信息。
利用此功能可以将 ``baseUri`` 的值传递给自定义扩展类。

最后，使用自定义的组合注解按以下方式实现，可以使用继承 :java:extdoc:`BasicHttpRequestTestTemplate <nablarch.test.core.http.BasicHttpRequestTestTemplate>` 的自定义扩展类。

.. code-block:: java

  // 在测试类上设置自定义的组合注解（也设置 baseUri ）
  @CustomHttpRequestTest(baseUri = "/custom/")
  class YourTest {
      // 将自定义扩展类声明为字段
      CustomHttpRequestTestSupport support;
  
      @Test
      void test() {
          // 在测试中使用自定义扩展类
          support.customMethod();
      }
  }

实现事前处理・事后处理
=============================

在用于自定义扩展的Extension中，通过覆盖以下方法可以实现测试的事前处理・事后处理。

* beforeAll
* beforeEach
* afterAll
* afterEach

``beforeAll`` 和 ``afterAll`` 可以实现测试类整体的事前・事后处理。
而 ``beforeEach`` 和 ``afterEach`` 可以实现每个测试方法的事前・事后处理。

覆盖各方法时，必须按以下方式执行父类的同名方法。
否则，父类中定义的事前・事后处理将不会被调用。

.. code-block:: java

  @Override
  public void beforeAll(ExtensionContext context) {
      // 务必首先执行父类方法
      super.beforeAll(context);

      // 实现自定义的事前处理
      ...
  }

重现JUnit 4的TestRule
=============================

说明现有项目等中创建的自定义扩展类中使用JUnit 4的 ``TestRule`` 时，移植到本扩展功能的方法。

例如，假设存在以下自定义扩展类。

.. code-block:: java

  import org.junit.Rule;
  import org.junit.rules.Timeout;
  import java.util.concurrent.TimeUnit;
  
  public class CustomTestSupport extends TestSupport {
      // 使用JUnit 4的TestRule
      @Rule
      public Timeout timeout = new Timeout(1000, TimeUnit.MILLISECONDS);
  
      public CustomTestSupport(Class<?> testClass) {
          super(testClass);
      }
  }

将此移植到本扩展功能时，按以下方式实现用于自定义扩展的Extension类。

.. code-block:: java

  public class CustomTestSupportExtension extends TestSupportExtension {
  
      @Override
      protected TestEventDispatcher createSupport(Object testInstance, ExtensionContext context) {
          return new CustomTestSupport(testInstance.getClass());
      }
  
      // 1. 覆盖 resolveTestRules 方法
      @Override
      protected List<TestRule> resolveTestRules() {
          // 2. 基于父类 resolveTestRules() 的结果生成列表
          List<TestRule> rules = new ArrayList<>(super.resolveTestRules());
          // 3. 将自定义扩展类中定义的TestRule添加到列表
          rules.add(((CustomTestSupport) support).timeout);
          // 4. 返回生成的列表
          return rules;
      }
  }

在用于自定义扩展的Extension中，可以覆盖 ``resolveTestRules()`` 方法。
在此方法中，实现将要重现的JUnit 4 ``TestRule`` 以列表形式返回。
这样，即使在JUnit 5的测试上也能重现JUnit 4的 ``TestRule`` 。

此外，覆盖 ``resolveTestRules()`` 时，务必以父类 ``resolveTestRules()`` 返回的列表为基础。
否则，父类中注册的 ``TestRule`` 将不会被重现。


-------------------------------
使用RegisterExtension
-------------------------------

在JUnit 5中，提供了RegisterExtension机制用于程序性地生成Extension实例并应用于测试类。

.. tip::
  关于RegisterExtension的说明，请参考 `官方指南的「5.2.2. Programmatic Extension Registration」(外部网站、英语) <https://junit.org/junit5/docs/5.11.0/user-guide/#extensions-registration-programmatic>`_ 。

本扩展功能提供的Extension也可以使用RegisterExtension。
但是，此时务必使用static字段。
如果使用实例字段， ``beforeAll`` 和 ``afterAll`` 等处理将不会执行，导致Extension无法正常工作。

以下显示实现示例。

.. code-block:: java

  class YourTest {
      // 1. 在 static 字段中使用 RegisterExtension
      @RegisterExtension
      static TestSupportExtension extension = new TestSupportExtension();
  
      // 2. 声明自动化测试框架提供类的实例字段
      TestSupport support;
  
      @Test
      void test() {
          // 3. 在测试中使用 support
          ...
      }
  }

