.. _on_error_interceptor:

OnError 拦截器
============================

.. contents:: 目录
  :depth: 3
  :local:

在业务Action发生异常时，返回指定响应的拦截器。

使用 :ref:`inject_form_interceptor` 进行输入值检查时，
也需要将此拦截器配置在 :ref:`inject_form_interceptor` 之前执行，
以便可以指定验证错误对应的响应。

通过在业务Action方法上设置 :java:extdoc:`OnError <nablarch.fw.web.interceptor.OnError>` 来启用此拦截器。

.. tip::

  如需指定多个异常对应的响应，请使用 :ref:`on_errors_interceptor` 。

.. important::

  不能为单一异常指定多个响应。
  如需为异常指定多个响应，请参考 :ref:`on_error-multiple` 。
  
拦截器类名
--------------------------------------------------
* :java:extdoc:`nablarch.fw.web.interceptor.OnError`

模块列表
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web</artifactId>
  </dependency>

使用 OnError
--------------------------------------------------
将 :java:extdoc:`OnError <nablarch.fw.web.interceptor.OnError>` 注解设置在业务Action处理请求的方法上。

以下示例中，指定了业务Action方法内发生业务错误( `ApplicationException` )时的跳转目标。

要点
 * type属性可以指定 `RuntimeException` 及其子类。
 * type属性指定的异常的子类也成为处理对象。

.. code-block:: java

  @OnError(type = ApplicationException.class, path = "/WEB-INF/view/project/index.jsp")
  public HttpResponse handle(HttpRequest request, ExecutionContext context) {
      // 业务处理省略
  }

.. _on_error-forward:

获取错误时跳转目标画面显示的数据
------------------------------------------------------------
有时需要从数据库等获取要在错误时跳转目标画面中显示的数据，如下拉框的选项等。

这种情况下，对获取显示数据的业务Action方法执行内部forward，
从数据库等获取初始显示数据，并设置到请求作用域。

详情请参考 :ref:`forwarding_handler` 。

以下展示验证错误发生时forward到初始显示用方法的实现示例。

要点
 * path属性设置为内部forward用的路径。

.. code-block:: java

  /**
   * 执行输入值检查的业务Action方法。
   */
  @InjectForm(form = PersonForm.class, prefix = "form")
  @OnError(type = ApplicationException.class, path = "forward://initializeRegisterPage")
  public HttpResponse confirmForRegister(HttpRequest request, ExecutionContext context) {

    PersonForm form = context.getRequestScopedVar("form");

    return new HttpResponse("/WEB-INF/view/person/confirmForRegister.jsp");
  }

  /**
   * 获取登记画面初始显示数据的方法。
   */
  public HttpResponse initializeRegisterPage(HttpRequest request, ExecutionContext context) {
    // 从数据库等获取画面显示数据并设置到请求作用域

    return new HttpResponse("/WEB-INF/view/person/inputForRegister.jsp");
  }

.. _on_error-multiple:

指定多个响应
--------------------------------------------------
本拦截器不能为单一异常指定多个响应，
因此如需指定多个响应，需要在业务Action方法内单独生成 :java:extdoc:`HttpErrorResponse <nablarch.fw.web.HttpErrorResponse>` 。

以下展示实现示例。

.. code-block:: java

  public HttpResponse handle(HttpRequest request, ExecutionContext context) {
      try {
          // 业务处理省略
      } catch (ApplicationException e) {
          if (/* 记述条件表达式 */) {
              return new HttpErrorResponse("/WEB-INF/view/project/index.jsp");
          } else {
              return new HttpErrorResponse("/WEB-INF/view/error.jsp");
          }
      }
  }
