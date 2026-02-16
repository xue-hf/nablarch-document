.. _mail_sender_freemarker_adaptor:

E-mail FreeMarker适配器
==================================================

.. contents:: 目录
  :depth: 3
  :local:

提供用于使用 `FreeMarker(外部网站) <https://freemarker.apache.org/>`_ 进行定型邮件发送处理的适配器。

模块列表
--------------------------------------------------
.. code-block:: xml

  <!-- E-mail FreeMarker适配器 -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-mail-sender-freemarker-adaptor</artifactId>
  </dependency>
  
.. tip::

  使用FreeMarker版本2.3.27-incubating进行测试。
  要更改版本时，请在项目侧进行测试确认无问题。

进行使用E-mail FreeMarker适配器的设置
----------------------------------------------------------------------------------------------------
要使用本适配器，需要在组件配置文件中将 :java:extdoc:`FreeMarkerMailProcessor<nablarch.integration.mail.freemarker.FreeMarkerMailProcessor>` 设置到 :java:extdoc:`MailRequester<nablarch.common.mail.MailRequester>` 。

``FreeMarkerMailProcessor`` 需要设置FreeMarker提供的 ``Configuration`` 。
由于以下原因，建议创建 :java:extdoc:`ComponentFactory<nablarch.core.repository.di.ComponentFactory>` 的实现类来设置组件。

* ``Configuration`` 的默认构造函数已被弃用
* 对 ``Configuration`` 的设置使用Java代码比使用组件配置文件更容易

以下显示创建 ``Configuration`` 的 ``ComponentFactory`` 实现类的示例。

.. code-block:: java

  package com.example;

  import freemarker.template.Configuration;
  import nablarch.core.repository.di.ComponentFactory;

  public class ConfigurationFactory implements ComponentFactory<Configuration> {

      private String basePackagePath;
      private String encoding;

      @Override
      public Configuration createObject() {
          Configuration cfg = new Configuration(Configuration.getVersion());
          ClassLoader classLoader = getClass().getClassLoader();
          cfg.setClassLoaderForTemplateLoading(classLoader, basePackagePath);
          cfg.setDefaultEncoding(encoding);
          //根据需要向Configuration进行其他设置
          return cfg;
      }

      public void setBasePackagePath(String basePackagePath) {
          this.basePackagePath = basePackagePath;
      }

      public void setEncoding(String encoding) {
          this.encoding = encoding;
      }
  }

以下显示使用此 ``ConfigurationFactory`` 的组件配置文件设置示例。

.. code-block:: xml

  <component name="templateEngineMailProcessor"
             class="nablarch.integration.mail.freemarker.FreeMarkerMailProcessor" autowireType="None">
    <property name="configuration">
      <component class="com.example.ConfigurationFactory">
        <property name="basePackagePath" value="com/example/template/"/>
        <property name="encoding" value="UTF-8"/>
      </component>
    </property>
  </component>

  <!-- 邮件发送请求API -->
  <component name="mailRequester" class="nablarch.common.mail.MailRequester">
    <property name="templateEngineMailProcessor" ref="templateEngineMailProcessor"/>
    <!-- 其他设置省略 -->
  </component>

创建邮件模板
--------------------------------------------------
使用FreeMarker的定型邮件处理中，主题和正文记述在一个模板中。

主题和正文以称为分隔符的行分割。
默认的分隔符是 ``---`` （3个半角连字符）。

以下显示模板示例。

.. code-block:: none

 ${title}关于${option}
 ---
 ${title}已以申请编号${requestId}申请。
 ${approver}请尽快批准${title}。${option}

更详细的主题和正文分割规则请参阅 :java:extdoc:`TemplateEngineProcessedResult#valueOf<nablarch.common.mail.TemplateEngineProcessedResult.valueOf(java.lang.String)>` 。

模板文件的放置位置根据 ``Configuration`` 的设置而异。
例如，在前一节显示的设置示例中，模板文件从类路径加载。
此外，由于 ``basePackagePath`` 设置为 ``com/example/template/`` ，
因此需要将模板文件放置在类路径上的 ``com/example/template/`` 目录中。

注册邮件发送请求
--------------------------------------------------
只需注册定型邮件的发送请求即可。
请参阅 :ref:`mail-request` 。
