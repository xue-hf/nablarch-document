.. _`platform`:

运行环境
====================================

.. contents:: 目录
   :depth: 3
   :local:

关于Nablarch框架的运行环境的说明。

.. tip::
 关于Nablarch框架以外的内容（例如Nablarch SQL Executor等）的运行环境，请参阅各内容的相关文档。

Nablarch框架运行环境要求
-----------------------------------------------------
Nablarch框架只使用了Java标准进行开发，运行时至少需要满足以下条件。

* Java SE 17
* JDBC 3.0

此外，根据所使用的Nablarch功能，需要以下的Jakarta EE规范。

* Jakarta Standard Tag Library 3.0
* Jakarta Activation 2.1
* Jakarta Server Pages 3.1
* Jakarta Servlet 6.0
* Jakarta Mail 2.1
* Jakarta Messaging 3.1
* Jakarta Persistence 3.1
* Jakarta Batch 2.1
* Jakarta Bean Validation 3.0
* Jakarta RESTful Web Services 3.1

.. important::
 此处所示的版本号虽指定了特定版本，
 但基本上可理解为“版本号及以上”均可使用，
 这是因为Java标准规范和Jakarta EE规范在版本升级时基本保持向后兼容性。

Nablarch框架的测试环境
-----------------------------------------------------
Nablarch框架已在以下环境中进行了测试，并已确认能够正常运行。

Java
 * Java SE 17/21 [#java21]_

数据库
 * Oracle Database 19c/21c/23ai
 * IBM Db2 11.5/12.1
 * SQL Server 2017/2019/2022
 * PostgreSQL 12.2/13.2/14.0/15.2/16.2/17.4

应用服务器
 * WebSphere Application Server Liberty 25.0.0.2
 * Open Liberty 25.0.0.2
 * Red Hat JBoss Enterprise Application Platform 8.0.0
 * WildFly 35.0.1.Final
 * Apache Tomcat 10.1.17

Jakarta EE
 * Hibernate Validator 8.0.0.Final
 * JBeret 2.1.1.Final

MOM（面向消息的中间件）
 * IBM MQ 9.3

浏览器
 PC
  * Microsoft Edge
  * Mozilla Firefox
  * Google Chrome
  * Safari

.. [#java21] 使用Java21时，需要额外进行配置，具体的配置方法请参考 :doc:`../blank_project/setup_blankProject/setup_Java21` 。
