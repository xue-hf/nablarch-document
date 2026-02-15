.. _resource_mapping:

资源映射handler
==================================================
.. contents:: 目录
  :depth: 3
  :local:

本handler提供不经过业务action直接返回响应的功能。
本功能用于通过Nablarch的handler下载静态资源。

.. important::
  使用本handler下载静态资源的方法存在"日志大量输出"、
  "在有大量访问的服务器上，应用服务器负载大"等缺点。

  因此，对于不需要通过handler的静态资源下载，
  不推荐使用本handler。
  静态资源请通过Web容器或Web服务器的功能下载，
  本handler仅限于"需要对内容下载进行授权检查"等
  需要经过其他handler的内容使用。

本handler执行以下处理。

* 返回下载静态资源的响应

.. important::
  本handler主要与 :ref:`request_handler_entry` 组合使用，实现 "当为特定扩展名时下载静态资源" 的功能。

  此用途的使用示例请参考 :ref:`请求handler入口的使用示例 <request_handler_entry_usage>` 。

处理流程如下。
如图中显示，本handler不调用后续handler。

.. image:: ../images/ResourceMapping/flow.png

handler类名
--------------------------------------------------
* :java:extdoc:`nablarch.fw.web.handler.ResourceMapping`

模块列表
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web</artifactId>
  </dependency>

约束
------------------------------

配置在 :ref:`forwarding_handler` 之后
  本handler可以使用 :ref:`forwarding_handler` 的功能提供的 ``forward://`` 方案。
  因此，本handler需要配置在 :ref:`forwarding_handler` 之后。

配置在 :ref:`http_response_handler` 之后
  本handler可以使用 :ref:`http_response_handler` 的功能提供的 ``servlet://`` 、 ``file://`` 、 ``classpath://`` 方案。
  另外，发生错误时返回404(Not Found)响应。
  为处理这些响应，本handler需要配置在 :ref:`http_response_handler` 之后。

.. _resource_mapping_usage:

静态资源的下载
------------------------------

本handler的主要用途下载静态资源时，需要如下设置 ``baseUri`` 和 ``basePath`` 两个属性。

.. code-block:: xml

  <!-- 执行图像文件静态资源下载的handler -->
  <component name="imgMapping"
             class="nablarch.fw.web.handler.ResourceMapping">
    <property name="baseUri" value="/"/>
    <property name="basePath" value="servlet:///"/>
  </component>

各设置项目的含义如下

============================= ==========================================================
设置项目                      含义
============================= ==========================================================
baseUri                       处理对象的URL。如果URL不匹配，handler将
                              |br|
                              返回HTTP状态404(NotFound)响应。
basePath                      匹配baseUri时的响应基础URL。
                              |br|
                              省略方案指定时，使用 ``servlet://`` 方案。
============================= ==========================================================

但是，如果直接将上述设置的handler放入handler队列，
服务器发送的所有URL处理都将作为静态资源处理。
也就是说，handler队列上本handler之后的所有handler都将不会执行。

因此，需要如 :ref:`request_handler_entry_usage` 所述，与 :ref:`request_handler_entry` 组合使用。



.. |br| raw:: html

   <br />
