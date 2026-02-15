Jakarta Batch应用的启动
==================================================
.. contents:: 目录
  :depth: 3
  :local:

.. _jsr352_run_batch_application:

启动Batch应用
--------------------------------------------------
对于符合Jakarta Batch的Batch应用，Batch的启动使用Jakarta Batch规定的API进行。

Nablarch提供了 :java:extdoc:`nablarch.fw.batch.ee.Main` 作为标准实现类。
该类将目标JOB的XML文件名（不含.xml扩展名）作为执行参数指定。

如果想在作业执行时指定参数，需要向 :java:extdoc:`nablarch.fw.batch.ee.Main` 指定启动选项。
启动选项中指定的值将被设置到 :java:extdoc:`JobOperator#start <jakarta.batch.operations.JobOperator.start(java.lang.String,java.util.Properties)>` 的jobParameters中。

启动选项需要在名称前添加 ``--`` ，在名称后的参数中设置值。

启动选项使用示例
  .. code-block:: bash

    # 在这个例子中，将设置「option1=value1」和「option2=value2」两个jobParameters。
    $ java nablarch.fw.batch.ee.Main jobName --option1 value1 --option2 value2
  
.. tip::

  创建项目特有的启动类时，也可以参考这个Main类进行实现。


.. _jsr352_exitcode_batch_application:

Batch应用的退出码
--------------------------------------------------
上述Main类程序的退出码如下。

* 正常结束：0 - 结束状态为 "WARNING" 以外，且Batch状态为 :java:extdoc:`BatchStatus.COMPLETED <jakarta.batch.runtime.BatchStatus>` 的情况
* 异常结束：1 - 结束状态为 "WARNING" 以外，且Batch状态为 :java:extdoc:`BatchStatus.COMPLETED <jakarta.batch.runtime.BatchStatus>` 以外的情况
* 警告结束：2 - 结束状态为 "WARNING" 的情况

另外，如果在等待JOB结束期间被中断，则返回异常结束的代码。

在发生验证错误等需要警告的事项时，可以进行警告结束。
警告结束的方法是在chunk或batchlet内调用 :java:extdoc:`JobContext#setExitStatus(String) <jakarta.batch.runtime.context.JobContext.setExitStatus(java.lang.String)>`
将 "WARNING" 设置为结束状态。警告结束时，允许Batch状态为任意值，
因此即使抛出异常导致Batch状态变为 :java:extdoc:`BatchStatus.COMPLETED <jakarta.batch.runtime.BatchStatus>` 以外，
只要将 "WARNING" 设置为结束状态，上述类就会进行警告结束。

.. _jsr352_run_batch_init_repository:

初始化系统仓库
--------------------------------------------------
:ref:`repository` 可以通过在作业监听器中设置 ``nablarchJobListenerExecutor`` 来初始化。

系统仓库的根xml文件文件名为 ``batch-boot.xml`` ，放置在类路径根目录下。
如果要更改文件名或放置位置，可以通过 ``nablarchJobListenerExecutor`` 的参数进行更改。

以下显示示例。

使用默认的 ``batch-boot.xml`` 时的示例
  .. code-block:: xml

    <job id="sample-job" xmlns="https://jakarta.ee/xml/ns/jakartaee" version="2.0">
      <listeners>
        <!-- 在作业监听器中设置nablarchJobListenerExecutor -->
        <listener ref="nablarchJobListenerExecutor" />
      </listeners>

      <!-- 步骤定义省略 -->
    </job>

使用默认以外的配置文件时的示例
  .. code-block:: xml

    <job id="sample-job" xmlns="https://jakarta.ee/xml/ns/jakartaee" version="2.0">
      <listeners>
        <listener ref="nablarchJobListenerExecutor">
          <properties>
            <!--
            在diConfigFilePath属性中设置要加载的xml
            这个例子中，类路径下的「sample_project/batch-boot.xml」
            将被加载到系统仓库
            -->
            <property name="diConfigFilePath" value="sample_project/batch-boot.xml" />
          </properties>
        </listener>
      </listeners>

      <!-- 步骤定义省略 -->
    </job>
