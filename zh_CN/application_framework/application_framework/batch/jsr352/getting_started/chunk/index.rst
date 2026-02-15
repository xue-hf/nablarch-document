.. _`getting_started_chunk`:

创建导出数据的Batch（Chunk步骤）
===============================================================
以Example应用为基础，解说从现有数据进行计算并新导出数据的 :ref:`Chunk步骤<jsr352-batch_type_chunk>` 方式的Batch。

创建的功能概述
  .. image:: ../images/chunk/overview.png

操作确认步骤
  1. 删除注册目标表（奖金表）的数据

     从H2控制台执行以下SQL，删除奖金表的数据。

     .. code-block:: sql

       TRUNCATE TABLE BONUS;

  2. 执行奖金计算Batch

     从命令提示符执行奖金计算Batch。

    .. code-block:: bash

      $cd {nablarch-example-batch-ee系统仓库}
      $mvn exec:java -Dexec.mainClass=nablarch.fw.batch.ee.Main ^
          -Dexec.args=bonus-calculate

  5. 确认Batch执行后的状态

    从H2控制台执行以下SQL，确认奖金信息已注册。

    .. code-block:: sql

        SELECT * FROM BONUS;

导出数据
-------------------
按以下顺序说明从现有数据新导出数据的Batch实现方法。

#. :ref:`getting_started_chunk-read`
#. :ref:`getting_started_chunk-business_logic`
#. :ref:`getting_started_chunk-persistence`
#. :ref:`getting_started_chunk-job`

关于处理流程，请参考 :ref:`Chunk步骤的Batch处理流程<jsr352-batch_flow_chunk>` 。
关于职责配置，请参考 :ref:`Chunk步骤的职责配置<jsr352-chunk_design>` 。

Batch处理通过实现 |jsr352| 规定的接口，以及提供事务控制等通用处理的监听器来构成。
监听器的详细信息请参考 :ref:`Batch应用中使用的监听器<jsr352-listener>` 以及 :ref:`监听器的指定方法<jsr352-listener>` 。

.. _`getting_started_chunk-read`:

从输入数据源读取数据
+++++++++++++++++++++++++++++++++++++
实现获取计算所需数据的处理。

#. :ref:`创建Form<getting_started_chunk-form>`
#. :ref:`创建ItemReader<getting_started_chunk-reader>`

.. _`getting_started_chunk-form`:

创建Form
  在Chunk步骤中，使用Form在 :java:extdoc:`ItemReader<jakarta.batch.api.chunk.ItemReader>` 和
  :java:extdoc:`ItemProcessor<jakarta.batch.api.chunk.ItemProcessor>` 之间进行数据传递。

  EmployeeForm.java
    .. code-block:: java

      public class EmployeeForm {

          //仅摘录部分

          /** 员工ID */
          private Long employeeId;

          /**
           * 返回员工ID。
           *
           * @return 员工ID
           */
          public Long getEmployeeId() {
              return employeeId;
          }

          /**
           * 设置员工ID。
           *
           * @param employeeId 员工ID
           */
          public void setEmployeeId(Long employeeId) {
              this.employeeId = employeeId;
          }
      }

.. _`getting_started_chunk-reader`:

创建ItemReader
  继承 :java:extdoc:`AbstractItemReader<jakarta.batch.api.chunk.AbstractItemReader>` ，进行数据读取。

    ==================================================================   =============================================================================================
    接口名                                                               职责
    ==================================================================   =============================================================================================
    :java:extdoc:`ItemReader<jakarta.batch.api.chunk.ItemReader>`          进行数据读取。

                                                                         继承提供空实现的 :java:extdoc:`AbstractItemReader<jakarta.batch.api.chunk.AbstractItemReader>` 。

                                                                           * `ItemReader#open`
                                                                           * `ItemReader#readItem`
                                                                           * `ItemReader#close`
    ==================================================================   =============================================================================================

  EmployeeSearchReader.java
    .. code-block:: java

      @Dependent
      @Named
      public class EmployeeSearchReader extends AbstractItemReader {

          /** 员工信息列表 */
          private DeferredEntityList<EmployeeForm> list;

          /** 保存员工信息的迭代器 */
          private Iterator<EmployeeForm> iterator;

          @Override
          public void open(Serializable checkpoint) throws Exception {
              list = (DeferredEntityList<EmployeeForm>) UniversalDao.defer()
                      .findAllBySqlFile(EmployeeForm.class, "SELECT_EMPLOYEE");
              iterator = list.iterator();
          }

          @Override
          public Object readItem() {
              if (iterator.hasNext()) {
                  return iterator.next();
              }
              return null;
          }

          @Override
          public void close() throws Exception {
              list.close();
          }
      }

  EmployeeForm.sql
    .. code-block:: java

      SELECT_EMPLOYEE=
      SELECT
          EMPLOYEE.EMPLOYEE_ID,
          EMPLOYEE.FULL_NAME,
          EMPLOYEE.BASIC_SALARY,
          EMPLOYEE.GRADE_CODE,
          GRADE.BONUS_MAGNIFICATION,
          GRADE.FIXED_BONUS
      FROM
          EMPLOYEE
      INNER JOIN GRADE ON EMPLOYEE.GRADE_CODE = GRADE.GRADE_CODE

  这个实现的要点
    * 在类上添加 :java:extdoc:`Named<jakarta.inject.Named>` 和 :java:extdoc:`Dependent<jakarta.enterprise.context.Dependent>` 。
      详细信息请参考 :ref:`Batchlet的Named和Dependent说明 <getting_started_batchlet-cdi>` 。
    * 在 `open` 方法中读取处理对象的数据。
    * SQL文件的放置位置和创建方法等，请参考 :ref:`universal_dao-sql_file` 。
    * 读取大量数据时，为防止内存压力，使用 :java:extdoc:`UniversalDao#defer <nablarch.common.dao.UniversalDao.defer()>`
      进行 :ref:`延迟加载<universal_dao-lazy_load>` 。
    * 在 `readItem` 方法中从读取的数据返回一行数据。
      在这个方法中返回的对象，将作为后续 :java:extdoc:`ItemProcessor<jakarta.batch.api.chunk.ItemProcessor>` 的 `processItem` 方法的参数传入。

.. _`getting_started_chunk-business_logic`:

执行业务逻辑
++++++++++++++++++++++
实现奖金计算等业务逻辑。

创建ItemProcessor
  实现 :java:extdoc:`ItemProcessor<jakarta.batch.api.chunk.ItemProcessor>` ，
  执行业务逻辑（持久化处理是 :java:extdoc:`ItemWriter<jakarta.batch.api.chunk.ItemWriter>` 的职责，因此不执行）。

    =====================================================================   =============================================================================================
    接口名                                                                  职责
    =====================================================================   =============================================================================================
    :java:extdoc:`ItemProcessor<jakarta.batch.api.chunk.ItemProcessor>`      对一行数据进行业务处理。

                                                                               * `ItemProcessor#processItem`
    =====================================================================   =============================================================================================

  BonusCalculateProcessor.java
    .. code-block:: java

      @Dependent
      @Named
      public class BonusCalculateProcessor implements ItemProcessor {

          @Override
          public Object processItem(Object item) {

              EmployeeForm form = (EmployeeForm) item;
              Bonus bonus = new Bonus();
              bonus.setEmployeeId(form.getEmployeeId());
              bonus.setPayments(calculateBonus(form));

              return bonus;
          }

          /**
           * 根据员工信息进行奖金计算。
           *
           * @param form 员工信息Form
           * @return 奖金
           */
          private static Long calculateBonus(EmployeeForm form) {
              if (form.getFixedBonus() == null) {
                  return form.getBasicSalary() * form.getBonusMagnification() / 100;
              } else {
                  return form.getFixedBonus();
              }
          }
      }

  这个实现的要点
    * 当 `processItem` 方法返回一定数量的实体时（ :ref:`getting_started_chunk-job` 中解说设置方法），
      将执行后续 :java:extdoc:`ItemWriter<jakarta.batch.api.chunk.ItemWriter>` 的 `writeItems` 方法。

.. _`getting_started_chunk-persistence`:

执行持久化处理
++++++++++++++++++++
实现DB更新等持久化处理。

创建ItemWriter
  实现 :java:extdoc:`ItemWriter<jakarta.batch.api.chunk.ItemWriter>` ，进行数据持久化。

    ==================================================================   =============================================================================================
    接口名                                                                职责
    ==================================================================   =============================================================================================
    :java:extdoc:`ItemWriter<jakarta.batch.api.chunk.ItemWriter>`          进行数据持久化。

                                                                           * `ItemWriter#writeItems`
    ==================================================================   =============================================================================================

  BonusWriter.java
    .. code-block:: java

      @Dependent
      @Named
      public class BonusWriter extends AbstractItemWriter {

          @Override
          public void writeItems(List<Object> items) {
              UniversalDao.batchInsert(items);
          }
      }

  这个实现的要点
    * 使用 :java:extdoc:`UniversalDao#batchInsert <nablarch.common.dao.UniversalDao.batchInsert(java.util.List)>` 批量注册实体列表。
    * `writeItems` 方法执行后事务将提交，并开始新的事务。
    * `writeItems` 方法执行后，Batch处理将从 `readItem` 方法执行开始重复进行。

.. _`getting_started_chunk-job`:

创建JOB设置文件
+++++++++++++++++++++++++
创建记载JOB执行设置的文件。

  bonus-calculate.xml
    .. code-block:: xml

     <job id="bonus-calculate" xmlns="https://jakarta.ee/xml/ns/jakartaee" version="2.0">
       <listeners>
         <listener ref="nablarchJobListenerExecutor" />
       </listeners>

       <step id="step1">
         <listeners>
           <listener ref="nablarchStepListenerExecutor" />
           <listener ref="nablarchItemWriteListenerExecutor" />
         </listeners>

         <chunk item-count="1000">
           <reader ref="employeeSearchReader" />
           <processor ref="bonusCalculateProcessor" />
           <writer ref="bonusWriter" />
         </chunk>
       </step>
     </job>

  这个实现的要点
    * 作业定义文件放置在 `/src/main/resources/META-INF/batch-jobs/` 下。
    * `job` 元素的 `id` 属性指定作业名称。
    * `chunk` 元素的 `item-count` 属性设置 `writeItems` 每次处理的件数。
    * 配置文件的详细记述方法请参考 |jsr352| 。

.. |jsr352| raw:: html

  <a href="https://jakarta.ee/specifications/batch/" target="_blank">Jakarta Batch(外部网站，英语)</a>
