.. _nablarch_validation:

Nablarch Validation
==================================================

.. contents:: 目录
  :depth: 3
  :local:

本章介绍Nablarch独自实现的验证功能。

.. tip::

  如 :ref:`validation` 中所述，建议使用 :doc:`bean_validation` 。

功能概述
--------------------------------------------------

可以进行验证和类型转换及值的规范化
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
在Nablarch的验证中，可以进行验证和输入值的类型转换、规范化。

由于可以进行类型转换，因此可以将输入值直接映射到Bean类的数值类型（Integer或Long）等。
此外，也可以在类型转换时进行已编辑值的编辑解除（规范化）等。

详情请参考 :ref:`nablarch_validation-definition_validator_convertor` 。

支持域验证
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
可以按域定义验证规则。

使用域验证后，Bean类的setter只需指定域名，便于修改验证规则。

详情请参考 `使用域验证`_ 。


.. _nablarch_validation-validator_convertor:

提供常用的验证器及转换器
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Nablarch标准提供了常用的验证器和转换器。
因此，项目侧只需进行 :ref:`nablarch_validation-definition_validator_convertor` 的设置，即可执行验证。

Nablarch提供的验证器及转换器请参考以下链接。

* :java:extdoc:`nablarch.core.validation.validator`
* :java:extdoc:`nablarch.core.validation.convertor`
* :java:extdoc:`nablarch.common.date`
* :java:extdoc:`nablarch.common.code.validator`


.. _nablarch_validation-module_list:

模块列表
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-validation</artifactId>
  </dependency>

  <!-- 仅在需要使用日期的验证器、转换器时 -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-date</artifactId>
  </dependency>

  <!-- 仅在需要使用代码值的验证器、转换器时 -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-code</artifactId>
  </dependency>

使用方法
--------------------------------------------------

.. _nablarch_validation-definition_validator_convertor:

设置要使用的验证器和转换器
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
要启用验证，需要在组件设置文件中注册要使用的验证器和转换器。

关于Nablarch提供的验证器及转换器，请参考 :ref:`nablarch_validation-validator_convertor` 。

.. important::

  如果没有验证器和转换器的设置，则无法使用验证功能，因此请务必设置。

设置示例
  * 以 **validationManager** 的名称对 :java:extdoc:`ValidationManager <nablarch.core.validation.ValidationManager>` 进行组件定义。
  * 在 :java:extdoc:`ValidationManager#convertors <nablarch.core.validation.ValidationManager.setConvertors(java.util.List)>` 中列举要使用的转换器。
  * 在 :java:extdoc:`ValidationManager#validators <nablarch.core.validation.ValidationManager.setValidators(java.util.List)>` 中列举要使用的验证器。

  .. code-block:: xml

    <component name="validationManager" class="nablarch.core.validation.ValidationManager">
      <property name="convertors">
        <list>
          <!-- 在这里列举要使用的转换器 -->
        </list>
      </property>
      <property name="validators">
        <list>
          <!-- 在这里列举要使用的验证器 -->
        </list>
      </property>

      <!--
      其他属性省略
      详情请参考ValidationManager的Javadoc
       -->
    </component>

设置验证规则
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
验证规则的注解设置在验证目标Bean类的属性（setter）中。
请注意，不能对getter设置注解。（即使设置了也无效）

.. tip::

  如果单独设置注解，会增加实现时的错误并提高维护成本，
  因此建议使用后述的 :ref:`域验证 <nablarch_validation-domain_validation>` 。

实现示例
  请参考 :ref:`Nablarch提供的验证器和转换器 <nablarch_validation-validator_convertor>` ，设置注解。

  此示例中， `userName` 为必填，允许全角文字最大10个字符。
  `birthday` 允许半角数字8位。
  `age` 允许整数最多3位。

  .. code-block:: java

    public class SampleForm {

      @Length(max = 10)
      @SystemChar(charsetDef = "全角文字")
      @Required
      public void setUserName(String userName) {
          this.userName = userName;
      }

      @Length(min = 8, max = 8)
      @SystemChar(charsetDef = "半角数字")
      public void setBirthday(String birthday) {
          this.birthday = birthday;
      }

      @Digits(integer = 3)
      public void setAge(Integer age) {
          this.age = age;
      }
    }

.. _nablarch_validation-domain_validation:

使用域验证
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
展示使用域验证的设置和实现示例。

创建定义了每个域的验证规则的Enum
  要使用域验证，首先需要创建持有每个域的验证规则的Enum（域Enum）。
  此Enum必须实现 `DomainDefinition` 接口。

  Enum的各个枚举值即为域名。以下示例中定义了 ``NAME`` 和 ``DATE`` 两个域。

  .. code-block:: java

    public enum SampleDomain implements DomainDefinition {

        @Length(max = 10)
        @SystemChar(charsetDef = "全角文字")
        NAME,

        @Length(min = 8, max = 8)
        @SystemChar(charsetDef = "半角数字")
        DATE;

        // 接口中定义的方法的实现
        // 实现内容必须与此示例完全相同
        @Override
        public Annotation getConvertorAnnotation() {
            return DomainValidationHelper.getConvertorAnnotation(this);
        }

        @Override
        public List<Annotation> getValidatorAnnotations() {
            return DomainValidationHelper.getValidatorAnnotations(this);
        }
    }

创建表示域的注解
  创建表示域的注解。
  使 `value` 属性可以指定上述创建的域Enum。

  .. code-block:: java

    @ConversionFormat
    @Validation
    @Target(ElementType.METHOD)
    @Retention(RetentionPolicy.RUNTIME)
    public @interface Domain {
        SampleDomain value();
    }

在验证目标的Bean中设置域
  通过设置上述创建的表示域的注解，即可进行域验证。

  此示例中，对 `userName` 执行 `SampleDomain.NAME` 中设置的验证。
  ※如果设置了转换器，也会进行转换器对值的转换。

  .. code-block:: java

    @Domain(SampleDomain.NAME)
    public void setUserName(String userName) {
        this.userName = userName;
    }

启用域验证所需的设置
  要启用域验证，需要以下设置。

  * :java:extdoc:`DomainValidationHelper <nablarch.core.validation.domain.DomainValidationHelper>` 的设置
  * :java:extdoc:`DomainValidator <nablarch.core.validation.domain.DomainValidator>` 的设置
  * :java:extdoc:`ValidationManager <nablarch.core.validation.ValidationManager>` 的设置
  * 初始化组件的设置

  以下展示示例。

  :java:extdoc:`DomainValidationHelper <nablarch.core.validation.domain.DomainValidationHelper>` 的设置
    * 在 :java:extdoc:`domainAnnotation属性 <nablarch.core.validation.domain.DomainValidationHelper.setDomainAnnotation(java.lang.String)>`   
      中设置表示域的注解的完全限定名（FQCN）。

    .. code-block:: xml

      <component name="domainValidationHelper"
          class="nablarch.core.validation.domain.DomainValidationHelper">

        <property name="domainAnnotation" value="sample.Domain" />

      </component>

  :java:extdoc:`DomainValidator <nablarch.core.validation.domain.DomainValidator>` 的设置
    * 在 :java:extdoc:`domainValidationHelper属性 <nablarch.core.validation.domain.DomainValidator.setDomainValidationHelper(nablarch.core.validation.domain.DomainValidationHelper)>` 
      中，设置上述设置的 :java:extdoc:`DomainValidationHelper <nablarch.core.validation.domain.DomainValidationHelper>` 。
    * 在 :java:extdoc:`validators属性 <nablarch.core.validation.domain.DomainValidator.setValidators(java.util.List)>` 
      中设置验证器列表。

    .. code-block:: xml

      <component name="domainValidator"
          class="nablarch.core.validation.domain.DomainValidator">

        <!--
          请勿在此处设置DomainValidator。如果设置会导致循环引用，
          系统仓库初始化时会发生错误。
        -->
        <property name="validators">
          <list>
            <component-ref name="requiredValidator" />
          </list>
        </property>
        <property name="domainValidationHelper" ref="domainValidationHelper" />
      </component>


  :java:extdoc:`ValidationManager <nablarch.core.validation.ValidationManager>` 的设置
    * 在 :java:extdoc:`domainValidationHelper属性 <nablarch.core.validation.ValidationManager.setDomainValidationHelper(nablarch.core.validation.domain.DomainValidationHelper)>` 
      中，设置上述设置的 :java:extdoc:`DomainValidationHelper <nablarch.core.validation.domain.DomainValidationHelper>` 。
    * 在 :java:extdoc:`validators属性 <nablarch.core.validation.ValidationManager.setValidators(java.util.List)>` 
      中设置验证器列表（不要忘记上述设置的 :java:extdoc:`DomainValidator <nablarch.core.validation.domain.DomainValidator>` ）。


    .. code-block:: xml

      <component name="validationManager" class="nablarch.core.validation.ValidationManager">
        <property name="validators">
          <list>
            <component-ref name="domainValidator" />
            <!-- 其他验证器的描述省略 -->
          </list>
        </property>
        <property name="domainValidationHelper" ref="domainValidationHelper" />
      </component>

  初始化组件的设置
    将上述设置的 :java:extdoc:`DomainValidator <nablarch.core.validation.domain.DomainValidator>` 和
    :java:extdoc:`ValidationManager <nablarch.core.validation.ValidationManager>` 设置到初始化目标列表中。
    
    .. code-block:: xml

      <component name="initializer"
          class="nablarch.core.repository.initialization.BasicApplicationInitializer">

        <property name="initializeList">
          <list>
            <component-ref name="validationManager" />
            <component-ref name="domainValidator" />
          </list>
        </property>
      </component>

在域验证中设置多个验证规则时的行为
  在域验证中，如果1个输入项目存在多个错误，则在第1个错误处停止验证。

  .. code-block:: java

        public enum SampleDomain implements DomainDefinition {
          @Length(max = 10)
          @SystemChar(charsetDef = "全角文字")
          NAME;
       }

  如果上述 `NAME` 发生 `Length` 验证错误，则不执行 `SystemChar` 验证。


继承验证目标的Bean
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
验证目标的Bean可以继承，但由于以下原因不推荐继承。

如果轻易继承，可能由于父类的更改导致执行意外的验证，
或者需要注意复杂的验证覆盖规则来设置注解，从而成为错误（Bug）的原因。

另外，继承Bean时的动作如下。

* 仅在子类侧添加 :java:extdoc:`@PropertyName <nablarch.core.validation.PropertyName>` 时，使用父类侧的验证器和转换器。
* 如果在子类侧添加1个验证器用的注解，则忽略父类侧的验证器注解，
  使用子类侧的验证器。转换器使用父类的。
* 如果在子类侧添加1个转换器用的注解，则忽略父类的转换器注解，
  使用子类侧的转换器。验证器使用父类的。
* 如果在子类侧同时设置了验证器和转换器，则全部使用子类侧的设置。
* 无法在子类侧删除父类侧的转换器设置。


在以下父子关系的Bean中，对 `ChildForm` 的 `value` 属性，
执行 :java:extdoc:`@Digits <nablarch.core.validation.convertor.Digits>` 和 :java:extdoc:`@NumberRange <nablarch.core.validation.validator.NumberRange>` 的验证。

.. code-block:: java

  // 父Form
  public class ParentForm {
    @Digits(integer=5, fraction=3)
    public void setValue(BigDecimal value) {
        this.value = value;
    }
  }

  // 子Form
  public class ChildForm extends ParentForm {
    @Override
    @NumberRange(min=100.0, max=20000.0)
    public void setValue(BigDecimal value) {
        super.setBdValue(value);
    }
  }

.. _nablarch_validation-execute:

执行验证
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
验证可以通过调用 :java:extdoc:`ValidationUtil <nablarch.core.validation.ValidationUtil>` 提供的方法来执行。

实现示例
  首先，为了从输入值生成Bean对象，在验证目标的Bean中实现以Map为参数的构造函数。

  接下来实现用于对验证目标Bean进行验证的static方法。
  对此方法设置 :java:extdoc:`@ValidateFor <nablarch.core.validation.ValidateFor>` 注解，并通过参数指定用于识别验证的任意值。

  此方法所需的处理是使用 :java:extdoc:`ValidationUtil <nablarch.core.validation.ValidationUtil>` 执行验证。

  .. code-block:: java

    public class SampleForm {

      public SampleForm(Map<String, Object> params) {
          userName = (String) params.get("userName");
          birthDay = (String) params.get("birthDay");
          age = (Integer) params.get("age");
      }

      @Domain(SampleDomain.NAME)
      @Required
      public void setUserName(String userName) {
          this.userName = userName;
      }

      @Domain(SampleDomain.DATE)
      public void setBirthday(String birthday) {
          this.birthday = birthday;
      }

      @Domain(SampleDomain.AGE)
      public void setAge(Integer age) {
          this.age = age;
      }

      @ValidateFor("validate")
      public static void validate(ValidationContext<SampleForm> context) {
        // 对userName和birthday和age执行验证
        ValidationUtil.validate(context, new String[] {"userName", "birthday", "age"});
      }
    }

  要使用上述Bean验证输入值的 `request` ，请如下使用 :java:extdoc:`ValidationUtil <nablarch.core.validation.ValidationUtil>` 。
  另外，在Web应用的情况下，可以通过 `进行Web应用的用户输入值校验`_ 更简便地进行验证。

  .. code-block:: java

    // 执行验证
    // 使用SampleForm检查输入参数的request。
    //
    // 最后一个参数指定使用SampleForm的哪个验证方法进行验证。
    // 此示例中指向validate，因此使用SampleForm的@ValidateFor注解中
    // 指定为validate的方法执行验证。
    ValidationContext<SampleForm> validationContext =
            ValidationUtil.validateAndConvertRequest(SampleForm.class, request, "validate");

    // 如果发生验证错误，abortIfInvalid会抛出异常
    validationContext.abortIfInvalid();

    // 使用以Map为参数的构造函数生成Form。
    // （可以获取输入值request被转换后的Form）
    SampleForm form = validationContext.createObject();

.. _nablarch_validation-execute_explicitly:

显式执行验证
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
在 `执行验证`_ 中，是基于在Bean的属性（setter）中设置的注解执行验证，
这里介绍不设置注解而直接执行验证的方法。

原则上使用 `执行验证`_ 的方法进行验证，但在需要单独执行验证的情况下，
请使用此方法进行验证。
例如，使用 :ref:`代码管理的模式<code-use_pattern>` ，
只想在特定画面更改模式进行验证时，单独执行验证。


实现示例
  显式执行验证是在Bean类的 :java:extdoc:`@ValidateFor <nablarch.core.validation.ValidateFor>` 注解设置的方法中进行的。
  另外，显式执行验证时可指定的注解仅限于实现了 :java:extdoc:`DirectCallableValidator <nablarch.core.validation.DirectCallableValidator>` 的注解。
  （不能指定转换器。）

  .. code-block:: java

    public class SampleForm {
      // 属性省略

      @ValidateFor("validate")
      public static void validate(ValidationContext<SampleForm> context) {

          ValidationUtil.validate(context, new String[]{"userName", "prefectureCode"});

          // 对userName执行必填检查
          ValidationUtil.validate(context, "userName", Required.class);

          // 注解的参数以Map指定
          Map<String, Object> params = new HashMap<String, Object>();
          params.put("codeId", "1052");     // 代码ID
          params.put("pattern", "A");       // 使用的代码模式名
          params.put("messageId", "M4865"); // 错误消息的ID
          ValidationUtil.validate(context, "prefectureCode", CodeValue.class, params);
      }
    }

  .. important::

    要执行显式验证，需要事先对目标项目执行验证。
    详情请参考 :ref:`nablarch_validation-execute`

.. _nablarch_validation-system_char_validator:

进行字符种类验证
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
字符种类验证的定义方法与 :ref:`bean_validation` 相同。
详细的设置方法请参考 :ref:`Bean Validation的字符种类验证 <bean_validation-system_char_validator>` 。
但是，允许代理对的设置与 :ref:`bean_validation` 不同，请参考下文。

另外，使用的注解是 :java:extdoc:`@SystemChar <nablarch.core.validation.validator.unicode.SystemChar>` ，
与 :ref:`bean_validation` 的完全限定名不同（注解名相同），请注意。

允许代理对
  此验证默认不允许代理对。
  （即使在 `LiteralCharsetDef` 中明确定义了代理对的字符也不允许）

  要允许代理对时，需要在组件设置文件中如下设置 :java:extdoc:`SystemCharValidator#allowSurrogatePair <nablarch.core.validation.validator.unicode.SystemCharValidator.setAllowSurrogatePair(boolean)>` 。

  .. code-block:: xml

    <component name="systemCharValidator" class="nablarch.core.validation.validator.unicode.SystemCharValidator">
      <!-- 允许代理对 -->
      <property name="allowSurrogatePair" value="true"/>
  
      <!-- 其他属性省略 -->
    </component>

.. _nablarch_validation-correlation_validation:

进行关联验证
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
使用多个项目的关联验证是在Bean类的 :java:extdoc:`@ValidateFor <nablarch.core.validation.ValidateFor>` 注解设置的方法中实现的。
在此方法中首先执行每个项目的验证，如果没有发生错误，则执行使用多个项目的验证。

实现示例
  此示例进行使用mailAddress和confirmMailAddress的关联验证。

  关联验证出错时，将表示应通知用户的消息的消息ID显式添加到 :java:extdoc:`ValidationContext <nablarch.core.validation.ValidationContext>` 中。

  .. code-block:: java

    public class SampleForm {

      @Domain(SampleDomain.MAIL)
      @Required
      public void setMailAddress(String mailAddress) {
          this.mailAddress = mailAddress;
      }

      @Domain(SampleDomain.MAIL)
      @Required
      public void setConfirmMailAddress(String confirmMailAddress) {
          this.confirmMailAddress = confirmMailAddress;
      }

      @ValidateFor("validate")
      public static void validate(ValidationContext<SampleForm> context) {
          // 执行mailAddress和confirmMailAddress的验证
          ValidationUtil.validate(context, new String[] {"mailAddress", "confirmMailAddress"});

          // 如果发生错误，则不执行关联验证
          if (!context.isValid()) {
              return;
          }

          // 生成form对象，执行关联验证
          SampleForm form = context.createObject();
          if (!Objects.equals(form.mailAddress, form.confirmMailAddress)) {
              // mailAddress和confirmMailAddress不一致时出错
              context.addMessage("compareMailAddress");
          }
      }
    }

.. _nablarch_validation-nest_bean:

在批量注册等以Bean数组为输入的功能中进行验证
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
存在如批量注册这样输入多个相同信息的情况。
这种情况下，可以通过对验证目标Bean定义嵌套Bean来应对。

对嵌套Bean的setter设置 :java:extdoc:`@ValidationTarget <nablarch.core.validation.ValidationTarget>` 注解，指定嵌套Bean的大小。
如果元素数固定（编译时确定），则在 :java:extdoc:`size <nablarch.core.validation.ValidationTarget.size()>` 属性中指定。如果是可变的，
则在 :java:extdoc:`sizeKey <nablarch.core.validation.ValidationTarget.sizeKey()>` 属性中设置持有大小的属性名。

此示例中，由于可以批量输入 `AddressForm` 的信息，因此 `SampleForm` 将 `AddressForm` 作为数组持有。
另外，大小在编译时尚未确定，因此使用 :java:extdoc:`sizeKey <nablarch.core.validation.ValidationTarget.sizeKey()>` 。

.. code-block:: java

  public class SampleForm {
      private AddressForm[] addressForms;
      // addressForms的大小
      // 需要从画面的hidden等发送
      private Integer addressSize;

      @ValidationTarget(sizeKey = "addressSize")
      public void setAddressForms(AddressForm[] addressForms) {
          this.addressForms = addressForms;
      }

      @Domain(SampleDomain.SIZE)
      @Required
      public void setAddressSize(Integer addressSize) {
          this.addressSize = addressSize;
      }

      @ValidateFor("validate")
      public static void validate(ValidationContext<SampleForm> context) {
          ValidationUtil.validate(context, new String[] {"addressSize", "addressForms"});
      }
  }

  public class AddressForm {
      // 省略
  }

.. _nablarch_validation-conditional:

根据单选按钮或列表框的选择值更改验证项目
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
通过使用 :java:extdoc:`WebUtil <nablarch.common.web.WebUtil>` 类，可以根据单选按钮或列表框等的选择值来切换验证项目。

此示例中，当从画面发送的 **form.radio** 的值为 **ptn1** 时，仅对 `item1` 进行验证。
**ptn1** 以外的情况下，对 `item1` 和 `item2` 进行验证。

.. code-block:: java

  public class SampleForm {

      // 属性省略

      @ValidateFor("validate")
      public static void validate(ValidationContext<SampleForm> context) {
          if (WebUtil.containsPropertyKeyValue(context, "form.radio", "ptn1")) {
              ValidationUtil.validate(context, new String[] {"item1"});
          } else {
              ValidationUtil.validate(context, new String[] {"item1", "item2"});
          }
      }
  }

.. tip::

  此示例中，使用 :java:extdoc:`WebUtil.containsPropertyKeyValue <nablarch.common.web.WebUtil.containsPropertyKeyValue(nablarch.core.validation.ValidationContext,java.lang.String,java.lang.String)>` 检查到发送的值为止，
  但如果只是想简单地检查单选按钮是否被选中，请使用 :java:extdoc:`WebUtil.containsPropertyKey <nablarch.common.web.WebUtil.containsPropertyKey(nablarch.core.validation.ValidationContext,java.lang.String)>` 。


想创建与特定项目关联的验证错误消息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
请参考 :ref:`Bean Validation的创建与特定项目关联的验证错误消息 <bean_validation-create_message_for_property>` 。

.. _nablarch_validation-property_name:

想在验证错误消息中嵌入项目名
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
要在消息中嵌入项目名，请使用 :java:extdoc:`@PropertyName <nablarch.core.validation.PropertyName>` 注解指定验证目标项目的项目名。

实现示例
  在消息中使用用于嵌入项目名的模式字符。
  项目名始终指定在开头，因此在嵌入项目名的位置指定 **{0}** 。

  .. code-block:: properties

    required.message = 请输入{0}。

  对验证目标项目，与验证用的注解一起设置指定项目名的 `@PropertyName` 注解。

  .. code-block:: java

    public class SampleForm {

        @Domain(SampleDomain.NAME)
        @Required
        @PropertyName("姓名")
        public void setUserName(String userName) {
            this.userName = userName;
        }

        @Domain(SampleDomain.DATE)
        @PropertyName("生日")
        public void setBirthday(String birthday) {
            this.birthday = birthday;
        }
    }

生成的消息
  在上述实现中，如果 `username` 属性发生必填错误，生成的消息为 **「请输入姓名。」** 。

转换为数值类型
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
如果验证后想将输入值转换为Bean类的数值类型，该项目必须设置 :java:extdoc:`@Digits <nablarch.core.validation.convertor.Digits>` 注解。
※使用域验证时，需要对域Enum进行设置。

另外，用于转换为数值类型的转换器需要按照 :ref:`nablarch_validation-definition_validator_convertor` 的步骤进行设置。

实现示例
  此示例中虽然指定在setter中，但建议使用域验证时指定在域Enum中。

  .. code-block:: java

    public class SampleForm {

        @PropertyName("年龄")
        @Digits(integer = 3)
        public void setAge(Integer age) {
            this.age = age;
        }
    }

.. _nablarch_validation-database:

进行与数据库的关联验证
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
与数据库的关联验证在业务Action中进行。

在业务Action中进行的理由请参考 :ref:`Bean Validation的与数据库的关联验证 <bean_validation-database_validation>` 。

进行Web应用的用户输入值校验
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Web应用的用户输入值校验使用 :ref:`inject_form_interceptor` 进行。
详情请参考 :ref:`inject_form_interceptor`

扩展示例
--------------------------------------------------
想添加项目特有的验证器
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
要添加验证器，需要以下步骤。

#. 创建注解
#. 创建验证器
#. 在设置文件中注册验证器

以下展示步骤。

创建注解
  注解需要满足以下条件。

  * 设置 :java:extdoc:`@Validation <nablarch.core.validation.Validation>` 注解。
  * 在 :java:extdoc:`@Target <java.lang.annotation.Target>` 注解中设置 `ElementType.METHOD` 。
  * 在 :java:extdoc:`@Retention <java.lang.annotation.Retention>` 注解中设置 `RetentionPolicy.RUNTIME` 。

  .. code-block:: java

    @Validation
    @Target(ElementType.METHOD)
    @Retention(RetentionPolicy.RUNTIME)
    public @interface Sample {
    }

创建验证器
  验证器实现 :java:extdoc:`Validator <nablarch.core.validation.Validator>` 接口，实现验证逻辑。

  .. code-block:: java

    public class SampleValidator implements Validator {

      public Class<? extends Annotation> getAnnotationClass() {
          return Sample.class;
      }

      public <T> boolean validate(ValidationContext<T> context,
          // 省略
      }
    }

在设置文件中注册验证器
   请参考 :ref:`nablarch_validation-definition_validator_convertor` 。

想添加项目特有的转换器
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
要添加转换器，需要以下步骤。

#. 创建转换器
#. 在设置文件中注册转换器

以下展示步骤。

创建转换器
  转换器实现 :java:extdoc:`Convertor <nablarch.core.validation.Convertor>` 接口，实现类型转换逻辑等。

  .. code-block:: java

    public class SampleConvertor implements Convertor {

        @Override
        public Class<?> getTargetClass() {
            return Short.class;
        }

        @Override
        public <T> boolean isConvertible(ValidationContext<T> context, String propertyName, Object propertyDisplayName,
                Object value, Annotation format) {

            boolean convertible = true;

            if (value instanceof String) {
                try {
                    Short.valueOf((String) value);
                } catch (NumberFormatException e) {
                    convertible = false;
                }
            } else {
                convertible = false;
            }

            if (!convertible) {
                context.addResultMessage(propertyName, "sampleconvertor.message", propertyDisplayName);
            }
            return convertible;
        }

        @Override
        public <T> Object convert(ValidationContext<T> context, String propertyName, Object value, Annotation format) {
            return Short.valueOf((String) value);
        }
    }

在设置文件中注册转换器
  请参考 :ref:`nablarch_validation-definition_validator_convertor` 。

想更改验证目标Bean对象的生成方法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
要更改验证目标Bean对象的生成方法，需要以下步骤。

#. 创建 :java:extdoc:`FormCreator <nablarch.core.validation.FormCreator>` 的实现类
#. 在 :java:extdoc:`ValidationManager.formCreator <nablarch.core.validation.ValidationManager.setFormCreator(nablarch.core.validation.FormCreator)>` 中，添加创建的类的组件定义
