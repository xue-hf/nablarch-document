.. _use_token_interceptor:

UseToken 拦截器
=====================================

.. contents:: 目录
  :depth: 3
  :local:

为 :ref:`防止重复提交(同一请求的双重发送) <tag-double_submission_server_side>` 发行令牌的拦截器。

此拦截器主要用于采用JSP以外模板引擎的情况。

在JSP以外的模板引擎中，除了使用此拦截器外，还需要在模板中显式将令牌嵌入hidden。
令牌的嵌入方法后述。
另外，使用JSP时，通过 :ref:`tag-form_tag` 的useToken属性执行令牌生成和嵌入hidden的操作。

为检查令牌，需要对后续Action设置
:ref:`on_double_submission_interceptor`
。

拦截器类名
--------------------------------------------------
* :java:extdoc:`nablarch.common.web.token.UseToken`

模块列表
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web-tag</artifactId>
  </dependency>

使用 UseToken
--------------------------------------------------
将 :java:extdoc:`UseToken <nablarch.common.web.token.UseToken>` 注解设置在Action方法上。

.. code-block:: java

 @UseToken
 public HttpResponse confirm(HttpRequest req, ExecutionContext ctx) {
     // 省略
 }

另外，需要显式将令牌嵌入输入表单。

Thymeleaf 实现示例
 .. code-block:: xml

  <form th:action="@{/path/to/action}" method="post">
    <input type="hidden" name="nablarch_token" th:value="${nablarch_request_token}" />

如本例所示，name属性需设置为"nablarch_token"，value属性需设置为从请求作用域以"nablarch_request_token"为键获取的值。
此name属性和从请求作用域获取值的键可以更改。
详情请参考 :ref:`服务器端防止重复提交 <tag-double_submission_server_side>` 。
