.. _nablarch_servlet_context_listener:

Nablarch Servlet 上下文初始化监听器
==================================================

.. contents:: 目录
  :depth: 3
  :local:

本类作为 Servlet Context Listener 进行定义，在Web应用启动和关闭时执行以下处理。

启动时
 * :ref:`repository` 的初始化处理
 * :ref:`log` 的初始化处理

关闭时
 * :ref:`log` 的终止处理

模块列表
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web</artifactId>
  </dependency>
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core</artifactId>
  </dependency>
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-repository</artifactId>
  </dependency>
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-applog</artifactId>
  </dependency>

初始化 System Repository
--------------------------------------------------

要初始化 System Repository，需进行以下配置：

 * 将本类注册为 Servlet Context Listener。
 * 将组件配置文件的路径作为 Servlet Context 的初始化参数进行设置。

在 `web.xml` 中的配置示例如下：

要点
 * 参数名称必须为 **di.config**。

.. code-block:: xml

  <context-param>
    <param-name>di.config</param-name>
    <param-value>web-boot.xml</param-value>
  </context-param>

  <listener>
    <listener-class>nablarch.fw.web.servlet.NablarchServletContextListener</listener-class>
  </listener>

在后续处理中获取初始化结果
--------------------------------------------------

可通过调用 :java:extdoc:`NablarchServletContextListener#isInitializationCompleted <nablarch.fw.web.servlet.NablarchServletContextListener.isInitializationCompleted()>` 方法，
判断本类的初始化是否成功。若初始化成功，该方法将返回 ``true``。

当本类初始化失败时，整个应用的启动也会失败。但在注册了多个 Servlet Context Listener 的情况下，
后续的 Listener 仍有可能被执行。利用此功能，可在后续的 Listener 中实现如下逻辑：
仅当 System Repository 初始化成功时才继续执行处理。

.. code-block:: java

  public class CustomServletContextListener implements ServletContextListener {
      @Override
      public void contextInitialized(ServletContextEvent sce) {
          if(NablarchServletContextListener.isInitializationCompleted()){
            // 执行依赖 System Repository 的处理
          }
      }

需要注意的是，Servlet Context Listener 的执行顺序由其在 `web.xml` 中的声明顺序决定。
若注册的 Listener 需要使用 System Repository，则必须在 `web.xml` 中将其声明在本类之后，如下所示。
此外，使用 ``@WebListener`` 注解注册的 Listener 无法保证执行顺序，
因此必须通过 `web.xml` 显式定义。

.. code-block:: xml

  <listener>
    <listener-class>nablarch.fw.web.servlet.NablarchServletContextListener</listener-class>
  </listener>
  <listener>
    <listener-class>please.change.me.CustomServletContextListener</listener-class>
  </listener>

.. tip::

  当注册了多个 Servlet Context Listener 时，若前一个 Listener 抛出异常，后续处理是中止还是继续，
  取决于具体的 Servlet 容器实现。