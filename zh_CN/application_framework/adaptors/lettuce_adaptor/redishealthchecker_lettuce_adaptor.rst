.. _redishealthchecker_lettuce_adaptor:

Redis健康检查器(Lettuce)适配器
================================================================================================

.. contents:: 目录
  :depth: 3
  :local:

提供可以进行 `Redis(外部网站，英语) <https://redis.io/>`_ 健康检查的适配器。
关于健康检查请参阅 :ref:`health_check_endpoint_handler` 。

健康检查可以通过创建继承 :ref:`health_check_endpoint_handler-add_health_checker` 中说明的
:java:extdoc:`HealthChecker <nablarch.fw.web.handler.health.HealthChecker>` 的类来添加。
本适配器提供了继承HealthChecker的 :java:extdoc:`RedisHealthChecker <nablarch.integration.health.RedisHealthChecker>` 。

.. _redishealthchecker_lettuce_adaptor_settings:

进行Redis的健康检查
-----------------------------------------------------------------------------------------------
通过在HealthCheckEndpointHandler的healthCheckers属性中指定RedisHealthChecker，可以实现Redis的健康检查。

以下显示设置示例。

.. code-block:: xml

    <!-- 健康检查端点处理程序 -->
    <component class="nablarch.fw.web.handler.HealthCheckEndpointHandler">
      <!-- healthCheckers属性以列表指定 -->
      <property name="healthCheckers">
        <list>
          <!-- Redis的健康检查 -->
          <component class="nablarch.integration.health.RedisHealthChecker">
            <!-- 指定Redis的客户端(LettuceRedisClient) -->
            <property name="client" ref="lettuceRedisClient" />
          </component>
        </list>
      </property>
    </component>

RedisHealthChecker使用 :java:extdoc:`LettuceRedisClient<nablarch.integration.redisstore.lettuce.LettuceRedisClient>` 
进行键的存在确认，如果不发生异常则判断健康检查成功。键可以不存在。
关于LettuceRedisClient请参阅 :ref:`redisstore_redis_client_config_client_classes` 。

想要更改键时，在RedisHealthChecker的key属性中指定。

.. code-block:: xml

    <!-- Redis的健康检查 -->
    <component class="nablarch.integration.health.RedisHealthChecker">
      <!-- 指定Redis的客户端(LettuceRedisClient) -->
      <property name="client" ref="lettuceRedisClient" />
      <!-- 指定键 -->
      <property name="key" ref="pingtest" />
    </component>
