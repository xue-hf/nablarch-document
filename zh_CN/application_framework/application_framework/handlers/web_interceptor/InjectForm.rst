.. _inject_form_interceptor:

InjectForm 拦截器
============================

.. contents:: 目录
  :depth: 3
  :local:

对输入值进行验证，并将生成的表单对象设置到请求作用域的拦截器。

通过在业务Action方法上设置 :java:extdoc:`InjectForm <nablarch.common.web.interceptor.InjectForm>` 来启用此拦截器。

拦截器类名
--------------------------------------------------
* :java:extdoc:`nablarch.common.web.interceptor.InjectForm`

模块列表
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web</artifactId>
  </dependency>

  <!-- 仅在输入值校验中使用BeanValidation时 -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-validation-ee</artifactId>
  </dependency>

  <!-- 仅在输入值校验中使用NablarchValidation时 -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-validation</artifactId>
  </dependency>

使用 InjectForm
--------------------------------------------------
将 :java:extdoc:`InjectForm <nablarch.common.web.interceptor.InjectForm>` 注解设置在业务Action处理请求的方法上。


以下展示实现示例。

输入画面html示例
  .. code-block:: html

    <!-- 验证对象外-->
    <input name="flag" type="hidden" />

    <!-- 验证对象 -->
    <input name="form.userId" type="text" />
    <input name="form.password" type="password" />

业务Action示例
  此示例中，对从画面发送的以 ``form`` 开头的请求参数执行验证。
  当验证未发生错误时， :java:extdoc:`InjectForm#form <nablarch.common.web.interceptor.InjectForm.form()>` 指定的类的对象将被存储到请求作用域。

  将验证后的表单存储到请求作用域时使用的变量名，在 :java:extdoc:`InjectForm#name <nablarch.common.web.interceptor.InjectForm.name()>` 中指定。
  未指定时，表单将以 ``form`` 作为变量名存储。

  业务Action执行时，必定可以从请求作用域获取对象。

  .. code-block:: java

    @InjectForm(form = UserForm.class, prefix = "form", validate = "register")
    @OnError(type = ApplicationException.class, path = "forward://registerForm.jsp")
    public HttpResponse handle(HttpRequest req, ExecutionContext ctx) {

      // 从请求作用域获取验证后的表单。
      UserForm form = ctx.getRequestScopedVar("form");

      // 基于form执行业务处理。
    }


.. tip::
  使用 :ref:`bean_validation` 进行验证时，可以设置即使在验证错误时也能从请求作用域获取对象。详情请参考『\ :ref:`bean_validation_onerror`\ 』。
    
指定验证错误时的跳转目标
-------------------------------------------------
验证错误发生时的跳转目标画面，使用 :java:extdoc:`OnError <nablarch.fw.web.interceptor.OnError>` 注解进行设置。

:java:extdoc:`OnError <nablarch.fw.web.interceptor.OnError>` 注解设置在配置了 :java:extdoc:`InjectForm <nablarch.common.web.interceptor.InjectForm>` 的业务Action方法上。
请注意，如果未设置 :java:extdoc:`OnError <nablarch.fw.web.interceptor.OnError>` ，验证错误将被视为系统错误。

如需在验证错误发生时获取跳转目标画面显示的数据，请参考 :ref:`on_error-forward` 。

指定 Bean Validation 的组
-------------------------------------------------
使用 :ref:`bean_validation` 进行验证时，可以在 :java:extdoc:`InjectForm#validationGroup <nablarch.common.web.interceptor.InjectForm.validationGroup()>` 中指定组。

以下展示实现示例。

  .. code-block:: java

    // 使用UserForm类中设置的验证规则中，仅属于Create组的规则进行验证。
    @InjectForm(form = UserForm.class, prefix = "form", validationGroup = Create.class)
    public HttpResponse handle(HttpRequest req, ExecutionContext ctx) {

      // 从请求作用域获取验证后的表单。
      UserForm form = ctx.getRequestScopedVar("form");

      // 基于form执行业务处理。
    }
