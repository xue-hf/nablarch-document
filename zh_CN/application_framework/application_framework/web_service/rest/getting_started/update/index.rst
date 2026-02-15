创建更新功能
================================================================
基于Example应用程序讲解更新功能。
 
功能说明
  本功能在PUT请求时通过请求主体设置JSON格式的项目信息，
  更新数据库上项目ID匹配的项目信息。

动作确认步骤
  1. 事先确认DB状态
 
     从H2控制台执行以下SQL，确认要更新的记录。

     .. code-block:: sql

       SELECT * FROM PROJECT WHERE PROJECT_ID = 1;
 
  2. 更新项目信息

    使用任意REST客户端发送以下请求。

    URL
      http://localhost:9080/projects
    HTTP方法
      PUT
    Content-Type
      application/json
    请求主体
      .. code-block:: json

        {
            "projectId": 1,
            "projectName": "项目９９９",
            "projectType": "development",
            "projectClass": "ss",
            "projectManager": "山田",
            "projectLeader": "田中",
            "clientId": 10,
            "projectStartDate": "20160101",
            "projectEndDate": "20161231",
            "note": "备注９９９",
            "sales": 10000,
            "costOfGoodsSold": 20000,
            "sga": 30000,
            "allocationOfCorpExpenses": 40000,
            "version": 1
        }
 
  3. 动作确认

    从H2控制台执行以下SQL，确认记录已更新。

    .. code-block:: sql

      SELECT * FROM PROJECT WHERE PROJECT_ID = 1;
 
更新项目信息
---------------------------------

创建Form
  创建接收客户端发送值的Form。
 
  ProjectUpdateForm.java
    .. code-block:: java

      public class ProjectUpdateForm implements Serializable {
 
          // 仅摘录部分

          /** 项目名称 */
          @Required
          @Domain("id")
          private String projectId;
 
          /** 项目名称 */
          @Required
          @Domain("projectName")
          private String projectName;

          /** 项目类型 */
          @Required
          @Domain("projectType")
          private String projectType;
 
          // getter及setter省略
      }
 
    实现要点
     * 属性全部声明为String型。详细信息请参考 :ref:`验证规则的设置方法 <bean_validation-form_property>` 。
 
实现业务Action方法
  实现更新数据库上的项目信息的处理。
 
  ProjectAction.java
    .. code-block:: java

      @Consumes(MediaType.APPLICATION_JSON)
      @Valid
      public HttpResponse update(ProjectUpdateForm form) {
          Project project = BeanUtil.createAndCopy(Project.class, form);

          UniversalDao.update(project);

          return new HttpResponse(HttpResponse.Status.OK.getStatusCode());
      }
 
   实现要点
    * 为以JSON形式接收请求主体，在 :java:extdoc:`Consumes<jakarta.ws.rs.Consumes>` 注解中
      指定 ``MediaType.APPLICATION_JSON`` 。
    * 使用 :java:extdoc:`Valid <jakarta.validation.Valid>` 注解进行请求的验证。
      详细信息请参考 :ref:`jaxrs_bean_validation_handler` 。
    * 使用 :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` 从Form创建Entity，
      使用 :ref:`universal_dao` 更新项目信息。
    * 更新成功时，返回表示正常结束(状态码： ``200`` )的 :java:extdoc:`HttpResponse<nablarch.fw.web.HttpResponse>` 。

    .. tip::

      Example应用程序中独立扩展了 :java:extdoc:`ErrorResponseBuilder<nablarch.fw.jaxrs.ErrorResponseBuilder>` ，
      :java:extdoc:`NoDataException<nablarch.common.dao.NoDataException>` 发生时返回 ``404`` 、
      :java:extdoc:`OptimisticLockException<jakarta.persistence.OptimisticLockException>` 发生时返回 ``409``
      的响应给客户端。
 
定义URL映射
  使用 :ref:`router_adaptor` 进行业务Action与URL的映射。
  映射使用 :ref:`Jakarta RESTful Web Services的Path注解 <router_adaptor_path_annotation>` 。

  ProjectAction.java
    .. code-block:: java

      @Path("/projects")
      public class ProjectAction {
        @PUT
        @Consumes(MediaType.APPLICATION_JSON)
        @Valid
        public HttpResponse update(ProjectUpdateForm form) {
            Project project = BeanUtil.createAndCopy(Project.class, form);

            UniversalDao.update(project);

            return new HttpResponse(HttpResponse.Status.OK.getStatusCode());
        }

  实现要点
    * 使用 ``@Path`` 注解和 ``@PUT`` 注解定义PUT请求时映射的业务Action方法。
