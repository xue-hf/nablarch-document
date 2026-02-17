.. _nablarch_openapi_generator:

====================================================
Nablarch OpenAPI Generator
====================================================

.. contents:: 目录
  :depth: 3
  :local:

工具概述
-------------

Nablarch OpenAPI Generator是 `OpenAPI(外部站点、英文) <https://www.openapis.org/>`_ 文档生成源代码的 `OpenAPI Generator(外部站点、英文) <https://openapi-generator.tech/>`_ 的Generator实现。

本工具提供用于Nablarch RESTful Web服务的Generator，通过嵌入到 `OpenAPI Generator的Maven插件(外部站点、英文) <https://openapi-generator.tech/docs/plugins>`_ 中执行来生成源代码。

使用生成的源代码，可以更容易地实现遵循OpenAPI文档中定义的REST API接口的Action类。

前提条件
---------

* 已创建作为Nablarch RESTful Web服务源代码生成源的OpenAPI文档
* OpenAPI文档使用 `OpenAPI 3.0.3(外部站点、英文) <https://spec.openapis.org/oas/v3.0.3.html>`_ 规范编写

动作概述
--------

本工具通过将源代码生成源的OpenAPI文档作为输入指定，从OpenAPI文档生成以下源代码。

* 基于路径和操作定义的资源(Action)接口
* 基于模式定义的、与请求和响应对应的模型

.. tip::

  根据OpenAPI Generator的规范， ``.openapi-generator-ignore`` 、 ``.openapi-generator/FILES`` 、 ``.openapi-generator/VERSION`` 会生成到 :ref:`NablarchOpenApiGeneratorConfiguration` 的 ``output`` 指定的目录下，但这些不使用。

使用方法
--------

本工具设想以下使用方法。

#. 基于Web服务的设计信息创建OpenAPI文档
#. 创建Nablarch RESTful Web服务的项目，作为Maven插件配置OpenAPI Generator及本工具
#. 构建项目，生成资源(Action)接口和模型
#. 使用生成的资源(Action)接口和模型，实现Nablarch RESTful Web服务

.. tip::

  本工具设想会随着OpenAPI文档的修改而反复执行。由于Nablarch RESTful Web服务的Action类是通过实现生成的资源(Action)接口来创建的，因此即使再次执行本工具的自动生成，Action类中实现的内容也不会丢失。

.. tip::

  OpenAPI Generator及本工具设想以Maven插件形式执行，但也可以通过CLI使用。详情请参考 :ref:`NablarchOpenApiGeneratorAsCli` 。

使用方式
---------

Maven插件的配置
===========================

以下展示使用本工具所需的最低限度的OpenAPI Generator的Maven插件配置示例。

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

                <!-- 指定其他本工具的选项 -->
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

使用OpenAPI Generator的Maven插件时，最低限度需要的配置是指定作为源代码生成源的OpenAPI文档的 ``inputSpec`` 和指定使用哪个Generator的 ``generatorName`` 这2个。

通过将 ``generatorName`` 指定为 ``nablarch-jaxrs`` ，可以使用本工具。

其他配置项目请参考 :ref:`NablarchOpenApiGeneratorConfiguration` 。

.. tip::

  本工具使用OpenAPI Generator 7.10.0进行开发和测试。
  如果更改OpenAPI Generator的版本，请在项目侧进行测试并确认没有问题。

执行方法
========

本工具可以在Maven的compile目标中执行。

.. code-block:: text

  mvn compile

另外，如果显式设置了 :ref:`NablarchOpenApiGeneratorConfiguration` 的 ``sourceFolder`` ，则在 ``mvn compile`` 时会将生成的源代码包含在配置了Maven插件的项目的编译目标中。

此动作由OpenAPI Generator的Maven插件执行。

输出位置
========

在OpenAPI Generator的Maven插件的默认配置中，生成的源代码输出到 ``target/generated-sources/openapi/src/gen/java`` 。

如果要更改输出位置，请参考 :ref:`NablarchOpenApiGeneratorConfiguration` 的 ``output`` 和 ``sourceFolder`` 。

.. _NablarchOpenApiGeneratorConfiguration:

Generator的配置项目
===========================

以下展示OpenAPI Generator的Maven插件的主要配置项目。这些作为 ``configuration`` 标签内直接下的标签指定。

==================  =========================================================  ==========  ===============================
项目名              设置内容                                                   必需/任意   默认值
==================  =========================================================  ==========  ===============================
``inputSpec``       指定输入的OpenAPI文档的文件路径。                          必需        无
``generatorName``   指定生成源代码的Generator的名称。 |br|                     必需        无
                    本工具中指定为 ``nablarch-jarxrs`` 。
``output``          指定源代码的生成目标目录。                                 任意        ``generated-sources/openapi``
==================  =========================================================  ==========  ===============================

以下展示本工具的配置项目。全部为任意项目，这些在 ``configOptions`` 标签内指定。

==================================== ======================================================================================================= =====================================================================
项目名                               设置内容                                                                                                默认值
==================================== ======================================================================================================= =====================================================================
``apiPackage``                       指定生成的资源(Action)接口的包。                                                                         ``org.openapitools.api``
``modelPackage``                     指定生成的模型的包。                                                                                    ``org.openapitools.model``
``hideGenerationTimestamp``          在 ``Generated`` 注解中是否赋予 ``date`` 属性。 |br|                                                    ``false``
                                     默认会输出生成源代码的日期时间。
``sourceFolder``                     指定源代码的生成目标目录。 |br|                                                                         ``src/gen/java``
                                     作为OpenAPI Generator的Maven插件设置的 ``output`` 的 |br|
                                     相对路径解释。 |br|
                                     指定此项目后，本工具生成的源代码会在 |br|
                                     ``mvn compile`` 时被包含在编译目标中。
``useTags``                          将生成的资源(Action)接口的单位 |br|                                                                     ``false``
                                     设为不是路径而是端点上附加的标签的单位。 |br|
                                     另外，如果端点上附加了多个标签，则第一个 |br|
                                     标签有效。
``serializableModel``                在生成的模型中实现 ``java.io.Serializable`` |br|                                                        ``false``
                                     接口。
``generateBuilders``                 生成针对模型的Builder类。                                                                               ``false``
``useBeanValidation``                从OpenAPI文档的验证定义中，|br|                                                                         ``false``
                                     生成使用 :ref:`bean_validation` 功能进行 |br|
                                     验证的源代码。
``additionalModelTypeAnnotations``   在生成的模型的类声明中附加额外的注解。 |br|                                                               无
                                     添加多个注解时用 ``;`` 分隔指定。
``additionalEnumTypeAnnotations``    在生成的enum类型中附加额外的注解。 |br|
                                     添加多个注解时用 ``;`` 分隔指定。                                                                         无
``primitivePropertiesAsString``      将模型的原始数据类型的属性全部 |br|                                                                     ``false``
                                     作为 ``String`` 输出。
``supportConsumesMediaTypes``        指定生成的资源(Action)接口接受 |br|                                                                     ``application/json,multipart/form-data``
                                     请求的媒体类型，用 ``,`` 分隔。
``supportProducesMediaTypes``        指定生成的资源(Action)接口作为 |br|                                                                     ``application/json``
                                     响应的媒体类型，用 ``,`` 分隔。
==================================== ======================================================================================================= =====================================================================

生成使用Bean Validation的源代码
==================================================

要生成使用 :ref:`bean_validation` 的源代码时，将 ``useBeanValidation`` 的值设置为 ``true`` 。

以下展示设置示例。

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

``useBeanValidation`` 的默认值是 ``false`` ，因此默认情况下不会附加使用 :ref:`bean_validation` 功能的注解。

这是因为OpenAPI规范中规定的验证定义往往无法满足业务需求，而且也无法定义相关验证。

考虑到这些观点，关于生成使用验证功能的源代码时的规格和运用上的注意事项，在 :ref:`openapi_property_to_bean_validation` 中有详细记载，请参考。

.. _NablarchOpenApiGeneratorAsCli:

作为CLI执行
===========================

本工具主要设想作为Maven插件使用，但也可以作为CLI使用。这里作为补充介绍CLI的执行方法。

要作为CLI执行，需要下载 `OpenAPI Generator 7.10.0的JAR文件(外部站点) <https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/7.10.0/openapi-generator-cli-7.10.0.jar>`_ 和 `本工具的JAR文件(外部站点) <https://repo1.maven.org/maven2/com/nablarch/tool/nablarch-openapi-generator/1.0.0/nablarch-openapi-generator-1.0.0.jar>`_ ，然后用java命令执行。以下展示执行示例。

.. code-block:: text

  java -cp openapi-generator-cli-7.10.0.jar:nablarch-openapi-generator-1.0.0.jar org.openapitools.codegen.OpenAPIGenerator generate --generator-name nablarch-jaxrs --input-spec openapi.yaml --output out --additional-properties=apiPackage=com.example.api,modelPackage=com.example.model,useBeanValidation=true,hideGenerationTimestamp=true

``--generator-name`` 指定 ``nablarch-jaxrs`` 。 :ref:`NablarchOpenApiGeneratorConfiguration` 中OpenAPI Generator的配置项目也可以在OpenAPI Generator的CLI中指定。详情请参考以下命令的结果。

.. code-block:: text

  java -jar openapi-generator-cli-7.10.0.jar help generate

.. tip::

  OpenAPI Generator的配置项目会变成 ``--generator-name`` 这样的连字符分隔形式。

:ref:`NablarchOpenApiGeneratorConfiguration` 中本工具固有的配置项目，在 ``--additional-properties`` 中以 ``key=value`` 的形式指定。指定多个时用 ``,`` 分隔。

.. tip::

  本工具固有的配置项目，像 ``--additional-properties=hideGenerationTimestamp=true`` 这样，在 ``--additional-properties=`` 后直接按原样指定项目名。


源代码生成规格
------------------------

以下记载本工具基于OpenAPI文档生成源代码的规格。

.. important::

  由于Nablarch RESTful Web服务并不支持Jakarta RESTful Web Services提供的所有注解，因此请注意此处记载内容以外的OpenAPI文档内容不会反映到生成的源代码中。

  关于Nablarch RESTful Web服务支持的注解，请参考 :ref:`restful_web_service_architecture` 以及路由适配器的 :ref:`router_adaptor_path_annotation` 。

资源(Action)接口生成规格
===============================================

这里记载资源(Action)接口的生成规格。由于按照 :ref:`rest_feature_details-method_signature` 生成，因此也请参考这里。

以下展示资源(Action)接口的生成单位和类型定义相关的规格。

* 基于OpenAPI文档中定义的路径和操作信息生成。
* 生成为Java的接口。
* 资源(Action)接口的生成单位可以从以下中选择。

  * 默认情况下是OpenAPI文档中路径的第一层级汇总的结果。
  * 将 ``useTags`` 设为 ``true`` 时则是操作上附加的标签的单位。

* 在资源(Action)接口的声明中附加 ``Path`` 注解。
* 附加 ``Generated`` 注解。

以下展示资源(Action)接口的方法生成相关的规格。

**方法声明中附加的注解**

================== ====================================================================================================
注解               说明
================== ====================================================================================================
``GET``            操作的HTTP方法是GET时附加。
``POST``           操作的HTTP方法是POST时附加。
``PUT``            操作的HTTP方法是PUT时附加。
``DELETE``         操作的HTTP方法是DELETE时附加。
``PATCH``          操作的HTTP方法是PATCH时附加。
``HEAD``           操作的HTTP方法是HEAD时附加。
``OPTIONS``        操作的HTTP方法是OPTIONS时附加。
``Consumes``       有请求的内容类型时附加。
``Produces``       有响应的内容类型，且不是 ``type: string`` 和 ``format: binary`` 时附加。
``Valid``          有请求主体，且 ``useBeanValidation`` 为 ``true`` 时附加。
================== ====================================================================================================

.. tip::

  ``type: string`` 且 ``format: binary`` 表示文件下载，此时使用 :java:extdoc:`HttpResponse#setContentType<nablarch.fw.web.HttpResponse.setContentType(java.lang.String)>` 设置内容类型。

**方法名的生成规格**

* 使用OpenAPI文档的 ``operationId`` 元素的值作为方法名。
* 未指定 ``operationId`` 元素时，组合路径的值和HTTP方法名生成方法名。

**方法参数的生成规格**

====================================================================== =============================================================================================================================
方法参数的类型                                                          说明
====================================================================== =============================================================================================================================
请求模型的类型                                                          接收请求主体，且请求的内容类型不是多部分时，设置对应模型类型的参数。
:java:extdoc:`JaxRsHttpRequest <nablarch.fw.jaxrs.JaxRsHttpRequest>`   始终生成，并设置到参数中。
:java:extdoc:`ExecutionContext <nablarch.fw.ExecutionContext>`         始终生成，并设置到参数中。
====================================================================== =============================================================================================================================

.. tip::

  * RESTful Web服务不支持Jakarta RESTful Web Services中规定的 ``PathParam`` 和 ``QueryParam`` 等，因此 ``parameters`` 的定义不会反映到方法参数中。请从 :java:extdoc:`JaxRsHttpRequest <nablarch.fw.jaxrs.JaxRsHttpRequest>` 获取这些信息。
  * 请求的内容类型为 ``multipart/form-data`` 时，不会生成请求模型类型的参数。上传的文件请从 :java:extdoc:`JaxRsHttpRequest <nablarch.fw.jaxrs.JaxRsHttpRequest>` 获取。

**方法返回值的生成规格**

====================================================================== ==========================================================================================
方法返回值的类型                                                       说明
====================================================================== ==========================================================================================
:java:extdoc:`EntityResponse <nablarch.fw.jaxrs.EntityResponse>`       响应为模型时生成。型参数反映模型的类型。
:java:extdoc:`HttpResponse <nablarch.fw.web.HttpResponse>`             响应不是模型或HTTP状态码不是 ``200`` 时生成。
====================================================================== ==========================================================================================

模型生成规格
===============

以下展示模型的生成单位和类型定义相关的规格。

* 对定义为模式的模型生成。
* 生成为Java的类。
* 附加 ``JsonTypeName`` 注解。
* 附加 ``Generated`` 注解。

以下展示模型的属性相关的生成规格。

* 生成对应OpenAPI文档的模式中定义的字段的属性。
* 生成属性对应的getter和setter，并附加 ``JsonProperty`` 注解。
* 生成设置属性值并返回模型自身类型的、支持方法链的方法。
* ``useBeanValidation`` 为 ``true`` 且OpenAPI文档中有验证定义时，启用使用 :ref:`bean_validation` 的验证。
* 验证中使用的注解，使用Nablarch提供的 :ref:`bean_validation` 固有的和Jakarta EE标准的 :java:extdoc:`jakarta.validation.constraints` 包的。

OpenAPI文档中的数据类型和格式与Java数据类型的对应规格记载在 :ref:`openapi_datatypes_format_to_java_datatypes` ，验证定义与验证中使用的注解的对应规格记载在 :ref:`openapi_property_to_bean_validation` 。

以下展示模型的其他生成规格。

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

RESTful Web服务的空白项目中设置的依赖关系中包含所有这些。

.. _openapi_datatypes_format_to_java_datatypes:

OpenAPI文档的数据类型及格式与Java数据类型的对应规格
===========================================================================

对于OpenAPI文档上定义的数据类型和格式，以下展示本工具对应的Java数据类型的对应表。

=================================== ======================================== =======================================================
OpenAPI中的数据类型( ``type`` )     OpenAPI中的格式( ``format`` )            模型的属性的数据类型
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
``string``                                                                   enum (指定 ``enum`` 则生成对应的Enum类型)
``array``                                                                    ``java.util.List``
``array``                                                                    ``java.util.Set`` ( ``uniqueItems: true`` 时)
``object``                                                                   对应的模型类型
``object``                                                                   没有对应类型时为 ``java.lang.Object``
=================================== ======================================== =======================================================

.. tip::

  * ``type: string`` 且 ``format: binary`` 仅在请求的内容类型为 ``multipart/form-data`` 时可用，在其他内容类型或响应的模型定义内使用时则中止模型生成。
  * ``type: string`` 时除了上述表以外还有许多格式，但全部生成为 ``java.lang.String`` 。

.. _openapi_property_to_bean_validation:

OpenAPI文档的验证定义与Bean Validation的对应规格
=======================================================================

本工具中 ``useBeanValidation`` 的默认值为 ``false`` ，因此无论OpenAPI文档的定义如何，默认情况下都不会附加 :ref:`bean_validation` 中使用的注解，但当设为 ``true`` 时，根据OpenAPI文档的记述内容，会按以下2个方针向属性附加注解。

* OpenAPI规范中规定的属性对应的验证
* 域验证

OpenAPI规范中规定的属性对应的验证
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

使用 `OpenAPI规范中规定的属性(外部站点、英文) <https://spec.openapis.org/oas/v3.0.3.html#properties>`_ 进行验证定义时，按照以下对应表附加注解。

=================================== ======================================== ========================================== ============================================================================================================
OpenAPI中的数据类型( ``type`` )     OpenAPI中的格式( ``format`` )            OpenAPI中使用的属性                        附加的验证用注解
=================================== ======================================== ========================================== ============================================================================================================
``integer``                         (格式不限)                               ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``integer``                                                                  ``minimum`` 以及 ``maximum``               :java:extdoc:`NumberRange(min = {minimum}, max = {maximum}) <nablarch.core.validation.ee.NumberRange>`
``integer``                         ``int32``                                ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``integer``                         ``int32``                                ``minimum`` 以及 ``maximum``               :java:extdoc:`NumberRange(min = {minimum}, max = {maximum}) <nablarch.core.validation.ee.NumberRange>`
``integer``                         ``int64``                                ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``integer``                         ``int64``                                ``minimum`` 以及 ``maximum``               :java:extdoc:`NumberRange(min = {minimum}, max = {maximum}) <nablarch.core.validation.ee.NumberRange>`
``number``                          (格式不限)                               ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``number``                                                                   ``minimum`` 以及 ``maximum``               :java:extdoc:`DecimalRange(min = "{minimum}", max = "{maximum}") <nablarch.core.validation.ee.DecimalRange>`
``number``                          ``float``                                ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``number``                          ``float``                                ``minimum`` 以及 ``maximum``               :java:extdoc:`DecimalRange(min = "{minimum}", max = "{maximum}") <nablarch.core.validation.ee.DecimalRange>`
``number``                          ``double``                               ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``number``                          ``double``                               ``minimum`` 以及 ``maximum``               :java:extdoc:`DecimalRange(min = "{minimum}", max = "{maximum}") <nablarch.core.validation.ee.DecimalRange>`
``boolean``                                                                  ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``string``                          (格式不限)                               ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``string``                                                                   ``minLength`` 以及 ``maxLength``           :java:extdoc:`Length(min = {minLength}, max = {maxLength}) <nablarch.core.validation.ee.Length>`
``string``                                                                   ``pattern``                                :java:extdoc:`Pattern(regexp = "{pattern}")<jakarta.validation.constraints.Pattern>`
``array``                                                                    ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``array``                                                                    ``minItems`` 以及 ``maxItems``             :java:extdoc:`Size(min = {minItems}, max = {maxItems}) <nablarch.core.validation.ee.Size>`
=================================== ======================================== ========================================== ============================================================================================================

.. tip::

  * 不支持 ``multipleOf`` 、 ``exclusiveMinimum`` 、 ``exclusiveMaximum`` 、 ``minProperties`` 、 ``maxProperties`` 。
  * ``minimum`` 和 ``maximum`` 、 ``minLength`` 和 ``maxLength`` 、 ``minItems`` 和 ``maxItems`` 可以只指定其中一个。
  * Java的数据类型为 ``java.math.BigDecimal`` 、 ``java.util.List`` 、 ``java.util.Set`` 或模型时，附加 ``Valid`` 注解。
  * 仅 :java:extdoc:`Pattern<jakarta.validation.constraints.Pattern>` 附加Jakarta Bean Validation标准的注解，其他附加Nablarch提供的 :ref:`bean_validation` 固有的注解。

域验证
+++++++++++++++++++++++++

本工具使用 `OpenAPI规范的扩展属性(外部站点、英文) <https://spec.openapis.org/oas/v3.0.3.html#specification-extensions>`_ 来支持OpenAPI规范无法表达的 :ref:`bean_validation-domain_validation` 。

扩展属性使用 ``x-nablarch-domain`` ，值指定域名。

.. code-block:: yaml

        propertyName:
          type: string
          x-nablarch-domain: "domainName"

将 ``useBeanValidation`` 设为 ``true`` 生成源代码时，会向目标属性附加 :java:extdoc:`Domain("{domainName}") <nablarch.core.validation.ee.Domain>` 。

另外，由于域验证可以包含各种验证定义，当检测到可能冲突的验证定义时，会中止源代码生成。这是因为如果指定了与域中包含的验证规则相同的内容，会导致重复进行验证。

具体来说，如果 ``x-nablarch-domain`` 指定的属性中指定了 ``minimum`` 、 ``maximum`` 、 ``minLength`` 、 ``maxLength`` 、 ``minItems`` 、 ``maxItems`` 、 ``pattern`` 中的任何一个，则中止源代码生成。

``required`` 表示必需项，不是由域侧强制的，因此允许并用。

关于验证的运用注意事项
========================================

记载使用本工具生成包含验证定义的源代码时的运用注意事项。

OpenAPI规范的规定范围无法满足项目单位或相关验证要求时的注意事项
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

OpenAPI规范中规定的验证只有必需定义和长度检查、正则表达式检查，作为业务应用程序所要求的内容可能不足。

另外，由于直接修改自动生成的源代码并不理想，因此即使使用域验证也无法在生成的模型中实现相关验证。

因此，请注意OpenAPI规范和本工具的覆盖范围无法满足验证要求而需要另行实现时，结果会导致自动生成的模型和手动实现的Form等中验证定义容易分散的状况。

**不包含验证定义的自动生成模型的实现方法**

这里介绍创建与作为验证定义自动生成的模型相同定义的Form等，使用 :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` 复制属性值后，显式执行验证的方法。

本工具默认不附加验证用注解，是因为如前述容易产生验证定义分散的状况，而这是不希望发生的。

思路与 :ref:`bean_validation-execute_explicitly` 相同，以下记载实现示例。

.. code-block:: java

  public class ProjectAction implements ProjectsApi {  // ProjectsApi是本工具生成的接口

      // 实现接口中定义的方法
      @Override
      public EntityResponse<ProjectResponse> createProject(ProjectCreateRequest projectCreateRequest, JaxRsHttpRequest jaxRsHttpRequest, ExecutionContext context) {
          // 在与模型相同的属性定义中，添加单项目验证和相关验证的Form
          ProjectCreateForm form;

          try {
              // 在工具类中从模型复制值到Form后，显式执行验证
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
       * 从HTTP请求生成Bean并执行验证。
       *
       * @param beanClass 想要生成的Bean类
       * @param src 属性复制源对象
       * @return  属性中注册了值的Bean对象
       */
      public static <T> T validate(Class<T> beanClass, Object src) {
          T bean = BeanUtil.createAndCopy(beanClass, src));
          ValidatorUtil.validate(bean);
          return bean;
      }
  }

使用域验证时的注意事项
++++++++++++++++++++++++++++++++++++++++++++++++++

使用域验证可以通过为模型的属性定义域来汇总验证定义，或使用OpenAPI规范不支持的验证。

但请注意，包括OpenAPI规范支持的验证范围在内的验证规格也容易隐藏在域侧，可能导致从OpenAPI文档无法看到验证规格。

OpenAPI文档和生成的源代码示例
---------------------------------------------------

以下记载OpenAPI文档和生成的源代码示例。

源代码生成时本工具的设置示例如下。在需要与此不同的设置项目的示例中，也会同时记载本工具的设置示例。

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

另外，记载的各种示例为了理解概念而进行了摘录。

OpenAPI文档的路径和操作定义与源代码生成示例
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
          description: 已注册的项目信息
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
       * @param context handler执行上下文
       * @return 已注册的项目信息
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
       * @param context handler执行上下文
       * @return 获取的项目信息
       * @return 未找到项目时
       */
      @GET
      @Path("/{id}")
      @Produces({ "application/json" })
      EntityResponse<ProjectResponse> findProjectById(JaxRsHttpRequest jaxRsHttpRequest, ExecutionContext context);

  }

OpenAPI文档的模式定义与源代码生成示例
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
          description: 开始日期
          type: string
        endDate:
          format: date
          description: 结束日期
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
       * 开始日期
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
       * 结束日期
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

生成使用Bean Validation的源代码示例
====================================================================================================

OpenAPI文档示例

.. code-block:: yaml

  ## 路径以及操作
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
          description: 开始日期
          type: string
        endDate:
          format: date
          description: 结束日期
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
                <!-- 使用Bean Validation时将useBeanValidation设为true -->
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
       * @param context handler执行上下文
       * @return project created
       */
      @POST
      @Consumes({ "application/json" })
      @Produces({ "application/json" })
      // 通过HTTP主体接收请求时附加@Valid注解
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
       * 开始日期
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
       * 结束日期
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

      // hashCode、equals、toString等省略
  }

使用域验证生成源代码示例
=======================================================

OpenAPI文档示例

.. code-block:: yaml

  ## 路径以及操作
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
      type: object
      properties:
        projectName:
          description: 项目名
          type: string
          ## 使用域验证
          x-nablarch-domain: "projectName"

本工具的设置示例

.. code-block:: xml

            <configuration>
              <inputSpec>${project.basedir}/src/main/resources/openapi.yaml</inputSpec>
              <generatorName>nablarch-jaxrs</generatorName>
              <configOptions>
                <sourceFolder>src/gen/java</sourceFolder>
                <apiPackage>com.example.api</apiPackage>
                <modelPackage>com.example.model</modelPackage>
                <!-- 使用Bean Validation时将useBeanValidation设为true -->
                <useBeanValidation>true</useBeanValidation>
              </configOptions>
            </configuration>

本工具生成的模型示例

.. code-block:: java

  @JsonTypeName("ProjectCreateRequest")
  @jakarta.annotation.Generated(value = "nablarch.tool.openapi.codegen.JavaNablarchJaxrsServerCodegen", date = "2024-12-10T13:54:26.470544738+09:00[Asia/Tokyo]", comments = "Generator version: 7.10.0")
  public class ProjectCreateRequest   {
    private String projectName;
  
      /**
       * 项目名
       */
      public ProjectCreateRequest projectName(String projectName) {
          this.projectName = projectName;
          return this;
      }
  
      
      @JsonProperty("projectName")
      @Required @Domain("projectName")
      public String getProjectName() {
          return projectName;
      }
  
      @JsonProperty("projectName")
      public void setProjectName(String projectName) {
          this.projectName = projectName;
      }

      // hashCode、equals、toString等省略
  }

文件上传定义示例
==============================

OpenAPI文档示例

.. code-block:: yaml

  ## 路径以及操作
  /customers/upload:
    post:
      tags:
      - customer
      summary: 上传客户CSV文件
      description: 上传客户CSV文件并导入客户信息
      operationId: uploadCustomersCsvFile
      requestBody:
        description: 客户CSV文件信息
        content:
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CustomersCsvFileUploadRequest'
      responses:
        "200":
          description: 客户CSV文件上传导入结果
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CustomersCsvFileUploadResultResponse'


    ## 模式
    CustomersCsvFileUploadRequest:
      description: 客户CSV文件信息
      required:
      - fileName
      - file
      type: object
      properties:
        fileName:
          description: 文件名
          type: string
        file:
          description: 客户CSV文件
          type: string
          format: binary

本工具生成的资源(Action)接口示例

.. code-block:: java

  @Path("/customers/upload")
  @jakarta.annotation.Generated(value = "nablarch.tool.openapi.codegen.JavaNablarchJaxrsServerCodegen", date = "2024-12-10T14:36:36.602623815+09:00[Asia/Tokyo]", comments = "Generator version: 7.10.0")
  public interface CustomersApi {
      /**
       * POST  : 上传客户CSV文件
       *
       * 上传客户CSV文件并导入客户信息
       *
       * @param jaxRsHttpRequest HTTP请求
       * @param context handler执行上下文
       * @return 客户CSV文件上传导入结果
       */
      @POST
      @Consumes({ "multipart/form-data" })
      @Produces({ "application/json" })
      EntityResponse<CustomersCsvFileUploadResultResponse> uploadCustomersCsvFile(JaxRsHttpRequest jaxRsHttpRequest, ExecutionContext context);

  }

.. tip::

  文件上传时，请求的内容类型指定 ``multipart/form-data`` 。另外上传文件指定 ``type: string`` 且 ``format: binary`` 。此时不会生成对应模式的模型的源代码。上传的文件请从 :java:extdoc:`JaxRsHttpRequest <nablarch.fw.jaxrs.JaxRsHttpRequest>` 获取。

文件下载定义示例
==============================

OpenAPI文档示例

.. code-block:: yaml

  /customers/upload:
    get:
      tags:
      - customer
      summary: 将客户信息作为CSV文件下载
      description: 将客户信息作为CSV文件下载
      operationId: downloadCustomersCsvFile
      responses:
        "200":
          description: 客户CSV文件
          content:
            text/csv:
              schema:
                type: string
                format: binary

本工具生成的资源(Action)接口示例

.. code-block:: java

  @Path("/customers/upload")
  @jakarta.annotation.Generated(value = "nablarch.tool.openapi.codegen.JavaNablarchJaxrsServerCodegen", date = "2024-12-10T14:48:03.670170037+09:00[Asia/Tokyo]", comments = "Generator version: 7.10.0")
  public interface CustomersApi {
      /**
       * GET  : 将客户信息作为CSV文件下载
       *
       * 将客户信息作为CSV文件下载
       *
       * @param jaxRsHttpRequest HTTP请求
       * @param context handler执行上下文
       * @return 客户CSV文件
       */
      @GET
      HttpResponse downloadCustomersCsvFile(JaxRsHttpRequest jaxRsHttpRequest, ExecutionContext context);

  }

.. tip::

  文件下载中响应的内容类型可以是任意的。响应的模式定义设为 ``type: string`` 且 ``format: binary`` ，下载的文件内容和响应头部使用 :java:extdoc:`HttpResponse <nablarch.fw.web.HttpResponse>` 设置。


.. |br| raw:: html

  <br />
