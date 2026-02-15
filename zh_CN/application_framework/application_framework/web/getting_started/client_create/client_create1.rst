.. _`client_create_1`:

创建注册画面初始显示
==========================================
本章将介绍注册画面的初始显示。

创建注册画面的JSP
  将JSP模板文件放置到 `/src/main/webapp/WEB-INF/view/client` 目录下。

     :download:`create.jsp <../downloads/client_create/create.jsp>`

实现画面初始显示部分
  向create.jsp添加注册画面的内容。

  /src/main/webapp/WEB-INF/view/client/create.jsp
    .. code-block:: jsp

      <n:form>
          <div class="row m-3">
              <label class="col-md-2 col-form-label fs-5">客户名称</label>
              <!-- 客户名称的文本框 -->
              <!-- 由于Form尚未创建，name属性暂时使用临时值 -->
              <div class="col-md-10 form-group">
                  <n:text name="tmp" cssClass="form-control form-control-lg"/>
              </div>
          </div>
          <div class="row m-3">
              <label class="col-md-2 col-form-label fs-5">行业</label>
              <!-- 行业的下拉框 -->
              <!-- 由于Form尚未创建，name属性暂时使用临时值 -->
              <div class="col-md-10 form-group">
                  <n:select
                          listName="industries"
                          elementValueProperty="industryCode"
                          elementLabelProperty="industryName"
                          name="tmp"
                          withNoneOption="true"
                          cssClass="form-select form-select-lg"/>
              </div>
          </div>
          <div class="button-nav">
              <!-- 注册按钮 -->
              <!-- 由于注册内容确认画面尚未创建，uri属性暂时使用临时值 -->
              <n:button
                      uri="tmp"
                      cssClass="btn btn-lg btn-success">注册</n:button>
          </div>
      </n:form>

  实现要点
    * 使用 :ref:`tag` 创建文本输入框和下拉框。
      参考 :ref:`tag-input_form` 。
    * 在 :ref:`tag-select_tag` 的 `listName` 属性中指定后续初始显示方法注册到request scope的行业列表名称，用于下拉框显示。
      参考 :ref:`tag-selection` 。

在业务Action中创建初始显示方法
  在 `ClientAction` 中添加执行以下处理的业务Action方法

    * 获取下拉框显示的数据并注册到request scope。
    * forward到初始显示画面的JSP。

    ClientAction.java
      .. code-block:: java

        public HttpResponse input(HttpRequest request, ExecutionContext context) {
            EntityList<Industry> industries = UniversalDao.findAll(Industry.class);
            context.setRequestScopedVar("industries", industries);
            return new HttpResponse("/WEB-INF/view/client/create.jsp");
        }

    业务Action方法的签名必须符合以下条件。
    如果业务Action方法不满足以下签名，将发生404错误。

    .. java:method:: public HttpResponse methodName(HttpRequest request, ExecutionContext context)

      :param request: 框架传递的请求对象

      :param context: 框架传递的执行上下文

      :param return: 设置了跳转目标的响应对象


    实现要点
      * 为了在注册画面显示行业下拉框，使用 :ref:`universal_dao` 从数据库获取所有行业信息。
      * 为了向JSP传递值，将获取的行业列表注册到request scope。

URL与业务Action的映射
  映射处理使用OSS库 `http_request_router(外部站点) <https://github.com/kawasima/http-request-router>`_ 。
  添加将指定URL与初始显示处理进行映射的设置。

    routes.xml
      .. code-block:: xml

        <routes>
          <!-- 从上往下评估，所以要在其他映射之前设置 -->
          <get path="/action/client" to="Client#input"/>
          <!-- 其他设置省略 -->
        </routes>

    .. tip::
      routes.xml的指定方法请参考 `库的README文档(外部站点) <https://github.com/kawasima/http-request-router/blob/master/README.ja.md>`_ 。

创建注册画面的链接
  在头部菜单中创建客户注册画面的链接。

  /src/main/webapp/WEB-INF/view/common/menu.jsp
    .. code-block:: jsp

      <ul class="navbar-nav me-auto">
        <!-- 其他链接省略 -->
        <li class="nav-item px-2">
          <n:a href="/action/client" cssClass="nav-link">客户注册</n:a>
        </li>
      </ul>

  实现要点
    * 使用 :ref:`tag` 的 :ref:`tag-a_tag` 创建链接。

进行动作确认
  按以下步骤进行动作确认。

  1. 登录应用程序，确认头部菜单中已创建「客户注册」链接。

    .. image:: ../images/client_create/header_menu.png

  2. 点击「客户注册」链接后跳转到客户注册画面，确认显示了「客户名称」表单、「行业」下拉框和注册按钮。

    .. image:: ../images/client_create/initial_display.png

  3. 确认「行业」下拉框可以选择。

    .. image:: ../images/client_create/initial_display_select.png

:ref:`下一页<client_create_2>`
