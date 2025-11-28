.. _web_front_controller:

Web前端控制器
==================================================

.. contents:: 目录
  :depth: 3
  :local:

Web应用中作为Handler队列执行起点的类。

通过使用本类，可以将客户端接收到的请求处理委托给handler队列。

模块一览
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web</artifactId>
  </dependency>

配置handler队列
--------------------------------------------------
说明将请求处理委托给handler队列的步骤。

在组件配置文件中进行设置
  将 :java:extdoc:`WebFrontController <nablarch.fw.web.servlet.WebFrontController>` 配置到组件配置文件中，
  并在 :java:extdoc:`handlerQueue <nablarch.fw.HandlerQueueManager.setHandlerQueue(java.util.Collection)>` 属性中
  按顺序添加应用中使用的handler。`

  组件配置文件的设置示例如下。

  要点
   * 组件名称必须为 **webFrontController**。

  .. code-block:: xml

    <component name="webFrontController" class="nablarch.fw.web.servlet.WebFrontController">
      <property name="handlerQueue">
        <list>
          <component class="nablarch.fw.web.handler.HttpCharacterEncodingHandler"/>
          <component class="nablarch.fw.handler.GlobalErrorHandler"/>

          <!-- 省略 -->

        </list>
      </property>
    </component>

设置Servlet过滤器
  将 :java:extdoc:`RepositoryBasedWebFrontController <nablarch.fw.web.servlet.RepositoryBasedWebFrontController>`
  作为Servlet过滤器在 `web.xml` 中进行设置。
  通过该过滤器，客户端接收到的请求处理将被委托给之前在System Repository中注册的handler队列。

  在 `web.xml` 中的设置示例如下。

  要点
   * 为初始化System Repository，需将 :ref:`nablarch_servlet_context_listener` 设置为监听器。

  .. code-block:: xml

    <context-param>
      <param-name>di.config</param-name>
      <param-value>web-boot.xml</param-value>
    </context-param>

    <listener>
      <listener-class>nablarch.fw.web.servlet.NablarchServletContextListener</listener-class>
    </listener>

    <filter>
      <filter-name>entryPoint</filter-name>
      <filter-class>nablarch.fw.web.servlet.RepositoryBasedWebFrontController</filter-class>
    </filter>

    <filter-mapping>
      <filter-name>entryPoint</filter-name>
      <url-pattern>/action/*</url-pattern>
    </filter-mapping>

.. _change_web_front_controller_name:

更改被委托的Web前端控制器名称
--------------------------------------------------

  在基于Web应用的系统中，有时需要将部分请求作为RESTful Web服务进行处理，
  从而同时使用Web应用和Web服务。
  在这种情况下，需要定义多个具有不同Handler结构的Web前端控制器。
  :java:extdoc:`RepositoryBasedWebFrontController <nablarch.fw.web.servlet.RepositoryBasedWebFrontController>` 默认会
  以 ``webFrontController`` 这个名称从System Repository获取被委托的Web前端控制器。
  通过在 `web.xml` 中设置初始化参数，可以更改从System Repository获取的Web前端控制器的名称。

  以下为配置两个分别用于Web应用和RESTful Web服务、具有不同Handler结构的Web前端控制器的示例。

  首先，在组件定义中，将具有Web应用Handler结构的Web前端控制器定义为 ``webFrontController``，
  而将具有RESTful Web服务Handler结构的Web前端控制器以不同于 ``webFrontController`` 的组件名称进行定义。

  .. code-block:: xml

    <component name="webFrontController"
              class="nablarch.fw.web.servlet.WebFrontController">
      <property name="handlerQueue">
        <list>
          <!-- Web应用用的Handler结构 -->
        </list>
      </property>
    </component>

    <component name="jaxrsController"
              class="nablarch.fw.web.servlet.WebFrontController">
      <property name="handlerQueue">
        <list>
          <!-- RESTful Web服务用的Handler结构 -->
        </list>
      </property>
    </component>

  接着，在 `web.xml` 中设置Servlet过滤器，用于使用上述配置的Web前端控制器。

  要点
   * 使用 ``<init-param>``，通过参数名为 ``controllerName`` 的参数设置从System Repository获取的控制器名称。
   * 在 ``<filter-mapping>`` 中设置每个Web前端控制器所处理的URL模式。

  .. code-block:: xml

    <context-param>
      <param-name>di.config</param-name>
      <param-value>web-boot.xml</param-value>
    </context-param>

    <listener>
      <listener-class>nablarch.fw.web.servlet.NablarchServletContextListener</listener-class>
    </listener>

    <filter>
      <filter-name>webEntryPoint</filter-name>
      <filter-class>nablarch.fw.web.servlet.RepositoryBasedWebFrontController</filter-class>
    </filter>
    <filter>
      <filter-name>jaxrsEntryPoint</filter-name>
      <filter-class>nablarch.fw.web.servlet.RepositoryBasedWebFrontController</filter-class>
      <init-param>
        <param-name>controllerName</param-name>
        <param-value>jaxrsController</param-value>
      </init-param>
    </filter>

    <filter-mapping>
      <filter-name>webEntryPoint</filter-name>
      <url-pattern>/action/*</url-pattern>
      <url-pattern>/</url-pattern>
    </filter-mapping>
    <filter-mapping>
      <filter-name>jaxrsEntryPoint</filter-name>
      <url-pattern>/api/*</url-pattern>
    </filter-mapping>

