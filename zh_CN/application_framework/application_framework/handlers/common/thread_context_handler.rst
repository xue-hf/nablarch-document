.. _thread_context_handler:

线程上下文变量管理Handler
=======================================

.. contents:: 目录
  :depth: 3
  :local:

针对线程上下文的各属性值，对每个请求进行初始化处理的Handler。

线程上下文是指将请求ID、用户ID等在同一处理线程内共享的值保存在线程本地区域上的机制。

.. important::
  本Handler在线程本地上设置的值，需要使用 :ref:`thread_context_clear_handler` 在返回处理中进行删除。
  在往路处理中，如在本Handler之前的Handler中访问线程上下文，
  由于无法获取值，请注意不要在本Handler之前的Handler中访问线程上下文。

.. tip::
 线程上下文的属性值大多由本Handler设置，
 但本Handler以外的Handler和业务Action也可以设置任意变量。

本Handler执行以下处理。

* :ref:`thread_context_handler-initialization`

处理流程如下。

.. image:: ../images/ThreadContextHandler/ThreadContextHandler_flow.png

Handler类名
--------------------------------------------------
* :java:extdoc:`nablarch.common.handler.threadcontext.ThreadContextHandler`

模块一览
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw</artifactId>
  </dependency>

  <!-- 国际化对应中，仅当需要制作可选择语言和时区的画面时使用 -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web</artifactId>
  </dependency>

约束
---------------------------------------
无。

.. _thread_context_handler-initialization:

对每个请求进行线程上下文的初始化
-----------------------------------------------------------
线程上下文的初始化使用实现了
:java:extdoc:`ThreadContextAttribute接口 <nablarch.common.handler.threadcontext.ThreadContextAttribute>`
的类来进行。

默认提供以下类。

请求ID、内部请求ID
 * :java:extdoc:`RequestIdAttribute <nablarch.common.handler.threadcontext.RequestIdAttribute>`
 * :java:extdoc:`InternalRequestIdAttribute <nablarch.common.handler.threadcontext.InternalRequestIdAttribute>` \ [#]_\

.. [#] 
   在使用 :ref:`permission_check_handler` 或 :ref:`ServiceAvailabilityCheckHandler` 等针对内部请求ID执行处理的Handler时进行设置。

用户ID
 * :java:extdoc:`UserIdAttribute <nablarch.common.handler.threadcontext.UserIdAttribute>`
 * :java:extdoc:`UserIdAttributeInSessionStore <nablarch.common.web.handler.threadcontext.UserIdAttributeInSessionStore>`

语言
 * :java:extdoc:`LanguageAttribute <nablarch.common.handler.threadcontext.LanguageAttribute>`
 * :java:extdoc:`HttpLanguageAttribute <nablarch.common.web.handler.threadcontext.HttpLanguageAttribute>`
 * :java:extdoc:`LanguageAttributeInHttpCookie <nablarch.common.web.handler.threadcontext.LanguageAttributeInHttpCookie>`
 * :java:extdoc:`LanguageAttributeInHttpSession <nablarch.common.web.handler.threadcontext.LanguageAttributeInHttpSession>`

时区
 * :java:extdoc:`TimeZoneAttribute <nablarch.common.handler.threadcontext.TimeZoneAttribute>`
 * :java:extdoc:`TimeZoneAttributeInHttpCookie <nablarch.common.web.handler.threadcontext.TimeZoneAttributeInHttpCookie>`
 * :java:extdoc:`TimeZoneAttributeInHttpSession <nablarch.common.web.handler.threadcontext.TimeZoneAttributeInHttpSession>`

执行时ID
 * :java:extdoc:`ExecutionIdAttribute <nablarch.common.handler.threadcontext.ExecutionIdAttribute>`

这些类需要在组件配置文件中添加定义后使用。

.. code-block:: xml

 <component class="nablarch.common.handler.threadcontext.ThreadContextHandler">
   <property name="attributes">
     <list>

       <!-- 请求ID -->
       <component class="nablarch.common.handler.threadcontext.RequestIdAttribute" />

       <!-- 内部请求ID -->
       <component class="nablarch.common.handler.threadcontext.InternalRequestIdAttribute" />

       <!-- 用户ID -->
       <component class="nablarch.common.handler.threadcontext.UserIdAttribute">
         <property name="sessionKey"  value="user.id" />
         <property name="anonymousId" value="guest" />
       </component>

       <!-- 语言 -->
       <component class="nablarch.common.handler.threadcontext.LanguageAttribute">
         <property name="defaultLanguage" value="ja" />
       </component>

       <!-- 时区 -->
       <component class="nablarch.common.handler.threadcontext.TimeZoneAttribute">
         <property name="defaultTimeZone" value="Asia/Tokyo" />
       </component>

       <!-- 执行时ID -->
       <component class="nablarch.common.handler.threadcontext.ExecutionIdAttribute" />
     </list>
   </property>
 </component>

.. _thread_context_handler-user_id_attribute_setting:

设置用户ID
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:java:extdoc:`UserIdAttributeInSessionStore <nablarch.common.web.handler.threadcontext.UserIdAttributeInSessionStore>` 默认从会话存储中获取用户ID。
由于框架不会进行会话存储的设置，因此需要在登录时等由应用程序进行设置。
设置到会话存储时的键默认使用"user.id"。
如需覆盖，请在 :java:extdoc:`UserIdAttribute#sessionKey <nablarch.common.handler.threadcontext.UserIdAttribute.setSessionKey(java.lang.String)>` 中设置值。
以下是将"login_id"覆盖设置的示例。

.. code-block:: xml

  <component name="threadContextHandler" class="nablarch.common.handler.threadcontext.ThreadContextHandler">
    <property name="attributes">
      <list>
        <!-- 用户ID -->
        <component class="nablarch.common.web.handler.threadcontext.UserIdAttributeInSessionStore">
          <property name="sessionKey" value="login_id"/>
          <property name="anonymousId" value="${nablarch.userIdAttribute.anonymousId}"/>
        </component>
        <!-- 其他组件定义省略 -->
      </list>
    </property>
  </component>

以下是将用户ID设置到会话存储时使用默认键的实现示例。

.. code-block:: java

  SessionUtil.put(context, "user.id", userId);

此外，考虑到可能不是直接将用户ID存储到会话存储，而是希望将登录信息一并存储这样的需求。
在这种情况下，通过覆盖 :java:extdoc:`UserIdAttribute#getUserIdSession <nablarch.common.handler.threadcontext.UserIdAttribute.getUserIdSession(nablarch.fw.ExecutionContext,java.lang.String)>` 
就可以从任意获取源获取用户ID。
以下是从以"userContext"为键设置到会话存储的对象中获取用户ID时的实现示例。
这种情况下，也需要由应用程序将对象设置到会话存储。

.. code-block:: java

  public class SessionStoreUserIdAttribute extends UserIdAttribute {
      @Override
      protected Object getUserIdSession(ExecutionContext ctx, String skey) {
          LoginUserPrincipal userContext = SessionUtil.orNull(ctx, "userContext");
          if (userContext == null) {
              return null;
          }
          return String.valueOf(userContext.getUserId());
      }
  }

.. code-block:: xml

 <component class="nablarch.common.handler.threadcontext.ThreadContextHandler">
   <property name="attributes">
     <list>
        <!-- 用户ID -->
        <component class="com.nablarch.example.proman.web.common.handler.threadcontext.SessionStoreUserIdAttribute">
          <property name="anonymousId" value="${nablarch.userIdAttribute.anonymousId}"/>
        </component>
        <!-- 其他组件定义省略 -->
     </list>
   </property>
 </component>

.. _thread_context_handler-attribute_access:

设置/获取线程上下文的属性值
-----------------------------------------------------------
访问线程上下文使用
:java:extdoc:`ThreadContext <nablarch.core.ThreadContext>` 。

.. code-block:: java

 // 获取请求ID
 String requestId = ThreadContext.getRequestId();

.. _thread_context_handler-language_selection:

制作用户选择语言的画面
-----------------------------------------------------------
在国际化对应等场景中，有时会需要制作让用户可以选择语言的画面。
在这种情况下，通过使用以下任一类和
:java:extdoc:`LanguageAttributeInHttpUtil <nablarch.common.web.handler.threadcontext.LanguageAttributeInHttpUtil>`
，可以实现用户的语言选择。

* :java:extdoc:`LanguageAttributeInHttpCookie <nablarch.common.web.handler.threadcontext.LanguageAttributeInHttpCookie>`
* :java:extdoc:`LanguageAttributeInHttpSession <nablarch.common.web.handler.threadcontext.LanguageAttributeInHttpSession>`

这里展示将语言保存在Cookie中，通过链接让用户选择语言的画面实现示例。

设置示例
 .. code-block:: xml

  <!-- 为了使用LanguageAttributeInHttpUtil，
       将组件名设置为"languageAttribute"。-->
  <component name="languageAttribute"
             class="nablarch.common.web.handler.threadcontext.LanguageAttributeInHttpCookie">
    <property name="defaultLanguage" value="ja" />
    <property name="supportedLanguages" value="ja,en" />
  </component>

JSP实现示例
  .. code-block:: jsp

    <%-- 使用n:submitLink标签输出链接，
      使用n:param标签为每个链接发送不同的语言 --%>

    <n:submitLink uri="/action/menu/index" name="switchToEnglish">

      英语

      <n:param paramName="user.language" value="en" />
    </n:submitLink>
    <n:submitLink uri="/action/menu/index" name="switchToJapanese">

      日语

      <n:param paramName="user.language" value="ja" />
    </n:submitLink>

Handler实现示例
 .. code-block:: java

  // 保持用户选择语言的Handler。
  // 考虑到在多个画面中让用户选择语言的情况，作为Handler实现。
  public class I18nHandler implements HttpRequestHandler {

      public HttpResponse handle(HttpRequest request, ExecutionContext context) {
          String language = getLanguage(request, "user.language");
          if (StringUtil.hasValue(language)) {

              // 调用LanguageAttributeInHttpUtil的keepLanguage方法，
              // 将选择的语言设置到Cookie中。
              // 同时也会设置到线程上下文中。
              // 如果指定的语言不是支持的语言，
              // 则不设置到Cookie和线程上下文。
              LanguageAttributeInHttpUtil.keepLanguage(request, context, language);
          }
          return context.handleNext(request);
      }

      private String getLanguage(HttpRequest request, String paramName) {
          if (!request.getParamMap().containsKey(paramName)) {
              return null;
          }
          return request.getParam(paramName)[0];
      }
  }

.. _thread_context_handler-time_zone_selection:

制作用户选择时区的画面
-----------------------------------------------------------
在国际化对应等场景中，有时会需要制作让用户可以选择时区的画面。
在这种情况下，通过使用以下任一类和
:java:extdoc:`TimeZoneAttributeInHttpUtil <nablarch.common.web.handler.threadcontext.TimeZoneAttributeInHttpUtil>`
，可以实现用户的时区选择。

* :java:extdoc:`TimeZoneAttributeInHttpCookie <nablarch.common.web.handler.threadcontext.TimeZoneAttributeInHttpCookie>`
* :java:extdoc:`TimeZoneAttributeInHttpSession <nablarch.common.web.handler.threadcontext.TimeZoneAttributeInHttpSession>`

这里展示将时区保存在Cookie中，通过链接让用户选择时区的画面实现示例。

设置示例
 .. code-block:: xml

  <!-- 为了使用TimeZoneAttributeInHttpUtil，
       将组件名设置为"timeZoneAttribute"。-->
  <component name="timeZoneAttribute"
             class="nablarch.common.web.handler.threadcontext.TimeZoneAttributeInHttpCookie">
    <property name="defaultTimeZone" value="Asia/Tokyo" />
    <property name="supportedTimeZones" value="Asia/Tokyo,America/New_York" />
  </component>

JSP实现示例
 .. code-block:: jsp

  <%-- 使用n:submitLink标签输出链接，
    使用n:param标签为每个链接发送不同的时区 --%>

  <n:submitLink uri="/action/menu/index" name="switchToNewYork">

    纽约

    <n:param paramName="user.timeZone" value="America/New_York" />
  </n:submitLink>
  <n:submitLink uri="/action/menu/index" name="switchToTokyo">

    东京

    <n:param paramName="user.timeZone" value="Asia/Tokyo" />
  </n:submitLink>

Handler实现示例
 .. code-block:: java

  // 保持用户选择时区的Handler。
  // 考虑到在多个画面中让用户选择时区的情况，作为Handler实现。
  public class I18nHandler implements HttpRequestHandler {

      public HttpResponse handle(HttpRequest request, ExecutionContext context) {
          String timeZone = getTimeZone(request, "user.timeZone");
          if (StringUtil.hasValue(timeZone)) {

              // 调用TimeZoneAttributeInHttpUtil的keepTimeZone方法，
              // 将选择的时区设置到Cookie中。
              // 同时也会设置到线程上下文中。
              // 如果指定的时区不是支持的时区，
              // 则不设置到Cookie和线程上下文。
              TimeZoneAttributeInHttpUtil.keepTimeZone(request, context, timeZone);
          }
          return context.handleNext(request);
      }

      private String getTimeZone(HttpRequest request, String paramName) {
          if (!request.getParamMap().containsKey(paramName)) {
              return null;
          }
          return request.getParam(paramName)[0];
      }
  }
