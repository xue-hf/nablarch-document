.. _jaxrs_adaptor:

Jakarta RESTful Web Services适配器
===========================================

.. contents:: 目录
  :depth: 3
  :local:

.. tip::
  本功能在Nablarch5之前的名称为"JAX-RS 适配器"。
  但随着Java EE移交至Eclipse Foundation后规格名称变更，现更名为"Jakarta RESTful Web Services适配器"。

  变更的只有名称，功能上没有差异。

  关于Nablarch6中其他名称变更的功能，请参阅 :ref:`renamed_features_in_nablarch_6` 。

提供用于 :ref:`RESTful Web服务 <restful_web_service>` 的以下适配器。

* 使用 `Jackson(外部网站，英语) <https://github.com/FasterXML/jackson>`_ 转换JSON的适配器
* 在 `Jersey(外部网站，英语) <https://eclipse-ee4j.github.io/jersey/>`_ 中使用 :ref:`RESTful Web服务 <restful_web_service>` 的适配器
* 在 `RESTEasy(外部网站，英语) <https://resteasy.dev/>`_ 中使用 :ref:`RESTful Web服务 <restful_web_service>` 的适配器

模块列表
--------------------------------------------------
.. code-block:: xml

  <!-- 使用jackson适配器时 -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-jackson-adaptor</artifactId>
  </dependency>

  <!-- 使用Jersey适配器时 -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-jersey-adaptor</artifactId>
  </dependency>

  <!-- 使用RESTEasy适配器时 -->  
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-resteasy-adaptor</artifactId>
  </dependency>
  
.. tip::

  使用Jackson版本2.17.1进行测试。
  要更改版本时，请在项目侧进行测试确认无问题。
  

.. tip::

  由于Jackson1系库的漏洞修复已停止，从Nablarch5u16开始废止了对Jackson1系的支持。
  如果使用Jackson1系，请迁移到Jackson2系。

  【参考信息】

  * https://jvndb.jvn.jp/ja/contents/2019/JVNDB-2019-012258.html
  * https://github.com/advisories/GHSA-r6j9-8759-g62w
  
   
在Jersey环境下使用RESTful Web服务
--------------------------------------------------
当Web应用服务器捆绑的 `Jakarta RESTful Web Services(外部网站，英语) <https://jakarta.ee/specifications/restful-ws/>`_ 的实现为
`Jersey(外部网站，英语) <https://eclipse-ee4j.github.io/jersey/>`_ 时，使用Jersey适配器。

以下显示Jersey适配器的应用方法。

对 :java:extdoc:`JaxRsMethodBinderFactory#handlerList <nablarch.fw.jaxrs.JaxRsMethodBinderFactory.setHandlerList(java.util.List)>`
进行工厂注入，注入构建Jersey专用处理程序的工厂类(:java:extdoc:`JerseyJaxRsHandlerListFactory <nablarch.integration.jaxrs.jersey.JerseyJaxRsHandlerListFactory>`)。
这样将自动设置以下Jersey专用的处理程序构成。

* :ref:`body_convert_handler` 的设置(将设置以下转换器)

  * JSON转换器设置 :java:extdoc:`Jackson2BodyConverter <nablarch.integration.jaxrs.jackson.Jackson2BodyConverter>` 。
  * XML转换器设置 :java:extdoc:`JaxbBodyConverter <nablarch.fw.jaxrs.JaxbBodyConverter>` 。
  * application/x-www-form-urlencoded转换器设置 :java:extdoc:`FormUrlEncodedConverter <nablarch.fw.jaxrs.FormUrlEncodedConverter>` 。
  * multipart/form-data转换器设置 :java:extdoc:`MultipartFormDataBodyConverter <nablarch.fw.jaxrs.MultipartFormDataBodyConverter>` 。

.. tip::

  为了使用Date and Time API，JSON转换器添加了 `jackson-modules-java8(外部网站，英语) <https://github.com/FasterXML/jackson-modules-java8>`_ 中包含的Java 8 Date/time模块并进行设置。

* :ref:`jaxrs_bean_validation_handler`

.. code-block:: xml

  <component name="packageMapping" class="nablarch.integration.router.RoutesMapping">
    <property name="methodBinderFactory">
      <component class="nablarch.fw.jaxrs.JaxRsMethodBinderFactory">
        <property name="handlerList">
          <!-- 向handlerList属性工厂注入Jersey的处理程序队列 -->
          <component class="nablarch.integration.jaxrs.jersey.JerseyJaxRsHandlerListFactory"/>
        </property>
      </component>
    </property>

    <!-- 上述以外的属性省略 -->
  </component>

.. tip::
  如果使用的Web应用服务器未捆绑 `Jackson(外部网站，英语) <https://github.com/FasterXML/jackson>`_ ，
  请将Jackson模块与应用模块一起部署。
  
在RESTEasy环境下使用RESTful Web服务
--------------------------------------------------
当Web应用服务器捆绑的 `Jakarta RESTful Web Services(外部网站，英语) <https://jakarta.ee/specifications/restful-ws/>`_ 的实现为
`RESTEasy(外部网站，英语) <https://resteasy.dev/>`_ 时，使用RESTEasy适配器。

以下显示RESTEasy适配器的应用方法。

对 :java:extdoc:`JaxRsMethodBinderFactory#handlerList <nablarch.fw.jaxrs.JaxRsMethodBinderFactory.setHandlerList(java.util.List)>`
进行工厂注入，注入构建RESTEasy专用处理程序的工厂类(:java:extdoc:`ResteasyJaxRsHandlerListFactory <nablarch.integration.jaxrs.resteasy.ResteasyJaxRsHandlerListFactory>`)。
这样将自动设置以下RESTEasy专用的处理程序构成。

* :ref:`body_convert_handler` 的设置(将设置以下转换器)

  * JSON转换器设置 :java:extdoc:`Jackson2BodyConverter <nablarch.integration.jaxrs.jackson.Jackson2BodyConverter>` 。
  * XML转换器设置 :java:extdoc:`JaxbBodyConverter <nablarch.fw.jaxrs.JaxbBodyConverter>` 。
  * application/x-www-form-urlencoded转换器设置 :java:extdoc:`FormUrlEncodedConverter <nablarch.fw.jaxrs.FormUrlEncodedConverter>` 。
  * multipart/form-data转换器设置 :java:extdoc:`MultipartFormDataBodyConverter <nablarch.fw.jaxrs.MultipartFormDataBodyConverter>` 。

.. tip::

  为了使用Date and Time API，JSON转换器添加了 `jackson-modules-java8(外部网站，英语) <https://github.com/FasterXML/jackson-modules-java8>`_ 中包含的Java 8 Date/time模块并进行设置。

* :ref:`jaxrs_bean_validation_handler`

.. code-block:: xml

  <component name="packageMapping" class="nablarch.integration.router.RoutesMapping">
    <property name="methodBinderFactory">
      <component class="nablarch.fw.jaxrs.JaxRsMethodBinderFactory">
        <property name="handlerList">
          <!-- 向handlerList属性工厂注入RESTEasy的处理程序队列 -->
          <component class="nablarch.integration.jaxrs.resteasy.ResteasyJaxRsHandlerListFactory"/>
        </property>
      </component>
    </property>

    <!-- 上述以外的属性省略 -->
  </component>

.. tip::
  如果使用的Web应用服务器未捆绑 `Jackson(外部网站，英语) <https://github.com/FasterXML/jackson>`_ ，
  请将Jackson模块与应用模块一起部署。

想要更改（添加）在各环境下使用的正文转换器
----------------------------------------------------------------------
当项目中需要对应的MIME增加时，需要实现 :java:extdoc:`JaxRsHandlerListFactory <nablarch.fw.jaxrs.JaxRsHandlerListFactory>` 来对应。

实现方法可参考本适配器
(:java:extdoc:`JerseyJaxRsHandlerListFactory <nablarch.integration.jaxrs.jersey.JerseyJaxRsHandlerListFactory>` 、 :java:extdoc:`ResteasyJaxRsHandlerListFactory <nablarch.integration.jaxrs.resteasy.ResteasyJaxRsHandlerListFactory>`)。



