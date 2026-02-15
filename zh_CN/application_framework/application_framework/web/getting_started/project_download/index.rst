.. _`project_download`:

创建文件下载功能
==========================================
基于Example应用程序讲解下载CSV文件的功能。

功能说明
  1. 点击项目一览画面搜索结果右侧的下载按钮。

    .. image:: ../images/project_download/project_download-list.png
      :scale: 80

  2. 下载输出当前搜索结果的CSV文件。

    .. image:: ../images/project_download/project_download-download.png
      :scale: 80

下载CSV文件
---------------------------------
讲解下载CSV文件功能的实现方法。

关于项目搜索功能的创建方法，请参考 :ref:`创建搜索功能<project_search>` 。

  #. :ref:`创建下载按钮<project_download-download_button>`
  #. :ref:`创建绑定文件的Bean<project_download-create_bean>`
  #. :ref:`创建业务Action方法<project_upload-file_download_action>`

.. _`project_download-download_button`:

创建下载按钮
  放置发送GET请求到文件下载方法的链接。

  /src/main/webapp/WEB-INF/view/project/index.jsp
    .. code-block:: jsp

      <!-- 仅记载下载按钮周边 -->
      <div style="float:left;">
          <span class="font-group">
          搜索结果
          </span>
          <span class="search-result-count">
              <c:if test="${not empty searchResult}">
                  <n:write name="searchResult.pagination.resultCount" />
              </c:if>
          </span>
          <!-- 将当前搜索条件设置为参数 -->
          <c:url value="/action/project/download" var="download_uri">
              <c:param name="searchForm.clientId" value="${searchForm.clientId}"/>
              <c:param name="searchForm.clientName" value="${searchForm.clientName}"/>
              <c:param name="searchForm.projectName" value="${searchForm.projectName}"/>
              <c:param name="searchForm.projectType" value="${searchForm.projectType}"/>
              <c:forEach items="${searchForm.projectClass}" var="projectClass">
                  <c:param name="searchForm.projectClass" value="${projectClass}" />
              </c:forEach>
              <c:param name="searchForm.projectStartDateBegin" value="${searchForm.projectStartDateBegin}"/>
              <c:param name="searchForm.projectStartDateEnd" value="${searchForm.projectStartDateEnd}"/>
              <c:param name="searchForm.projectEndDateBegin" value="${searchForm.projectEndDateBegin}"/>
              <c:param name="searchForm.projectEndDateEnd" value="${searchForm.projectEndDateEnd}"/>
              <c:param name="searchForm.sortKey" value="${searchForm.sortKey}"/>
              <c:param name="searchForm.sortDir" value="${searchForm.sortDir}"/>
              <c:param name="searchForm.pageNumber" value="${searchForm.pageNumber}"/>
          </c:url>
          <n:a href="${download_uri}">
              <n:write name="label" />
              <n:img src="/images/download.png" alt="下载" />
          </n:a>
      </div>

.. _`project_download-create_bean`:

创建绑定文件的Bean
  创建绑定文件内容的Bean。

  ProjectDownloadDto.java
    .. code-block:: java

      @Csv(headers = { /** 记述头部 **/},
              properties = { /** 绑定对象的属性 **/},
              type = Csv.CsvType.CUSTOM)
      @CsvFormat(charset = "Shift_JIS", fieldSeparator = ',',ignoreEmptyLine = true,
              lineSeparator = "\r\n", quote = '"',
              quoteMode = CsvDataBindConfig.QuoteMode.NORMAL, requiredHeader = true, emptyToNull = true)
      public class ProjectDownloadDto implements Serializable {

          // 仅摘录部分项目。getter及setter省略

          /** 项目名称 */
          private String projectName;

          /** 项目类型 */
          private String projectType;
      }

  实现要点
    * 下载的CSV文件内容与Bean属性的绑定设置使用 :java:extdoc:`@Csv<nablarch.common.databind.csv.Csv>` 。
      接收的CSV格式指定使用 :java:extdoc:`@CsvFormat<nablarch.common.databind.csv.CsvFormat>` 。
      (使用 :ref:`默认格式指定<data_bind-csv_format_set>` 时，不需要 :java:extdoc:`@CsvFormat<nablarch.common.databind.csv.CsvFormat>` )
      注解设置方法的详细信息请参考 :ref:`CSV文件绑定到Java Beans类时的格式指定方法 <data_bind-csv_format-beans>` 。

.. _`project_upload-file_download_action`:

创建业务Action方法
  创建将搜索结果写入CSV文件的业务Action方法。

  ProjectAction.java
    .. code-block:: java

      @InjectForm(form = ProjectSearchForm.class, prefix = "searchForm", name = "searchForm")
      @OnError(type = ApplicationException.class, path = "/WEB-INF/view/project/index.jsp")
      public HttpResponse download(HttpRequest request, ExecutionContext context) {

          ProjectSearchForm searchForm = context.getRequestScopedVar("searchForm");
          ProjectSearchDto searchCondition = BeanUtil.createAndCopy(ProjectSearchDto.class, searchForm);
          LoginUserPrincipal userContext = SessionUtil.get(context, "userContext");
          searchCondition.setUserId(userContext.getUserId());

          final Path path = TempFileUtil.createTempFile();
          try (DeferredEntityList<ProjectDownloadDto> searchList = (DeferredEntityList<ProjectDownloadDto>) UniversalDao
                  .defer()
                  .findAllBySqlFile(ProjectDownloadDto.class, "SEARCH_PROJECT", searchCondition);
               ObjectMapper<ProjectDownloadDto> mapper = ObjectMapperFactory.create(ProjectDownloadDto.class,
                       TempFileUtil.newOutputStream(path))) {

              for (ProjectDownloadDto dto : searchList) {
                  mapper.write(dto);
              }
          }
          
          FileResponse response = new FileResponse(path.toFile(), true);
          response.setContentType("text/csv; charset=Shift_JIS");
          response.setContentDisposition("项目一览.csv");

          return response;
      }

  实现要点
    * 关于搜索处理的实现方法请参考 :ref:`创建搜索功能：实现业务Action<project_search-create_action>` 。
    * 要将Bean绑定到文件并输出，使用 :ref:`数据绑定<data_bind>` 提供的
      :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` 。
    * 要下载输出到文件的数据，使用 :java:extdoc:`FileResponse <nablarch.common.web.download.FileResponse>` 。
      详细信息请参考 :ref:`在下载中使用数据绑定<data_bind-file_download>` 。
    * 读取大量数据时，为防止内存压力，使用 :java:extdoc:`UniversalDao#defer <nablarch.common.dao.UniversalDao.defer()>` 
      :ref:`延迟加载<universal_dao-lazy_load>` 搜索结果。
    * 响应的内容类型使用
      :java:extdoc:`HttpResponse#setContentType<nablarch.fw.web.HttpResponse.setContentType(java.lang.String)>` 设置。
      详细信息请参考 :ref:`在下载中使用通用数据格式 <data_format-file_download>` 。
    * 下载文件的文件名使用
      :java:extdoc:`HttpResponse#setContentDisposition<nablarch.fw.web.HttpResponse.setContentDisposition(java.lang.String)>` 设置。
      详细信息请参考 :ref:`在下载中使用通用数据格式 <data_format-file_download>` 。

文件下载功能讲解完毕。

:ref:`返回Getting Started TOP页 <getting_started>`
