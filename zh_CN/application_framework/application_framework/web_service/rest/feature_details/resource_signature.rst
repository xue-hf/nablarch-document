资源(Action)类的实现相关
==================================================


.. _rest_feature_details-method_signature:

资源类的方法签名
--------------------------------------------------
显示资源类的方法参数及返回值可使用的类型。

方法参数
  .. list-table::
    :header-rows: 1
    :class: white-space-normal
    :widths: 30 70

    * - 参数定义
      - 说明

    * - 无参数
      - 不需要参数或请求主体时，可以将方法定义为无参数。

        示例
          .. code-block:: java

            public HttpResponse sample() {
              // 省略
            }

    * - Form(Java Beans)
      - 基于从请求主体转换的Form进行处理时，将Form定义为参数。
      
        示例
          .. code-block:: java

            public HttpResponse sample(SampleForm form) {
              // 省略
            }

    * - :java:extdoc:`JaxRsHttpRequest <nablarch.fw.jaxrs.JaxRsHttpRequest>`\ [#]_\
      - 使用 :ref:`路径参数 <rest_feature_details-path_param>` 或 :ref:`查询参数 <rest_feature_details-query_param>`
        或想要获取HTTP头部值等时，将 :java:extdoc:`JaxRsHttpRequest <nablarch.fw.jaxrs.JaxRsHttpRequest>` 定义为参数。

        示例
          .. code-block:: java

            public HttpResponse sample(JaxRsHttpRequest request) {
              // 省略
            }

    * - :java:extdoc:`ExecutionContext <nablarch.fw.ExecutionContext>`
      - 想要访问 :java:extdoc:`ExecutionContext <nablarch.fw.ExecutionContext>` 提供的范围变量时，
        将 :java:extdoc:`ExecutionContext <nablarch.fw.ExecutionContext>` 定义为参数。
        
        示例
          .. code-block:: java

            public HttpResponse sample(ExecutionContext context) {
              // 省略
            }

    * - 组合
      - 可根据用途组合上述类型。
        
        例如，需要HTTP头部信息和从请求主体转换的Form的方法定义如下。

        .. code-block:: java

          public HttpResponse sample(SampleForm form, JaxRsHttpRequest request) {
            // 省略
          }

.. [#] 
  为维持向后兼容性也可以使用HttpRequest，但原则上使用JaxRsHttpRequest。  

方法返回值
  .. list-table::
    :header-rows: 1
    :class: white-space-normal
    :widths: 30 70

    * - 返回值类型
      - 说明

    * - void
      - 表示响应主体为空，向客户端返回 ``204: NoContent`` 。

    * - Form(Java Beans)
      - 方法返回的Form由 :ref:`body_convert_handler` 转换为响应主体输出内容后返回客户端。

    * - :java:extdoc:`HttpResponse <nablarch.fw.web.HttpResponse>`
      - 方法返回的 :java:extdoc:`HttpResponse <nablarch.fw.web.HttpResponse>` 信息返回客户端。



.. _rest_feature_details-path_param:

处理路径参数
--------------------------------------------------
显示将表示搜索、更新、删除目标资源的值指定为路径参数时的实现方法。

URL示例
  将 ``GET /users/123`` 的 ``123`` 作为路径参数。

路由设置
  URL与Action映射时为路径参数部设置任意名称。
  此示例中设置名称为 ``id`` ，仅允许数值。
  
  详细信息请参考 :ref:`router_adaptor` 。

  .. code-block:: xml

    <routes>
      <get path="users/:id" to="UsersResource#find">
        <requirements>
          <requirement name="id" value="\d+$" />
        </requirements>
      </get>
    </routes>

资源类方法的实现
  路径参数从 :java:extdoc:`JaxRsHttpRequest <nablarch.fw.jaxrs.JaxRsHttpRequest>` 获取。
  因此，在资源方法中将 :java:extdoc:`JaxRsHttpRequest <nablarch.fw.jaxrs.JaxRsHttpRequest>` 定义为形式参数。

  :java:extdoc:`JaxRsHttpRequest <nablarch.fw.jaxrs.JaxRsHttpRequest>` 中指定的参数名使用
  路由设置中指定的路径参数名称。

  .. code-block:: java

    @Produces(MediaType.APPLICATION_JSON)
    public User delete(JaxRsHttpRequest req) {
      // 从JaxRsHttpRequest获取路径参数值
      Long id = Long.valueOf(req.getPathParam("id"));
      return UniversalDao.findById(User.class, id);
    }

.. important::
  注意不能使用Jakarta RESTful Web Services规定的 :java:extdoc:`PathParam <jakarta.ws.rs.PathParam>` 。

.. _rest_feature_details-query_param:

处理查询参数
--------------------------------------------------
资源搜索处理中，有时希望将搜索条件指定为查询参数。
以下显示这种情况的实现方法。

URL示例
  ``GET /users/search?name=Duke``

路由设置
  路由设置中，基于除去查询参数的路径进行资源类映射。

  .. code-block:: xml

    <routes>
      <get path="users/search" to="Users#search"/>
    </routes>

资源类方法的实现
  查询参数从 :java:extdoc:`JaxRsHttpRequest <nablarch.fw.jaxrs.JaxRsHttpRequest>` 获取。
  因此，在资源方法中将 :java:extdoc:`JaxRsHttpRequest <nablarch.fw.jaxrs.JaxRsHttpRequest>` 定义为形式参数。

  使用 :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` 将从 :java:extdoc:`JaxRsHttpRequest <nablarch.fw.jaxrs.JaxRsHttpRequest>` 获取的参数映射到Form类。

  .. code-block:: java

    public HttpResponse search(JaxRsHttpRequest req) {

      // 将请求参数转换为Bean
      UserSearchForm form = BeanUtil.createAndCopy(UserSearchForm.class, req.getParamMap());

      // 执行验证
      ValidatorUtil.validate(form)

      // 执行业务逻辑(省略)
    }

    // 映射查询参数的Form
    public UserSearchForm {
      private String name;
      // 省略
    }

.. important::
  注意不能使用Jakarta RESTful Web Services规定的 :java:extdoc:`QueryParam <jakarta.ws.rs.QueryParam>` 。

.. _rest_feature_details-response_header:

设置响应头部
--------------------------------------------------
有时需要在资源类方法中单独指定响应头部。

.. important::
  想要指定应用程序全体共通的响应头部时请使用handler设置。
  想要指定安全相关的响应头部时使用 :ref:`secure_handler` 即可。

资源类方法中创建 :java:extdoc:`HttpResponse <nablarch.fw.web.HttpResponse>` 时，
在HttpResponse中指定响应头部即可。

  .. code-block:: java

    public HttpResponse something(JaxRsHttpRequest request) {

        // 处理省略

        HttpResponse response = new HttpResponse();
        response.setHeader("Cache-Control", "no-store"); // 指定响应头部
        return response;
    }

使用Produces注解，资源类方法返回实体（Bean）时，
无法直接指定响应头部。

  .. code-block:: java

    @Produces(MediaType.APPLICATION_JSON)
    public List<Client> something(JaxRsHttpRequest request, ExecutionContext context) {

        // 处理省略
        List<Client> clients = service.findClients(condition);

        return clients;
    }

框架为了在使用Produces注解时指定响应头部和状态码，
提供了 :java:extdoc:`EntityResponse <nablarch.fw.jaxrs.EntityResponse>` 。
返回EntityResponse代替实体即可。

  .. code-block:: java

    @Produces(MediaType.APPLICATION_JSON)
    public EntityResponse<List<Client>> something(JaxRsHttpRequest request, ExecutionContext context) {

        // 处理省略
        List<Client> clients = service.findClients(condition);

        EntityResponse<List<Client>> response = new EntityResponse<>();
        response.setEntity(clients); // 指定实体
        response.setStatusCode(HttpResponse.Status.OK.getStatusCode()); // 指定状态码
        response.setHeader("Cache-Control", "no-store"); // 指定响应头部
        return response;
    }
