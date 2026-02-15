.. _`getting_started_http_massaging-save`:

创建注册功能
==========================================================
讲解将请求的信息(JSON格式)注册到DB的功能。

功能概要说明
  .. image:: ../images/overview.png

动作确认步骤
  1. 事先确认DB状态

     从H2控制台执行以下SQL，确认记录不存在。

     .. code-block:: sql

       SELECT * FROM PROJECT WHERE PROJECT_NAME = '项目９９９';

  2. 注册项目信息

    使用任意REST客户端发送以下请求。

    URL
      http://localhost:9080/ProjectSaveAction
    HTTP方法
      POST
    HTTP头部
      Content-Type: application/json |br|
      X-Message-Id: 1
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

执行注册
----------------------

#. :ref:`创建格式文件<getting_started_http_messaging-format>`
#. :ref:`创建Form<getting_started_http_messaging-form>`
#. :ref:`创建业务Action<getting_started_http_messaging-action>`

.. _`getting_started_http_messaging-format`:

创建格式文件
  HTTP消息处理使用 :ref:`data_format` 解析请求的HTTP消息。

  ProjectSaveAction_RECEIVE.fmt
    .. code-block:: bash

      file-type:        "JSON"
      text-encoding:    "UTF-8"

      [project]
      1  projectName                       N
      2  projectType                       N
      3  projectClass                      N
      4  projectStartDate[0..1]            N
      5  projectEndDate[0..1]              N
      6  clientId                          X9
      7  projectManager[0..1]              N
      8  projectLeader[0..1]               N
      9  note[0..1]                        N
      10 sales[0..1]                       X9
      11 costOfGoodsSold[0..1]             X9
      12 sga[0..1]                         X9
      13 allocationOfCorpExpenses[0..1]    X9
      14 userId[0..1]                      X9

  实现要点
    * 格式文件名称采用「请求ID + "_RECEIVE"」的形式。
    * 格式文件的记述方法请参考 :ref:`data_format-definition` 。

.. _`getting_started_http_messaging-form`:

创建Form
  创建绑定请求主体内容的Form。

  ProjectForm.java
    .. code-block:: java

      public class ProjectForm {

          // 仅摘录部分项目

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
              return projectName;
          }

          /**
           * 设置项目名称。
           *
           * @param projectName 要设置的项目名称
           *
           */
          public void setProjectName(String projectName) {
              this.projectName = projectName;
          }
      }

  实现要点
    * 为了使用 :ref:`bean_validation` 进行验证，设置验证用注解。

.. _`getting_started_http_messaging-action`:

创建业务Action
  创建将项目注册到DB的业务Action。

  ProjectSaveAction.java
    .. code-block:: java

      public class ProjectSaveAction extends MessagingAction {

          /**
           * 接收电文时执行的业务处理。
           * <p>
           * 验证项目信息并注册到DB。
           * 此方法是注册单个项目的处理。
           * (通过通用格式的格式检查保证是单个项目)
           * </p>
           * 注册完成时设置记载响应代码的响应电文。
           * 发生异常时，在{@link ProjectSaveAction#onError(Throwable, RequestMessage, ExecutionContext)}
           * 中设置响应电文。
           * 
           * @param requestMessage   接收的消息
           * @param executionContext 执行上下文
           * @return 响应电文
           */
          @Override
          protected ResponseMessage onReceive(RequestMessage requestMessage,
                                              ExecutionContext executionContext) {

              // 将输入值绑定到Form
              ProjectForm form = BeanUtil.createAndCopy(ProjectForm.class,
                      requestMessage.getParamMap());

              // 存在验证错误时抛出业务异常
              ValidatorUtil.validate(form);

              UniversalDao.insert(BeanUtil.createAndCopy(Project.class, form));

              // 创建响应电文的formatter
              requestMessage.setFormatterOfReply(createFormatter());

              // 设置响应电文中记载的响应状态码
              Map<String, String> map = new HashMap<>();
              map.put("statusCode", String.valueOf(HttpResponse.Status.CREATED.getStatusCode()));

              // 返回响应数据
              return requestMessage.reply()
                     .setStatusCodeHeader(String.valueOf(HttpResponse.Status.CREATED.getStatusCode()))
                     .addRecord("data", map);
          }
      }


  实现要点
    * 继承 :java:extdoc:`MessagingAction <nablarch.fw.messaging.action.MessagingAction>` ，创建业务方法。
    * 在 :java:extdoc:`MessagingAction#onReceive <nablarch.fw.messaging.action.MessagingAction.onReceive(nablarch.fw.messaging.RequestMessage,nablarch.fw.ExecutionContext)>`
      中实现接收请求时执行的处理。
    * 请求主体的值在通过 :ref:`data_format` 解析后，由参数 :java:extdoc:`RequestMessage <nablarch.fw.messaging.RequestMessage>` 对象
      保持。使用 `getParamMap` 方法获取请求主体的值。
    * 使用 :ref:`bean_validation` 进行请求值的验证。
    * 使用 :java:extdoc:`UniversalDao <nablarch.common.dao.UniversalDao>` 将项目注册到DB。
    * 返回设置表示处理结果的响应代码的 :java:extdoc:`ResponseMessage <nablarch.fw.messaging.ResponseMessage>` 。

  .. tip::
    业务异常被抛出时，通过 :ref:`http_messaging_error_handler` 的处理设置响应代码「400」。

.. |br| raw:: html

  <br />
