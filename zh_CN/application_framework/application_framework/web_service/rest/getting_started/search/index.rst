创建搜索功能
================================================================
基于Example应用程序讲解搜索功能。

功能说明
  本功能在GET请求时通过查询参数附加搜索条件，
  以JSON格式返回符合条件的项目信息。

  搜索条件可以指定 ``客户ID(完全匹配)`` 、 ``项目名称(部分匹配)`` 。
  不指定搜索条件时返回所有项目信息。

动作确认步骤
  1. 搜索项目信息

    此处搜索客户ID为 `1` 的项目信息。

    使用任意REST客户端发送以下请求。

    URL
      http://localhost:9080/projects?clientId=1
    HTTP方法
      GET

  2. 确认搜索结果

    执行1的结果，确认返回以下JSON格式的响应。

    .. code-block:: javascript

      [{
          "projectId":1,
          "projectName":"项目００１",
          "projectType":"development",

          // 省略

      }]

搜索项目信息
---------------------------------

创建Form
  创建接收客户端发送值的Form。

  ProjectSearchForm.java
    .. code-block:: java

      public class ProjectSearchForm implements Serializable {

          /** 客户ID */
          @Domain("id")
          private String clientId;

          /** 项目名称 */
          @Domain("projectName")
          private String projectName;

          // getter及setter省略
      }

  实现要点
    * 属性全部声明为String型。详细信息请参考 :ref:`验证规则的设置方法 <bean_validation-form_property>` 。

创建保持搜索条件的Bean
  创建保持搜索条件的Bean。

  ProjectSearchDto.java
    .. code-block:: java

      public class ProjectSearchDto implements Serializable {

          /** 客户ID */
          private Integer clientId;

          /** 项目名称 */
          private String projectName;

          // getter及setter省略

  实现要点
   * Bean的属性必须是 :ref:`与对应条件列定义(类型)兼容的类型<universal_dao-search_with_condition>` 。

创建搜索使用的SQL
  创建搜索使用的SQL。

    Project.sql
      .. code-block:: none

        FIND_PROJECT =
        SELECT
            *
        FROM
            PROJECT
        WHERE
            $if(clientId) {CLIENT_ID = :clientId}
            AND $if(projectName) {PROJECT_NAME LIKE :%projectName%}

    实现要点
      * 为防止SQL注入，SQL写入外部文件。详细信息请参考 :ref:`database-use_sql_file` 。
      * 使用Bean的属性名向SQL绑定值。详细信息请参考 :ref:`database-input_bean` 。
      * 仅将搜索画面中指定的项目作为条件时，使用 :ref:`$if 语法构建SQL语句<database-use_variable_condition>` 。

实现业务Action方法
  实现基于搜索条件从数据库搜索的处理。

  ProjectAction.java
    .. code-block:: java

      @Produces(MediaType.APPLICATION_JSON)
      public List<Project> find(JaxRsHttpRequest req) {

          // 将请求参数转换为Bean
          ProjectSearchForm form =
                  BeanUtil.createAndCopy(ProjectSearchForm.class, req.getParamMap());

          // 执行BeanValidation
          ValidatorUtil.validate(form);

          ProjectSearchDto searchCondition = BeanUtil.createAndCopy(ProjectSearchDto.class, form);
          return UniversalDao.findAllBySqlFile(Project.class, "FIND_PROJECT", searchCondition);
      }

  实现要点
   * 为以JSON格式向客户端返回搜索结果，在 :java:extdoc:`Produces<jakarta.ws.rs.Produces>` 注解中
     指定 ``MediaType.APPLICATION_JSON`` 。
   * 查询参数从 :java:extdoc:`JaxRsHttpRequest<nablarch.fw.jaxrs.JaxRsHttpRequest>` 获取。
   * 使用 :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` 从请求参数创建Form。
   * 使用 :java:extdoc:`ValidatorUtil#validate <nablarch.core.validation.ee.ValidatorUtil.validate(java.lang.Object)>`
     进行Form的验证。
   * 使用 :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` 将Form的值复制到搜索条件Bean。
   * 返回使用 :ref:`universal_dao` 获取的项目信息列表作为返回值。
   * 返回值的对象由 :ref:`body_convert_handler` 转换为JSON格式，
     因此无需在业务Action方法内实现转换处理。

定义URL映射
  使用 :ref:`router_adaptor` 进行业务Action与URL的映射。
  映射使用 :ref:`Jakarta RESTful Web Services的Path注解 <router_adaptor_path_annotation>` 。

  ProjectAction.java
    .. code-block:: java

      @Path("/projects")
      public class ProjectAction {
        @GET
        @Produces(MediaType.APPLICATION_JSON)
        public List<Project> find(JaxRsHttpRequest req) {

            // 将请求参数转换为Bean
            ProjectSearchForm form =
                    BeanUtil.createAndCopy(ProjectSearchForm.class, req.getParamMap());

            // 执行BeanValidation
            ValidatorUtil.validate(form);

            ProjectSearchDto searchCondition = BeanUtil.createAndCopy(ProjectSearchDto.class, form);
            return UniversalDao.findAllBySqlFile(Project.class, "FIND_PROJECT", searchCondition);
        }

  实现要点
    * 使用 ``@Path`` 注解和 ``@GET`` 注解定义GET请求时映射的业务Action方法。
