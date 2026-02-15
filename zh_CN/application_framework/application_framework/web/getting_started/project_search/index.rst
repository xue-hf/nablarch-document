.. _`project_search`:

创建搜索功能
==========================================
基于Example应用程序讲解搜索功能。

功能说明
  1. 在侧边菜单「项目名称」栏输入搜索条件，点击搜索按钮。

    .. image:: ../images/project_search/project_search_sidemenu.png
      :scale: 60

  2. 显示按项目名称搜索的结果。

    .. image:: ../images/project_search/project_search_search_with_condition.png
      :scale: 80

  3. 清除项目名称，点击「按期间搜索」栏的「今年开始」链接。

    .. image:: ../images/project_search/project_search_start_date.png
          :scale: 60

  4. 显示项目开始日期为今年的项目。

    .. image:: ../images/project_search/project_search_start_date_result.png
      :scale: 80

搜索
-----------

按以下顺序说明搜索功能的基本实现方法。

  #. :ref:`创建Form<project_search-create_form>`
  #. :ref:`创建搜索条件输入部分的JSP<project_search-create_jsp>`
  #. :ref:`创建搜索条件Bean<project_search-create_bean>`
  #. :ref:`创建搜索使用的SQL<project_search-create_sql>`
  #. :ref:`实现业务Action<project_search-create_action>`
  #. :ref:`创建搜索结果显示部分<project_search-create_result_jsp>`

.. _`project_search-create_form`:

创建Form
  创建接收搜索条件的Form。

  ProjectSearchForm.java
    .. code-block:: java

      public class ProjectSearchForm extends SearchFormBase implements Serializable {

          // 仅摘录部分

          /** 项目名称 */
          @Domain("projectName")
          private String projectName;

          /** 项目开始日期（FROM） */
          @Domain("date")
          private String projectStartDateBegin;

          // getter及setter省略

  实现要点
    * 接收输入值的属性全部声明为String型。详细信息请参考 :ref:`验证规则的设置方法 <bean_validation-form_property>` 。

.. _`project_search-create_jsp`:

创建搜索条件输入部分的JSP
  创建搜索条件输入部分的JSP。

  /src/main/webapp/WEB-INF/view/common/sidemenu.jsp
    .. code-block:: jsp

      <n:form method="GET" action="list">
          <!-- 省略 -->
          <label for="projectName" class="control-label mb-3">项目名称</label>
          <div>
              <n:text
                      id="projectName"
                      name="searchForm.projectName"
                      size="25"
                      maxlength="64"
                      cssClass="form-control form-control-lg"
                      errorCss="input-error"
                      placeholder="项目名称"/>
              <n:error errorCss="message-error" name="searchForm.projectName" />
          </div>
          <!-- 省略 -->
          <div align="center">
              <input type="submit" id="search" class="btn btn-lg btn-primary" value="搜索" />
          </div>
      </n:form>

    实现要点
      * 使用GET发送请求时，在 :ref:`tag-form_tag` 的 `method` 属性中指定GET。
        此外，使用GET时不能使用自定义标签创建按钮或链接，需要用HTML创建按钮或链接。详细信息请参考 :ref:`tag-using_get` 。

.. _`project_search-create_bean`:

创建搜索条件Bean
  创建设置搜索条件并传递给 :ref:`universal_dao` 的Bean。
  Bean的属性必须是 :ref:`与对应条件列定义(类型)兼容的类型<universal_dao-search_with_condition>` 。

  ProjectSearchDto.java
    .. code-block:: java

      public class ProjectSearchDto implements Serializable {

          // 仅摘录部分

          /** 项目名称 */
          private String projectName;

          /** 项目开始日期(FROM） */
          private java.sql.Date projectStartDateBegin;

          // getter及setter省略

    实现要点
      * 使用 :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` 从Form向搜索条件Bean移送值。
        :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` 会移送属性名相同的项目，
        因此搜索条件使用的项目的属性名需要在Form和搜索条件Bean中保持一致。
      * 使用 :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` 移送值时，如果是兼容的类型，
        可以在类型转换后移送。详细信息请参考 :ref:`BeanUtil的类型转换规则<utility-conversion>` 。
      * Bean的属性使用与对应列类型匹配的Java类型定义。

.. _`project_search-create_sql`:

创建搜索使用的SQL
  创建搜索使用的SQL。

    Project.sql
      .. code-block:: none

        SEARCH_PROJECT =
        SELECT
            PROJECT_ID,
            PROJECT_NAME,
            PROJECT_TYPE,
            PROJECT_CLASS,
            PROJECT_START_DATE,
            PROJECT_END_DATE,
            VERSION
        FROM
            PROJECT
        WHERE
            USER_ID = :userId
            AND $if(clientId)     {CLIENT_ID = :clientId}
            AND $if(projectName) {PROJECT_NAME LIKE  :%projectName%}
            AND $if(projectType) {PROJECT_TYPE = :projectType}
            AND $if(projectClass) {PROJECT_CLASS IN (:projectClass[])}
            AND $if(projectStartDateBegin) {PROJECT_START_DATE >= :projectStartDateBegin}
            AND $if(projectStartDateEnd) {PROJECT_START_DATE <= :projectStartDateEnd}
            AND $if(projectEndDateBegin) {PROJECT_END_DATE >= :projectEndDateBegin}
            AND $if(projectEndDateEnd) {PROJECT_END_DATE <= :projectEndDateEnd}
        $sort(sortId){
            (idAsc PROJECT_ID)
            (idDesc PROJECT_ID DESC)
            (nameAsc PROJECT_NAME, PROJECT_ID)
            (nameDesc PROJECT_NAME DESC, PROJECT_ID DESC)
            (startDateAsc PROJECT_START_DATE, PROJECT_ID)
            (startDateDesc PROJECT_START_DATE DESC, PROJECT_ID DESC)
            (endDateAsc PROJECT_END_DATE, PROJECT_ID)
            (endDateDesc PROJECT_END_DATE DESC, PROJECT_ID DESC)
        }

    实现要点
      * 为防止SQL注入，SQL写入外部文件。详细信息请参考 :ref:`database-use_sql_file` 。
      * 使用Bean的属性名向SQL绑定值。详细信息请参考 :ref:`database-input_bean` 。
      * 仅在搜索画面输入的项目作为条件时，使用 :ref:`$if 语法构建SQL语句<database-use_variable_condition>` 。
      * 排序键可从画面选择时，使用 :ref:`$sort 语法构建SQL语句<database-make_order_by>` 。

.. _`project_search-create_action`:

实现业务Action
  在业务Action中实现搜索处理。

  创建业务Action方法
    创建基于画面给出的搜索条件进行搜索的方法。

    ProjectAction.java
      .. code-block:: java

          @InjectForm(form = ProjectSearchForm.class, prefix = "searchForm", name = "searchForm")
          @OnError(type = ApplicationException.class, path = "/WEB-INF/view/project/index.jsp")
          public HttpResponse list(HttpRequest request, ExecutionContext context) {

              ProjectSearchForm searchForm = context.getRequestScopedVar("searchForm");
              ProjectSearchDto searchCondition =
                      BeanUtil.createAndCopy(ProjectSearchDto.class, searchForm);

              List<Project> searchList = searchProject(searchCondition, context);
              context.setRequestScopedVar("searchResult", searchList);

              return new HttpResponse("/WEB-INF/view/project/index.jsp");
          }

    实现要点
      * 搜索条件来自外部的输入值，无法保证安全性，
        因此添加 :java:extdoc:`InjectForm <nablarch.common.web.interceptor.InjectForm>` 注解进行验证。
      * 通过 :java:extdoc:`InjectForm <nablarch.common.web.interceptor.InjectForm>` 完成验证的Form，
        可以从request scope中取出。
      * 使用 :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` 将Form的值复制到搜索条件Bean。

  创建搜索数据库的私有方法
    在此方法中，指定前述SQL搜索数据库。

      ProjectAction.java
        .. code-block:: java

          private List<Project> searchProject(ProjectSearchDto searchCondition,
                                              ExecutionContext context) {

              LoginUserPrincipal userContext = SessionUtil.get(context, "userContext");
              searchCondition.setUserId(userContext.getUserId());

              return UniversalDao
                      .page(searchCondition.getPageNumber())
                      .per(20L)
                      .findAllBySqlFile(Project.class, "SEARCH_PROJECT", searchCondition);
          }

      实现要点
        * 要执行前述SQL语句，需要在 :java:extdoc:`UniversalDao#findAllBySqlFile <nablarch.common.dao.UniversalDao.findAllBySqlFile(java.lang.Class,java.lang.String,java.lang.Object)>` 的第二参数中指定
          :ref:`SQLID <database-execute_sqlid>` (前述SQL的情况下是"SEARCH_PROJECT")。
        * 用于分页的搜索可以使用 :java:extdoc:`UniversalDao#per <nablarch.common.dao.UniversalDao.per(long)>` 方法、
          以及 :java:extdoc:`UniversalDao#page <nablarch.common.dao.UniversalDao.page(long)>` 。
          详细信息请参考 :ref:`为分页而缩小搜索范围<universal_dao-paging>` 。

.. _`project_search-create_result_jsp`:

创建搜索结果显示部分
  在JSP中实现将注册到request scope的搜索结果显示在画面上的处理。

  /src/main/webapp/WEB-INF/view/project/index.jsp
    .. code-block:: jsp

      <!-- 搜索结果 -->
      <app:listSearchResult>
      <!-- app:listSearchResult的属性值指定省略 -->
      <!-- 省略 -->
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
                      <!-- 创建添加了项目ID的URL -->
                      <!-- 跳转到项目详情画面 -->
                      <n:a href="show/${row.projectId}">
                          <n:write name="row.projectId"/>
                      </n:a>
                  </td>
                  <!-- 省略 -->
                  <td>
                      <n:write name="row.projectName" />
                  </td>
                  <!-- 省略 -->
                  <td>
                      <n:write name="row.projectStartDate" valueFormat="dateTime{yyyy/MM/dd}"/>
                  </td>
                  <!-- 省略 -->
              </tr>
          </jsp:attribute>
      </app:listSearchResult>

  实现要点
    * 跳转到详情画面的链接等，想要在GET请求URL中包含参数时，使用JSTL的 `<c:url>` 标签或EL表达式创建。
    * Example应用程序中设置了如下路由，因此末尾附加项目ID的URL会映射到「 `ProjectAction#show` 」。
      详细信息请参考 `库的README文档(外部站点) <https://github.com/kawasima/http-request-router/blob/master/README.ja.md>`_ 。

      routes.xml
        .. code-block:: xml

          <routes>
                <match path="/action/:controller/:action/:projectId">
                    <requirements>
                        <requirement name="projectId" value="\d+$" />
                    </requirements>
                </match>
            <!-- 其他设置省略 -->
          </routes>

    * 使用 :ref:`tag-write_tag` 输出值。
      想要以「日期」或「金额」等格式输出值时，在 `valueFormat` 属性中指定格式。详细信息请参考 :ref:`tag-format_value` 。
    * 关于 `<app:listSearchResult>` 的使用方法请参考 :ref:`list_search_result` 。


搜索功能讲解完毕。

:ref:`返回Getting Started TOP页 <getting_started>`
