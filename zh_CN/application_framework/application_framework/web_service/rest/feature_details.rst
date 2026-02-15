功能详情
========================================
.. contents:: 目录
  :depth: 3
  :local:

Nablarch初始化
----------------------------------------
请参考 :ref:`Web应用程序的Nablarch初始化 <web_feature_details-nablarch_initialization>` 。

.. _rest-request_validation:
 
输入值检查
----------------------------------------
* :ref:`输入值检查 <validation>`

数据库访问
----------------------------------------
* :ref:`数据库访问 <database_management>`

并发控制
----------------------------------------
* :ref:`universal_dao`

  * :ref:`universal_dao_jpa_optimistic_lock`
  * :ref:`universal_dao_jpa_pessimistic_lock`

.. important::

  RESTful Web服务不支持使用 `ETag` 或 `If-Match` 的乐观锁。
  因此，在RESTful Web服务中进行乐观锁时，请直接在请求主体中包含版本号。

.. important::

  :ref:`exclusive_control` 功能以与客户端(taglib)联动为前提，
  因此无法在RESTful Web服务中使用。

.. _rest-action_mapping:

URI与资源(Action)类的映射
------------------------------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/resource_signature

* :ref:`router_adaptor>`
* :ref:`资源类的方法签名 <rest_feature_details-method_signature>`

.. _rest-path_query_param:

路径参数和查询参数
----------------------------------------------------------------------------------------------------
* :ref:`rest_feature_details-path_param`
* :ref:`rest_feature_details-query_param`

响应头部
----------------------------------------------------------------------------------------------------
* :ref:`在资源类方法中单独设置响应头部 <rest_feature_details-response_header>`
* :ref:`jaxrs_response_handler-response_finisher`

国际化支持
----------------------------------------
关于静态资源的多语言化支持请参考以下文档。

* :ref:`消息的多语言化 <message-multi_lang>`
* :ref:`代码名称的多语言化 <code-use_multilingualization>`

认证
----------------------------------------
认证因项目需求而异，因此框架不提供。

授权检查
----------------------------------------
授权检查因项目需求而异，因此框架不提供。

错误时返回的响应
--------------------------------------------------
* :ref:`jaxrs_response_handler-error_response_body`
* :ref:`jaxrs_response_handler-individually_error_response`


Web应用程序的扩展设计
---------------------------------------

* :ref:`stateless_web_app`

CSRF对策
----------------------------------------
* :ref:`CSRF对策 <csrf_token_verification_handler>`

CORS
----------------------------------------
* :ref:`CORS <cors_preflight_request_handler>`

从OpenAPI文档生成源代码
---------------------------------------------
* :ref:`nablarch_openapi_generator`
