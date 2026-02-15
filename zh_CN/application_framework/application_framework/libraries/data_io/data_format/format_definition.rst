.. _`data_format-definition`:

格式定义文件的描述规则
==================================================

.. contents:: 目录
  :depth: 3
  :local:

.. |br| raw:: html

    <br/>

格式定义文件的共同记法
--------------------------------------------------
说明格式定义文件的共同描述规则。

字符编码
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
格式定义文件的字符编码为 ``UTF-8`` 。


字面量表示
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
在设置值中记述字面量时，请遵循以下规则。


.. list-table::
  :class: white-space-normal
  :header-rows: 1
  :widths: 30 70

  * - 字面量类型
    - 说明
  * - 字符串
    - 与Java的字符字面量一样用 ``"`` 包围值记述。

      不支持Unicode转义和八进制转义。
      
      记述例
       | "Nablarch"
       | "\\r\\n"

  * - 10进制整数
    - 与Java的数值字面量一样记述。

      不支持小数。

      记述例
        | 123
        | -123

  * - 布尔值
    - 以 ``true`` 或 ``false`` 设置。(大写也可)

注释
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
行中 ``#`` 以后的部分作为注释处理。

以下显示示例。

.. code-block:: bash

  #
  # 示例文件
  # 
  file-type:     "Fixed"  # 固定长度
  text-encoding: "ms932"  # 字符代码是ms932
  record-length:  120     # 各行长度是120字节




格式定义文件的结构
--------------------------------------------------

格式定义文件主要由以下两个要素构成。

:指令声明部:
  定义使用的数据形式(固定长度、JSON等)和编码等共同设置。

  详细请参考 :ref:`data_format-definition_directive` 。

:记录格式定义部:
  定义记录的内容。

  具体定义记录内的字段定义以及各字段的数据类型和数据转换规则。

  详细请参考 :ref:`data_format-definition_record` 。

.. _data_format-definition_directive:

指令声明部的定义
--------------------------------------------------

共同可用的指令一览
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
所有数据形式使用的指令定义如下。

.. list-table::
  :class: white-space-normal
  :widths: 30 70
  :header-rows: 1

  * - 指令
    - 说明
  * - file-type ``必填``
    - 指定数据形式。 

      标准可以指定以下数据形式。

      * Fixed(固定长度)
      * Variable(CSV或TSV等可变长度)
      * JSON
      * XML

  * - text-encoding ``必填``
    - .. _data_format-directive_text_encoding:

      指定字符串字段读写时使用的编码。

      只能指定使用的JVM支持的字符编码。例如， ``UTF-8`` 、 ``SJIS`` 等。

      `file-type` 指定为JSON时，只能指定以下编码

      * UTF-8
      * UTF-16(BE or LE)
      * UTF-32(BE or LE)

      `file-type` 指定为XML时，本设置值会被XML声明部指定的编码优先。

  * - record-separator ``可选``
    - 指定记录终止字符(换行字符)。

      `file-type` 指定为Variable(可变长度)时，为 ``必填`` 。

      `file-type` 为JSON或XML时，不使用本设置值。

Fixed(固定长度)形式可指定的指令一览
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Fixed(固定长度)形式的数据使用的指令如下。

.. list-table::
  :class: white-space-normal
  :widths: 30 70
  :header-rows: 1

  * - 指令
    - 说明
  * -  record-length ``必填``
    - 指定1条记录的字节长度。

  * - positive-zone-sign-nibble ``可选``
    - .. _data_format-positive_zone_sign_nibble:

      以16进制表示的字符串指定带符号区域数值的区域部设置的正符号。

      默认根据 :ref:`text-encoding <data_format-directive_text_encoding>` 的值使用以下值。

      :ASCII兼容: 0x3      
      :EBCDIC兼容: 0xC

  * - negative-zone-sign-nibble ``可选``
    - .. _data_format-negative_zone_sign_nibble:

      以16进制表示的字符串指定带符号区域数值的区域部设置的负符号。

      默认根据 :ref:`text-encoding <data_format-directive_text_encoding>` 的值使用以下值。

      :ASCII兼容: 0x7      
      :EBCDIC兼容: 0xD

  * - positive-pack-sign-nibble ``可选``
    - .. _data_format-positive_pack_sign_nibble:
      
      以16进制表示的字符串指定带符号压缩数值的符号位设置的正符号。

      默认根据 :ref:`text-encoding <data_format-directive_text_encoding>` 的值使用以下值。

      :ASCII兼容: 0x3      
      :EBCDIC兼容: 0xC
  
  * - negative-pack-sign-nibble ``可选``
    - .. _data_format-negative_pack_sign_nibble:
      
      以16进制表示的字符串指定带符号压缩数值的符号位设置的负符号。

      默认根据 :ref:`text-encoding <data_format-directive_text_encoding>` 的值使用以下值。

      :ASCII兼容: 0x7      
      :EBCDIC兼容: 0xD

  * - required-decimal-point ``可选``
    - 指定无符号数值及带符号数值的小数点是否需要。

      指定 ``true`` 时写入的数据会附加小数点。

      指定 ``false`` 时，写入的数据不附加小数点。(成为固定小数点)

      默认动作是附加小数点( ``true`` )。

  * - fixed-sign-position ``可选``
    - 指定带符号数值的符号位置是否固定。

      符号位置固定( ``true`` )时，符号位置固定在项目的开头。
      符号位置不固定( ``false`` )时，符号位置附加在填充前数值的开头。

      默认动作是固定( ``true`` )。

      例
        :符号位置固定: -000123456
        :符号位置不固定: 000-123456

  
  * - required-plus-sign ``可选``
    - 指定带符号数值的正符号是否需要。

      指定 ``true`` 时，读取的数据需要有正符号( ``+`` )，
      写入的数据会附加正符号( ``+`` )。

      默认动作是不附加( ``false`` )。



以下显示示例。

.. code-block:: bash

  #
  # 指令定义部
  #
  file-type:                      "Fixed"  # 固定长度文件
  text-encoding:                  "ms932"  # 字符串型字段的字符编码
  record-length:                  120      # 各记录byte长度 
  positive-zone-sign-nibble:      "C"      # 区域数值的正符号
  negative-zone-sign-nibble:      "D"      # 区域数值的负符号
  positive-pack-sign-nibble:      "C"      # 压缩数值的正符号
  negative-pack-sign-nibbleL      "D"      # 压缩数值的负符号
  required-decimal-point:         true     # 有小数点
  fixed-sign-position:            true     # 符号在开头
  required-plus-sign:             false    # 不附加正符号

.. _data_format-variable_data_directive:

Variable(可变长度)形式可指定的指令一览
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Variable(可变长度)形式的数据使用的指令如下。

.. list-table::
  :class: white-space-normal
  :widths: 30 70
  :header-rows: 1

  * - 指令
    - 说明
  * - field-separator ``必填``
    - 指定字段(项目)的分隔字符。

      例如，CSV则指定 ``,`` ，TSV则指定 ``\t`` 。

  * - quoting-delimiter ``可选``
    - 指定对字段(项目)值进行引号包围时使用的字符。

      例如，设置双引号时指定 ``"`` ，
      设置单引号时指定 ``'`` 。

      输出时，设置了值时所有字段(项目)都会被引号包围。
      默认不进行引号包围。
      
      输入时，设置了值时字段前后的引号字符会被去除。
      换行和字段内的引号字符处理等请参考RFC4180。

  * - ignore-blank-lines ``可选``
    - 设置数据读取时是否忽略空行。

      设置 ``true`` 时，空行(仅换行)的记录会被忽略。

      默认忽略空行。

  * - requires-title ``可选``
    - .. _data_format-requires-title:
      
      设置是否将第一条记录作为标题读写。

      设置 ``true`` 时，将第一条记录作为标题处理。

      默认不将第一条记录作为标题处理。

      标题记录的布局定义请参考 :ref:`title-record-type-name指令 <data_format-title_type_name>` 。

  * - title-record-type-name ``可选``
    - .. _data_format-title_type_name:
      
      设置标题的记录类型名。

      未指定时，标题的记录类型名为 ``Title`` 。

      按照本指令指定的记录类型名关联的记录格式定义编辑标题记录。

      使用标题记录类型名的格式定义文件示例请参考
      :ref:`标题记录的格式定义示例 <data_format-variable_title_sample>` 。

      记录类型和记录定义的详细内容请参考 :ref:`data_format-definition_record` 。

  * - max-record-length ``可选``
    - 指定允许读取的1条记录的字符数。

      读取记录分隔字符不存在的数据(损坏的数据)时，
      如果将记录全部展开到堆上可能会因堆不足导致进程异常终止。

      因此，如果读取到本指令设置值的字符数仍未发现记录分隔字符，
      则作为异常数据中止读取处理并抛出异常。

      默认为1,000,000字符。

以下显示示例。

.. code-block:: bash

  #
  # 指令定义部
  #
  file-type:                  "Variable"  # 可变长度文件
  text-encoding:              "utf-8"     # 字符串型字段的字符编码
  record-separator:           "\\r\\n"    # 换行

  field-separator:            ","         # CSV
  quoting-delimiter:          "\""        # 用双引号包围项目
  ignore-blank-lines:         true        # 忽略空行
  requires-title:             false       # 无标题记录
  max-record-length:          1000        # 此csv的记录最多1000字符

JSON形式可指定的指令一览
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
JSON数据形式固有的指令不存在。

以下显示示例。

.. code-block:: bash

  file-type:      "JSON"      # json格式
  text-encoding:  "utf-8"     # 字符串型字段的字符编码


XML形式可指定的指令一览
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
XML数据形式固有的指令不存在。

以下显示示例。

.. code-block:: bash

  file-type:      "XML"       # xml格式
  text-encoding:  "utf-8"     # 字符串型字段的字符编码

.. _data_format-definition_record:

记录格式定义部
--------------------------------------------------
在记录格式定义部中，设置构成记录的字段(项目)的定义信息(记录内的位置和数据类型等)。

记录格式定义示例如下。

要点
  * 为识别记录，用 ``[`` 、 ``]`` 包围定义记录类型名。
  * 记录类型名在格式定义文件内必须唯一。
  * 记录类型名定义任意值。
  * 从记录类型名的下一行开始，定义记录内的字段(项目)。
  * 字段(项目)定义重复定义字段数次。
  * 字段定义的书写格式请参考 :ref:`字段定义的书写格式 <data_format-field_definition>` 。

.. code-block:: bash

  [data]              # 记录类型名:data
  1 name  N(100)      # 姓名
  2 age   X9(3)       # 年龄

.. important::

  JSON和XML数据形式定义字段时，同一字段名不能混用字段类型为 ``OB`` 和非 ``OB`` 的。

  混用时，OB的定义会优先，非OB的字段类型指定会被忽略。

  结果，本不是OB的字段在读写时会作为OB型处理。
  因此，会发生数据与格式项目定义不匹配，数据无法正确读写的问题。

  不适当的示例
    .. code-block:: bash

      [order]
      1 id     N
      2 data   OB  # 字段类型:OB
      3 detail OB

      [data]
      1 value  N

      [detail]
      1 data   N   # 字段类型:N  ← 不适当的记述：会作为指定字段类型为OB处理

.. _data_format-field_definition:

字段定义
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
字段定义以以下形式定义。

.. code-block:: text
  
  <字段开始位置> <字段名> <多重性> <字段类型> <字段转换器>

字段定义各要素的详细内容如下。

.. list-table::
  :class: white-space-normal
  :widths: 30 70

  * - 字段开始位置 ``必填``
    - 各数据形式按照以下规则定义字段开始位置。

      :Fixed(固定长度): 设置字段的开始字节数(从1开始)。
      :Variable(可变长度): 设置字段的项目序号。
      :JSON: 设置字段的元素序号
      :XML: 设置字段的元素序号

  * - 字段名 ``必填``
    - 设置用于识别字段的名称。

      字段名是本功能输入输出使用的 :java:extdoc:`java.util.Map` 的键。

      字段名开头附加 ``?`` 时，该项目在输入时不会读取到 :java:extdoc:`java.util.Map` 中。
      例如，可用于主机中常用的固定长度文件的filler项目，排除不需要的输入对象项目。

      .. important::

        注意数字-only的字段名无法定义。

      XML数据形式时，字段名开头附加 ``@`` 可以将该项目作为属性值处理。

      以下显示示例。
      
      .. code-block:: bash

        [tagName]
        @attr

      上述对应的XML如下。

      .. code-block:: xml

        <tagName attr="val">
        ...
        </tagName>

  * - 多重性 ``可选``
    - 指定字段的可定义数。

      此值只能在JSON和XML数据形式时指定。

      记述规则如下。
        * 可定义数用 ``[`` 、 ``]`` 包围记述。
        * 有下限和上限时，在下限和上限之间记述 ``..`` 。
        * 没有上限时记述 ``*`` 。
        * 省略时为 ``[1]`` 。

      以下显示指定示例。

      .. code-block:: bash

        address [1..3]    # 可定义1到3个
        address           # 省略所以只能是1个
        address [0..*]    # 无条件(0到无限制)
        address [*]       # 无条件(0到无限制)
        address [1..*]    # 1个以上

      以下xml时， ``address`` 字段的可定义数为 ``2`` 。

      .. code-block:: xml

        <person>
          <address>家庭地址</address>
          <address>工作地址</address>
        </person>

      以下JSON时， ``address`` 字段的元素数为 ``3`` 。

      .. code-block:: json

        {
          "address" : ["家庭地址", "工作地址", "寄送地址"]
        }
      

  * - 字段类型 ``必填``
    - 定义字段的数据类型。

      默认可指定的字段类型请参考 :ref:`data_format-field_type_list` 。

  * - 字段转换器 ``可选``
    - 定义对字段类型的选项指定和数据转换等输入输出的预处理内容。

      默认可指定的字段类型请参考 :ref:`data_format-field_convertor_list` 。

      字段转换器也可以设置多个。


.. _data_format-multi_layout_data:

定义多格式形式的记录
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
多格式形式的数据时，在格式定义文件上定义多个记录格式。

输入输出数据属于哪个记录格式，根据特定字段的值自动判定。
如果输入输出目标数据与任何记录类型都不匹配，则作为异常数据异常终止处理。

以下显示多格式形式的格式定义示例。

要点
  * 定义记录识别字段。记录类型名设为 ``Classifier`` 。
  * 各记录定义的记录类型名正下方，定义用于判断记录的条件。
  * 记录识别(Classifier)中定义的字段必须存在于记录定义内。

.. code-block:: bash

  file-type:        "Fixed" # 固定长度
  text-encoding:    "MS932" # 字符串型字段的字符编码
  record-length:    40      # 各记录的长度
  record-separator: "\r\n"  # 换行代码(crlf)

  # 记录识别条件的定义
  [Classifier]
  1 dataKbn X(1)      # 使用开头1字节字段判定是哪个记录

  # 头部记录的定义
  [header]
  dataKbn = "1"         # dataKbn为"1"时是头部记录
  1 dataKbn X(1)
  2 data    X(39)

  # 数据记录的定义
  [data]
  dataKbn = "2"        # dataKbn为"2"时是数据记录
  1 dataKbn X(1)
  2 data    X(39)

多格式的定义示例请参考以下链接。

.. toctree::
  :maxdepth: 1

  multi_format_example

.. tip::

  JSON和XML数据形式中不存在记录概念，
  因此不支持多格式形式的格式定义。

.. _data_format-field_type_list:

字段类型一览
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
标准提供的数据类型定义一览如下。

Fixed(固定长度)数据形式可用的字段类型一览
  .. list-table::
    :class: white-space-normal
    :header-rows: 1
    :widths: 13 15 72

    * - 类型
      - Java型
      - 说明

    * - .. _data_format-field_type-single_byte_character_string:

        X
      - String
      - 单字节字符串(字节长度 = 字符串长度)

        默认进行半角空白右修剪及填充。

        :参数: 字节长度(数值) ``必填``

        输出目标值为 ``null`` 时，将值转换为空字符串后处理。

        读取值为空字符串时转换为 ``null`` 。
        不想将空字符串转换为 ``null`` 时，
        在 :java:extdoc:`convertEmptyToNull <nablarch.core.dataformat.convertor.FixedLengthConvertorSetting.setConvertEmptyToNull(boolean)>` 中设置 ``false`` 。

    * - N
      - String
      - 双字节字符串 (字节长度 = 字符数 ÷ 2)

        默认进行全角空白右修剪和填充。

        :参数: 字节长度(数值) ``必填``

        字节长度不是2的倍数时会语法错误。

        输出目标值为 ``null`` 时或读取值为空字符串时的处理方式与
        :ref:`单字节字符串的字段类型 <data_format-field_type-single_byte_character_string>` 相同。

    * - XN
      - String
      - 多字节字符串

        处理UTF-8等字节长度不同的字符混在一起的字段时指定此字段类型。

        另外，全角字符串(双字节字符串)的填充使用半角空格时也使用本字段类型。

        默认进行半角空白右修剪和填充。

        :参数: 字节长度(数值) ``必填``

        输出目标值为 ``null`` 时或读取值为空字符串时的处理方式与
        :ref:`单字节字符串的字段类型 <data_format-field_type-single_byte_character_string>` 相同。

    * - .. _data_format-field_type-zoned_decimal:

        Z
      - BigDecimal
      - 区域数值(字节长度 = 位数)

        默认进行 ``0`` 左修剪和填充。

        :参数1: 字节长度(数值) ``必填``
        :参数2: 小数点以下位数(数值) ``可选`` 默认: ``0``

        输出目标值为 ``null`` 时，将值转换为 ``0`` 后处理。

        读取值的字节数为 ``0`` 时转换为 ``null`` 。
        字节数为 ``0`` 时不想转换为 ``null`` 时，
        在 :java:extdoc:`convertEmptyToNull <nablarch.core.dataformat.convertor.FixedLengthConvertorSetting.setConvertEmptyToNull(boolean)>` 中设置 ``false`` 。

    * - SZ
      - BigDecimal
      - 带符号区域数值 (字节长度 = 位数)

        默认进行 ``0`` 左修剪和填充。

        :参数1: 字节长度(数值) ``必填``
        :参数2: 小数点以下位数(数值) ``可选`` 默认: ``0``
        :参数3: 区域部设置的正符号(16进制表示的字符串) ``可选``
        :参数4: 区域部设置的负符号(16进制表示的字符串) ``可选``

        参数3和参数4在覆盖 :ref:`带符号区域数值的正符号 <data_format-positive_zone_sign_nibble>` 及
        :ref:`带符号区域数值的负符号 <data_format-negative_zone_sign_nibble>` 时设置。

        输出目标值为 ``null`` 时或读取值的字节数为 ``0`` 时的处理方式与
        :ref:`区域数值的字段类型 <data_format-field_type-zoned_decimal>` 相同。

    * - P
      - BigDecimal
      - 压缩数值 (字节长度 = 位数 ÷ 2 [小数点进位])

        默认进行 ``0`` 左修剪和填充。

        :参数1: 字节长度(数值) ``必填``
        :参数2: 小数点以下位数(数值) ``可选`` 默认: ``0``

        输出目标值为 ``null`` 时或读取值的字节数为 ``0`` 时的处理方式与
        :ref:`区域数值的字段类型 <data_format-field_type-zoned_decimal>` 相同。

    * - SP
      - BigDecimal
      - 带符号压缩数值 (字节长度 = (位数 + 1) ÷ 2 [小数点进位])

        默认进行 ``0`` 左修剪和填充。

        :参数1: 字节长度(数值) ``必填``
        :参数2: 小数点以下位数(数值) ``可选`` 默认: ``0``
        :参数3: 符号位设置的正符号 (16进制表示的字符串) ``可选``
        :参数4: 符号位设置的负符号 (16进制表示的字符串) ``可选``

        参数3和参数4在覆盖 :ref:`带符号压缩数值的正符号 <data_format-positive_pack_sign_nibble>` 及
        :ref:`带符号压缩数值的负符号 <data_format-negative_pack_sign_nibble>` 时设置。

        输出目标值为 ``null`` 时或读取值的字节数为 ``0`` 时的处理方式与
        :ref:`区域数值的字段类型 <data_format-field_type-zoned_decimal>` 相同。

    * - B
      - byte[]
      - 二进制列

        不进行填充和修剪。

        :参数: 字节长度(数值) ``必填``

        输出目标值为 ``null`` 时的转换规格因应用而异。
        因此，本字段类型即使在这种情况下也不进行值转换，
        抛出 :java:extdoc:`InvalidDataFormatException <nablarch.core.dataformat.InvalidDataFormatException>` 。

        使用本字段类型时，请根据需求在应用侧显式设置值。

    * - X9
      - BigDecimal
      - 无符号数字符串 (字节长度 = 字符数)

        将字段中的单字节字符串(X)作为数值处理。

        默认进行 ``0`` 左修剪和填充。
        字符串中可以包含小数点符号( ``.`` )。

        :参数1: 字节长度(数值) ``必填``
        :参数2: 固定小数点时的小数点以下位数(数值) ``可选`` 默认: ``0``

        输出目标值为 ``null`` 时的处理方式与
        :ref:`区域数值的字段类型 <data_format-field_type-zoned_decimal>` 相同。

        读取值为空字符串时的处理方式与
        :ref:`单字节字符串的字段类型 <data_format-field_type-single_byte_character_string>` 相同。


    * - SX9
      - BigDecimal
      - 带符号数字符串 (字节长度 = 字符数)

        将字段中的单字节字符串(X)作为带符号数值处理。
        默认进行 ``0`` 左修剪和填充。

        :参数1: 字节长度(数值) ``必填``
        :参数2: 固定小数点时的小数点以下位数(数值) ``可选`` 默认: ``0``

        输出目标值为 ``null`` 时的处理方式与
        :ref:`区域数值的字段类型 <data_format-field_type-zoned_decimal>` 相同。

        读取值为空字符串时的处理方式与
        :ref:`单字节字符串的字段类型 <data_format-field_type-single_byte_character_string>` 相同。

        想更改符号字符(``+`` 、``-``)时，请参考以下类的实现创建项目固有的字段类型来对应。

        * :java:extdoc:`SignedNumberStringDecimal <nablarch.core.dataformat.convertor.datatype.SignedNumberStringDecimal>`

        关于添加字段类型，请参考 :ref:`data_format-field_type_add` 。

Variable(可变长度)数据形式可用的字段类型一览
  .. list-table::
    :class: white-space-normal
    :header-rows: 1
    :widths: 13 15 72

    * - 类型
      - Java型
      - 说明

    * - X |br|
        N |br|
        XN |br|
        X9 |br|
        SX9
      - String
      - 可变长度数据形式中，所有字段都作为字符串(String)读写。

        指定哪个类型标识符动作都不会改变。
        而且，由于没有字段长度概念，不需要参数。

        如果想将字符串作为数值形式(BigDecimal)读写，
        使用 :ref:`number转换器 <data_format-number_convertor>`
        或 :ref:`signed_number转换器 <data_format-signed_number_convertor>` 。

        输出目标值为 ``null`` 时，将值转换为空字符串后处理。
        
        读取值为空字符串时转换为 ``null`` 。
        不想将空字符串转换为 ``null`` 时，在 :java:extdoc:`convertEmptyToNull <nablarch.core.dataformat.convertor.VariableLengthConvertorSetting.setConvertEmptyToNull(boolean)>` 中设置 ``false`` 。


JSON和XML数据形式可用的字段类型一览
  .. list-table::
    :class: white-space-normal
    :header-rows: 1
    :widths: 13 15 72

    * - 类型
      - Java型
      - 说明

    * - .. _data_format-field_type-nullable_string:

        X |br|
        N |br|
        XN
      - String
      - 字符串数据类型

        不进行填充等编辑。

        JSON时，输出时值用双引号 ``"`` 包围。

        输出目标值为 ``null`` 时，JSON中不进行值转换，
        XML中转换为空字符串。

    * - X9 |br|
        SX9 |br|
      - String
      - 数字字符串类型

        不进行填充等数据编辑。输出时值原样输出。

        如果想将字符串作为数值形式(BigDecimal)读写，
        使用 :ref:`number转换器 <data_format-number_convertor>`
        或 :ref:`signed_number转换器 <data_format-signed_number_convertor>` 。

        输出目标值为 ``null`` 时的处理方式与
        :ref:`字符串数据类型的字段类型 <data_format-field_type-nullable_string>` 相同。

    * - BL
      - String	
      - 字符串( ``true`` 或 ``false`` 的字符串表示)

        不进行填充等数据编辑。输出时值原样输出。

        输出目标值为 ``null`` 时的处理方式与
        :ref:`字符串数据类型的字段类型 <data_format-field_type-nullable_string>` 相同。

    * - .. _data_format-nest_object:

        OB
      - \-
      - 指定嵌套记录类型时使用。

        与字段名对应的记录类型作为嵌套元素输入输出。

        输出目标值为 ``null`` 时的处理方式与
        :ref:`字符串数据类型的字段类型 <data_format-field_type-nullable_string>` 相同。

        以下显示使用示例。

        json
          .. code-block:: json

            {
              "users": [
                {
                  "name"    : "姓名",
                  "age"     : 30,
                  "address" : "地址"
                },
                {
                  "name"    : "姓名1",
                  "age"     : 31,
                  "address" : "地址1"
                }
              ]
            }

        xml
          .. code-block:: xml
            
            <users>
              <user>
                <name>姓名</name>
                <age>30</age>
                <address>地址</address>
              </user>
              <user>
                <name>姓名1</name>
                <age>31</age>
                <address>地址1</address>
              </user>
            </users>

        上述json及xml对应的格式定义文件如下。

        .. code-block:: bash

          [users]       # 根元素
          1 user [1..*] OB

          [user]        # 嵌套元素
          1 name    N   # 最下层元素
          2 age     X9
          3 address N


.. _data_format-field_convertor_list:

字段转换器一览
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
标准提供的数据转换器一览如下。

.. list-table::
  :class: white-space-normal
  :header-rows: 1
  :widths: 20 30 50

  * - 转换器名
    - 型转换规格
    - 说明

  * - pad
    - 无型转换
    - 设置填充及修剪的字符。

      填充及修剪位置按字段类型分别如下动作。

      :X: 右修剪、右填充
      :N: 右修剪、右填充
      :XN: 右修剪、右填充
      :Z: 左修剪、左填充
      :SZ: 左修剪、左填充
      :P: 左修剪、左填充
      :SP: 左修剪、左填充
      :X9: 左修剪、左填充
      :SX9: 左修剪、左填充

      字段类型的详细内容请参考 :ref:`data_format-field_type_list` 。

      :参数: 填充、修剪的对象值 ``必填``

  * - encoding
    - 无型转换
    - 设置字符串型字段的字符编码。

      特定字段覆盖共同设置( :ref:`text-encoding <data_format-directive_text_encoding>` )时设置。

      只能对 ``X`` 、 ``N`` 、 ``XN`` 字段使用。
      对其他字段类型设置时会被忽略。

      :参数: 编码名(字符串) ``必填``


  * - 字面量值
    - 无型转换
    - 设置输出时的默认值。

      输出时值为未设置时，输出指定的字面量值。

      输入时不使用此设置值。

  * - .. _data_format-number_convertor:
    
      number
    - String <-> BigDecimal
    - 将数字字符串转换为数值(BigDecimal)时设置。

      :输入时: 检查输入的数字字符串是否为无符号数值形式，\
               转换为BigDecimal型。

      :输出时: 将输出值转换为字符串，检查是否为无符号数值形式后输出。

  * - .. _data_format-signed_number_convertor:
      
      signed_number

    - String <-> BigDecimal

    - 将带符号的数字字符串转换为数值(BigDecimal)时设置。

      允许符号的点以外与 :ref:`number转换器 <data_format-number_convertor>` 规格相同。

  * - .. _data_format-replacement_convertor:
      
      replacement
    - 无型转换
    - 输入输出时都将替换对象字符转换为替换目标字符返回。

      :参数: 替换类型名 ``可选``

      详细内容请参考 :ref:`data_format-replacement` 。


项目定义的省略
--------------------------------------------------
说明格式定义文件的项目定义与实际数据的项目定义不匹配时的行为。

固定长度及可变长度数据时
  固定长度及可变长度数据时，实际数据与格式定义的项目定义必须严格匹配。
  因此，即使应用中有不需要的项目存在，也需要在格式定义文件上定义项目。

JSON及XML数据时
  JSON及XML时，格式定义文件上未定义的项目会成为读取对象外。
  因此，即使实际数据上存在项目，如果应用中不需要则可以不定义项目。
  
