==================================
取引单元测试的实施方法（批处理）
==================================

批处理的取引单元测试使用自动测试框架进行测试。
通过连续执行请求单元测试，以交易单位进行测试。

测试类需要满足以下条件进行创建。

* 测试类的包名为测试目标交易的包名。
* 以<交易ID>Test作为测试类的类名进行创建。

例如，测试目标交易的交易ID为B21AC01时，测试类如下所示。

.. code-block:: java

 package nablarch.sample.ss21AC01

 import nablarch.test.core.batch.BatchRequestTestSupport;

 // 中略
 
 public class B21AC01Test extends BatchRequestTestSupport {
 

测试用例分割方针
====================

原则上，\ **1个工作表对应1个测试用例**\ 。
以下显示例外事项。


复杂测试用例的情况
------------------------

如果测试数据量大，或1个交易中包含的处理多，
将所有的测试数据塞进1个工作表中会导致工作表内数据过多，
测试数据的可读性下降。\
这种情况下，可以将1个用例分割到多个工作表中描述。


非常简单的测试用例的情况
------------------------------

非常简单的测试用例，且测试数据量少时，
可以在1个工作表中包含所有测试用例。


基本的描述方法
================

原则上，将1个测试用例汇总到1个工作表中描述。\
通过在1个工作表内记载多个批处理执行，实现以交易单位的测试。

以下示例中，处理由3个批处理(文件输入批处理、用户删除批处理、文件输出批处理)\
构成的交易。

.. code-block:: java

 /** 正常结束的情况 */
 @Test
 public void testSuccess() {
     execute();
 }


**【testSuccess工作表】**

LIST_MAP=testShots

=== ============= ==================  ========== ========= ============== ============ ===============
no  description   expectedStatusCode  setUpTable setUpFile expectedTable  expectedFile   requestPath    
=== ============= ==================  ========== ========= ============== ============ ===============
 1  文件输入                     100  default    default   default                     fileInputBatch 
 2  用户删除                     100  default              default                     userDeleteBatch
 3  文件输出                     100  default              fileInputBatch default      fileOutputBatch          
=== ============= ==================  ========== ========= ============== ============ ===============


将1个测试用例分割到多个工作表的情况
=======================================

                                           
例如，前项(\ `基本的描述方法`\ )中示例的测试用例，可以如下分割描述。


.. code-block:: java

 package nablarch.sample.ss21AA01

 import org.junit.Test;
 import nablarch.test.core.messaging.BatchRequestTestSupport;

 // 中略

 public class B21AA01Test extends BatchRequestTestSupport {

     @Test
     public void testSuccess() {
      
         // 将输入文件注册到临时表
         execute("testSuccess_fileInput");
      
         // 从临时表信息删除用户相关表
         execute("testSuccess_userDelete");
      
         // 将结果输出到文件
         execute("testSuccess_fileOutput");
     }

\

**【testSuccess_fileInput工作表】**

LIST_MAP=testShots

==== ============= ==================  ========== ========= ===============
 no  case          expectedStatusCode  setUpTable setUpFile    requestPath    
==== ============= ==================  ========== ========= ===============
  1  文件输入                     100  default    default   fileInputBatch 
==== ============= ==================  ========== ========= ===============

\

**【testSuccess_userDelete工作表】**

LIST_MAP=testShots

==== ============= ==================  ========== ============= ===============
 no  case          expectedStatusCode  setUpTable expectedTable requestPath    
==== ============= ==================  ========== ============= ===============
  1  用户删除                     100  default    default       userDeleteBatch
==== ============= ==================  ========== ============= ===============


**【testSuccess_fileOutput工作表】**

LIST_MAP=testShots

==== ============= ==================  ========== ========= ===============
 no  case          expectedStatusCode  setUpTable outFile    requestPath    
==== ============= ==================  ========== ========= ===============
  1  文件输出                     100  default    default   fileOutputBatch 
==== ============= ==================  ========== ========= ===============


在1个工作表中包含多个用例的情况
===============================

非常简单的测试用例时，可以汇总到多个。

以下示例中，在1个工作表中记述了2个测试用例（通常的情况和输入数据为0件的情况）

.. code-block:: java

 /** 正常结束的情况 */
 @Test
 public void testSuccess() {
     execute();
 }


**【testSuccess工作表】**

LIST_MAP=testShots

=== ==================== ==================  ========== ========= ============== ============ ===============
 no  description         expectedStatusCode  setUpTable setUpFile expectedTable  expectedFile   requestPath    
=== ==================== ==================  ========== ========= ============== ============ ===============
1-1  文件输入                        100      shot1      shot1                                fileInputBatch 
1-2  用户删除                        100                           shot1                      userDeleteBatch
2-1  文件输入（0件）                 100      shot2      shot2                                fileInputBatch 
2-2  用户删除（0件）                 100                           shot2                      userDeleteBatch
=== ==================== ==================  ========== ========= ============== ============ ===============

\

.. tip::
 通过使用组ID可以在1个工作表中描述多个用例的测试数据。
 详情请参考『\ :ref:`tips_groupId`\ 』项。


