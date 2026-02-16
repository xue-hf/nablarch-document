=================================
请求单元测试的实施方法
=================================

前提条件
-----------

RESTful Web服务执行基础测试时，除了其他执行基础测试框架外
还需要添加依赖的模块。
详情请参考 :ref:`自动测试框架的使用方法 <rest_testing_fw>` 。

测试类的编写方法
-------------------------------

* :ref:`继承框架准备的测试类的父类。 <rest_test_extends_superclass>`
* 使用JUnit4的注解 (给测试方法添加 @Test 注解)
* :ref:`使用事前准备辅助功能 <rest_test_helper>` 生成请求
* :ref:`发送请求 <rest_test_execute>`
* :ref:`确认结果 <rest_test_assert>`

.. code-block:: java

    import nablarch.fw.web.HttpResponse;
    import nablarch.fw.web.RestMockHttpRequest;
    import nablarch.test.core.http.RestTestSupport;
    import org.json.JSONException;
    import org.junit.Test;
    import org.skyscreamer.jsonassert.JSONAssert;
    import org.skyscreamer.jsonassert.JSONCompareMode;

    import static com.jayway.jsonpath.matchers.JsonPathMatchers.hasJsonPath;
    import static org.hamcrest.Matchers.hasSize;
    import static org.junit.Assert.assertThat;

    public class SampleTest extends RestTestSupport { //继承RestTestSupport
        @Test  //添加注解
        public void 可以获取项目列表() throws JSONException {
            String message = "项目列表获取";

            RestMockHttpRequest request = get("/projects");               //生成请求
            HttpResponse response = sendRequest(request);                 //发送请求
            assertStatusCode(message, HttpResponse.Status.OK, response);  //确认结果

            assertThat(response.getBodyString(), hasJsonPath("$", hasSize(10)));    //使用json-path-assert验证响应主体

            JSONAssert.assertEquals(message, readTextResource("可以获取项目列表.json")
                    , response.getBodyString(), JSONCompareMode.LENIENT);                  //使用JSONAssert验证响应主体
        }
    }

.. _rest_test_extends_superclass:

继承框架准备的测试类的父类
=================================================================

测试类的父类继承 ``nablarch.test.core.http.RestTestSupport`` 类。
如果不需要数据投入和数据库断言，则继承 ``nablarch.test.core.http.SimpleRestTestSupport`` 类。
这种情况下可以跳过以下 :ref:`测试数据的编写方法 <rest_test_data>` 。

各父类的详情请参考 :ref:`自动测试框架的使用方法 <rest_test_superclasses>` 。

使用JUnit4的注解
=================================
测试框架基于JUnit4，因此给测试目标方法添加 ``@Test`` 注解。

使用事前准备辅助功能生成请求
===================================================
使用父类中准备的 :ref:`事前准备辅助功能 <rest_test_helper>` 生成请求。

发送请求
=======================
通过调用父类中准备的 :ref:`请求发送方法 <rest_test_execute>` 来发送请求。

确认结果
=================
状态码通过调用父类中准备的 :ref:`方法 <rest_test_assert>` 来验证。
响应主体请使用任意库根据应用程序进行验证。

.. _rest_test_data:

测试数据的编写方法
--------------------

可以按照 :ref:`how_to_write_excel` 中记载的方法描述测试数据。
但是，RESTful Web服务执行基础测试时自动读取的数据仅限于以下。

* 测试类中通用的数据库初始值
* 每个测试方法的数据库初始值

.. important::
    RESTful Web服务执行基础以外的测试时，每个测试类必须有一个Excel文件，
    但RESTful Web服务执行基础测试时，即使没有Excel文件也不会报错，只是跳过
    向数据库的数据投入。

.. important::
    可以在Excel文件中记载上述以外的测试数据，但记载时需要
    按照 :ref:`how_to_get_data_from_excel` 中记载的方法，在测试类中记述获取值的处理。
    为了减少测试类的记述量，父类 ``RestTestSupport`` 提供了以下
    方法。

    .. code-block:: java

        List<Map<String, String>> getListMap(String sheetName, String id)
        List<Map<String, String[]>> getListParamMap(String sheetName, String id)
        Map<String, String[]> getParamMap(String sheetName, String id)

测试类中通用的数据库初始值
========================================

请参考 :ref:`request_test_setup_db` 。

每个测试方法的数据库初始值
====================================

在记载测试数据的Excel文件中，用\ **测试方法的名称**\ 准备工作表，
用\ **SETUP_TABLES**\数据类型记载数据库初始值。
这里记载的数据将由框架在测试方法执行时投入。
