.. _`client_create`:

创建登录功能（实战教程）
==========================================
本节将通过实际为示例应用实现客户信息登录功能，  
详细介绍使用 Nablarch 开发 Web 应用登录功能的方法。

功能说明
  1. 点击页面头部菜单中的「客户登录」链接。

    .. image:: ../images/client_create/header_menu.png

  2. 显示客户登录页面。

    .. image:: ../images/client_create/input_display.png

  3. 在客户名称中输入全角字符串，从行业下拉框中选择任意值，然后点击「登录」按钮。

    .. image:: ../images/client_create/input_name_select.png

  4. 显示登录确认页面。

    .. image:: ../images/client_create/confirm_display.png

  5. 点击「确定」按钮，将客户数据保存到数据库，并显示完成页面。

    .. image:: ../images/client_create/complete_display.png

客户登录功能规格
------------------------------------------
下表列出了客户登录功能的各项处理，以及对应的 URL 和业务Action方法的映射关系。

.. image:: ../images/client_create/client_create.png

=== ================== ====================== ====================== ============
NO.  处理名称           URL                    动作类#方法             HTTP请求方式
=== ================== ====================== ====================== ============
1   初始显示           /action/client/        ClientAction#input     GET
2   确认登录内容       /action/client/confirm ClientAction#confirm   POST
3   返回登录页面       /action/client/back    ClientAction#back      POST
4   执行登录处理       /action/client/create  ClientAction#create    POST
=== ================== ====================== ====================== ============

所使用的数据库表结构定义如下。

  .. image:: ../images/client_create/client_table.png

----

本功能的详细说明分为以下四章：

.. toctree::
  :maxdepth: 1

  client_create1
  client_create2
  client_create3
  client_create4