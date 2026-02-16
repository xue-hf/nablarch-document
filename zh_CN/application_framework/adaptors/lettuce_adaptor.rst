.. _lettuce_adaptor:

Lettuce适配器
================================================================================================

.. contents:: 目录
  :depth: 3
  :local:

提供适配器，使Nablarch提供的以下功能可以使用 `Redis(外部网站，英语) <https://redis.io/>`_ 。

- :ref:`session_store`
- :ref:`health_check_endpoint_handler`

本适配器使用 `Lettuce(外部网站，英语) <https://redis.github.io/lettuce/>`_ 作为Redis的客户端库。

.. _lettuce_adaptor_module_list:

模块列表
-----------------------------------------------------------------------------------------------

.. code-block:: xml

  <!-- RedisStore Lettuce适配器 -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-lettuce-adaptor</artifactId>
  </dependency>

  <!-- 默认配置 -->
  <dependency>
    <groupId>com.nablarch.configuration</groupId>
    <artifactId>nablarch-main-default-configuration</artifactId>
  </dependency>

.. tip::

  使用Redis 5.0.9、Lettuce 5.3.0.RELEASE版本进行测试。
  要更改版本时，请在项目侧进行测试确认无问题。

各功能对应的适配器说明请参阅以下内容。

.. toctree::
  :maxdepth: 1

  lettuce_adaptor/redisstore_lettuce_adaptor
  lettuce_adaptor/redishealthchecker_lettuce_adaptor
