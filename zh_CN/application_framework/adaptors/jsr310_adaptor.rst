.. _jsr310_adaptor:

JSR310(Date and Time API)适配器
==================================================

.. contents:: 目录
  :depth: 3
  :local:
  
提供用于使用JSR310(Date and Time API)添加的日期时间相关功能的适配器。
使用此适配器，可以在 :ref:`bean_util` 中使用JSR310(Date and Time API)。

.. important::

  本适配器提供的功能从Nablarch 6u2开始已纳入框架本体，因此即使不使用本适配器也可以在 :ref:`bean_util` 中使用JSR310(Date and Time API)。
  本适配器为保持向后兼容而保留。

.. important::

  本适配器支持的类型如下。
  要处理这些以外的类型时，需要在项目侧添加Converter等。
  
  * :java:extdoc:`LocalDate <java.time.LocalDate>`
  * :java:extdoc:`LocalDateTime <java.time.LocalDateTime>`

模块列表
--------------------------------------------------
.. code-block:: xml

  <!-- JSR310适配器 -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-jsr310-adaptor</artifactId>
  </dependency>
  
使用方法
---------------------------------------------------------------------

可转换类型和转换规则等详细信息，请参阅 :java:extdoc:`converter列表 <nablarch.core.beans.converter>` 。

设置
  在 :ref:`repository` 的组件配置文件中添加以下内容，即可启用本功能。

  .. code-block:: xml

      <import file="JSR310.xml" />

.. tip::
 
  想要更改从字符串转换时的格式时，需要进行以下操作。
  
  创建持有格式等定义的类
    添加 :java:extdoc:`DateTimeConfiguration <nablarch.integration.jsr310.util.DateTimeConfiguration>` 的实现类，
    定义日期和日期时间的格式。
    可参考基本实现的 :java:extdoc:`BasicDateTimeConfiguration <nablarch.integration.jsr310.util.BasicDateTimeConfiguration>`
    
  在组件配置文件中定义添加的类
    将组件名设为 ``dateTimeConfiguration`` ，定义组件。
    
    以下显示示例。
    
    .. code-block:: xml
    
      <component name="dateTimeConfiguration" class="sample.SampleDateTimeConfiguration" />
