.. _`main`:

通用启动launcher
==================================================

.. contents:: 目录
  :depth: 3
  :local:

standalone启动的应用程序的起点handler。

通过从java命令直接启动，可以初始化系统仓库并执行其中定义的handler队列。

本handler执行以下处理。
处理详情请参考括号内的Javadoc。

* 命令行参数解析( :java:extdoc:`CommandLine<nablarch.fw.launcher.CommandLine>` )
* 启动日志输出( :java:extdoc:`LauncherLogFormatter#getStartLogFormat<nablarch.fw.launcher.logging.LauncherLogFormatter.getStartLogFormat()>` )
* 系统仓库初始化
* 执行上下文初始化( :java:extdoc:`Main#setupExecutionContext <nablarch.fw.launcher.Main.setupExecutionContext(nablarch.fw.launcher.CommandLine,nablarch.fw.ExecutionContext)>` )
* 应用设置日志输出( :java:extdoc:`ApplicationSettingLogFormatter<nablarch.core.log.app.ApplicationSettingLogFormatter>` )
* handler队列执行
* 根据异常及错误的日志输出
* 结束日志输出( :java:extdoc:`LauncherLogFormatter#getEndLogFormat<nablarch.fw.launcher.logging.LauncherLogFormatter.getEndLogFormat()>` )

处理流程如下。

.. image:: ../images/Main/Main_flow.png

handler类名
--------------------------------------------------
* :java:extdoc:`nablarch.fw.launcher.Main`

模块列表
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-standalone</artifactId>
  </dependency>

.. _main-run_application:

启动应用程序
--------------------------------------------------
通过java命令指定 :java:extdoc:`Main类<nablarch.fw.launcher.Main>` 来启动应用程序。

框架运行所需的以下3个选项必须指定。
如果缺少以下任一选项，将立即异常结束。(结束代码 = 127)

\-diConfig
 指定系统仓库设置文件的路径。
 使用此选项指定的路径初始化系统仓库。

\-requestPath
 指定要执行的action和请求ID。

 设置按以下格式定义的字符串。

 .. code-block:: bash

  要执行的action类名/请求ID

 此选项指定的请求路径将
 :java:extdoc:`Request#getRequestPath<nablarch.fw.Request.getRequestPath()>`
 返回。

\-userId
 设置用户ID。
 此值将作为 ``user.id`` 名称存储在会话上下文变量中。

以下显示执行示例。

.. code-block:: bash

 java nablarch.fw.launcher.Main \
   -diConfig file:./batch-config.xml \
   -requestPath admin.DataUnloadBatchAction/BC0012 \
   -userId testUser

.. _main-option_parameter:

为应用程序启动设置任意选项
--------------------------------------------------
:java:extdoc:`Main类<nablarch.fw.launcher.Main>` 启动时，可以指定任意选项参数。

选项参数以"选项名称"和"选项值"的配对形式设置。

例如，选项名称为 ``optionName`` 且值为 ``optionValue`` 时，指定如下。

.. code-block:: bash

 java nablarch.fw.launcher.Main \
   -optionName optionValue

在应用程序中使用选项时，从 :java:extdoc:`ExecutionContext <nablarch.fw.ExecutionContext>` 获取。

.. code-block:: java

     @Override
    public Result handle(String inputData, ExecutionContext ctx) {
      // 指定选项名称给getSessionScopedVar，获取值。
      final String value = ctx.getSessionScopedVar("optionName");

      // 处理

      return new Result.Success();
    } 

.. tip::

  应用程序启动时必须指定的选项请参考 :ref:`main-run_application`

根据异常及错误的处理内容
--------------------------------------------------
本handler根据捕获的异常及错误内容，执行以下处理并返回结果。

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 25 75

  * - 异常类
    - 处理内容

  * - :java:extdoc:`Result.Error <nablarch.fw.Result.Error>`

      (包含子类)

    - 输出FATAL级别日志。

      日志输出后，作为handler处理结果返回以下值。

       状态码为0～127时
        直接返回状态码。

       状态码为0～127以外时
        返回127。

  * - 上述以外的异常类

    - 输出FATAL级别日志。

      日志输出后，作为handler处理结果返回127。
