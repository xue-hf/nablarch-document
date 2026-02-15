.. _bean_validation:

Bean Validation
==================================================
.. contents:: 目录
  :depth: 3
  :local:

本章介绍符合Jakarta EE的Jakarta Bean Validation标准的验证功能。

.. important::

  此功能并非实现Jakarta Bean Validation引擎。

  在Jakarta EE环境（如WebLogic、WildFly等）中，将使用服务器内部捆绑的Jakarta Bean Validation实现。
  在Jakarta EE环境外使用时，需要另行添加Jakarta Bean Validation的参考库。
  （建议使用兼容实现 `Hibernate Validator(外部站点、英文) <https://hibernate.org/validator/>`_ 。）

功能概述
---------------------

支持域验证
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
提供可以按域定义验证规则的功能。

使用域验证后，Bean的属性只需指定域名，便于修改验证规则。

详情请参考 `使用域验证`_ 。

.. _bean_validation-validator:

提供常用的验证器
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Nablarch提供了常用的验证器，因此基本的验证无需自行开发即可使用。

Nablarch提供的验证器请参考以下包中的注解（注释类型）。

* :java:extdoc:`nablarch.core.validation.ee`
* :java:extdoc:`nablarch.common.code.validator.ee`

模块列表
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-validation-ee</artifactId>
  </dependency>
  
  <!--
   仅在需要使用消息管理来构建消息时
   默认使用消息管理
  -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-message</artifactId>
  </dependency>

  <!-- 仅在需要使用代码值验证器时 -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-code</artifactId>
  </dependency>
  
  <!-- 在Web应用中使用的情况 -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web</artifactId>
  </dependency>
  

使用方法
--------------------------------------------------

.. _bean_validation-configuration:

使用Bean Validation所需的设置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
使用Bean Validation所需的设置如下。

MessageInterpolator的设置
  设置用于在Jakarta Bean Validation发生验证错误时构建消息的类（实现了 :java:extdoc:`MessageInterpolator <jakarta.validation.MessageInterpolator>` 的类）。

  如果省略设置（默认），则使用使用 :ref:`message` 的 :java:extdoc:`NablarchMessageInterpolator <nablarch.core.validation.ee.NablarchMessageInterpolator>` 。

  例如，使用Hibernate Validator的从属性文件构建消息的实现时，请进行如下设置。

  .. important::

    组件名称必须设置为 **messageInterpolator** 。

  .. code-block:: xml

    <!-- 在组件名中指定messageInterpolator，设置MessageInterpolator的实现类 -->
    <compnent name="messageInterpolator"
        class="org.hibernate.validator.messageinterpolation.ResourceBundleMessageInterpolator"/>

域验证的设置
  请参考 :ref:`bean_validation-domain_validation`

在Web应用中使用Bean Validation的设置
  请参考 :ref:`bean_validation-web_application`

在RESTful Web服务中使用Bean Validation的设置
  请参考 :ref:`bean_validation-restful_web_service`

定义验证错误时的错误消息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
如 :ref:`bean_validation-configuration` 中所述，默认使用 :ref:`message` 来构建验证错误时的消息。
因此，关于消息的定义位置等详情，请参考 :ref:`message` 。

使用默认的 :java:extdoc:`NablarchMessageInterpolator <nablarch.core.validation.ee.NablarchMessageInterpolator>` 时的消息定义规则如下。

* 仅当注解的 ``message`` 属性中指定的值被 ``{`` 、``}`` 包围时，才使用 :ref:`message` 构建消息。
* 在消息文本中，可以使用占位符来嵌入验证注解的属性信息。
  占位符的定义方式是用 ``{`` 、 ``}`` 包围注解的属性名。
* 不能使用动态组装消息的表达式（如EL表达式）。

示例如下。

Java实现示例
  .. code-block:: java

      public class SampleForm {

        @Length(max = 10)
        @SystemChar(charsetDef = "全角文字")
        @Required
        private String userName;

        @Length(min = 8, max = 8)
        @SystemChar(charsetDef = "半角数字")
        private String birthday;

        // getter、setter省略
      }

消息定义示例
  以注解中指定的消息ID为键定义消息。
  如果未指定注解的message属性，则使用默认值作为消息ID。

  .. code-block:: properties

    # 对应Length注解的消息
    # 可以将Length注解的min和max属性中指定的值嵌入到消息中
    nablarch.core.validation.ee.Length.min.message=请输入{min}个字符以上。
    nablarch.core.validation.ee.Length.max.message=请输入{max}个字符以内。
    nablarch.core.validation.ee.Length.min.max.message=请输入{min}个字符以上{max}个字符以内。

    # 对应SystemChar的消息
    nablarch.core.validation.ee.SystemChar.message=请输入{charsetDef}。

.. tip:: 
  如果在 :ref:`bean_validation-configuration` 中修改了默认行为，
  请按照 :java:extdoc:`MessageInterpolator <jakarta.validation.MessageInterpolator>` 的实现来定义消息。


验证规则的设置方法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
验证规则可以通过将注解设置到Field或Property（getter）上来指定。
请注意，不能对setter设置注解。（即使设置了也无效（会被忽略））

.. _bean_validation-form_property:

.. tip::

  Bean类的属性类型请全部定义为String。

  在Bean Validation中，验证是在输入值转换为Bean之后进行的。
  因此，无论外部输入什么样的值作为输入值，都必须将其转换为Bean。

  如果存在String以外的属性，并且发送了不正确的值（例如，对数值类型发送了英文字母），
  则在验证前进行的向Bean的转换处理将失败，导致抛出意外异常而成为故障。

  本来，无论输入什么样的值，都不应作为故障，而应将验证结果通知给外部（例如画面）。

  如果想将来自外部的值转换为String以外的类型，请在验证后进行转换。

  即使在客户端使用JavaScript进行验证，
  也不能保证服务器端会接收到已验证的值，因此属性必须始终为 `String` 。
  这是因为用户可以轻易地在客户端禁用JavaScript或使用浏览器的开发者工具进行篡改。
  如果进行了此类操作，客户端验证可能被绕过，导致不正确的值被发送到服务器端。

实现示例
  请参考 :ref:`Nablarch提供的验证器 <bean_validation-validator>` ，设置注解。

  .. tip::

    如果单独设置注解，会增加实现时的错误并提高维护成本，
    因此建议使用后述的 :ref:`域验证 <bean_validation-domain_validation>` 。

  .. code-block:: java

    public class SampleForm {

      @Length(max = 10)
      @SystemChar(charsetDef = "全角文字")
      @Required
      private String userName;

      @Length(min = 8, max = 8)
      @SystemChar(charsetDef = "半角数字")
      private String birthday;

      // getter、setter省略
    }

.. _bean_validation-domain_validation:

使用域验证
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
展示使用域验证的设置和实现示例。

创建定义了每个域的验证规则的Bean
  要使用域验证，首先需要创建持有每个域的验证规则的Bean（域Bean）。

  在此Bean类中，定义每个域的字段，并对字段设置注解。
  字段名即为域名。以下示例中定义了 ``name`` 和 ``date`` 两个域。

  .. tip::

   表示必填项的 :java:extdoc:`@Required <nablarch.core.validation.ee.Required>` 注解应设置在单独的Bean侧，而不是域Bean中。
   因为是否必填不是域可以强制决定的，而是由功能设计决定的。

  .. code-block:: java

    package sample;

    import nablarch.core.validation.ee.Length;
    import nablarch.core.validation.ee.SystemChar;

    public class SampleDomainBean {

        @Length(max = 10)
        @SystemChar(charsetDef = "全角文字")
        String name;

        @Length(min = 8, max = 8)
        @SystemChar(charsetDef = "半角数字")
        String date;

    }

启用域Bean
  要启用域Bean，需要创建 :java:extdoc:`DomainManager <nablarch.core.validation.ee.DomainManager>` 实现类。
  :java:extdoc:`getDomainBean <nablarch.core.validation.ee.DomainManager.getDomainBean()>` 中返回域Bean的类对象。

  .. code-block:: java

    package sample;

    public class SampleDomainManager implements DomainManager<SampleDomainBean> {
      @Override
      public Class<SampleDomainBean> getDomainBean() {
          // 返回域Bean的Class对象
          return SampleDomainBean.class;
      }
    }


  通过在组件设置文件中定义 :java:extdoc:`DomainManager <nablarch.core.validation.ee.DomainManager>` 实现类的 `SampleDomainBean` ，
  即可启用使用 `SampleDomainBean` 的域验证。

  .. code-block:: xml

    <!-- DomainManager实现类必须以domainManager这个名称设置 -->
    <component name="domainManager" class="sample.SampleDomainManager"/>

在各Bean中使用域验证
  通过对Bean的验证目标属性设置 :java:extdoc:`@Domain <nablarch.core.validation.ee.Domain>` 注解，即可进行域验证。

  此示例中，对 `userName` 执行 `SampleDomainBean` 的 `name` 字段中设置的验证。
  同样，对 `birthday` 执行 `date` 字段中设置的验证。

  ※userName为必填项。

  .. code-block:: java

    public class SampleForm {

      @Domain("name")
      @Required
      private String userName;

      @Domain("date")
      private String birthday;

      // getter、setter省略
    }

.. _bean_validation-system_char_validator:

进行字符种类验证
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
通过使用系统允许字符的验证功能，可以按字符种类进行验证。

要按字符种类进行验证，需要为每个字符种类定义允许的字符集。
例如，对于"半角数字"这个字符种类，需要定义允许半角的 ``0`` 到 ``9`` 。

以下展示每个字符种类的允许字符集的定义方法。

在组件定义中定义允许的字符集
  允许的字符集使用以下类之一进行注册。
  注册时，请将组件名设置为表示字符种类的任意名称。

  * :java:extdoc:`RangedCharsetDef <nablarch.core.validation.validator.unicode.RangedCharsetDef>` （使用范围注册允许字符集时使用）
  * :java:extdoc:`LiteralCharsetDef <nablarch.core.validation.validator.unicode.LiteralCharsetDef>` （使用字面量注册所有允许字符时使用）
  * :java:extdoc:`CompositeCharsetDef <nablarch.core.validation.validator.unicode.CompositeCharsetDef>` （注册由多个RangedCharsetDef或LiteralCharsetDef组成的允许字符时使用）

  设置示例如下。

  .. code-block:: xml

    <!-- 半角数字 -->
    <component name="半角数字" class="nablarch.core.validation.validator.unicode.LiteralCharsetDef">
      <property name="allowedCharacters" value="01234567890" />
      <property name="messageId" value="numberString.message" />
    </component>

    <!-- ASCII(除控制字符外) -->
    <component name="ascii" class="nablarch.core.validation.validator.unicode.RangedCharsetDef">
      <property name="startCodePoint" value="U+0020" />
      <property name="endCodePoint" value="U+007F" />
      <property name="messageId" value="ascii.message" />
    </component>

    <!-- 英数字 -->
    <component name="英数字" class="nablarch.core.validation.validator.unicode.CompositeCharsetDef">
      <property name="charsetDefList">
        <list>
          <!-- 半角数字的定义 -->
          <component-ref name="半角数字" />

          <!-- 半角英文字母的定义 -->
          <component class="nablarch.core.validation.validator.unicode.LiteralCharsetDef">
            <property name="allowedCharacters"
                value="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" />
          </component>
        </list>
      </property>
      <property name="messageId" value="asciiAndNumberString.message" />
    </component>

在注解中指定字符种类
  对要进行字符种类验证的属性设置 :java:extdoc:`@SystemChar <nablarch.core.validation.ee.SystemChar>` 注解。
  此注解的 :java:extdoc:`charsetDef <nablarch.core.validation.ee.SystemChar.charsetDef()>` 属性中设置表示允许字符种类的名称。
  此名称即为上述在组件设置文件中注册字符种类集时的组件名。

  此示例中指定了 ``半角数字`` ，因此根据上述组件定义，允许「0123456789」。

  .. code-block:: java

    public class SampleForm {

        @SystemChar(charsetDef = "半角数字")
        public void setAccountNumber(String accountNumber) {
            this.accountNumber = accountNumber;
        }
    }

.. tip::

  当允许的字符集的字符数变得很大时，对后面定义的字符的检查将花费时间。（因为只是简单地从前向后依次检查字符是否包含在字符集中）
  为解决此问题，提供了缓存已检查字符结果的机制。

  ※原则上开发时请勿使用缓存功能，当字符种类验证确实成为瓶颈时，再考虑是否使用缓存功能。

  使用方法很简单，只需在以下组件定义中，将原始字符种类集的定义设置到用于缓存的 :java:extdoc:`CachingCharsetDef <nablarch.core.validation.validator.unicode.CachingCharsetDef>` 中即可。

  .. code-block:: xml

    <component name="半角数字" class="nablarch.core.validation.validator.unicode.CachingCharsetDef">
      <property name="charsetDef">
        <component class="nablarch.core.validation.validator.unicode.LiteralCharsetDef">
          <property name="allowedCharacters" value="01234567890" />
        </component>
      </property>
      <property name="messageId" value="numberString.message" />
    </component>

允许代理对
  此验证默认不允许代理对。
  （即使在 `LiteralCharsetDef` 中明确定义了代理对的字符也不允许）

  要允许代理对时，需要在组件设置文件中如下设置 :java:extdoc:`SystemCharConfig <nablarch.core.validation.ee.SystemCharConfig>` 。

  要点
   * 组件名必须为 ``ee.SystemCharConfig``

  .. code-block:: xml

    <component name="ee.SystemCharConfig" class="nablarch.core.validation.ee.SystemCharConfig">
      <!-- 允许代理对 -->
      <property name="allowSurrogatePair" value="true"/>
    </component>

.. _bean_validation-correlation_validation:

进行关联验证
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
要使用多个项目进行关联验证，需要使用Jakarta Bean Validation的 :java:extdoc:`@AssertTrue <jakarta.validation.constraints.AssertTrue>` 注解。

实现示例
  此示例验证邮箱地址和确认用邮箱地址是否一致。
  验证出错时， `message` 属性中指定的消息将成为错误消息。

  .. code-block:: java

    public class SampleForm {
      private String mailAddress;

      private String confirmMailAddress;

      @AssertTrue(message = "{compareMailAddress}")
      public boolean isEqualsMailAddress() {
        return Objects.equals(mailAddress, confirmMailAddress);
      }
    }

.. important::

  在Jakarta Bean Validation中，验证的执行顺序不保证，
  因此关联验证可能会在单项验证之前被调用。

  因此，在关联验证中，即使单项验证尚未执行，
  也需要实现验证逻辑以避免发生意外异常。

  例如，在上述示例中，如果 `mailAddress` 及 `confirmMailAddress` 为可选项目，
  则在未输入的情况下需要不执行验证而直接返回结果。

  .. code-block:: java
    
    @AssertTrue(message = "{compareMailAddress}")
    public boolean isEqualsMailAddress() {
      if (StringUtil.isNullOrEmpty(mailAddress) || StringUtil.isNullOrEmpty(confirmMailAddress)) {
        // 如果任一未输入，则不进行关联验证（视为验证OK）
        return true;
      }
      return Objects.equals(mailAddress, confirmMailAddress);
    }


.. _bean_validation-database_validation:

进行与数据库的关联验证
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
与数据库的关联验证，由于以下原因应在业务Action侧实现。

原因
  如果使用Bean Validation对数据库进行关联验证，
  将使用验证前不安全的值来访问数据库。
  （Bean Validation执行期间的对象值不能保证是安全的。）
  这可能导致SQL注入等漏洞，是应该避免的实现方式。

  通过在验证后在业务Action中进行验证，
  可以使用已验证的安全值访问数据库。

.. _bean_validation-create_message_for_property:

想创建与特定项目关联的验证错误消息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
如 :ref:`与数据库的关联验证 <bean_validation-database_validation>` 这样在Action Handler中进行验证时出错，
可能希望在画面上将目标项目作为错误高亮显示。

这种情况下，如以下实现示例所示，使用 :java:extdoc:`ValidationUtil#createMessageForProperty <nablarch.core.validation.ValidationUtil.createMessageForProperty(java.lang.String,java.lang.String,java.lang.Object...)>`
构建错误消息，并抛出 :java:extdoc:`ApplicationException <nablarch.core.message.ApplicationException>` 。

.. code-block:: java

  throw new ApplicationException(
          ValidationUtil.createMessageForProperty("form.mailAddress", "duplicate.mailAddress"));


在批量注册等输入多个Bean的功能中进行验证
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
存在如批量注册这样输入多个相同信息的情况。
这种情况下，可以通过对验证目标Bean定义嵌套Bean来应对。

.. tip::
  这是Jakarta Bean Validation的规范，详情请参考Jakarta Bean Validation的规范。

示例如下。

.. code-block:: java

  // 保存批量输入的所有信息的Form
  public class SampleBulkForm {

    // 设置Valid注解，表示对嵌套Bean也执行验证。
    @Valid
    private List<SampleForm> sampleForm;

    public SampleBulkForm() {
      sampleForm = new ArrayList<>();
    }

    // setter、getter省略
  }


  // 保存批量输入信息中的1条信息的Form
  public class SampleForm {
    @Domain("name")
    private String name;

    // setter、getter省略
  }

验证嵌套Bean时的注意事项
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
在使用浏览器开发者工具篡改html或Web服务接收到不正确的Json或XML时，可能无法接收到嵌套Bean的信息。
这种情况下，嵌套Bean将处于未初始化状态（null），无法成为验证目标。
因此，需要确保嵌套Bean的状态能够被验证的实现。

以下展示几个实现示例。

父Bean与嵌套Bean为1对N的情况
  将嵌套Bean作为验证目标，并在父Bean初始化时也初始化嵌套Bean的字段。
  如果嵌套Bean的信息是必填的（至少需要选择或输入1个），
  则设置 :java:extdoc:`Size <nablarch.core.validation.ee.Size>` 注解。
  
  .. code-block:: java

    // 通过设置Size注解，验证至少选择了1个。
    @Valid
    @Size(min = 1, max = 5)
    private List<SampleNestForm> sampleNestForms;

    public SampleForm() {
      // 在创建实例时初始化嵌套Bean的字段
      sampleNestForms = new ArrayList<>();
    }

父Bean与嵌套Bean为1对1的情况
  考虑是否可以将Bean不嵌套而做成扁平的Bean。
  如果由于连接端的要求无法实现，则需要确保对嵌套Bean的验证能够可靠执行。

  .. code-block:: java
  
    // 将嵌套Bean作为验证目标
    @Valid
    private SampleNestForm sampleNestForm;

    public SampleForm() {
      // 在创建实例时初始化嵌套Bean的字段
      sampleNestForm = new SampleNestForm();
    }


.. _bean_validation-web_application:

进行Web应用的用户输入值校验
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Web应用的用户输入值校验使用 :ref:`inject_form_interceptor` 进行。
详情请参考 :ref:`inject_form_interceptor` 。

要在 :ref:`inject_form_interceptor` 中使用Bean Validation，需要在组件设置文件中进行定义。
如下例所示，将 :java:extdoc:`BeanValidationStrategy <nablarch.common.web.validator.BeanValidationStrategy>` 以 ``validationStrategy`` 的名称进行组件定义。

.. code-block:: xml

  <component name="validationStrategy" class="nablarch.common.web.validator.BeanValidationStrategy" />

.. tip::

  在BeanValidationStrategy中，验证错误的错误消息按以下顺序排序。

  * jakarta.servlet.ServletRequest#getParameterNames返回的项目名顺序
    （如果发生错误的项目不存在于请求参数中，则移动到末尾）

  请注意， ``getParameterNames`` 返回的值依赖于实现，根据使用的应用服务器不同，排序可能会改变。
  如果项目中想要更改排序，请继承BeanValidationStrategy并对应处理。


.. _bean_validation-restful_web_service:

进行RESTful Web服务的用户输入值校验
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
RESTful Web服务的用户输入值校验，通过对接收输入值的资源类的方法设置 :java:extdoc:`Valid <jakarta.validation.Valid>` 注解来进行。
详情请参考 :ref:`jaxrs_bean_validation_handler_perform_validation` 。

.. _bean_validation_onerror:


验证错误时也想从请求作用域获取请求参数
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

使用 :ref:`inject_form_interceptor`\ ，验证成功后会将验证后的表单存入请求作用域。
虽然可以使用它来引用请求参数，但有时也希望在验证错误时同样从请求作用域获取参数。


例如，使用JSTL标签（EL表达式）时，与Nablarch自定义标签不同，不能隐式地引用请求参数\ [#1]_ ，
因此需要添加如下处理。

* 首先使用Nablarch标签 ``<n:set>`` 将请求参数的值存入变量
* 使用隐式对象 ``param`` 访问请求参数  

以下展示使用前者的 ``<n:set>`` 的示例。
  
.. code-block:: jsp
                  
   <%-- 将请求参数的值赋值给变量，以便JSTL(EL表达式)也能引用 --%>
   <n:set var="quantity" name="form.quantity" />
   <c:if test="${quantity >= 100}">
     <%-- 数量在100以上的情况... --%>


这种情况下，通过将 :java:extdoc:`BeanValidationStrategy <nablarch.common.web.validator.BeanValidationStrategy>`\
的属性 ``copyBeanToRequestScopeOnError`` 设置为 ``true`` ，\
即使在验证错误时，也可以将复制了请求参数的Bean存入请求作用域。
以下展示设置示例。

.. code-block:: xml

  <component name="validationStrategy" class="nablarch.common.web.validator.BeanValidationStrategy">
    <!-- 验证错误时复制值到请求作用域 -->
    <property name="copyBeanToRequestScopeOnError" value="true"/>
  </component>

请求作用域中，以 ``@InjectForm`` 的 ``name`` 指定的键名存储Bean\
（与\ :ref:`inject_form_interceptor`\ 的正常动作相同）。

  
启用此功能后，上述JSP可以如下描述。


.. code-block:: jsp
                
   <%-- 通过请求作用域，JSTL(EL表达式)也能引用请求参数的值 --%>
   <c:if test="${form.quantity >= 100}">
     <%-- 数量在100以上的情况... --%>

.. [#1] 关于Nablarch自定义标签的动作，请参考 :ref:`tag-access_rule` 。
     
.. _bean_validation-property_name:


想在验证错误消息中包含项目名
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
在Jakarta Bean Validation的规范中，不能在消息中包含项目名，
但根据需求等有时希望在消息中包含项目名。
因此，Nablarch即使在Jakarta Bean Validation中使用时，也提供了在消息中包含发生错误的项目名的功能。

以下展示使用方法。

组件设置文件
  设置生成包含项目名的消息的消息转换器的工厂类。
  组件名设置为 ``constraintViolationConverterFactory`` ，
  类名设置为 :java:extdoc:`ItemNamedConstraintViolationConverterFactory <nablarch.core.validation.ee.ItemNamedConstraintViolationConverterFactory>` 。

  .. code-block:: xml

    <component name="constraintViolationConverterFactory"
        class="nablarch.core.validation.ee.ItemNamedConstraintViolationConverterFactory" />

验证目标的Form
  .. code-block:: java
  
    package sample;

    public class User {

      @Required
      private String name;

      @Required
      private String address;
    }

项目名的定义
  项目名作为消息定义。
  项目名的消息ID为验证目标类的完全限定名 + "." + 项目的属性名。

  上述Form类的情况下， ``sample.User`` 为完全限定名，有 ``name`` 和 ``address`` 两个属性。
  项目名的定义需要如下 ``sample.User.name`` 和 ``sample.User.address`` 。

  另外，如果未定义项目名，则消息中不会附加项目名。

  .. code-block:: properties

    # Required的消息
    nablarch.core.validation.ee.Required.message=请输入。

    # 项目名的定义
    sample.User.name = 用户名
    sample.User.address = 地址

生成的消息
  生成的消息是在错误消息的开头附加项目名。
  项目名用 ``[`` 、 ``]`` 包围。

  .. code-block:: text

    [用户名]请输入。
    [地址]请输入。
  
.. tip::
  如果要更改向消息添加项目名的方法，请参考 :java:extdoc:`ItemNamedConstraintViolationConverterFactory <nablarch.core.validation.ee.ItemNamedConstraintViolationConverterFactory>` 
  ，在项目侧添加实现进行对应。

.. _bean_validation-execute_explicitly:

显式执行验证
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
通常，验证按照 `进行Web应用的用户输入值校验`_ 或 `进行RESTful Web服务的用户输入值校验`_ 中介绍的方法进行，但在想要处理验证错误等情况下，可能无法使用这些方法。

这种情况下，可以使用 :java:extdoc:`ValidatorUtil#validate <nablarch.core.validation.ee.ValidatorUtil.validate(java.lang.Object)>` 显式执行验证。

  .. code-block:: java

    // 显式执行验证
    ValidatorUtil.validate(form);

如果发生验证错误，将抛出 :java:extdoc:`ApplicationException <nablarch.core.message.ApplicationException>` 。

Web应用的情况
    在Web应用中显式执行验证时，需要将请求参数中包含的输入值转换为Bean。

    要转换为Bean，需要在验证前从 :java:extdoc:`HttpRequest#getParamMap <nablarch.fw.web.HttpRequest.getParamMap()>` 获取请求参数。
    但是，如果应用开发人员可以自由处理验证前的输入值，则可能在未经验证的情况下执行业务逻辑，在某些情况下可能导致故障。

    因此，获取请求参数的 :java:extdoc:`HttpRequest#getParamMap <nablarch.fw.web.HttpRequest.getParamMap()>` 是作为面向架构师的公开API，禁止在Action类中使用。

    如果需要在Web应用中显式执行验证，建议作为共通基础设施部件创建如下的工具类。

  .. code-block:: java

    public final class ProjectValidatorUtil {
        // 其他处理省略

        /**
         * 从HTTP请求生成Bean，并进行Bean Validation。
         *
         * @param beanClass 要生成的Bean类
         * @param request HTTP请求
         * @return  属性已注册的Bean对象
         */
        public static <T> T validate(Class<T> beanClass, HttpRequest request) {
            T bean = BeanUtil.createAndCopy(beanClass, request.getParamMap());
            ValidatorUtil.validate(bean);
            return bean;
        }
    }



.. _bean_validation-execute:

想在验证错误时执行任意处理
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
如果希望在验证错误时执行任意处理，通过显式执行验证可以处理验证错误时发生的异常，因此可以执行任意处理。

以下展示使用 `显式执行验证`_ 的实现示例中的工具类的实现示例。

  .. code-block:: java

    @OnError(type = ApplicationException.class, path = "/WEB-INF/view/project/create.jsp")
    public HttpResponse create(HttpRequest request, ExecutionContext context) {

        ProjectForm form;

        try {
            // 显式执行验证，获取验证后的表单
            form = ProjectValidatorUtil.validate(ProjectForm.class, request);
        } catch (ApplicationException e) {
            // 验证错误时执行任意处理
            // ...

            // 抛出ApplicationException，跳转到@OnError注解指定的跳转目标
            throw e;
        }

        // 以下省略
    }


.. _bean_validation-use_groups:

想使用Bean Validation的组功能
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
在Jakarta Bean Validation的规范中，如果在验证执行时指定组，则可以将验证使用的规则限制为特定的组。
Nablarch也提供了可以在Bean Validation中指定组的API。

以下展示使用示例。

验证目标的Form
  .. code-block:: java

    public class SampleForm {

        @SystemChar(charsetDef = "数字", groups = {Default.class, Test1.class})
        String id;

        @SystemChar.List({
                @SystemChar(charsetDef = "全角文字") // 未指定组时，视为属于Default组
                @SystemChar(charsetDef = "半角英数", groups = Test1.class),
        })
        String name;

        public interface Test1 {}
    }


执行验证的处理
  .. code-block:: java

    SampleForm form = new SampleForm();

    ...

    // 未指定组时，使用属于Default组的规则进行验证。
    ValidatorUtil.validate(form);

    // 指定组时，使用属于指定组的规则进行验证。
    ValidatorUtil.validateWithGroup(form, SampleForm.Test1.class);


API详情请参考 :java:extdoc:`ValidatorUtil#validateWithGroup <nablarch.core.validation.ee.ValidatorUtil.validateWithGroup(java.lang.Object,java.lang.Class...)>`
及 :java:extdoc:`ValidatorUtil#validateProperty <nablarch.core.validation.ee.ValidatorUtil.validateProperty(java.lang.Object,java.lang.String,java.lang.Class...)>` 。

.. tip::
   通过使用组功能切换验证规则，可以使一个表单类在多个画面或API中共用。
   但是，Nablarch不推荐这样的使用方法（请参考 :ref:`表单类按html的form单位创建 <application_design-form_html>` 及 :ref:`表单类按API单位创建 <rest-application_design-form_html>` ）。
   如果以共用表单类为目的使用组功能，请在项目侧充分讨论后再使用。


扩展示例
---------------
想添加项目特有的注解和验证逻辑
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
如果 :ref:`bean_validation-validator` 中记载的验证器无法满足需求，
请在项目侧添加注解及验证逻辑。

关于实现方法等详情，请参考以下链接及Nablarch的实现。

* `Hibernate Validator(外部站点、英文) <https://hibernate.org/validator/>`_
* `Jakarta Bean Validation(外部站点、英文) <https://jakarta.ee/specifications/bean-validation/>`_
