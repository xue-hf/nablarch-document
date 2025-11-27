.. _`getting_started_nablarch_batch`:

创建一个读取文件写入数据库的Batch应用
==========================================================
根据Example应用说明一个读取文件写入数据库的Batch应用。

目标功能概述
  .. image:: ../images/overview.png

住址文件登录Batch执行说明
  1. 删除登录目标表的数据

     在H2控制台执行下面的SQL，数据登录的目标表的数据删除。

     .. code-block:: sql

       TRUNCATE TABLE ZIP_CODE_DATA;

  2. 执行住址文件登录Batch

    在命令提示行中执行下面的命令。

    .. code-block:: bash

      $cd {nablarch-example-batch仓库}
      $mvn exec:java -Dexec.mainClass=nablarch.fw.launcher.Main ^
          -Dexec.args="'-requestPath' 'ImportZipCodeFileAction/ImportZipCodeFile' '-diConfig' 'classpath:import-zip-code-file.xml' '-userId' '105'"

  3. 确认数据库中登录的文件中的内容

     在H2控制台执行下面的SQL，确认住址信息被正确登录了。

     .. code-block:: sql

       SELECT * FROM ZIP_CODE_DATA;

将文件中的数据登录到数据库中
---------------------------------------
关于如何创建将文件中的数据登录到数据库中的Batch，
在 :ref:`从输入数据源读取数据<getting_started_nablarch_batch-read>`
和 :ref:`执行业务逻辑<getting_started_nablarch_batch-business-action>` 中分开进行了说明。

处理流程请参考 :ref:`Nablarch Batch的处理流程<nablarch_batch-process_flow>` 。
关于职责配置请参考 :ref:`Nablarch Batch应用职责配置<nablarch_batch-application_design>` 。

住址文件登录Batch的handler构成请参考 `import-zip-code-file.xml`

.. _`getting_started_nablarch_batch-read`:

从输入数据源读取数据
++++++++++++++++++++++++++++++++++++
接下来说明从输入数据源读取数据的相关内容。

#. :ref:`创建接收输入文件的表单<getting_started_nablarch_batch-form>`
#. :ref:`创建数据读取器<getting_started_nablarch_batch-data_reader>`

.. _`getting_started_nablarch_batch-form`:

创建接收输入文件的Form类
  使用 :ref:`data_bind` 创建绑定 CSV（住址文件）的Form类。

  ZipCodeForm.java
    .. code-block:: java

      @Csv(properties = {/** 省略属性定义 **/}, type = CsvType.CUSTOM)
      @CsvFormat(charset = "UTF-8", fieldSeparator = ',',
              ignoreEmptyLine = true, lineSeparator = "\r\n", quote = '"',
              quoteMode = QuoteMode.NORMAL, requiredHeader = false, emptyToNull = true)
      public class ZipCodeForm {

          // 仅提取部分字段

          /** 全国地方公共团体代码 */
          @Domain("localGovernmentCode")
          @Required
          private String localGovernmentCode;

          /**
           * 取得邮政编码（五位数）。
           *
           * @return 邮政编码（五位数）
           */
          public String getZipCode5digit() {
              return zipCode5digit;
          }

          /**
           * 用于保存行数的列
           */
          private Long lineNumber;

          /**
           * 取得行数。
           *
           * @return 行数
           */
          @LineNumber
          public Long getLineNumber() {
              return lineNumber;
          }

          // 省略了其他的getter和setter

      }

  实现要点：
    * 使用 :ref:`data_bind` 将 CSV 绑定到表单时，需附加 :java:extdoc:`Csv<nablarch.common.databind.csv.Csv>`
      和 :java:extdoc:`CsvFormat<nablarch.common.databind.csv.CsvFormat>` 。
    * 为执行 :ref:`bean_validation` ，需附加用于验证的注解。
    * 定义行数属性，并在 getter 上附加 :java:extdoc:`LineNumber<nablarch.common.databind.LineNumber>` 可自动设置目标数据所属的行号。

.. _`getting_started_nablarch_batch-data_reader`:

创建数据读取器
  创建 :java:extdoc:`DataReader<nablarch.fw.DataReader>` 的实现类，用于读取文件并将每一行传递给业务Action的处理方法。

  ZipCodeFileReader.java
    .. code-block:: java

      public class ZipCodeFileReader implements DataReader<ZipCodeForm> {

          /**
           * 读入的文件名
           */
          private static final String FILE_NAME = "importZipCode";

          /**
           * 返回处理对象的Iterator
           */
          private ObjectMapperIterator<ZipCodeForm> iterator;

          /**
           * 返回业务handler所需要处理的一行数据。
           *
           * @param ctx 运行上下文
           * @return 单行数据
           */
          @Override
          public ZipCodeForm read(ExecutionContext ctx) {
              if (iterator == null) {
                  initialize();
              }
              return iterator.next();
          }

          /**
           * 判断是否有后续数据。
           *
           * @param ctx 运行上下文
           * @return 如果有后续数据 {@code true} 、如果没有后续数据 {@code false}
           */
          @Override
          public boolean hasNext(ExecutionContext ctx) {
              if (iterator == null) {
                  initialize();
              }
              return iterator.hasNext();
          }

          /**
           * 关闭处理。
           * <p/>
           * 调用{@link ObjectMapperIterator#close()} 。
           * @param ctx 运行上下文
           */
          @Override
          public void close(ExecutionContext ctx) {
              iterator.close();
          }

          /**
           * 初始化处理。
           * <p/>
           * 创建iterator
           * @throws RuntimeException 文件读取失败
           */
          private void initialize() {
              FilePathSetting filePathSetting = FilePathSetting.getInstance();
              File zipCodeFile = filePathSetting.getFileWithoutCreate("csv-input", FILE_NAME);

              // 创建文件读出使用的iterator
              try {
                  iterator
                      = new ObjectMapperIterator<>(ObjectMapperFactory.create(ZipCodeForm.class,
                          new FileInputStream(zipCodeFile)));
              } catch (FileNotFoundException e) {
                  throw new IllegalStateException(e);
              }
          }
      }

  实现要点：
    * 在 `read` 方法中实现返回一行数据的逻辑。`read` 方法中读取的数据将会作为业务Action的参数。
    * 在 `hasNext` 方法中实现是否有下一条数据的判断的逻辑。这个方法返回 `false` 标志着文件读取结束。
    * 在 `close` 方法中实现关闭流的逻辑。

  .. tip::
    对于像 :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` 这样不提供
    `hasNext` 方法的类，通过创建迭代器，不仅可以简化数据读取器的实现，
    还能避免为每个批次单独实现数据读取逻辑的繁琐工作。
    有关迭代器的具体实现，请参考示例应用程序中的`ObjectMapperIterator.java`

.. _`getting_started_nablarch_batch-business-action`:

执行业务逻辑
++++++++++++++++++++++++++++++++++++
关于执行业务逻辑部分的说明。

#. :ref:`创建业务Action<getting_started_nablarch_batch-action>`

.. _`getting_started_nablarch_batch-action`:

创建业务Action
  继承 :java:extdoc:`BatchAction<nablarch.fw.action.BatchAction>` 创建业务Action。

  ImportZipCodeFileAction.java
    .. code-block:: java

      public class ImportZipCodeFileAction extends BatchAction<ZipCodeForm> {

         /**
          * 接收来自 {@link com.nablarch.example.app.batch.reader.ZipCodeFileReader} 的一行数据并将其注册到数据库中。
          *
          * 由于在方法执行时会被 {@link com.nablarch.example.app.batch.interceptor.ValidateData} 拦截，
          * 因此传入本方法的 {@param inputData} 始终为已通过验证的数据。
          *
          * @param inputData 一行住址信息
          * @param ctx 运行上下文
          * @return 结果对象
          */
          @Override
          @ValidateData
          public Result handle(ZipCodeForm inputData, ExecutionContext ctx) {

              ZipCodeData data = BeanUtil.createAndCopy(ZipCodeData.class, inputData);
              UniversalDao.insert(data);

              return new Result.Success();
          }

          /**
           * 创建读取器。
           *
           * @param ctx 运行上下文
           * @return 读取器对象
           */
          @Override
          public DataReader<ZipCodeForm> createReader(ExecutionContext ctx) {
              return new ZipCodeFileReader();
          }
      }

  实现要点：
    * 在 `handle` 方法中实现从读取器读取到的一条数据如何处理的逻辑。
    * 使用 :java:extdoc:`UniversalDao#insert <nablarch.common.dao.UniversalDao.insert(java.lang.Object)>` 将住址Entity插入到数据库中。
    * 实现 `createReader` 方法，返回数据读取器对象。

  .. tip::
    由于执行 :ref:`bean_validation` 的逻辑在各个批处理中并无差异，因此在 Example 应用中通过创建拦截器来实现验证处理的共通化。
    关于拦截器的实现，请参考 Example 应用中的 `ValidateData.java`。