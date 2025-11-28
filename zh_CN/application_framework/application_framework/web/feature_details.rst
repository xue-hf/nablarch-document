功能详细
========================================

.. contents:: 目录
  :depth: 3
  :local:

.. _web_feature_details-nablarch_initialization:

Nablarch的初始化
----------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/nablarch_servlet_context_listener
  feature_details/web_front_controller

为了进行Nablarch的初始化，需要进行 :ref:`用于加载System Repository的设置 <nablarch_servlet_context_listener>`
以及 :ref:`handler队列的设置（构建）<web_front_controller>`。

输入值校验
----------------------------------------
.. toctree::
    :maxdepth: 1
    :hidden:

    feature_details/error_message

* :ref:`输入值校验 <validation>`
* :doc:`在页面上显示错误消息 <feature_details/error_message>`

数据库访问
----------------------------------------
* :ref:`数据库访问 <database_management>`

数据库锁控制
----------------------------------------
关于数据库锁控制，虽然Nablarch提供了以下两种方式，
但是根据 :ref:`为什么推荐使用UniversalDao <exclusive_control-deprecated>` ，
推荐使用 :ref:`universal_dao`。

* :ref:`exclusive_control`
* :ref:`universal_dao`

  * :ref:`universal_dao_jpa_optimistic_lock`
  * :ref:`universal_dao_jpa_pessimistic_lock`

文件上传
----------------------------------------
* :ref:`multipart_handler-read_upload_file`

文件下载
----------------------------------------
虽然提供了两种不同的提供下载功能的方法，
但是根据:ref:`为什么推荐数据绑定 <data_converter-data_bind_recommend>` ，
推荐使用:ref:`data_bind`。

* :ref:`使用数据绑定的文件上传 <data_bind-file_download>`
* :ref:`使用通用数据模板的文件上传 <data_format-file_download>`

下载大量数据时，参考:ref:`universal_dao-lazy_load`，
注意数据库的检索结果不要导致堆溢出。

URI与Action类的映射（路由）
----------------------------------------
虽然提供了以下两种方法，
但是根据 :ref:`为什么推荐使用route适配器<http_request_java_package_mapping-router_adaptor>` ，
推荐使用 :ref:`router_adaptor` 。

* :ref:`router_adaptor`
* :ref:`http_request_java_package_mapping`

防抖
----------------------------------------
* :ref:`防抖 <tag-double_submission>`

此外，使用JSP以外的模板引擎时，还可以参考 :ref:`use_token_interceptor`。

保存输入数据
----------------------------------------
* :ref:`session_store`

分页
----------------------------------------
从数据库获取指定范围的数据的方法，请参考 :ref:`database_management` 。

关于客户端，由于项目需求不同而导致规格各异，因此框架本身并未提供。

创建页面
----------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/jsp_session
  feature_details/view/other

* 使用JSP的情况

  * :ref:`使用JSP的taglib进行页面开发 <tag>`
  * :ref:`jsp_session`

* 使用JSP以外的其他模板引擎的情况

  * :ref:`使用Thymeleaf进行页面开发 <web_thymeleaf_adaptor>`
  * :ref:`view_other`

国际化
----------------------------------------
关于静态资源的多语言支持，请参照如下内容。

* :ref:`消息的多语言化 <message-multi_lang>`
* :ref:`code名称的多语言化 <code-use_multilingualization>`

虽然提供了以下两种切换页面文本的语言的方式，
但是使用 :ref:`使用消息tag实现多语言 <tag-write_message>` 的时候
可能导致页面布局不稳定的情况。
因此只有在能接受页面布局不稳定的情况下才可以使用 :ref:`使用消息tag实现多语言 <tag-write_message>`。

* :ref:`使用消息tag实现多语言 <tag-write_message>`
* :ref:`根据语言切换资源路径 <tag_change_resource_path_of_lang>`

认证
----------------------------------------
因为在不同的项目中，认证方式存在各种差异，因此框架不提供认证相关的功能。
请根据项目要求自行实现。

关于认证信息的保存，请参照如下内容。

* :ref:`session_store-authentication_data`

权限校验
----------------------------------------
* :ref:`permission_check`


.. _web_feature_details-status_code:

错误画面跳转与状态码
--------------------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/forward_error_page

* :ref:`根据状态码设置默认的跳转指定错误页面。 <HttpErrorHandler_DefaultPage>`
* :ref:`通过handler中根据异常类跳转指定错误页面。 <forward_error_page-handler>`
* 在Action中编写发生错误时跳转指定错误页面的逻辑

  * 定义与异常类对应的跳转目标。 (:ref:`on_error_interceptor` 、 :ref:`on_errors_interceptor`)
  * :ref:`为一个异常定义多个跳转目标。 <forward_error_page-try_catch>`
* `我该使用什么状态码(外链) <https://qiita.com/kawasima/items/e48180041ace99842779>`_

发送面向消息的中间件消息
----------------------------------------
* :ref:`发送同步消息<mom_system_messaging-sync_message_send>`


Web应用的横向扩展设计
---------------------------------------

* :ref:`stateless_web_app`

CSRF
----------------------------------------
* :ref:`CSRF <csrf_token_verification_handler>`

Web应用与RESTful Web服务的结合使用
-----------------------------------------------------
* :ref:`更改委托的Web前端控制器名称 <change_web_front_controller_name>`

内容安全策略(CSP)
----------------------------------------
* :ref:`Content Security Policy(CSP)<content_security_policy>`
