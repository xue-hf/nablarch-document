.. _`restful_web_service_functional_comparison`:

Jakarta RESTful Web Services支持/Jakarta RESTful Web Services/HTTP消息处理的功能比较
=================================================================================================

.. contents:: 目录
  :depth: 3
  :local:

此处显示以下功能比较。

 - :ref:`Nablarch的Jakarta RESTful Web Services支持 <restful_web_service>`
 - :ref:`HTTP消息处理 <http_messaging>`
 - `Jakarta RESTful Web Services(外部站点，英文) <https://jakarta.ee/specifications/restful-ws/>`_

.. tip::

 只有Nablarch的Jakarta RESTful Web Services支持和HTTP消息处理，点击表中的标记可以跳转到解说文档的说明页面。

.. |br| raw:: html

   <br />

.. list-table:: 功能比较（○：提供　△：部分提供　×：不提供　－:对象外）
   :header-rows: 1
   :class: something-special-class

   * - 功能
     - Jakarta RESTful |br| Web Services |br| 支持
     - HTTP |br| 消息处理
     - Jakarta RESTful |br| Web Services
   * - 请求与资源方法的映射
     - :ref:`△ <rest-action_mapping>`
     - :ref:`○ <http_messaging-action_mapping>`
     - ○
   * - 请求与参数的映射
     - :ref:`△ <rest-path_query_param>`
     - × [1]_
     - ○
   * - HTTP方法匹配
     - :ref:`△ <rest-action_mapping>`
     - × [1]_
     - ○
   * - 根据媒体类型的 |br| 请求/响应转换
     - :ref:`△ <body_convert_handler>`
     - × [1]_
     - ○
   * - Entity验证
     - :ref:`○ <rest-request_validation>`
     - :ref:`○ <http_messaging-request_validation>`
     - ○
   * - 资源类注入 |br| (Jakarta Contexts and Dependency Injection)
     - × [2]_
     - × [2]_
     - ○
   * - 请求/响应过滤器
     - × [3]_
     - × [3]_
     - ○
   * - 主体读写拦截器
     - × [4]_
     - × [5]_
     - ○
   * - 客户端API
     - × [6]_
     - :ref:`○ <http_system_messaging-message_send>`
     - ○
   * - 异步处理
     - × [7]_
     - × [7]_
     - ○
   * - 错误时日志输出
     - :ref:`○ <jaxrs_response_handler-error_log>`
     - :ref:`○ <http_messaging_error_handler-error_response_and_log>`
     - －
   * - 请求主体最大容量检查
     - × [8]_
     - :ref:`○ <http_messaging_request_parsing_handler-limit_size>`
     - －
   * - 证迹日志输出
     - × [9]_
     - :ref:`○ <messaging_log>`
     - －
   * - 重送控制
     - × [9]_
     - :ref:`○ <message_resend_handler>`
     - －
   * - 服务提供可用性检查
     - × [10]_
     - × [10]_
     - －
   * - 事务控制
     - × [11]_
     - × [11]_
     - －
   * - 业务处理错误时的回调
     - × [12]_
     - :java:extdoc:`○ <nablarch.fw.messaging.action.MessagingAction>`
     - －

.. [1] HTTP消息处理不是为REST设计的。RESTful Web服务请使用Jakarta RESTful Web Services支持。
.. [2] Jakarta RESTful Web Services支持和HTTP消息处理作为Nablarch的Web应用程序运行，因此无法使用Jakarta Contexts and Dependency Injection。
.. [3] 想要创建请求/响应过滤器时，请创建handler。
.. [4] 想要创建主体读写拦截器时，请创建Jakarta RESTful Web Services支持的BodyConverter。
.. [5] 主体读写使用Nablarch的数据格式。要更改时请创建数据格式的DataRecordFormatter。
.. [6] 需要Jakarta RESTful Web Services客户端时，请使用Jakarta RESTful Web Services的实现(Jersey或RESTEasy等)。
.. [7] 假设服务器端没有需要异步处理的需求。如有需求将考虑支持。
.. [8] 使用Web服务器或应用服务器中的请求大小检查功能。
.. [9] 假设每个应用程序的需求不同。请在应用程序中进行设计/实现。
.. [10] 如果Nablarch提供的服务可用性检查符合应用程序需求则使用它。不符合时请在应用程序中进行设计/实现。
.. [11] 使用Nablarch提供的事务管理。
.. [12] 假设错误处理会通用化，通过定制JaxRsResponseHandler实现。如果业务处理中需要单独进行错误处理，请在资源方法中使用try/catch。
