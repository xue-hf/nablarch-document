.. _redisstore_lettuce_adaptor:

Redis存储(Lettuce)适配器
================================================================================================

.. contents:: 目录
  :depth: 3
  :local:

提供可以在会话存储中使用 `Redis(外部网站，英语) <https://redis.io/>`_ 的适配器。

在会话存储中使用Redis，与选择DB存储相比可以获得以下好处。

* 无需事先准备用于保存会话信息的表
* 无需创建批处理来删除已过有效期的会话信息

.. _redisstore_minimum_settings:

最小构成运行
-----------------------------------------------------------------------------------------------
这里以连接到在 ``localhost`` 的 ``6379`` 端口运行的单个Redis实例为例，说明设置方法。

.. tip::
  在本地试用时，可以使用Docker通过执行以下命令构建Redis实例。
  
  .. code-block:: shell

    > docker run --name redis -d -p 6379:6379 redis:5.0.9
  
  停止时执行以下命令。

  .. code-block:: shell

    > docker stop redis



.. _redisstore_minimum_settings_content:

设置内容
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

要以最小构成开始使用Redis存储，需要修改应用程序的组件定义和环境设置值。

.. _redisstore_minimum_settings_how_modify_component_definition:

修改组件配置文件
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
首先，说明修改组件配置文件的方法。

.. code-block:: xml

  <!-- 省略 -->
  <config-file file="nablarch/webui/redisstore-lettuce.config" />
  <config-file file="common.properties" />
  <config-file file="env.properties" />
  
  <!-- 省略 -->
  <import file="nablarch/webui/redisstore-lettuce.xml" />

首先，加载默认配置提供的以下2个设置文件。

* ``nablarch/webui/redisstore-lettuce.config``
* ``nablarch/webui/redisstore-lettuce.xml``

``redisstore-lettuce.config`` 中声明了 ``redisstore-lettuce.xml`` 中使用的占位符的默认值。

如果应用程序有准备的环境设置文件（``env.properties`` 等），请将 ``redisstore-lettuce.config`` 放在其之前加载。
这样做可以根据需要在应用程序的环境设置文件中覆盖默认的占位符值。

此外，使用 :ref:`repository-overwrite_environment_configuration_by_os_env_var` 中说明的方法，可以根据执行环境切换要连接的Redis。

.. tip::

  默认设置为连接到在 ``localhost`` 的 ``6379`` 端口运行的单个Redis实例。


``redisstore-lettuce.xml`` 中定义了使用Redis存储所需的组件。

使用 ``redisstore-lettuce.xml`` 后，就不再需要 ``nablarch/webui/session-store.xml`` 了。
如果使用 :ref:`Web原型 <firstStepGenerateWebBlankProject>` 生成项目，默认设置为使用 ``session-store.xml`` ，
因此请删除 ``session-store.xml`` 的导入，改为导入 ``redisstore-lettuce.xml`` 。


.. code-block:: xml

  <!-- 需要初始化的组件 -->
  <component name="initializer"
             class="nablarch.core.repository.initialization.BasicApplicationInitializer">
    <property name="initializeList">
      <list>
        <!-- 省略 -->
        <component-ref name="lettuceRedisClientProvider"/>
      </list>
    </property>
  </component>

接下来，将 :java:extdoc:`LettuceRedisClientProvider<nablarch.integration.redisstore.lettuce.LettuceRedisClientProvider>` 的组件添加到 :java:extdoc:`BasicApplicationInitializer<nablarch.core.repository.initialization.BasicApplicationInitializer>` 的 ``initializeList`` 中。

``LettuceRedisClientProvider`` 的组件在 ``redisstore-lettuce.xml`` 中以 ``lettuceRedisClientProvider`` 名称定义，因此可以使用名称引用进行设置。

关于此设置的说明请参阅 :ref:`redisstore_initialize_client` 。


.. code-block:: xml

  <!-- 需要废弃的组件 -->
  <component name="disposer"
             class="nablarch.core.repository.disposal.BasicApplicationDisposer">
    <property name="disposableList">
      <list>
        <!-- 省略 -->
        <component-ref name="lettuceRedisClientProvider"/>
      </list>
    </property>
  </component>

此外，将 :java:extdoc:`LettuceRedisClientProvider<nablarch.integration.redisstore.lettuce.LettuceRedisClientProvider>` 的组件添加到 :java:extdoc:`BasicApplicationDisposer<nablarch.core.repository.disposal.BasicApplicationDisposer>` 的 ``disposableList`` 中。

关于此设置的说明请参阅 :ref:`repository-dispose_object` 。


.. _redisstore_minimum_settings_how_modify_env_config:

修改环境设置值
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
接下来，说明环境设置值的修改方法。

.. code-block:: properties

  # 默认的会话存储名称
  nablarch.sessionManager.defaultStoreName=redis

在项目的环境设置文件中定义 ``nablarch.sessionManager.defaultStoreName`` 设置项，并将值设为 ``redis`` 。

.. tip::

  如果使用 :ref:`Web原型 <firstStepGenerateWebBlankProject>` 生成项目，
  则在 ``src/main/resources/common.properties`` 中声明了 ``nablarch.sessionManager.defaultStoreName`` 。


以上即可完成使用在 ``localhost`` 的 ``6379`` 端口运行的Redis作为会话存储的设置。

.. _redisstore_redis_client_config:

根据Redis的构成进行设置
-----------------------------------------------------------------------------------------------
:ref:`redisstore_minimum_settings` 中显示了连接到在本地运行的单个Redis实例的示例。

但是，实际在生产等环境中使用Redis时，需要能够连接到以下构成的Redis。

* 使用Sentinel的Master-Replica构成
* Cluster构成

这里说明如何根据要连接的Redis的构成更改设置。

.. _redisstore_redis_client_config_client_classes:

各构成专用的客户端类
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

本适配器为每种要连接的Redis构成准备了专用的客户端类（:java:extdoc:`LettuceRedisClient<nablarch.integration.redisstore.lettuce.LettuceRedisClient>` 的实现类）。

:java:extdoc:`LettuceSimpleRedisClient<nablarch.integration.redisstore.lettuce.LettuceSimpleRedisClient>`
  直接连接到单个Redis实例时使用的类。

:java:extdoc:`LettuceMasterReplicaRedisClient<nablarch.integration.redisstore.lettuce.LettuceMasterReplicaRedisClient>`
  连接到Master-Replica构成的Redis实例时使用的类。
  通过Sentinel连接时也使用此类。

:java:extdoc:`LettuceClusterRedisClient<nablarch.integration.redisstore.lettuce.LettuceClusterRedisClient>`
  连接到Cluster构成的Redis实例时使用的类。

需要根据应用程序使用的Redis构成，从这些中选择要使用的客户端类进行设置。

.. tip::

  这些客户端类的组件在 ``redisstore-lettuce.xml`` 中定义，因此使用者无需自行定义。

.. _redisstore_redis_client_config_how_select_client:

设置要使用的客户端类
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
要使用的客户端类可以通过环境设置值 ``nablarch.lettuce.clientType`` 进行设置。

设置值与采用的客户端类的关系如下表所示。

================= ======================================
设置值             客户端类
================= ======================================
``simple``        ``LettuceSimpleRedisClient``
``masterReplica`` ``LettuceMasterReplicaRedisClient``
``cluster``       ``LettuceClusterRedisClient``
================= ======================================

因此，在应用程序的环境设置文件中按以下方式设置，即可连接到Cluster构成的Redis。

.. code-block:: properties

  nablarch.lettuce.clientType=cluster

.. tip::

  ``nablarch.lettuce.clientType`` 的默认值在 ``redisstore-lettuce.config`` 中设置为 ``simple`` 。

.. _redisstore_redis_client_config_uri:

设置连接URI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
连接目标的Redis信息以URI指定。

URI可以在每种Redis构成的以下环境设置值中进行设置。

=============== ====================================== =============
Redis的构成     环境设置值                               默认值(在redisstore-lettuce.config中设置的值)
=============== ====================================== =============
单一            ``nablarch.lettuce.simple.uri``         ``redis://localhost:6379``
Master-Replica  ``nablarch.lettuce.masterReplica.uri`` ``redis-sentinel://localhost:26379,localhost:26380,localhost:26381?sentinelMasterId=masterGroupName``
Cluster         ``nablarch.lettuce.cluster.uriList``   ``redis://localhost:6379,redis://localhost:6380,redis://localhost:6381``
=============== ====================================== =============

Cluster的设置值是枚举连接到各节点的URI，用半角逗号分隔的值。
关于各个URI格式的详细信息，请参阅 `Lettuce文档(外部网站，英语) <https://redis.github.io/lettuce/user-guide/connecting-redis/#uri-syntax>`_ 。

.. _redisstore_redis_client_config_advanced:

更高级的设置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
环境设置值只能指定客户端类的种类和URI。
想要进行更详细的设置时，需要创建继承各客户端类的自定义客户端类。

各客户端类中定义了以 ``protected`` 修饰符生成Lettuce实例的方法。
各客户端类中准备的 ``protected`` 方法如下表所示。

=================================== ======================================== =============
客户端类                            方法                                     返回值类型
=================================== ======================================== =============
``LettuceSimpleRedisClient``        ``createClient()``                       `RedisClient(外部网站，英语) <https://www.javadoc.io/static/io.lettuce/lettuce-core/5.3.0.RELEASE/io/lettuce/core/RedisClient.html>`_
\                                   ``createConnection(RedisClient)``        `StatefulRedisConnection<byte[], byte[]>(外部网站，英语) <https://www.javadoc.io/static/io.lettuce/lettuce-core/5.3.0.RELEASE/io/lettuce/core/api/StatefulRedisConnection.html>`_
``LettuceMasterReplicaRedisClient`` ``createClient()``                       `RedisClient(外部网站，英语) <https://www.javadoc.io/static/io.lettuce/lettuce-core/5.3.0.RELEASE/io/lettuce/core/RedisClient.html>`_
\                                   ``createConnection(RedisClient)``        `StatefulRedisMasterReplicaConnection<byte[], byte[]>(外部网站，英语) <https://www.javadoc.io/static/io.lettuce/lettuce-core/5.3.0.RELEASE/io/lettuce/core/masterreplica/StatefulRedisMasterReplicaConnection.html>`_
``LettuceClusterRedisClient``       ``createClient()``                       `RedisClusterClient(外部网站，英语) <https://www.javadoc.io/static/io.lettuce/lettuce-core/5.3.0.RELEASE/io/lettuce/core/cluster/RedisClusterClient.html>`_
\                                   ``createConnection(RedisClusterClient)`` `StatefulRedisClusterConnection<byte[], byte[]>(外部网站，英语) <https://www.javadoc.io/static/io.lettuce/lettuce-core/5.3.0.RELEASE/io/lettuce/core/cluster/api/StatefulRedisClusterConnection.html>`_
=================================== ======================================== =============

通过在自定义客户端类中覆盖这些方法并实现返回自行设置的Lettuce实例，可以进行任意设置。

然后，以与原始组件相同的名称定义自定义客户端类的组件，即可替换客户端类的组件。

各客户端类的组件名称如下表所示。

=================================== ====================================
客户端类                            组件名
=================================== ====================================
``LettuceSimpleRedisClient``        ``lettuceSimpleRedisClient``
``LettuceMasterReplicaRedisClient`` ``lettuceMasterReplicaRedisClient``
``LettuceClusterRedisClient``       ``lettuceClusterRedisClient``
=================================== ====================================

.. _redisstore_redis_client_config_advanced_topology_refresh_example:

示例：启用Cluster的拓扑更新监控
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
以启用Cluster的拓扑更新监控的设置为例，说明自定义客户端类的实现和设置方法。

首先，继承Cluster构成用的客户端类 ``LettuceClusterRedisClient`` ，创建自定义客户端类（``CustomClusterRedisClient``）。

.. code-block:: java
  
  package com.nablarch.example.redisstore;
  
  import io.lettuce.core.RedisURI;
  import io.lettuce.core.cluster.ClusterClientOptions;
  import io.lettuce.core.cluster.ClusterTopologyRefreshOptions;
  import io.lettuce.core.cluster.RedisClusterClient;
  import nablarch.integration.redisstore.lettuce.LettuceClusterRedisClient;
  
  import java.time.Duration;
  import java.util.List;
  import java.util.stream.Collectors;
  
  public class CustomClusterRedisClient extends LettuceClusterRedisClient {
  
      @Override
      protected RedisClusterClient createClient() {
          List<RedisURI> redisUriList = uriList.stream().map(RedisURI::create).collect(Collectors.toList());
          RedisClusterClient client = RedisClusterClient.create(redisUriList);
  
          ClusterTopologyRefreshOptions clusterTopologyRefreshOptions = ClusterTopologyRefreshOptions.builder()
                  .enableAllAdaptiveRefreshTriggers()
                  .enablePeriodicRefresh(Duration.ofSeconds(10))
                  .build();
  
          ClusterClientOptions clusterClientOptions = ClusterClientOptions.builder()
                  .topologyRefreshOptions(clusterTopologyRefreshOptions)
                  .build();
  
          client.setOptions(clusterClientOptions);
  
          return client;
      }
  }

要在Lettuce中启用Cluster的拓扑更新监控，需要将设置了必要信息的 `ClusterTopologyRefreshOptions（外部网站，英语） <https://www.javadoc.io/static/io.lettuce/lettuce-core/5.3.0.RELEASE/io/lettuce/core/cluster/ClusterTopologyRefreshOptions.html>`_ 
设置到 `RedisClusterClient（外部网站，英语） <https://www.javadoc.io/static/io.lettuce/lettuce-core/5.3.0.RELEASE/io/lettuce/core/cluster/RedisClusterClient.html>`_ 中。

因此，在 ``CustomClusterRedisClient`` 中覆盖生成 ``RedisClusterClient`` 的 ``createClient()`` ，
实现返回设置了必要信息的 ``RedisClusterClient`` 实例。

.. tip::

  关于Lettuce设置的详细信息，请参阅 `Lettuce文档（外部网站，英语） <https://redis.github.io/lettuce/advanced-usage/#cluster-specific-options>`_ 。

接下来，定义此自定义客户端类的组件。

.. code-block:: xml

  <import file="nablarch/webui/redisstore-lettuce.xml" />

  <component name="lettuceClusterRedisClient" class="com.nablarch.example.redisstore.CustomClusterRedisClient">
    <property name="uriList" ref="redisClusterUriListFactory" />
  </component>

由于 ``CustomClusterRedisClient`` 的原始客户端类是 ``LettuceClusterRedisClient`` ，
因此以 ``lettuceClusterRedisClient`` 名称定义即可覆盖组件。

``uriList`` 属性的设置直接沿用了原始 ``redisstore-lettuce.xml`` 中的设置。
创建继承其他客户端类的类时，也请直接沿用 ``redisstore-lettuce.xml`` 中的属性设置。

以上即可启用拓扑更新监控。

.. _redisstore_mechanism_to_decide_client:

使用客户端类的决定机制
-----------------------------------------------------------------------------------------------
:ref:`redisstore_redis_client_config_how_select_client` 中说明了可以通过环境设置值 ``nablarch.lettuce.clientType`` 设置要使用的客户端类。
这里具体说明客户端类是如何决定的机制。

3个客户端类的组件中实际使用哪个，由 :java:extdoc:`LettuceRedisClientProvider<nablarch.integration.redisstore.lettuce.LettuceRedisClientProvider>` 决定。

``LettuceRedisClientProvider`` 在 ``redisstore-lettuce.xml`` 中定义如下。

.. code-block:: xml

  <component name="lettuceRedisClientProvider" class="nablarch.integration.redisstore.lettuce.LettuceRedisClientProvider">
      <property name="clientType" value="${nablarch.lettuce.clientType}" />
      <property name="clientList">
          <list>
              <component-ref name="lettuceSimpleRedisClient" />
              <component-ref name="lettuceMasterReplicaRedisClient" />
              <component-ref name="lettuceClusterRedisClient" />
          </list>
      </property>
  </component>

此类具有 ``clientList`` 和 ``clientType`` 两个属性。

``clientList`` 中列表形式设置了候选的客户端类组件。
而 ``clientType`` 中设置要使用的客户端类的标识符。

各客户端类具有返回自身标识符的 ``getType()`` 方法。
``LettuceRedisClientProvider`` 比较 ``clientType`` 属性中设置的值和 ``clientList`` 属性中设置的各组件返回的 ``getType()`` 值。
然后，将值一致的组件决定为实际使用的组件。

``LettuceRedisClientProvider`` 实现了 :java:extdoc:`ComponentFactory<nablarch.core.repository.di.ComponentFactory>` ，
``createObject()`` 方法实现为返回决定的客户端类（:java:extdoc:`LettuceRedisClient<nablarch.integration.redisstore.lettuce.LettuceRedisClient>`）的组件。

.. _redisstore_initialize_client:

客户端类的初始化
-----------------------------------------------------------------------------------------------
本适配器提供的3个客户端类都需要初始化才能建立到Redis的连接。

各客户端类实现了 :java:extdoc:`Initializable<nablarch.core.repository.initialization.Initializable>` ，
执行 ``initialize()`` 方法即可建立到Redis的连接。
因此，必须将使用的客户端类组件设置到 :java:extdoc:`BasicApplicationInitializer<nablarch.core.repository.initialization.BasicApplicationInitializer>` 的 ``initializeList`` 属性中。

实际的 ``initializeList`` 设置如下，使用 :ref:`redisstore_mechanism_to_decide_client` 中说明的 ``LettuceRedisClientProvider`` 的组件。

.. code-block:: xml

  <!-- 需要初始化的组件 -->
  <component name="initializer"
             class="nablarch.core.repository.initialization.BasicApplicationInitializer">
    <property name="initializeList">
      <list>
        <!-- 省略 -->
        <component-ref name="lettuceRedisClientProvider"/>
      </list>
    </property>
  </component>

这样做可以在不更改组件定义记述的情况下，初始化决定的客户端类组件。

客户端类的废弃处理
-----------------------------------------------------------------------------------------------

各客户端类实现了 :java:extdoc:`Disposable<nablarch.core.repository.disposal.Disposable>` ，
执行 ``dispose()`` 方法即可关闭到Redis的连接。
因此，通过将使用的客户端类组件设置到 :java:extdoc:`BasicApplicationDisposer<nablarch.core.repository.disposal.BasicApplicationDisposer>` 的 ``disposableList`` 属性中，
可以在应用程序结束时关闭与Redis的连接。

.. code-block:: xml

  <!-- 需要废弃的组件 -->
  <component name="disposer"
             class="nablarch.core.repository.disposal.BasicApplicationDisposer">
    <property name="disposableList">
      <list>
        <!-- 省略 -->
        <component-ref name="lettuceRedisClientProvider"/>
      </list>
    </property>
  </component>

与 ``BasicApplicationInitializer`` 的 ``initializeList`` 一样，
在 ``disposableList`` 属性中指定 ``LettuceRedisClientProvider`` 组件，即可执行实际使用的客户端类的废弃处理。


.. _redisstore_session_persistence:

会话信息的保存方法
-----------------------------------------------------------------------------------------------
保存到Redis的会话信息以 ``nablarch.session.<会话ID>`` 的键保存。

以下显示使用 ``redis-cli`` 显示保存键的状态。

.. code-block:: shell

  127.0.0.1:6379> keys *
  1) "nablarch.session.8b00bce5-d19f-4f63-b1fe-d14ecca9a4f6"

此外，会话信息（:java:extdoc:`SessionEntry<nablarch.common.web.session.SessionEntry>` 的列表）
默认以 :java:extdoc:`JavaSerializeStateEncoder<nablarch.common.web.session.encoder.JavaSerializeStateEncoder>` 
编码的二进制形式保存。

可以通过以 ``serializeEncoder`` 名称定义其他编码器的组件来更改使用的编码器。

.. _redisstore_expiration:

有效期的管理方法
-----------------------------------------------------------------------------------------------
Redis提供了为保存的键设置有效期的机制。
已过有效期的键会自动删除。

本适配器使用此Redis的有效期机制来管理会话的有效期。
因此，已过有效期的会话信息会自动删除，无需准备批处理来删除作为垃圾残留的会话信息。

以下显示使用 `pttl 命令（外部网站，英语） <https://redis.io/docs/latest/commands/pttl/>`_ 确认会话信息有效期的状态。

.. code-block:: shell

  127.0.0.1:6379> pttl "nablarch.session.8b00bce5-d19f-4f63-b1fe-d14ecca9a4f6"
  (integer) 879774
