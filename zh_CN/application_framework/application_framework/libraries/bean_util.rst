.. _bean_util:

BeanUtil
==================================================
.. contents:: 目录
  :depth: 3
  :local:

提供与Java Beans相关的以下功能。此外，Java16起标准化的记录(record)也可以像Java Beans一样处理。
详细请参考 :ref:`bean_util-use_record` 。

* 对属性设置值和获取值
* 向其他Java Beans移送值
* Java Beans与java.util.Map之间的值移送

模块列表
---------------------------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-beans</artifactId>
  </dependency>

.. _bean_util-use_java_beans:

使用方法
--------------------------------------------------
使用 :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` 提供的API，可以实现对任意Java Beans的操作。

以下显示BeanUtil的使用示例。

Bean定义
  .. code-block:: java

    public class User {
        private Long id;
        private String name;
        private Date birthDay;
        private Address address;
        // getter & setter省略
    }

    public class Address {
        private String postNo;
        // getter & setter省略
    }

    public class UserDto {
        private String name;
        private String birthDay;
        // getter & setter省略
    }

BeanUtil使用示例
  以下显示若干API的使用示例。
  详细请参考BeanUtil的 :java:extdoc:`Javadoc <nablarch.core.beans.BeanUtil>` 。

  .. code-block:: java

    final User user = new User();
    user.setId(1L);
    user.setName("名称");
    user.setBirthDay(new Date());

    final Address address = new Address();
    address.setPostNo("1234");
    user.setAddress(address);
    

    // 指定属性名获取值(可获取1)
    // 值通过getter获取
    final Long id = (Long) BeanUtil.getProperty(user, "id");

    // 指定属性名设置值(name属性的值变更为"新名称")
    // 值通过setter设置
    BeanUtil.setProperty(user, "name", "新名称");

    // 创建其他Bean的同时移送值
    // 向User的属性名与UserDto一致的属性移送值
    // 值的移送使用getter和setter进行
    // 目标不存在的属性将被忽略
    // 目标属性类型不同时，通过ConversionUtil进行类型转换
    final UserDto dto = BeanUtil.createAndCopy(UserDto.class, user);

    // 将属性值移送至Map
    // Map的键为属性名，值为getter获取的值
    // 嵌套Bean的值键名以"."分隔移送(不做Map -> Map的嵌套)
    // 例如，address.postNo
    final Map<String, Object> map = BeanUtil.createMapAndCopy(user);
    final String postNo = (String) map.get("address.postNo");     // 可获取1234

    // 将Map的值移送至Bean
    // 使用Map键匹配的属性的setter将Map的值移送
    // 向嵌套Bean移送值时，Map键名需要以"."分隔(无法处理Map -> Map的嵌套)
    // 例如，通过定义address.postNo键名，可以向User.address的postNo属性设置值
    final Map<String, Object> userMap = new HashMap<String, Object>();
    userMap.put("id", 1L);
    userMap.put("address.postNo", 54321);
    final User user = BeanUtil.createAndCopy(User.class, userMap);
    final String postNo2 = user.getAddress()
                          .getPostNo();             // 可获取54321

.. important::

  BeanUtil不支持List型的型参数。要使用List型的型参数，请在具体类中覆盖getter来应对。

  .. code-block:: java

    public class ItemsForm<D extends Serializable> {
        private List<D> items;
        public List<D> getItems() {
            return items;
        }
        public void setItems(List<D> items) {
            this.items = items;
        }
    }

    public class Item implements Serializable {
        // 属性省略
    }

    // 不在具体类中覆盖的情况
    // 调用BeanUtil.createAndCopy(BadSampleForm.class, map)时，
    // 由于不支持List型的型参数，将发生运行时异常
    public class BadSampleForm extends ItemsForm<Item> {
    }

    // 在具体类中覆盖的情况
    // BeanUtil.createAndCopy(GoodSampleForm.class, map)正常运行
    public static class GoodSampleForm extends ItemsForm<Item> {
        @Override
        public List<Item> getItems() {
            return super.getItems();
        }
    }

.. _utility-conversion:

BeanUtil的类型转换规则
--------------------------------------------------
:java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` 在从Java Beans对象或Map对象
向其他Java Beans对象迁移数据时会转换属性类型。

另外，从Map对象向Java Beans对象迁移数据时，
如果Map对象的键包含 ``.`` ，则将该属性作为嵌套对象处理。

关于类型转换规则，请参考配置在 :java:extdoc:`nablarch.core.beans.converter` 包下的
各 :java:extdoc:`Converter <nablarch.core.beans.Converter>` 实现类。

.. important::

  默认提供的类型转换规则中，转换为精度较小的类型时(例如从Long转换为Integer)，
  即使指定了超过转换目标精度的值也会正常结束处理。
  因此，使用BeanUtil进行复制时，需要通过 :ref:`validation` 事先验证要复制的值是否被系统允许。
  如果不验证，可能会将非法值引入系统导致故障。

.. important::

  类型转换规则是应用共通的设置。
  如果只想在特定处理中应用不同的类型转换规则，请参考 :ref:`bean_util-format_logical` ，
  对特定属性或类型应用 :java:extdoc:`Converter <nablarch.core.beans.Converter>` 实现来应对。

.. _utility-conversion-add-rule:

添加类型转换规则
--------------------------------------------------

添加类型转换规则需要以下步骤。

1. 根据需要实现以下接口来实现类型转换处理

  * :java:extdoc:`Converter <nablarch.core.beans.Converter>`
  * :java:extdoc:`ExtensionConverter <nablarch.core.beans.ExtensionConverter>`
  
2. 创建 :java:extdoc:`ConversionManager <nablarch.core.beans.ConversionManager>` 的实现类。
   这次是在标准类型转换规则基础上添加规则，因此创建持有 :java:extdoc:`ConversionManager <nablarch.core.beans.ConversionManager>` 作为属性的
   :java:extdoc:`ConversionManager <nablarch.core.beans.ConversionManager>` 实现类。

  .. code-block:: java

    public class SampleConversionManager implements ConversionManager {

        private ConversionManager delegateManager;

        @Override
        public Map<Class<?>, Converter<?>> getConverters() {
            Map<Class<?>, Converter<?>> converters = new HashMap<Class<?>, Converter<?>>();

            // 标准转换器
            converters.putAll(delegateManager.getConverters());

            // 本次创建的转换器
            converters.put(BigInteger.class, new CustomConverter());

            return Collections.unmodifiableMap(converters);
        }

        @Override
        public List<ExtensionConverter<?>> getExtensionConvertor() {
            final List<ExtensionConverter<?>> extensionConverters =
                new ArrayList<ExtensionConverter<?>>(delegateManager.getExtensionConvertor());
            extensionConverters.add(new CustomExtensionConverter());
            return extensionConverters;
        }

        public void setDelegateManager(ConversionManager delegateManager) {
            this.delegateManager = delegateManager;
        }
    }

3. 在组件配置文件中设置 :java:extdoc:`ConversionManager <nablarch.core.beans.ConversionManager>` 的实现类

   要点
    * 组件名设为 **conversionManager** 。

   .. code-block:: xml

    <component name="conversionManager" class="sample.SampleConversionManager">
      <property name="delegateManager">
        <component class="nablarch.core.beans.BasicConversionManager" />
      </property>
    </component>

指定类型转换时允许的格式
--------------------------------------------------
类型转换时，可以通过指定允许的格式来解除日期和数值的格式。
例如，可以将String型的逗号编辑值(1,000,000)转换为数值型(1000000)。

允许的格式有以下3种指定方法。优先顺序为上面记载的较高。

* :ref:`BeanUtil调用时设置 <bean_util-format_logical>`
* :ref:`按属性用注解设置 <bean_util-format_property_setting>`
* :ref:`默认设置(系统共通设置) <bean_util-format_default_setting>`

.. _bean_util-format_default_setting:

设置默认(系统共通)的允许格式
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
格式的默认设置在组件配置文件中设置。

例如，对于画面上输入的数值，如果也要允许逗号编辑的情况，设置为默认值后可以省去个别指定。

以下显示设置方法。

要点
  * 以组件名 **conversionManager** 定义 :java:extdoc:`BasicConversionManager <nablarch.core.beans.BasicConversionManager>` 。
  * 在 ``datePatterns`` 属性中设置允许的日期及日期时间格式。
  * 在 ``numberPatterns`` 属性中设置允许的数值格式定义。
  * 允许多种格式时设置多个。

设置示例
  .. code-block:: xml

    <component name="conversionManager" class="nablarch.core.beans.BasicConversionManager">
      <!-- 指定日期及日期时间的允许格式 -->
      <property name="datePatterns">
        <list>
          <value>yyyy/MM/dd</value>
          <value>yyyy-MM-dd</value>
        </list>
      </property>
      <!-- 指定数值的允许格式 -->
      <property name="numberPatterns">
        <list>
          <value>#,###</value>
        </list>
      </property>
    </component>

.. important::

  如 ``yyyy/MM/dd`` 和 ``yyyy/MM/dd HH:mm:ss`` 这样指定了日期和日期时间格式时，
  日期时间格式的值也能被 `yyyy/MM/dd` 解析，导致时间信息丢失的情况。

  因此，默认指定时只需指定日期格式，对于日期时间格式的项目需要使用 :ref:`按属性用注解设置 <bean_util-format_property_setting>`
  覆盖默认设置等应对措施。

.. _bean_util-format_property_setting:

对复制目标的属性设置允许的格式
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
有时希望特定功能不应用 :ref:`默认设置 <bean_util-format_default_setting>` 而指定不同格式。
这种情况下，对复制目标的Bean(复制源或复制目标)的对应属性字段指定注解，覆盖允许的格式。

注解在复制源和复制目标任一方指定都可以工作，但基本上建议对String型属性对应的字段指定允许的格式。
因为持有格式值的是String型属性，对该属性指定允许格式是自然的。
如果复制源和复制目标双方都指定了，则使用复制源的设置。

例如，默认设置指定了日期格式，而只有特定功能希望允许日期时间格式时，可以使用此方法。

以下显示实现示例。

要点
  * 对复制源(复制目标)属性对应的字段设置 :java:extdoc:`CopyOption <nablarch.core.beans.CopyOption>` 注解。
  * 在CopyOption的 ``datePattern`` 中指定允许的日期及日期时间格式。
  * 在CopyOption的 ``numberPattern`` 中指定允许的数值格式。

实现示例
  .. code-block:: java

    public class Bean {
        // 指定允许的日期时间格式
        @CopyOption(datePattern = "yyyy/MM/dd HH:mm:ss")
        private String timestamp;

        // 指定允许的数值格式
        @CopyOption(numberPattern = "#,###")
        private String number;

        // setter及getter省略
    }

.. _bean_util-format_logical:

在BeanUtil调用时设置允许的格式
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
有时希望特定功能不应用 :ref:`默认设置 <bean_util-format_default_setting>` 而指定不同格式，
但使用OSS等自动生成Bean时可能无法使用 :ref:`按属性用注解设置 <bean_util-format_property_setting>` 。
此外，有时只想对特定属性应用不同的类型转换规则。

这种情况下，在调用 :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` 时，设置允许的格式和类型转换规则来应对。

以下显示实现示例。

要点
  * 使用 :java:extdoc:`CopyOptions <nablarch.core.beans.CopyOptions>` 对属性进行设置。
    ``CopyOptions`` 的构建方法请参考 :java:extdoc:`CopyOptions.Builder <nablarch.core.beans.CopyOptions.Builder>` 。
  * 使用生成的 :java:extdoc:`CopyOptions <nablarch.core.beans.CopyOptions>` 调用 :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` 。

实现示例
  .. code-block:: java

   final CopyOptions copyOptions = CopyOptions.options()
           // 对timestamp属性指定允许的格式
           .datePatternByName("timestamp", "yyyy年MM月dd日 HH时mm分ss秒")
           // 对custom属性应用CustomDateConverter
           .converterByName("custom", Date.class, new CustomDateConverter())
           .build();

    // 指定CopyOptions调用BeanUtil
    final DestBean copy = BeanUtil.createAndCopy(DestBean.class, bean, copyOptions);


.. _bean_util-use_record:

在BeanUtil中使用记录(record)
--------------------------------------------------

BeanUtil可以像Java Beans一样处理Java16起标准化的记录(record)。

需要注意，一旦生成的记录之后无法更改。
因此，如果将记录作为变更对象的对象传递给 :java:extdoc:`BeanUtil.setProperty <nablarch.core.beans.BeanUtil.setProperty(java.lang.Object,java.lang.String,java.lang.Object)>` 或
:java:extdoc:`BeanUtil.copy <nablarch.core.beans.BeanUtil.copy(SRC,DEST)>` 等method的参数，将发生运行时异常。

使用方法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

与 :ref:`Java Beans的操作 <bean_util-use_java_beans>` 相同。

.. important::

  BeanUtil不支持包含List型型参数的记录。由于记录无法继承，
  因此List型的型参数需要从开始就设置为具体类型来定义记录。

  .. code-block:: java

    public class Item implements Serializable {
        // 属性省略
    }

    // List型的型参数未设置具体类型的情况
    // 调用BeanUtil.createAndCopy(BadSampleRecord.class, map)时，
    // 由于不支持List型的型参数，将发生运行时异常
    public class BadSampleRecord<T>(List<T> items) {}

    // List型的型参数设置了具体类型的情况
    // BeanUtil.createAndCopy(GoodSampleRecord.class, map)正常运行
    public record GoodSampleRecord(List<Item> items) {}
