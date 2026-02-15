日期管理
=====================================================================

.. contents:: 目录
  :depth: 3
  :local:

提供统一管理系统日期时间（OS日期时间）和业务日期的功能。

功能概述
--------------------------

可以切换系统日期时间（OS日期时间）和业务日期
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
该功能使用组件定义中指定的类来获取系统日期时间（OS日期时间）和业务日期。
因此，只需替换组件定义中指定的类，
就可以切换应用程序中使用的系统日期时间（OS日期时间）和业务日期的获取方式。
这种切换可用于在测试等情况下临时切换系统日期时间（OS日期时间）和业务日期。

* :ref:`date-system_time_change`
* :ref:`date-business_date_change`

模块列表
---------------------------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core</artifactId>
  </dependency>

  <!-- 仅在使用业务日期管理功能时 -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-jdbc</artifactId>
  </dependency>

使用方法
--------------------------------------------------

.. _date-system_time_settings:

使用系统日期时间管理功能的配置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
要使用系统日期时间管理功能，
需要将 :java:extdoc:`BasicSystemTimeProvider <nablarch.core.date.BasicSystemTimeProvider>` 的配置添加到组件定义中。
组件名称需指定为 **systemTimeProvider** 。

.. code-block:: xml

 <component name="systemTimeProvider" class="nablarch.core.date.BasicSystemTimeProvider" />

获取系统日期时间
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
获取系统日期时间使用 :java:extdoc:`SystemTimeUtil <nablarch.core.date.SystemTimeUtil>` 。

.. _date-business_date_settings:

使用业务日期管理功能的配置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
业务日期管理功能使用数据库来管理多个业务日期。
表的结构如下。

================ ===================================================
区分(PK)         用于识别业务日期的值。字符串类型
日期             业务日期。字符串类型，格式为yyyyMMdd
================ ===================================================

要使用业务日期管理功能，
需要将 :java:extdoc:`BasicBusinessDateProvider <nablarch.core.date.BasicBusinessDateProvider>` 的配置添加到组件定义中。
组件名称需指定为 **businessDateProvider** 。

此外，由于需要初始化，请将其设置到初始化目标列表中。

.. code-block:: xml

 <component name="businessDateProvider" class="nablarch.core.date.BasicBusinessDateProvider">
   <!-- 表名 -->
   <property name="tableName" value="BUSINESS_DATE" />
   <!-- 区分的列名 -->
   <property name="segmentColumnName" value="SEGMENT"/>
   <!-- 日期的列名 -->
   <property name="dateColumnName" value="BIZ_DATE"/>
   <!-- 省略区分获取业务日期时使用的区分 -->
   <property name="defaultSegment" value="00"/>
   <!-- 数据库访问使用的transaction manager -->
   <property name="transactionManager" ref="transactionManager" />
 </component>

 <component name="initializer"
     class="nablarch.core.repository.initialization.BasicApplicationInitializer">
   <property name="initializeList">
     <list>
       <!-- 其他组件省略 -->
       <component-ref name="businessDateProvider" />
     </list>
   </property>
 </component>

获取业务日期
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
获取业务日期使用 :java:extdoc:`BusinessDateUtil <nablarch.core.date.BusinessDateUtil>` 。

将业务日期覆盖为任意日期
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
在批处理故障重新执行时，可能希望将过去日期作为批处理执行时的业务日期。
在这种情况下，可以仅对重新执行的进程将任意日期作为业务日期执行。

.. tip::
 对于像Web应用这样所有功能都在一个进程内执行的情况，
 只需简单地更改数据库中管理的日期即可。

业务日期的覆盖使用 :ref:`repository-overwrite_environment_configuration` 进行。
作为系统属性，按以下格式指定。

系统属性的格式
 BasicBusinessDateProvider.<区分>=日期

 ※日期格式为yyyyMMdd

系统属性的示例
 希望将区分"batch"的日期覆盖为"2016/03/17"时

 -DBasicBusinessDateProvider.batch=20160317

更新业务日期
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
业务日期的更新使用 :java:extdoc:`BasicBusinessDateProvider <nablarch.core.date.BasicBusinessDateProvider>` 进行。

.. code-block:: java

 // 从系统仓库获取BasicBusinessDateProvider
 BusinessDateProvider provider = SystemRepository.get("businessDateProvider");

 // 调用setDate方法进行更新
 provider.setDate(segment, date);

扩展示例
--------------------------------------------------

.. _date-system_time_change:

切换系统日期时间
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
在执行单元测试等需要切换系统日期时间时，按以下步骤进行。

1. 创建实现 :java:extdoc:`SystemTimeProvider <nablarch.core.date.SystemTimeProvider>` 的类。
2. 按照 :ref:`date-system_time_settings` 进行配置。

.. _date-business_date_change:

切换业务日期
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
在执行单元测试等需要切换业务日期时，按以下步骤进行。

1. 创建实现 :java:extdoc:`BusinessDateProvider <nablarch.core.date.BusinessDateProvider>` 的类。
2. 按照 :ref:`date-business_date_settings` 进行配置。
