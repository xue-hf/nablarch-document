.. _on_double_submission_interceptor:

OnDoubleSubmission 拦截器
=====================================

.. contents:: 目录
  :depth: 3
  :local:

执行 :ref:`重复提交检查(同一请求的双重发送) <tag-double_submission_server_side>` 的拦截器。

使用此拦截器需要
:ref:`在jsp中使用form标签设置令牌 <tag-double_submission_token_setting>`
或
:ref:`使用 UseToken 拦截器设置令牌 <use_token_interceptor>`
。

拦截器类名
--------------------------------------------------
* :java:extdoc:`nablarch.common.web.token.OnDoubleSubmission`

模块列表
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web-tag</artifactId>
  </dependency>

使用 OnDoubleSubmission
--------------------------------------------------
将 :java:extdoc:`OnDoubleSubmission <nablarch.common.web.token.OnDoubleSubmission>` 注解设置在Action方法上。

.. code-block:: java

 // 在path属性中指定判定为重复提交时的跳转目标。
 @OnDoubleSubmission(path = "/WEB-INF/view/error/userError.jsp")
 public HttpResponse register(HttpRequest req, ExecutionContext ctx) {
     // 省略。
 }

指定 OnDoubleSubmission 的默认值
--------------------------------------------------
如需设置应用程序整体使用的
:java:extdoc:`OnDoubleSubmission <nablarch.common.web.token.OnDoubleSubmission>` 注解默认值，
请将
:java:extdoc:`BasicDoubleSubmissionHandler <nablarch.common.web.token.BasicDoubleSubmissionHandler>`
以 ``doubleSubmissionHandler`` 名称添加到组件定义中。

:java:extdoc:`BasicDoubleSubmissionHandler <nablarch.common.web.token.BasicDoubleSubmissionHandler>`
在注解属性未指定时，使用自身属性中设置的资源路径、消息ID、状态码。

配置示例
 .. code-block:: xml

  <component name="doubleSubmissionHandler"
             class="nablarch.common.web.token.BasicDoubleSubmissionHandler">
    <!-- 判定为重复提交时的跳转目标资源路径 -->
    <property name="path" value="/WEB-INF/view/error/userError.jsp" />
    <!-- 判定为重复提交时在跳转目标画面上显示错误消息使用的消息ID -->
    <property name="messageId" value="DOUBLE_SUBMISSION_ERROR" />
    <!-- 判定为重复提交时的响应状态码。默认为400 -->
    <property name="statusCode" value="200" />
  </component>

.. important::
 :java:extdoc:`OnDoubleSubmission <nablarch.common.web.token.OnDoubleSubmission>`
 和 :java:extdoc:`BasicDoubleSubmissionHandler <nablarch.common.web.token.BasicDoubleSubmissionHandler>` 
 两者都未指定path时，由于判定为重复提交时跳转目标不明，将成为系统错误。

 因此，使用 :ref:`使用令牌防止重复提交 <tag-double_submission_server_side>`
 的应用程序中，必须指定其中之一的path。

更改 OnDoubleSubmission 的行为
--------------------------------------------------
:java:extdoc:`OnDoubleSubmission <nablarch.common.web.token.OnDoubleSubmission>` 注解的行为，
可以通过实现
:java:extdoc:`DoubleSubmissionHandler <nablarch.common.web.token.DoubleSubmissionHandler>`
接口来更改。将实现的类以 ``doubleSubmissionHandler`` 名称添加到组件定义中。
