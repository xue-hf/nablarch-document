.. _router_adaptor:

路由适配器
==================================================

.. contents:: 目录
  :depth: 3
  :local:

使用 `http-request-router(外部网站) <https://github.com/kawasima/http-request-router>`_ ，
进行请求URL与业务Action映射的适配器。

使用本适配器，可以在构建 :ref:`Web应用程序 <web_application>` 和 :ref:`RESTful Web服务 <restful_web_service>` 时，
容易地定义URL与业务Action的映射。

模块列表
--------------------------------------------------
.. code-block:: xml

  <!-- 路由适配器 -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-router-adaptor</artifactId>
  </dependency>

.. tip::
  
  使用http-request-router版本0.1.1进行测试。
  要更改版本时，请在项目侧进行测试确认无问题。

进行使用路由适配器的设置
--------------------------------------------------
以下显示使用本适配器的步骤。

设置调度处理程序
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
将 :java:extdoc:`RoutesMapping <nablarch.integration.router.RoutesMapping>` 作为调度处理程序设置在处理器队列的最后。

以下显示设置示例。

要点
 * 组件名设为 **packageMapping** 。
 * basePackage属性中设置存放Action类的包。
   (Action类存放在多个包时，设置共同的父包。)
 * 将 :java:extdoc:`RoutesMapping <nablarch.integration.router.RoutesMapping>` 设置在初始化对象的列表中。

.. code-block:: xml

  <component name="packageMapping" class="nablarch.integration.router.RoutesMapping">
    <property name="basePackage" value="sample.web.action" />
  </component>

  <component name="webFrontController" class="nablarch.fw.web.servlet.WebFrontController">
    <property name="handlerQueue">
      <list>
        <!-- 其他处理程序省略 -->
        <component-ref name="packageMapping" />
      </list>
    </property>
  </component>

  <component name="initializer"
      class="nablarch.core.repository.initialization.BasicApplicationInitializer">
    <property name="initializeList">
      <list>
        <!-- 其他初始化处理省略 -->
        <component-ref name="packageMapping"/>
      </list>
    </property>
  </component>

创建路由定义文件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
在类路径根目录创建 `routes.xml` ，
设置指定URL与业务Action的映射。

路由定义文件的设置方法请参阅 `库的README文档(外部网站) <https://github.com/kawasima/http-request-router/blob/master/README.ja.md>`_ 。

自动映射业务Action与URL
--------------------------------------------------------
在路由定义文件中，在 `match` 标签的path属性中使用 ``:controller`` 和 ``:action``
等参数，可以进行业务Action与URL的自动映射。

.. important::

  使用 `JBoss` 或 `WildFly` 作为应用服务器时，无法使用此功能。
  请使用 `get` 标签等单独定义业务Action与URL的映射。

.. important::

  不建议将此功能与使用 `get` 标签等的映射个别定义并用。
  因为并用时，业务Action与URL如何映射将变得难以从路由定义文件中读取。

要启用此功能，在类路径根目录创建的 `net/unit8/http/router` 目录中
创建 `routes.properties` ，并按以下方式设置值。

.. code-block:: bash

  router.controllerDetector=nablarch.integration.router.NablarchControllerDetector

以下显示路由定义文件的设置示例和映射示例。

路由定义文件
  .. code-block:: xml

    <routes>
      <match path="/action/:controller/:action" />
    </routes>

业务Action与映射URL的示例
  ========================== ===========================
  业务Action                  URL
  ========================== ===========================
  PersonAction#index         /action/person/index
  PersonAction#search        /action/person/search
  LoginAction#index          /action/login/index
  ProjectUploadAction#index  /action/projectUpload/index
  ========================== ===========================

.. _router_adaptor_path_annotation:

使用Jakarta RESTful Web Services的Path注解进行映射
--------------------------------------------------------------------
从本适配器版本1.2.0开始，可以使用Jakarta RESTful Web Services的 ``jakarta.ws.rs.Path`` 注解（以下简称为 ``Path`` 注解）进行路由映射。

这里说明如何对现有的 :ref:`RESTful Web服务 <restful_web_service>` 启用使用 ``Path`` 注解的路由，以及各种设置的详细信息。

.. important::

  本功能无法在类路径下资源由独立文件系统管理的部分Web应用服务器中使用。

  例如，在Jboss和Wildfly中，类路径下的资源由称为vfs的虚拟文件系统管理，
  因此无法搜索被 ``Path`` 注解注釈的类。

  使用此类Web应用服务器时，请使用传统的XML路由定义。

更改调度处理程序
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
使用XML映射定义时，使用 :java:extdoc:`RoutesMapping <nablarch.integration.router.RoutesMapping>` 作为调度处理程序的实现。
另一方面，使用 ``Path`` 注解的映射定义时，需要将 :java:extdoc:`PathOptionsProviderRoutesMapping <nablarch.integration.router.PathOptionsProviderRoutesMapping>` 设置为调度处理程序。

.. code-block:: xml

  <!-- 启用Path注解路由定义的设置示例 -->
  <component name="packageMapping" class="nablarch.integration.router.PathOptionsProviderRoutesMapping">
    <property name="pathOptionsProvider">
      <component class="nablarch.integration.router.jaxrs.JaxRsPathOptionsProvider">
        <property name="applicationPath" value="${nablarch.webApi.applicationPath}" />
        <property name="basePackage" value="${nablarch.commonProperty.basePackage}" />
      </component>
    </property>

    <property name="methodBinderFactory">
      <component class="nablarch.fw.jaxrs.JaxRsMethodBinderFactory">
        <property name="handlerList">
          <component class="nablarch.integration.jaxrs.jersey.JerseyJaxRsHandlerListFactory"/>
        </property>
      </component>
    </property>
  </component>

  <!-- 处理器队列构成 -->
  <component name="webFrontController" class="nablarch.fw.web.servlet.WebFrontController">
    <property name="handlerQueue">
      <list>
        <!-- 省略 -->
        <component-ref name="packageMapping"/>
      </list>
    </property>
  </component>

| 要使用 ``Path`` 注解的路由，需要在 :java:extdoc:`PathOptionsProviderRoutesMapping <nablarch.integration.router.PathOptionsProviderRoutesMapping>` 的 ``pathOptionsProvider`` 属性中设置 :java:extdoc:`JaxRsPathOptionsProvider <nablarch.integration.router.jaxrs.JaxRsPathOptionsProvider>` 。
| （关于 ``methodBinderFactory`` 属性的设置请参阅 :ref:`jaxrs_adaptor` ）

此外，需要对此 :java:extdoc:`JaxRsPathOptionsProvider <nablarch.integration.router.jaxrs.JaxRsPathOptionsProvider>` 设置以下2个属性。

**applicationPath**

  | 设置映射路径共同的前缀。
  | 这与Jakarta RESTful Web Services的 ``jakarta.ws.rs.ApplicationPath`` 注解中设置的值含义相同。

**basePackage**

  | 设置作为搜索被 ``Path`` 注解设置的类的根包名。


定义的 :java:extdoc:`PathOptionsProviderRoutesMapping <nablarch.integration.router.PathOptionsProviderRoutesMapping>` 组件需要初始化，因此请添加到初始化对象的列表中。

.. code-block:: xml

  <component name="initializer"
             class="nablarch.core.repository.initialization.BasicApplicationInitializer">
    <property name="initializeList">
      <list>
        <component-ref name="packageMapping" />
        <!-- 省略 -->
      </list>
    </property>
  </component>

通过以上设置，即可使用 ``Path`` 注解的路由注册功能。

映射的实现方法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
以下显示使用 ``Path`` 注解定义映射的实现示例。

.. code-block:: java

    @Path("/sample")
    public class SampleAction {

        @GET
        @Produces(MediaType.APPLICATION_JSON)
        public List<Person> findAll() {
            // 省略
        }

        @POST
        @Produces(MediaType.APPLICATION_JSON)
        public int register(JaxRsHttpRequest request) {
            // 省略
        }
    }

| 使用 ``Path`` 注解注釈Action类，可以通过 ``Path`` 注解的 ``value`` 中设置的路径与Action类关联。
| 此外，使用 ``jakarta.ws.rs.GET`` 等表示HTTP方法的注解注釈Action类的方法，可以将HTTP方法与Action类的方法关联。

在上述实现示例中，HTTP请求将按以下方式调度。


============ ============== ============================
路径          HTTP方法        调度的方法
============ ============== ============================
``/sample``   ``GET``        ``SampleAction#findAll()``
``/sample``   ``POST``       ``SampleAction#register(JaxRsHttpRequest)``
============ ============== ============================

.. tip::
 用于关联HTTP方法的注解，标准中提供了以下注解。

  * ``jakarta.ws.rs.DELETE``
  * ``jakarta.ws.rs.GET``
  * ``jakarta.ws.rs.HEAD``
  * ``jakarta.ws.rs.OPTIONS``
  * ``jakarta.ws.rs.PATCH``
  * ``jakarta.ws.rs.POST``
  * ``jakarta.ws.rs.PUT``

此外，如下所示使用 ``Path`` 注解注釈方法，还可以定义子路径的映射。

.. code-block:: java

    @Path("/sample")
    public class TestAction {

        @GET
        @Path("/foo")
        @Produces(MediaType.APPLICATION_JSON)
        public Person foo() {
            // 省略
        }

        @GET
        @Path("/bar")
        @Produces(MediaType.APPLICATION_JSON)
        public Person bar() {
            // 省略
        }
    }

此时，HTTP请求的调度如下所示。

================ ============== ============================
路径              HTTP方法        调度的方法
================ ============== ============================
``/sample/foo``   ``GET``       ``TestAction#foo()``
``/sample/bar``   ``GET``       ``TestAction#bar()``
================ ============== ============================

路径参数的定义
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
如下所示，还可以在路径中包含参数。

.. code-block:: java

    @Path("/sample")
    public class TestAction {

        @GET
        @Path("/foo/{param}")
        @Produces(MediaType.APPLICATION_JSON)
        public Person foo(JaxRsHttpRequest request) {
            String param = request.getPathParam("param");
            // 省略
        }

        @GET
        @Path("/bar/{id : \\d+}")
        @Produces(MediaType.APPLICATION_JSON)
        public Person bar(JaxRsHttpRequest request) {
            int id = Integer.parseInt(request.getPathParam("id");
            // 省略
        }
    }

| 路径参数不使用http-request-router的记述方式，而是遵循Jakarta RESTful Web Services的规格记述。
| 这是因为本功能（ ``Path`` 注解路由定义）遵循Jakarta RESTful Web Services的规格。

| 将路径的一部分记述为 ``{参数名}`` ，即可将该部分定义为参数。
| 通过将此处定义的参数名传递给 :java:extdoc:`JaxRsHttpRequest#getPathParam(String) <nablarch.fw.jaxrs.JaxRsHttpRequest.getPathParam(java.lang.String)>` ，可以获取路径参数的值。

| 此外，记述为 ``{参数名 : 正则表达式}`` ，可以使用正则表达式定义该路径参数的格式。
| 上述实现示例中指定了 ``\\d+`` 正则表达式，因此只有当路径的值为数值时才会调度到该方法。

HTTP请求调度示例如下。

===================== ============== ============================
路径                   HTTP方法        调度的方法
===================== ============== ============================
``/sample/foo/hello`` ``GET``        ``TestAction#foo(JaxRsHttpRequest)``
``/sample/foo/world`` ``GET``        ``TestAction#foo(JaxRsHttpRequest)``
``/sample/bar/123``   ``GET``        ``TestAction#bar(JaxRsHttpRequest)``
``/sample/bar/987``   ``GET``        ``TestAction#bar(JaxRsHttpRequest)``
===================== ============== ============================

继承接口和父类的注解
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Action类可以继承实现的接口或继承的父类中被 ``Path`` 注解注釈的内容以及方法中被注釈的注解内容。

以下显示实现示例。

.. code-block:: java

    @Path("/sample")
    public interface TestApi {

        @GET
        @Path("/foo/{param}")
        @Produces(MediaType.APPLICATION_JSON)
        Person foo(JaxRsHttpRequest request);

        @GET
        @Path("/bar/{id : \\d+}")
        @Produces(MediaType.APPLICATION_JSON)
        Person bar(JaxRsHttpRequest request);
    }

    public class TestAction implements TestApi {

        @Override
        public Person foo(JaxRsHttpRequest request) {
            String param = request.getPathParam("param");
            // 省略
        }

        @Override
        public Person bar(JaxRsHttpRequest request) {
            int id = Integer.parseInt(request.getPathParam("id");
            // 省略
        }
    }

在上述实现示例中， ``TestApi`` 接口中定义了路径参数和HTTP方法，方法实现在 ``TestAction`` 类中进行。 ``TestAction`` 类的方法没有被 ``Path`` 注解或HTTP方法相关注解注釈，但执行时会使用 ``TestApi`` 接口方法中被注釈的注解作为定义。

.. tip::
  
  在此机制中，类型定义中被 ``Path`` 注解注釈的类或接口非常重要。

  如果Action类继承了其他类或实现了接口，则会遍历该层次结构，
  找到第一个 ``Path`` 注解在类型定义中被注釈的类或接口，
  将该类或接口中声明的被注解注釈的方法识别为接收请求的方法。

以下显示说明补充内容的实现示例。

.. code-block:: java

    @Path("/sample")  // Path注解在类型定义中被注釈
    public interface TestApi {
        // TestApi接口的Path注解在类型定义中被注釈，因此foo方法被识别为接收请求的方法
        @GET
        @Path("/foo/{param}")
        @Produces(MediaType.APPLICATION_JSON)
        Person foo(JaxRsHttpRequest request);
    }

    public class TestAction implements TestApi {

        @Override
        public Person foo(JaxRsHttpRequest request) {
            // 省略
        }

        // TestAction类没有被Path注解注釈，因此bar方法不会被识别为接收请求的方法
        @GET
        @Path("/bar/{id : \\d+}")
        @Produces(MediaType.APPLICATION_JSON)
        public Person bar(JaxRsHttpRequest request) {
            // 省略
        }
    }

此示例中， ``TestApi`` 接口被 ``Path`` 注解注釈，
因此 ``foo`` 方法被识别为接收请求的方法，而 ``TestAction`` 类中声明的 ``bar`` 方法虽然被 ``@GET`` 等注解注釈，但作为接收请求的方法会被忽略。

=============================== ======================== ======================================
类或接口                        声明的方法               能否接收请求？
=============================== ======================== ======================================
``TestApi``                     ``foo``                  ○
``TestAction``                  ``bar``                  ×
=============================== ======================== ======================================

请注意，哪个类型定义被 ``Path`` 注解注釈，以及该类中是否定义了被注解注釈的方法，决定了哪个方法接收请求。

一览确认路由定义
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:java:extdoc:`PathOptionsProviderRoutesMapping <nablarch.integration.router.PathOptionsProviderRoutesMapping>` 读取的路由定义将在初始化时以调试级别输出到日志。

默认情况下，路由列表将按以下方式输出到日志。

.. code-block:: text

    2020-07-20 13:35:53.092 -DEBUG- nablarch.integration.router.PathOptionsProviderRoutesMapping [null] boot_proc = [] proc_sys = [jaxrs] req_id = [null] usr_id = [null] GET /api/bar => com.example.BarAction#findAll
    GET /api/bar/fizz => com.example.BarAction#fizz
    GET /api/foo => com.example.FooAction#findAll
    POST /api/foo => com.example.FooAction#register
    DELETE /api/foo/(:id) => com.example.FooAction#delete
    GET /api/foo/(:id) => com.example.FooAction#find
    POST /api/foo/(:id) => com.example.FooAction#update

要更改日志格式，请创建实现 :java:extdoc:`PathOptionsFormatter <nablarch.integration.router.PathOptionsFormatter>` 的类，
并设置在 :java:extdoc:`PathOptionsProviderRoutesMapping <nablarch.integration.router.PathOptionsProviderRoutesMapping>` 的 ``pathOptionsFormatter`` 属性中。

.. code-block:: xml

  <component name="packageMapping" class="nablarch.integration.router.PathOptionsProviderRoutesMapping">
    <property name="methodBinderFactory">
      <!-- 省略 -->
    </property>
    <property name="pathOptionsProvider">
      <!-- 省略 -->
    </property>

    <property name="pathOptionsFormatter">
      <!-- 设置自定义的格式类 -->
      <component class="com.example.CustomPathOptionsFormatter" />
    </property>
  </component>
