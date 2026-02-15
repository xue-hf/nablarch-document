.. _`getting_started_batchlet`:

创建删除目标表数据的Batch（Batchlet步骤）
================================================================
以Example应用为基础，解说使用 :ref:`batchlet步骤<jsr352-batch_type_Batchlet>` 删除目标表数据的Batch。

创建的功能说明
  1. 确认当前DB的状态

     从H2控制台执行以下SQL。

     .. code-block:: sql

       SELECT * FROM ZIP_CODE_DATA;
       SELECT * FROM ZIP_CODE_DATA_WORK;

     如果数据未注册，则执行步骤2的操作。

  2. （数据未注册时）将数据库重置为初始状态

    从命令提示符执行以下命令。

    .. code-block:: bash

      $cd {nablarch-example-batch-ee系统仓库}
      $mvn generate-resources

    从H2控制台执行以下SQL确认数据已注册。

    .. code-block:: sql

      SELECT * FROM ZIP_CODE_DATA;
      SELECT * FROM ZIP_CODE_DATA_WORK;

  3. 执行地址表删除Batch

    从命令提示符执行以下命令。

    .. code-block:: bash

      $cd {nablarch-example-batch-ee系统仓库}
      $mvn exec:java -Dexec.mainClass=nablarch.fw.batch.ee.Main ^
          -Dexec.args=zip-code-truncate-table

  4. 确认目标表的数据已被删除

     从H2控制台执行以下SQL，确认数据已被删除。

     .. code-block:: sql

       SELECT * FROM ZIP_CODE_DATA;
       SELECT * FROM ZIP_CODE_DATA_WORK;

删除目标表的数据
---------------------------------
说明删除地址信息Batch的实现方法。

关于处理流程，请参考 :ref:`Batchlet步骤的Batch处理流程<jsr352-batch_flow_batchlet>` 。
关于职责配置，请参考 :ref:`Batchlet步骤的职责配置<jsr352-batchlet_design>` 。

  #. :ref:`创建Batchlet<getting_started_batchlet_create>`
  #. :ref:`创建JOB设置文件<getting_started_batchlet_job>`

.. _`getting_started_batchlet_create`:

创建Batchlet
  创建删除地址信息Batch的Batchlet类。

  应实现的接口及其职责
    Batchlet类通过实现以下接口来创建Batch处理。重写的方法将由Batch Runtime在适当的时机调用。

   ==================================================================   =============================================================================================
   接口                                                                 实现
   ==================================================================   =============================================================================================
   :java:extdoc:`Batchlet<jakarta.batch.api.Batchlet>`                    实现Batch处理。

                                                                        继承提供默认实现的 :java:extdoc:`AbstractBatchlet<jakarta.batch.api.AbstractBatchlet>` 。

                                                                          * `Batchlet#process`
                                                                          * `Batchlet#stop`
   ==================================================================   =============================================================================================

  .. tip::

    Batch处理除了实现上述接口外，还通过提供事务控制等通用处理的监听器来构成。
    监听器的详细信息请参考 :ref:`Batch应用中使用的监听器<jsr352-listener>` 以及 :ref:`监听器的指定方法<jsr352-listener_definition>` 。

  TruncateTableBatchlet.java
    .. code-block:: java

      @Dependent
      @Named
      public class TruncateTableBatchlet extends AbstractBatchlet {

          @Inject
          @BatchProperty
          private String tableName;

          @Override
          public String process() {

              final AppDbConnection conn = DbConnectionContext.getConnection();
              final SqlPStatement statement
                  = conn.prepareStatement("TRUNCATE TABLE " + tableName);
              statement.executeUpdate();

              return "SUCCESS";
          }
      }

    这个实现的要点
      * 继承 :java:extdoc:`AbstractBatchlet<jakarta.batch.api.AbstractBatchlet>` ，在 `process` 方法中执行业务处理。

      .. _getting_started_batchlet-cdi:

      * 在类上添加 :java:extdoc:`Named<jakarta.inject.Named>` 和 :java:extdoc:`Dependent<jakarta.enterprise.context.Dependent>` 。 |br|
        设置Named及Dependent注解后，可以将Batchlet实现类作为CDI的管理Bean。
        这样，就可以在作业定义中使用CDI的管理名来记述Batchlet类名。 |br|
        （如果不作为CDI管理Bean，则需要使用完全限定名(FQCN)来记述）

      * 使用 :ref:`数据库访问<database>` 执行TRUNCATE语句。

.. _`getting_started_batchlet_job`:

创建作业定义文件
  创建定义作业执行设置的文件。

  zip-code-truncate-table.xml
    .. code-block:: xml

     <job id="zip-code-truncate-table" xmlns="https://jakarta.ee/xml/ns/jakartaee" version="2.0">
       <listeners>
         <listener ref="nablarchJobListenerExecutor" />
       </listeners>

       <step id="step1" next="step2">
         <listeners>
           <listener ref="nablarchStepListenerExecutor" />
         </listeners>
         <batchlet ref="truncateTableBatchlet">
           <properties>
             <property name="tableName" value="ZIP_CODE_DATA" />
           </properties>
         </batchlet>
       </step>
       <step id="step2">
         <listeners>
           <listener ref="nablarchStepListenerExecutor" />
         </listeners>
         <batchlet ref="truncateTableBatchlet">
           <properties>
             <property name="tableName" value="ZIP_CODE_DATA_WORK" />
           </properties>
         </batchlet>
       </step>
     </job>

  这个实现的要点
    * 作业定义文件放置在 `/src/main/resources/META-INF/batch-jobs/` 下。
    * `job` 元素的 `id` 属性指定作业名称。
    * 由多个步骤构成的Batch作业，需要定义多个 `step` 元素，依次执行处理。
    * `batchlet` 元素的 `ref` 属性指定将Batchlet类名首字母小写后的名称。
    * `property` 元素指定注入到Batchlet类属性的值。
    * 配置文件的详细记述方法请参考 |jsr352|

.. |jsr352| raw:: html

  <a href="https://jakarta.ee/specifications/batch/" target="_blank">Jakarta Batch(外部网站，英语)</a>

.. |br| raw:: html

  <br />
