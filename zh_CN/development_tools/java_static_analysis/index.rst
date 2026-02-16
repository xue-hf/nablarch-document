高效的Java静态检查
=========================

.. contents:: 目录
  :depth: 2
  :local:

为了提高代码质量和可维护性，需要实践以下三点。

* :ref:`code-analysis`
* :ref:`code-format`
* :ref:`api-analysis`

为了进行上述操作，Nablarch推荐使用JetBrains公司的IDE `IntelliJ IDEA(外部网站) <https://www.jetbrains.com/idea/>`_ 。
本页面将说明使用IntelliJ IDEA进行高效的Java静态检查的方法。

.. _code-analysis:

进行Inspection
------------------

IntelliJ IDEA具有进行静态检查的 `Inspection功能(外部网站) <https://www.jetbrains.com/help/idea/code-inspection.html>`_ ，可以检查是否符合Java编码惯例、是否包含潜在的bug等，并实时发出警告。

Inspection默认设置为对一般需要注意的事项进行警告。

如果项目制定了规范，可以将其更改为适合项目的设置，从而更有效地利用Inspection。
更改后的设置可以通过导出和导入在项目开发人员之间共享。
关于导出和导入的方法，请参阅 `配置配置文件(外部网站) <https://www.jetbrains.com/help/idea/customizing-profiles.html>`_ 。

.. _code-format:

统一格式
----------------------

使用IntelliJ IDEA的代码格式化程序功能，可以在项目中统一代码风格。
关于使用方法，请参阅 `Java样式指南的Java代码格式化程序说明 <https://github.com/Fintan-contents/coding-standards/blob/main/java/code-formatter.md>`_ 。

.. _api-analysis:

检查是否使用了不允许的API
-------------------------------------------------

为此检查提供了两种工具：IntelliJ IDEA插件和不依赖于IntelliJ IDEA的SpotBugs插件。

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
使用nablarch-intellij-plugin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
`nablarch-intellij-plugin <https://github.com/nablarch/nablarch-intellij-plugin>`_ 是用于支持Nablarch开发的IntelliJ IDEA插件，具有以下功能。

* 当使用了Nablarch非公开API时发出警告
* 当使用了黑名单中注册的Java API时发出警告

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
使用不允许API检查工具
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
不允许API检查工具是作为SpotBugs插件创建的工具。
详细的规格和执行方法请参阅 `Java样式指南的不允许API检查工具说明 <https://github.com/Fintan-contents/coding-standards/blob/main/java/staticanalysis/unpublished-api/README.md>`_ 。

此外，空白项目中已预先配置了 `使用Maven执行的设置 <https://github.com/Fintan-contents/coding-standards/blob/main/java/staticanalysis/spotbugs/docs/Maven-settings.md>`_ ，因此可以立即执行检查。
