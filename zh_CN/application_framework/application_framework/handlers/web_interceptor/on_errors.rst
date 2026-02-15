.. _on_errors_interceptor:

OnErrors 拦截器
============================

.. contents:: 目录
  :depth: 3
  :local:

在业务Action发生异常时，返回指定响应的拦截器。
可以为多个异常指定响应。

通过在业务Action方法上设置 :java:extdoc:`OnErrors <nablarch.fw.web.interceptor.OnErrors>` 来启用此拦截器。

拦截器类名
--------------------------------------------------
* :java:extdoc:`nablarch.fw.web.interceptor.OnErrors`

模块列表
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web</artifactId>
  </dependency>

使用 OnErrors
--------------------------------------------------
将 :java:extdoc:`OnErrors <nablarch.fw.web.interceptor.OnErrors>` 注解设置在业务Action处理请求的方法上。

各个异常对应的响应指定，使用 :java:extdoc:`OnError <nablarch.fw.web.interceptor.OnError>` 进行。

以下展示业务Action方法内抛出以下异常时的实现示例。

* `ApplicationException` (业务错误)
* `AuthenticationException` (认证错误)
* `UserLockedException` (账户锁定错误。 `AuthenticationException` 的子类)

.. code-block:: java

  @OnErrors({
          @OnError(type = UserLockedException.class, path = "/WEB-INF/view/login/locked.jsp"),
          @OnError(type = AuthenticationException.class, path = "/WEB-INF/view/login/index.jsp"),
          @OnError(type = ApplicationException.class, path = "/WEB-INF/view/login/index.jsp")
  })
  public HttpResponse handle(HttpRequest request, ExecutionContext context) {
      // 业务处理省略
  }

.. important::

  按照 :java:extdoc:`OnError <nablarch.fw.web.interceptor.OnError>` 的定义顺序处理异常，
  因此定义有继承关系的异常时，必须先从子类异常开始定义。
