.. _`project_bulk_update`:

创建批量更新功能
==========================================
基于Example应用程序讲解批量更新功能。

功能说明
  1. 点击菜单的批量更新链接，跳转到批量更新画面。

    .. image:: ../images/project_bulk_update/project_bulk_update-menu.png
      :scale: 80

  2. 显示项目全件搜索结果。

    .. image:: ../images/project_bulk_update/project_bulk_update-list.png
      :scale: 80

  3. 在该页面改写要更新的项目，点击更新按钮(不能跨页更新)。

    .. image:: ../images/project_bulk_update/project_bulk_update-list_changed.png
      :scale: 80

  4. 显示更新确认画面，点击确定按钮。

    .. image:: ../images/project_bulk_update/project_bulk_update-confirm.png
      :scale: 80

  5. 数据库被更新，显示更新完成画面。

    .. image:: ../images/project_bulk_update/project_bulk_update-complete.png
      :scale: 80

创建批量更新功能
---------------------
讲解批量更新功能的创建方法。

  #. :ref:`创建Form<project_bulk_update-create_form>`
  #. :ref:`创建向画面传递更新目标的Bean<project_bulk_update-create_bean>`
  #. :ref:`创建显示批量更新画面的业务Action方法<project_bulk_update-action_list>`
  #. :ref:`创建批量更新画面JSP<project_bulk_update-update_jsp>`
  #. :ref:`创建确认更新内容的业务Action方法<project_bulk_update-confirm_action>`
  #. :ref:`创建确认画面JSP<project_bulk_update-confirm_jsp>`
  #. :ref:`创建批量更新数据库的业务Action方法<project_bulk_update-bulk_update>`
  #. :ref:`创建完成画面<project_bulk_update-complete_jsp>`

.. _`project_bulk_update-create_form`:

创建Form
  分别创建接收搜索条件的Form和接收更新内容的Form。

  创建搜索Form
    搜索Form的实现与 :ref:`创建搜索功能：创建Form<project_search-create_form>` 相同，请参考。

  创建更新Form
    为了批量发送多个项目的更新信息，创建两种Form。

      #. :ref:`接收单个项目更新信息的Form<project_bulk_update-create_single_pj_form>`
      #. :ref:`以单个项目Form列表作为属性的父Form<project_bulk_update-create_multi_pj_form>`

        .. image:: ../images/project_bulk_update/project_bulk_update-form.png

    .. _`project_bulk_update-create_single_pj_form`:

    接收单个项目更新信息的Form
      创建接收单个项目更新值的Form。

        InnerProjectForm.java
          .. code-block:: java

            public class InnerProjectForm implements Serializable {

                // 仅摘录部分项目

                /** 项目名称 */
                @Required
                @Domain("projectName")
                private String projectName;

                // getter及setter省略
            }

      实现要点
        * 为了对嵌套Form也执行 :ref:`Bean Validation<bean_validation>` ，
          需要添加 :java:extdoc:`@Required<nablarch.core.validation.ee.Required>` 或 :java:extdoc:`@Domain<nablarch.core.validation.ee.Domain>`
          等验证用注解。

    .. _`project_bulk_update-create_multi_pj_form`:

    以单个项目Form列表作为属性的父Form
      为了批量接收多个项目的更新信息，创建定义了接收单个项目更新信息Form列表的父Form。

      ProjectBulkForm.java
        .. code-block:: java

          public class ProjectBulkForm implements Serializable {

              /** 项目信息列表 */
              @Valid
              private List<InnerProjectForm> projectList = new ArrayList<>();

              // getter及setter省略
          }

      实现要点
        * 通过添加 :java:extdoc:`@Valid<jakarta.validation.Valid>` 注解，可以将嵌套的Form也纳入 :ref:`Bean Validation<bean_validation>` 的对象。

.. _`project_bulk_update-create_bean`:

创建向画面传递业务Action获取的更新目标列表的Bean
  创建向画面传递业务Action获取的更新目标列表的Bean。此Bean会在批量更新画面和确认画面间传递，因此注册到 :ref:`session store <session_store>` 。

    ProjectListDto.java
      .. code-block:: java

        public class ProjectListDto implements Serializable {

            /** 项目列表 */
            private List<Project> projectList = new ArrayList<>();

            // getter及setter省略
        }

    实现要点
      * 将数组或集合类型注册到 :ref:`session store <session_store>` 时，需要定义为可序列化Bean的属性，
        然后将该Bean注册到 :ref:`session store <session_store>` 。详细信息请参考 :ref:`session store使用上的限制<session_store-constraint>` 。

.. _`project_bulk_update-action_list`:

创建显示批量更新画面的业务Action方法
  创建从数据库获取目标项目并显示在批量更新画面的业务Action方法。

  ProjectBulkAction.java
    .. code-block:: java

      @InjectForm(form = ProjectSearchForm.class, prefix = "searchForm",  name = "searchForm")
      @OnError(type = ApplicationException.class, path = "forward://initialize")
      public HttpResponse list(HttpRequest request, ExecutionContext context) {

          ProjectSearchForm searchForm = context.getRequestScopedVar("searchForm");

          // 执行搜索
          ProjectSearchDto projectSearchDto
              = BeanUtil.createAndCopy(ProjectSearchDto.class, searchForm);
          EntityList<Project> projectList = searchProject(projectSearchDto, context);
          ProjectListDto projectListDto = new ProjectListDto();
          projectListDto.setProjectList(projectList);
          SessionUtil.put(context, "projectListDto", projectListDto);

          // 将更新目标传递到画面
          context.setRequestScopedVar("bulkForm", projectListDto);

          // 保存搜索条件
          SessionUtil.put(context, "projectSearchDto", projectSearchDto);

          return new HttpResponse("/WEB-INF/view/projectBulk/update.jsp");
      }

  实现要点
    * 关于搜索方法的实现请参考 :ref:`创建搜索功能：实现业务Action<project_search-create_action>` 。
    * 为了从确认画面返回批量更新画面时能以相同条件进行分页或再搜索，
      将搜索条件注册到 :ref:`session store <session_store>` 进行传递。

.. _`project_bulk_update-update_jsp`:

创建批量更新画面JSP
  创建显示搜索结果和编辑多个项目信息的批量更新画面JSP。

  /src/main/webapp/WEB-INF/projectBulk/update.jsp
    .. code-block:: jsp

      <!-- 客户搜索结果显示部分 -->
      <n:form>
          <!-- 将当前搜索结果显示使用的搜索条件作为参数持有的URI，
               作为变量注册到page scope。
               此变量用作<app:listSearchResult>标签的分页用URI。-->
          <c:url value="list" var="uri">
              <!-- 从session store上的projectSearchDto获取搜索条件 -->
              <c:param name="searchForm.clientId" value="${projectSearchDto.clientId}"/>
              <c:param name="searchForm.clientName" value="${projectSearchDto.clientName}"/>
              <c:param name="searchForm.projectName" value="${projectSearchDto.projectName}"/>
              <!-- 以下同样是搜索条件参数因此省略 -->

          </c:url>
          <app:listSearchResult>
          <!-- listSearchResult的属性值省略 -->
              <jsp:attribute name="headerRowFragment">
                  <tr>
                      <th>项目ID</th>
                      <th>项目名称</th>
                      <th>项目类型</th>
                      <th>开始日期</th>
                      <th>结束日期</th>
                  </tr>
              </jsp:attribute>
              <jsp:attribute name="bodyRowFragment">
                  <tr class="info">
                      <td>
                          <!-- 显示以项目ID为参数的链接 -->
                          <n:a href="show/${row.projectId}">
                              <n:write name="bulkForm.projectList[${status.index}].projectId"/>
                          </n:a>
                          <n:plainHidden name="bulkForm.projectList[${status.index}].projectId"/>
                      </td>
                      <td>
                          <div class="form-group">
                              <n:text name="bulkForm.projectList[${status.index}].projectName"
                                      maxlength="64" cssClass="form-control form-control-lg"
                                      errorCss="input-error"/>
                              <n:error errorCss="message-error"
                                      name="bulkForm.projectList[${status.index}].projectName" />
                          </div>
                      </td>
                      <!-- 其他编辑项目省略 -->

                  </tr>
              </jsp:attribute>
          </app:listSearchResult>
          <div class="title-nav page-footer">
              <div class="button-nav">
                  <n:button id="bottomUpdateButton" uri="/action/projectBulk/confirmOfUpdate"
                      disabled="${isUpdatable}" cssClass="btn btn-lg btn-success">
                          更新</n:button>
                  <n:a id="bottomCreateButton" type="button" uri="/action/project"
                      cssClass="btn btn-lg btn-light" value="新規登録"></n:a>
              </div>
          </div>
      </n:form>

  实现要点
    * 搜索结果显示JSP的创建方法与 :ref:`创建搜索功能：创建搜索结果显示部分<project_search-create_result_jsp>` 相同，请参考。
    * 为了从确认画面返回批量更新画面时能进行相同条件的再搜索或分页，基于从 :ref:`session store <session_store>` 获取的搜索条件构建搜索条件参数。
      在JSP中，注册到 :ref:`session store <session_store>` 的对象可以与注册到request scope的对象同样处理。
    * 数组型或 :java:extdoc:`List<java.util.List>` 型属性的元素可以通过 `属性名[index]` 形式访问。
      详细信息请参考 :ref:`tag-access_rule` 。

.. _`project_bulk_update-confirm_action`:

创建确认更新内容的业务Action方法
  创建确认更新内容的业务Action方法。

  ProjectBulkAction.java
    .. code-block:: java

      @InjectForm(form = ProjectBulkForm.class, prefix = "bulkForm", name = "bulkForm")
      @OnError(type = ApplicationException.class, path = "/WEB-INF/view/projectBulk/update.jsp")
      public HttpResponse confirmOfUpdate(HttpRequest request, ExecutionContext context) {

          ProjectBulkForm form = context.getRequestScopedVar("bulkForm");
          ProjectListDto dto = SessionUtil.get(context, "projectListDto");

          // 将更新内容覆盖到会话
          final List<InnerProjectForm> innerForms = form.getProjectList();
          dto.getProjectList()
             .forEach(project ->
                     innerForms.stream()
                               .filter(innerForm ->
                                       Objects.equals(innerForm.getProjectId(), project.getProjectId()
                                                                                       .toString()))
                               .findFirst()
                               .ifPresent(innerForm -> BeanUtil.copy(innerForm, project)));

          return new HttpResponse("/WEB-INF/view/projectBulk/confirmOfUpdate.jsp");
      }

  实现要点
    * 更新信息保存在 :ref:`session store <session_store>` 中。

.. _`project_bulk_update-confirm_jsp`:

创建确认画面JSP
  创建显示变更后项目信息的画面JSP。

  /src/main/webapp/WEB-INF/projectBulk/confirmOfUpdate.jsp
    .. code-block:: jsp

          <section>
              <div class="title-nav">
                  <span>项目搜索一览更新画面</span>
                  <div class="button-nav">
                      <n:form useToken="true">
                        <!-- 按钮部分省略 -->
                      </n:form>
                  </div>
              </div>
              <h2 class="font-group my-3">项目变更一览</h2>
              <div>
                  <table class="table table-striped table-hover">
                      <tr>
                          <th>项目ID</th>
                          <th>项目名称</th>
                          <th>项目类型</th>
                          <th>开始日期</th>
                          <th>结束日期</th>
                      </tr>
                      <c:forEach var="row" items="${projectListDto.projectList}">
                          <tr class="<n:write name='oddEvenCss' />">
                              <td>
                                  <n:write name="row.projectId" />
                              </td>
                              <!-- 其他项目省略 -->
                          </tr>
                      </c:forEach>
                  </table>
              </div>
          </section>

.. _`project_bulk_update-bulk_update`:

创建批量更新数据库的业务Action方法
  批量更新目标项目。

  ProjectBulkAction.java
    .. code-block:: java

      @OnDoubleSubmission
      public HttpResponse update(HttpRequest request, ExecutionContext context) {

        ProjectListDto projectListDto = SessionUtil.get(context, "projectListDto");
        projectListDto.getProjectList().forEach(UniversalDao::update);

        return new HttpResponse(303, "redirect://completeOfUpdate");
      }

  实现要点
    * 基本实现方法与 :ref:`创建更新功能：创建更新数据库的业务Action方法<project_update-create_decide_action>` 相同。
    * 执行更新次数份的 :java:extdoc:`UniversalDao#update <nablarch.common.dao.UniversalDao.update(java.lang.Object)>` 。
      发生并发控制错误时全部更新都会回滚。

      .. tip::
        Example应用程序中添加了自定义错误控制handler，因此 :java:extdoc:`OptimisticLockException<jakarta.persistence.OptimisticLockException>` 发生时
        会跳转到并发控制错误画面。handler进行错误控制的创建方法请参考 :ref:`在handler中根据异常类跳转到对应错误页面 <forward_error_page-handler>` 。

    * :java:extdoc:`UniversalDao<nablarch.common.dao.UniversalDao>` 也提供了以Entity列表为参数的
      :java:extdoc:`UniversalDao#batchUpdate <nablarch.common.dao.UniversalDao.batchUpdate(java.util.List)>` 方法，
      但此方法是以 :ref:`批量执行<universal_dao-batch_execute>` 使用为前提的，不进行并发控制。
      需要并发控制时，请使用 :java:extdoc:`UniversalDao#update <nablarch.common.dao.UniversalDao.update(java.lang.Object)>`
      。

.. _`project_bulk_update-complete_jsp`:

显示完成画面
  完成画面的实现方法与 :ref:`创建更新功能：创建更新完成画面<project_update-create_success_jsp>` 相同，请参考。

批量更新功能讲解完毕。

:ref:`返回Getting Started TOP页 <getting_started>`
