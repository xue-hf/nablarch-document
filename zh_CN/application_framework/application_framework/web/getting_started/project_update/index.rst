.. _`project_update`:

创建更新功能
==========================================
基于Example应用程序讲解更新功能。

功能说明
  1. 点击项目一览的项目ID。

    .. image:: ../images/project_update/project_update_detail_link.png
      :scale: 80

  2. 显示目标项目的详情画面，点击变更按钮。

    .. image:: ../images/project_update/project_update_detail.png
      :scale: 80

  3. 修改要更新的项目，点击更新按钮。

    .. image:: ../images/project_update/project_update_update.png
      :scale: 80

  4. 显示更新确认画面，点击确定按钮。

    .. image:: ../images/project_update/project_update_confirm.png
      :scale: 80

  5. 数据库被更新，显示更新完成画面。

    .. image:: ../images/project_update/project_update_complete.png
      :scale: 80

更新内容的输入和确认
---------------------
按以下顺序讲解更新功能的实现方法中，更新内容的输入及确认部分。

  #. :ref:`创建Form<project_update-create_form>`
  #. :ref:`创建显示更新画面的业务Action方法<project_update-create_edit_action>`
  #. :ref:`创建更新画面的JSP<project_update-create_update_jsp>`
  #. :ref:`创建进行更新内容确认的业务Action方法<project_update-create_confirm_action>`
  #. :ref:`创建更新确认画面的JSP<project_update-create_confirm_jsp>`

.. _`project_update-create_form`:

创建Form
  创建从详情画面跳转到更新画面时接收参数的Form，以及接收更新画面编辑栏输入值的Form。

  从详情画面跳转到更新画面时接收参数的Form
    创建接收从详情画面跳转到更新画面时以路径参数(「show/:projectId」的「:projectId」部分)传递的
    目标项目ID的Form。

    ProjectTargetForm.java
      .. code-block:: java

        public class ProjectTargetForm implements Serializable {

            /** 项目ID */
            @Required
            @Domain("id")
            private String projectId;

            // getter及setter省略

  接收从更新画面输入的值的Form
    创建接收从更新画面输入的编辑后值的Form。

    ProjectUpdateForm.java
      .. code-block:: java

        public class ProjectUpdateForm implements Serializable {

            // 仅摘录部分

            /** 项目名称 */
            @Required
            @Domain("projectName")
            private String projectName;

            /**
             * 获取项目名称。
             *
             * @return 项目名称
             */
            public String getProjectName() {
                return this.projectName;
            }

            /**
             * 设置项目名称。
             *
             * @param projectName 要设置的项目名称
             */
            public void setProjectName(String projectName) {
                this.projectName = projectName;
            }
        }

    实现要点
      * 虽然输入项目与项目注册画面重复，
        但根据职责配置 :ref:`Form应该按HTML表单单位创建<application_design-form_html>` ，因此创建项目更新画面专用的Form。

.. _`project_update-create_edit_action`:

创建显示更新画面的业务Action方法
  创建从数据库获取当前信息并显示更新画面的业务Action方法。

  ProjectAction.java
    .. code-block:: java

        @InjectForm(form = ProjectTargetForm.class)
        public HttpResponse edit(HttpRequest request, ExecutionContext context) {

            // 删除更新处理中使用的会话信息。
            SessionUtil.delete(context, "project");

            ProjectTargetForm targetForm = context.getRequestScopedVar("form");
            LoginUserPrincipal userContext = SessionUtil.get(context, "userContext");

            // 如果目标项目被其他用户删除则抛出NoDataException
            ProjectDto dto = UniversalDao.findBySqlFile(ProjectDto.class, "FIND_BY_PROJECT",
                    new Object[]{targetForm.getProjectId(), userContext.getUserId()});

            // 将输出信息设置到request scope
            context.setRequestScopedVar("form", dto);

            SessionUtil.put(context, "project", BeanUtil.createAndCopy(Project.class, dto));

            return new HttpResponse("/WEB-INF/view/project/update.jsp");
        }

  实现要点
    * 为了获取要在编辑Form中初始显示的值，
      使用 :java:extdoc:`UniversalDao#findBySqlFile <nablarch.common.dao.UniversalDao.findBySqlFile(java.lang.Class,java.lang.String,java.lang.Object)>`
      进行主键搜索。
      为了 :ref:`获取JOIN表的结果<universal_dao-join>` ，搜索结果用Bean接收。
      主键搜索时，如果目标数据不存在则抛出 :java:extdoc:`NoDataException<nablarch.common.dao.NoDataException>` 。

        .. tip::
          Example应用程序中添加了自定义错误控制handler，因此发生 :java:extdoc:`NoDataException<nablarch.common.dao.NoDataException>` 时会跳转到404错误画面。
          handler进行错误控制的创建方法请参考 :ref:`在handler中根据异常类跳转到对应错误页面 <forward_error_page-handler>` 。

    * 考虑到编辑中可能被其他用户更新，为了使用编辑开始时的版本号进行 :ref:`乐观锁<universal_dao_jpa_version>` (后述)，
      将编辑开始时的Entity注册到 :ref:`session_store` 。

.. _`project_update-create_update_jsp`:

创建更新画面的JSP
  关于画面的创建，在注册篇的 :ref:`client_create_1` 中已经说明，此处省略。

.. _`project_update-create_confirm_action`:

创建进行更新内容确认的业务Action方法
  创建验证更新内容并显示确认画面的业务Action方法。
  除了 :ref:`bean_validation` 外，还在业务Action方法内实现了伴随数据库搜索的验证。

  ProjectAction.java
    .. code-block:: java

      @InjectForm(form = ProjectUpdateForm.class, prefix = "form")
      @OnError(type = ApplicationException.class,
              path = "/WEB-INF/view/project/update.jsp")
      public HttpResponse confirmOfUpdate(HttpRequest request, ExecutionContext context) {
          ProjectUpdateForm form = context.getRequestScopedVar("form");

          // 搜索数据库确认是否存在具有输入ID的客户
          if (form.hasClientId()) {
              if (!UniversalDao.exists(Client.class, "FIND_BY_CLIENT_ID",
                      new Object[] {Integer.parseInt(form.getClientId()) })) {
                          throw new ApplicationException(
                              MessageUtil.createMessage(MessageLevel.ERROR,
                                  "errors.nothing.client", form.getClientId()));

              }
          }

          Project project = SessionUtil.get(context, "project");

          // 将Form的值覆盖到会话
          BeanUtil.copy(form, project);

          // 将输出信息设置到request scope
          context.setRequestScopedVar("form", BeanUtil.createAndCopy(ProjectDto.class, form));
          context.setRequestScopedVar("profit", new ProjectProfit(
                  project.getSales(),
                  project.getCostOfGoodsSold(),
                  project.getSga(),
                  project.getAllocationOfCorpExpenses()
          ));

          return new HttpResponse("/WEB-INF/view/project/confirmOfUpdate.jsp");
      }

  实现要点
    * 需要数据库搜索的验证写在业务Action方法中。
      确认数据存在时，使用 :java:extdoc:`UniversalDao#exists <nablarch.common.dao.UniversalDao.exists(java.lang.Class,java.lang.String,java.lang.Object)>`
      。详细信息请参考 :ref:`需要数据库搜索的验证<bean_validation-database_validation>` 。
    * 根据职责配置 :ref:`不应直接将Form存储到session store<session_store-form>` ，因此需要转换到Bean。

  创建SQL
    为了确认客户存在，创建从客户ID获取客户信息的SQL。

    client.sql
      .. code-block:: sql

        FIND_BY_CLIENT_ID =
        SELECT
            CLIENT_ID,
            CLIENT_NAME,
            INDUSTRY_CODE
        FROM
            CLIENT
        WHERE
            CLIENT_ID = :clientId

      实现要点
        * 存在确认用的SQL以SELECT文形式创建。

.. _`project_update-create_confirm_jsp`:

创建更新确认画面的JSP
  复用更新画面创建更新确认画面。

  /src/main/webapp/WEB-INF/view/project/update.jsp
    .. code-block:: jsp

      <n:form useToken="true">
        <!-- 注册内容的确认部分 -->
          <div class="title-nav page-footer">
              <!-- 页面下部的按钮部分 -->
              <div class="button-nav">
                  <n:forInputPage>
                      <!-- 输入画面用按钮部分 -->
                  </n:forInputPage>
                  <n:forConfirmationPage>
                      <!-- 确认画面用按钮部分 -->
                      <n:submit value = "确定" uri="/action/project/update" id="bottomSubmitButton"
                              cssClass="btn btn-lg btn-success"
                              allowDoubleSubmission="false" type="button" />
                  </n:forConfirmationPage>
              </div>
          </div>
      </n:form>

  实现要点
    * 复用更新画面作为确认画面的方法在 :ref:`注册功能的确认画面创建<client_create_forConfirmationPage>` 中已经说明，此处省略。
    * 为了添加防止重复提交的JavaScript，在 :ref:`tag-submit_tag` 的 `allowDoubleSubmission` 属性中指定false。
      详细信息请参考 :ref:`tag-double_submission` 。

数据库更新
---------------------
按以下顺序讲解更新功能的实现方法中，更新内容确认部分。

  #. :ref:`创建业务Action方法<project_update-create_decide_action>`
  #. :ref:`创建更新完成画面<project_update-create_success_jsp>`

.. _`project_update-create_decide_action`:

创建业务Action方法
  创建更新数据库并确认变更的业务Action方法。
  同时讲解用于进行 :ref:`乐观锁<universal_dao_jpa_version>` 的Entity定义。

  创建进行数据库更新的业务Action方法
    创建更新数据库并重定向到完成画面显示方法的业务Action方法。

      ProjectAction.java
        .. code-block:: java

          @OnDoubleSubmission
          public HttpResponse update(HttpRequest request, ExecutionContext context) {
              Project targetProject = SessionUtil.delete(context, "project");
              UniversalDao.update(targetProject);

              return new HttpResponse(303, "redirect://completeOfUpdate");
          }

    实现要点
      * 在Entity中设置要更新的值，使用 :java:extdoc:`UniversalDao#update <nablarch.common.dao.UniversalDao.update(java.lang.Object)>` 更新数据库。
        更新处理中会执行乐观锁。
      * 为了防止重复提交，添加 :java:extdoc:`@OnDoubleSubmission <nablarch.common.web.token.OnDoubleSubmission>` 注解。
      * 为防止浏览器刷新导致的再次执行，将响应重定向。
      
        * 关于资源路径格式请参考 :java:extdoc:`ResourceLocator <nablarch.fw.web.ResourceLocator>` 。
        * 关于重定向指定的状态码请参考 :ref:`web_feature_details-status_code` 。

  创建作为乐观锁对象的Entity
    创建启用 :ref:`乐观锁<universal_dao_jpa_version>` 的Entity。

    Project.java
      .. code-block:: java

        // 其他属性省略

        /** 版本号 */
        private Long version;

        /**
         * 返回版本号。
         *
         * @return 版本号
         */
        @Version
        @Column(name = "VERSION", precision = 19, nullable = false, unique = false)
        public Long getVersion() {
            return version;
        }

        /**
         * 设置版本号。
         *
         * @param version 版本号
         */
        public void setVersion(Long version) {
            this.version = version;
        }

    实现要点
      * 为了进行 :ref:`乐观锁<universal_dao_jpa_version>` ，在Entity中创建 `version` 属性，
        并在getter上添加 :ref:`@Version <universal_dao_jpa_version>` 注解。

  .. _`project_update-create_complete_action`:

  创建显示完成画面的业务Action方法
    创建作为更新方法重定向目标的、显示完成画面的业务Action方法。

    ProjectAction.java
      .. code-block:: java

        public HttpResponse completeOfUpdate(HttpRequest request, ExecutionContext context) {
            return new HttpResponse("/WEB-INF/view/project/completeOfUpdate.jsp");
        }

.. _`project_update-create_success_jsp`:

创建更新完成画面
  创建更新完成画面。

  /src/main/webapp/WEB-INF/view/project/completeOfUpdate.jsp
    .. code-block:: jsp

      <n:form>
          <div class="title-nav">
              <h1 class="page-title">项目变更完成画面</h1>
              <div class="button-nav">
                <!-- 省略 -->
              </div>
          </div>
          <div class="message-area message-info">
              项目更新已完成。
          </div>
          <!-- 省略 -->
      </n:form>

更新功能讲解完毕。

:ref:`返回Getting Started TOP页 <getting_started>`
