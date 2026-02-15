.. _`format`:

格式化器
==================================================

.. contents:: 目录
  :depth: 3
  :local:

功能概述
---------------------------------------------------------------------

提供将日期、数值等数据格式化为字符串类型转换的功能。
通过将格式化设置集中到本功能中，无需为画面、文件、邮件等不同格式分别进行设置。


模块列表
---------------------------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core</artifactId>
  </dependency>

使用方法
---------------------------------------------------------------------

格式化器的设置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
本功能即使不进行特别设置，也可以使用框架默认支持的格式化器。

如需更改默认的格式模式或添加格式化器，
请参考 :ref:`format_custom` 在系统仓库中添加设置。

使用格式化器
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

进行格式化时使用
:java:extdoc:`FormatterUtil <nablarch.core.text.FormatterUtil>`
。

格式化器除了类名外，还具有用于识别格式化器的格式化器名称。

调用FormatterUtil.format时，需指定格式化器名称、格式化目标和格式化模式，
根据格式化名称和格式化目标的数据类型选择适当的格式化器。

使用选定的格式化器和指定的格式化模式进行格式化。
如未明确指定格式化模式，则使用各格式化器设置的默认模式。

实现示例

.. code-block:: java

  // 使用默认模式进行格式化时
  // 第1参数指定要使用的格式化器名称
  // 第2参数指定要格式化的值
  FormatterUtil.format("dateTime", input);

  // 指定模式进行格式化时
  // 第1、第2参数与默认模式时相同
  // 第3参数指定要使用的格式化模式。
  FormatterUtil.format("dateTime", input, "yyyy年MM月dd日");

以下展示本功能默认提供的格式化器。

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 20,40,40,40

  * - 格式化器名称
    - 格式化数据的类型
    - 默认的格式化模式
    - 备注

  * - :ref:`dateTime <format_datetime>`
    - :java:extdoc:`Date <java.util.Date>`
    - yyyy/MM/dd
    -

  * - :ref:`dateTime <format_datetime>`
    - :java:extdoc:`String <java.lang.String>`
    - yyyy/MM/dd
    - 需要格式化目标日期字符串的模式（默认为 ``yyyyMMdd`` ）

  * - :ref:`number <format_number>`
    - :java:extdoc:`Number <java.lang.Number>`
    - #,###.###
    -

  * - :ref:`number <format_number>`
    - :java:extdoc:`String <java.lang.String>`
    - #,###.###
    -

.. _`format_dateTime`:

dateTime
  格式化日期的格式化器。

  格式化目标的类型为 :java:extdoc:`Date <java.util.Date>` 及其派生类和 :java:extdoc:`String <java.lang.String>` 。
  模式中指定
  :java:extdoc:`SimpleDateFormat <java.text.SimpleDateFormat>`
  规定的语法。
  默认模式为 ``yyyy/MM/dd`` 。

  格式化 :java:extdoc:`String <java.lang.String>` 类型时，还需设置作为格式化目标的日期字符串的模式。
  默认情况下，作为格式化目标的日期字符串的模式为 ``yyyyMMdd`` 。
  如需更改设置，请参考 :ref:`format_custom` 。

.. _`format_number`:

number
  格式化数值的格式化器。

  格式化目标的类型为 :java:extdoc:`Number <java.lang.Number>` 的派生类和 :java:extdoc:`String <java.lang.String>` 。
  模式中指定
  :java:extdoc:`DecimalFormat <java.text.DecimalFormat>`
  规定的语法。
  默认模式为 ``#,###.###`` 。

使用示例
  例如，使用数据绑定向文件输出时使用本功能，
  可以在Bean的getter中使用。

  .. code-block:: java

    import java.util.Date;

    public class SampleDto {
        private Date startDate;
        private Integer sales;

        // 创建获取格式化后字符串的getter
        public String getFormattedStartDate() {
            return FormatterUtil.format("dateTime", startDate);
        }

        public String getFormattedSales() {
            return FormatterUtil.format("number", sales, "#,### 円");
        }

        // 其他 getter & setter 省略
    }


.. _`format_custom`:

更改格式化器的设置
---------------------------------------------------------------------

更改格式化器的设置需要以下步骤。

在组件配置文件中设置 ``nablarch.core.text.FormatterConfig`` 。

  要点
   * 组件名称需为 ``formatterConfig`` 。

  在 ``nablarch.core.text.FormatterConfig`` 中设置要使用的格式化器列表。
  列表的属性名需为 ``formatters`` 。


  以下展示框架默认支持的格式化器的初始设置。

  .. code-block:: xml

    <component name="formatterConfig" class="nablarch.core.text.FormatterConfig">
      <!-- 保存格式化器的列表 -->
      <property name="formatters">
        <list>
          <component class="nablarch.core.text.DateTimeFormatter">
            <!-- 调用格式化器时使用的名称 -->
            <property name="formatterName" value="dateTime" />
            <!-- 默认格式化模式的设置 -->
            <property name="defaultPattern" value="yyyy/MM/dd" />
          </component>
          <component class="nablarch.core.text.DateTimeStrFormatter">
            <property name="formatterName" value="dateTime" />
            <property name="defaultPattern" value="yyyy/MM/dd" />
            <!-- 日期字符串的格式化器还需设置表示日期字符串模式的属性 -->
            <property name="dateStrPattern" value="yyyyMMdd" />
          </component>
          <component class="nablarch.core.text.NumberFormatter">
            <property name="formatterName" value="number" />
            <property name="defaultPattern" value="#,###.###" />
          </component>
          <component class="nablarch.core.text.NumberStrFormatter">
            <property name="formatterName" value="number" />
            <property name="defaultPattern" value="#,###.###" />
          </component>
        </list>
      </property>
    </component>

  .. important::
    在组件定义中更改默认格式化器的设置时，
    对于不更改的格式化器和属性也必须记述设置。
    组件定义中未记述的格式化器将无法使用。


添加格式化器
---------------------------------------------------------------------

添加格式化器时需要以下步骤。

1. 创建实现 :java:extdoc:`Formatter <nablarch.core.text.Formatter>` 的实现类。

  格式化处理由实现 :java:extdoc:`Formatter <nablarch.core.text.Formatter>` 的类执行。


2. 在组件配置文件中添加创建的格式化器设置

  参考 :ref:`format_custom` ，在组件配置文件中设置 ``nablarch.core.text.FormatterConfig`` 和格式化器列表。

  .. code-block:: xml

    <component name="formatterConfig" class="nablarch.core.text.FormatterConfig">
      <property name="formatters">
        <list>
          <!-- 默认的格式化器 -->
          <component class="nablarch.core.text.DateTimeFormatter">
            <property name="formatterName" value="dateTime" />
            <property name="defaultPattern" value="yyyy/MM/dd" />
          </component>
          <component class="nablarch.core.text.DateTimeStrFormatter">
            <property name="formatterName" value="dateTime" />
            <property name="defaultPattern" value="yyyy/MM/dd" />
            <property name="dateStrPattern" value="yyyyMMdd" />
          </component>
          <component class="nablarch.core.text.NumberFormatter">
            <property name="formatterName" value="number" />
            <property name="defaultPattern" value="#,###.###" />
          </component>
          <component class="nablarch.core.text.NumberStrFormatter">
            <property name="formatterName" value="number" />
            <property name="defaultPattern" value="#,###.###" />
          </component>
          <!-- 添加的格式化器 -->
          <component class="sample.SampleFormatter">
            <property name="formatterName" value="sample" />
            <property name="defaultPattern" value="#,### 円" />
          </component>
        </list>
      </property>
    </component>
