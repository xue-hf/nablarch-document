.. _slf4j_adaptor:

SLF4J适配器
==================================================

.. contents:: 目录
  :depth: 3
  :local:

Java的OSS中有许多使用 `SLF4J(外部网站，英语) <https://www.slf4j.org/>`_ 进行日志输出的模块，
在使用这些模块时，有时希望将日志输出集中到Nablarch的 :ref:`日志输出功能 <log>` 中。
为应对这种情况，提供了通过SLF4J的API使用Nablarch的日志输出功能进行日志输出的适配器。

模块列表
--------------------------------------------------

.. code-block:: xml

  <!-- SLF4J适配器 -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>slf4j-nablarch-adaptor</artifactId>
  </dependency>

.. tip::

  使用SLF4J版本2.0.11进行测试。
  要更改版本时，请在项目侧进行测试确认无问题。
  另外，SLF4J版本2.0.0以后日志实现的搜索方法已更改。例如使用了不兼容的1.7系版本时，会输出以下日志，之后不再进行日志输出，请注意。

  .. code-block:: none

    SLF4J: Failed to load class "org.slf4j.impl.StaticLoggerBinder".
    SLF4J: Defaulting to no-operation (NOP) logger implementation
    SLF4J: See http://www.slf4j.org/codes.html#StaticLoggerBinder for further details.  

使用SLF4J适配器
--------------------------------------------------
由于SLF4J会在运行时自动检测所需的类，因此只需将本适配器添加到项目的依赖模块中即可使用。
日志输出的设置请参阅Nablarch的 :ref:`日志输出功能 <log>` 。

.. code-block:: xml

  <!-- SLF4J适配器 -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>slf4j-nablarch-adaptor</artifactId>
    <scope>runtime</scope>
  </dependency>
