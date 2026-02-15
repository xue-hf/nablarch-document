.. _http_access_log_handler:

HTTP访问日志handler
==================================================
.. contents:: 目录
  :depth: 3
  :local:

输出 :ref:`HTTP访问日志 <http_access_log>` 的handler。

本handler执行以下处理。

* 请求处理开始时输出访问日志
* 请求处理完成时输出访问日志

处理流程如下。

.. image:: ../images/HttpAccessLogHandler/flow.png

handler类名
--------------------------------------------------
* :java:extdoc:`nablarch.common.web.handler.HttpAccessLogHandler`

模块列表
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web</artifactId>
  </dependency>

约束
--------------------------------------------------

应配置在 :ref:`thread_context_handler` 之后
  从此handler调用的日志输出处理中，通常需要 :java:extdoc:`ThreadContext <nablarch.core.ThreadContext>` 中保存的内容。
  因此，需要配置在 :ref:`thread_context_handler` 之后。

应配置在 :ref:`http_error_handler` 之前
  此外，完成时的日志输出需要错误代码，因此需要配置在 :ref:`http_error_handler` 之前。

输出会话存储ID时应配置在 :ref:`session_store_handler` 之后
  详细请参考 :ref:`http_access_log-session_store_id` 。

访问日志输出内容的切换
--------------------------------------------------

访问日志输出内容的切换方法请参考 :ref:`log` 和 :ref:`http_access_log` 。
