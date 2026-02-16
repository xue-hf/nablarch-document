==================================
取引单元测试的实施方法
==================================

在Web服务中，交易大多在1个请求中完成。这种情况下，1请求=1交易，不需要进行取引单元测试。

但是，如果多个请求构成交易，则可以通过连续执行每个请求的测试来实施取引单元测试。

取引单元测试的测试类示例
---------------------------------

以下示例中获取更新目标，从获取的信息创建更新用的表单并执行更新，验证是否按预期更新。

.. code-block:: java

    @Test
    public void 项目更新交易() {
        String message1 = "获取变更目标";
        RestMockHttpRequest request001 = get("/projects?projectName=项目００１");
        HttpResponse response001 = sendRequest(request001);
        assertStatusCode(message1, HttpResponse.Status.OK, response001);
        // 使用获取的变更目标创建更新用表单
        Project project = parseProject(response001).setProjectName("项目８８８");
        ProjectUpdateForm updateForm = new ProjectUpdateForm(project);

        String message2 = "项目更新";
        RestMockHttpRequest updateRequest = put("/projects").setBody(updateForm);
        HttpResponse updateResponse = sendRequest(updateRequest);
        assertStatusCode(message2, HttpResponse.Status.OK, updateResponse);

        String message3 = "获取的项目与变更内容一致";
        RestMockHttpRequest request888 = get("/projects?projectName=项目８８８");
        HttpResponse response888 = sendRequest(request888);
        assertStatusCode(message3, HttpResponse.Status.OK, response888);
        assertProjectEquals(project, parseProject(response888));
    }

继承前响应信息如Cookie的方法
----------------------------------------------------
取引单元测试时，可能希望将前次请求的响应中从服务器接收的会话ID和CSRF令牌等值
包含到下一个请求中。
这种情况下可以通过以下方法实现。

创建 ``RequestResponseProcessor`` 的实现类
****************************************************************
RESTful Web服务执行基础测试框架准备了 :java:extdoc:`RequestResponseProcessor<nablarch.test.core.http.RequestResponseProcessor>` 
用于操作请求和响应的接口。

请根据各应用程序的需求创建此接口的实现类。

框架提供了常用实现 :java:extdoc:`RequestResponseCookieManager<nablarch.test.core.http.RequestResponseCookieManager>` 。
此实现可以从响应的 ``Set-Cookie`` 头部提取属性中指定名称的Cookie，并继承到请求的 ``Cookie`` 头部。

还提供了专门针对 :ref:`session_store` 会话ID的实现 :java:extdoc:`NablarchSIDManager<nablarch.test.core.http.NablarchSIDManager>` 。
此实现以 :ref:`session_store_handler` 保持会话ID时的默认Cookie名称 ``NABLARCH_SID`` 从 ``Set-Cookie`` 头部提取Cookie。
如果更改了会话ID的Cookie名称，请使用 :java:extdoc:`RequestResponseCookieManager<nablarch.test.core.http.RequestResponseCookieManager>` 并显式指定Cookie名称。

``RequestResponseProcessor`` 用于在1个取引单元测试用例内将先接收的响应值传递到下一个请求。
此时，为将响应中提取的值传递到请求，会在内部作为状态持有。
如果通过以下方法配置组件，在Nablarch的DI容器中实例会成为单例，
如果不显式初始化状态，则状态会在多个测试用例间继承。
为防止这种情况，框架在每个测试用例调用 :java:extdoc:`RequestResponseProcessor#reset<nablarch.test.core.http.RequestResponseProcessor.reset()>` 。
如果不希望在多个测试用例间继承状态，需要在 ``reset()`` 中实现初始化处理。
如果没有内部状态，或希望在多个测试用例间共享状态，可以将 ``reset()`` 方法设为空方法。

在组件配置文件中以 ``defaultProcessor`` 名称设置实现类
***********************************************************************************
.. code-block:: xml

  <component name="defaultProcessor" class="nablarch.test.core.http.RequestResponseCookieManager"/>
    <property name="cookieName" value="JSESSIONID"/>
  </component>


另外，如果希望设置多个 ``RequestResponseProcessor`` ，可以使用 :java:extdoc:`ComplexRequestResponseProcessor<nablarch.test.core.http.ComplexRequestResponseProcessor>` 来实现。

.. code-block:: xml

  <component name="defaultProcessor" class="nablarch.test.core.http.ComplexRequestResponseProcessor">
    <property name="processors">
      <list>
        <component class="nablarch.test.core.http.RequestResponseCookieManager"/>
          <property name="cookieName" value="JSESSIONID"/>
        </component>
        <component class="nablarch.test.core.http.NablarchSIDManager"/>
        <component class="com.example.test.CSRFTokenManager"/>
      </list>
    </property>
  </component>

以 ``defaultProcessor`` 名称设置的 ``RequestResponseProcessor`` ，在向内置服务器发送请求前
执行 :java:extdoc:`RequestResponseProcessor#processRequest<nablarch.test.core.http.RequestResponseProcessor.processRequest(nablarch.fw.web.HttpRequest)>` ，
接收响应后执行 :java:extdoc:`RequestResponseProcessor#processResponse<nablarch.test.core.http.RequestResponseProcessor.processResponse(nablarch.fw.web.HttpRequest,nablarch.fw.web.HttpResponse)>` 。
