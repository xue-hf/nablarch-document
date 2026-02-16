.. _web_thymeleaf_adaptor:

Web应用程序 Thymeleaf适配器
========================================

.. contents:: 目录
  :depth: 3
  :local:

提供在Web应用程序中使用 `Thymeleaf(外部网站) <https://www.thymeleaf.org>`_
作为模板引擎的适配器。

模块列表
--------------

.. code-block:: xml

  <!-- Web应用程序 Thymeleaf适配器 -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-web-thymeleaf-adaptor</artifactId>
  </dependency>
  
.. tip::

  使用Thymeleaf版本3.1.1.RELEASE进行测试。
  要更改版本时，请在项目侧进行测试确认无问题。


进行Web应用程序 Thymeleaf适配器的设置
------------------------------------------------------------------


要使用本适配器，需要在组件配置文件中将
:java:extdoc:`ThymeleafResponseWriter<nablarch.fw.web.handler.responsewriter.thymeleaf.ThymeleafResponseWriter>` 设置到\
:java:extdoc:`HttpResponseHandler<nablarch.fw.web.handler.HttpResponseHandler>` 。

``ThymeleafResponseWriter`` 需要设置Thymeleaf提供的 ``TemplateEngine`` 。

以下显示组件配置文件的设置示例。

.. code-block:: xml

  <component name="templateEngine" class="org.thymeleaf.TemplateEngine" autowireType="None">
    <property name="templateResolver">
      <component class="org.thymeleaf.templateresolver.ClassLoaderTemplateResolver">
        <property name="prefix" value="template/"/>
      </component>
    </property>
  </component>

  <component name="thymeleafResponseWriter"
             class="nablarch.fw.web.handler.responsewriter.thymeleaf.ThymeleafResponseWriter"
             autowireType="None">
    <property name="templateEngine" ref="templateEngine" />
  </component>

  <component name="httpResponseHandler"
             class="nablarch.fw.web.handler.HttpResponseHandler">
    <property name="customResponseWriter" ref="thymeleafResponseWriter"/>
    <!-- 其他设置省略 -->
  </component>


.. tip::

  ``ITemplateResolver`` 接口的实现类中，
  存在 ``org.thymeleaf.templateresolver.ServletContextTemplateResolver`` ，
  但由于以下原因，无法作为组件注册到 :ref:`repository` 。

  * 构造函数参数需要 ``jakarta.servlet.ServletContext`` (没有默认构造函数)。
  * 在系统仓库构建时无法访问 ``jakarta.servlet.ServletContext`` ，也无法通过 :ref:`工厂<repository-factory_injection>` 生成对象。

  因此，请使用 ``ServletContextTemplateResolver`` 以外的其他实现类，如 ``ClassLoaderTemplateResolver`` 等。
  

关于处理对象判定
~~~~~~~~~~~~~~~~~~~~
  
:java:extdoc:`ThymeleafResponseWriter<nablarch.fw.web.handler.responsewriter.thymeleaf.ThymeleafResponseWriter>` 根据\
:java:extdoc:`HttpResponse<nablarch.fw.web.HttpResponse>` 的内容路径内容，
判断是否使用模板引擎输出响应。
默认情况下，如果内容路径以 ``.html`` 结尾，则判定为处理对象并使用模板引擎输出。

例如，假设在Action类中按以下方式返回 ``HttpResponse`` 。

.. code-block:: java

  return new HttpResponse("template/index.html");

在这种情况下，内容路径(\ ``template/index.html``\ )以 ``.html`` 结尾，
因此被判定为模板引擎的输出对象。


未被判定为处理对象时，不会执行模板引擎的输出，\
而是执行Servlet转发。
例如，以下示例中内容路径不以 ``.html`` 结尾，因此执行Servlet转发。

.. code-block:: java

  return new HttpResponse("/path/to/anotherServlet");

  
此处理对象判定条件可以更改。可以在属性\ ``pathPattern`` 中\
设置用于判定的正则表达式(默认值为 ``.*\.html`` )。\
如果内容路径匹配此正则表达式，则判定为模板引擎的处理对象。


.. important::

  在Thymeleaf中，解析模板路径时可以省略后缀设置，
  但使用本适配器时请不要省略后缀。

  * OK: ``return new HttpResponse("index.html");``
  * NG: ``return new HttpResponse("index");``

  如果省略后缀，会话存储到请求范围的转送将不会执行，
  模板将无法引用会话存储的值。



使用模板引擎
------------------------------

使用模板引擎需要创建并放置模板文件。

模板文件的放置位置根据 ``TemplateEngine`` 的设置而异。
在前一节显示的设置示例中，模板文件从类路径加载。
此外，由于 ``ClassLoaderTemplateResolver`` 的属性 ``prefix`` 设置为 ``template/`` ，
因此需要将模板文件放置在类路径上的 ``template`` 目录下。

要使用放置的模板输出响应，需要返回指定模板文件路径的 ``HttpResponse`` 作为Action类的返回值。

例如，假设在 ``src/main/resources/template`` 下放置了 ``index.html`` 模板文件。
在这种情况下，该模板文件在类路径上位于 ``template/index.html`` ，
因此Action类需要返回指定此路径的 ``HttpResponse`` 。

如前面的设置示例那样指定了前缀时，指定省略前缀的路径。

.. code-block:: java

  return new HttpResponse("index.html");


不指定前缀时，直接指定完整路径。

.. code-block:: java

  return new HttpResponse("template/index.html");


这样将使用放置的模板文件输出响应。
