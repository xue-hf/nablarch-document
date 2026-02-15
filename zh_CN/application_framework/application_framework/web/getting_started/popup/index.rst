.. _`client_popup`:

创建弹出窗口画面
==========================================
基于Example应用程序讲解弹出窗口画面的创建方法。

弹出窗口画面按照 :ref:`tag-submit_popup` 的说明，不是以独立窗口而是以对话框形式创建。

功能说明
  1. 点击项目详情画面的变更按钮。

    .. image:: ../images/popup/popup-project_update_btn.png
      :scale: 80

  2. 点击客户栏的搜索按钮。

    .. image:: ../images/popup/popup-project_update.png
      :scale: 75

  3. 客户搜索画面以对话框形式显示。点击搜索按钮。

    .. image:: ../images/popup/popup-popup_init.png
      :scale: 60

  4. 点击搜索结果的客户ID链接。

    .. image:: ../images/popup/popup-popup_search.png
      :scale: 80

  5. 客户搜索画面关闭，所选值设置到项目变更画面的客户ID和客户名称。

    .. image:: ../images/popup/popup-complete.png
      :scale: 80

显示弹出窗口(对话框)
------------------------------------------------
弹出窗口(对话框)的显示使用OSS(Bootstrap)实现。
详细信息请参考 `Bootstrap文档(外部站点) <https://getbootstrap.jp/docs/5.3/getting-started/introduction/>`_ 。

.. _`popup-action`:

创建业务Action方法
  搜索客户并将选择结果传递给父画面。
  
  本功能通过从对话框进行Ajax调用来实现搜索处理。
  Action类的实现方法请参考 :ref:`restful_web_service` 。

.. _`popup-popup_jsp`:

创建弹出窗口画面的JSP
  使用jQuery基于Ajax调用结果构建DOM并显示结果。
  由于使用了jQuery，详细说明省略。
  
  关于jQuery请参考 `文档(外部站点，英文) <https://jquery.com/>`_ 。

.. _`popup-parent_hand_over`:

创建从弹出窗口画面向父窗口传递值的JavaScript函数
  使用jQuery将对话框内的信息设置到客户名称和客户ID区域。
  由于使用了jQuery，详细说明省略。
  
  关于jQuery请参考 `文档(外部站点，英文) <https://jquery.com/>`_ 。
  
弹出窗口画面的讲解完毕。

:ref:`返回Getting Started TOP页 <getting_started>`
