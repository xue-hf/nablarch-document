.. _`stateless_web_app`:

使Web应用无状态化
=====================================================================

.. contents:: 目录
  :depth: 3

基本思路
--------------------------------------------------

Servlet API提供的HTTP会话会在AP服务器上保持状态，因此如果直接使用，将无法进行横向扩展。
通常，要对AP服务器进行横向扩展，需要采取以下措施：

1. 在负载均衡器中启用粘性会话
2. 使用AP服务器的会话复制功能
3. 将AP服务器的HTTP会话保存目标设置为NoSQL

1、2在 `Twelve-Factor App <https://12factor.net/ja/>`_ 中所说的可丢弃性方面较差，2、3会依赖于AP服务器。

Nablarch使用的功能中，有些依赖于HTTP会话，
通过将这些功能切换为不依赖HTTP会话的功能，
可以使AP服务器无状态化。

.. _http-session-dependence:

依赖于HTTP会话的功能
--------------------------------------------------

以下功能默认依赖于HTTP会话。

* :ref:`session_store`
* :ref:`双重提交防止<tag-double_submission>`
* :ref:`thread_context_handler`
* :ref:`http_rewrite_handler`
* :ref:`hidden加密<tag-hidden_encryption>`

不依赖HTTP会话的功能的引入方法
--------------------------------------------------

对于 :ref:`http-session-dependence` 中的各功能，通过进行如下设置，可以消除对HTTP会话的依赖。

会话存储
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* :ref:`db_managed_expiration`

双重提交防止
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* :ref:`db_double_submit` 

线程上下文变量管理处理器
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在 :ref:`线程上下文的初始化<thread_context_handler-initialization>` 中不使用以下组件。

* :java:extdoc:`LanguageAttributeInHttpSession <nablarch.common.web.handler.threadcontext.LanguageAttributeInHttpSession>`
* :java:extdoc:`TimeZoneAttributeInHttpSession <nablarch.common.web.handler.threadcontext.TimeZoneAttributeInHttpSession>`
* :java:extdoc:`UserIdAttribute <nablarch.common.handler.threadcontext.UserIdAttribute>`


分别可以使用以下组件作为不使用HTTP会话的实现来替代。

* :java:extdoc:`LanguageAttributeInHttpCookie <nablarch.common.web.handler.threadcontext.LanguageAttributeInHttpCookie>`
* :java:extdoc:`TimeZoneAttributeInHttpCookie <nablarch.common.web.handler.threadcontext.TimeZoneAttributeInHttpCookie>`
* :java:extdoc:`UserIdAttributeInSessionStore <nablarch.common.web.handler.threadcontext.UserIdAttributeInSessionStore>`

HTTP重写处理器
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

不使用 :ref:`http_rewrite_handler` 。
如果使用，请设置为不访问会话作用域。

hidden加密
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Nablarch提供了 :ref:`hidden加密<tag-hidden_encryption>` 功能。
由于该功能依赖于HTTP会话，因此请在 :ref:`useHiddenEncryption <tag-use_hidden_encryption>` 中设置为 ``false`` 以不使用该功能。

使用本地文件系统
--------------------------------------------------
如果上传的文件等保存在AP服务器的本地，就会变成保持状态。
在这种情况下，需要准备共享存储等，使AP服务器不在本地保存文件。

检测HTTP会话的误生成
--------------------------------------------------
为了防止因设置遗漏或实现错误而误生成HTTP会话，提供了检测HTTP会话生成功能。
启用该功能后，当尝试生成HTTP会话时会抛出异常。

该功能可通过将 :java:extdoc:`WebFrontController <nablarch.fw.web.servlet.WebFrontController>` 的 ``preventSessionCreation`` 属性设置为 ``true`` 来启用（默认为 ``false`` ，禁用）。

具体而言，在定义了 :java:extdoc:`WebFrontController <nablarch.fw.web.servlet.WebFrontController>` 组件的配置文件中，通过如下描述可以启用检测功能。

.. code-block:: xml

  <!-- 处理器队列构成 -->
  <component name="webFrontController"
             class="nablarch.fw.web.servlet.WebFrontController">

    <!-- 检测HTTP会话的误生成 -->
    <property name="preventSessionCreation" value="true" />
