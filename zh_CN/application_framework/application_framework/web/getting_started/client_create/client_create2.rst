.. _`client_create_2`:

确认注册内容
==========================================
本章将介绍确认注册内容的处理。

:ref:`上一页<client_create_1>`

向注册画面添加输入项目
  为了跳转到注册确认画面，首先在注册画面添加客户信息注册所需的以下输入项目。

  创建Form
    为了接收注册画面输入的值，新建 `ClientForm` 类。

    ClientForm.java
      .. code-block:: java

        package com.nablarch.example.app.web.form;

        public class ClientForm implements Serializable {

            // 客户名称
            private String clientName;

            // 行业代码
            private String industryCode;

            // getter、setter省略
        }

    实现要点
      * Form类中必须创建setter和getter。
      * 为了使用 :java:extdoc:`@InjectForm <nablarch.common.web.interceptor.InjectForm>` 执行验证 ( :ref:`后述<client_create-setup_validation>` )，Form需要实现 `Serializable` 接口。
      * 接收输入值的属性全部声明为String型。详细信息请参考 :ref:`验证规则的设置方法 <bean_validation-form_property>` 。

  修改注册画面的JSP
    向注册画面的JSP添加以下项目。

    * 在 :ref:`tag-text_tag` 的 `name` 属性中添加接收客户名称的Form属性名。
    * 在 :ref:`tag-select_tag` 的 `name` 属性中添加接收行业代码的Form属性名。
    * 各标签 `name` 属性的指定方法请参考 :ref:`tag-access_rule` 。
    * 向 :ref:`tag-text_tag` 、 :ref:`tag-select_tag` 添加输入错误发生时的CSS类。
    * 在注册按钮( :ref:`tag-button_tag` )的 `uri` 属性中添加跳转到注册确认画面的URI。
      `uri` 属性的指定方法请参考 :ref:`tag-specify_uri` 。
    * 添加输入错误发生时的错误消息显示区域。

    /src/main/webapp/WEB-INF/view/client/create.jsp
      .. code-block:: jsp
        :emphasize-lines: 6,7,9,20,23,25,31

        <n:form>
            <div class="row m-3">
                <label class="col-md-2 col-form-label fs-5">客户名称</label>
                <!-- 客户名称的文本框 -->
                <div class="col-md-10 form-group">
                    <n:text name="form.clientName"
                            cssClass="form-control form-control-lg" errorCss="input-error" />
                            <!-- 客户名称的输入错误时的错误消息 -->
                            <n:error errorCss="message-error mt-2" name="form.clientName" />
                </div>
            </div>
            <div class="row m-3">
                <label class="col-md-2 col-form-label fs-5">行业</label>
                <!-- 行业的下拉框 -->
                <div class="col-md-10 form-group">
                    <n:select
                            listName="industries"
                            elementValueProperty="industryCode"
                            elementLabelProperty="industryName"
                            name="form.industryCode"
                            withNoneOption="true"
                            cssClass="form-select form-select-lg"
                            errorCss="input-error" />
                    <!-- 行业的输入错误时的错误消息 -->
                    <n:error errorCss="message-error mt-2" name="form.industryCode" />
                </div>
            </div>
            <div class="button-nav">
                <!-- 注册按钮 -->
                <n:button
                        uri="/action/client/confirm"
                        cssClass="btn btn-lg btn-success">注册</n:button>
            </div>
        </n:form>

.. _`client_create_validation_rule`:

设置输入值的校验规则
  使用 :ref:`bean_validation` 设置输入值的校验规则。

  ClientForm.java
    .. code-block:: java

      @Required
      @Domain("clientName")
      private String clientName;

      @Required(message = "{nablarch.core.validation.ee.Required.select.message}")
      @Domain("industryCode")
      private String industryCode;

   messages.properties
    .. code-block:: jproperties

      #其他消息省略
      #添加适合下拉框的输入必填消息
      nablarch.core.validation.ee.Required.select.message=请选择。

  实现要点
    * 为了进行 :ref:`bean_validation` ，需要添加 `nablarch.core.validation.ee` 包下的注解
      (注意 `nablarch.core.validation.validator` 包下可能存在同名注解)。
    * 使用 :ref:`域验证 <bean_validation-domain_validation>` ，在 `ClientForm` 类的属性中定义验证规则。
    * 为了显示适合目标项目的消息，在 :java:extdoc:`Required <nablarch.core.validation.ee.Required>` 的 `message` 属性中指定自定义定义的消息。
      消息定义的详细信息请参考 :ref:`message-property_definition` 。

.. _`client_create-setup_validation`:

创建confirm方法并设置执行验证
  创建在执行前进行输入值校验的方法。

  ClientAction.java
    .. code-block:: java

      @InjectForm(form = ClientForm.class, prefix = "form")
      @OnError(type = ApplicationException.class, path = "forward://input")
      public HttpResponse confirm(HttpRequest request, ExecutionContext context) {

          // 获取验证后的对象
          ClientForm form = context.getRequestScopedVar("form");

          // 实现内容后述
      }

  实现要点
      * 在业务Action方法上添加 :java:extdoc:`InjectForm <nablarch.common.web.interceptor.InjectForm>` 注解来执行 :ref:`bean_validation` 。
      * 在 :java:extdoc:`OnError <nablarch.fw.web.interceptor.OnError>` 的 `path` 属性中设置验证错误发生时内部forward到input方法
        (因为要在注册画面显示时需要设置行业列表)。
      * 如果没有发生验证错误，可以从request scope获取验证后的对象。

实现注册确认画面的显示处理
  将后续注册处理要使用的客户信息保存到 :ref:`session_store` ，并显示注册确认画面。

  ClientAction.java
    .. code-block:: java

      @InjectForm(form = ClientForm.class, prefix = "form")
      @OnError(type = ApplicationException.class, path = "forward://input")
      public HttpResponse confirm(HttpRequest request, ExecutionContext context) {
          ClientForm form = context.getRequestScopedVar("form");

          Client client = BeanUtil.createAndCopy(Client.class, form);
          SessionUtil.put(context, "client", client);

          EntityList<Industry> industries = UniversalDao.findAll(Industry.class);
          context.setRequestScopedVar("industries", industries);

          return new HttpResponse("/WEB-INF/view/client/confirm.jsp");
      }

  实现要点
    * 与注册画面显示处理时相同，从数据库获取行业信息并设置到request scope。
    * 保存到 :ref:`session store <session_store>` 使用 :java:extdoc:`SessionUtil <nablarch.common.web.session.SessionUtil>` 。
    * 由于 :ref:`不将Form存储到session store <session_store-form>` ，
      使用 :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` 将Form转换为Entity后再注册到 :ref:`session store <session_store>` 。
    * 使用 :ref:`session store <session_store>` 时的详细实现示例请参考 :ref:`create_example` 。

.. _`client_create_forConfirmationPage`:

创建注册确认画面的JSP
  新建注册确认画面的JSP。

  /src/main/webapp/WEB-INF/view/client/confirm.jsp
    .. code-block:: jsp

      <%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
      <%@ taglib prefix="c" uri="jakarta.tags.core" %>
      <%@ taglib prefix="n" uri="http://tis.co.jp/nablarch" %>
      <!-- 将注册画面转换为确认画面显示 -->
      <n:confirmationPage path="./create.jsp" ></n:confirmationPage>

  实现要点
    * 使用 :ref:`tag-confirmation_page_tag` 可以复用注册画面的JSP来创建确认画面。详细信息请参考 :ref:`tag-make_common` 。

修改注册画面
  修改注册画面的JSP，使其可以区分仅在注册画面显示的项目和仅在确认画面显示的项目。

  /src/main/webapp/WEB-INF/view/client/create.jsp
    .. code-block:: jsp

      <div class="button-nav">
          <!-- 注册按钮仅在注册画面显示 -->
          <n:forInputPage>
              <n:button uri="/action/client/confirm"
                        cssClass="btn btn-lg btn-success">注册</n:button>
          </n:forInputPage>
          <!-- 返回输入、确定按钮仅在确认画面显示 -->
          <n:forConfirmationPage>
              <n:button uri="/action/client/back"
                        cssClass="btn btn-lg btn-light">返回输入</n:button>
              <n:button uri="/action/client/create"
                        cssClass="btn btn-lg btn-success">确定</n:button>
          </n:forConfirmationPage>
      </div>

  实现要点
    * 仅在注册画面显示的项目写在 :ref:`tag-for_input_page_tag` 内部。
    * 仅在确认画面显示的项目写在 :ref:`tag-for_confirmation_page_tag` 内部。

进行动作确认
  为了确认注册确认处理已正确实现，按以下步骤进行动作确认。

验证错误不发生的情况
  1. 显示客户注册画面。

    .. image:: ../images/client_create/input_display.png

  2. 在客户名称输入全角字符串，行业选择任意值后点击确认按钮。

    .. image:: ../images/client_create/input_valid_value.png

  3. 显示注册确认画面，确认 `2` 中输入的客户名称、行业以标签形式显示。

    .. image:: ../images/client_create/confirm_display.png

验证错误发生的情况
  1. 显示客户注册画面。

    .. image:: ../images/client_create/input_display.png

  2. 在客户名称输入半角字符串，行业保持未选择状态点击确认按钮。

    .. image:: ../images/client_create/input_invalid_value.png

  3. 注册画面再次显示，确认显示了错误消息。

    .. image:: ../images/client_create/input_invalid_display.png

:ref:`下一页<client_create_3>`
