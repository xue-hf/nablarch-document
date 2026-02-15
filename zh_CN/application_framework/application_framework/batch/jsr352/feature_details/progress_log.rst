进度日志输出
==================================================
.. contents:: 目录
  :depth: 3
  :local:
  
.. _jsr352-progress_log:

进度日志输出的内容
--------------------------------------------------
以下内容将输出到日志中。

* 作业的开始和结束日志
* 步骤的开始和结束日志
* 处理对象件数日志（处理对象件数需要在应用侧获取）
* 步骤的进度日志

  * 从开始后的TPS（从处理对象件数和处理完成件数计算得出的TPS）
  * 最新的TPS（从前次TPS计算时经过的时间和处理件数计算得出的TPS）
  * 未处理件数
  * 结束预测时间（从未处理件数和TPS计算的步骤结束预测时间）
  
以下显示输出示例。

.. code-block:: bash

  INFO progress start job. job name: [test-job]
  INFO progress start step. job name: [test-job] step name: [test-step]
  INFO progress job name: [test-job] step name: [test-step] input count: [25]
  INFO progress job name: [test-job] step name: [test-step] total tps: [250.00] current tps: [250.00] estimated end time: [2017/02/13 04:02:25.656] remaining count: [15]
  INFO progress job name: [test-job] step name: [test-step] total tps: [384.62] current tps: [519.32] estimated end time: [2017/02/13 04:02:25.668] remaining count: [5]
  INFO progress job name: [test-job] step name: [test-step] total tps: [409.84] current tps: [450.00] estimated end time: [2017/02/13 04:02:25.677] remaining count: [0]
  INFO progress finish step. job name: [test-job] step name: [test-step] step status: [null]
  INFO progress finish job. job name: [test-job]

添加将进度日志输出到专用日志文件的设置
-----------------------------------------------------------------
表示进度的日志，使用 ``progress`` 作为日志类别名输出。
使用这个类别名，可以将日志输出到进度日志专用的文件中。

以下显示使用 :ref:`log` 时的 ``log.properties`` 设置示例。
如果使用 :ref:`log_adaptor` ，请参考适配器对应的日志库手册等进行设置。

.. code-block:: properties

  # progress log file
  writer.progressLog.className=nablarch.core.log.basic.FileLogWriter
  writer.progressLog.filePath=./log/progress.log
  writer.progressLog.encoding=UTF-8
  writer.progressLog.formatter.className=nablarch.core.log.basic.BasicLogFormatter
  writer.progressLog.formatter.format=$date$ -$logLevel$- $message$
  
  # logger list
  availableLoggersNamesOrder=SQL,MON,PROGRESS,ROO
  
  # progress logger setting
  loggers.PROGRESS.nameRegex=progress
  loggers.PROGRESS.level=INFO
  loggers.PROGRESS.writerNames=progressLog

在Batchlet步骤中输出进度日志
--------------------------------------------------
以下显示在Batchlet步骤中将进度输出到日志的实现示例。

另外，Batchlet基本上是执行任务导向的处理，因此需要进度日志的情况较少。
如果在Batchlet中需要进行伴随循环的处理时，可以参考以下实现示例输出进度日志。

要点
  * 在process方法的头部，获取处理对象件数（数据库count结果或文件记录数等），设置到 :java:extdoc:`inputCount <nablarch.fw.batch.ee.progress.ProgressManager.setInputCount(long)>` 中。
  
    .. important::
    
      TPS计算的起点时间，是在调用 :java:extdoc:`inputCount <nablarch.fw.batch.ee.progress.ProgressManager.setInputCount(long)>` 的时间点。
      如果在调用 :java:extdoc:`inputCount <nablarch.fw.batch.ee.progress.ProgressManager.setInputCount(long)>` 后执行从数据库提取对象数据等重处理，
      TPS会与实际不同（比实际小的值），请注意。
      
  * 在执行处理的循环内，以一定间隔调用输出进度日志的 :java:extdoc:`outputProgressInfo <nablarch.fw.batch.ee.progress.ProgressManager.outputProgressInfo(long)>` 。

实现示例
  .. code-block:: java

    @Named
    @Dependent
    public class ProgressBatchlet extends AbstractBatchlet {

        /** 输出进度日志的功能 */
        private final ProgressManager progressManager;
        
        /** 输出进度日志的间隔 */
        private static final int PROGRESS_LOG_INTERVAL = 1000;

        /**
         * 使用构造器注入注入输出进度日志的功能。
         */
        @Inject
        public ProgressBatchlet(ProgressManager progressManager) {
          this.progressManager = progressManager;
        }

        @Override
        public String process() throws Exception {
         
          // 设置处理对象件数。
          // 实际中，数据库或文件的记录数等即为处理件数。
          progressManager.setInputCount(10000);
          
          // 处理完成件数
          long processedCount = 0;
          
          while (处理对象存在期间) {
              processedCount++;
              
              // 实际处理省略
              
              if (processedCount % PROGRESS_LOG_INTERVAL == 0) {
                // 将处理完成件数传递给进度日志输出功能，即可输出进度日志
                progressManager.outputProgressInfo(processedCount);
              }
          }
          return "SUCCESS";
        }
    }
  
在Chunk步骤中输出进度日志
--------------------------------------------------
以下显示在Chunk步骤中将进度输出到日志的实现示例。

.. _jsr352-progress_reader:

ItemReader
  要点
    * 使用构造器注入注入输出进度日志的接口( :java:extdoc:`ProgressManager <nablarch.fw.batch.ee.progress.ProgressManager>` )。
    * 在open方法中，获取处理对象件数（数据库count结果或文件记录数等），设置到 :java:extdoc:`inputCount <nablarch.fw.batch.ee.progress.ProgressManager.setInputCount(long)>` 中。
    
      .. important::
      
        TPS计算的起点时间，是在调用 :java:extdoc:`inputCount <nablarch.fw.batch.ee.progress.ProgressManager.setInputCount(long)>` 的时间点。
        如果在调用 :java:extdoc:`inputCount <nablarch.fw.batch.ee.progress.ProgressManager.setInputCount(long)>` 后执行从数据库提取对象数据等重处理，
        TPS会与实际不同（比实际小的值），请注意。
    
  实现示例
    .. code-block:: java

      @Named
      @Dependent
      public class ProgressReader extends AbstractItemReader {

        /** 输出进度日志的功能 */
        private final ProgressManager progressManager;

        /**
         * 使用构造器注入注入输出进度日志的功能。
         */
        @Inject
        public ProgressReader(ProgressManager progressManager) {
            this.progressManager = progressManager;
        }

        @Override
        public void open(Serializable checkpoint) throws Exception {
          // 在open方法内，将处理对象件数设置到输出进度日志的功能中。
          // 实际中，设置为对数据库的count语句结果或文件记录数。
          progressManager.setInputCount(10000);
        }

        @Override
        public Object readItem() throws Exception {
          // 省略
        }
      }

.. _jsr352-progress_listener:

作业定义文件
  要点
    * 在step下的监听器列表中设置输出进度日志的监听器（名称固定为 ``progressLogListener`` ）。
    
  实现示例
    .. code-block:: xml
    
      <job id="batchlet-progress-test" xmlns="https://jakarta.ee/xml/ns/jakartaee" version="2.0">
        <listeners>
          <listener ref="nablarchJobListenerExecutor" />
        </listeners>
      
        <step id="step">
          <listeners>
            <listener ref="nablarchStepListenerExecutor" />
            <listener ref="nablarchItemWriteListenerExecutor" />
            <!-- 在step下设置输出进度日志的监听器。 -->
            <listener ref="progressLogListener" />
          </listeners>
          <chunk item-count="1000">
            <reader ref="progressReader" />
            <writer ref="progressWriter" />
          </chunk>
        </step>
      </job>

.. important::
  如果在 :ref:`ItemReader <jsr352-progress_reader>` 中没有设置处理对象件数，
  却设置了 :ref:`进度日志输出监听器 <jsr352-progress_listener>` ，将作为设置不完整的错误抛出异常并异常结束处理。
  因此，如果不需要进度日志，请务必删除 :ref:`进度日志输出监听器 <jsr352-progress_listener>` 的设置。
  
.. important::
  在chunk步骤中设置了Retrying Exceptions时，监听器输出的进度日志将无法正常运作。
  这是因为监听器用作处理完成件数的 :java:extdoc:`metrics <jakarta.batch.runtime.context.StepContext.getMetrics()>`
  的读取完成件数与实际不符。
  
  因此，如果想使用Retrying Exceptions进行异常发生时的重试处理，需要在 :java:extdoc:`ItemWriter <jakarta.batch.api.chunk.ItemWriter>` 的实现类中计算处理完成件数，
  使用 :java:extdoc:`outputProgressInfo <nablarch.fw.batch.ee.progress.ProgressManager.outputProgressInfo(long)>` 输出进度日志。
  

