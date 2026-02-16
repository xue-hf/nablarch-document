.. _log_adaptor:

日志适配器
==================================================
将Nablarch提供的 :ref:`日志输出功能 <log>` 的日志输出处理委托给以下日志框架的适配器。

* `slf4j(外部网站，英语) <https://www.slf4j.org/>`_ 
* `JBoss Logging(外部网站，英语) <https://github.com/jboss-logging>`_

在需要根据客户要求或使用的产品等统一日志记录器时使用适配器。
使用适配器后，使用Nablarch的 :ref:`日志输出功能 <log>` 进行的所有日志输出处理都将委托给选择的日志框架。

.. important::

  Nablarch5u15之前提供的log4j适配器由于使用了已达到EOL的 `log4j1.2(外部网站，英语) <https://logging.apache.org/log4j/1.x/>`_ ，
  且 `漏洞 <https://jvndb.jvn.jp/ja/contents/2019/JVNDB-2019-013606.html>`_ 修复未公开，因此已废止。
  请使用slf4j或JBoss Logging。

.. tip::

  日志框架的设置方法等请参阅产品的手册等。
  
模块列表
--------------------------------------------------

slf4j
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: xml

  <!-- slf4j适配器 -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-slf4j-adaptor</artifactId>
  </dependency>

.. important::

  由于slf4j不存在FATAL级别，因此nablarch-slf4j-adaptor的规格为当尝试以FATAL级别输出日志时，全部以ERROR级别输出。

.. tip::
  
  使用slf4j版本2.0.11进行测试。
  要更改版本时，请在项目侧进行测试确认无问题。
  另外，SLF4J版本2.0.0以后日志实现的搜索方法已更改。例如使用了不兼容的1.7系版本时，会输出以下日志，之后不再进行日志输出，请注意。

  .. code-block:: none

    SLF4J: Failed to load class "org.slf4j.impl.StaticLoggerBinder".
    SLF4J: Defaulting to no-operation (NOP) logger implementation
    SLF4J: See http://www.slf4j.org/codes.html#StaticLoggerBinder for further details.  


JBoss Logging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: xml

  <!-- JBoss Logging适配器 -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-jboss-logging-adaptor</artifactId>
  </dependency>
  
.. tip::
  
  使用JBoss Logging版本3.6.0.Final进行测试。
  要更改版本时，请在项目侧进行测试确认无问题。
  
进行使用日志框架的设置
--------------------------------------------------
在 :ref:`日志输出功能 <log>` 的设置文件(\ **log.properties**\ )中设置工厂。
通过此设置，日志输出处理将委托给日志框架。

slf4j
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: properties

  # 使用slf4j的工厂设置
  loggerFactory.className=nablarch.integration.log.slf4j.Slf4JLoggerFactory
  
JBoss Logging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: properties

  # 使用JBoss Logging的工厂设置
  loggerFactory.className=nablarch.integration.log.jbosslogging.JbossLoggingLoggerFactory
