.. _message:

消息管理
======================

.. contents:: 目录
  :depth: 3
  :local:

消息是指画面的固定文本(项目标题等)或错误消息。

如果没有国际化需求，画面的固定文本直接嵌入JSP也没有问题。

.. tip::

  消息不要轻易通用化，尽量单独定义。

  如果轻易进行通用化，可能会发生以下问题。

  例如，因为其他业务的消息看起来可以用而使用了该消息。
  如果其他业务由于规格变更更改了该消息，就会在与该消息使用位置无关的地方显示消息。

功能概述
--------------------------

可以指定消息的定义位置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
消息可以在数据库或属性文件中管理。默认为属性文件管理。

将属性文件设为默认的理由如下。

使用属性文件管理时，可以方便地进行消息的添加、更改和确认。
例如，添加消息时，比起向数据库insert，向属性文件添加行要容易得多。

属性文件管理的详情请参照以下。

* :ref:`message-property_unit`
* :ref:`message-property_definition`

.. tip::
 无论消息的定义位置如何，本功能都不提供在应用程序运行中更新消息的功能。
 要更新消息时，需要重启应用程序。

可以格式化消息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
消息使用 :java:extdoc:`java.text.MessageFormat` 的扩展功能进行格式化。
如果想在运行时嵌入持有的值到消息中，请按照 :ref:`message-format-spec` 定义模式字符串。

模块列表
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core</artifactId>
  </dependency>
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-message</artifactId>
  </dependency>

  <!-- 仅在数据库中管理消息时需要 -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-jdbc</artifactId>
  </dependency>

使用方法
---------------------------

.. _message-property_unit:

属性文件的创建单位
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
按应用程序单位创建。
即使是1个系统，如果有面向公司内部和面向消费者的应用程序，请分别创建属性文件。

按应用程序单位创建，可以将消息的影响范围限定在应用程序内。
（可以防止常见的「没想到那个应用程序也在用」导致的故障）

示例
  面向消费者的应用程序
    consumer/main/resources/messages.properties

  面向员工的应用程序
    intra/main/resources/messages.properties

.. _message-property_definition:

在属性文件中定义消息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
默认设置中，属性文件的路径为 ``classpath:messages.properties`` 。

消息使用 :java:extdoc:`java.util.Properties` 加载。
另外，由于Nablarch6假设使用Java17以上，因此使用 **UTF-8** 创建即可，不需要Unicode转换(native2ascii)。

属性文件示例
  .. code-block:: properties

    label.user.register.title=用户注册画面
    errors.login.alreadyExist=输入的登录ID已注册。请输入其他登录ID。
    errors.login=登录失败。登录ID或密码错误。
    errors.compare.date={0}请输入晚于{1}的日期。
    success.delete.project=项目删除已完成。
    success.update.project=项目更新已完成。

.. _message-multi_lang:

多语言化支持
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
进行消息的多语言化时，需要准备各语言的属性文件，并将支持的语言设置到 :java:extdoc:`PropertiesStringResourceLoader.locales <nablarch.core.message.PropertiesStringResourceLoader.setLocales(java.util.List)>` 中。
另外，对应默认区域的语言可以不添加到支持的语言中。

.. important:: 

  默认区域通过 :java:extdoc:`PropertiesStringResourceLoader.defaultLocale  <nablarch.core.message.PropertiesStringResourceLoader.setDefaultLocale(java.lang.String)>` (默认语言)设置。如果不设置，默认区域将采用 :java:extdoc:`Locale.getDefault().getLanguage() <java.util.Locale.getLanguage()>` 的值。
  
  :java:extdoc:`Locale.getDefault().getLanguage() <java.util.Locale.getLanguage()>` 的值会根据OS设置而变化，如果将此值作为默认区域，可能会因执行环境不同而值发生变化，从而导致故障。请务必设置默认语言。

获取消息时使用哪种语言由 :java:extdoc:`ThreadContext#getLanguage <nablarch.core.ThreadContext.getLanguage()>` 返回的区域决定。
如果无法从 :java:extdoc:`ThreadContext#getLanguage <nablarch.core.ThreadContext.getLanguage()>` 获取区域，则使用 :java:extdoc:`Locale.getDefault() <java.util.Locale.getDefault()>` 。

  
设置到PropertiesStringResourceLoader的语言
  作为支持的语言，设置 ``en`` 、 ``zh`` 、 ``de`` 时的示例如下。

  .. code-block:: xml

    <component class="nablarch.core.cache.BasicStaticDataCache" name="messageCache">
      <property name="loader">
        <!-- 多语言化的PropertiesStringResourceLoader定义 -->
        <component class="nablarch.core.message.PropertiesStringResourceLoader">
          <!-- 支持的语言 -->
          <property name="locales">
            <list>
              <value>en</value>
              <value>zh</value>
              <value>de</value>
            </list>
          </property>

          <!-- 默认的语言 -->
          <property name="defaultLocale" value="ja" />
        </component>
      </property>
    </component>

    <component name="stringResourceHolder" class="nablarch.core.message.StringResourceHolder">
      <!-- 设置拥有多语言化PropertiesStringResourceLoader的BasicStaticDataCache -->
      <property name="stringResourceCache" ref="messageCache" />
    </component>

    <component name="initializer" 
               class="nablarch.core.repository.initialization.BasicApplicationInitializer">
      <property name="initializeList">
        <list>
          <!-- 将BasicStaticDataCache添加到初始化对象 -->
          <component-ref name="messageCache" />
        </list>
      </property>
    </component>


创建各语言的属性文件
  展示创建对应上述 :java:extdoc:`PropertiesStringResourceLoader <nablarch.core.message.PropertiesStringResourceLoader>` 中设置的支持语言的属性文件示例。

  创建对应 :java:extdoc:`PropertiesStringResourceLoader <nablarch.core.message.PropertiesStringResourceLoader>` 中设置的语言的属性文件。
  文件名为 **messages_语言.properties** 。

  对应默认区域的属性文件，不包含语言，作为 **messages.properties** 创建。
  如果不存在 **messages.properties** ，将作为错误结束处理，请注意。

  .. code-block:: none

    main/resources/messages.properties       # 对应默认语言的文件
                   messages_en.properties    # 对应en的文件
                   messages_zh.properties    # 对应zh的文件
                   messages_de.properties    # 对应de的文件

抛出持有消息的业务异常
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
展示抛出持有属性文件中设置的消息的业务异常( :java:extdoc:`ApplicationException <nablarch.core.message.ApplicationException>` )的示例。

要获取属性文件中设置的消息，使用 :java:extdoc:`MessageUtil <nablarch.core.message.MessageUtil>` 类。
使用从 :java:extdoc:`MessageUtil <nablarch.core.message.MessageUtil>` 获取的 :java:extdoc:`Message <nablarch.core.message.Message>` 生成并抛出业务异常( :java:extdoc:`ApplicationException <nablarch.core.message.ApplicationException>` )。


属性文件
  .. code-block:: properties

    errors.login.alreadyExist=输入的登录ID已注册。请输入其他登录ID。

实现示例
  .. code-block:: java

    Message message = MessageUtil.createMessage(MessageLevel.ERROR, "errors.login.alreadyExist");

    throw new ApplicationException(message);

.. _message-format-spec:

使用嵌入字符
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
支持 :java:extdoc:`java.text.MessageFormat` 格式的嵌入字符。
如果在要嵌入消息的值中仅指定 :java:extdoc:`Map <java.util.Map>` ，
则使用不使用 :java:extdoc:`java.text.MessageFormat` 而基于 :java:extdoc:`Map <java.util.Map>` 的键值嵌入值的扩展功能。

使用嵌入字符时，在消息中使用模式字符，获取消息时指定嵌入字符。

嵌入字符中使用 :java:extdoc:`Map <java.util.Map>` 以外时
  属性文件
    按照 :java:extdoc:`java.text.MessageFormat` 的规格定义消息。

    .. code-block:: properties

      success.upload.project=已注册{0}件项目。


  实现示例
    `projects.size()` 返回 **5** 时，获取的消息为「已注册5件项目。」。

    .. code-block:: java

      MessageUtil.createMessage(MessageLevel.INFO, "success.upload.project", projects.size());

嵌入字符中仅使用 :java:extdoc:`Map <java.util.Map>` 时
  属性文件
    嵌入字符部分，使用 ``{`` 、 ``}`` 包围 :java:extdoc:`Map <java.util.Map>` 的键名来定义。

    .. code-block:: properties

      success.upload.project=已注册{projectCount}件项目。

  实现示例
    获取消息时在嵌入字符中指定 :java:extdoc:`Map <java.util.Map>` 。

    `projects.size()` 返回 **5** 时，获取的消息为「已注册5件项目。」。

    .. code-block:: java

      Map<String, Object> options = new HashMap<>();
      options.put("projectCount", projects.size());

      MessageUtil.createMessage(MessageLevel.INFO, "success.upload.project", options);

    .. important:: 

      可指定为嵌入字符的值仅限 :java:extdoc:`Map <java.util.Map>` 。
      如果指定多个 :java:extdoc:`Map <java.util.Map>` ，或与 :java:extdoc:`Map <java.util.Map>` 以外的值一起指定，
      将使用 :java:extdoc:`java.text.MessageFormat` 进行值嵌入处理。

想更改消息的格式化方法时，请参考 :ref:`message-change_formatter` 进行应对。

从消息获取画面的固定文本
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
想在画面的固定文本中输出消息值时，使用自定义标签库的 `message` 标签。

`message` 标签的详细使用方法请参考 :ref:`tag-write_message` 。

属性文件
  .. code-block:: properties

    login.title=登录

JSP
  .. code-block:: jsp

    <div class="title-nav">
      <span><n:message messageId="login.title" /></span>
    </div>

画面显示结果
  属性文件中定义的消息作为固定文本显示。

  .. image:: images/message/jsp_title.png

.. _message-level:

区分使用消息级别
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
通过区分使用消息级别，可以在画面显示时切换样式。
样式的切换可以通过使用自定义标签库的 :ref:`errors <tag-write_error_errors_tag>` 标签来实现。

.. important::

  使用消息级别和自定义标签进行样式更改存在以下问题。

  * 自定义标签库输出的DOM结构有约束，与一般CSS框架的兼容性差
  * 消息级别只有3种，无法进行更细致的分类
  * 不能在JSP以外的模板引擎中使用
  
  因此，建议不使用 :ref:`使用errors标签根据消息级别切换样式<message-level_with_tag>` ，而是使用以下实现方法。

  服务器端
    在服务器端构建消息字符串，设置到请求作用域中。
    生成消息时消息级别是必需的，因此指定INFO级别即可。

    .. code-block:: java

      context.setRequestScopedVar("message", 
          MessageUtil.createMessage(MessageLevel.INFO, "login.message").formatMessage());

  View
    在View(JSP等)中输出设置到请求作用域中的消息。
    使用JSP时，使用 :ref:`write <tag-write_tag>` 标签输出设置到请求作用域中的消息。

    .. code-block:: jsp
        
       <div class="alert alert-success" role="alert">
         <n:write name="message" />
       </div>

.. _message-level_with_tag:

使用errors标签根据消息级别切换样式示例
  消息级别有 `INFO` 、 `WARN` 、 `ERROR` 3种，
  定义在 :java:extdoc:`MessageLevel <nablarch.core.message.MessageLevel>` 中。

  使用errors标签时，根据消息级别会应用以下css类。
  `errors` 标签的详细使用方法请参考 :ref:`tag-write_error` 。

  :INFO: nablarch_info
  :WARN: nablarch_warn
  :ERROR: nablarch_error

  .. tip::

    :doc:`验证功能 <validation>` 抛出的业务异常( :java:extdoc:`ApplicationException <nablarch.core.message.ApplicationException>` )所持有的消息，
    全部为 `ERROR` 级别。


  属性文件
    .. code-block:: properties

      info=信息
      warn=警告
      error=错误

  样式表
    定义对应消息级别的样式。

    .. code-block:: css

      .nablarch_info {
        color: #3333BB;
      }

      .nablarch_warn {
        color: #EA8128;
      }

      .nablarch_error {
        color: #ff0000;
      }

  action class
    `errors` 标签输出的消息，使用 :java:extdoc:`WebUtil.notifyMessages <nablarch.common.web.WebUtil.notifyMessages(nablarch.fw.ExecutionContext,nablarch.core.message.Message...)>` 存储到请求作用域中。

    .. code-block:: java

      WebUtil.notifyMessages(context, MessageUtil.createMessage(MessageLevel.INFO, "info"));
      WebUtil.notifyMessages(context, MessageUtil.createMessage(MessageLevel.WARN, "warn"));
      WebUtil.notifyMessages(context, MessageUtil.createMessage(MessageLevel.ERROR, "error"));

  JSP
    使用 `errors` 标签显示存储在 :java:extdoc:`WebUtil <nablarch.common.web.WebUtil>` 中的消息。

    .. code-block:: jsp

      <n:errors />

  画面显示结果
    可以看到根据消息级别切换了样式。

    .. image:: images/message/message_level.png


扩展示例
--------------------------------------------------
更改属性文件名或存储位置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:java:extdoc:`PropertiesStringResourceLoader <nablarch.core.message.PropertiesStringResourceLoader>` 中准备了用于更改文件名和目录路径的属性。
想更改默认构成时，请使用这些属性进行更改。



在数据库中管理消息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
要在数据库中管理消息，需要使用 :java:extdoc:`BasicStringResourceLoader <nablarch.core.message.BasicStringResourceLoader>` 加载消息。

以下展示使用在数据库中管理的消息所需的设置示例。

.. code-block:: xml

  <!-- 从数据库加载消息的组件 -->
  <component name="stringResourceLoader" class="nablarch.core.message.BasicStringResourceLoader">
    <property name="dbManager" ref="defaultDbManager"/>
    <property name="tableName" value="MESSAGE"/>
    <property name="idColumnName" value="ID"/>
    <property name="langColumnName" value="LANG"/>
    <property name="valueColumnName" value="MESSAGE"/>
  </component>

  <!-- 缓存加载消息的组件 -->
  <component name="stringResourceCache" class="nablarch.core.cache.BasicStaticDataCache">
    <!-- 加载器中指定从数据库加载消息的类 -->
    <property name="loader" ref="stringResourceLoader"/>
    <!-- 启动时批量加载 -->
    <property name="loadOnStartup" value="true"/>
  </component>

  <!--
  保持消息原始字符串资源的组件
  组件名请设为stringResourceHolder
  -->
  <component name="stringResourceHolder" class="nablarch.core.message.StringResourceHolder">
    <!-- 指定缓存消息的组件 -->
    <property name="stringResourceCache" ref="stringResourceCache"/>
  </component>

.. _message-change_formatter:

更改消息的格式化方法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
消息的格式化方法可以通过创建 :java:extdoc:`MessageFormatter <nablarch.core.message.MessageFormatter>` 的实现类并进行组件定义来更改。

以下展示示例。

MessageFormatter的实现类
  .. code-block:: java

    package sample;

    import nablarch.core.message.MessageFormatter;

    public class SampleMessageFormatter implements MessageFormatter {

        @Override
        public String format(final String template, final Object[] options) {
            return String.format(template, options);
        }
    }

组件设置文件
  将组件名设为 ``messageFormatter`` ，设置 `MessageFormatter` 的实现类。

  .. code-block:: xml

    <!-- 将组件名定义为messageFormatter。 -->
    <component name="messageFormatter" class="sample.SampleMessageFormatter" />

另外，作为 `MessageFormatter` 的实现提供以下类。

:java:extdoc:`BasicMessageFormatter <nablarch.core.message.BasicMessageFormatter>`:
  按照 :ref:`嵌入字符的规格 <message-format-spec>` 格式化消息。
  如果未进行 `MessageFormatter` 实现类的组件定义，则使用本类。
:java:extdoc:`JavaMessageFormatBaseMessageFormatter <nablarch.core.message.JavaMessageFormatBaseMessageFormatter>`:
  使用 :java:extdoc:`MessageFormat <java.text.MessageFormat>` 格式化消息。
