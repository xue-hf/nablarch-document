.. _micrometer_adaptor:

Micrometer适配器
==================================================

.. contents:: 目录
  :depth: 3
  :local:

提供用于使用 `Micrometer(外部网站、英语) <https://micrometer.io/>`_ 进行指标收集的适配器。

使用本适配器可以实现以下功能，获得便于应用程序运维监控的优势。

* 可以收集JVM内存使用量、CPU使用率等应用程序指标
* 可以将收集的指标联动到 `Datadog(外部网站) <https://www.datadoghq.com/ja/>`_ 或 `CloudWatch(外部网站) <https://aws.amazon.com/jp/cloudwatch/>`_ 等监控服务


模块列表
--------------------------------------------------
.. code-block:: xml

  <!-- Micrometer适配器 -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-micrometer-adaptor</artifactId>
  </dependency>
  
.. tip::

  使用Micrometer版本1.13.0进行测试。
  更改版本时，请在项目侧进行测试确认无问题。

进行Micrometer适配器的使用设置
--------------------------------------------------
要在Micrometer中收集指标，需要创建称为 `registry(外部网站、英语) <https://docs.micrometer.io/micrometer/reference/concepts/registry.html>`_ 的类。
本适配器提供了用于将此registry注册到 :ref:`repository` 的 :java:extdoc:`ComponentFactory<nablarch.core.repository.di.ComponentFactory>` 。

这里以将 `LoggingMeterRegistry(外部网站、英语)`_ 注册为组件的 :java:extdoc:`LoggingMeterRegistryFactory<nablarch.integration.micrometer.logging.LoggingMeterRegistryFactory>` 为例说明设置方法。

.. tip::

  `LoggingMeterRegistry(外部网站、英语)`_ 提供了使用SLF4J或Java Util Logging将指标输出到日志的功能。
  未特别设置时，将使用Java Util Logging输出到标准输出，适合进行简单的动作确认。

  其他registry需要准备联动目标服务、创建输出指标的处理等，比较麻烦。
  因此，本说明使用可以最简单确认动作的 `LoggingMeterRegistry(外部网站、英语)`_ 。

另外，基础应用程序使用 `Web应用程序的Example(外部网站) <https://github.com/nablarch/nablarch-example-web>`_ 。

.. _micrometer_adaptor_declare_default_meter_binder_list_provider_as_component:

将DefaultMeterBinderListProvider声明为组件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Micrometer中存在 `MeterBinder(外部网站、英语)`_ 接口。

JVM内存使用量、CPU使用率等常用指标的收集，已事先以实现了此接口的类形式准备好。
（例：JVM内存使用量为 `JvmMemoryMetrics(外部网站、英语)`_ 、CPU使用率为 `ProcessorMetrics(外部网站、英语)`_ ）

:java:extdoc:`DefaultMeterBinderListProvider <nablarch.integration.micrometer.DefaultMeterBinderListProvider>` 是提供此 `MeterBinder(外部网站、英语)`_ 列表的类，使用本类可以收集JVM内存使用量、CPU使用率等指标。

首先在 ``src/main/resources/web-component-configuration.xml`` 中，添加此 :java:extdoc:`DefaultMeterBinderListProvider <nablarch.integration.micrometer.DefaultMeterBinderListProvider>` 的声明。

.. code-block:: xml

  <component name="meterBinderListProvider"
             class="nablarch.integration.micrometer.DefaultMeterBinderListProvider" />


关于收集的指标的具体说明，请参阅 :ref:`micrometer_default_metrics` 。

将DefaultMeterBinderListProvider设为废弃处理对象
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:java:extdoc:`DefaultMeterBinderListProvider <nablarch.integration.micrometer.DefaultMeterBinderListProvider>` 是需要废弃处理的组件，因此如下声明为废弃处理对象。

.. code-block:: xml
  
  <component name="disposer"
      class="nablarch.core.repository.disposal.BasicApplicationDisposer">

    <property name="disposableList">
      <list>
        <component-ref name="meterBinderListProvider"/>
      </list>
    </property>

  </component>

关于对象的废弃处理，请参阅 :ref:`repository-dispose_object` 。

将registry的factory类声明为组件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: xml

  <component class="nablarch.integration.micrometer.logging.LoggingMeterRegistryFactory">
    <property name="meterBinderListProvider" ref="meterBinderListProvider" />
    <property name="applicationDisposer" ref="disposer" />
  </component>

接下来，将各registry准备的factory类声明为组件。

此时，设置 ``meterBinderListProvider`` 和 ``applicationDisposer`` 两个属性。
各属性分别设置上面声明的 :java:extdoc:`DefaultMeterBinderListProvider <nablarch.integration.micrometer.DefaultMeterBinderListProvider>` 和 :java:extdoc:`BasicApplicationDisposer <nablarch.core.repository.disposal.BasicApplicationDisposer>` 。

关于本适配器提供的factory类，在 :ref:`micrometer_registry_factory` 中列出。


创建设置文件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

最后，在 ``src/main/resources`` 下创建名为 ``micrometer.properties`` 的文本文件。

这里内容如下描述。

.. code-block:: properties

  # 为方便确认，每5秒输出指标（默认1分钟）
  nablarch.micrometer.logging.step=5s
  # 设置即使在step指定时间之前应用程序结束，废弃处理时也会输出日志
  nablarch.micrometer.logging.logInactive=true

.. important::

  ``micrometer.properties`` 即使内容为空也必须配置。


.. _micrometer_metrics_output_example:

执行结果
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
以上，即可使用 ``LoggingMeterRegistry`` 收集指标。

启动应用程序，可以确认收集的指标如下输出到标准输出。

.. code-block:: text

  2020-09-04 15:33:40.689 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.gc.count{memory.manager.name=PS Scavenge} throughput=2.6/s
  2020-09-04 15:33:40.690 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.gc.count{memory.manager.name=PS MarkSweep} throughput=0.4/s
  2020-09-04 15:33:40.691 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.buffer.count{id=mapped} value=0 buffers
  2020-09-04 15:33:40.691 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.buffer.count{id=direct} value=2 buffers
  2020-09-04 15:33:40.692 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.buffer.memory.used{id=direct} value=124 KiB
  2020-09-04 15:33:40.692 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.buffer.memory.used{id=mapped} value=0 B
  2020-09-04 15:33:40.692 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.buffer.total.capacity{id=mapped} value=0 B
  2020-09-04 15:33:40.692 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.buffer.total.capacity{id=direct} value=124 KiB
  2020-09-04 15:33:40.693 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.classes.loaded{} value=9932 classes
  2020-09-04 15:33:40.693 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.gc.live.data.size{} value=0 B
  2020-09-04 15:33:40.693 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.gc.max.data.size{} value=2.65918 GiB
  2020-09-04 15:33:40.694 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.committed{area=heap,id=PS Old Gen} value=182.5 MiB
  2020-09-04 15:33:40.694 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.committed{area=heap,id=PS Survivor Space} value=44 MiB
  2020-09-04 15:33:40.694 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.committed{area=heap,id=PS Eden Space} value=197 MiB
  2020-09-04 15:33:40.694 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.committed{area=nonheap,id=Code Cache} value=29.125 MiB
  2020-09-04 15:33:40.694 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.committed{area=nonheap,id=Compressed Class Space} value=6.796875 MiB
  2020-09-04 15:33:40.694 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.committed{area=nonheap,id=Metaspace} value=55.789062 MiB
  2020-09-04 15:33:40.695 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.max{area=heap,id=PS Old Gen} value=2.65918 GiB
  2020-09-04 15:33:40.695 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.max{area=heap,id=PS Survivor Space} value=44 MiB
  2020-09-04 15:33:40.696 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.max{area=nonheap,id=Code Cache} value=240 MiB
  2020-09-04 15:33:40.696 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.max{area=nonheap,id=Metaspace} value=-1 B
  2020-09-04 15:33:40.696 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.max{area=heap,id=PS Eden Space} value=1.243652 GiB
  2020-09-04 15:33:40.696 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.max{area=nonheap,id=Compressed Class Space} value=1 GiB
  2020-09-04 15:33:40.697 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.used{area=nonheap,id=Code Cache} value=28.618713 MiB
  2020-09-04 15:33:40.697 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.used{area=nonheap,id=Compressed Class Space} value=6.270714 MiB
  2020-09-04 15:33:40.697 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.used{area=nonheap,id=Metaspace} value=54.118324 MiB
  2020-09-04 15:33:40.698 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.used{area=heap,id=PS Old Gen} value=69.320663 MiB
  2020-09-04 15:33:40.698 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.used{area=heap,id=PS Survivor Space} value=7.926674 MiB
  2020-09-04 15:33:40.698 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.used{area=heap,id=PS Eden Space} value=171.750542 MiB
  2020-09-04 15:33:40.698 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.threads.daemon{} value=28 threads
  2020-09-04 15:33:40.698 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.threads.live{} value=29 threads
  2020-09-04 15:33:40.699 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.threads.peak{} value=31 threads
  2020-09-04 15:33:40.702 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.threads.states{state=blocked} value=0 threads
  2020-09-04 15:33:40.703 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.threads.states{state=runnable} value=9 threads
  2020-09-04 15:33:40.703 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.threads.states{state=new} value=0 threads
  2020-09-04 15:33:40.703 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.threads.states{state=timed-waiting} value=3 threads
  2020-09-04 15:33:40.703 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.threads.states{state=terminated} value=0 threads
  2020-09-04 15:33:40.704 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.threads.states{state=waiting} value=17 threads
  2020-09-04 15:33:41.199 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: process.cpu.usage{} value=0.111672
  2020-09-04 15:33:41.199 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: process.start.time{} value=444222h 33m 14.544s
  2020-09-04 15:33:41.199 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: process.uptime{} value=26.729s
  2020-09-04 15:33:41.200 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: system.cpu.count{} value=8
  2020-09-04 15:33:41.200 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: system.cpu.usage{} value=0.394545



.. _micrometer_registry_factory:

Registry Factory
--------------------------------------------------
本适配器提供以下registry的factory类。

.. list-table::

  * - Registry
    - Factory类
    - 提供的适配器版本
  * - `SimpleMeterRegistry(外部网站、英语)`_
    - :java:extdoc:`SimpleMeterRegistryFactory <nablarch.integration.micrometer.simple.SimpleMeterRegistryFactory>`
    - ``1.0.0`` 以上
  * - `LoggingMeterRegistry(外部网站、英语)`_
    - :java:extdoc:`LoggingMeterRegistryFactory <nablarch.integration.micrometer.logging.LoggingMeterRegistryFactory>`
    - ``1.0.0`` 以上
  * - `CloudWatchMeterRegistry(外部网站、英语)`_
    - :java:extdoc:`CloudWatchMeterRegistryFactory <nablarch.integration.micrometer.cloudwatch.CloudWatchMeterRegistryFactory>`
    - ``1.0.0`` 以上
  * - `DatadogMeterRegistry(外部网站、英语)`_
    - :java:extdoc:`DatadogMeterRegistryFactory <nablarch.integration.micrometer.datadog.DatadogMeterRegistryFactory>`
    - ``1.0.0`` 以上
  * - `StatsdMeterRegistry(外部网站、英语)`_
    - :java:extdoc:`StatsdMeterRegistryFactory <nablarch.integration.micrometer.statsd.StatsdMeterRegistryFactory>`
    - ``1.0.0`` 以上
  * - `OtlpMeterRegistry(外部网站、英语)`_
    - :java:extdoc:`OtlpMeterRegistryFactory <nablarch.integration.micrometer.otlp.OtlpMeterRegistryFactory>`
    - ``1.3.0`` 以上


.. _micrometer_configuration:

设置文件
--------------------------------------------------

存放位置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
本适配器的设置文件，创建时应以 ``micrometer.properties`` 名称存放在类路径根目录下。

格式
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
此文件中记载的设置，按以下格式描述。

.. code-block:: text

  nablarch.micrometer.<subPrefix>.<key>=要设置的值

这里， ``<subPrefix>`` 设置的值因使用的registry factory而异。

各registry factory在 ``<subPrefix>`` 中指定的值如下表所示。

=================================== ================
Registry Factory                      subPrefix
=================================== ================
``SimpleMeterRegistryFactory``      ``simple``
``LoggingMeterRegistryFactory``     ``logging``
``CloudWatchMeterRegistryFactory``  ``cloudwatch``
``DatadogMeterRegistryFactory``     ``datadog``
``StatsdMeterRegistryFactory``      ``statsd``
``OtlpMeterRegistryFactory``        ``otlp``
=================================== ================

另外， ``<key>`` 中指定Micrometer为各registry提供的 `设置类(外部网站、英语) <https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/config/MeterRegistryConfig.html>`_ 中定义的方法同名。

例如，对于 `DatadogMeterRegistry(外部网站、英语)`_ 准备了 `DatadogConfig(外部网站、英语)`_ 设置类。
并且，此设置类中定义了 `apiKey(外部网站、英语) <https://javadoc.io/doc/io.micrometer/micrometer-registry-datadog/1.13.0/io/micrometer/datadog/DatadogConfig.html#apiKey()>`_ 方法。




因此，在 ``micrometer.properties`` 中如下描述即可设置 ``apiKey`` 。

.. code-block:: text

  nablarch.micrometer.datadog.apiKey=XXXXXXXXXXXXXXXXXXXX

通过OS环境变量・系统属性覆盖
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``micrometer.properties`` 中描述的设置值，可以通过OS环境变量和系统属性覆盖。

设置值按优先级从高到低的顺序采用如下。

#. 系统属性中指定的值
#. OS环境变量中指定的值
#. ``micrometer.properties`` 的设置值

例如，假设在以下条件中设置。

micrometer.properties

  .. code-block:: text

    nablarch.micrometer.example.one=PROPERTIES
    nablarch.micrometer.example.two=PROPERTIES
    nablarch.micrometer.example.three=PROPERTIES

OS环境变量

  .. code-block:: text

    $ export NABLARCH_MICROMETER_EXAMPLE_TWO=OS_ENV

    $ export NABLARCH_MICROMETER_EXAMPLE_THREE=OS_ENV

系统属性

  .. code-block:: text

    -Dnablarch.micrometer.example.three=SYSTEM_PROP

此时，各设置值最终采用如下值。

========== ================
key        采用的值
========== ================
``one``    ``PROPERTIES``
``two``    ``OS_ENV``
``three``  ``SYSTEM_PROP``
========== ================

关于通过OS环境变量覆盖时的命名规则，请参阅 :ref:`关于OS环境变量的名称 <repository-overwrite_environment_configuration_by_os_env_var_naming_rule>` 。

更改设置的前缀
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

设置的前缀 (``nablarch.micrometer.<subPrefix>``) ，可通过在各registry factory中指定 :java:extdoc:`prefix <nablarch.integration.micrometer.MeterRegistryFactory.setPrefix(java.lang.String)>` 属性来更改。

以下记载更改前缀的示例。

.. code-block:: xml

  <component name="meterRegistry" class="nablarch.integration.micrometer.logging.LoggingMeterRegistryFactory">
    <property name="meterBinderListProvider" ref="meterBinderListProvider" />
    <property name="applicationDisposer" ref="disposer" />

    <!-- 在prefix属性中设置任意前缀 -->
    <property name="prefix" value="sample.prefix" />
  </component>

此时， ``micrometer.properties`` 可以如下设置。

.. code-block:: text

  sample.prefix.step=10s

更改设置文件的位置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

设置文件（``micrometer.properties``）的位置，可通过以下方法更改。

首先，在registry factory的 :java:extdoc:`xmlConfigPath <nablarch.integration.micrometer.MeterRegistryFactory.setXmlConfigPath(java.lang.String)>` 属性中，指定读取设置文件的XML文件路径。

.. code-block:: xml

  <component name="meterRegistry" class="nablarch.integration.micrometer.logging.LoggingMeterRegistryFactory">
    <property name="meterBinderListProvider" ref="meterBinderListProvider" />
    <property name="applicationDisposer" ref="disposer" />

    <!-- 指定读取设置文件的XML文件路径 -->
    <property name="xmlConfigPath" value="config/metrics.xml" />
  </component>

然后，在 ``xmlConfigPath`` 属性指定的位置，配置读取设置文件的XML文件。
以下设置中，类路径内的 ``config/metrics.properties`` 将作为设置文件被读取。

.. code-block:: xml

  <?xml version="1.0" encoding="UTF-8"?>
  <component-configuration
          xmlns="http://tis.co.jp/nablarch/component-configuration"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://tis.co.jp/nablarch/component-configuration https://nablarch.github.io/schema/component-configuration.xsd">

    <!-- 读取Micrometer适配器的设置 -->
    <config-file file="config/metrics.properties" />

  </component-configuration>

.. tip::

  此XML文件可以用与组件设置文件相同的格式描述。

  但是，即使在此文件中定义组件，也无法从系统仓库获取引用。


.. _micrometer_default_metrics:

DefaultMeterBinderListProvider收集的指标
-----------------------------------------------------

:java:extdoc:`DefaultMeterBinderListProvider <nablarch.integration.micrometer.DefaultMeterBinderListProvider>` 生成的 `MeterBinder(外部网站、英语)`_ 列表包含以下类。


* `JvmMemoryMetrics(外部网站、英语)`_
* `JvmGcMetrics(外部网站、英语)`_
* `JvmThreadMetrics(外部网站、英语)`_
* `ClassLoaderMetrics(外部网站、英语)`_
* `ProcessorMetrics(外部网站、英语)`_
* `FileDescriptorMetrics(外部网站、英语)`_
* `UptimeMetrics(外部网站、英语)`_
* :java:extdoc:`NablarchGcCountMetrics <nablarch.integration.micrometer.instrument.binder.jvm.NablarchGcCountMetrics>`



由此，可收集以下指标。

.. list-table::

  * - 指标名
    - 说明
  * - ``jvm.buffer.count``
    - 缓冲池内的缓冲数量
  * - ``jvm.buffer.memory.used``
    - 缓冲池的使用量
  * - ``jvm.buffer.total.capacity``
    - 缓冲池的总容量
  * - ``jvm.memory.used``
    - 内存池的内存使用量
  * - ``jvm.memory.committed``
    - 内存池的已提交内存量
  * - ``jvm.memory.max``
    - 内存池的最大内存量
  * - ``jvm.gc.max.data.size``
    - OLD区域的最大内存量
  * - ``jvm.gc.live.data.size``
    - Full GC后的OLD区域内存使用量
  * - ``jvm.gc.memory.promoted``
    - GC前后增加的OLD区域内存使用量增量
  * - ``jvm.gc.memory.allocated``
    - 上次GC后至本次GC的Young区域内存使用量增量
  * - ``jvm.gc.concurrent.phase.time``
    - 并发阶段的处理时间
  * - ``jvm.gc.pause``
    - GC暂停所花费的时间
  * - ``jvm.threads.peak``
    - 线程数的峰值
  * - ``jvm.threads.daemon``
    - 当前守护线程数
  * - ``jvm.threads.live``
    - 当前非守护线程数
  * - ``jvm.threads.states``
    - 当前各线程状态的数目
  * - ``jvm.classes.loaded``
    - 当前已加载的类数
  * - ``jvm.classes.unloaded``
    - JVM启动至今卸载的类数
  * - ``system.cpu.count``
    - JVM可使用的处理器数
  * - ``system.load.average.1m``
    - 最近1分钟的系统负载平均值（参考： `OperatingSystemMXBean(外部网站) <https://docs.oracle.com/javase/jp/17/docs/api/java.management/java/lang/management/OperatingSystemMXBean.html#getSystemLoadAverage()>`_ ）
  * - ``system.cpu.usage``
    - 系统整体的最近CPU使用率
  * - ``process.cpu.usage``
    - JVM的最近CPU使用率
  * - ``process.files.open``
    - 打开的文件描述符数
  * - ``process.files.max``
    - 文件描述符的最大数
  * - ``process.uptime``
    - JVM的运行时间
  * - ``process.start.time``
    - JVM的启动时间（UNIX时间）
  * - ``jvm.gc.count``
    - GC次数
  * - ``jvm.threads.started``
    - JVM启动的线程数
  * - ``process.cpu.time``
    - Java虚拟机进程使用的CPU时间

实际收集的指标示例请参阅 :ref:`micrometer_metrics_output_example` 。

设置通用标签
--------------------------------------------------

在registry factory的 :java:extdoc:`tags <nablarch.integration.micrometer.MeterRegistryFactory.setTags(java.util.Map)>` 属性中，可以设置所有指标共通的标签。

此功能可用于设置识别应用程序运行主机、实例、区域等信息的用途。

以下记载设置方法。

.. code-block:: xml

  <component name="meterRegistry" class="nablarch.integration.micrometer.logging.LoggingMeterRegistryFactory">
    <property name="meterBinderListProvider" ref="meterBinderListProvider" />
    <property name="applicationDisposer" ref="disposer" />

    <!-- 在tags属性中设置共通标签 -->
    <property name="tags">
      <map>
        <entry key="foo" value="FOO" />
        <entry key="bar" value="BAR" />
      </map>
    </property>
  </component>

``tags`` 属性的类型为 ``Map<String, String>`` ，可以使用 ``<map>`` 标签设置。
此时，Map的键对应标签名，Map的值对应标签值。

上述设置情况下，收集的指标如下所示。

.. code-block:: text

  （省略）
  2020-09-04 17:30:06.656 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: process.start.time{bar=BAR,foo=FOO} value=444224h 29m 38.875000064s
  2020-09-04 17:30:06.656 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: process.uptime{bar=BAR,foo=FOO} value=27.849s
  2020-09-04 17:30:06.656 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: system.cpu.count{bar=BAR,foo=FOO} value=8
  2020-09-04 17:30:06.657 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: system.cpu.usage{bar=BAR,foo=FOO} value=0.475654

可以确认所有指标都设置了 ``foo=FOO``、``bar=BAR`` 的标签。

.. _micrometer_collaboration:

与监控服务联动
--------------------------------------------------

要与监控服务联动，大致需要进行以下设置。

#. 添加监控服务或联动方法对应的Micrometer模块到依赖
#. 将使用的registry factory定义为组件
#. 其他，各监控服务独自的设置

这里说明与各监控服务联动的方法。


与Datadog联动
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

添加依赖
  .. code-block:: xml

    <dependency>
      <groupId>io.micrometer</groupId>
      <artifactId>micrometer-registry-datadog</artifactId>
      <version>1.13.0</version>
    </dependency>

声明registry factory
  .. code-block:: xml
  
    <component name="meterRegistry" class="nablarch.integration.micrometer.datadog.DatadogMeterRegistryFactory">
      <property name="meterBinderListProvider" ref="meterBinderListProvider" />
      <property name="applicationDisposer" ref="disposer" />
    </component>

设置API密钥
  .. code-block:: text

    nablarch.micrometer.datadog.apiKey=XXXXXXXXXXXXXXXX

  API密钥可通过 ``nablarch.micrometer.datadog.apiKey`` 设置。

设置站点URL
  .. code-block:: text

    nablarch.micrometer.datadog.uri=<站点URL>

  站点URL可通过 ``nablarch.micrometer.datadog.uri`` 设置。

  其他设置请参阅 `DatadogConfig(外部网站、英语)`_ 。

禁用联动
  .. code-block:: text

    nablarch.micrometer.datadog.enabled=false
    nablarch.micrometer.datadog.apiKey=XXXXXXXXXXXXXXXX

  在 ``micrometer.properties`` 中将 ``nablarch.micrometer.datadog.enabled`` 设为 ``false`` ，可以禁用指标联动。
  此设置可通过环境变量覆盖，因此可以仅在生产环境通过环境变量覆盖为 ``true`` 来启用联动。

  .. important::
    禁用联动时， ``nablarch.micrometer.datadog.apiKey`` 也需要设置某种值。
    值可以是虚拟的。

与CloudWatch联动
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

添加依赖
  .. code-block:: xml

    <dependency>
      <groupId>io.micrometer</groupId>
      <artifactId>micrometer-registry-cloudwatch2</artifactId>
      <version>1.13.0</version>
    </dependency>

声明registry factory
  .. code-block:: xml
  
    <component name="meterRegistry" class="nablarch.integration.micrometer.cloudwatch.CloudWatchMeterRegistryFactory">
      <property name="meterBinderListProvider" ref="meterBinderListProvider" />
      <property name="applicationDisposer" ref="disposer" />
    </component>

设置区域和访问密钥
  .. code-block:: bash
    
    $ export AWS_REGION=ap-northeast-1

    $ export AWS_ACCESS_KEY_ID=XXXXXXXXXXXXXXXXXXXXX

    $ export AWS_SECRET_ACCESS_KEY=YYYYYYYYYYYYYYYYYYYYY

  ``micrometer-registry-cloudwatch2`` 模块使用AWS SDK。
  因此，区域和访问密钥等设置遵循AWS SDK的方法。

  以上是在Linux中使用OS环境变量设置的示例。
  更详细的信息请参阅 `AWS文档(外部网站) <https://docs.aws.amazon.com/ja_jp/sdk-for-java/v1/developer-guide/setup-credentials.html>`_ 。

设置命名空间
  .. code-block:: text

    nablarch.micrometer.cloudwatch.namespace=test

  指标的自定义命名空间可通过 ``nablarch.micrometer.cloudwatch.namespace`` 设置。

  其他设置请参阅 `CloudWatchConfig(外部网站、英语)`_ 。

更详细的设置
  无法通过OS环境变量或设置文件指定、需要更详细设置时，可以通过实现 :java:extdoc:`CloudWatchAsyncClientProvider <nablarch.integration.micrometer.cloudwatch.CloudWatchAsyncClientProvider>` 的自定义provider来对应。

  .. code-block:: java

      package example.micrometer.cloudwatch;

      import nablarch.integration.micrometer.cloudwatch.CloudWatchAsyncClientProvider;
      import software.amazon.awssdk.services.cloudwatch.CloudWatchAsyncClient;

      public class CustomCloudWatchAsyncClientProvider implements CloudWatchAsyncClientProvider {
          @Override
          public CloudWatchAsyncClient provide() {
              return CloudWatchAsyncClient
                      .builder()
                      .asyncConfiguration(...) // 进行任意设置
                      .build();
          }
      }

  :java:extdoc:`CloudWatchAsyncClientProvider <nablarch.integration.micrometer.cloudwatch.CloudWatchAsyncClientProvider>` 具有提供 ``CloudWatchAsyncClient`` 的 ``provide()`` 方法。
  在自定义provider中，实现 ``provide()`` 方法以返回进行了任意设置的 ``CloudWatchAsyncClient`` 。

  .. code-block:: xml

    <component name="meterRegistry" class="nablarch.integration.micrometer.cloudwatch.CloudWatchMeterRegistryFactory">
      <property name="meterBinderListProvider" ref="meterBinderListProvider" />
      <property name="applicationDisposer" ref="disposer" />

      <!-- 在cloudWatchAsyncClientProvider属性中设置自定义provider -->
      <property name="cloudWatchAsyncClientProvider">
        <component class="example.micrometer.cloudwatch.CustomCloudWatchAsyncClientProvider" />
      </property>
    </component>

  创建的自定义provider，设置在 ``CloudWatchMeterRegistryFactory`` 的 :java:extdoc:`cloudWatchAsyncClientProvider <nablarch.integration.micrometer.cloudwatch.CloudWatchMeterRegistryFactory.setCloudWatchAsyncClientProvider(nablarch.integration.micrometer.cloudwatch.CloudWatchAsyncClientProvider)>` 属性中。

  由此，自定义provider生成的 ``CloudWatchAsyncClient`` 将用于指标联动。

  .. tip::

    默认使用 `CloudWatchAsyncClient.create() (外部网站、英语) <https://javadoc.io/static/software.amazon.awssdk/cloudwatch/2.13.4/software/amazon/awssdk/services/cloudwatch/CloudWatchAsyncClient.html#create-->`_ 创建的实例。

禁用联动
  .. code-block:: text

    nablarch.micrometer.cloudwatch.enabled=false
    nablarch.micrometer.cloudwatch.namespace=test

  在 ``micrometer.properties`` 中将 ``nablarch.micrometer.cloudwatch.enabled`` 设为 ``false`` ，可以禁用指标联动。
  此设置可通过环境变量覆盖，因此可以仅在生产环境通过环境变量覆盖为 ``true`` 来启用联动。

  .. important::
    禁用联动时， ``nablarch.micrometer.cloudwatch.namespace`` 也需要设置某种值。
    另外，需要设置环境变量 ``AWS_REGION`` 。

    值都可以是虚拟的。

与Azure联动
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

使用Micrometer向Azure联动指标的方法
  Azure提供了使用Java代理向Azure联动指标的机制（**Java 3.0 Agent**）。

  * `使用Azure Monitor Application Insights监视Java的无代码应用程序(外部网站) <https://learn.microsoft.com/ja-jp/azure/azure-monitor/app/opentelemetry-enable?tabs=java>`_

  此Java 3.0 Agent提供了自动收集Micrometer `全局registry(外部网站、英语) <https://docs.micrometer.io/micrometer/reference/concepts/registry.html#_global_registry>`_ 输出的指标并联动到Azure的机制。

  * `从应用程序发送自定义遥测(外部网站) <https://learn.microsoft.com/ja-jp/azure/azure-monitor/app/opentelemetry-enable?tabs=java>`_

  .. important::
    Java 3.0 Agent在初始化处理中会加载大量jar文件。
    因此，Java 3.0 Agent初始化处理期间GC可能会频繁发生。

    因此，请注意应用程序启动后一段时间内，由于GC影响性能可能会暂时下降。

    另外，高负载时Java 3.0 Agent的处理开销可能会影响性能。
    因此，性能测试时请像生产环境一样引入Java 3.0 Agent，确认性能在预期范围内。


  Java 3.0 Agent的设置方法请参阅 :ref:`Azure中的分布式追踪 <azure_distributed_tracing>` 。

使用Micrometer适配器向Azure联动指标的设置
  要在Micrometer适配器中将指标联动到Azure，需要进行以下设置。

  * 在应用程序启动选项中添加Java 3.0 Agent
  * 定义组件以使用全局registry作为 ``MeterRegistry``

  关于第1个启动选项的设置方法，请参阅 `Azure文档 <https://learn.microsoft.com/ja-jp/azure/azure-monitor/app/opentelemetry-enable?tabs=java#modify-your-application>`_ 。

  关于第2个使用全局registry的方法，本适配器提供了全局registry的factory类 :java:extdoc:`GlobalMeterRegistryFactory <nablarch.integration.micrometer.GlobalMeterRegistryFactory>` 。
  以下显示此factory类的组件定义示例。

  .. code-block:: xml

    <component name="meterRegistry" class="nablarch.integration.micrometer.GlobalMeterRegistryFactory">
      <property name="meterBinderListProvider" ref="meterBinderListProvider" />
      <property name="applicationDisposer" ref="disposer" />
    </component>

  此设置后，指标收集将由全局registry执行。
  并且，全局registry收集的指标将由Java 3.0 Agent联动到Azure。

  .. tip::
    此方法使用Java 3.0 Agent，不使用Azure用的 ``MeterRegistry`` 。
    因此，即使不将Azure用模块添加到依赖也可以联动指标。


关于详细设置
  指标联动由Azure提供的Java 3.0 Agent执行。
  因此，指标联动的相关设置都需要使用Java 3.0 Agent提供的方法进行。

  关于Java 3.0 Agent设置的详细信息，请参阅 `配置选项(外部网站) <https://learn.microsoft.com/ja-jp/azure/azure-monitor/app/java-standalone-config>`_ 。

  .. important::
    本适配器用的设置文件 ``micrometer.properties`` 不能使用，但文件需要配置（内容为空即可）。

禁用联动
  不使用Java 3.0 Agent启动应用程序，即可禁用指标联动。

通过StatsD联动
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Datadog支持使用 `DogStatsD(外部网站) <https://docs.datadoghq.com/ja/developers/dogstatsd/?tab=hostagent>`_ 这种 `StatsD(外部网站、英语) <https://github.com/statsd/statsd>`_ 协议进行联动。
因此，使用 ``micrometer-registry-statsd`` 模块，也可以通过StatsD与Datadog联动。

这里以使用StatsD协议与Datadog联动为例进行说明。
关于DogStatsD的安装方法等，请参阅 `Datadog网站(外部网站) <https://docs.datadoghq.com/ja/agent/>`_ 。

添加依赖
  .. code-block:: xml

    <dependency>
      <groupId>io.micrometer</groupId>
      <artifactId>micrometer-registry-statsd</artifactId>
      <version>1.13.0</version>
    </dependency>

声明registry factory
  .. code-block:: xml
  
    <component name="meterRegistry" class="nablarch.integration.micrometer.statsd.StatsdMeterRegistryFactory">
      <property name="meterBinderListProvider" ref="meterBinderListProvider" />
      <property name="applicationDisposer" ref="disposer" />
    </component>

根据需要描述设置文件
  与StatsD守护进程联动的设置，已调整为默认值与默认配置安装DogStatsD时一致。
  
  因此，如果使用默认配置安装DogStatsD，则无需特别明示设置即可与DogStatsD联动。

  如果使用默认配置以外的配置安装，请参阅 `StatsdConfig(外部网站、英语)`_ ，进行与实际环境相符的设置。

  .. code-block:: text

    # 更改端口
    nablarch.micrometer.statsd.port=9999

禁用联动
  .. code-block:: text

    nablarch.micrometer.statsd.enabled=false

  在 ``micrometer.properties`` 中将 ``nablarch.micrometer.statsd.enabled`` 设为 ``false`` ，可以禁用指标联动。
  此设置可通过环境变量覆盖，因此可以仅在生产环境通过环境变量覆盖为 ``true`` 来启用联动。

通过OpenTelemetry Protocol (OTLP)联动
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

许多监控服务支持 `OpenTelemetry(外部网站) <https://opentelemetry.io/ja>`_ ，可以使用通信协议OpenTelemetry Protocol（以下简称OTLP）收集指标。
使用 ``micrometer-registry-otlp`` 模块，可以通过OTLP与各种监控服务联动。

  .. important::
     OpenTelemetry的指标收集中，何种联动方法合适（可用）因监控服务而异，请确认使用监控服务的信息。
     作为示例，以下显示一些监控服务的信息。

     * `Datadog的OpenTelemetry(外部网站) <https://docs.datadoghq.com/ja/opentelemetry/>`_
     * `New Relic介绍的OpenTelemetry(外部网站) <https://docs.newrelic.com/jp/docs/opentelemetry/opentelemetry-introduction>`_
     * `Prometheus | HTTP API | OTLP Receiver(外部网站、英语) <https://prometheus.io/docs/prometheus/latest/querying/api/#otlp-receiver>`_

这里以向在localhost 9090端口启动的Prometheus通过OTLP联动为例进行说明。

添加依赖
  .. code-block:: xml

    <dependency>
      <groupId>io.micrometer</groupId>
      <artifactId>micrometer-registry-otlp</artifactId>
      <version>1.13.0</version>
    </dependency>

声明registry factory
  .. code-block:: xml
  
    <component name="meterRegistry" class="nablarch.integration.micrometer.otlp.OtlpMeterRegistryFactory">
      <property name="meterBinderListProvider" ref="meterBinderListProvider" />
      <property name="applicationDisposer" ref="disposer" />
    </component>

描述设置文件
  .. code-block:: text

    # 更改发送目标
    nablarch.micrometer.otlp.url=http://localhost:9090/api/v1/otlp/v1/metrics

设置头部信息
  .. code-block:: text

    nablarch.micrometer.otlp.headers=key1=value1,key2=value2

  如果需要认证使用的API密钥等头部信息，可通过 ``nablarch.micrometer.otlp.headers`` 设置。

禁用联动
  .. code-block:: text

    nablarch.micrometer.otlp.enabled=false

  在 ``micrometer.properties`` 中将 ``nablarch.micrometer.otlp.enabled`` 设为 ``false`` ，可以禁用指标联动。
  此设置可通过环境变量覆盖，因此可以仅在生产环境通过环境变量覆盖为 ``true`` 来启用联动。

各应用程序形式收集的指标示例
---------------------------------------------------------

这里说明按应用程序形式（Web・批处理）分别收集哪些指标比较好。

Web应用程序收集的指标示例
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

HTTP请求的处理时间
  通过测量每个HTTP请求的处理时间，可以实现以下功能。

  * 确认各URL的访问频率
  * 确认请求处理需要多少时间

  此外，通过测量百分位数，还可以确认大部分请求在多长的时间内可以处理完成。

  收集这些指标的方法请参阅以下指南。

  * :ref:`micrometer_timer_metrics_handler`
  * :ref:`micrometer_timer_metrics_handler_percentiles`

SQL的处理时间
  通过测量SQL的处理时间，可以实现以下功能。

  * 确认各SQL处理需要多少时间
  * 确认是否存在处理时间比预想长的SQL

  测量SQL处理时间的方法请参阅以下指南。

  * :ref:`micrometer_sql_time`

各日志级别的输出次数
  通过测量各日志级别的输出次数，可以实现以下功能。

  * 确认警告日志是否异常频繁输出（攻击检测）
  * 检测错误日志

  关于各日志级别的输出次数，请参阅以下指南。

  * :ref:`micrometer_log_count`

应用服务器或库提供的资源信息
  将应用服务器或库提供的资源（线程池或DB连接池等）状态作为指标收集，
  可以在故障发生时作为确定原因位置的信息源使用。

  许多应用服务器通过JMX的MBean公开资源状态。
  收集MBean信息的方法请参阅以下指南。

  * :ref:`micrometer_mbean_metrics`

批处理应用程序收集的指标示例
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

批处理的处理时间
  平时测量批处理的处理时间可以了解正常时的处理时间。
  这样当处理时间与正常时不同的值时，可以快速检测异常。

  批处理的处理时间可以通过 :ref:`micrometer_default_metrics` 中收集的 ``process.uptime`` 测量。

事务单位的处理时间
  通过测量事务单位的处理时间，可以确认多线程批处理是否均匀分配处理等。

  此外，与批处理的处理时间一样，当处理时间偏离正常时也可以快速检测异常。

  关于批处理事务单位的处理时间测量，请参阅以下指南。

  * :ref:`micrometer_adaptor_batch_transaction_time`

批处理的处理件数
  通过测量批处理的处理件数，可以实现以下功能。

  * 确认批处理的进度
  * 确认是否以预想的速度进行处理
  * 确认是否处理了预想的件数

  关于批处理处理件数的测量，请参阅以下指南。

  * :ref:`micrometer_batch_processed_count`

SQL的处理时间
  通过测量SQL的处理时间，可以实现以下功能。

  * 确认各SQL处理需要多少时间
  * 确认是否存在处理时间比预想长的SQL

  测量SQL处理时间的方法请参阅以下指南。

  * :ref:`micrometer_sql_time`

各日志级别的输出次数
  通过测量各日志级别的输出次数，可以检测警告日志或错误日志。

  关于各日志级别的输出次数，请参阅以下指南。

  * :ref:`micrometer_log_count`

库提供的资源信息
  将库提供的资源（DB连接池等）状态作为指标收集，
  可以在故障发生时作为确定原因位置的信息源使用。

  某些库通过JMX的MBean公开资源状态。
  收集MBean信息的方法请参阅以下指南。

  * :ref:`micrometer_mbean_metrics`


.. _micrometer_timer_metrics_handler:

测量处理时间的处理程序
--------------------------------------------------

在处理程序队列中设置 :java:extdoc:`TimerMetricsHandler <nablarch.integration.micrometer.instrument.handler.TimerMetricsHandler>` ，
可以测量后续处理程序的处理时间并将其作为指标收集。
这样可以监控处理程序队列内处理的平均处理时间和最大处理时间。

``TimerMetricsHandler`` 需要设置实现 :java:extdoc:`HandlerMetricsMetaDataBuilder <nablarch.integration.micrometer.instrument.handler.HandlerMetricsMetaDataBuilder>` 接口的类实例。
``HandlerMetricsMetaDataBuilder`` 提供构建收集指标时设置的以下元信息的功能。

* 指标的名称
* 指标的说明
* 指标设置的标签列表

以下显示 ``HandlerMetricsMetaDataBuilder`` 的实现示例。

.. code-block:: java

  import io.micrometer.core.instrument.Tag;
  import nablarch.fw.ExecutionContext;
  import nablarch.integration.micrometer.instrument.handler.HandlerMetricsMetaDataBuilder;

  import java.util.Arrays;
  import java.util.List;

  public class CustomHandlerMetricsMetaDataBuilder<TData, TResult>
      implements HandlerMetricsMetaDataBuilder<TData, TResult> {
    
      @Override
      public String getMetricsName() {
          return "metrics.name";
      }

      @Override
      public String getMetricsDescription() {
          return "Description of this metrics.";
      }

      @Override
      public List<Tag> buildTagList(TData param, ExecutionContext executionContext, TResult tResult, Throwable thrownThrowable) {
          return Arrays.asList(Tag.of("foo", "FOO"), Tag.of("bar", "BAR"));
      }
  }

``getMetricsName()`` 和 ``getMetricsDescription()`` 分别实现返回指标的名称和说明。

``buildTagList()`` 中传递了传递给处理程序的参数和后续处理程序的执行结果，以及后续处理程序抛出的异常（未抛出异常时为 ``null`` ）。
本方法根据需要参考这些信息，实现以 ``List<io.micrometer.core.instrument.Tag>`` 返回指标设置的标签列表。

接下来，以下显示在处理程序队列中设置 ``TimerMetricsHandler`` 的示例。

.. code-block:: xml

  <!-- 处理程序队列构成 -->
  <component name="webFrontController"
             class="nablarch.fw.web.servlet.WebFrontController">
    <property name="handlerQueue">
      <list>
        <!-- 省略 -->

        <component class="nablarch.integration.micrometer.instrument.handler.TimerMetricsHandler">
          <property name="meterRegistry" ref="meterRegistry" />

          <property name="handlerMetricsMetaDataBuilder">
            <component class="xxx.CustomHandlerMetricsMetaDataBuilder" />
          </property>
        </component>

        <!-- 省略 -->
      </list>
    </property>
  </component>

在处理程序队列中添加 ``TimerMetricsHandler`` ，并在 ``handlerMetricsMetaDataBuilder`` 属性中设置创建的 ``HandlerMetricsMetaDataBuilder`` 组件。

此外， ``meterRegistry`` 属性需要设置使用的注册表工厂生成的 `MeterRegistry(外部网站、英语)`_ 。

这样可以收集此后处理程序的处理时间作为指标。

另外，Nablarch提供了以下功能作为 ``HandlerMetricsMetaDataBuilder`` 的实现类。
详情请参阅链接处的说明。

* :ref:`micrometer_adaptor_http_request_process_time_metrics`

.. _micrometer_timer_metrics_handler_percentiles:

收集百分位数
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``TimerMetricsHandler`` 提供了以下属性用于将百分位数值联动到监控服务。

.. list-table::

  * - 属性
    - 说明
  * - ``percentiles``
    - 要收集的百分位数值列表。
      收集95百分位数时指定为 ``0.95`` 。
  * - ``enablePercentileHistogram``
    - 是否将收集的直方图桶联动到监控服务的标志。
      如果联动目标的监控服务不支持从直方图计算百分位数值的机制，则此设置被忽略。
  * - ``serviceLevelObjectives``
    - 添加到收集的直方图中的桶值列表。
      单位为毫秒。
      此值基于SLO(Service Level Objective)设置。
  * - ``minimumExpectedValue``
    - 设置收集的直方图桶的最小值。
      单位为毫秒。
  * - ``maximumExpectedValue``
    - 设置收集的直方图桶的最大值。
      单位为毫秒。

这些属性用作Micrometer提供的 `Timer(外部网站、英语)`_ 中设置的值。
更详细的说明请参阅 `Micrometer文档 <https://docs.micrometer.io/micrometer/reference/concepts/histogram-quantiles.html>`_ 。

这些属性默认全部未设置，因此不收集百分位数信息。
如果需要收集百分位数信息，请显式设置这些属性。
以下显示设置示例。

.. code-block:: xml

  <component class="nablarch.integration.micrometer.instrument.handler.TimerMetricsHandler">
    <property name="meterRegistry" ref="meterRegistry" />
    <property name="handlerMetricsMetaDataBuilder">
      <component class="nablarch.integration.micrometer.instrument.http.HttpRequestTimeMetricsMetaDataBuilder" />
    </property>

    <!-- 收集98、90、50百分位数 -->
    <property name="percentiles">
      <list>
        <value>0.98</value>
        <value>0.90</value>
        <value>0.50</value>
      </list>
    </property>

    <!-- 将直方图桶联动到监控服务 -->
    <property name="enablePercentileHistogram" value="true" />

    <!-- 将1000ms、1500ms设置为SLO -->
    <property name="serviceLevelObjectives">
      <list>
        <value>1000</value>
        <value>1500</value>
      </list>
    </property>
    
    <!-- 将桶最小值设为500 ms -->
    <property name="minimumExpectedValue" value="500" />
    <!-- 将桶最大值设为3000 ms -->
    <property name="maximumExpectedValue" value="3000" />
  </component>

使用支持直方图桶的 ``MeterRegistry`` 时，通过上述设置可以收集以下指标。

.. code-block:: text

  http_server_requests_seconds{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",quantile="0.98",} 1.475346432
  http_server_requests_seconds{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",quantile="0.9",} 1.408237568
  http_server_requests_seconds{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",quantile="0.5",} 0.737148928
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="0.5",} 9.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="0.536870911",} 9.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="0.626349396",} 12.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="0.715827881",} 16.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="0.805306366",} 16.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="0.894784851",} 17.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="0.984263336",} 17.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="1.0",} 18.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="1.073741824",} 20.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="1.431655765",} 29.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="1.5",} 32.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="1.789569706",} 32.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="2.147483647",} 32.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="2.505397588",} 32.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="2.863311529",} 32.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="3.0",} 32.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="+Inf",} 32.0

.. tip::
  本适配器提供的 ``MeterRegistry`` 中只有 ``OtlpMeterRegistry`` 支持直方图桶。

  示例中为了显示直方图桶的具体示例（``http_server_requests_seconds_bucket``）使用了 `PrometheusMeterRegistry(外部网站、英语)`_ （`Prometheus(外部网站、英语) <https://prometheus.io/>`_ 支持通过直方图计算百分位数）。
  但是， ``PrometheusMeterRegistry`` 的 ``MeterRegistryFactory`` 本适配器不提供。
  实际想尝试 ``PrometheusMeterRegistry`` 时，请自行准备如下类。

  .. code-block:: java

    package example.micrometer.prometheus;

    import io.micrometer.prometheusmetrics.PrometheusConfig;
    import io.micrometer.prometheusmetrics.PrometheusMeterRegistry;
    import nablarch.core.repository.di.DiContainer;
    import nablarch.integration.micrometer.MeterRegistryFactory;
    import nablarch.integration.micrometer.MicrometerConfiguration;
    import nablarch.integration.micrometer.NablarchMeterRegistryConfig;

    public class PrometheusMeterRegistryFactory extends MeterRegistryFactory<PrometheusMeterRegistry> {

        @Override
        protected PrometheusMeterRegistry createMeterRegistry(MicrometerConfiguration micrometerConfiguration) {
            return new PrometheusMeterRegistry(new Config(prefix, micrometerConfiguration));
        }

        @Override
        public PrometheusMeterRegistry createObject() {
            return doCreateObject();
        }

        static class Config extends NablarchMeterRegistryConfig implements PrometheusConfig {

            public Config(String prefix, DiContainer diContainer) {
                super(prefix, diContainer);
            }

            @Override
            protected String subPrefix() {
                return "prometheus";
            }
        }
    }

预先准备的HandlerMetricsMetaDataBuilder实现
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

这里介绍Nablarch预先准备的 ``HandlerMetricsMetaDataBuilder`` 实现类。

.. _micrometer_adaptor_http_request_process_time_metrics:

收集HTTP请求的处理时间
*********************************************************************

:java:extdoc:`HttpRequestTimeMetricsMetaDataBuilder <nablarch.integration.micrometer.instrument.http.HttpRequestTimeMetricsMetaDataBuilder>` 用于构建HTTP请求处理时间测量指标的元信息。

本类在指标名称中使用 ``http.server.requests`` 。

此外，本类生成以下标签。

.. list-table::

  * - 标签名
    - 说明
  * - ``class``
    - 处理请求的Action类名(``Class.getName()``)。
      无法获取时为 ``UNKNOWN`` 。
  * - ``method``
    - 处理请求的Action类方法名与参数类型名(``Class.getCanonicalName()``)用下划线(``_``)连接而成的字符串。
      无法获取时为 ``UNKNOWN`` 。
  * - ``httpMethod``
    - HTTP方法
  * - ``status``
    - HTTP状态码
  * - ``outcome``
    - 表示状态码种类的字符串（1XX: ``INFORMATION`` , 2XX: ``SUCCESS`` , 3XX: ``REDIRECTION`` , 4XX: ``CLIENT_ERROR`` , 5XX: ``SERVER_ERROR`` , 其他: ``UNKNOWN`` ）
  * - ``exception``
    - 请求处理中抛出的异常的简单名（未抛出异常时为 ``None`` ）

以下显示使用本类的设置示例。

.. code-block:: xml

  <!-- 处理程序队列构成 -->
  <component name="webFrontController"
             class="nablarch.fw.web.servlet.WebFrontController">
    <property name="handlerQueue">
      <list>
        <!-- HTTP请求处理时间指标收集处理程序 -->
        <component class="nablarch.integration.micrometer.instrument.handler.TimerMetricsHandler">
          <!-- 将注册表工厂生成的 MeterRegistry 设置到 meterRegistry 属性 -->
          <property name="meterRegistry" ref="meterRegistry" />

          <!-- 将 HttpRequestTimeMetricsMetaDataBuilder 设置到 handlerMetricsMetaDataBuilder -->
          <property name="handlerMetricsMetaDataBuilder">
            <component class="nablarch.integration.micrometer.instrument.http.HttpRequestTimeMetricsMetaDataBuilder" />
          </property>
        </component>

        <component class="nablarch.fw.web.handler.HttpCharacterEncodingHandler"/>

        <!-- 省略 -->
     </list>
    </property>
  </component>

为测量请求整体的处理时间， ``TimerMetricsHandler`` 设置在处理程序队列的开头。

通过以上设置，使用 ``LoggingMeterRegistry`` 时可以收集以下指标。

.. code-block:: text

  2020-10-06 13:52:10.309 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: http.server.requests{class=com.nablarch.example.app.web.action.AuthenticationAction,exception=None,httpMethod=POST,method=login_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext,outcome=REDIRECTION,status=303} throughput=0.2/s mean=0.4617585s max=0.4617585s
  2020-10-06 13:52:10.309 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: http.server.requests{class=com.nablarch.example.app.web.action.IndustryAction,exception=None,httpMethod=GET,method=find,outcome=SUCCESS,status=200} throughput=0.2/s mean=0.103277s max=0.103277s
  2020-10-06 13:52:10.310 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: http.server.requests{class=com.nablarch.example.app.web.action.AuthenticationAction,exception=None,httpMethod=GET,method=index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext,outcome=SUCCESS,status=200} throughput=0.2/s mean=4.7409146s max=4.7409146s
  2020-10-06 13:52:10.310 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: http.server.requests{class=com.nablarch.example.app.web.action.ProjectAction,exception=None,httpMethod=GET,method=index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext,outcome=SUCCESS,status=200} throughput=0.2/s mean=0.5329547s max=0.5329547s

.. _micrometer_adaptor_batch_transaction_time:

测量批处理事务单位的处理时间
--------------------------------------------------

使用 :java:extdoc:`BatchTransactionTimeMetricsLogger <nablarch.integration.micrometer.instrument.batch.BatchTransactionTimeMetricsLogger>` 可以测量 :ref:`nablarch_batch` 事务单位的处理时间作为指标。
这样可以监控事务单位的平均处理时间和最大处理时间。

``BatchTransactionTimeMetricsLogger`` 使用 `Timer(外部网站、英语)`_ 以 ``batch.transaction.time`` 名称收集指标。
此名称可以通过 :java:extdoc:`setMetricsName(String) <nablarch.integration.micrometer.instrument.batch.BatchTransactionTimeMetricsLogger.setMetricsName(java.lang.String)>` 更改。

此外，指标会附加以下标签。

.. list-table::

  * - 标签名
    - 说明
  * - ``class``
    - Action的类名（从 :ref:`-requestPath <nablarch_batch-resolve_action>` 获取的值）

以下显示使用 ``BatchTransactionTimeMetricsLogger`` 的设置示例。

.. code-block:: xml

  <!-- 组合多个CommitLogger -->
  <component name="commitLogger"
             class="nablarch.core.log.app.CompositeCommitLogger">
    <property name="commitLoggerList">
      <list>
        <!-- 设置默认的 CommitLogger -->
        <component class="nablarch.core.log.app.BasicCommitLogger">
          <property name="interval" value="${nablarch.commitLogger.interval}" />
        </component>

        <!-- 事务单位处理时间的测量 -->
        <component class="nablarch.integration.micrometer.instrument.batch.BatchTransactionTimeMetricsLogger">
          <property name="meterRegistry" ref="meterRegistry" />
        </component>
      </list>
    </property>
  </component>

首先，以 ``commitLogger`` 名称将 :java:extdoc:`CompositeCommitLogger <nablarch.core.log.app.CompositeCommitLogger>` 定义为组件。
然后，在 ``commitLoggerList`` 属性中设置 :java:extdoc:`BasicCommitLogger <nablarch.core.log.app.BasicCommitLogger>` 和 ``BatchTransactionTimeMetricsLogger`` 的组件。

通过以上设置，可以测量事务单位的时间。
以下说明其机制。

Nablarch批处理通过 :ref:`loop_handler` 控制事务的提交间隔。
此事务循环控制处理程序提供了在事务提交时调用 :java:extdoc:`CommitLogger <nablarch.core.log.app.CommitLogger>` 的 ``increment(long)`` 方法的机制。
此 ``CommitLogger`` 实体可以通过以 ``commitLogger`` 名称定义组件来覆盖。

``BatchTransactionTimeMetricsLogger`` 实现了 ``CommitLogger`` 接口。
然后，通过测量 ``increment(long)`` 调用间隔来测量事务单位的时间。
因此，以 ``commitLogger`` 名称定义 ``BatchTransactionTimeMetricsLogger`` 组件，即可测量事务单位的时间。

但是，如果直接将 ``BatchTransactionTimeMetricsLogger`` 以 ``commitLogger`` 名称定义，默认定义的 ``CommitLogger`` 组件 ``BasicCommitLogger`` 将无法工作。
因此上述设置示例中，使用可以组合多个 ``CommitLogger`` 的 ``CompositeCommitLogger`` ，使 ``BasicCommitLogger`` 和 ``BatchTransactionTimeMetricsLogger`` 并用。

使用 ``LoggingMeterRegistry`` 时， ``BatchTransactionTimeMetricsLogger`` 的测量结果输出如下。

.. code-block:: text

  12 17, 2020 1:50:33 午後 io.micrometer.core.instrument.logging.LoggingMeterRegistry lambda$publish$5
  情報: batch.transaction.time{class=MetricsTestAction} throughput=1/s mean=2.61463556s max=3.0790852s

.. _micrometer_batch_processed_count:

测量批处理的处理件数
--------------------------------------------------

使用 :java:extdoc:`BatchProcessedRecordCountMetricsLogger <nablarch.integration.micrometer.instrument.batch.BatchProcessedRecordCountMetricsLogger>` 可以测量 :ref:`nablarch_batch` 处理的输入数据件数。
这样可以监控批处理的进度和处理速度的变化。

``BatchProcessedRecordCountMetricsLogger`` 使用 `Counter(外部网站、英语)`_ 以 ``batch.processed.record.count`` 名称收集指标。
此名称可以通过 :java:extdoc:`setMetricsName(String) <nablarch.integration.micrometer.instrument.batch.BatchProcessedRecordCountMetricsLogger.setMetricsName(java.lang.String)>` 更改。

此外，指标会附加以下标签。

.. list-table::

  * - 标签名
    - 说明
  * - ``class``
    - Action的类名（从 :ref:`-requestPath <nablarch_batch-resolve_action>` 获取的值）

以下显示使用 ``BatchProcessedRecordCountMetricsLogger`` 的设置示例。

.. code-block:: xml

  <!-- 组合多个CommitLogger -->
  <component name="commitLogger"
             class="nablarch.core.log.app.CompositeCommitLogger">
    <property name="commitLoggerList">
      <list>
        <!-- 设置默认的 CommitLogger -->
        <component class="nablarch.core.log.app.BasicCommitLogger">
          <property name="interval" value="${nablarch.commitLogger.interval}" />
        </component>

        <!-- 测量处理件数 -->
        <component class="nablarch.integration.micrometer.instrument.batch.BatchProcessedRecordCountMetricsLogger">
          <property name="meterRegistry" ref="meterRegistry" />
        </component>
      </list>
    </property>
  </component>

``BatchProcessedRecordCountMetricsLogger`` 与"批处理事务单位处理时间的测量"一样，利用 :java:extdoc:`CommitLogger <nablarch.core.log.app.CommitLogger>` 的机制测量处理件数。
关于 ``CommitLogger`` 的机制及其使用方法请参阅 :ref:`micrometer_adaptor_batch_transaction_time` 。

通过以上设置，可以使用 ``BatchProcessedRecordCountMetricsLogger`` 。

使用 ``LoggingMeterRegistry`` 时，可以确认指标输出如下。

.. code-block:: text

  12 23, 2020 3:23:24 午後 io.micrometer.core.instrument.logging.LoggingMeterRegistry lambda$publish$4
  情報: batch.processed.record.count{class=MetricsTestAction} throughput=10/s
  12 23, 2020 3:23:34 午後 io.micrometer.core.instrument.logging.LoggingMeterRegistry lambda$publish$4
  情報: batch.processed.record.count{class=MetricsTestAction} throughput=13/s
  12 23, 2020 3:23:39 午後 io.micrometer.core.instrument.logging.LoggingMeterRegistry lambda$publish$4
  情報: batch.processed.record.count{class=MetricsTestAction} throughput=13/s

.. _micrometer_log_count:

测量各日志级别的输出次数
--------------------------------------------------

使用 :java:extdoc:`LogCountMetrics <nablarch.integration.micrometer.instrument.binder.logging.LogCountMetrics>` 可以测量各日志级别的输出次数。
这样可以监控特定级别日志的输出频率或错误日志的监控等。

``LogCountMetrics`` 使用 `Counter(外部网站、英语)`_ 以 ``log.count`` 名称收集指标。
此名称可以在接收 :java:extdoc:`MetricsMetaData <nablarch.integration.micrometer.instrument.binder.MetricsMetaData>` 的 :java:extdoc:`构造函数 <nablarch.integration.micrometer.instrument.binder.logging.LogCountMetrics.<init>(nablarch.integration.micrometer.instrument.binder.MetricsMetaData)>` 中更改。

此外，指标会附加以下标签。

.. list-table::

  * - 标签名
    - 说明
  * - ``level``
    - 日志级别。
  * - ``logger``
    - 从 :java:extdoc:`LoggerManager <nablarch.core.log.LoggerManager>` 获取日志记录器时使用的名称。

设置LogPublisher
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``LogCountMetrics`` 使用 :java:extdoc:`LogPublisher <nablarch.core.log.basic.LogPublisher>` 的机制检测日志输出事件。

因此开始使用 ``LogCountMetrics`` 前，需要首先进行 ``LogPublisher`` 的设置。
关于 ``LogPublisher`` 的设置请参阅 :ref:`log-publisher_usage` 。

创建自定义的DefaultMeterBinderListProvider
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``LogCountMetrics`` 作为 `MeterBinder(外部网站、英语)`_ 的实现类提供。
因此，需要创建继承 :java:extdoc:`DefaultMeterBinderListProvider <nablarch.integration.micrometer.DefaultMeterBinderListProvider>` 的类，实现返回包含 ``LogCountMetrics`` 的 ``MeterBinder`` 列表。

.. tip::

  关于 ``DefaultMeterBinderListProvider`` 的说明请参阅 :ref:`micrometer_adaptor_declare_default_meter_binder_list_provider_as_component` 。

以下显示其实现示例。

.. code-block:: java

  package example.micrometer.log;

  import io.micrometer.core.instrument.binder.MeterBinder;
  import nablarch.integration.micrometer.DefaultMeterBinderListProvider;
  import nablarch.integration.micrometer.instrument.binder.logging.LogCountMetrics;

  import java.util.ArrayList;
  import java.util.List;

  public class CustomMeterBinderListProvider extends DefaultMeterBinderListProvider {

      @Override
      protected List<MeterBinder> createMeterBinderList() {
          // 向默认的 MeterBinder 列表添加 LogCountMetrics
          List<MeterBinder> meterBinderList = new ArrayList<>(super.createMeterBinderList());
          meterBinderList.add(new LogCountMetrics());
          return meterBinderList;
      }
  }

最后，在 ``MeterRegistryFactory`` 组件的 ``meterBinderListProvider`` 属性中设置创建的自定义 ``DefaultMeterBinderListProvider`` 。
以上即可使用 ``LogCountMetrics`` 。

使用 ``LoggingMeterRegistry`` 时，可以确认指标输出如下。

.. code-block:: text

  2020-12-22 14:25:36.978 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: log.count{level=WARN,logger=com.nablarch.example.app.web.action.MetricsAction} throughput=0.4/s
  2020-12-22 14:25:41.978 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: log.count{level=ERROR,logger=com.nablarch.example.app.web.action.MetricsAction} throughput=1.4/s

聚合对象的日志级别
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

默认只有 ``WARN`` 以上的日志输出次数成为聚合对象。

聚合对象的日志级别阈值可以通过在 ``LogCountMetrics`` 构造函数中传递 :java:extdoc:`LogLevel <nablarch.core.log.basic.LogLevel>` 进行更改。
以下实现示例中将阈值更改为 ``INFO`` 。

.. code-block:: java

  // （省略）
  import nablarch.core.log.basic.LogLevel;

  public class CustomMeterBinderListProvider extends DefaultMeterBinderListProvider {

      @Override
      protected List<MeterBinder> createMeterBinderList() {
          List<MeterBinder> meterBinderList = new ArrayList<>(super.createMeterBinderList());
          meterBinderList.add(new LogCountMetrics(LogLevel.INFO)); // 指定LogLevel的阈值
          return meterBinderList;
      }
  }

.. important::

  如果日志级别阈值设置过低，根据应用程序可能会收集大量指标。
  根据使用监控服务的费用体系，使用费用可能会增加，请注意设置。

.. _micrometer_sql_time:

测量SQL的处理时间
--------------------------------------------------

使用 :java:extdoc:`SqlTimeMetricsDaoContext <nablarch.integration.micrometer.instrument.dao.SqlTimeMetricsDaoContext>` 可以测量通过 :ref:`universal_dao` 执行的SQL处理时间。
这样可以监控各SQL的平均处理时间和最大处理时间。

``SqlTimeMetricsDaoContext`` 使用 `Timer(外部网站、英语)`_ 以 ``sql.process.time`` 名称收集指标。
此名称可以在 ``SqlTimeMetricsDaoContext`` 的工厂类 :java:extdoc:`SqlTimeMetricsDaoContextFactory <nablarch.integration.micrometer.instrument.dao.SqlTimeMetricsDaoContextFactory>` 的 :java:extdoc:`setMetricsName(String) <nablarch.integration.micrometer.instrument.dao.SqlTimeMetricsDaoContextFactory.setMetricsName(java.lang.String)>` 中更改。

此外，指标会附加以下标签。

.. list-table::

  * - 标签名
    - 说明
  * - ``sql.id``
    - 传递给 ``DaoContext`` 方法参数的SQLID（无SQLID时为 ``"None"`` ）
  * - ``entity``
    - 实体类的名称（``Class.getName()`` ）
  * - ``method``
    - 执行的 ``DaoContext`` 的方法名

以下显示使用 ``SqlTimeMetricsDaoContext`` 的设置示例。

.. code-block:: xml

  <!-- 以 daoContextFactory 名称定义 SqlTimeMetricsDaoContextFactory -->
  <component name="daoContextFactory"
             class="nablarch.integration.micrometer.instrument.dao.SqlTimeMetricsDaoContextFactory">
    <!-- 向 delegate 设置委托目标的 DaoContext 工厂 -->
    <property name="delegate">
      <component class="nablarch.common.dao.BasicDaoContextFactory">
        <property name="sequenceIdGenerator">
          <component class="nablarch.common.idgenerator.SequenceIdGenerator" />
        </property>
      </component>
    </property>

    <!-- 将注册表工厂生成的 MeterRegistry 设置到 meterRegistry 属性 -->
    <property name="meterRegistry" ref="meterRegistry" />
  </component>

``SqlTimeMetricsDaoContext`` 通过包装 :java:extdoc:`DaoContext <nablarch.common.dao.DaoContext>` 来测量各数据库访问方法的处理时间。
而 :java:extdoc:`SqlTimeMetricsDaoContextFactory <nablarch.integration.micrometer.instrument.dao.SqlTimeMetricsDaoContextFactory>` 是生成包装 ``DaoContext`` 的 ``SqlTimeMetricsDaoContext`` 的工厂类。

将此 ``SqlTimeMetricsDaoContextFactory`` 以 ``daoContextFactory`` 名称定义为组件。
这样， :ref:`universal_dao` 使用的 ``DaoContext`` 将被替换为 ``SqlTimeMetricsDaoContext`` 。

以上即可使用 ``SqlTimeMetricsDaoContext`` 。

使用 ``LoggingMeterRegistry`` 时，可以确认指标输出如下。

.. code-block:: text

  2020-12-23 15:00:25.161 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: sql.process.time{entity=com.nablarch.example.app.entity.Project,method=delete,sql.id=None} throughput=0.2/s mean=0.0005717s max=0.0005717s
  2020-12-23 15:00:25.161 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: sql.process.time{entity=com.nablarch.example.app.entity.Project,method=findAllBySqlFile,sql.id=SEARCH_PROJECT} throughput=0.6/s mean=0.003364233s max=0.0043483s
  2020-12-23 15:00:25.161 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: sql.process.time{entity=com.nablarch.example.app.web.dto.ProjectDto,method=findBySqlFile,sql.id=FIND_BY_PROJECT} throughput=0.2/s mean=0.000475s max=0.0060838s
  2020-12-23 15:00:25.162 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: sql.process.time{entity=com.nablarch.example.app.entity.Industry,method=findAll,sql.id=None} throughput=0.8/s mean=0.00058155s max=0.0013081s

.. _micrometer_mbean_metrics:

将任意MBean获取的值作为指标测量
-------------------------------------------------------------

使用 :java:extdoc:`JmxGaugeMetrics <nablarch.integration.micrometer.instrument.binder.jmx.JmxGaugeMetrics>` 可以将任意MBean获取的值作为指标测量。
这样可以测量使用的应用服务器或库通过MBean提供的各种信息并进行监控。

.. tip::

  MBean是Java Management Extensions(JMX)定义的Java对象，提供访问管理对象资源的API等。
  Tomcat等许多应用服务器通过MBean公开服务器状态（线程池状态等）。
  应用程序可以通过访问这些MBean获取服务器状态。

  关于JMX的详细信息请参阅 `Java Management Extensions 指南(外部网站) <https://docs.oracle.com/javase/jp/17/jmx/java-management-extensions-jmx-user-guide.html>`_ 。

``JmxGaugeMetrics`` 使用 `Gauge(外部网站、英语)`_ 测量从MBean获取的值。

以下说明 ``JmxGaugeMetrics`` 的设置示例。

首先作为应用服务器提供的MBean引用示例，显示获取Tomcat线程池状态的示例。
接下来作为应用内嵌入的库提供的MBean引用示例，显示获取HikariCP连接池状态的示例。

获取Tomcat线程池的状态
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``JmxGaugeMetrics`` 作为 `MeterBinder(外部网站、英语)`_ 的实现类提供。
因此，需要创建继承 :java:extdoc:`DefaultMeterBinderListProvider <nablarch.integration.micrometer.DefaultMeterBinderListProvider>` 的类，实现返回包含 ``JmxGaugeMetrics`` 的 ``MeterBinder`` 列表。

.. tip::

  关于 ``DefaultMeterBinderListProvider`` 的说明请参阅 :ref:`micrometer_adaptor_declare_default_meter_binder_list_provider_as_component` 。

以下显示实现示例。

.. code-block:: java

  package example.micrometer;

  import io.micrometer.core.instrument.binder.MeterBinder;
  import nablarch.integration.micrometer.DefaultMeterBinderListProvider;
  import nablarch.integration.micrometer.instrument.binder.MetricsMetaData;
  import nablarch.integration.micrometer.instrument.binder.jmx.JmxGaugeMetrics;
  import nablarch.integration.micrometer.instrument.binder.jmx.MBeanAttributeCondition;

  import java.util.ArrayList;
  import java.util.List;

  public class CustomMeterBinderListProvider extends DefaultMeterBinderListProvider {

      @Override
      protected List<MeterBinder> createMeterBinderList() {
          List<MeterBinder> meterBinderList = new ArrayList<>(super.createMeterBinderList());
          meterBinderList.add(new JmxGaugeMetrics(
              // 指标的名称和说明
              new MetricsMetaData("thread.count.current", "Current thread count."),
              // 确定要收集的MBean属性的信息
              new MBeanAttributeCondition("Catalina:type=ThreadPool,name=\"http-nio-8080\"", "currentThreadCount")
          ));
          return meterBinderList;
      }
  }

``JmxGaugeMetrics`` 的构造函数需要传递以下2个类。

* :java:extdoc:`MetricsMetaData <nablarch.integration.micrometer.instrument.binder.MetricsMetaData>`
    * 指定指标的名称、说明、标签等元信息
* :java:extdoc:`MBeanAttributeCondition <nablarch.integration.micrometer.instrument.binder.jmx.MBeanAttributeCondition>`
    * 指定确定要收集Mbean的对象名和属性名

``JmxGaugeMetrics`` 基于 ``MBeanAttributeCondition`` 指定的信息获取MBean信息。
然后，基于 ``MetricsMetaData`` 指定的信息构建指标。

.. tip::

  可以使用JDK附带的JConsole工具确认Tomcat创建的MBean的对象名・属性名。
  使用JConsole连接运行Tomcat的JVM，打开「MBeans」标签页，会显示连接的JVM可获取的MBean列表。

  关于JConsole的详细信息请参阅 `监视和管理指南(外部网站) <https://docs.oracle.com/javase/jp/17/management/using-jconsole.html#GUID-77416B38-7F15-4E35-B3D1-34BFD88350B5>`_ 。

通过以上设置使用 ``LoggingMeterRegistry`` 时，可以确认指标输出如下。

.. code-block:: text

  24-Dec-2020 16:20:24.467 情報 [logging-metrics-publisher] io.micrometer.core.instrument.logging.LoggingMeterRegistry.lambda$publish$3 thread.count.current{} value=10

获取HikariCP连接池的状态
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`HikariCP(外部网站、英语) <https://github.com/brettwooldridge/HikariCP>`_ 提供了可以通过MBean引用连接池信息的功能。

* `MBean (JMX) Monitoring and Management(外部网站、英语) <https://github.com/brettwooldridge/HikariCP/wiki/MBean-(JMX)-Monitoring-and-Management>`_

使用此功能可以通过 ``JmxGaugeMetrics`` 收集连接池信息。

首先，启用HikariCP通过MBean公开信息的功能。
要启用MBean信息公开，在 ``com.zaxxer.hikari.HikariDataSource`` 的 ``registerMbeans`` 属性中设置 ``true`` 。

.. code-block:: xml

  <?xml version="1.0" encoding="UTF-8"?>
  <component-configuration
          xmlns="http://tis.co.jp/nablarch/component-configuration"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://tis.co.jp/nablarch/component-configuration https://nablarch.github.io/schema/component-configuration.xsd">
    <!-- 省略 -->

    <!-- 数据源设置 -->
    <component name="dataSource"
              class="com.zaxxer.hikari.HikariDataSource" autowireType="None">
      <property name="driverClassName" value="${nablarch.db.jdbcDriver}"/>
      <property name="jdbcUrl"         value="${nablarch.db.url}"/>
      <property name="username"        value="${nablarch.db.user}"/>
      <property name="password"        value="${nablarch.db.password}"/>
      <property name="maximumPoolSize" value="${nablarch.db.maxPoolSize}"/>
      <!-- 启用MBean信息公开 -->
      <property name="registerMbeans"  value="true"/>
    </component>

  </component-configuration>

上述设置中， ``HikariDataSource`` 的组件定义在 ``registerMbeans`` 属性中设置了 ``true`` 。

接下来，指定HikariCP公开的MBean对象名和要测量的属性名来设置 ``JmxGaugeMetrics`` 。
对象名和属性名的规格记载在 `上述HikariCP文档(外部网站、英语) <https://github.com/brettwooldridge/HikariCP/wiki/MBean-(JMX)-Monitoring-and-Management#programmatic-access>`_ 中。

以下是测量连接池最大数和活跃数的 ``JmxGaugeMetrics`` 实现示例。

.. code-block:: java

  package com.nablarch.example.app.metrics;

  import io.micrometer.core.instrument.binder.MeterBinder;
  import nablarch.integration.micrometer.DefaultMeterBinderListProvider;
  import nablarch.integration.micrometer.instrument.binder.MetricsMetaData;
  import nablarch.integration.micrometer.instrument.binder.jmx.JmxGaugeMetrics;
  import nablarch.integration.micrometer.instrument.binder.jmx.MBeanAttributeCondition;

  import java.util.ArrayList;
  import java.util.List;

  public class CustomMeterBinderListProvider extends DefaultMeterBinderListProvider {

      @Override
      protected List<MeterBinder> createMeterBinderList() {
          List<MeterBinder> meterBinderList = new ArrayList<>(super.createMeterBinderList());
          // 最大数
          meterBinderList.add(new JmxGaugeMetrics(
              new MetricsMetaData("db.pool.total", "Total DB pool count."),
              new MBeanAttributeCondition("com.zaxxer.hikari:type=Pool (HikariPool-1)", "TotalConnections")
          ));
          // 活跃数
          meterBinderList.add(new JmxGaugeMetrics(
              new MetricsMetaData("db.pool.active", "Active DB pool count."),
              new MBeanAttributeCondition("com.zaxxer.hikari:type=Pool (HikariPool-1)", "ActiveConnections")
          ));
          return meterBinderList;
      }
  }

通过以上设置使用 ``LoggingMeterRegistry`` 时，可以确认指标输出如下。

.. code-block:: text

  2020-12-24 16:37:57.143 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: db.pool.active{} value=0
  2020-12-24 16:37:57.143 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: db.pool.total{} value=5

关于服务器启动时输出的警告日志
*********************************************************************

Micrometer向监控服务联动指标的方法大体存在以下2种。

* 应用程序定期向监控服务发送指标 (Client pushes)
    * Datadog, CloudWatch 等
* 监控服务定期向应用程序查询指标 (Server polls)
    * Prometheus 等

前者(Client pushes)情况下， ``MeterRegistry`` 在组件生成后开始定期发送指标。
另一方面，HikariCP的连接池在首次进行数据库访问时才首次创建的规格。

因此，如果首次数据库访问发生前执行了指标发送， ``JmxGaugeMetrics`` 将引用不存在的连接池信息。
此时，Micrometer会输出以下警告日志。

.. code-block:: text

  24-Dec-2020 16:57:16.729 警告 [logging-metrics-publisher] io.micrometer.core.util.internal.logging.WarnThenDebugLogger.log Failed to apply the value function for the gauge 'db.pool.active'. Note that subsequent logs will be logged at debug level.
          java.lang.RuntimeException: javax.management.InstanceNotFoundException: com.zaxxer.hikari:type=Pool (HikariPool-1)
                  at nablarch.integration.micrometer.instrument.binder.jmx.JmxGaugeMetrics.obtainGaugeValue(JmxGaugeMetrics.java:59)
                  at io.micrometer.core.instrument.Gauge.lambda$builder$0(Gauge.java:58)
                  at io.micrometer.core.instrument.StrongReferenceGaugeFunction.applyAsDouble(StrongReferenceGaugeFunction.java:47)
                  at io.micrometer.core.instrument.internal.DefaultGauge.value(DefaultGauge.java:54)
                  at io.micrometer.core.instrument.logging.LoggingMeterRegistry.lambda$publish$3(LoggingMeterRegistry.java:98)
                  at io.micrometer.core.instrument.Meter.use(Meter.java:158)
                  at io.micrometer.core.instrument.logging.LoggingMeterRegistry.lambda$publish$12(LoggingMeterRegistry.java:97)
                  at java.util.stream.ForEachOps$ForEachOp$OfRef.accept(ForEachOps.java:183)
                  at java.util.stream.SortedOps$SizedRefSortingSink.end(SortedOps.java:357)
                  at java.util.stream.AbstractPipeline.copyInto(AbstractPipeline.java:483)
                  at java.util.stream.AbstractPipeline.wrapAndCopyInto(AbstractPipeline.java:472)
                  at java.util.stream.ForEachOps$ForEachOp.evaluateSequential(ForEachOps.java:150)
                  at java.util.stream.ForEachOps$ForEachOp$OfRef.evaluateSequential(ForEachOps.java:173)
                  at java.util.stream.AbstractPipeline.evaluate(AbstractPipeline.java:234)
                  at java.util.stream.ReferencePipeline.forEach(ReferencePipeline.java:485)
                  at io.micrometer.core.instrument.logging.LoggingMeterRegistry.publish(LoggingMeterRegistry.java:95)
                  at io.micrometer.core.instrument.push.PushMeterRegistry.publishSafely(PushMeterRegistry.java:52)
                  at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
                  at java.util.concurrent.FutureTask.runAndReset(FutureTask.java:308)
                  at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$301(ScheduledThreadPoolExecutor.java:180)
                  at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:294)
                  at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
                  at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
                  at java.lang.Thread.run(Thread.java:748)
          Caused by: javax.management.InstanceNotFoundException: com.zaxxer.hikari:type=Pool (HikariPool-1)
                  at com.sun.jmx.interceptor.DefaultMBeanServerInterceptor.getMBean(DefaultMBeanServerInterceptor.java:1095)
                  at com.sun.jmx.interceptor.DefaultMBeanServerInterceptor.getAttribute(DefaultMBeanServerInterceptor.java:643)
                  at com.sun.jmx.mbeanserver.JmxMBeanServer.getAttribute(JmxMBeanServer.java:678)
                  at nablarch.integration.micrometer.instrument.binder.jmx.JmxGaugeMetrics.obtainGaugeValue(JmxGaugeMetrics.java:52)
                  ... 23 more

连接池未生成期间，指标值为 ``NaN`` 。

.. code-block:: text

  24-Dec-2020 17:01:31.443 情報 [logging-metrics-publisher] io.micrometer.core.instrument.logging.LoggingMeterRegistry.lambda$publish$3 db.pool.active{} value=NaN
  24-Dec-2020 17:01:31.443 情報 [logging-metrics-publisher] io.micrometer.core.instrument.logging.LoggingMeterRegistry.lambda$publish$3 db.pool.total{} value=NaN

此警告日志仅首次输出，第2次以后会被抑制。
此外，执行数据库访问生成连接池后，之后将正常收集连接池的值。

也就是说，此警告日志即使应用程序正常也可能因时序而输出。
但是，没有实质危害，忽略也没有问题。

但是，如果一定要抑制警告日志，可以通过以下实现一定程度上回避。

.. code-block:: java

  package example.micrometer;

  // 省略
  import nablarch.core.log.Logger;
  import nablarch.core.log.LoggerManager;
  import nablarch.core.repository.initialization.Initializable;
  import java.sql.SQLException;
  import javax.sql.DataSource;
  import java.sql.Connection;

  public class CustomMeterBinderListProvider extends DefaultMeterBinderListProvider implements Initializable {
      private static final Logger LOGGER = LoggerManager.get(CustomMeterBinderListProvider.class);

      private DataSource dataSource;

      @Override
      protected List<MeterBinder> createMeterBinderList() {
          // 省略
      }

      public void setDataSource(DataSource dataSource) {
          this.dataSource = dataSource;
      }

      @Override
      public void initialize() {
          try (Connection con = dataSource.getConnection()) {
              // 初始化时建立连接以抑制因无法获取MBean而输出的警告日志
          } catch (SQLException e) {
              LOGGER.logWarn("Failed initial connection.", e);
          }
      }
  }

在自定义的 ``DefaultMeterBinderListProvider`` 中实现 :java:extdoc:`Initializable <nablarch.core.repository.initialization.Initializable>` 。
此外，修改实现以可以接收 ``java.sql.DataSource`` 作为属性。
然后，在 ``initialize()`` 方法中实现连接数据库。

在组件定义中，修改以通过属性传递 ``DataSource`` 。
然后，在需要初始化的组件列表中添加此类。

.. code-block:: xml

  <component name="meterBinderListProvider"
             class="example.micrometer.CustomMeterBinderListProvider">
    <!-- 设置 DataSource -->
    <property name="dataSource" ref="dataSource" />
  </component>

  <!-- 需要初始化的组件 -->
  <component name="initializer"
             class="nablarch.core.repository.initialization.BasicApplicationInitializer">
    <property name="initializeList">
      <list>
        <!-- 省略 -->

        <!-- 添加为需要初始化的组件 -->
        <component-ref name="meterBinderListProvider" />
      </list>
    </property>
  </component>

通过以上修改，系统仓库初始化时将执行数据库连接。
指标发送间隔默认为1分钟，因此大多数情况下指标发送前会创建连接池。
这样可以不输出警告日志。

但是，如果指标发送间隔设置得非常短，系统仓库初始化前可能会发送指标而输出警告日志，请注意。



.. _MeterBinder(外部网站、英语): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/binder/MeterBinder.html
.. _Counter(外部网站、英语): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/Counter.html
.. _Gauge(外部网站、英语): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/Gauge.html
.. _DatadogConfig(外部网站、英语): https://javadoc.io/doc/io.micrometer/micrometer-registry-datadog/1.13.0/io/micrometer/datadog/DatadogConfig.html
.. _CloudWatchConfig(外部网站、英语): https://javadoc.io/doc/io.micrometer/micrometer-registry-cloudwatch2/1.13.0/io/micrometer/cloudwatch2/CloudWatchConfig.html
.. _StatsdConfig(外部网站、英语): https://javadoc.io/doc/io.micrometer/micrometer-registry-statsd/1.13.0/io/micrometer/statsd/StatsdConfig.html
.. _OtlpConfig(外部网站、英语): https://javadoc.io/static/io.micrometer/micrometer-registry-otlp/1.13.0/io/micrometer/registry/otlp/OtlpConfig.html
.. _MeterRegistry(外部网站、英语): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/MeterRegistry.html
.. _DatadogMeterRegistry(外部网站、英语): https://javadoc.io/doc/io.micrometer/micrometer-registry-datadog/1.13.0/io/micrometer/datadog/DatadogMeterRegistry.html
.. _StatsdMeterRegistry(外部网站、英语): https://javadoc.io/doc/io.micrometer/micrometer-registry-statsd/1.13.0/io/micrometer/statsd/StatsdMeterRegistry.html
.. _OtlpMeterRegistry(外部网站、英语): https://javadoc.io/static/io.micrometer/micrometer-registry-otlp/1.13.0/io/micrometer/registry/otlp/OtlpMeterRegistry.html
.. _DatadogMeterRegistry(外部网站、英语): https://javadoc.io/doc/io.micrometer/micrometer-registry-datadog/1.13.0/io/micrometer/datadog/DatadogMeterRegistry.html
.. _CloudWatchMeterRegistry(外部网站、英语): https://javadoc.io/doc/io.micrometer/micrometer-registry-cloudwatch2/1.13.0/io/micrometer/cloudwatch2/CloudWatchMeterRegistry.html
.. _LoggingMeterRegistry(外部网站、英语): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/logging/LoggingMeterRegistry.html
.. _SimpleMeterRegistry(外部网站、英语): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/simple/SimpleMeterRegistry.html
.. _JvmMemoryMetrics(外部网站、英语): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/binder/jvm/JvmMemoryMetrics.html
.. _ProcessorMetrics(外部网站、英语): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/binder/system/ProcessorMetrics.html
.. _JvmGcMetrics(外部网站、英语): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/binder/jvm/JvmGcMetrics.html
.. _JvmThreadMetrics(外部网站、英语): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/binder/jvm/JvmThreadMetrics.html
.. _ClassLoaderMetrics(外部网站、英语): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/binder/jvm/ClassLoaderMetrics.html
.. _FileDescriptorMetrics(外部网站、英语): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/binder/system/FileDescriptorMetrics.html
.. _UptimeMetrics(外部网站、英语): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/binder/system/UptimeMetrics.html
.. _Timer(外部网站、英语): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/Timer.html
.. _PrometheusMeterRegistry(外部网站、英语): https://javadoc.io/doc/io.micrometer/micrometer-registry-prometheus/1.13.0/io/micrometer/prometheusmetrics/PrometheusMeterRegistry.html
