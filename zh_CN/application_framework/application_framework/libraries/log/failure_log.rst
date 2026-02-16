.. _failure_log:

故障日志的输出
==================================================

.. contents:: 目录
  :depth: 3
  :local:

框架中，在处理方式各自的异常处理器中输出。
应用程序中，在批处理发生故障时需要继续后续处理等情况下输出。

故障日志的输出方针
--------------------------------------------------
故障通知日志，是通过日志监控工具进行监控来检测故障的设想，
因此赋予日志记录器名称输出到故障通知专用文件中。
故障解析日志，输出到进行应用程序整体日志输出的应用程序日志中。

.. list-table:: 故障日志的输出方针
   :header-rows: 1
   :class: white-space-normal
   :widths: 30,30,30

   * - 日志类型
     - 日志级别
     - 日志记录器名称

   * - 故障通知日志
     - FATAL、ERROR
     - MONITOR

   * - 故障解析日志
     - FATAL、ERROR
     - 类名

针对上述输出方针的日志输出设置示例如下所示。

log.properties的设置示例
 .. code-block:: properties

  writerNames=monitorLog,appLog

  # 故障通知日志的输出目标
  writer.monitorLog.className=nablarch.core.log.basic.FileLogWriter
  writer.monitorLog.filePath=/var/log/app/monitor.log
  writer.monitorLog.formatter.className=nablarch.core.log.basic.BasicLogFormatter
  writer.monitorLog.formatter.format=$date$ -$logLevel$- $runtimeLoggerName$ [$executionId$] boot_proc = [$bootProcess$] proc_sys = [$processingSystem$] req_id = [$requestId$] usr_id = [$userId$] $message$

  # 应用程序日志的输出目标
  writer.appLog.className=nablarch.core.log.basic.FileLogWriter
  writer.appLog.filePath=/var/log/app/app.log
  writer.appLog.maxFileSize=10000
  writer.appLog.formatter.className=nablarch.core.log.basic.BasicLogFormatter
  writer.appLog.formatter.format=$date$ -$logLevel$- $runtimeLoggerName$ [$executionId$] boot_proc = [$bootProcess$] proc_sys = [$processingSystem$] req_id = [$requestId$] usr_id = [$userId$] $message$$information$$stackTrace$

  availableLoggersNamesOrder=MON,ROO

  # 应用程序日志的设置
  loggers.ROO.nameRegex=.*
  loggers.ROO.level=INFO
  loggers.ROO.writerNames=appLog

  # 故障通知日志的输出设置
  loggers.MON.nameRegex=MONITOR
  loggers.MON.level=ERROR
  loggers.MON.writerNames=monitorLog

app-log.properties的设置示例
 .. code-block:: properties

  # FailureLogFormatter
  #failureLogFormatter.className=
  failureLogFormatter.defaultFailureCode=MSG99999
  failureLogFormatter.defaultMessage=an unexpected exception occurred.
  failureLogFormatter.language=ja
  failureLogFormatter.notificationFormat=fail_code = [$failureCode$] $message$
  failureLogFormatter.analysisFormat=fail_code = [$failureCode$] $message$\nInput Data :\n$data$
  #failureLogFormatter.contactFilePath=
  #failureLogFormatter.fwFailureCodeFilePath=

.. tip::

 在大型系统中故障时的联系方式存在多个的情况下，
 可以使用 :ref:`failure_log-add_contact` 按请求ID将联系方式信息包含在日志中。


使用方法
--------------------------------------------------

.. _failure_log-logging:

输出故障日志
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
输出故障日志时，使用 :java:extdoc:`FailureLogUtil <nablarch.core.log.app.FailureLogUtil>` 。

.. code-block:: java

  try {
      // 业务处理
  } catch (UserNotFoundException e) {
      // 指定了捕获的异常、处理对象数据、故障代码。
      FailureLogUtil.logError(e, inputData, "USER_NOT_FOUND");
  }

另外，在批处理和消息传递中，当检测到故障时，
可能希望输出故障日志后结束业务处理。
这种情况下，
可以抛出 :java:extdoc:`TransactionAbnormalEnd <nablarch.fw.results.TransactionAbnormalEnd>` 或
:java:extdoc:`ProcessAbnormalEnd <nablarch.fw.launcher.ProcessAbnormalEnd>` ，
委托异常处理器(:ref:`global_error_handler` 或 :ref:`request_thread_loop_handler`)输出故障日志。

.. code-block:: java

  // 自己生成异常的情况
  if (user == null) {
      // 指定了退出代码、故障代码。
      throw new TransactionAbnormalEnd(100, "USER_NOT_FOUND");
  }

  // 捕获异常的情况
  try {
      // 业务处理
  } catch (UserNotFoundException e) {
      // 指定了退出代码、捕获的异常、故障代码。
      throw new ProcessAbnormalEnd(100, e, "USER_NOT_FOUND");
  }

.. tip::
 如上例所示，在输出故障日志时，为了从日志中确定故障内容，需要指定故障代码。
 故障代码的代码体系，请按项目自行规定。

故障日志中输出的消息
 故障日志中输出的消息，使用 :ref:`message` 获取与故障代码对应的消息。
 :ref:`message` 中，如果找不到消息会发生异常。
 如果在消息获取处理中发生异常，则除了故障日志外，
 还会以WARN级别输出消息获取处理中发生的异常，并在故障日志中输出以下消息。

 .. code-block:: bash

  failed to get the message to output the failure log. failureCode = [<故障代码>]

 在框架的异常处理器中捕获异常或错误等情况，没有指定故障代码时，
 输出设置中指定的默认 :ref:`故障代码 <failure_log-prop_default_failure_code>` 和
 :ref:`消息 <failure_log-prop_default_message>` 。

.. _failure_log-setting:

故障日志的设置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
故障日志的设置，在 :ref:`log-app_log_setting` 中说明的属性文件中进行。

描述规则
 \

 failureLogFormatter.className
  实现了 :java:extdoc:`FailureLogFormatter <nablarch.core.log.app.FailureLogFormatter>` 的类。
  需要替换时指定。

 .. _failure_log-prop_default_failure_code:

 failureLogFormatter.defaultFailureCode ``必需``
  默认的故障代码。
  在异常处理器中捕获异常或错误等情况，没有指定故障代码时使用。

 .. _failure_log-prop_default_message:

 failureLogFormatter.defaultMessage ``必需``
  默认的消息。
  使用默认故障代码时输出的消息。

 failureLogFormatter.language
  从故障代码获取消息时使用的语言。
  未指定时使用 :java:extdoc:`ThreadContext <nablarch.core.ThreadContext>` 中设置的语言。

 .. _failure_log-prop_notification_format:

 failureLogFormatter.notificationFormat
  故障通知日志的格式。

  格式中可指定的占位符
   \

   .. list-table::
      :header-rows: 1
      :class: white-space-normal
      :widths: 20,20,60

      * - 项目名
        - 占位符
        - 说明

      * - 故障代码
        - $failureCode$
        - 唯一标识故障的代码。用于确定故障内容。

      * - 消息
        - $message$
        - 与故障代码对应的消息。用于确定故障内容。

      * - 处理对象数据
        - $data$
        - 用于确定故障发生处理所针对的数据。
          调用使用数据读取器读取的数据对象的toString方法输出。

      * - 联系方式
        - $contact$
        - 用于确定联系方式。

  默认格式
   .. code-block:: java

    fail_code = [$failureCode$] $message$

 failureLogFormatter.analysisFormat
  故障解析日志的格式。
  格式中可指定的占位符和默认格式与
  :ref:`故障通知日志的格式 <failure_log-prop_notification_format>` 相同。

 failureLogFormatter.contactFilePath
  指定了故障联系方式信息的属性文件的路径。
  需要输出故障联系方式信息时指定。
  详细内容请参考 :ref:`failure_log-add_contact` 。

 failureLogFormatter.fwFailureCodeFilePath
  指定了框架故障代码更改信息的属性文件的路径。
  需要在输出故障日志时更改框架的故障代码时指定。
  详细内容请参考 :ref:`failure_log-change_fw_failure_code` 。


 .. important::
  根据系统的安全要求，即使在故障解析日志中也不允许输出个人信息或机密信息的情况下，
  请参考 :ref:`failure_log-placeholder_customize` ，在项目中进行自定义。

 .. tip::
  通过输出处理对象数据，可以在故障日志中输出来源运行时信息。
  来源运行时信息是指，例如，从Web向批处理进行数据协作的情况下，
  画面处理执行时的运行时信息（请求ID、运行时ID等）成为批处理中的来源运行时信息。
  来源运行时信息的输出方法，请参考 :ref:`failure_log-output_src_exe_info` 。

描述示例
 .. code-block:: properties

  failureLogFormatter.className=nablarch.core.log.app.FailureLogFormatter
  failureLogFormatter.defaultFailureCode=UNEXPECTED_ERROR
  failureLogFormatter.defaultMessage=an unexpected exception occurred.
  failureLogFormatter.language=en
  failureLogFormatter.notificationFormat=fail_code = [$failureCode$] $message$
  failureLogFormatter.analysisFormat=fail_code = [$failureCode$] $message$
  failureLogFormatter.derivedRequestIdPropName=insertRequestId
  failureLogFormatter.derivedUserIdPropName=updatedUserId
  failureLogFormatter.contactFilePath=classpath:failure-log-contact.properties
  failureLogFormatter.fwFailureCodeFilePath=classpath:failure-log-fw-codes.properties

.. _failure_log-add_contact:

向故障日志添加联系方式信息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
在大型系统中故障时的联系方式存在多个的情况下等，可能希望向故障日志中包含联系方式信息。
因此，在故障日志输出中，提供了按请求ID指定联系方式信息的功能。

联系方式信息的添加，在属性文件中指定。键指定请求ID，值指定联系方式信息。
对键指定的请求ID，针对从 :java:extdoc:`ThreadContext <nablarch.core.ThreadContext>` 获取的请求ID进行前缀匹配搜索。
因此，属性文件的内容在读取后，按键名长度降序排序，以便从更具体的请求ID开始搜索。

联系方式信息添加示例如下所示。

首先，准备属性文件。假设以 ``failure-log-contact.properties`` 的文件名放置在类路径根目录下。

failure-log-contact.properties的设置示例
 .. code-block:: properties

  # 请求ID=联系方式信息
  /users/=USRMGR999
  /users/index=USRMGR300
  /users/list=USRMGR301
  /users/new=USRMGR302
  /users/edit=USRMGR303

 上述属性文件在读取后按如下排序，从上到下用于搜索。

 .. code-block:: properties

  # 键名长度相同的项目，每次执行顺序可能不同。
  /users/index=USRMGR300
  /users/list=USRMGR301
  /users/edit=USRMGR303
  /users/new=USRMGR302
  /users/=USRMGR999

接下来，在故障日志的格式中指定表示联系方式信息的占位符 ``$contact$`` 。
并且，指定属性文件的路径。

app-log.properties的设置示例
 .. code-block:: properties

  # FailureLogFormatter的设置
  failureLogFormatter.defaultFailureCode=UNEXPECTED_ERROR
  failureLogFormatter.defaultMessage=an unexpected exception occurred.
  failureLogFormatter.notificationFormat=[$failureCode$:$message$] <$contact$>
  failureLogFormatter.analysisFormat=fail_code = [$failureCode$] $message$ <$contact$>

  # 指定属性文件的路径。
  failureLogFormatter.contactFilePath=classpath:failure-log-contact.properties

通过上述设置，将按请求ID输出联系方式信息。
请求ID为 ``/users/new`` 时发生故障的输出示例如下所示。
在指定了 ``$contact$`` 的位置（<>包围的部分）输出 ``USRMGR302`` 。

.. code-block:: bash

 # 故障通知日志
 2011-02-15 15:09:57.691 -FATAL- [APUSRMGR0001201102151509320020009] R[/users/new] U[0000000001] [UNEXPECTED_ERROR:an unexpected exception occurred.] <USRMGR302>

 # 故障解析日志
 2011-02-15 15:09:57.707 -FATAL- [APUSRMGR0001201102151509320020009] R[/users/new] U[0000000001] fail_code = [UNEXPECTED_ERROR] an unexpected exception occurred. <USRMGR302>
 # 堆栈跟踪省略。

另外，如果找不到与请求ID对应的联系方式信息，则输出null。

.. _failure_log-change_fw_failure_code:

更改框架的故障代码
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
框架中，在发生预期外的错误时会抛出RuntimeException系异常。
因此，框架抛出的异常，全部使用默认的故障代码输出故障日志。
在故障监控中，可能存在希望通过故障代码过滤监控对象的情况，
因此，在故障日志输出中，提供了指定框架故障代码的功能。

框架的故障代码，可以按抛出异常的类名指定。
"抛出异常的类"是指堆栈跟踪的根元素。
例如，在下面的堆栈跟踪中，是nablarch.core.message.StringResourceHolder类。

.. code-block:: bash

 Stack Trace Information :
 java.lang.RuntimeException: ValidateFor method invocation failed. targetClass = java.lang.Class, method = validateForRegisterUser
     at nablarch.core.validation.ValidationManager.validateAndConvert(ValidationManager.java:202)
     # 中间的堆栈跟踪省略。
 Caused by: nablarch.core.message.MessageNotFoundException: message was not found. message id = MSG00010
     at nablarch.core.message.StringResourceHolder.get(StringResourceHolder.java:40)
     # 以后的堆栈跟踪省略。（以后不出现Caused by）

但是，按框架的类设置故障代码分类过于细致，不够现实。
基本按包名单位指定故障代码，以便判断框架的哪个功能抛出了异常。

框架的故障代码，在属性文件中指定。
在属性文件中，键指定框架的包名，值指定故障代码。
对键指定的包名，针对从堆栈跟踪获取的抛出异常的类的FQCN（完全限定类名）进行前缀匹配搜索。
因此，属性文件的内容在读取后，按键名长度降序排序，以便从更具体的包名开始搜索。

框架故障代码更改示例如下所示。

首先，准备属性文件。
假设以 ``failure-log-fw-codes.properties`` 的文件名放置在类路径根目录下。
通过指定nablarch包名，可以对未单独指定的所有包指定故障代码。

failure-log-fw-codes.properties的设置示例
 .. code-block:: properties

  # 框架的包名=故障代码
  nablarch=FW_ERROR
  nablarch.core.cache=FW_CACHE_ERROR
  nablarch.core.date=FW_DATE_ERROR
  nablarch.core.db=FW_DB_ERROR
  nablarch.core.message=FW_MESSAGE_ERROR
  nablarch.core.repository=FW_REPOSITORY_ERROR
  nablarch.core.transaction=FW_TRANSACTION_ERROR

 上述属性文件在读取后按如下排序，从上到下用于搜索。

 .. code-block:: properties

   nablarch.core.transaction=FW_TRANSACTION_ERROR
   nablarch.core.repository=FW_REPOSITORY_ERROR
   nablarch.core.message=FW_MESSAGE_ERROR
   nablarch.core.cache=FW_CACHE_ERROR
   nablarch.core.date=FW_DATE_ERROR
   nablarch.core.db=FW_DB_ERROR
   nablarch=FW_ERROR

接下来，在FailureLogFormatter的设置中指定属性文件的路径。

app-log.properties的设置示例
 .. code-block:: properties

  failureLogFormatter.defaultFailureCode=UNEXPECTED_ERROR
  failureLogFormatter.defaultMessage=an unexpected exception occurred.
  failureLogFormatter.notificationFormat=[$failureCode$:$message$]
  failureLogFormatter.analysisFormat=fail_code = [$failureCode$] $message$
  # 指定属性文件的路径。
  failureLogFormatter.fwFailureCodeFilePath=classpath:failure-log-fw-codes.properties

通过上述设置，框架的故障代码将被更改。故障通知日志的几个输出示例如下所示。

nablarch.core.date.BasicBusinessDateProvider类抛出异常的情况
 .. code-block:: bash

  # 属性文件的nablarch.core.date=FW_DATE_ERROR适用。
  2011-02-15 16:48:54.993 -FATAL- [APUSRMGR0001201102151648315060002] R[/login] U[9999999999] fail_code = [FW_DATE_ERROR] segment was not found. segment:00.
  Stack Trace Information :
  java.lang.IllegalStateException: segment was not found. segment:00.
      at nablarch.core.date.BasicBusinessDateProvider.getDate(BasicBusinessDateProvider.java:103)
      # 以后的堆栈跟踪省略。

nablarch.core.message.StringResourceHolder类抛出异常的情况
 .. code-block:: bash

  # 属性文件的nablarch.core.message=FW_MESSAGE_ERROR适用。
  2011-02-15 16:54:06.413 -FATAL- [APUSRMGR0001201102151653476260011] R[/users/edit] U[0000000001] fail_code = [FW_MESSAGE_ERROR] ValidateFor method invocation failed. targetClass = java.lang.Class, method = validateForRegisterUser
  Stack Trace Information :
  java.lang.RuntimeException: ValidateFor method invocation failed. targetClass = java.lang.Class, method = validateForRegisterUser
      at nablarch.core.validation.ValidationManager.validateAndConvert(ValidationManager.java:202)
      # 中间的堆栈跟踪省略。
  Caused by: nablarch.core.message.MessageNotFoundException: message was not found. message id = MSG00010
      at nablarch.core.message.StringResourceHolder.get(StringResourceHolder.java:40)
      # 以后的堆栈跟踪省略。

nablarch.common.authentication.PasswordAuthenticator类抛出异常的情况
 .. code-block:: bash

  # 属性文件的nablarch=FW_ERROR适用。
  2011-02-15 16:59:03.076 -FATAL- [APUSRMGR0001201102151658551890017] R[/login] U[9999999999] fail_code = [FW_ERROR] authentication failed.
  Stack Trace Information :
  nablarch.common.authentication.AuthenticationFailedException
      at nablarch.common.authentication.PasswordAuthenticator.authenticate(PasswordAuthenticator.java:302)
      # 以后的堆栈跟踪省略。

.. _failure_log-output_src_exe_info:

输出来源运行时信息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
来源运行时信息是指，例如，从Web向批处理进行数据协作的情况下，
画面处理执行时的运行时信息成为批处理中的来源运行时信息。
以下，将处理方式间进行数据协作时，先进行处理的一侧称为前段处理，后进行处理的一侧称为后段处理。
在后段处理发生故障时，为了减轻前段处理的追踪工作而输出来源运行时信息。

输出来源运行时信息时，可以使用本功能的占位符"$data$"。
指定了占位符"$data$"时，将输出使用数据读取器读取的数据到故障日志。
使用此功能，通过在前段处理中预先在数据中包含运行时信息，
在后段处理发生故障时将作为处理对象数据输出前段处理的运行时信息。

这里，显示使用数据库进行数据协作时的来源运行时信息输出示例。
假设在前段处理中以下列名设置了运行时信息。

==================== ====================
项目                 列名
请求ID               INSERT_REQUEST_ID
运行时ID             INSERT_EXECUTION_ID
用户ID               UPDATED_USER_ID
==================== ====================

app-log.properties的设置示例
 .. code-block:: properties

  failureLogFormatter.defaultFailureCode=UNEXPECTED_ERROR
  failureLogFormatter.defaultMessage=an unexpected exception occurred.
  failureLogFormatter.notificationFormat=fail_code = [$failureCode$] $message$
  # 在处理对象数据的占位符"data"指定到故障解析日志的格式中。
  failureLogFormatter.analysisFormat=fail_code = [$failureCode$] $message$\nInput Data :\n$data$

故障解析日志的输出示例
 .. code-block:: bash

  # 故障解析日志
  2011-09-26 21:06:35.745 -FATAL- root [EXECUTION_ID_0000000123456789] boot_proc = [] proc_sys = [] req_id = [RB11AC0160] usr_id = [batchuser1] fail_code = [USER_REGISTER_FAILED] 用户信息注册失败。
  Input Data :
  {MOBILE_PHONE_NUMBER_AREA_CODE=002, KANJI_NAME=山本太郎, USER_INFO_ID=00000000000000000113, INSERT_EXECUTION_ID=EXECUTION_ID_2000000123456789, MAIL_ADDRESS=yamamoto@sample.com, MOBILE_PHONE_NUMBER_CITY_CODE=0003, UPDATED_USER_ID=batch_user, MOBILE_PHONE_NUMBER_SBSCR_CODE=0004, KANA_NAME=YamamotoTaro, EXTENSION_NUMBER_BUILDING=13, LOGIN_ID=12345678901234567890, EXTENSION_NUMBER_PERSONAL=1235, INSERT_REQUEST_ID=RB11AC0140}
  Stack Trace Information :
  [100 TransactionAbnormalEnd] 用户信息注册失败。
      at nablarch.sample.ss11AC.B11AC016Action.handle(B11AC016Action.java:73)
      at nablarch.sample.ss11AC.B11AC016Action.handle(B11AC016Action.java:1)
      at nablarch.fw.action.BatchAction.handle(BatchAction.java:1)
      # 以后的堆栈跟踪省略。

处理对象数据（输出示例的"Input Data :"）中输出以下运行时信息。
 .. code-block:: properties

  INSERT_REQUEST_ID=RB11AC0140
  INSERT_EXECUTION_ID=EXECUTION_ID_2000000123456789
  UPDATED_USER_ID=batch_user

.. _failure_log-placeholder_customize:

自定义占位符的输出处理
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
处理对象数据($data$)默认通过toString方法输出所有数据项，
因此可能存在项目安全要求需要对特定项目进行掩码输出的情况。
像这样，希望自定义占位符的输出处理时，请按以下方式处理。

* 创建实现了 :java:extdoc:`LogItem <nablarch.core.log.LogItem>` 的类
* 创建继承 :java:extdoc:`FailureLogFormatter <nablarch.core.log.app.FailureLogFormatter>` 的类，添加占位符
* 在设置中使用继承 :java:extdoc:`FailureLogFormatter <nablarch.core.log.app.FailureLogFormatter>` 的类

这里，显示处理对象数据($data$)输出处理的自定义示例。

创建实现了 :java:extdoc:`LogItem <nablarch.core.log.LogItem>` 的类
 创建提供处理对象数据($data$)输出内容的类。
 这次继承框架提供的 :java:extdoc:`DataItem <nablarch.core.log.app.FailureLogFormatter.DataItem>` 创建，
 仅在处理对象数据为Map型时进行掩码处理。

 .. code-block:: java

  // 作为FailureLogFormatter扩展类的内部类定义。
  private static final class CustomDataItem extends DataItem {

      /** 掩码字符 */
      private static final char MASKING_CHAR = '*';

      /** 掩码对象的模式 */
      private static final Pattern[] MASKING_PATTERNS
              = new Pattern[] { Pattern.compile(".*MOBILE_PHONE_NUMBER.*"),
                                Pattern.compile(".*MAIL.*")};

      /**
       * 掩码Map值的编辑器。
       * 框架提供的Map编辑工具。
       */
      private MapValueEditor mapValueEditor
          = new MaskingMapValueEditor(MASKING_CHAR, MASKING_PATTERNS);

      @Override
      @SuppressWarnings("unchecked")
      public String get(FailureLogContext context) {

          // 调用FailureLogContext的getData方法获取处理对象数据。
          Object data = context.getData();

          // 如果不是Map则调用框架的默认实现。
          if (!(data instanceof Map)) {
              return super.get(context);
          }

          // 返回掩码后的Map字符串。
          Map<String, String> editedMap = new TreeMap<String, String>();
          for (Map.Entry<Object, Object> entry : ((Map<Object, Object>) data).entrySet()) {
              String key = entry.getKey().toString();
              editedMap.put(key, mapValueEditor.edit(key, entry.getValue()));
          }
          return editedMap.toString();
      }
  }

创建继承 :java:extdoc:`FailureLogFormatter <nablarch.core.log.app.FailureLogFormatter>` 的类，添加占位符
 重写 :java:extdoc:`FailureLogFormatter#getLogItems <nablarch.core.log.app.FailureLogFormatter.getLogItems(java.util.Map)>`
 ，对占位符 ``$data$`` 设置上述的CustomDataItem。

 .. code-block:: java

  public class CustomDataFailureLogFormatter extends FailureLogFormatter {

      @Override
      protected Map<String, LogItem<FailureLogContext>> getLogItems(Map<String, String> props) {

          Map<String, LogItem<FailureLogContext>> logItems = super.getLogItems(props);

          // 使用CustomDataItem覆盖设置$data$。
          logItems.put("$data$", new CustomDataItem());

          return logItems;
      }

      private static final class CustomDataItem extends DataItem {
          // 省略。
      }
   }

在设置中使用继承 :java:extdoc:`FailureLogFormatter <nablarch.core.log.app.FailureLogFormatter>` 的类
 在 ``app-log.properties`` 中设置使用CustomDataFailureLogFormatter作为故障日志的格式化器。

 .. code-block:: properties

  # 指定CustomDataFailureLogFormatter。
  failureLogFormatter.className=nablarch.core.log.app.CustomDataFailureLogFormatter
  failureLogFormatter.defaultFailureCode=UNEXPECTED_ERROR
  failureLogFormatter.defaultMessage=an unexpected exception occurred.
  failureLogFormatter.notificationFormat=fail_code = [$failureCode$] $message$
  failureLogFormatter.analysisFormat=fail_code = [$failureCode$] $message$\nInput Data :\n$data$

.. _failure_log-json_setting:

作为JSON格式的结构化日志输出
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
通过 :ref:`log-json_log_setting` 设置可以以JSON格式输出日志，
但在 :java:extdoc:`FailureLogFormatter <nablarch.core.log.app.FailureLogFormatter>` 中
故障日志的各项是作为字符串输出到message的值中。
要将故障日志的各项也作为JSON的值输出，
请使用 :java:extdoc:`FailureJsonLogFormatter <nablarch.core.log.app.FailureJsonLogFormatter>` 。
设置在 :ref:`log-app_log_setting` 中说明的属性文件中进行。

描述规则
 使用 :java:extdoc:`FailureJsonLogFormatter <nablarch.core.log.app.FailureJsonLogFormatter>` 时
 指定的属性如下。
 
 failureLogFormatter.className ``必需``
  以JSON格式输出日志时，
  指定 :java:extdoc:`FailureJsonLogFormatter <nablarch.core.log.app.FailureJsonLogFormatter>` 。
 
 failureLogFormatter.defaultFailureCode ``必需``
  默认的故障代码。
  在异常处理器中捕获异常或错误等情况，没有指定故障代码时使用。
 
 failureLogFormatter.defaultMessage ``必需``
  默认的消息。
  使用默认故障代码时输出的消息。
 
 failureLogFormatter.language
  从故障代码获取消息时使用的语言。
  未指定时使用 :java:extdoc:`ThreadContext <nablarch.core.ThreadContext>` 中设置的语言。
 
 .. _failure_log-prop_notification_targets:
 
 failureLogFormatter.notificationTargets
  故障通知日志的输出项。以逗号分隔指定。
 
  可指定的输出项以及默认输出项
   \

   .. list-table::
      :header-rows: 1
      :class: white-space-normal
      :widths: 25,20,60,30

      * - 项目名
        - 输出项
        - 说明
        - 默认输出

      * - 故障代码
        - failureCode
        - 唯一标识故障的代码。用于确定故障内容。
        - ○

      * - 消息
        - message
        - 与故障代码对应的消息。用于确定故障内容。
        - ○

      * - 处理对象数据
        - data
        - 用于确定故障发生处理所针对的数据。
          调用使用数据读取器读取的数据对象的toString方法输出。
        - 

      * - 联系方式
        - contact
        - 用于确定联系方式。
        - 

 failureLogFormatter.analysisTargets
  故障解析日志的输出项。以逗号分隔指定。
  可指定的输出项和默认设置与
  :ref:`故障通知日志的输出项 <failure_log-prop_notification_targets>` 相同。
 
 failureLogFormatter.contactFilePath
  指定了故障联系方式信息的属性文件的路径。
  需要输出故障联系方式信息时指定。
  详细内容请参考 :ref:`failure_log-add_contact` 。
 
 failureLogFormatter.fwFailureCodeFilePath
  指定了框架故障代码更改信息的属性文件的路径。
  需要在输出故障日志时更改框架的故障代码时指定。
  详细内容请参考 :ref:`failure_log-change_fw_failure_code` 。
 
 failureLogFormatter.structuredMessagePrefix
  为了识别格式化后的消息字符串已格式化为JSON格式，在消息开头附加的标记字符串。
  如果消息开头的标记字符串与 :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` 中设置的标记字符串一致， :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` 会将消息作为JSON数据处理。
  默认为 ``"$JSON$"`` 。
  更改时，请使用LogWriter的 ``structuredMessagePrefix`` 属性为 :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` 设置相同的值（关于LogWriter的属性请参考 :ref:`log-basic_setting` ）。
 
描述示例
 .. code-block:: properties
 
  failureLogFormatter.className=nablarch.core.log.app.FailureJsonLogFormatter
  failureLogFormatter.structuredMessagePrefix=$JSON$
  failureLogFormatter.notificationTargets=failureCode,message,contact
  failureLogFormatter.analysisTargets=failureCode,message,data
  failureLogFormatter.defaultFailureCode=UNEXPECTED_ERROR
  failureLogFormatter.defaultMessage=an unexpected exception occurred.
