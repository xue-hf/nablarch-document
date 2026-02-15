功能详情
========================================
.. contents:: 目录
  :depth: 3
  :local:

Nablarch初始化
----------------------------------------
请参考 :ref:`Web应用程序的Nablarch初始化 <web_feature_details-nablarch_initialization>` 。

.. _http_messaging-request_validation:

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

  :ref:`exclusive_control` 功能以与客户端(taglib)联动为前提，
  因此无法在HTTP消息处理中使用。

.. _http_messaging-action_mapping:

URI与Action类的映射
----------------------------------------
* :ref:`http_request_java_package_mapping`

.. tip::
 HTTP消息处理无法使用 :ref:`router_adaptor` 。
 HTTP消息处理使用 :ref:`mom_system_messaging` 提供的
 :java:extdoc:`MessagingAction<nablarch.fw.messaging.action.MessagingAction>`
 创建Action类，因此没有根据URI调用不同Action类方法的设想。

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
* :ref:`permission_check`

错误时返回的响应
--------------------------------------------------
* :ref:`http_messaging_error_handler`
