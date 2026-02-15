.. _`client_create_4`:

向数据库注册
==========================================
本章将介绍将客户信息注册到数据库的处理。

:ref:`上一页<client_create_3>`

实现注册处理
  在 `ClientAction` 中添加执行客户信息注册的方法。

  ClientAction.java
    .. code-block:: java

      public HttpResponse create(HttpRequest request, ExecutionContext context) {

          Client client = SessionUtil.get(context, "client");

          UniversalDao.insert(client);

          SessionUtil.delete(context, "client");

          return new HttpResponse(303, "redirect://complete");
      }

  实现要点
    * 从 :ref:`session store <session_store>` 取出客户Entity，使用 :ref:`universal_dao` 注册到数据库。
    * 从 :ref:`session store <session_store>` 删除客户信息。
    * 在响应对象的跳转目标中指定重定向到注册完成画面显示处理(防止在完成画面点击浏览器刷新按钮导致客户信息重复注册)。
      关于重定向指定的状态码请参考 :ref:`web_feature_details-status_code` 。

防止重复提交
  为了防止双击按钮等情况下请求被重复发送，在业务Action和JSP两处添加控制。

  ClientAction.java
    .. code-block:: java

      @OnDoubleSubmission
      public HttpResponse create(HttpRequest request, ExecutionContext context) {

      // 实现内容不变

      }

  实现要点
    * 添加 :java:extdoc:`OnDoubleSubmission <nablarch.common.web.token.OnDoubleSubmission>` 注解，
      在业务Action方法被重复执行时跳转到错误页面。详细信息请参考 :ref:`tag-double_submission` 。

  .. tip::

    Example应用程序中设置了重复提交时的默认跳转画面。
    默认跳转目标的指定方法请参考 :ref:`tag-double_submission` 。

  /src/main/webapp/WEB-INF/view/client/create.jsp
    .. code-block:: jsp

      <!-- 不修改的部分省略 -->
      <!-- 返回输入、确定按钮仅在确认画面显示 -->
        <n:forConfirmationPage>
            <n:button uri="/action/client/back"
                      cssClass="btn btn-lg btn-light">返回输入</n:button>
            <!-- allowDoubleSubmission属性指定false -->
            <n:button uri="/action/client/create"
                      allowDoubleSubmission="false"
                      cssClass="btn btn-lg btn-success">确定</n:button>
        </n:forConfirmationPage>

  实现要点
    * 在 :ref:`tag-button_tag` 的 `allowDoubleSubmission` 属性中指定false，将添加控制重复提交的JavaScript。
    * 考虑浏览器JavaScript被禁用等情况，在服务器端也要控制重复提交。

实现注册完成画面的显示处理
  实现注册完成画面的显示处理。

  实现业务Action方法
    实现注册完成画面的显示处理。

    ClientAction.java
      .. code-block:: java

        public HttpResponse complete(HttpRequest request, ExecutionContext context) {
            return new HttpResponse("/WEB-INF/view/client/complete.jsp");
        }

  创建注册完成画面的JSP
    新建注册完成画面的JSP。

    /src/main/webapp/WEB-INF/view/client/complete.jsp
      .. code-block:: jsp

        <%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
        <%@ taglib prefix="c" uri="jakarta.tags.core" %>
        <%@ taglib prefix="n" uri="http://tis.co.jp/nablarch" %>
        <%@ page session="false" %>
        <!DOCTYPE html>
        <html>
            <head>
                <title>客户注册完成画面</title>
            </head>
            <body>
                <n:include path="/WEB-INF/view/common/menu.jsp" />
                <n:include path="/WEB-INF/view/common/header.jsp" />
                <div class="container-fluid mainContents">
                    <section class="row">
                        <div class="title-nav">
                            <span class="page-title">客户注册完成画面</span>
                        </div>
                        <div class="message-area message-info">
                            客户注册已完成。
                        </div>
                    </section>
                </div>
                <n:include path="/WEB-INF/view/common/footer.jsp" />
            </body>
        </html>

进行动作确认
  按以下步骤确认注册处理已正确实现。

  1. 显示客户注册画面。

    .. image:: ../images/client_create/input_display.png

  2. 在客户名称输入全角字符串，行业选择任意值后点击「注册」按钮。

    .. image:: ../images/client_create/input_valid_value.png

  3. 显示注册确认画面，确认 `2` 中输入的客户名称、行业以标签形式显示。

    .. image:: ../images/client_create/confirm_display.png

  4. 点击「确定」按钮，确认显示注册完成画面。

    .. image:: ../images/client_create/complete_display.png

  5. 点击侧边菜单客户栏的搜索按钮，跳转到客户搜索画面。

    .. image:: ../images/client_create/client_confirm_sidemenu.png

  6. 确认可以搜索到注册的的客户信息。

    .. image:: ../images/client_create/client_search_result.png


注册功能讲解完毕。

:ref:`返回Getting Started TOP页 <getting_started>`
