.. _jsp_session:

JSP中禁止自动创建HTTP session的方法
===========================================================================
JSP的默认行为是在HTTP session不存在时自动创建一个新的HTTP session。
例如，在不需要HTTP session的页面（如登录画面）中，默认情况下仍会自动创建HTTP session，
导致应用服务器的内存被无谓地消耗。

因此，建议在JSP中禁用HTTP session的自动创建。

要在JSP中禁用HTTP session的自动创建，需在每个JSP文件的开头添加以下指令：

.. code-block:: jsp

  <%@ page session="false" %>


.. important::

  如果使用了 :ref:`隐藏字段加密功能（已过时功能）<tag-hidden_encryption>`，
  由于加密处理内部依赖HTTP session，因此**不能**使用上述设置，请特别注意。