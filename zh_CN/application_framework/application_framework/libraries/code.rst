.. _code:

代码管理
==================================================

.. contents:: 目录
  :depth: 3
  :local:

提供管理应用中使用的值与名称映射关系的功能。

例如，管理以下性别区分与显示名称的映射信息。

=======   ======== =============
值        名称     简称
=======   ======== =============
male      男性     男
female    女性     女
=======   ======== =============


.. important::

  本功能管理的是静态代码信息(值与名称的映射)，
  "商品代码"或"企业代码"等值关联信息动态变化的对象不在管理范围内。
  此类信息请在应用中创建主数据表来应对。


.. important::

  使用本功能后，无法对持有代码名称的表和持有代码值的表设置RDBMS的参照完整性约束。
  此类约束检查请使用 :ref:`code-validation` 。


.. tip::

  静态代码信息使用enum表达更好，原因如下。

  * 如果只是想做值与名称的简单映射，使用数据库进行代码定义过于庞大，维护成本高。
  * 使用数据库进行代码定义时，为了在Java上处理代码值，往往需要定义数值型常量，导致双重维护。

  但是，Nablarch不具备将enum值与数据库值相互转换的功能，无法将enum值注册到数据库。

  使用Doma可以将enum值注册到数据库。
  使用Doma时，请参考 :ref:`doma_adaptor` 进行设置。


功能概述
--------------------------------------------------
支持国际化
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
本功能可以按语言管理名称。

详细请参考 :ref:`code-use_multilingualization` 。

.. _code-table:

代码信息通过表管理
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
本功能在数据库上管理值及名称信息。
因此，需要事先在数据库中创建表，并在表上注册静态代码信息。

详细请参考 :ref:`code-setup_table` 。

模块列表
---------------------------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-code</artifactId>
  </dependency>
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-code-jdbc</artifactId>
  </dependency>

使用方法
--------------------------------------------------

.. _code-setup_table:

使用代码管理功能的初始设置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
要使用本功能，需要创建用于管理代码的表，并在配置文件中设置相关信息。

以下显示表结构及设置示例。

表结构
  代码信息使用 ``代码模式表`` 和 ``代码名称表`` 两个表。
  两个表的关系如下。

  .. image:: images/code/code_table.png

  |
  |

  各列的用途等如下。

  :ID:            唯一识别代码信息的ID

                  性别区分或地址区分等每种设置唯一的ID。

  :VALUE:         识别代码信息内名称的值

                  如果是性别区分，则为 ``male`` 或 ``female`` 等值。

  :PATTERN:       表示是否使用该值的标志(设置为 ``0`` 或 ``1`` )

                  用于切换有效值。不需要时可以省略。

                  详细请参考 :ref:`code-use_pattern` 。

  :LANG:          语言

                  支持多语言化时，存储支持语言的 *Local#getLanguage()* 。

                  仅支持日语时，设置为 ``ja`` 。

  :SORT_ORDER:    排序顺序

                  获取关联ID的一览信息时，结果将按此列设置值升序返回。

                  详细请参考 :ref:`code-use_sort_order` 。

  :NAME:          名称
  
                  设置与VALUE对应的名称。

  :SHORT_NAME:    简称

                  设置与VALUE对应的简称。

  :OPTIONAL_NAME: 选项名称

                  当名称和简称无法管理足够的显示文本值时使用。
                  可以定义需要的列名和列数。

                  详细请参考 :ref:`code-option_name` 。
                

配置文件示例
  以下显示使用代码管理的配置文件示例。

  要点
    * :java:extdoc:`BasicCodeManager <nablarch.common.code.BasicCodeManager>` 的组件名设为 **codeManager** 。
    * :java:extdoc:`BasicStaticDataCache <nablarch.core.cache.BasicStaticDataCache>` 的 :java:extdoc:`loadOnStartup <nablarch.core.cache.BasicStaticDataCache.setLoadOnStartup(boolean)>` 设置值，请参考 :ref:`static_data_cache-cache_timing` 。
    * :java:extdoc:`BasicCodeLoader <nablarch.common.code.BasicCodeLoader>` 及 :java:extdoc:`BasicStaticDataCache <nablarch.core.cache.BasicStaticDataCache>` 需要初始化，因此请设置到初始化对象列表中。

  .. code-block:: xml

    <component name="codeLoader" class="nablarch.common.code.BasicCodeLoader">

      <!-- 代码模式表的schema信息 -->
      <property name="codePatternSchema">
        <component class="nablarch.common.code.schema.CodePatternSchema">
          <!-- 设置CodePatternSchema的表名及列名属性 -->
        </component>
      </property>

      <!-- 代码名称表的schema信息 -->
      <property name="codeNameSchema">
        <component class="nablarch.common.code.schema.CodeNameSchema">
          <!-- 设置CodeNameSchema的表名及列名属性 -->
        </component>
      </property>
    </component>

    <!-- 缓存从数据库获取的信息的设置 -->
    <component name="codeCache" class="nablarch.core.cache.BasicStaticDataCache" >
      <property name="loader" ref="codeLoader"/>
      <property name="loadOnStartup" value="false"/>
    </component>

    <!-- 将缓存从数据库获取的信息的类设置到BasicCodeManager -->
    <component name="codeManager" class="nablarch.common.code.BasicCodeManager" >
      <property name="codeDefinitionCache" ref="codeCache"/>
    </component>

    <!-- BasicCodeLoader和BasicStaticDataCache需要初始化，因此设置到初始化列表 -->
    <component name="initializer"
        class="nablarch.core.repository.initialization.BasicApplicationInitializer">
      <property name="initializeList">
        <list>
          <component-ref name="codeLoader"/>
          <component-ref name="codeCache"/>
        </list>
      </property>
    </component>
    

.. _code-use_pattern:

按功能切换使用的代码信息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
在列表显示代码信息时，有时希望按功能切换显示/隐藏。
这种情况下，使用代码模式表的pattern，按功能切换显示哪个pattern的信息。


以下显示示例。

在代码模式表定义pattern列
  在代码模式表中定义持有显示pattern的pattern列。

  pattern列通过设置在 :java:extdoc:`CodePatternSchema.patternColumnNames <nablarch.common.code.schema.CodePatternSchema.setPatternColumnNames(java.lang.String[])>` 中使用。
  设置到配置文件的方法请参考 :ref:`code-setup_table` 。


  本例中，定义了 ``PATTERN1`` 和 ``PATTERN2`` 两个pattern，
  ``PATTERN2`` 中不显示OTHER。

  代码模式表
    ======= =========   ========  ===========
    ID      VALUE       PATTERN1  PATTERN2
    ======= =========   ========  ===========
    GENDER  MALE        1         1
    GENDER  FEMALE      1         1
    GENDER  OTHER       1         0
    ======= =========   ========  ===========

  代码名称表
    ======= ========= ====  ==========  ==========  ===========
    ID      VALUE     LANG  SORT_ORDER  NAME        SHORT_NAME
    ======= ========= ====  ==========  ==========  ===========
    GENDER  MALE      ja    1           男性        男
    GENDER  FEMALE    ja    2           女性        女
    GENDER  OTHER     ja    3           其他        他
    ======= ========= ====  ==========  ==========  ===========

指定pattern获取代码信息
  代码信息使用 :java:extdoc:`CodeUtil <nablarch.common.code.CodeUtil>` 获取。

  使用pattern时，以字符串指定使用哪个pattern。
  此值需要与 :ref:`code-setup_table` 中配置文件设置的列名严格一致。

  .. code-block:: java


    // 获取PATTER1的列表
    // 可获取[MALE, FEMALE, OTHER]
    List<String> pattern1 = CodeUtil.getValues("GENDER", "PATTERN1");

    // 获取PATTER2的列表
    // 可获取[MALE, FEMALE]
    List<String> pattern2 = CodeUtil.getValues("GENDER", "PATTERN2");

在画面(JSP)指定pattern获取代码信息
  使用获取代码信息的自定义标签库时，通过指定pattern可以只显示该pattern的信息。

  自定义标签库的详细使用方法请参考以下内容。

  * :ref:`tag-code_input_output`

  指定PATTERN2时，在 `pattern` 属性中如下指定。

  .. code-block:: jsp

    <n:codeSelect name="form.gender" codeId="GENDER" pattern="PATTERN2" cssClass="form-control" />

  将输出PATTERN2中作为对象的 ``男性`` 和 ``女性`` 。
  
  .. image:: images/code/code_pattern.png


.. _code-use_multilingualization:

名称的多语言化支持
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
要进行名称的多语言化支持，需要在代码名称表中准备支持语言的各数据。

以下显示示例。

代码名称表的数据
  本例中，支持 ``ja`` 和 ``en`` 两种语言。

  ======= ========= ====  ==========  ==========  ===========
  ID      VALUE     LANG  SORT_ORDER  NAME        SHORT_NAME
  ======= ========= ====  ==========  ==========  ===========
  GENDER  MALE      ja    1           男性        男
  GENDER  FEMALE    ja    2           女性        女
  GENDER  OTHER     ja    3           其他        他
  GENDER  MALE      en    1           Male        M
  GENDER  FEMALE    en    2           Female      F
  GENDER  OTHER     en    3           Unknown     \-
  ======= ========= ====  ==========  ==========  ===========

指定语言获取代码信息
  使用 :java:extdoc:`CodeUtil <nablarch.common.code.CodeUtil>` 可以获取对应语言的名称。

  .. code-block:: java

    // 名称
    CodeUtil.getName("GENDER", "MALE", Locale.JAPANESE);    // -> 男性
    CodeUtil.getName("GENDER", "MALE", Locale.ENGLISH);     // -> Male

    // 简称
    CodeUtil.getShortName("GENDER", "MALE", Locale.JAPANESE) // -> 男
    CodeUtil.getShortName("GENDER", "MALE", Locale.ENGLISH) // -> M

.. important::

  JSP提供的自定义标签库中，注意不能通过指定语言来获取值。
  自定义标签库使用的语言信息详细请参考 :ref:`tag-code_input_output` 。

.. _code-use_sort_order:

定义画面等显示名称的排序顺序
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
可以定义在画面列表框或复选框中显示代码信息时的排序顺序。
排序顺序可能因国家而异，因此可以按语言设置。


以下显示示例。

在代码名称表的SORT_ORDER设置排序顺序
  排序顺序设置在代码名称表的SORT_ORDER列中。

  本例中，将按 ``MALE`` -> ``FEMALE`` -> ``OTHER`` 的顺序显示。

  ======= ========= ====  ==========  ==========  ===========
  ID      VALUE     LANG  SORT_ORDER  NAME        SHORT_NAME
  ======= ========= ====  ==========  ==========  ===========
  GENDER  MALE      ja    1           男性        男
  GENDER  FEMALE    ja    2           女性        女
  GENDER  OTHER     ja    3           其他        他
  ======= ========= ====  ==========  ==========  ===========

画面显示示例
  使用自定义标签库的 `codeSelect` 时，
  将按  ``MALE(男性)`` -> ``FEMALE(女性)`` -> ``OTHER(其他)`` 的顺序显示。

  .. image:: images/code/code_sort.png

.. _code-option_name:

定义名称、简称以外的名称
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
默认动作中可以使用名称和简称两种名称。

根据需求，有时希望定义这些以外的显示名称。
这种情况下，使用选项名称区域来应对。

以下显示示例。
 
在代码名称表定义选项名称列
  在代码名称表中定义持有选项名称的列。

  pattern列通过设置在 :java:extdoc:`CodePatternSchema.patternColumnNames <nablarch.common.code.schema.CodePatternSchema.setPatternColumnNames(java.lang.String[])>` 中使用。
  设置到配置文件的方法请参考 :ref:`code-setup_table` 。

  本例中，作为选项名称的列，定义了 ``FORM_NAME`` 和 ``KANA_NAME`` 两个。

  ======= ========= ====  ==========  ==========  =========== =========== ===========
  ID      VALUE     LANG  SORT_ORDER  NAME        SHORT_NAME  FORM_NAME   KANA_NAME
  ======= ========= ====  ==========  ==========  =========== =========== ===========
  GENDER  MALE      ja    1           男性        男          Male        男性(拼音)
  GENDER  FEMALE    ja    2           女性        女          Female      女性(拼音)
  GENDER  OTHER     ja    3           其他        他          Other       其他(拼音)
  ======= ========= ====  ==========  ==========  =========== =========== ===========


获取选项名称
  选项名称使用 :java:extdoc:`CodeUtil <nablarch.common.code.CodeUtil>` 获取。

  获取选项名称时，以字符串指定获取哪个选项名称。
  此值需要与 :ref:`code-setup_table` 中配置文件设置的列名严格一致。

  .. code-block:: java

    CodeUtil.getOptionalName("GENDER", "MALE", "KANA_NAME") // -> 男性(拼音)
    CodeUtil.getOptionalName("GENDER", "FEMALE", "FORM_NAME", Locale.JAPANESE) // -> Female

在画面(JSP)显示可选名称
  使用自定义标签库时，通过指定可选名称可以显示该名称。

  自定义标签库的详细使用方法请参考以下内容。

  * code_select
  * code

  显示KANA_NAME的名称时，如下指定 `optionColumnName` ，在 `labelPattern` 中指定 **$OPTIONALNAME$** 。

  .. code-block:: jsp

    <n:codeSelect name="form.gender" codeId="GENDER" optionColumnName="KANA_NAME" cssClass="form-control" labelPattern="$OPTIONALNAME$"/>

  将显示选项名称KANA_NAME的值。
  
  .. image:: images/code/code_option_name.png

.. _code-validation:

检查输入值是否为有效代码值
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
提供可以检查输入值(画面时为客户端发送的请求参数)是否在代码有效范围内的功能。
使用本功能可以通过仅设置注解来进行输入值检查。

以下显示示例。

:ref:`bean_validation`
  使用 :ref:`bean_validation` 时，使用 :java:extdoc:`nablarch.common.code.validator.ee.CodeValue` 注解。

  .. code-block:: java

    @CodeValue(codeId = "GENDER")
    private String gender;

:ref:`nablarch_validation`
  使用 :ref:`nablarch_validation` 时，使用 :java:extdoc:`nablarch.common.code.validator.CodeValue` 注解。

  .. code-block:: java

    @CodeValue(codeId = "GENDER")
    public void setGender(String gender) {
      this.gender = gender;
    }

在输入画面等中，使用 :ref:`pattern <code-use_pattern>` 限制可选值时，
验证时也需要检查是否在该pattern内的有效值。

通过在验证用注解的 `pattern` 属性中指定pattern名，
可以检查是否该pattern中的有效值。

以下显示示例。

.. code-block:: java

  @CodeValue(codeId = "GENDER", pattern = "PATTERN2")
  private String gender;

.. tip::

  使用 :ref:`领域验证 <bean_validation-domain_validation>` 时，1个领域只能指定1个pattern。
  因此，要对应多个pattern，需要定义对应pattern的领域。

  但是，无需定义对应所有pattern的领域，只需定义验证所需的领域即可。

  以下显示示例。

  .. code-block:: java

    public class SampleDomainBean {

      // PATTERN1用领域
      @CodeValue(codeId = "FLOW_STATUS", pattern = "PATTERN1")
      String flowStatusGeneral;

      // PATTERN2用领域
      @CodeValue(codeId = "FLOW_STATUS", pattern = "PATTERN2")
      String flowStatusGuest;

    }



