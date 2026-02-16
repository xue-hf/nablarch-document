.. _nablarch_openapi_generator:

====================================================
Nablarch OpenAPI Generator
====================================================

.. contents:: 目录
  :depth: 3
  :local:

工具概要
-------------

Nablarch OpenAPI Generator是 `OpenAPI(外部网站，英语) <https://www.openapis.org/>`_ 文档生成源代码的 `OpenAPI Generator(外部网站，英语) <https://openapi-generator.tech/>`_ 的Generator实现。

本工具提供用于Nablarch RESTful Web服务的Generator，通过嵌入到 `OpenAPI Generator的Maven插件(外部网站，英语) <https://openapi-generator.tech/docs/plugins>`_ 中执行来生成源代码。

使用生成的源代码，可以容易地实现遵循OpenAPI文档中定义的REST API接口的Action类。

前提条件
---------

* 已创建作为Nablarch RESTful Web服务源代码生成源的OpenAPI文档
* OpenAPI文档使用 `OpenAPI 3.0.3(外部网站，英语) <https://spec.openapis.org/oas/v3.0.3.html>`_ 规格记述

动作概要
--------

本工具通过将OpenAPI文档指定为源代码生成源的输入，从OpenAPI文档生成以下源代码。

* 基于路径和操作定义的资源(Action)接口
* 基于模式定义的、对应请求和响应的模型

.. tip::

  由于OpenAPI Generator的规格， ``.openapi-generator-ignore`` 、 ``.openapi-generator/FILES`` 、 ``.openapi-generator/VERSION`` 会生成到 :ref:`NablarchOpenApiGeneratorConfiguration` 的 ``output`` 指定的目录下，但这些不使用。

运用方法
--------

本工具设想以下运用方法。

#. 根据Web服务的设计信息创建OpenAPI文档
#. 创建Nablarch RESTful Web服务项目，作为Maven插件进行OpenAPI Generator和本工具的设置
#. 构建项目，生成资源(Action)接口和模型
#. 使用生成的资源(Action)接口和模型，实现Nablarch RESTful Web服务

.. tip::

  本工具设想在OpenAPI文档修正时反复执行。由于Nablarch RESTful Web服务的Action类是通过实现生成的资源(Action)接口创建的，因此即使再次执行本工具的自动生成，Action类中实现的内容也不会丢失。

.. tip::

  OpenAPI Generator及本工具设想作为Maven插件执行，但也可以使用CLI。详情请参阅 :ref:`NablarchOpenApiGeneratorAsCli` 。

使用方法
---------

Maven插件的设置
===========================

以下显示使用本工具所需的最低限度OpenAPI Generator的Maven插件设置示例。

.. code-block:: xml

      <plugin>
        <groupId>org.openapitools</groupId>
        <artifactId>openapi-generator-maven-plugin</artifactId>
        <version>7.10.0</version>
        <dependencies>
          <!-- 将本工具的模块添加到依赖关系 -->
          <dependency>
            <groupId>com.nablarch.tool</groupId>
            <artifactId>nablarch-openapi-generator</artifactId>
            <version>1.0.0</version>
          </dependency>
        </dependencies>
        <executions>
          <execution>
            <goals>
              <goal>generate</goal>
            </goals>
            <configuration>
              <!-- 指定OpenAPI文档的文件路径 -->
              <inputSpec>${project.basedir}/src/main/resources/openapi.yaml</inputSpec>
              <generatorName>nablarch-jaxrs</generatorName>
              <configOptions>
                <sourceFolder>src/gen/java</sourceFolder>
                <apiPackage>com.example.api</apiPackage>
                <modelPackage>com.example.model</modelPackage>

                <!-- 其他，指定本工具的选项 -->
              </configOptions>
            </configuration>
          </execution>
        </executions>
      </plugin>

本工具通过以下依赖关系提供。

.. code-block:: xml

          <dependency>
            <groupId>com.nablarch.tool</groupId>
            <artifactId>nablarch-openapi-generator</artifactId>
            <version>1.0.0</version>
          </dependency>

使用OpenAPI Generator的Maven插件时，最低限度需要的设置是指定作为源代码生成对象的OpenAPI文档的 ``inputSpec`` 和指定使用哪个Generator的 ``generatorName`` 这2个。

通过将 ``generatorName`` 指定为 ``nablarch-jaxrs`` ，可以使用本工具。

关于其他设置项目请参阅 :ref:`NablarchOpenApiGeneratorConfiguration` 。

.. tip::

  本工具使用OpenAPI Generator 7.10.0进行开发和测试。
  要更改OpenAPI Generator的版本时，请在项目侧进行测试确认无问题。

执行方法
========

本工具可以在Maven的compile目标中执行。

.. code-block:: text

  mvn compile

另外，如果显式设置了 :ref:`NablarchOpenApiGeneratorConfiguration` 的 ``sourceFolder`` ， ``mvn compile`` 时会将生成的源代码包含在设置Maven插件的项目的编译对象中。

此动作由OpenAPI Generator的Maven插件执行。

输出目标
========

OpenAPI Generator的Maven插件的默认设置中，生成的源代码输出到 ``target/generated-sources/openapi/src/gen/java`` 。  

要更改输出目标时请参阅 :ref:`NablarchOpenApiGeneratorConfiguration` 的 ``output`` 和 ``sourceFolder`` 。

.. _NablarchOpenApiGeneratorConfiguration:

Generator的设置项目
===========================

以下显示OpenAPI Generator的Maven插件的主要设置项目。这些作为 ``configuration`` 标签内直属的标签指定。

==================  =========================================================  ==========  ===============================
项目名               设置内容                                                    必需/任意   默认值
==================  =========================================================  ==========  ===============================
``inputSpec``       指定作为输入的OpenAPI文档的文件路径。                       必需        无
``generatorName``   指定生成源代码的Generator名称。|br|                         必需        无
                    本工具中指定为 ``nablarch-jarxrs`` 。
``output``          指定源代码的生成目标目录。                                  任意        ``generated-sources/openapi``
==================  =========================================================  ==========  ===============================

以下显示本工具的设置项目。全部为任意项目，这些在 ``configOptions`` 标签内指定。

==================================== ======================================================================================================= =====================================================================
项目名                               设置内容                                                                                                默认值
==================================== ======================================================================================================= =====================================================================
``apiPackage``                       指定生成的资源(Action)接口的包。|br|                                                                   ``org.openapitools.api``
                                     
``modelPackage``                     指定生成的模型的包。                                                                                    ``org.openapitools.model``
``hideGenerationTimestamp``          用 ``Generated`` 注解标注时是否赋予 ``date`` 属性。|br|                                                 ``false``
                                     默认会输出生成源代码的日期时间。
``sourceFolder``                     指定源代码的生成目标目录。 |br|                                                                         ``src/gen/java``
                                     解释为相对于OpenAPI Generator的Maven插件设置的 ``output`` 的 |br|
                                     相对路径。|br|
                                     指定此项目后，本工具生成的源代码将被 |br|
                                     包含在 ``mvn compile`` 时的编译对象中。
``useTags``                          将生成的资源(Action)接口的单位 |br|                                                                    ``false``
                                     设为不是路径而是端点上附带的标签的单位。|br|
                                     另外，端点上附有多个标签时第一个 |br|
                                     标签有效。
``serializableModel``                在生成的模型上实现 ``java.io.Serializable`` |br|                                                        ``false``
                                     接口。
``generateBuilders``                 为模型生成Builder类。                                                                                   ``false``
``useBeanValidation``                从OpenAPI文档的验证定义，|br|                                                                           ``false``
                                     生成使用 :ref:`bean_validation` 功能进行 |br|
                                     验证的源代码。
``additionalModelTypeAnnotations``   为生成的模型的类声明添加额外的注解。|br|                                                               无
                                     要添加多个注解时用 ``;`` 分隔指定。
``additionalEnumTypeAnnotations``    为生成的enum型添加额外的注解。|br|
                                     要添加多个注解时用 ``;`` 分隔指定。                                       无
``primitivePropertiesAsString``      将模型的原始数据类型的属性全部 |br|                                                                     ``false``
                                     输出为 ``String`` 。
``supportConsumesMediaTypes``        指定生成的资源(Action)接口接受的请求 |br|                                                              ``application/json,multipart/form-data``
                                     媒体类型，用 ``,`` 分隔。
``supportProducesMediaTypes``        指定生成的资源(Action)接口作为响应 |br|                                                                 ``application/json``
                                     的媒体类型，用 ``,`` 分隔。
==================================== ======================================================================================================= =====================================================================

生成使用Bean Validation的源代码
==================================================

要生成使用 :ref:`bean_validation` 的源代码时，将 ``useBeanValidation`` 的值设置为 ``true`` 。

以下显示设置示例。

.. code-block:: xml

            <configuration>
              <!-- 指定OpenAPI文档的文件路径 -->
              <inputSpec>${project.basedir}/src/main/resources/openapi.yaml</inputSpec>
              <generatorName>nablarch-jaxrs</generatorName>
              <configOptions>
                <sourceFolder>src/gen/java</sourceFolder>
                <apiPackage>com.example.api</apiPackage>
                <modelPackage>com.example.model</modelPackage>

                <!-- 生成使用Bean Validation的源代码 -->
                <useBeanValidation>true</useBeanValidation>
              </configOptions>
            </configuration>

``useBeanValidation`` 的默认值是 ``false`` ，因此默认情况下不标注使用 :ref:`bean_validation` 功能的注解。

这是因为OpenAPI规格中规定的验证定义往往无法满足业务需求，而且也无法定义相关验证。

包含此类观点，关于生成使用验证功能的源代码时的规格和运用上的注意事项，详细记载在 :ref:`openapi_property_to_bean_validation` 中，请参阅。

.. _NablarchOpenApiGeneratorAsCli:

作为CLI执行
===========================

本工具主要设想作为Maven插件使用，但也可以作为CLI使用。此处作为补充介绍CLI的执行方法。

作为CLI执行时，需要下载 `OpenAPI Generator 7.10.0的JAR文件(外部网站) <https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/7.10.0/openapi-generator-cli-7.10.0.jar>`_ 和 `本工具的JAR文件(外部网站) <https://repo1.maven.org/maven2/com/nablarch/tool/nablarch-openapi-generator/1.0.0/nablarch-openapi-generator-1.0.0.jar>`_ ，然后用java命令执行。执行示例如下。

.. code-block:: text

  java -cp openapi-generator-cli-7.10.0.jar:nablarch-openapi-generator-1.0.0.jar org.openapitools.codegen.OpenAPIGenerator generate --generator-name nablarch-jaxrs --input-spec openapi.yaml --output out --additional-properties=apiPackage=com.example.api,modelPackage=com.example.model,useBeanValidation=true,hideGenerationTimestamp=true

``--generator-name`` 请指定 ``nablarch-jaxrs`` 。 :ref:`NablarchOpenApiGeneratorConfiguration` 中OpenAPI Generator的设置项目也可以在OpenAPI Generator的CLI中指定。详情请参阅以下命令的结果。

.. code-block:: text

  java -jar openapi-generator-cli-7.10.0.jar help generate

.. tip::

  OpenAPI Generator的设置项目会变成 ``--generator-name`` 这样的连字符分隔形式。

:ref:`NablarchOpenApiGeneratorConfiguration` 中本工具固有的设置项目，用 ``--additional-properties`` 以 ``key=value`` 的形式指定。要指定多个时用 ``,`` 分隔。

.. tip::

  本工具固有的设置项目，像 ``--additional-properties=hideGenerationTimestamp=true`` 这样直接在 ``--additional-properties=`` 后面指定项目名。


源代码生成规格
------------------------

以下记载本工具从OpenAPI文档生成源代码的规格。

.. important::

  由于Nablarch RESTful Web服务并不支持Jakarta RESTful Web Services提供的所有注解，此处记载内容以外的OpenAPI文档内容可能不会反映到生成的源代码中，请注意。

  关于Nablarch RESTful Web服务支持的注解，请参阅 :ref:`restful_web_service_architecture` 以及路由适配器的 :ref:`router_adaptor_path_annotation` 。

资源(Action)接口生成规格
===============================================

此处记载资源(Action)接口的生成规格。由于会按照 :ref:`rest_feature_details-method_signature` 的形式生成，也请参阅此处。

以下显示资源(Action)接口的生成单位和类型定义相关的规格。

* 根据OpenAPI文档中定义的路径和操作信息生成。
* 生成为Java接口。
* 资源(Action)接口的生成单位可从以下选择。

  * 默认情况下为OpenAPI文档路径的第一层汇总的内容。
  * ``useTags`` 设为 ``true`` 时为操作上附带的标签的单位。

* 资源(Action)接口的声明上标注 ``Path`` 注解。
* 标注 ``Generated`` 注解。

以下显示资源(Action)接口的方法生成相关的规格。

**方法声明上标注的注解**

================== ====================================================================================================
注解                说明
================== ====================================================================================================
``GET``            操作的HTTP方法为GET时标注。
``POST``           操作的HTTP方法为POST时标注。
``PUT``            操作的HTTP方法为PUT时标注。
``DELETE``         操作的HTTP方法为DELETE时标注。
``PATCH``          操作的HTTP方法为PATCH时标注。
``HEAD``           操作的HTTP方法为HEAD时标注。
``OPTIONS``        操作的HTTP方法为OPTIONS时标注。
``Consumes``       请求的Content-Type存在时标注。
``Produces``       响应的Content-Type存在且不是 ``type: string`` 和 ``format: binary`` 时标注。
``Valid``          请求主体存在且 ``useBeanValidation`` 为 ``true`` 时标注。
================== ====================================================================================================

.. tip::

  ``type: string`` 且 ``format: binary`` 表示文件下载，此时Content-Type使用 :java:extdoc:`HttpResponse#setContentType<nablarch.fw.web.HttpResponse.setContentType(java.lang.String)>` 设置。

**方法名的生成规格**

* 使用OpenAPI文档的 ``operationId`` 元素的值作为方法名。
* 未指定 ``operationId`` 元素时，组合路径的值和HTTP方法名生成方法名。

**方法参数的生成规格**

====================================================================== =============================================================================================================================
方法参数的类型                                                         说明
====================================================================== =============================================================================================================================
请求模型的类型                                                         接收请求主体且请求Content-Type不是多部分时，设置对应模型类型的参数。
:java:extdoc:`JaxRsHttpRequest <nablarch.fw.jaxrs.JaxRsHttpRequest>`   始终生成并设置到参数。
:java:extdoc:`ExecutionContext <nablarch.fw.ExecutionContext>`         始终生成并设置到参数。
====================================================================== =============================================================================================================================

.. tip::

  * RESTful Web服务不支持Jakarta RESTful Web Services规定的 ``PathParam`` 、 ``QueryParam`` 等，因此 ``parameters`` 的定义不会反映到方法参数中。请从 :java:extdoc:`JaxRsHttpRequest <nablarch.fw.jaxrs.JaxRsHttpRequest>` 获取这些信息。
  * 请求的Content-Type为 ``multipart/form-data`` 时，不会生成请求模型类型的参数。上传的文件请从 :java:extdoc:`JaxRsHttpRequest <nablarch.fw.jaxrs.JaxRsHttpRequest>` 获取。

**方法返回值的生成规格**

====================================================================== ==========================================================================================
方法返回值的类型                                                       说明
====================================================================== ==========================================================================================
:java:extdoc:`EntityResponse <nablarch.fw.jaxrs.EntityResponse>`       响应为模型时生成。类型参数中反映模型的类型。
:java:extdoc:`HttpResponse <nablarch.fw.web.HttpResponse>`             响应不是模型或HTTP状态码不是 ``200`` 时生成。
====================================================================== ==========================================================================================

模型生成规格
===============

以下显示模型的生成单位和类型定义相关的规格。

* 对定义为模式的模型生成。
* 生成为Java类。
* 标注 ``JsonTypeName`` 注解。
* 标注 ``Generated`` 注解。

以下显示模型的属性相关的生成规格。

* 生成对应于OpenAPI文档模式中定义的字段的属性。
* 为属性生成getter和setter，并标注 ``JsonProperty`` 注解。
* 生成设置属性值并返回模型自身类型的、可进行方法链的方法。
* ``useBeanValidation`` 为 ``true`` 且OpenAPI文档中有验证定义时，启用使用 :ref:`bean_validation` 的验证。
* 验证使用的注解使用Nablarch提供的 :ref:`bean_validation` 固有的和Jakarta EE标准的 :java:extdoc:`jakarta.validation.constraints` 包的。

OpenAPI文档中的数据类型和格式与Java数据类型的对应规格请参阅 :ref:`openapi_datatypes_format_to_java_datatypes` ，验证定义与验证使用的注解的对应规格请参阅 :ref:`openapi_property_to_bean_validation` 。

模型的其他生成规格如下。

* 生成 ``hashCode`` 、 ``equals`` 、 ``toString`` 方法。

生成的源代码依赖的模块
==================================================

要构建本工具生成的源代码，依赖关系中需要以下模块。

.. code-block:: xml

    <dependency>
      <groupId>com.nablarch.framework</groupId>
      <artifactId>nablarch-fw-jaxrs</artifactId>
    </dependency>
    <dependency>
       <groupId>com.nablarch.framework</groupId>
       <artifactId>nablarch-core-validation-ee</artifactId>
    </dependency>
    <dependency>
      <groupId>jakarta.ws.rs</groupId>
      <artifactId>jakarta.ws.rs-api</artifactId>
    </dependency>
    <dependency>
      <groupId>jakarta.annotation</groupId>
      <artifactId>jakarta.annotation-api</artifactId>
    </dependency>
    <dependency>
      <groupId>com.fasterxml.jackson.core</groupId>
      <artifactId>jackson-annotations</artifactId>
      <version>2.17.1</version>
    </dependency>

RESTful Web服务的空白项目中设置的依赖关系中已包含所有这些。

.. _openapi_datatypes_format_to_java_datatypes:

OpenAPI文档的数据类型及格式与Java数据类型的对应规格
===========================================================================

以下显示OpenAPI文档上定义的数据类型和格式与本工具对应的Java数据类型的对应表。

=================================== ======================================== =======================================================
OpenAPI中的数据类型( ``type`` )     OpenAPI中的格式( ``format`` )            模型属性的数据类型
=================================== ======================================== =======================================================
``integer``                                                                  ``java.lang.Integer``
``integer``                         ``int32``                                ``java.lang.Integer``
``integer``                         ``int64``                                ``java.lang.Long``
``number``                                                                   ``java.math.BigDecimal``
``number``                          ``float``                                ``java.lang.Float``
``number``                          ``double``                               ``java.lang.Double``
``boolean``                                                                  ``java.lang.Boolean``
``string``                                                                   ``java.lang.String``
``string``                          ``byte``                                 ``byte[]``
``string``                          ``date``                                 ``java.time.LocalDate``
``string``                          ``date-time``                            ``java.time.OffsetDateTime``
``string``                          ``number``                               ``java.math.BigDecimal``
``string``                          ``uuid``                                 ``java.util.UUID``
``string``                          ``uri``                                  ``java.net.URI``
``string``                                                                   enum (指定 ``enum`` 时生成对应的Enum类型)
``array``                                                                    ``java.util.List``
``array``                                                                    ``java.util.Set`` ( ``uniqueItems: true`` 时)
``object``                                                                   对应的模型类型
``object``                                                                   无对应类型时为 ``java.lang.Object``
=================================== ======================================== =======================================================

.. tip::

  * ``type: string`` 且 ``format: binary`` 仅在请求Content-Type为 ``multipart/form-data`` 时可用，在其他Content-Type或响应模型定义内使用时将中止模型生成。
  * ``type: string`` 时除上表外还有许多格式，但全部生成为 ``java.lang.String`` 。

.. _openapi_property_to_bean_validation:

OpenAPI文档的验证定义与Bean Validation的对应规格
=======================================================================

本工具中 ``useBeanValidation`` 的默认值为 ``false`` ，因此默认情况下无论OpenAPI文档的定义如何都不标注 :ref:`bean_validation` 使用的注解，但设为 ``true`` 时根据OpenAPI文档的记述内容会按照以下2个方针为属性标注注解。

* OpenAPI规格中规定的属性对应的验证
* 域验证(domain validation)

OpenAPI规格中规定的属性对应的验证
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

使用 `OpenAPI规格中规定的属性(外部网站，英语) <https://spec.openapis.org/oas/v3.0.3.html#properties>`_ 进行验证定义时，会按照以下对应表标注注解。

=================================== ======================================== ========================================== ============================================================================================================
OpenAPI中的数据类型( ``type`` )     OpenAPI中的格式( ``format`` )            OpenAPI中使用的属性                         标注的验证用注解
=================================== ======================================== ========================================== ============================================================================================================
``integer``                         (格式不限)                                ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``integer``                                                                  ``minimum`` 以及 ``maximum``               :java:extdoc:`NumberRange(min = {minimum}, max = {maximum}) <nablarch.core.validation.ee.NumberRange>`
``integer``                         ``int32``                                ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``integer``                         ``int32``                                ``minimum`` 以及 ``maximum``               :java:extdoc:`NumberRange(min = {minimum}, max = {maximum}) <nablarch.core.validation.ee.NumberRange>`
``integer``                         ``int64``                                ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``integer``                         ``int64``                                ``minimum`` 以及 ``maximum``               :java:extdoc:`NumberRange(min = {minimum}, max = {maximum}) <nablarch.core.validation.ee.NumberRange>`
``number``                          (格式不限)                                ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``number``                                                                   ``minimum`` 以及 ``maximum``               :java:extdoc:`DecimalRange(min = "{minimum}", max = "{maximum}") <nablarch.core.validation.ee.DecimalRange>`
``number``                          ``float``                                ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``number``                          ``float``                                ``minimum`` 以及 ``maximum``               :java:extdoc:`DecimalRange(min = "{minimum}", max = "{maximum}") <nablarch.core.validation.ee.DecimalRange>`
``number``                          ``double``                               ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``number``                          ``double``                               ``minimum`` 以及 ``maximum``               :java:extdoc:`DecimalRange(min = "{minimum}", max = "{maximum}") <nablarch.core.validation.ee.DecimalRange>`
``boolean``                                                                  ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``string``                          (格式不限)                                ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``string``                                                                   ``minLength`` 以及 ``maxLength``           :java:extdoc:`Length(min = {minLength}, max = {maxLength}) <nablarch.core.validation.ee.Length>`
``string``                                                                   ``pattern``                                :java:extdoc:`Pattern(regexp = "{pattern}")<jakarta.validation.constraints.Pattern>`
``array``                                                                    ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``array``                                                                    ``minItems`` 以及 ``maxItems``             :java:extdoc:`Size(min = {minItems}, max = {maxItems}) <nablarch.core.validation.ee.Size>`
=================================== ======================================== ========================================== ============================================================================================================

.. tip::

  * 不支持 ``multipleOf`` 、 ``exclusiveMinimum`` 、 ``exclusiveMaximum`` 、 ``minProperties`` 、 ``maxProperties`` 。
  * ``minimum`` 以及 ``maximum`` 、 ``minLength`` 以及 ``maxLength`` 、 ``minItems`` 以及 ``maxItems`` 即使只指定其中一方也可以。
  * Java数据类型为 ``java.math.BigDecimal`` 、 ``java.util.List`` 、 ``java.util.Set`` 或模型时标注 ``Valid`` 注解。
  * 仅 :java:extdoc:`Pattern<jakarta.validation.constraints.Pattern>` 标注Jakarta Bean Validation标准的注解，其他标注Nablarch提供的 :ref:`bean_validation` 固有的注解。

域验证(domain validation)
+++++++++++++++++++++++++++

本工具使用 `OpenAPI规格的扩展属性(外部网站，英语) <https://spec.openapis.org/oas/v3.0.3.html#specification-extensions>`_ 来支持OpenAPI规格无法表达的 :ref:`bean_validation-domain_validation` 。

扩展属性中使用 ``x-nablarch-domain`` ，值中指定域名。

.. code-block:: yaml

        propertyName:
          type: string
          x-nablarch-domain: "domainName"

将 ``useBeanValidation`` 指定为 ``true`` 生成源代码时，会在目标属性上标注 :java:extdoc:`Domain("{domainName}") <nablarch.core.validation.ee.Domain>` 。

另外，由于域验证可以包含各种验证定义，如果检测到可能存在冲突的验证定义将中止源代码生成。这是因为如果在域中已包含相同的验证规则时又进行指定，会导致验证重复执行。

具体来说，对指定了 ``x-nablarch-domain`` 的属性，如果指定了 ``minimum`` 、 ``maximum`` 、 ``minLength`` 、 ``maxLength`` 、 ``minItems`` 、 ``maxItems`` 、 ``pattern`` 中的任何一个，将中止源代码生成。

``required`` 表示必需项，不是域侧强制要求的，因此允许并用。

验证相关的运用注意事项
========================================

记载使用本工具生成包含验证定义的源代码时的运用注意事项。

OpenAPI规格的规定范围无法满足项目单位或相关验证要求时的注意事项
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

OpenAPI规格中规定的验证仅有必需定义、长度检查、正则表达式检查，作为业务应用程序来说可能不足。

另外由于直接修改自动生成的源代码并不理想，因此即使使用域验证也无法在生成的模型中实现相关验证。

因此请注意，OpenAPI规格和本工具的覆盖范围可能无法满足验证需求而需要另行实现，结果可能导致自动生成的模型与手动实现的表单等中验证定义分散的状况。

**不在自动生成的模型中包含验证定义时的实现方法**

此处介绍将验证定义作为与自动生成的模型相同定义的表单等创建，使用 :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` 复制属性值后，显式执行验证的方法。

本工具默认不标注验证用注解是因为如前述考虑，验证定义容易分散的状况是不希望看到的。

思路与 :ref:`bean_validation-execute_explicitly` 相同，实现示例记载如下。

.. code-block:: java

  public class ProjectAction implements ProjectsApi {  // ProjectsApi是本工具生成的接口

      // 实现接口中定义的方法
      @Override
      public EntityResponse<ProjectResponse> createProject(ProjectCreateRequest projectCreateRequest, JaxRsHttpRequest jaxRsHttpRequest, ExecutionContext context) {
          // 与模型相同属性定义，并加入单项验证和相关验证的表单
          ProjectCreateForm form;

          try {
              // 在工具类内从模型复制值到表单后，显式执行验证
              form = ProjectValidatorUtil.validate(ProjectCreateForm.class, projectCreateRequest);
          } catch (ApplicationException e) {
              // 验证错误时执行任意处理
              // ...

              throw e;
          }

          // 省略

          return response;
      }
  }

  // 工具类的示例
  public final class ProjectValidatorUtil {
      // 其他处理省略

      /**
       * 从HTTP请求生成Bean，并进行验证。
       *
       * @param beanClass 要生成的Bean类
       * @param src 属性复制源对象
       * @return  属性已注册的Bean对象
       */
      public static <T> T validate(Class<T> beanClass, Object src) {
          T bean = BeanUtil.createAndCopy(beanClass, src));
          ValidatorUtil.validate(bean);
          return bean;
      }
  }

使用域验证时的注意事项
++++++++++++++++++++++++++++++++++++++++++++++++++

使用域验证可以通过为模型属性定义域来汇总验证定义，或使用OpenAPI规格不支持的验证。

但请注意，OpenAPI规格支持的验证范围也会包含在内，验证规格容易被隐藏在域侧，可能导致从OpenAPI文档看不到验证规格。

OpenAPI文档与生成的源代码的示例
---------------------------------------------------

以下记载OpenAPI文档与生成的源代码的示例。

源代码生成时本工具的设置示例如下。与示例中需要不同设置项目的示例中，也会一并记载本工具的设置示例。

.. code-block:: xml

            <configuration>
              <inputSpec>${project.basedir}/src/main/resources/openapi.yaml</inputSpec>
              <generatorName>nablarch-jaxrs</generatorName>
              <configOptions>
                <sourceFolder>src/gen/java</sourceFolder>
                <apiPackage>com.example.api</apiPackage>
                <modelPackage>com.example.model</modelPackage>
              </configOptions>
            </configuration>

另外，记载的各种示例以理解形象为目的，为摘录记载。

OpenAPI文档的路径及操作定义与源代码的生成示例
===========================================================================

OpenAPI文档示例

.. code-block:: yaml

  /projects:
    post:
      tags:
      - project
      summary: 注册项目
      description: 注册项目
      operationId: createProject
      requestBody:
        description: 项目注册信息
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ProjectCreateRequest'
      responses:
        "200":
          description: 注册的项目信息
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProjectResponse'
  /projects/{id}:
    get:
      tags:
      - project
      summary: 获取项目
      description: 指定项目ID获取项目
      operationId: findProjectById
      parameters:
      - name: id
        in: path
        description: ID
        required: true
        schema:
          type: string
      responses:
        "200":
          description: 获取的项目信息
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProjectResponse'
        "404":
          description: 未找到项目时

本工具生成的资源(Action)接口示例

.. code-block:: java

  @Path("/projects")
  @jakarta.annotation.Generated(value = "nablarch.tool.openapi.codegen.JavaNablarchJaxrsServerCodegen", date = "2024-12-10T13:54:26.470544738+09:00[Asia/Tokyo]", comments = "Generator version: 7.10.0")
  public interface ProjectsApi {
      /**
       * POST  : 注册项目
       *
       * 注册项目
       *
       * @param projectCreateRequest 项目注册信息
       * @param jaxRsHttpRequest HTTP请求
       * @param context Handler执行上下文
       * @return 注册的项目信息
       */
      @POST
      @Consumes({ "application/json" })
      @Produces({ "application/json" })
      EntityResponse<ProjectResponse> createProject(ProjectCreateRequest projectCreateRequest, JaxRsHttpRequest jaxRsHttpRequest, ExecutionContext context);

      /**
       * GET /{id} : 获取项目
       *
       * 指定项目ID获取项目
       *
       * @param jaxRsHttpRequest HTTP请求
       * @param context Handler执行上下文
       * @return 获取的项目信息
       * @return 未找到项目时
       */
      @GET
      @Path("/{id}")
      @Produces({ "application/json" })
      EntityResponse<ProjectResponse> findProjectById(JaxRsHttpRequest jaxRsHttpRequest, ExecutionContext context);

  }

OpenAPI文档的模式定义与源代码的生成示例
============================================================

OpenAPI文档示例

.. code-block:: yaml

    ProjectResponse:
      description: 项目信息
      type: object
      properties:
        id:
          format: uuid
          description: 项目ID
          type: string
        name:
          description: 项目名
          type: string
        sales:
          format: int64
          description: 销售额
          type: integer
        startDate:
          format: date
          description: 开始日
          type: string
        endDate:
          format: date
          description: 结束日
          type: string

本工具生成的模型示例

.. code-block:: java

  @JsonTypeName("ProjectResponse")
  @jakarta.annotation.Generated(value = "nablarch.tool.openapi.codegen.JavaNablarchJaxrsServerCodegen", date = "2024-12-10T13:54:26.470544738+09:00[Asia/Tokyo]", comments = "Generator version: 7.10.0")
  public class ProjectResponse   {
    private UUID id;
    private String name;
    private Long sales;
    private LocalDate startDate;
    private LocalDate endDate;
   
      /**
       * 项目ID
       */
      public ProjectResponse id(UUID id) {
          this.id = id;
          return this;
      }
   
      
      @JsonProperty("id")
      public UUID getId() {
          return id;
      }
   
      @JsonProperty("id")
      public void setId(UUID id) {
          this.id = id;
      }
   
      /**
       * 项目名
       */
      public ProjectResponse name(String name) {
          this.name = name;
          return this;
      }
   
      
      @JsonProperty("name")
      public String getName() {
          return name;
      }
   
      @JsonProperty("name")
      public void setName(String name) {
          this.name = name;
      }
   
      /**
       * 销售额
       */
      public ProjectResponse sales(Long sales) {
          this.sales = sales;
          return this;
      }
   
      
      @JsonProperty("sales")
      public Long getSales() {
          return sales;
      }
   
      @JsonProperty("sales")
      public void setSales(Long sales) {
          this.sales = sales;
      }
   
      /**
       * 开始日
       */
      public ProjectResponse startDate(LocalDate startDate) {
          this.startDate = startDate;
          return this;
      }
   
      
      @JsonProperty("startDate")
      public LocalDate getStartDate() {
          return startDate;
      }
   
      @JsonProperty("startDate")
      public void setStartDate(LocalDate startDate) {
          this.startDate = startDate;
      }
   
      /**
       * 结束日
       */
      public ProjectResponse endDate(LocalDate endDate) {
          this.endDate = endDate;
          return this;
      }
   
      
      @JsonProperty("endDate")
      public LocalDate getEndDate() {
          return endDate;
      }
   
      @JsonProperty("endDate")
      public void setEndDate(LocalDate endDate) {
          this.endDate = endDate;
      }

      // hashCode、equals、toString等省略
  }

生成使用Bean Validation的源代码的示例
====================================================================================================

OpenAPI文档示例

.. code-block:: yaml

  ## 路径及操作
  /projects:
    post:
      tags:
      - project
      summary: 创建项目
      description: 创建项目
      operationId: createProject
      requestBody:
        description: 项目注册信息
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ProjectCreateRequest'
      responses:
        "200":
          description: project created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProjectResponse'

    ## 模式
    ProjectCreateRequest:
      description: 项目创建请求
      required:
      - projectName
      - projectType
      - startDate
      type: object
      properties:
        projectName:
          description: 项目名
          maxLength: 100
          minLength: 1
          type: string
        projectType:
          description: 项目类型
          maxLength: 100
          minLength: 1
          type: string
        startDate:
          format: date
          description: 开始日
          type: string
        endDate:
          format: date
          description: 结束日
          type: string

本工具的设置示例

.. code-block:: xml

            <configuration>
              <inputSpec>${project.basedir}/src/main/resources/openapi.yaml</inputSpec>
              <generatorName>nablarch-jaxrs</generatorName>
              <configOptions>
                <sourceFolder>src/gen/java</sourceFolder>
                <apiPackage>com.example.api</apiPackage>
                <modelPackage>com.example.model</modelPackage>
                <!-- 使用Bean Validation时请指定useBeanValidation为true -->
                <useBeanValidation>true</useBeanValidation>
              </configOptions>
            </configuration>

本工具生成的资源(Action)接口示例

.. code-block:: java

  @Path("/projects")
  @jakarta.annotation.Generated(value = "nablarch.tool.openapi.codegen.JavaNablarchJaxrsServerCodegen", date = "2024-12-10T13:54:26.470544738+09:00[Asia/Tokyo]", comments = "Generator version: 7.10.0")
  public interface ProjectsApi {
      /**
       * POST  : 创建项目
       *
       * 创建项目
       *
       * @param projectCreateRequest 项目注册信息
       * @param jaxRsHttpRequest HTTP请求
       * @param context Handler执行上下文
       * @return project created
       */
      @POST
      @Consumes({ "application/json" })
      @Produces({ "application/json" })
      // HTTP主体接收请求时赋予@Valid注解
      @Valid
      EntityResponse<ProjectResponse> createProject(ProjectCreateRequest projectCreateRequest, JaxRsHttpRequest jaxRsHttpRequest, ExecutionContext context);

  }

本工具生成的模型示例

.. code-block:: java

  @JsonTypeName("ProjectCreateRequest")
  @jakarta.annotation.Generated(value = "nablarch.tool.openapi.codegen.JavaNablarchJaxrsServerCodegen", date = "2024-12-10T13:54:26.470544738+09:00[Asia/Tokyo]", comments = "Generator version: 7.10.0")
  public class ProjectCreateRequest   {
    private String projectName;
    private String projectType;
    private LocalDate startDate;
    private LocalDate endDate;
  
      /**
       * 项目名
       */
      public ProjectCreateRequest projectName(String projectName) {
          this.projectName = projectName;
          return this;
      }
  
  
      @JsonProperty("projectName")
      @Required @Length(min = 1, max = 100)
      public String getProjectName() {
          return projectName;
      }
  
      @JsonProperty("projectName")
      public void setProjectName(String projectName) {
          this.projectName = projectName;
      }
  
      /**
       * 项目类型
       */
      public ProjectCreateRequest projectType(String projectType) {
          this.projectType = projectType;
          return this;
      }
  
  
      @JsonProperty("projectType")
      @Required @Length(min = 1, max = 100)
      public String getProjectType() {
          return projectType;
      }
  
      @JsonProperty("projectType")
      public void setProjectType(String projectType) {
          this.projectType = projectType;
      }
  
      /**
       * 开始日
       */
      public ProjectCreateRequest startDate(LocalDate startDate) {
          this.startDate = startDate;
          return this;
      }
  
  
      @JsonProperty("startDate")
      @Required
      public LocalDate getStartDate() {
          return startDate;
      }
  
      @JsonProperty("startDate")
      public void setStartDate(LocalDate startDate) {
          this.startDate = startDate;
      }
  
      /**
       * 结束日
       */
      public ProjectCreateRequest endDate(LocalDate endDate) {
          this.endDate = endDate;
          return this;
      }
  
  
      @JsonProperty("endDate")
  
      public LocalDate getEndDate() {
          return endDate;
      }
  
      @JsonProperty("endDate")
      public void setEndDate(LocalDate endDate) {
          this.endDate = endDate;
      }
