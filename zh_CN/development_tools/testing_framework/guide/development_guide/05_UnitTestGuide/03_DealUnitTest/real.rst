===============================================================
取引单元测试的实施方法（同步响应消息接收处理)
===============================================================

同步响应消息接收处理中，请求和交易的作用域大多相同。
这种情况下，1请求=1交易，不需要进行取引单元测试。

但是，如果多个消息构成交易，则\
与批处理中的取引单元测试相同，
通过连续执行每个请求的测试可以实施取引单元测试。

取引单元测试的实施方法基本与批处理相同。
但是，测试类继承的父类不同（使用\ ``MessagingRequestTestSupport``\ ）。
另外，测试类需要满足以下条件进行创建。

* 测试类的包名为测试目标交易的包名。
* 以<交易ID>Test作为测试类的类名进行创建。

例如，测试目标交易的交易ID为M21AA03时，测试类如下所示。

.. code-block:: java

 package nablarch.sample.ss21AA03

 import nablarch.test.core.messaging.MessagingRequestTestSupport;

 // 中略
 
 public class M21AA03Test extends MessagingRequestTestSupport {


实施方法请参考批处理的实施方法。

:doc:`./batch`


