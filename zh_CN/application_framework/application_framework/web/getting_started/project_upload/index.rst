.. _`project_upload`:

创建使用上传的批量注册功能
==========================================
基于Example应用程序讲解上传CSV文件进行批量注册的功能。

功能说明
  1. 点击头部菜单的「项目批量注册」。

    .. image:: ../images/project_upload/project_upload-link.png
      :scale: 80

  2. 从以下链接下载会发生验证错误的批量注册示例文件。

     :download:`项目批量注册_验证错误.csv<../downloads/project_upload/项目批量注册_验证错误.csv>`

  3. 上传示例文件，点击注册按钮。

    .. image:: ../images/project_upload/project_upload-invalid_upload.png
      :scale: 80

  3. 发生验证错误。

    .. image:: ../images/project_upload/project_upload-validate.png
      :scale: 80

  4. 从以下链接下载不会发生验证错误的批量注册示例文件。

    :download:`项目批量注册.csv<../downloads/project_upload/项目批量注册.csv>`

  5. 上传示例文件，点击注册按钮。

    .. image:: ../images/project_upload/project_upload-valid_upload.png
      :scale: 80

  6. 文件内容注册到数据库，显示完成消息。

    .. image:: ../images/project_upload/project_upload-complete.png
      :scale: 80

创建的业务Action方法的整体结构
-----------------------------------------------------

    ProjectUploadAction.java
      .. code-block:: java

        @OnDoubleSubmission
        @OnError(type = ApplicationException.class, path = "/WEB-INF/view/projectUpload/create.jsp")
        public HttpResponse upload(HttpRequest request, ExecutionContext context) {

            // 获取上传文件
            List<PartInfo> partInfoList = request.getPart("uploadFile");
            if (partInfoList.isEmpty()) {
                throw new ApplicationException(
                        MessageUtil.createMessage(MessageLevel.ERROR, "errors.upload"));
            }
            PartInfo partInfo = partInfoList.get(0);

            LoginUserPrincipal userContext = SessionUtil.get(context, "userContext");

            // 读取上传文件并验证
            List<Project> projects = readFileAndValidate(partInfo, userContext);

            // 批量注册到DB
            insertProjects(projects);

            // 添加完成消息
            context.setRequestScopedVar("uploadProjectSize", projects.size());

            // 保存文件
            saveFile(partInfo);

            return new HttpResponse("/WEB-INF/view/projectUpload/create.jsp");
        }
  
  业务Action方法的处理流程如下。
  
  #. :ref:`获取文件<project_upload-file_upload_action>`
  #. :ref:`将CSV文件内容绑定到Bean并进行验证<project_upload-validation>`
  #. :ref:`批量注册到DB<project_upload-bulk_insert>`
  #. :ref:`保存文件<project_upload-file_upload_action>`
  
  各处理的详细说明将在以下章节
  :ref:`文件上传功能的实现<project_upload-file_upload-impl>` 和
  :ref:`批量注册功能的实现<project_upload-bulk_insert-impl>` 中说明。

.. _`project_upload-file_upload-impl`:

文件上传功能的实现
-----------------------------------------------------
首先，说明使用上传的批量注册功能中，上传部分的创建方法。

  #. :ref:`创建文件上传画面<project_upload-upload_jsp>`
  #. :ref:`创建获取和保存文件的业务Action方法<project_upload-file_upload_action>`

  .. _`project_upload-upload_jsp`:

  创建文件上传画面
    创建带有文件上传栏的画面。

    /src/main/webapp/WEB-INF/view/projectUpload/create.jsp
      .. code-block:: jsp

        <n:form useToken="true" enctype="multipart/form-data">
            <!-- 省略 -->
            <div class="message-area margin-top">
                <!-- 完成消息显示部分 -->
                <c:if test="${not empty uploadProjectSize}">
                    <ul><li class="message-info"><n:message messageId="success.upload.project" option0="${uploadProjectSize}" /></li></ul>
                </c:if>
                <!-- 错误消息显示部分 -->
                <n:errors errorCss="message-error"/>
            </div>
            <!-- 省略 -->
            <h2 class="font-group mb-3">项目信息文件选择</h2>
            <table class="table">
                <!-- 画面设计相关描述省略 -->
                <tbody>
                    <tr>
                        <th class="item-norequired" colspan="2">项目信息文件选择</th>
                    </tr>
                    <tr>
                        <th class="width-250 required">项目信息文件</th>
                        <td >
                            <div class="input-group">
                                <n:file name="uploadFile" id="uploadFile"/>
                                <!-- 画面设计相关描述省略 -->
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
            <div class="title-nav">
                <div class="button-nav">
                    <n:button uri="/action/projectUpload/upload"
                              allowDoubleSubmission="false"
                              cssClass="btn btn-lg btn-light">注册</n:button>
                </div>
            </div>
        </n:form>

    实现要点
      * 为发送multipart文件，在 :ref:`tag-form_tag` 的 `enctype` 属性中指定 `multipart/form-data` 。
      * 使用 :ref:`tag-file_tag` 创建文件上传栏。 `name` 属性中指定注册到请求对象的名称。
        要在业务Action中获取文件，需要在 :java:extdoc:`HttpRequest#getPart<nablarch.fw.web.HttpRequest.getPart(java.lang.String)>`
        的参数中指定此注册名。
      * 上传完成时，使用 :ref:`tag-message_tag` 显示上传完成消息。
        为了在完成消息中包含上传件数，在 `option0` 属性中指定设置到request scope的上传件数。
      * 使用 :ref:`tag-errors_tag` 创建显示目标文件验证错误消息的列表区域。
        错误消息列表的输出格式请参考 :ref:`错误消息列表显示 <tag-write_error_errors_tag>` 。

  .. _`project_upload-file_upload_action`:

  创建业务Action方法
    说明业务Action方法中获取及保存文件的方法。

    ProjectUploadAction.java
      .. code-block:: java

        public HttpResponse upload(HttpRequest request, ExecutionContext context)
                throws IOException {

            List<PartInfo> partInfoList = request.getPart("uploadFile");
            if (partInfoList.isEmpty()) {
                throw new ApplicationException(MessageUtil.createMessage(MessageLevel.ERROR,
                         "errors.upload"));
            }
            PartInfo partInfo = partInfoList.get(0);

            // 批量注册处理后述因此省略

            // 保存文件
            saveFile(partInfo);

            return new HttpResponse("/WEB-INF/view/projectUpload/create.jsp");
        }
        
        /**
         * 保存文件。
         *
         * @param partInfo 上传文件的信息
         */
        private void saveFile(final PartInfo partInfo) {
            String fileName = generateUniqueFileName(partInfo.getFileName());
            UploadHelper helper = new UploadHelper(partInfo);
            helper.moveFileTo("uploadFiles", fileName);
        }

    实现要点
      * 使用 :java:extdoc:`HttpRequest#getPart<nablarch.fw.web.HttpRequest.getPart(java.lang.String)>` 获取文件。
      * 如果文件不存在(未上传)，获取的 :java:extdoc:`PartInfo<nablarch.fw.web.upload.PartInfo>` 列表大小为0。
        使用此值进行抛出业务异常等控制。
      * 上传的文件由 :ref:`multipart请求handler<multipart_handler>` 保存到临时区域。
        临时区域会自动删除，因此如果需要持久化（保存）上传文件，需要将文件转移到任意目录。
        但是，只有在 :ref:`文件路径管理<file_path_management>` 中管理文件和目录的输入输出时才能转移文件。
      * 文件转移使用 :java:extdoc:`UploadHelper#moveFileTo<nablarch.fw.web.upload.util.UploadHelper.moveFileTo(java.lang.String,java.lang.String)>` 方法。
        第一参数中指定配置文件中注册的文件存储目录的键名。
        Example应用程序中在下述文件中记载了设置。

        filepath-for-webui.xml
          .. code-block:: xml

            <!-- 文件路径定义 -->
            <component name="filePathSetting"
                    class="nablarch.core.util.FilePathSetting" autowireType="None">
              <property name="basePathSettings">
                <map>
                  <!--省略 -->
                  <!--上传文件的存储目录-->
                  <entry key="uploadFiles" value="file:./work/input" />
                </map>
              </property>
              <!-- 省略 -->
            </component>

.. _`project_upload-bulk_insert-impl`:

批量注册功能的实现
----------------------------
说明使用上传的批量注册功能中，批量注册部分的创建方法。

    #. :ref:`创建绑定文件的Bean<project_upload-create_bean>`
    #. :ref:`创建批量注册文件的业务Action方法<project_upload-bulk_action>`

.. _`project_upload-create_bean`:

创建绑定文件内容的Bean
  创建绑定文件内容的Bean。

  ProjectUploadDto.java
    .. code-block:: java

      @Csv(headers = { /** 记述头部 **/},
              properties = { /** 绑定对象的属性 **/},
              type = Csv.CsvType.CUSTOM)
      @CsvFormat(charset = "Shift_JIS", fieldSeparator = ',',ignoreEmptyLine = true,
              lineSeparator = "\r\n", quote = '"',
              quoteMode = CsvDataBindConfig.QuoteMode.NORMAL, requiredHeader = true, emptyToNull = true)
      public class ProjectUploadDto implements Serializable {

          // 仅摘录部分项目。getter及setter省略

          /** 项目名称 */
          @Required(message = "{nablarch.core.validation.ee.Required.upload}")
          @Domain("projectName")
          private String projectName;

          /** 项目类型 */
          @Required(message = "{nablarch.core.validation.ee.Required.upload}")
          @Domain("projectType")
          private String projectType;

          // 保持处理对象行行数的属性。setter省略。
          /** 行数 */
          private Long lineNumber;

          /**
           * 获取行数。
           * @return 行数
           */
          @LineNumber
          public Long getLineNumber() {
              return lineNumber;
          }
      }

  实现要点
    * 上传的CSV文件内容与Bean属性的绑定设置使用 :java:extdoc:`@Csv<nablarch.common.databind.csv.Csv>` 。
      接收的CSV格式指定使用 :java:extdoc:`@CsvFormat<nablarch.common.databind.csv.CsvFormat>` 。
      (使用 :ref:`默认格式指定<data_bind-csv_format_set>` 时，不需要 :java:extdoc:`@CsvFormat<nablarch.common.databind.csv.CsvFormat>` )
      注解设置方法的详细信息请参考 :ref:`CSV文件绑定到Java Beans类时的格式指定方法 <data_bind-csv_format-beans>` 。
    * 在属性上添加 :java:extdoc:`@Required<nablarch.core.validation.ee.Required>` 或 :java:extdoc:`@Domain<nablarch.core.validation.ee.Domain>`
      等验证用注解进行 :ref:`Bean Validation<bean_validation>` 。
    * 由于接收来自文件的输入值， :ref:`属性定义为String型<bean_validation-form_property>` ，
      到适当类型的转换对通过验证的安全值进行。
    * 定义行数属性，在getter上添加 :java:extdoc:`LineNumber<nablarch.common.databind.LineNumber>` 注解，
      可以自动设置目标数据是第几行的数据。

    .. tip::
      将输入必填项目的验证错误消息更改为适合文件上传的消息。
      关于验证消息的指定方法请参考 :ref:`设置输入值的校验规则<client_create_validation_rule>` 。

.. _`project_upload-bulk_action`:

创建业务Action方法
  创建将上传的文件内容注册到数据库的业务Action方法。

  .. _`project_upload-validation`:

  1.将CSV文件内容绑定到Bean并进行验证
    ProjectUploadAction.java
      .. code-block:: java

        private List<Project> readFileAndValidate(final PartInfo partInfo, final LoginUserPrincipal userContext) {
            List<Message> messages = new ArrayList<>();
            List<Project> projects = new ArrayList<>();

            // 将文件内容绑定到Bean并进行验证
            try (final ObjectMapper<ProjectUploadDto> mapper
                     = ObjectMapperFactory.create(
                            ProjectUploadDto.class, partInfo.getInputStream())) {
                ProjectUploadDto projectUploadDto;

                while ((projectUploadDto = mapper.read()) != null) {

                    // 验证并设置结果消息
                    messages.addAll(validate(projectUploadDto));

                    // 创建Entity
                    projects.add(createProject(projectUploadDto, userContext.getUserId()));
                }
            } catch (InvalidDataFormatException e) {
                // 如果存在文件格式不正确的行则在该时点结束解析
                messages.add(
                    MessageUtil.createMessage(
                        MessageLevel.ERROR, "errors.upload.format", e.getLineNumber()));
            }

            // 如果存在任何错误则不注册到数据库
            if (!messages.isEmpty()) {
                throw new ApplicationException(messages);
            }
            return projects;
        }
    
        /**
         * 验证项目信息并将结果存储到消息列表。
         *
         * @param projectUploadDto 从CSV生成的项目信息Bean
         * @return messages         验证结果的消息列表
         */
        private List<Message> validate(final ProjectUploadDto projectUploadDto) {

            List<Message> messages = new ArrayList<>();

            // 单项目验证。基于Dto中定义的注解执行Bean Validation
            try {
                ValidatorUtil.validate(projectUploadDto);
            } catch (ApplicationException e) {
                messages.addAll(e.getMessages()
                        .stream()
                        .map(message -> MessageUtil.createMessage(MessageLevel.ERROR,
                                "errors.upload.validate", projectUploadDto.getLineNumber(), message))
                        .collect(Collectors.toList()));
            }

            // 客户存在检查
            if (!existsClient(projectUploadDto)) {
                messages.add(MessageUtil.createMessage(MessageLevel.ERROR,
                        "errors.upload.client", projectUploadDto.getLineNumber()));
            }

            return messages;
        }

    实现要点
      * 要将文件绑定到Bean获取，使用 :ref:`数据绑定<data_bind>` 提供的
        :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` 。
      * 对获取的 :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` 对象执行
        :java:extdoc:`ObjectMapper#read <nablarch.common.databind.ObjectMapper.read()>` ，可以获取绑定后的Bean列表。
      * 使用 :java:extdoc:`ValidatorUtil#getValidator <nablarch.core.validation.ee.ValidatorUtil.getValidator()>` 生成
        :java:extdoc:`Validator <jakarta.validation.Validator>` 对象，可以对任意Bean执行 :ref:`Bean Validation<bean_validation>` 。
      * 如果在错误发生时不停止验证而是验证到最后一行，
        验证结束后将包含全部行错误消息的 :java:extdoc:`Message<nablarch.core.message.Message>` 列表
        作为参数生成并抛出 :java:extdoc:`ApplicationException<nablarch.core.message.ApplicationException>` ，
        可以在 :ref:`tag-errors_tag` 中输出到画面。
      * 关于在验证消息中添加属性名的方法
        请参考 :ref:`想在验证错误时的消息中包含项目名<bean_validation-property_name>` 实现。
    

  .. _`project_upload-bulk_insert`:

  2.批量注册到DB
    ProjectUploadAction.java
      .. code-block:: java

        public HttpResponse upload(HttpRequest request,ExecutionContext context)
                throws IOException {

            // 验证的执行前述

            // 批量注册到DB
            insertProjects(projects);

            // 文件保存前述
        }

        /**
         * 批量将多个项目Entity注册到数据库。
         * @param projects 已验证的项目列表
         */
        private void insertProjects(List<Project> projects) {

          List<Project> insertProjects = new ArrayList<Project>();

          for (Project project : projects) {
              insertProjects.add(project);
              // 每100件执行batchInsert
              if (insertProjects.size() >= 100) {
                  UniversalDao.batchInsert(insertProjects);
                  insertProjects.clear();
              }
          }

          if (!insertProjects.isEmpty()) {
              UniversalDao.batchInsert(insertProjects);
          }
        }

    实现要点
      * 批量注册使用 :java:extdoc:`UniversalDao#batchInsert <nablarch.common.dao.UniversalDao.batchInsert(java.util.List)>`
        执行。
      * 由于一次性注册件数过多可能导致性能下降，需要为每次批量注册设置上限件数。

使用上传的批量注册功能讲解完毕。

:ref:`返回Getting Started TOP页 <getting_started>`
