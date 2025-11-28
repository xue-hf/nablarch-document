.. _view_other:

使用其他模板引擎进行页面开发
==================================================
说明使用 :ref:`web_thymeleaf_adaptor` 以外的模板引擎的应对方法。

如果使用的模板引擎提供了通过 Servlet forward 向客户端返回响应的 Servlet，
则只需在 ``web.xml`` 中注册该Servlet即可。

对于不提供Servlet的模板引擎，
可以像 :ref:`web_thymeleaf_adaptor` 一样，实现 :java:extdoc:`CustomResponseWriter <nablarch.fw.web.handler.responsewriter.CustomResponseWriter>` 接口来完成适配。

有关具体实现方法和配置方法的详细信息，请参考以下文档和源码：

* :ref:`web_thymeleaf_adaptor`
* `Web应用 Thymeleaf适配器的源码 <https://github.com/nablarch/nablarch-web-thymeleaf-adaptor>`_
