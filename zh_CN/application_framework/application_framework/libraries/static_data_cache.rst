静态数据的缓存
==================================================

.. contents:: 目录
  :depth: 3
  :local:

提供用于加速访问存储在数据库或文件等中的静态数据的缓存功能。

该功能单独无法运行。
如果要缓存静态数据，请参考 :ref:`static_data_cache-load_data` 实现数据加载处理。

.. important::

  该功能将缓存的数据保存在堆上。
  如果缓存大量数据，可能会导致Full GC频繁发生，从而对性能产生负面影响，因此需要注意。

功能概要
--------------------------------------------------
可以缓存任意数据
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
通过实现该功能提供的接口，可以轻松缓存任意数据。

此外，数据缓存的控制由该功能提供的类进行。
因此，如果要缓存新数据，只需实现加载数据的处理即可。
特别是不需要处理多线程环境下的同步处理等，这是很大的优点。

详细信息请参考 :ref:`static_data_cache-load_data` 。

模块列表
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core</artifactId>
  </dependency>

使用方法
--------------------------------------------------

.. _static_data_cache-load_data:

缓存任意数据
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
要缓存任意静态数据，需要以下工作。

#. 实现 :java:extdoc:`StaticDataLoader <nablarch.core.cache.StaticDataLoader>` 接口，实现加载数据的处理。
#. 在 :java:extdoc:`BasicStaticDataCache <nablarch.core.cache.BasicStaticDataCache>` 类中设置 :java:extdoc:`StaticDataLoader <nablarch.core.cache.StaticDataLoader>` 的实现类。
#. 在使用缓存的类中设置 :java:extdoc:`BasicStaticDataCache <nablarch.core.cache.BasicStaticDataCache>` 。

以下显示详细步骤。

实现StaticDataLoader接口创建加载器
  实现 :java:extdoc:`StaticDataLoader <nablarch.core.cache.StaticDataLoader>` ，实现从任意存储加载静态数据的处理。

  虽然有多个需要实现的方法，但按照以下规则实现即可。

  :loadAll: 在系统启动时进行批量加载的情况下实现。其他情况下返回 `return null` 即可。
  :getValue: 加载与唯一标识静态数据的id对应的数据。
             当缓存中不存在数据时调用此方法。
  :上述以外的方法: 在想按索引管理静态数据时使用。
                       由于该功能不仅实现方法复杂，而且使用的好处也不大，因此原则上不使用。

                       实现时返回 `return null` 即可。

在BasicStaticDataCache类中设置加载器
  将实现 :java:extdoc:`StaticDataLoader <nablarch.core.cache.StaticDataLoader>` 的加载器设置到 :java:extdoc:`BasicStaticDataCache.loader <nablarch.core.cache.BasicStaticDataCache.setLoader(nablarch.core.cache.StaticDataLoader)>` 中。

  配置示例请参考 :ref:`静态数据缓存的配置文件示例 <static_data_cache-config_sample>` 。

  .. important::

    如配置示例中所示，必须将 :java:extdoc:`BasicStaticDataCache <nablarch.core.cache.BasicStaticDataCache>` 设置为初始化对象。
    初始化的详细信息请参考 :ref:`repository-initialize_object` 。

在使用缓存的类中设置BasicStaticDataCache
  在使用缓存的类中设置带有加载器的 :java:extdoc:`BasicStaticDataCache <nablarch.core.cache.BasicStaticDataCache>` ，就可以访问缓存的数据。


  以下显示使用缓存的类的示例。

  在此示例中，使用设置的 :java:extdoc:`StaticDataCache <nablarch.core.cache.StaticDataCache>` 获取缓存的数据。

  配置示例请参考 :ref:`静态数据缓存的配置文件示例 <static_data_cache-config_sample>` 。

  .. code-block:: java

    public class SampleService {

      private StaticDataCache<Integer> sampleCache;

      public int calc(int n) {
          return sampleCache.getValue(n);
      }

      public void setSampleCache(StaticDataCache<Integer> sampleCache) {
          this.sampleCache = sampleCache;
      }
    }

.. _static_data_cache-config_sample:

配置文件示例
  .. code-block:: xml

    <!-- 加载器 -->
    <component name="sampleLoader" class="sample.SampleLoader" />

    <!-- BasicStaticDataCache，用于缓存加载器加载的数据 -->
    <component name="sampleDataCache" class="nablarch.core.cache.BasicStaticDataCache">
      <property name="loader" ref="sampleLoader" />
    </component>

    <!--
    使用加载器加载的缓存的类。
    通过此类中设置的BasicStaticDataCache访问缓存。
    -->
    <component class="sample.SampleService">
      <property name="sampleCache" ref="sampleDataCache" />
    </component>

    <component name="initializer"
        class="nablarch.core.repository.initialization.BasicApplicationInitializer">

      <property name="initializeList">
        <list>
          <!-- 初始化BasicStaticDataCache -->
          <component-ref name="sampleDataCache" />
        </list>
      </property>

    </component>


.. _static_data_cache-cache_timing:

控制数据缓存时机
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
数据缓存时机可以从以下2种模式中选择。

* 批量加载（启动时缓存所有数据）
* 按需加载（首次收到获取请求时缓存）

.. tip::

  原则上在启动时批量加载没有问题，但如果静态数据量大且只使用一部分，选择按需加载比较好。
  例如，像批处理应用程序那样只访问部分数据时，选择按需加载比较好。


加载时机的更改在设置了加载器的 :java:extdoc:`BasicStaticDataCache.loadOnStartup <nablarch.core.cache.BasicStaticDataCache.setLoadOnStartup(boolean)>` 中进行。
如果此属性设置为 `true` ，则在启动时批量加载。

在以下示例中，由于设置了 `true` ，因此在启动时批量缓存数据。

.. code-block:: xml

  <component name="sampleLoader" class="sample.SampleLoader" />

  <component name="sampleDataCache" class="nablarch.core.cache.BasicStaticDataCache">
    <property name="loader" ref="sampleLoader" />
    <property name="loadOnStartup" value="true" />
  </component>
