====================================================================
请求单元测试的实施方法（无响应消息发送处理）
====================================================================

--------------------
概述
--------------------
无响应消息发送处理用的Action类作为Nablarch的一部分提供。
因此，在请求单元测试中使用此Action类，确认以下\ `测试目标交付物`\_的内容。

**※不需要像其他处理那样进行Action类的条件覆盖、边界值测试等。**

测试目标交付物
===================
* 定义报文布局的格式定义文件
* 以下3种SQL语句

  * 从报文发送表中获取状态为未发送的数据的SELECT语句
  * 报文发送后，将对应数据状态更新为已处理的UPDATE语句
  * 报文发送失败时，将对应数据状态更新为发送失败(错误)的UPDATE语句


--------------------
测试类的编写方法
--------------------

测试类需要满足以下条件进行创建。

* 测试类的包名为测试目标功能的包名。
* 以<报文的请求ID>RequestTest作为测试类的类名进行创建。
* 继承\ ``nablarch.test.core.batch.BatchRequestTestSupport``\ 。

例如，测试目标功能的包名为nablarch.sample.ss21AA、报文的请求ID为RM11AC0301时，测试类如下所示。

.. code-block:: java

  package nablarch.sample.ss21AA;
  
  // ～中略～

  public class RM11AC0301RequestTest extends BatchRequestTestSupport {


------------------------------
测试数据的编写方法
------------------------------
说明测试\ `测试目标交付物`\_所需的测试数据的描述方法。

测试数据的描述方法请参考\ :ref:`message_sendSyncMessage_test`\ 。
本项说明与\ :ref:`message_sendSyncMessage_test`\ 描述不同的地方。

请求报文的期望值以及返回的响应报文（响应消息）的准备
======================================================================

无响应消息发送处理中，由于不存在响应报文，因此不需要确认响应报文是否符合期望值。

因此，以下设置变为不需要。

* testShots的定义

  * responseMessage

* 期望值及准备数据的定义

  * RESPONSE_HEADER_MESSAGES
  * RESPONSE_BODY_MESSAGES


正常系测试
------------------

 | 确认报文正确发送的情况。
 | 在这种情况下，确认发送的报文以及对应数据的状态更新。
 |
 | 无响应消息发送处理用的Action类要求启动参数中报文的请求ID。
 | 因此，需要在「testShots」的定义中添加「KEY=messageRequestId」、「VALUE=报文的请求ID」，如下图所示。

 .. image:: _image/delayed_send.png
    :scale: 50


异常系测试(故障系测试)
------------------------------
  
 | 异常系测试是为了确认报文发送失败时将对应数据状态更新为错误的UPDATE语句所必需的。
 | 要实施异常系测试用例，在「testShots」的定义中如下所示设置「KEY=errorCase」、「VALUE=true」即可。
 | 另外，在异常系情况下由于不发送报文，因此不需要设置发送报文的期望值。

 .. image:: _image/delayed_send_error.png
    :scale: 70

 .. tip:: 
   要实施异常系测试用例，需要将无响应消息发送处理用共同Action切换为测试用Action。
   以下显示其设置示例。

   * 生产环境设置示例

     .. code-block:: xml

      <!--分派用handler-->
      <component name="requestPathJavaPackageMapping" class="nablarch.fw.handler.RequestPathJavaPackageMapping">
        <!-- 设置无响应消息发送处理用共同Action。 -->
        <property name="basePackage" value="nablarch.fw.messaging.action.AsyncMessageSendAction" />
        <property name="immediate" value="false" />
      </component>

   * 测试用设置

     用测试用Action类覆盖上述生产环境用设置。

     .. code-block:: xml

      <!--分派用handler-->
      <component name="requestPathJavaPackageMapping" class="nablarch.fw.handler.RequestPathJavaPackageMapping">
        <property name="basePackage" value="nablarch.test.core.messaging.AsyncMessageSendActionForUt" />
        <property name="immediate" value="false" />
      </component>
