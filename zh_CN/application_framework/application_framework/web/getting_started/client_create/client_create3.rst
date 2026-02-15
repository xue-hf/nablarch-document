.. _`client_create_3`:

从注册内容确认画面返回注册画面
==============================================
本章将介绍从注册内容确认画面返回注册画面的处理。

:ref:`上一页<client_create_2>`

实现返回注册画面的处理
  在 `ClientAction` 中添加执行返回注册画面处理的方法。

  ClientAction.java
    .. code-block:: java
      :emphasize-lines: 1,2,3,4,5,6,7,8,9,13

      public HttpResponse back(HttpRequest request, ExecutionContext context) {

          Client client = SessionUtil.get(context, "client");

          ClientForm form = BeanUtil.createAndCopy(ClientForm.class, client);
          context.setRequestScopedVar("form", form);

          return new HttpResponse("forward://input");
      }

      public HttpResponse input(HttpRequest request, ExecutionContext context) {

          SessionUtil.delete(context, "client");

          EntityList<Industry> industries = UniversalDao.findAll(Industry.class);
          context.setRequestScopedVar("industries", industries);

          return new HttpResponse("/WEB-INF/view/client/create.jsp");
      }

  实现要点
    * 从 :ref:`session store <session_store>` 获取客户信息。
    * 为了在注册画面显示获取的客户信息，使用 :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` 将客户Entity转换为Form，并注册到request scope。
    * 将响应对象的跳转目标设置为内部forward到初始显示处理
      (因为显示注册画面时需要重新获取下拉框显示的行业信息)。
    * 在初始显示处理中删除注册到 :ref:`session store <session_store>` 的对象(考虑不点击返回按钮而从头部菜单直接跳转到注册画面等情况)。

进行动作确认
  1. 显示注册画面。

    .. image:: ../images/client_create/input_display.png

  2. 在客户名称输入全角字符串，行业选择任意值后点击「注册」按钮。

    .. image:: ../images/client_create/input_valid_value.png

  3. 在确认画面点击「返回输入」按钮。

    .. image:: ../images/client_create/confirm_display.png

  4. 显示注册画面，确认 `2` 中输入的值显示在画面上。

    .. image:: ../images/client_create/input_back.png

:ref:`下一页<client_create_4>`
