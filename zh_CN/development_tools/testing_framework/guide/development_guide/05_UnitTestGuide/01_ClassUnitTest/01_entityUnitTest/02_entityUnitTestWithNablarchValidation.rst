.. _entityUnitTest:

==========================================================
对应Nablarch Validation的Form/Entity的类单元测试
==========================================================
本项说明输入值检查使用 :ref:`nablarch_validation` 实施的Form及Entity类单元测试(以下称为Form单元测试或Entity单元测试)。
两者几乎可以同样地进行单元测试，因此共通内容以Entity单元测试为基础说明，特有处理单独说明。

.. tip::
   Form、Entity的职责，请参照各处理方式的职责配置。
   例： :ref:`Web应用的职责配置<application_design>` 、 :ref:`Nablarch批处理应用的职责配置<nablarch_batch-application_design>` 

-----------------------------
Form/Entity单元测试的写法
-----------------------------
本项示例使用的测试类和测试数据如下(右键->保存下载)。

* :download:`测试类(SystemAccountEntityTest.java)<../_download/SystemAccountEntityTest.java>`
* :download:`测试数据(SystemAccountEntityTest.xlsx)<../_download/SystemAccountEntityTest.xlsx>`
* :download:`测试目标类(SystemAccountEntity.java)<../_download/SystemAccountEntity.java>`  

测试数据的创建
==================
说明记载测试数据的Excel文件本身的创建方法。记载测试数据的Excel文件与测试源代码放在同一目录下同名存储(仅扩展名不同)。\
此外，后述的\
\ :ref:`校验的测试用例<entityUnitTest_ValidationCase>`\ 、\
\ :ref:`构造函数的测试用例<entityUnitTest_ConstructorCase>`\ 、\
\ :ref:`setter、getter的测试用例<entityUnitTest_SetterGetterCase>`\ 
各自使用1个工作表为前提。

测试数据描述方法的详情请参考\ :doc:`../../../06_TestFWGuide/01_Abstract`\ 、\ :doc:`../../../06_TestFWGuide/02_DbAccessTest`\ 。

此外，消息数据和代码主数据等存储在数据库中的静态主数据，以项目中管理的数据已预先投入
(不将这些数据作为个别测试数据创建)为前提。

测试类的创建
==================
Form/Entity单元测试的测试类按以下条件创建。

* 测试类的包与测试目标的Form/Entity相同。
* 以Form/Entity类名Test的类名创建测试类。
* 继承nablarch.test.core.db.EntityTestSupport。

.. code-block:: java

   package nablarch.sample.management.user; // 【说明】包与SystemAccountEntity相同

   import java.util.HashMap;
   import java.util.Map;

   import org.junit.Test;

   import nablarch.test.core.db.EntityTestSupport;

   import static org.junit.Assert.assertArrayEquals;
   import static org.junit.Assert.assertEquals;

   /**
    * 执行SystemAccountEntity类测试的类。<br/>
    * 测试内容请参照Excel工作表。
    *
    * @author Miki Habu
    * @since 1.0
    */
   public class SystemAccountEntityTest extends EntityTestSupport {
   // 【说明】类名为SystemAccountEntityTest，继承EntityTestSupport
   

   // ～后略～
   
测试方法的描述方法请参考本项以后记载的代码示例。

.. _entityUnitTest_ValidationCase:

字符类型和字符串长的单项目校验测试用例
========================================

单项目校验相关的测试用例大多是关于输入的字符类型以及字符串长的。\
例如，假设有以下属性。

* 属性名「片假名」
* 最大字符串长为50字符
* 必填项
* 仅允许全角片假名

这种情况下，需要创建如下测试用例。

 =============================================== =========================
 用例                                           观点             
 =============================================== =========================
 输入全角片假名50字符，校验成功。               最大字符串长、字符类型的确认   
 输入全角片假名51字符，校验失败。               最大字符串长的确认         
 输入全角片假名1字符，校验成功。                最小字符串长、字符类型的确认  
 输入空字符，校验失败。                         必填校验的确认           
 输入半角片假名，校验失败。                     字符类型的确认\ [#]_\        
 =============================================== =========================

\ 
 
 .. [#] 同样，需要半角英文字母、全角平假名、汉字...等被输入时校验失败的用例。

像这样，单项目校验的测试用例，用例数量会变多，数据创建比较费力。\
因此，提供单项目校验测试专用的测试方法。由此可期待以下效果。

* 单项目校验的测试用例创建变得容易。
* 可以创建可维护性高的测试数据，便于校验和维护。


.. tip::
   本测试方法对属性中持有其他Form的Form不能使用。这种情况下，请自行实现校验处理的测试。
   属性中持有其他Form的Form是指，通过以下形式访问属性的父Form。
   
   .. code-block:: none
   
      <父Form>.<子Form>.<子Form的属性名>


测试用例表的创建方法
------------------------

准备以下列。

+--------------------------------+--------------------------------------------------------+
| 列名                           | 记载内容                                               |
+================================+========================================================+
|propertyName                    |测试目标的属性名                                        |
+--------------------------------+--------------------------------------------------------+
|allowEmpty                      |该属性是否允许未输入                                    |
+--------------------------------+--------------------------------------------------------+
|         min                    |该属性作为输入值允许的最小字符串长度（可选）             |                                          |
+--------------------------------+--------------------------------------------------------+
|         max                    |该属性作为输入值允许的最大字符串长                      |
+--------------------------------+--------------------------------------------------------+
|messageIdWhenEmptyInput         |未输入时期待的消息ID(可省略) \ [#]_\                    |
+--------------------------------+--------------------------------------------------------+
|messageIdWhenInvalidLength      |字符串长不适当时期待的消息ID(可省略)\ [#]_\             |
+--------------------------------+--------------------------------------------------------+
|messageIdWhenNotApplicable      |字符类型不适当时期待的消息ID                            |
+--------------------------------+--------------------------------------------------------+
|半角英字                        |是否允许半角英文字母                                    |
+--------------------------------+--------------------------------------------------------+
|半角数字                        |是否允许半角数字                                        |
+--------------------------------+--------------------------------------------------------+
|半角記号                        |是否允许半角符号                                        |
+--------------------------------+--------------------------------------------------------+
|半角カナ                        |是否允许半角片假名                                      |
+--------------------------------+--------------------------------------------------------+
|全角英字                        |是否允许全角英文字母                                    |
+--------------------------------+--------------------------------------------------------+
|全角数字                        |是否允许全角数字                                        |
+--------------------------------+--------------------------------------------------------+
|全角ひらがな                    |是否允许全角平假名                                      |
+--------------------------------+--------------------------------------------------------+
|全角カタカナ                    |是否允许全角片假名                                      |
+--------------------------------+--------------------------------------------------------+
|全角漢字                        |是否允许全角汉字                                        |
+--------------------------------+--------------------------------------------------------+
|全角記号その他                  |是否允许全角符号及其他                                  |
+--------------------------------+--------------------------------------------------------+
|外字                            |是否允许外字                                            |
+--------------------------------+--------------------------------------------------------+


.. [#] messageIdWhenEmptyInput省略时，使用 :ref:`entityUnitTest_EntityTestConfiguration` 中设置的emptyInputMessageId
       的值。

\

.. [#] messageIdWhenInvalidLength省略时，使用 :ref:`entityUnitTest_EntityTestConfiguration` 中
       设置的默认值。省略时使用哪个默认值由max栏及min栏的记载决定，如下所示。

+--------------+----------------+---------------------------------------------------------------+
| min栏的记载  | max与min的比较 | 省略时使用的默认值                                            |
+==============+================+===============================================================+
| 无           | (不适用)       | maxMessageId                                                  |
+--------------+----------------+---------------------------------------------------------------+
| 有           | max > min      | maxAndMinMessageId(超过时)、underLimitMessageId(不足时)       |
+--------------+----------------+---------------------------------------------------------------+
| 有           | max = min      | fixLengthMessageId                                            |
+--------------+----------------+---------------------------------------------------------------+


是否允许的列中，设置以下值。

========== ======= ========================
设置内容    设置值    备注
========== ======= ========================
允许        o      半角英文小写字母o
不允许      x      半角英文小写字母x
========== ======= ========================


具体示例如下。

.. image:: ../_image/entityUnitTest_CharsetAndLengthExample.png
   :scale: 100



测试方法的创建方法
------------------------

 
启动超类的以下方法。

.. code-block:: java

   void testValidateCharsetAndLength(Class entityClass, String sheetName, String id)


\ 

.. code-block:: java

   // 【说明】～前略～

  public class SystemAccountEntityTest extends EntityTestSupport {
    
       /** 测试目标Entity类 */
       private static final Class<SystemAccountEntity> ENTITY_CLASS = SystemAccountEntity.class;


       /**
        * 字符类型以及字符串长的测试用例
        */
       @Test
       public void testCharsetAndLength() {
            // 【说明】记载测试数据的工作表名
            String sheetName = "testCharsetAndLength";        

            // 【说明】测试数据的ID
            String id = "charsetAndLength";

            // 【说明】执行测试
            testValidateCharsetAndLength(ENTITY_CLASS, sheetName, id);
       }


       // 【说明】～后略～



执行此方法时，测试数据的每行按以下观点执行测试。

+---------------+-----------------------------+---------------------------------------------------+
| 观点          |输入值                       | 备注                                              |
+===============+=============================+===================================================+
| 字符类型      |半角英文字母                 | | max(最大字符串长)栏中记载的长度的字符串         |
+---------------+-----------------------------+ | 构成。                                          |
| 字符类型      |半角数字                     |                                                   |
+---------------+-----------------------------+                                                   |
| 字符类型      |半角数字                     |                                                   |
+---------------+-----------------------------+                                                   |
| 字符类型      |半角符号                     |                                                   |
+---------------+-----------------------------+                                                   |
| 字符类型      |半角片假名                   |                                                   |
+---------------+-----------------------------+                                                   |
| 字符类型      |全角英文字母                 |                                                   |
+---------------+-----------------------------+                                                   |
| 字符类型      |全角数字                     |                                                   |
+---------------+-----------------------------+                                                   |
| 字符类型      |全角平假名                   |                                                   |
+---------------+-----------------------------+                                                   |
| 字符类型      |全角片假名                   |                                                   |
+---------------+-----------------------------+                                                   |
| 字符类型      |全角汉字                     |                                                   |
+---------------+-----------------------------+                                                   |
| 字符类型      |全角符号及其他               |                                                   |
+---------------+-----------------------------+                                                   |
| 字符类型      |外字                         |                                                   |
+---------------+-----------------------------+---------------------------------------------------+
| 未输入        |空字符                       | | 长度0的字符串                                   |
+---------------+-----------------------------+---------------------------------------------------+
| 最小字符串    |最小字符串长的字符串         | | 输入值由标记o的字符类型构成。                   |
+---------------+-----------------------------+ | min栏省略时，                                   |
| 最长字符串    |最大字符串长的字符串         | | 字符串长不足的测试不会执行。                    |
+---------------+-----------------------------+                                                   |
| 字符串长不足  |最小字符串长－1的字符串      |                                                   |
+---------------+-----------------------------+                                                   |
| 字符串长超过  |最大字符串长＋1的字符串      |                                                   |
+---------------+-----------------------------+---------------------------------------------------+



其他单项目校验的测试用例
================================

前述的，使用字符类型和字符串长的单项目校验测试用例\
可以测试大部分单项目校验，但部分校验可能无法覆盖。
例如，可以列举数值输入项目的范围校验。


这些单项目校验的测试，也准备了可以简易测试的机制。
对各属性，通过描述1个输入值和期待的消息ID的组合，
可以使用任意值进行单项目校验的测试。


.. tip::
   本测试方法对属性中持有其他Form的Form不能使用。这种情况下，请自行实现校验处理的测试。
   属性中持有其他Form的Form是指，通过以下形式访问属性的父Form。
   
   .. code-block:: none
   
      <父Form>.<子Form>.<子Form的属性名>


测试用例表的创建方法
------------------------

准备以下列。

+-----------------------------+--------------------------------------------------+
| 列名                        | 记载内容                                         |
+=============================+==================================================+
|propertyName                 |测试目标的属性名                                  |
+-----------------------------+--------------------------------------------------+
|case                         |测试用例的简单说明                                |
+-----------------------------+--------------------------------------------------+
|input1\ [#]_                 |输入值 [#]_                                       |
+-----------------------------+--------------------------------------------------+
|messageId                    |上述输入值进行单项目校验时，预期发生              |
|                             |的消息ID(期待不发生校验错误时留空)                |
+-----------------------------+--------------------------------------------------+


.. [#] 一个键需要指定多个参数时，增加input2, input3等列。

\

.. [#] \ :ref:`special_notation_in_cell`\ 的记法可用于高效创建输入值。

具体示例如下。

.. image:: ../_image/entityUnitTest_singleValidationDataExample.png
   :scale: 70           


测试方法的创建方法
------------------------

 
启动超类的以下方法。

.. code-block:: java

   void testSingleValidation(Class entityClass, String sheetName, String id)




.. code-block:: java

 // 【说明】～前略～

 public class SystemAccountEntityTest extends EntityTestSupport {
    
      /** 测试目标Entity类 */
      private static final Class<SystemAccountEntity> ENTITY_CLASS = SystemAccountEntity.class;

      /**
       * 字符类型以及字符串长的单项目校验测试用例
       */
      // 【说明】～中略～

      /**                          
       * 单项目校验的测试用例(上述以外)          
       */                          
      @Test                      
      public void testSingleValidation() {         
          String sheetName = "testSingleValidation";   
          String id = "singleValidation";              
          testSingleValidation(ENTITY_CLASS, sheetName, id);
      }                                                     


       // 【说明】～后略～


验证方法的测试用例
====================================

上述的单项目校验测试中，只测试了Entity的setter方法赋予的注解是否
正确，Entity中实现的验证方法\ [#]_\ 并未执行。

因此，Entity中实现了自定义验证方法时，
需要另行创建测试。



.. [#] ``@ValidateFor``\ 注解赋予的static方法


测试用例表的创建
--------------------

* ID固定为"testShots"。
* 准备以下列。

 +---------------------------------+-----------------------------------------------+
 | 列名                            | 记载内容                                      |
 +=================================+===============================================+
 | title                           | 测试用例的标题                                |
 +---------------------------------+-----------------------------------------------+
 | description                     | 测试用例的简单说明                            |
 +---------------------------------+-----------------------------------------------+
 |expectedMessageId\ *n* \ [#]_   | 期待的消息(\ *n*\ 为从1开始的序号)            |
 +---------------------------------+-----------------------------------------------+
 | propertyName\ *n*              | 期待的属性(\ *n*\ 为从1开始的序号)            |
 +---------------------------------+-----------------------------------------------+

.. [#]  期待多个消息时，将数值增加为expectedMessageId2, propertyName2等，向右侧添加。


* 创建输入参数表

  * ID固定为"params"。
  * 上述测试用例表对应的输入参数\ [#]_ \逐行记载。

\

    .. [#] \ :ref:`special_notation_in_cell`\ 的记法可用于高效创建输入值。

\

    具体示例如下。

    .. image:: ../_image/entityUnitTest_validationTestData.png
      :scale: 70



测试用例、测试数据的创建
--------------------------------


.. _entityUnitTest_ValidationMethodSpecifyNormal:


校验目标确认
~~~~~~~~~~~~

指定校验目标的属性(\ :ref:`nablarch_validation`\ 参照)时，
需要创建确认该指定是否正确的用例。


对所有属性，各自准备单项目校验时发生错误的数据。\
校验目标属性的指定正确的话，应该只有校验目标的属性进行单项目校验。\
因此，作为期待值，记载全部校验目标属性名和各属性单项目校验错误时的消息ID。\


.. tip::
 校验目标属性误从校验目标遗漏时，\
 期待的消息不会输出，因此消息ID的断言会失败。\
 此外，非校验目标的属性误成为校验目标时，\
 因输入值不正规导致单项目校验失败，输出意外的消息。\
 由此可以检测校验目标的错误。


测试用例表中，记载全部校验目标属性的属性名和\
该属性单项目校验错误消息ID。

.. image:: ../_image/entityUnitTest_ValidationPropTestCases.png
 :scale: 70


输入参数表中，对所有属性各自记载单项目校验错误的值。


.. image:: ../_image/entityUnitTest_ValidationPropParams.png
 :scale: 68


.. tip::

   创建Form单元测试的测试用例和测试数据时，\
   有时想指定**属性中持有的其他Form的属性**。\
   这种情况下，可以如下指定。
   
   * Form的代码示例
   
   .. code-block:: java
   
     public class SampleForm {

         /** 系统用户 */
         private SystemUserEntity systemUser;

         /** 电话号码数组 */
         private UserTelEntity[] userTelArray;
     
         // 【说明】属性以外省略
     
     }

   * 指定持有Form的属性的方法(指定SystemUserEntity.userId时)
   
   .. code-block:: none
   
      sampleForm.systemUser.userId

   * 指定Form数组元素属性的方法(指定UserTelEntity数组首个元素属性时)
   
   .. code-block:: none
   
      sampleForm.userTelArray[0].telNoArea



项目间校验等
~~~~~~~~~~~~~~

项目间校验等，验证方法的\ :ref:`entityUnitTest_ValidationMethodSpecifyNormal`\ 
进行的校验目标指定以外的动作确认的用例。

下图中，创建了"newPassword和confirmPassword相等"这一验证方法的正常系用例。

.. image:: ../_image/entityUnitTest_RelationalValidation.png
 :scale: 100


测试方法的创建方法
------------------------

使用此前创建的测试用例、数据的测试方法如下所示。\
更改下述代码的变量内容，即可对应不同Entity的校验测试。

.. code-block:: java

    // ～前略～

    /** 测试目标Entity类 */
    private static final Class<SystemAccountEntity> ENTITY_CLASS = SystemAccountEntity.class;

    // ～中略～
    /**
     * {@link SystemAccountEntity#validateForRegisterUser(nablarch.core.validation.ValidationContext)} 的测试。
     */
    @Test
    public void testValidateForRegisterUser() {
        // 执行校验
        String sheetName = "testValidateForRegisterUser";
        String validateFor = "registerUser";
        testValidateAndConvert(ENTITY_CLASS, sheetName, validateFor);
    }

   // ～后略～



.. _entityUnitTest_ConstructorCase:

构造函数的测试用例
==================================

使用Nablarch Validation进行输入值检查的Entity，如 :ref:`nablarch_validation-execute` 所述
实现了以 ``Map<String, Object>`` 为参数的构造函数，需要创建对此构造函数的测试。

构造函数的测试中，创建确认参数指定的值是否正确设置到属性中的用例。\
此时作为目标的属性，是Entity中定义的所有属性。\
测试数据中，准备属性名和要设置到该属性的数据以及期待值(与getter获取的值比较的数据)。

下图中，如下对各属性指定了值。
测试中，确认构造函数被赋予这些值的组合时，各属性是否被指定了值(调用getter，是否能获取到预期的值)。

实际的测试代码中，构造函数的值设置及值的确认，在自动化测试框架提供的方法内进行。
详情请参照 :ref:`测试代码<test-constructor-java-label>` 。


.. tip::
   
   Entity是自动生成的，因此可能生成应用中不使用的构造函数。\
   这种情况下在请求单元测试中无法测试，因此必须在Entity单元测试中进行构造函数的测试。
   
   另一方面，一般的Form，只创建应用中使用的构造函数。\
   因此，可以在请求单元测试中进行构造函数的测试。\
   所以，一般的Form不需要在类单元测试中进行构造函数的测试。

Excel的定义
-------------
.. image:: ../_image/entityUnitTest_Constructor.png
    :scale: 80

上述设置值的测试内容(摘录)

=============== =========================== ================================
属性            设置到构造函数的值            期待值(getter获取的值)
=============== =========================== ================================
userId          userid                      userid
loginId         loginid                     loginid
password        password                    password
=============== =========================== ================================

.. _test-constructor-java-label:

使用此数据的测试方法如下所示。

.. code-block:: java

   // 【说明】～前略～

   public class SystemAccountEntityTest extends EntityTestSupport {

        /** 构造函数的测试 */
        @Test
        public void testConstructor() {
            Class<?> entityClass = SystemAccountEntity.class;
            String sheetName = "testAccessor";
            String id = "testConstructor";
            testConstructorAndGetter(entityClass, sheetName, id);
        }

   }


.. _testConstructorAndGetter-note-label:

.. tip::

  testConstructorAndGetter可测试的属性类型(类)有限制。
  不属于以下类型(类)时，需要在各测试类中显式调用构造函数和getter进行测试。


  * String及String数组
  * BigDecimal及BigDecimal数组
  * java.util.Date及java.util.Date数组(在Excel中以yyyy-MM-dd格式或yyyy-MM-dd HH:mm:ss格式记述)
  * 持有valueOf(String)方法的类及其数组类(例如Integer、Long、java.sql.Date、java.sql.Timestamp等)

  以下是个别测试实施方法的示例。
  此示例中，假设Form持有 ``List<String>`` 类型的属性 ``users`` 。


    * Excel数据记述示例

      .. image:: ../_image/entityUnitTest_ConstructorOther.png
        :scale: 80

    

    * 测试代码示例

      .. code-block:: java

       /** 构造函数的测试 */
       @Test
       public void testConstructor() {
           // 【说明】
           // 可以共通测试的项目，使用testConstructorAndGetter进行测试。
           Class<?> entityClass = SystemAccountEntity.class;
           String sheetName = "testAccessor";
           String id = "testConstructor";
           testConstructorAndGetter(entityClass, sheetName, id);

           // 【说明】
           // 无法共通测试的项目，个别进行测试。

           // 【说明】
           // 调用getParamMap，获取个别进行测试的属性的测试数据。
           // (测试目标的属性有多个时，使用getListParamMap。)
           Map<String, String[]> data = getParamMap(sheetName, "testConstructorOther");

           // 【说明】从Map<String, String[]>转换为Entity构造函数参数Map<String, Object>
           Map<String, Object> params = new HashMap<String, Object>();
           params.put("users", Arrays.asList(data.get("set")));

           // 【说明】使用上述生成的Map<String, Object>作为参数生成Entity。
           SystemAccountEntity entity = new SystemAccountEntity(params);

           // 【说明】调用getter，确认返回预期的值。
           assertEquals(entity.getUsers(), Arrays.asList(data.get("get")));

       }

.. _entityUnitTest_SetterGetterCase:

setter、getter的测试用例
==================================

请参照 :ref:`entityUnitTest_SetterGetterCase_BeanValidation` 。

\

.. _entityUnitTest_EntityTestConfiguration:

自动化测试框架设置值
==============================

说明执行 :ref:`entityUnitTest_ValidationCase`\ 时需要的初始值设置。


设置项目一览
------------

使用 ``nablarch.test.core.entity.EntityTestConfiguration``\ 类，
在组件设置文件中设置以下值(所有项目必填)。

+--------------------+----------------------------------------------+
|     设置项目名     |说明                                          |
+====================+==============================================+
|maxMessageId        |最大字符串长超过时的消息ID                    |
+--------------------+----------------------------------------------+
|maxAndMinMessageId  |最长最小字符串长范围外的消息ID(可变长)        |
+--------------------+----------------------------------------------+
|fixLengthMessageId  |最长最小字符串长范围外的消息ID(固定长)        |
+--------------------+----------------------------------------------+
|underLimitMessageId |字符串长不足时的消息ID                        |
+--------------------+----------------------------------------------+
|emptyInputMessageId |未输入时的消息ID                              |
+--------------------+----------------------------------------------+
|characterGenerator  |字符串生成类 \ [#]_\                          |
+--------------------+----------------------------------------------+

.. [#]
 ``nablarch.test.core.util.generator.CharacterGenerator``\ 的实现类。
 此类生成测试用的输入值。
 通常，使用 ``nablarch.test.core.util.generator.BasicJapaneseCharacterGenerator``\ 即可。


设置的消息ID要与验证器的设置值一致。

(参照以下记述示例)


组件设置文件的记述示例
------------------------------------

使用以下设置值时的组件设置文件记述示例如下。

**【校验类的组件设置文件】**

.. code-block:: xml

    <property name="validators">
      <list>
        <component class="nablarch.core.validation.validator.RequiredValidator">
          <property name="messageId" value="MSG00010"/>
        </component>
        <component class="nablarch.core.validation.validator.LengthValidator">
          <property name="maxMessageId" value="MSG00011"/>
          <property name="maxAndMinMessageId" value="MSG00011"/>
          <property name="fixLengthMessageId" value="MSG00023"/>
        </component>
        <!-- 中略 -->
    </property>


**【测试的组件设置文件】**

.. code-block:: xml
 
  <!-- Entity测试设置 -->
  <component name="entityTestConfiguration" class="nablarch.test.core.entity.EntityTestConfiguration">
    <property name="maxMessageId"        value="MSG00011"/>
    <property name="maxAndMinMessageId"  value="MSG00011"/>
    <property name="fixLengthMessageId"  value="MSG00023"/>
    <property name="underLimitMessageId" value="MSG00011"/>
    <property name="emptyInputMessageId" value="MSG00010"/>
    <property name="characterGenerator">
      <component name="characterGenerator"
                 class="nablarch.test.core.util.generator.BasicJapaneseCharacterGenerator"/>
    </property>
  </component>
