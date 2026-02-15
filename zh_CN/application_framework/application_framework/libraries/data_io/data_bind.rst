.. _data_bind:

数据绑定
==================================================

.. contents:: 目录
  :depth: 3
  :local:

提供将CSV、TSV、固定长度等数据作为Java Beans对象及Map对象处理的功能。

功能概述
---------------------------------------------------------------------

可以将数据作为Java Beans对象处理
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
可以将数据文件的数据作为Java Beans对象处理。

在向Java Beans对象转换时，使用 :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` 自动转换为Java Beans类中定义的属性类型。
如果类型转换失败则会发生异常，不会生成Java Beans对象。

.. important::

  读取从外部接收的上传文件等数据时，
  对于异常数据也需要将其作为业务错误通知而不应异常终止，
  因此Java Beans类的属性必须全部定义为String类型。

将数据作为Java Beans对象处理的方法详情请参考以下内容。

* :ref:`data_bind-file_to_bean`
* :ref:`data_bind-bean_to_file`

可以将数据作为Map对象处理
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
可以将数据文件的数据作为Map对象处理。

在向Map对象转换时，所有值都以String类型存储。

详情请参考以下内容。

* :ref:`data_bind-file_to_map`
* :ref:`data_bind-map_to_file`

可以通过注解指定数据文件的格式
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
数据文件的格式不是通过配置文件来定义，
而是可以使用注解或 :java:extdoc:`DataBindConfig <nablarch.common.databind.DataBindConfig>` 来定义。

详细格式指定方法请参考以下内容。

  * :ref:`data_bind-csv_format`
  * :ref:`data_bind-fixed_length_format`

模块列表
---------------------------------------------------------------------

.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-databind</artifactId>
  </dependency>

  <!-- 仅在使用文件下载时需要 -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web-extension</artifactId>
  </dependency>

使用方法
---------------------------------------------------------------------

.. _data_bind-file_to_bean:

将数据作为Java Beans对象读取
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
可以从文件开头逐条读取数据，并以Java Beans对象形式获取。

数据读取使用通过 :java:extdoc:`ObjectMapperFactory#create <nablarch.common.databind.ObjectMapperFactory.create(java.lang.Class,java.io.InputStream)>`
生成的 :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` [#thread-unsafe]_ 进行，
基于生成 :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` 时指定的
Java Beans类中定义的注解来读取数据。

Java Beans类的注解定义方法详情请参考以下内容。

  * :ref:`将CSV文件绑定到Java Beans类时的格式指定方法 <data_bind-csv_format-beans>`
  * :ref:`将固定长度文件绑定到Java Beans类时的格式指定方法 <data_bind-fixed_length_format-beans>`

以下显示读取全部数据时的实现示例。

.. code-block:: java

  try (ObjectMapper<Person> mapper = ObjectMapperFactory.create(Person.class, inputStream)) {
      Person person;
      while ((person = mapper.read()) != null) {
          // 编写每个Java Beans对象的处理(向Java Beans对象的转换处理等)
      }
  } catch (InvalidDataFormatException e) {
      // 编写读取的数据格式异常时的处理
  }

.. important::

  全部数据读取完成后，必须通过 :java:extdoc:`ObjectMapper#close <nablarch.common.databind.ObjectMapper.close()>` 释放资源。

  使用 ``try-with-resources`` 可以省略关闭处理。

.. _data_bind-bean_to_file:

将Java Beans对象的内容写入数据文件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
可以将Java Beans对象的内容逐条写入数据文件。

向数据文件写入使用通过 :java:extdoc:`ObjectMapperFactory#create <nablarch.common.databind.ObjectMapperFactory.create(java.lang.Class,java.io.OutputStream)>`
生成的 :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>`  [#thread-unsafe]_ 进行，
基于生成 :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` 时指定的
Java Beans类中定义的注解来写入数据。

Java Beans类的注解定义方法详情请参考以下内容。

  * :ref:`将CSV文件绑定到Java Beans类时的格式指定方法 <data_bind-csv_format-beans>`
  * :ref:`将固定长度文件绑定到Java Beans类时的格式指定方法 <data_bind-fixed_length_format-beans>`

以下显示将列表中的所有Java Beans对象写入数据文件时的实现示例。

.. code-block:: java

  try (ObjectMapper<Person> mapper = ObjectMapperFactory.create(Person.class, outputStream)) {
      for (Person person : personList) {
          mapper.write(person);
      }
  }

.. tip::

  属性值为 ``null`` 时，会输出表示未输入的值。
  例如，写入CSV文件时会输出空字符串。

.. _data_bind-file_to_map:

将数据作为Map对象读取
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
可以从文件开头逐条读取数据，并以Map对象形式获取。

数据读取使用通过
:java:extdoc:`ObjectMapperFactory#create <nablarch.common.databind.ObjectMapperFactory.create(java.lang.Class,java.io.InputStream,nablarch.common.databind.DataBindConfig)>`
生成的 :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` [#thread-unsafe]_ 进行，
基于生成 :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` 时指定的
:java:extdoc:`DataBindConfig <nablarch.common.databind.DataBindConfig>` 的设置值来读取数据。

:java:extdoc:`DataBindConfig <nablarch.common.databind.DataBindConfig>` 的设置方法详情请参考以下内容。

  * :ref:`将CSV文件绑定到Map类时的格式指定方法 <data_bind-csv_format-map>`
  * :ref:`将固定长度文件绑定到Map类时的格式指定方法 <data_bind-fixed_length_format-map>`

以下显示读取CSV文件全部数据时的实现示例。

.. code-block:: java

  // 生成DataBindConfig对象
  DataBindConfig config = CsvDataBindConfig.DEFAULT.withHeaderTitles("年龄", "姓名")
                                                   .withProperties("age", "name");
  try (ObjectMapper<Map> mapper = ObjectMapperFactory.create(Map.class, inputStream, config)) {
      Person person;
      while ((person = mapper.read()) != null) {
          // 编写每个Java Beans对象的处理(向Java Beans对象的转换处理等)
      }
  } catch (InvalidDataFormatException e) {
      // 编写读取的数据格式异常时的处理
  }

.. _data_bind-map_to_file:

将Map对象的内容写入数据文件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
可以将Map对象的内容逐条写入数据文件。

向数据文件写入使用通过
:java:extdoc:`ObjectMapperFactory#create <nablarch.common.databind.ObjectMapperFactory.create(java.lang.Class,java.io.OutputStream,nablarch.common.databind.DataBindConfig)>`
生成的 :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` [#thread-unsafe]_ 进行，
基于生成 :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` 时指定的
:java:extdoc:`DataBindConfig <nablarch.common.databind.DataBindConfig>` 的设置值来写入数据。

:java:extdoc:`DataBindConfig <nablarch.common.databind.DataBindConfig>` 的设置方法详情请参考以下内容。

  * :ref:`将CSV文件绑定到Map类时的格式指定方法 <data_bind-csv_format-map>`
  * :ref:`将固定长度文件绑定到Map类时的格式指定方法 <data_bind-fixed_length_format-map>`

以下显示将列表中的所有Map对象写入CSV文件时的实现示例。

.. code-block:: java

  // 生成DataBindConfig对象
  DataBindConfig config = CsvDataBindConfig.DEFAULT.withHeaderTitles("年龄", "姓名")
                                                   .withProperties("age", "name");
  try (ObjectMapper<Map> mapper = ObjectMapperFactory.create(Map.class, outputStream, config)) {
      for (Map<String, Object> person : personList) {
          mapper.write(person);
      }
  }

.. tip::

  Map对象的value值为 ``null`` 时，会输出表示未输入的值。
  例如，写入CSV文件时会输出空字符串。
  
.. _data_bind-line_number:

获取文件数据的逻辑行号
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
将文件数据作为Java Beans对象获取时，通过在Java Beans类中定义属性并使用
:java:extdoc:`LineNumber <nablarch.common.databind.LineNumber>`，可以同时获取数据的逻辑行号。

例如，在输入值校验时用于输出生成验证错误的数据行号到日志等场景。

以下显示实现示例。

.. code-block:: java

  private Long lineNumber;

  @LineNumber
  public Long getLineNumber() {
      return lineNumber;
  }

.. tip::

  作为Map对象获取时，无法获取数据的行号，请注意这一点。


.. _data_bind-validation:

校验数据的输入值
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
由于可以将数据作为Java Beans对象读取，
因此可以使用 :ref:`bean_validation` 进行输入值校验。

以下显示实现示例。

.. code-block:: java

  try (ObjectMapper<Person> mapper = ObjectMapperFactory.create(Person.class, inputStream)) {
      Person person;
      while ((person = mapper.read()) != null) {
          // 执行输入值校验
          ValidatorUtil.validate(person);

          // 后续处理省略
      }
  } catch (InvalidDataFormatException e) {
      // 编写数据文件格式异常时的处理
  }

.. _data_bind-file_download:

在文件下载中使用
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
以下显示在Web应用中，将Java Beans对象的内容作为数据文件下载的实现示例。

要点
  * 将数据展开到内存上可能会在下载大量数据时造成内存压力，因此输出到临时文件。
  * 向数据文件写入的详细内容请参考 :ref:`data_bind-bean_to_file` 。
  * 在生成 :java:extdoc:`FileResponse <nablarch.common.web.download.FileResponse>` 对象时指定数据文件。
  * 要在请求处理结束时自动删除文件，请在 `FileResponse` 构造函数的第二个参数中指定 ``true`` 。
  * 在响应中设置 `Content-Type` 及 `Content-Disposition` 。

.. code-block:: java

  public HttpResponse download(HttpRequest request, ExecutionContext context) {

      // 业务处理

      final Path path = Files.createTempFile(null, null);
      try (ObjectMapper<Person> mapper =
              ObjectMapperFactory.create(Person.class, Files.newOutputStream(path))) {
          for (Person person : persons) {
              mapper.write(BeanUtil.createAndCopy(PersonDto.class, person));
          }
      }

      // 将文件设置到body中。
      FileResponse response = new FileResponse(path.toFile(), true);

      // 设置Content-Type头部、Content-Disposition头部
      response.setContentType("text/csv; charset=Shift_JIS");
      response.setContentDisposition("person.csv");

      return response;
  }

.. _data_bind-upload_file:

读取上传文件的数据
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
以下显示在Web应用中，将画面上传的文件数据作为Java Beans对象读取的实现示例。

要点
 * 使用 :java:extdoc:`PartInfo#getInputStream <nablarch.fw.web.upload.PartInfo.getInputStream()>` 获取上传文件的流。
 * 由于可能输入了异常数据，因此使用 :ref:`bean_validation` 进行输入校验。

.. code-block:: java

  List<PartInfo> partInfoList = request.getPart("uploadFile");
  if (partInfoList.isEmpty()) {
      // 编写未找到上传文件时的处理
  }

  PartInfo partInfo = partInfoList.get(0);
  try (ObjectMapper<Person> mapper = ObjectMapperFactory.create(Person.class, partInfo.getInputStream())) {
      Person person;
      while ((person = mapper.read()) != null) {
          // 执行输入值校验
          ValidatorUtil.validate(person);

          // 后续处理省略
      }
  } catch (InvalidDataFormatException e) {
      // 编写数据文件格式异常时的处理
  }

.. _data_bind-csv_format:

指定CSV文件的格式
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CSV文件的格式指定，在绑定到Java Beans类和绑定到Map类时有两种不同的指定方法。

.. _data_bind-csv_format-beans:

绑定到Java Beans类时
  使用以下注解指定格式。

  * :java:extdoc:`Csv <nablarch.common.databind.csv.Csv>`
  * :java:extdoc:`CsvFormat <nablarch.common.databind.csv.CsvFormat>`

  可以从预先准备好的格式集中选择CSV文件的格式。
  关于格式集的详细内容请参考 :ref:`data_bind-csv_format_set` 。

  以下显示实现示例。

  .. code-block:: java

    @Csv(type = Csv.CsvType.DEFAULT, properties = {"age", "name"}, headers = {"年龄", "姓名"})
    public class Person {
        private Integer age;
        private String name;

        // getter、setter省略。
    }

  此外，如果CSV文件的格式不符合预先准备的任何格式集，
  可以使用 :java:extdoc:`CsvFormat <nablarch.common.databind.csv.CsvFormat>` 单独指定格式。

  以下显示实现示例。

  .. code-block:: java

    // type属性指定为CUSTOM。
    @Csv(type = Csv.CsvType.CUSTOM, properties = {"age", "name"})
    @CsvFormat(
            fieldSeparator = '\t',
            lineSeparator = "\r\n",
            quote = '\'',
            ignoreEmptyLine = false,
            requiredHeader = false,
            charset = "UTF-8",
            quoteMode = CsvDataBindConfig.QuoteMode.ALL,
            emptyToNull = true)
    public class Person {
        private Integer age;
        private String name;

        // getter、setter省略。
    }

  .. tip::

    绑定到Java Beans类时，由于格式指定是通过注解进行的，
    因此在生成 :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` 时
    不能使用 :java:extdoc:`DataBindConfig <nablarch.common.databind.DataBindConfig>` 指定格式。

.. _data_bind-csv_format-map:

绑定到Map类时
  在生成 :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` 时
  使用 :java:extdoc:`CsvDataBindConfig <nablarch.common.databind.csv.CsvDataBindConfig>` 单独指定格式。

  此外，指定格式时，
  通过 :java:extdoc:`CsvDataBindConfig#withProperties <nablarch.common.databind.csv.CsvDataBindConfig.withProperties(java.lang.String...)>`
  设置的属性名将作为Map对象的键使用。
  如果CSV存在标题行，可以省略属性名设置，使用标题作为键。

  以下显示实现示例。

  要点
    * 标题、属性名要与CSV的项目顺序一致定义

  .. code-block:: java

    // 标题、属性名要与CSV的项目顺序一致定义
    DataBindConfig config = CsvDataBindConfig.DEFAULT.withHeaderTitles("年龄", "姓名")
                                                     .withProperties("age", "name");
    ObjectMapper<Map> mapper = ObjectMapperFactory.create(Map.class, outputStream, config);

.. _data_bind-fixed_length_format:

指定固定长度文件的格式
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
固定长度文件的格式指定，在绑定到Java Beans类和绑定到Map类时有两种不同的指定方法。

.. _data_bind-fixed_length_format-beans:

绑定到Java Beans类时
  使用以下注解指定格式。

  * :java:extdoc:`FixedLength <nablarch.common.databind.fixedlength.FixedLength>`
  * :java:extdoc:`Field <nablarch.common.databind.fixedlength.Field>`

  此外，可以为固定长度文件的各字段指定用于执行填充、修剪等转换的转换器。
  标准可指定的转换器请参考 :java:extdoc:`nablarch.common.databind.fixedlength.converter` 包下的内容。

  以下显示实现示例。

  .. code-block:: java

    @FixedLength(length = 19, charset = "MS932", lineSeparator = "\r\n")
    public class Person {

        @Field(offset = 1, length = 3)
        @Lpad
        private Integer age;

        @Field(offset = 4, length = 16)
        @Rpad
        private String name;

        // getter、setter省略
    }

  如果存在如下所示的未使用区域，
  在向固定长度文件写入时会自动使用 ``FixedLength#fillChar`` 设置的字符进行填充。(默认为半角空格)

  .. code-block:: java

    @FixedLength(length = 24, charset = "MS932", lineSeparator = "\r\n", fillChar = '0')
    public class Person {

        @Field(offset = 1, length = 3)
        @Lpad
        private Integer age;

        @Field(offset = 9, length = 16)
        @Rpad
        private String name;

        // getter、setter省略
    }

.. _data_bind-fixed_length_format-map:

绑定到Map类时
  在生成 :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` 时
  使用 :java:extdoc:`FixedLengthDataBindConfig <nablarch.common.databind.fixedlength.FixedLengthDataBindConfig>` 单独指定格式。

  :java:extdoc:`FixedLengthDataBindConfig <nablarch.common.databind.fixedlength.FixedLengthDataBindConfig>` 可以使用
  :java:extdoc:`FixedLengthDataBindConfigBuilder <nablarch.common.databind.fixedlength.FixedLengthDataBindConfigBuilder>` 生成。

  以下显示实现示例。

  .. code-block:: java

    final DataBindConfig config = FixedLengthDataBindConfigBuilder
            .newBuilder()
            .length(19)
            .charset(Charset.forName("MS932"))
            .lineSeparator("\r\n")
            .singleLayout()
            .field("age", 1, 3, new Lpad.Converter('0'))
            .field("name", 4, 16, new Rpad.RpadConverter(' '))
            .build();

    final ObjectMapper<Map> mapper = ObjectMapperFactory.create(Map.class, outputStream, config);

.. _data_bind-fixed_length_format-multi_layout:

为固定长度文件指定多种格式
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
对于具有多种格式的固定长度文件的格式指定，
也有绑定到Java Beans类和绑定到Map类两种指定方法。

绑定到Java Beans类时
  通过为每种格式定义JavaBeans类，并创建以这些Java Beans类为属性的
  :java:extdoc:`MultiLayout <nablarch.common.databind.fixedlength.MultiLayout>` 继承类，
  可以对应多种格式的固定长度文件。

  以下显示格式指定的实现示例。

  要点
    * 为每种格式定义Java Beans类。
    * 定义以这些格式定义的Java Beans类为属性的
      :java:extdoc:`MultiLayout <nablarch.common.databind.fixedlength.MultiLayout>` 继承类。
    * 在 :java:extdoc:`MultiLayout <nablarch.common.databind.fixedlength.MultiLayout>` 继承类上设置
      :java:extdoc:`FixedLength <nablarch.common.databind.fixedlength.FixedLength>` 注解， ``multiLayout`` 属性设置为 ``true`` 。
    * 覆盖 :java:extdoc:`MultiLayout#getRecordIdentifier <nablarch.common.databind.fixedlength.MultiLayout.getRecordIdentifier()>` 方法，
      返回用于识别目标数据与哪种格式关联的 :java:extdoc:`RecordIdentifier <nablarch.common.databind.fixedlength.MultiLayoutConfig.RecordIdentifier>` 实现类。

  .. code-block:: java

    @FixedLength(length = 20, charset = "MS932", lineSeparator = "\r\n", multiLayout = true)
    public class Person extends MultiLayout {

        @Record
        private Header header;

        @Record
        private Data data;

        @Override
        public RecordIdentifier getRecordIdentifier() {
            return new RecordIdentifier() {
                @Override
                public RecordName identifyRecordName(byte[] record) {
                    return record[0] == 0x31 ? RecordType.HEADER : RecordType.DATA;
                }
            };
        }

        // getter、setter省略
    }

    public class Header {

        @Field(offset = 1, length = 1)
        private Long id;

        @Rpad
        @Field(offset = 2, length = 19)
        private String field;

        // getter、setter省略
    }

    public class Data {

        @Field(offset = 1, length = 1)
        private Long id;

        @Lpad
        @Field(offset = 2, length = 3)
        private Long age;

        @Rpad
        @Field(offset = 5, length = 16)
        private String name;

        // getter、setter省略
    }

    enum RecordType implements MultiLayoutConfig.RecordName {
        HEADER {
            @Override
            public String getRecordName() {
                return "header";
            }
        },
        DATA {
            @Override
            public String getRecordName() {
                return "data";
            }
        }
    }

  接下来，显示基于指定格式读取和写入固定长度数据的实现示例。

  .. code-block:: java

    // 读取时的实现示例
    try (ObjectMapper<Person> mapper = ObjectMapperFactory.create(Person.class, inputStream)) {
        final Person person = mapper.read();
        if (RecordType.HEADER == person.getRecordName()) {
            final Header header = person.getHeader();

            // 后续处理省略
        }
    }

    // 写入时的实现示例
    try (ObjectMapper<Person> mapper = ObjectMapperFactory.create(Person.class, outputStream)) {
        final Person person = new Person();
        person.setHeader(new Header("1", "test"));
        mapper.write(person);
    }


绑定到Map类时
  可以按照与 :ref:`绑定Map类时的固定长度文件格式指定方法 <data_bind-fixed_length_format-map>`
  相同的步骤指定格式。

  以下显示格式指定的实现示例。

  要点
    * 调用 ``multiLayout`` 方法，生成多布局用DataBindConfig。
    * ``recordIdentifier`` 方法中指定用于识别目标数据与哪种格式关联的
      :java:extdoc:`RecordIdentifier <nablarch.common.databind.fixedlength.MultiLayoutConfig.RecordIdentifier>` 实现类。

  .. code-block:: java

    final DataBindConfig config = FixedLengthDataBindConfigBuilder
            .newBuilder()
            .length(20)
            .charset(Charset.forName("MS932"))
            .lineSeparator("\r\n")
            .multiLayout()
            .record("header")
            .field("id", 1, 1, new DefaultConverter())
            .field("field", 2, 19, new Rpad.RpadConverter(' '))
            .record("data")
            .field("id", 1, 1, new DefaultConverter())
            .field("age", 2, 3, new Lpad.LpadConverter('0'))
            .field("name", 5, 16, new Rpad.RpadConverter(' '))
            .recordIdentifier(new RecordIdentifier() {
                @Override
                public RecordName identifyRecordName(byte[] record) {
                    return record[0] == 0x31 ? RecordType.HEADER : RecordType.DATA;
                }
            })
            .build();

  接下来，显示基于指定格式读取和写入固定长度数据的实现示例。

  .. code-block:: java

    // 读取时的实现示例
    try (ObjectMapper<Map> mapper = ObjectMapperFactory.create(Map.class, inputStream, config)) {
        final Map<String, ?> map = mapper.read();
        if (RecordType.HEADER == map.get("recordName")) {
            final Map<String, ?> header = map.get("header");

            // 后续处理省略
        }
    }

    // 写入时的实现示例
    try (ObjectMapper<Map> mapper = ObjectMapperFactory.create(Map.class, outputStream, config)) {
        final Map<String, ?> header = new HashMap<>();
        header.put("id", "1");
        header.put("field", "test");

        final Map<String, ?> map = new HashMap<>();
        map.put("recordName", RecordType.HEADER);
        map.put("header", header);

        mapper.write(map);
    }

.. _data_bind-formatter:

格式化输出数据的显示形式
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
输出数据时，可以使用 :ref:`format` 来格式化日期和数值等数据的显示形式。

详情请参考 :ref:`format` 。

扩展示例
---------------------------------------------------------------------

添加可以绑定到Java Beans类的文件格式
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
要添加可以绑定到Java Beans类的文件格式，需要以下步骤。

1. 创建用于将指定格式的文件与Java Beans类绑定的 :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` 实现类。
2. 创建继承 :java:extdoc:`ObjectMapperFactory <nablarch.common.databind.ObjectMapperFactory>` 的类，
   添加生成刚才创建的 :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` 实现类的处理。
3. 将继承 :java:extdoc:`ObjectMapperFactory <nablarch.common.databind.ObjectMapperFactory>` 的类设置到组件配置文件中。
   以下显示组件配置文件中的设置示例。


  要点
   * 组件名称必须是 **objectMapperFactory** 。

  .. code-block:: xml

    <component name="objectMapperFactory" class="sample.SampleObjectMapperFactory" />

.. _data_bind-csv_format_set:

可作为CSV文件格式指定的格式集
---------------------------------------------------------------------
默认提供的CSV文件格式集及设置值如下。

================== ================= ================= ================= =================
\                  DEFAULT           RFC4180           EXCEL             TSV
================== ================= ================= ================= =================
列分隔符           逗号(,)           逗号(,)           逗号(,)           制表符(\\t)
行分隔符           换行(\\r\\n)      换行(\\r\\n)      换行(\\r\\n)      换行(\\r\\n)
字段包围字符       双引号(")         双引号(")         双引号(")         双引号(")
忽略空行           true              false             false             false
有标题行           true              false             false             false
字符编码           UTF-8             UTF-8             UTF-8             UTF-8
引用模式           NORMAL            NORMAL            NORMAL            NORMAL
================== ================= ================= ================= =================

引用模式
  引用模式是指示在写入CSV文件时哪些字段用字段包围字符包围的模式。
  引用模式可以从以下模式中选择。

  ================ ================================================================
  引用模式名       用字段包围字符包围的目标字段
  ================ ================================================================
  NORMAL           包含字段包围字符、列分隔字符、换行之一的字段
  ALL              所有字段
  ================ ================================================================

  .. tip::

    读取CSV文件时，不使用引用模式，自动判断字段包围字符的有无并进行读取。
    
    
.. [#thread-unsafe]

  :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` 的读取和写入是线程不安全的，如果被多个线程同时调用，不保证其动作。
  因此，如果在多个线程间共享 :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` 的实例，需要在调用方进行同步处理。
  
