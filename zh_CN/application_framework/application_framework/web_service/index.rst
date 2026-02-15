.. _`web_service`:

Web服务篇
==================================================
本章提供使用Nablarch应用框架开发Web服务所需的信息。

Nablarch提供了以下2种RESTful Web服务框架。

.. toctree::
  :maxdepth: 1

  rest/index
  http_messaging/index

.. _web_service-recommended_jaxrs:

虽然使用任一框架都可以构建Web服务，
但基于以下理由，推荐使用 :ref:`restful_web_service` 创建Web服务。

理由
  :ref:`restful_web_service` 可以使用 `Jakarta RESTful Web Services(外部站点，英文) <https://jakarta.ee/specifications/restful-ws/>`_ 中规定的部分注解轻松构建Web服务。
  
  另一方面， :ref:`http_messaging` 在主体部分、HTTP头部、异常控制方面存在以下限制，无法进行灵活的设计和实现。

  * Nablarch的控制区域需要存在于HTTP头部或主体部分。

    在构建与已构建的外部系统联动的Web服务时，设计和实现难度会增加。

  * 无法轻松自定义响应头部中设置的项目。

    如 :ref:`http_messaging_response_building_handler-header` 所述，想要更改响应头部时需要替换handler本身。

  * 依赖于 :ref:`data_format` 功能。
  
    需要创建格式定义文件，开发成本较高。
    此外，不易定制，需要以Map对象处理输入输出数据，容易产生实现错误。

  * 请求主体解析时的异常全部映射到单一异常类，无法进行细致的异常处理。

    解析中的异常全部作为 :java:extdoc:`MessagingException <nablarch.fw.messaging.MessagingException>` 抛出，无法基于根本原因进行细致的处理控制。

.. tip::

  :ref:`restful_web_service` 和 :ref:`http_messaging` 提供的功能差异请参考 :ref:`restful_web_service_functional_comparison` 。

.. toctree::
  :maxdepth: 1
  :hidden:

  functional_comparison
