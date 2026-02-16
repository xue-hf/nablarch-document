.. _mail_sender_thymeleaf_adaptor:

E-mail Thymeleaf适配器
==================================================

.. contents:: 目录
  :depth: 3
  :local:

提供用于使用 `Thymeleaf(外部网站) <https://www.thymeleaf.org>`_ 进行定型邮件发送处理的适配器。

模块列表
--------------------------------------------------
.. code-block:: xml

  <!-- E-mail Thymeleaf适配器 -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-mail-sender-thymeleaf-adaptor</artifactId>
  </dependency>
  
.. tip::

  使用Thymeleaf版本3.1.1.RELEASE进行测试。
  要更改版本时，请在项目侧进行测试确认无问题。

进行使用E-mail Thymeleaf适配器的设置
----------------------------------------------------------------------------------------------------
要使用本适配器，需要在组件配置文件中将 :java:extdoc:`ThymeleafMailProcessor<nablarch.integration.mail.thymeleaf.ThymeleafMailProcessor>` 设置到 :java:extdoc:`MailRequester<nablarch.common.mail.MailRequester>` 。

``ThymeleafMailProcessor`` 需要设置Thymeleaf提供的 ``TemplateEngine`` 。

以下显示组件配置文件的设置示例。

.. code-block:: xml

  <component name="templateEngine" class="org.thymeleaf.TemplateEngine" autowireType="None">
    <property name="templateResolver">
      <component class="org.thymeleaf.templateresolver.ClassLoaderTemplateResolver" autowireType="None">
        <property name="prefix" value="com/example/template/" />
      </component>
    </property>
  </component>

  <component name="templateEngineMailProcessor"
    class="nablarch.integration.mail.thymeleaf.ThymeleafMailProcessor" autowireType="None">
    <property name="templateEngine" ref="templateEngine" />
  </component>

  <!-- 邮件发送请求API -->
  <component name="mailRequester" class="nablarch.common.mail.MailRequester">
    <property name="templateEngineMailProcessor" ref="templateEngineMailProcessor"/>
    <!-- 其他设置省略 -->
  </component>

创建邮件模板
--------------------------------------------------
使用Thymeleaf的定型邮件处理中，主题和正文记述在一个模板中。

主题和正文以称为分隔符的行分割。
默认的分隔符是 ``---`` （3个半角连字符）。

以下显示模板示例。

.. code-block:: none

 [(${title})]关于[(${option})]
 ---
 [(${title})]已以申请编号[(${requestId})]申请。
 [(${approver})]请尽快批准[(${title})]。[(${option})]

更详细的主题和正文分割规则请参阅 :java:extdoc:`TemplateEngineProcessedResult#valueOf<nablarch.common.mail.TemplateEngineProcessedResult.valueOf(java.lang.String)>` 。

模板文件的放置位置根据 ``TemplateEngine`` 的设置而异。
例如，在前一节显示的设置示例中，模板文件从类路径加载。
此外，由于 ``ClassLoaderTemplateResolver`` 的 ``prefix`` 设置为 ``com/example/template/`` ，
因此需要将模板文件放置在类路径上的 ``com/example/template/`` 目录中。

注册邮件发送请求
--------------------------------------------------
只需注册定型邮件的发送请求即可。
请参阅 :ref:`mail-request` 。
