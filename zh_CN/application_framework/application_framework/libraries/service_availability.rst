.. _`service_availability`:

服务可用性检查
=====================================================================

.. contents:: 目录
  :depth: 3
  :local:

本功能检查应用程序提供的功能的服务可用性。

使用本功能可以实现以下功能。

* 在Web中屏蔽部分功能的访问，返回503错误。
* 在常驻Batch中，进行空转（不处理而等待的状态）。

.. important::
 本功能仅在应用程序需求匹配时使用。
 本功能使用数据库管理服务可用性状态，
 按请求单位设置服务可用性（参见 :ref:`service_availability-settings` ）。
 例如，Web的注册功能一般由初始显示/确认/返回/注册等多个请求构成。
 因此，本功能虽然可以细粒度设置服务可用性，但需要非常细致的数据设计，
 可能导致开发生产力下降或发布后运维负荷增加。

功能概述
---------------------------------------------------------------------

可以按请求单位检查服务可用性
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:ref:`ServiceAvailabilityCheckHandler` 设置到handler队列后，
Web和常驻Batch都可以按请求单位检查服务可用性。
此功能不依赖于Web或常驻Batch等处理方式。

详细参见以下。

* :ref:`service_availability-settings`
* :ref:`service_availability-check`
* :ref:`service_availability-view_control`

模块列表
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-auth</artifactId>
  </dependency>
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-auth-jdbc</artifactId>
  </dependency>

使用方法
---------------------------------------------------------------------

.. _`service_availability-settings`:

使用服务可用性检查的设置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
本功能使用数据库管理服务可用性状态。
表的结构如下。

====================== ===================================================
请求ID(PK)             用于识别请求的值。字符串型
服务可用性状态         可用时为"1"。字符串型。可在设置中更改值。
====================== ===================================================

使用服务可用性检查，
需要将 :java:extdoc:`BasicServiceAvailability <nablarch.common.availability.BasicServiceAvailability>` 的定义添加到组件设置文件中。
组件名指定为 **serviceAvailability** 。

另外由于需要初始化，因此设置到初始化目标列表中。

.. code-block:: xml

 <component name="serviceAvailability" class="nablarch.common.availability.BasicServiceAvailability">
   <!-- 表名 -->
   <property name="tableName" value="REQUEST"/>
   <!-- 请求ID的列名 -->
   <property name="requestTableRequestIdColumnName" value="REQUEST_ID"/>
   <!-- 服务可用性状态的列名 -->
   <property name="requestTableServiceAvailableColumnName" value="SERVICE_AVAILABLE"/>
   <!-- 表示服务可用的值 -->
   <property name="requestTableServiceAvailableOkStatus" value="1"/>
   <!-- 数据库访问使用的事务管理器 -->
   <property name="dbManager" ref="serviceAvailabilityDbManager"/>
 </component>

 <component name="initializer"
     class="nablarch.core.repository.initialization.BasicApplicationInitializer">
   <property name="initializeList">
     <list>
       <!-- 其他组件省略 -->
       <component-ref name="serviceAvailability" />
     </list>
   </property>
 </component>

.. _`service_availability-check`:

检查服务可用性
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
服务可用性检查使用 :java:extdoc:`ServiceAvailabilityUtil <nablarch.common.availability.ServiceAvailabilityUtil>` 。

.. _`service_availability-view_control`:

根据服务可用性控制画面显示
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
要根据服务可用性控制按钮或链接的隐藏（非激活），使用自定义标签。
参见 :ref:`tag-submit_display_control` 。

扩展示例
---------------------------------------------------------------------
无。
