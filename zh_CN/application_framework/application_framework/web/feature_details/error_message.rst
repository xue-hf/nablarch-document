在页面上显示错误消息
==================================================
服务端执行校验后的消息存储通过 :ref:`http_error_handler` 存储在了请求scope中。
模板引擎通过访问请求scope中的错误消息便能够将错误消息显示在页面上。
请求scope的参数名请参考 :ref:`向请求scope中配置错误消息 <http_error_handler-error_messages>`

.. tip::

  虽然在使用JSP的情况下可以通过 :ref:`使用自定义的tag显示错误 <tag-write_error>` ，
  由于自定义标签输出的DOM结构存在限制，可能导致与CSS框架的兼容性较差。

  当使用存储在请求scope中的对象时，由于不再受DOM结构的限制，因此在JSP中可以直接访问请求作用域对象并显示错误消息。
  

以下是使用 :ref:`Thymeleaf <web_thymeleaf_adaptor>` 进行实现的例子。

若要显示与特定属性对应的错误消息，
  可使用 :java:extdoc:`ErrorMessages#hasError <nablarch.fw.web.message.ErrorMessages.hasError(java.lang.String)>` 或
  :java:extdoc:`ErrorMessages#getMessage <nablarch.fw.web.message.ErrorMessages.getMessage(java.lang.String)>` 方法，
  以判断是否存在与属性（即输入字段的 `name` 属性值）相关的错误，并显示对应的消息。

  在本例中，当请求作用域中存在与 ``form.userName`` 属性对应的错误消息时，将显示该消息。

  .. code-block:: html

    <input type='text' name='form.txt' />
    <span class="error" th:if="${errors.hasError('form.userName')}"
      th:text="${errors.getMessage('form.userName')}">请输入内容。</span>

若要显示全局消息（即不与特定属性关联的消息），
  可使用 :java:extdoc:`ErrorMessages#getGlobalMessages() <nablarch.fw.web.message.ErrorMessages.getGlobalMessages()>` 方法来输出全局消息。

  .. code-block:: html

    <ul>
      <li th:each="message : ${errors.globalMessages}" th:text="${message}"></li>
    </ul>

若要显示所有消息（包括字段相关消息和全局消息），
  可使用 :java:extdoc:`ErrorMessages#getAllMessages() <nablarch.fw.web.message.ErrorMessages.getAllMessages()>` 方法来输出全部消息。

  .. code-block:: html

    <ul>
      <li th:each="message : ${errors.allMessages}" th:text="${message}">错误消息</li>
    </ul>

