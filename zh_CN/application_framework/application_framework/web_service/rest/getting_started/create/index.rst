创建注册功能
================================================================
基于Example应用程序讲解注册功能。

功能说明
  本功能在POST请求时通过请求主体设置JSON格式的项目信息，
  将项目信息注册到数据库。

动作确认步骤
  1. 事先确认DB状态

     从H2控制台执行以下SQL，确认记录不存在。

     .. code-block:: sql

       SELECT * FROM PROJECT WHERE PROJECT_NAME = '项目９９９';

  2. 注册项目信息

    使用任意REST客户端发送以下请求。

    URL
      http://localhost:9080/projects
    HTTP方法
      POST
    Content-Type
      application/json
    请求主体
      .. code-block:: json

        {
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
            "allocationOfCorpExpenses": 40000
        }

  3. 动作确认

    从H2控制台执行以下SQL，确认可以获取1条记录。

    .. code-block:: sql

      SELECT * FROM PROJECT WHERE PROJECT_NAME = '项目９９９';

注册项目信息
---------------------------------

创建Form
  创建接收客户端发送值的Form。

  ProjectForm.java
    .. code-block:: java

      public class ProjectForm implements Serializable {

          // 仅摘录部分

          /** 项目名称 */
          @Required
          @Domain("projectName")
          private String projectName;

          // getter及setter省略
      }

    实现要点
     * 属性全部声明为String型。详细信息请参考 :ref:`验证规则的设置方法 <bean_validation-form_property>` 。

实现业务Action方法
  实现将项目信息注册到数据库的处理。

  ProjectAction.java
    .. code-block:: java

      @Consumes(MediaType.APPLICATION_JSON)
      @Valid
      public HttpResponse save(ProjectForm project) {
          UniversalDao.insert(BeanUtil.createAndCopy(Project.class, project));
          return new HttpResponse(HttpResponse.Status.CREATED.getStatusCode());
      }

   实现要点
    * 为以JSON形式接收请求，在 :java:extdoc:`Consumes<jakarta.ws.rs.Consumes>` 注解中
      指定 ``MediaType.APPLICATION_JSON`` 。
    * 使用 :java:extdoc:`Valid <jakarta.validation.Valid>` 注解进行请求的验证。
      详细信息请参考 :ref:`jaxrs_bean_validation_handler` 。
    * 使用 :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` 将Form转换为Entity，
      使用 :ref:`universal_dao` 将项目信息注册到数据库。
    * 返回表示资源创建完成(状态码： ``201`` )的 :java:extdoc:`HttpResponse<nablarch.fw.web.HttpResponse>` 作为返回值。

定义URL映射
  使用 :ref:`router_adaptor` 进行业务Action与URL的映射。
  映射使用 :ref:`Jakarta RESTful Web Services的Path注解 <router_adaptor_path_annotation>` 。

  ProjectAction.java
    .. code-block:: java

      @Path("/projects")
      public class ProjectAction {
        @POST
        @Consumes(MediaType.APPLICATION_JSON)
        @Valid
        public HttpResponse save(ProjectForm project) {
          UniversalDao.insert(BeanUtil.createAndCopy(Project.class, project));
          return new HttpResponse(HttpResponse.Status.CREATED.getStatusCode());
      }

  实现要点
    * 使用 ``@Path`` 注解和 ``@POST`` 注解定义POST请求时映射的业务Action方法。
