.. _mail_sender_velocity_adaptor:

E-mail Velocity适配器
==================================================

.. contents:: 目录
  :depth: 3
  :local:

提供用于使用 `Velocity(外部网站) <https://velocity.apache.org/>`_ 进行定型邮件发送处理的适配器。

模块列表
--------------------------------------------------
.. code-block:: xml

  <!-- E-mail Velocity适配器 -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-mail-sender-velocity-adaptor</artifactId>
  </dependency>
  
.. tip::

  使用Velocity版本2.0进行测试。
  要更改版本时，请在项目侧进行测试确认无问题。

进行使用E-mail Velocity适配器的设置
----------------------------------------------------------------------------------------------------
要使用本适配器，需要在组件配置文件中将 :java:extdoc:`VelocityMailProcessor<nablarch.integration.mail.velocity.VelocityMailProcessor>` 设置到 :java:extdoc:`MailRequester<nablarch.common.mail.MailRequester>` 。

``VelocityMailProcessor`` 需要设置Velocity提供的 ``VelocityEngine`` 。
由于以下原因，建议创建 :java:extdoc:`ComponentFactory<nablarch.core.repository.di.ComponentFactory>` 的实现类来设置组件。

* 对 ``VelocityEngine`` 的设置使用Java代码比使用组件配置文件更容易
* 设置 ``VelocityEngine`` 后需要调用 ``init`` 方法

以下显示创建 ``VelocityEngine`` 的 ``ComponentFactory`` 实现类的示例。

.. code-block:: java

  package com.example;

  import org.apache.velocity.app.VelocityEngine;
  import org.apache.velocity.runtime.resource.loader.ClasspathResourceLoader;

  import nablarch.core.repository.di.ComponentFactory;

  public class VelocityEngineFactory implements ComponentFactory<VelocityEngine> {

      @Override
      public VelocityEngine createObject() {
          VelocityEngine velocityEngine = new VelocityEngine();

          velocityEngine.setProperty("resource.loader", "classloader");
          velocityEngine.setProperty("classloader.resource.loader.class",
                  ClasspathResourceLoader.class.getName());

          //根据需要向VelocityEngine进行其他设置

          velocityEngine.init();

          return velocityEngine;
      }
  }

以下显示使用此 ``ConfigurationFactory`` 的组件配置文件设置示例。

.. code-block:: xml

  <component name="templateEngineMailProcessor"
             class="nablarch.integration.mail.velocity.VelocityMailProcessor" autowireType="None">
    <property name="velocityEngine">
      <component class="com.example.VelocityEngineFactory"/>
    </property>
  </component>

  <!-- 邮件发送请求API -->
  <component name="mailRequester" class="nablarch.common.mail.MailRequester">
    <property name="templateEngineMailProcessor" ref="templateEngineMailProcessor"/>
    <!-- 其他设置省略 -->
  </component>

创建邮件模板
--------------------------------------------------
使用Velocity的定型邮件处理中，主题和正文记述在一个模板中。

主题和正文以称为分隔符的行分割。
默认的分隔符是 ``---`` （3个半角连字符）。

以下显示模板示例。

.. code-block:: none

 $title关于$option
 ---
 $title已以申请编号$requestId申请。
 $approver请尽快批准$title。$option

更详细的主题和正文分割规则请参阅 :java:extdoc:`TemplateEngineProcessedResult#valueOf<nablarch.common.mail.TemplateEngineProcessedResult.valueOf(java.lang.String)>` 。

模板文件的放置位置根据 ``VelocityEngine`` 的设置而异。
例如，在前一节显示的设置示例中，模板文件从类路径加载，因此需要将模板文件放置在类路径上的目录中。

注册邮件发送请求
--------------------------------------------------
只需注册定型邮件的发送请求即可。
请参阅 :ref:`mail-request` 。
