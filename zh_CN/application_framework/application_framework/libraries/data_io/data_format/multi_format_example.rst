Fixed(固定长度)的多格式定义示例集
--------------------------------------------------

用单一字段识别格式的示例
  单一字段为条件时，该字段值与各格式定义的条件一致时，以该记录定义处理。

  本示例中，记录按以下规则识别。

  * dataKbn为1时，为header记录类型。
  * dataKbn为2时，为data记录类型。

  .. code-block:: bash

    file-type:        "Fixed" # 固定长度
    text-encoding:    "MS932" # 字符串型字段的字符编码
    record-length:    40      # 各记录的长度
    record-separator: "\r\n"  # 换行代码(crlf)

    # 记录识别字段的定义
    [Classifier]
    1 dataKbn X(1)

    # 头部记录的定义
    [header]
    dataKbn = "1"
    1 dataKbn X(1)
    2 data    X(39)

    # 数据记录的定义
    [data]
    dataKbn = "2"
    1 dataKbn X(1)
    2 data    X(39)

用多个字段识别格式的示例
  用多个字段识别记录时，满足所有条件时以该记录定义处理。

  本示例中，记录按以下规则识别。

  * dataKbn为1且type为01时，为parentData记录类型。
  * dataKbn为2且type为02时，为childData记录类型。

  .. code-block:: bash

    file-type:        "Fixed" # 固定长度
    text-encoding:    "MS932" # 字符串型字段的字符编码
    record-length:    40      # 各记录的长度
    record-separator: "\r\n"  # 换行代码(crlf)

    # 记录识别字段的定义
    [Classifier]
    1   dataKbn X(1)      # 开头1字节
    10  type    X(2)      # 第10字节起2字节

    [parentData]
    dataKbn = "1"
    type    = "01"
    1  dataKbn X(1)
    2  ?filler X(9)
    10 type    X(2)
    13 data    X(28)

    [childData]
    dataKbn = "1"
    type    = "02"
    1  dataKbn X(1)
    2  ?filler X(9)
    10 type    X(2)
    13 data    X(28)

各记录识别项目不同时的示例
  各记录识别使用的项目不同时，记录识别字段中定义识别使用的所有字段。
  各记录的条件定义部中，定义识别该记录的条件。

  本示例中，记录按以下规则识别。

  * dataKbn为1时，为header记录类型。
  * dataKbn为2且type为01时，为data1记录类型。
  * dataKbn为2且type为02时，为data2记录类型。

  .. code-block:: bash

    file-type:        "Fixed" # 固定长度
    text-encoding:    "MS932" # 字符串型字段的字符编码
    record-length:    40      # 各记录的长度
    record-separator: "\r\n"  # 换行代码(crlf)

    # 记录识别字段的定义
    [Classifier]
    1   dataKbn X(1)      # 开头1字节
    10  type    X(2)      # 第10字节起2字节

    # 头部
    [header]
    dataKbn = "1"
    1  dataKbn X(1)
    2  ?filler X(39)

    [data1]
    dataKbn = "2"
    type    = "01"
    1  dataKbn X(1)
    2  ?filler X(9)
    10 type    X(2)
    13 data    X(28)

    [data2]
    dataKbn = "2"
    type    = "02"
    1  dataKbn X(1)
    2  ?filler X(9)
    10 type    X(2)
    13 data    X(28)

Variable(可变长度)的多格式定义示例集
------------------------------------------------------------
说明Variable(可变长度)数据的多格式定义方法。

用单一字段识别格式的示例
  单一字段为条件时，该字段值与各格式定义的条件一致时，以该记录定义处理。

  本示例中，记录按以下规则识别。

  * dataKbn为1时，为header记录类型。
  * dataKbn为2时，为data记录类型。

  .. code-block:: bash

    file-type:        "Variable" # 可变长度
    text-encoding:    "MS932"    # 字符串型字段的字符编码
    record-separator: "\r\n"     # 换行代码(crlf)
    field-separator:  ","        # csv


    # 记录识别字段的定义
    [Classifier]
    1 dataKbn X

    # 头部记录的定义
    [header]
    dataKbn = "1"
    1 dataKbn X
    2 data    X

    # 数据记录的定义
    [data]
    dataKbn = "2"
    1 dataKbn X
    2 data    X

用多个字段识别格式的示例
  用多个字段识别记录时，满足所有条件时以该记录定义处理。

  本示例中，记录按以下规则识别。

  * dataKbn为1且type为01时，为parentData记录类型。
  * dataKbn为2且type为02时，为childData记录类型。

  .. code-block:: bash

    file-type:        "Variable" # 可变长度
    text-encoding:    "MS932"    # 字符串型字段的字符编码
    record-separator: "\r\n"     # 换行代码(crlf)
    field-separator:  ","        # csv

    # 记录识别字段的定义
    [Classifier]
    1 dataKbn X
    3 type    X

    [parentData]
    dataKbn = "1"
    type    = "01"
    1 dataKbn X
    2 ?filler X
    3 type    X
    4 data    X

    [childData]
    dataKbn = "1"
    type    = "02"
    1 dataKbn X
    2 ?filler X
    3 type    X
    4 data    X
 
各记录识别项目不同时的示例
  各记录识别使用的项目不同时，记录识别字段中定义识别使用的所有字段。
  各记录的条件定义部中，定义识别该记录的条件。

  本示例中，记录按以下规则识别。

  * dataKbn为1时，为header记录类型。
  * dataKbn为2且type为01时，为data1记录类型。
  * dataKbn为2且type为02时，为data2记录类型。

  .. code-block:: bash

    file-type:        "Variable" # 可变长度
    text-encoding:    "MS932"    # 字符串型字段的字符编码
    record-separator: "\r\n"     # 换行代码(crlf)
    field-separator:  ","        # csv

    # 记录识别字段的定义
    [Classifier]
    1   dataKbn X
    3   type    X

    # 头部
    [header]
    dataKbn = "1"
    1 dataKbn X
    2 ?filler X

    [data1]
    dataKbn = "2"
    type    = "01"
    1 dataKbn X
    2 ?filler X
    3 type    X
    4 data    X

    [data2]
    dataKbn = "2"
    type    = "02"
    1 dataKbn X
    2 ?filler X
    3 type    X
    4 data    X

.. _data_format-variable_title_sample:

使用标题记录时的示例
  :ref:`有标题记录 <data_format-requires-title>` 的可变长度文件时，标题记录不需要定义记录识别条件。

  标题记录以外的格式为单格式时，如下示例不需要定义记录识别( ``Classifier`` )。
  标题记录的布局定义将记录类型名设为 ``Title`` 定义。

  .. code-block:: bash

    # requires-title为true时，可以将第一行作为标题读写。
    requires-title: true  

    # 标题固有的记录类型。第一行以此记录类型读写。
    [Title]               
    1   Kubun      N
    2   Name       N
    3   Publisher  N
    4   Authors    N
    5   Price      N

    # 数据的记录类型。第一行以后的行以此记录类型读写。
    [DataRecord]          
    1   Kubun      X
    2   Name       N
    3   Publisher  N
    4   Authors    N
    5   Price      N

  标题记录以外的格式为多格式时，如下示例需要定义记录识别( ``Classifier`` )。
  表示标题记录的记录类型为 ``Title`` 的记录定义在多格式时不需要条件定义。

  .. code-block:: bash

    file-type:    "Variable"     # 可变长度
    text-encoding:     "ms932"   # 文件编码
    record-separator:  "\r\n"    # CRLF换行
    field-separator:   ","       # 字段分隔字符
    quoting-delimiter: "\""      # 包围字符
    requires-title: true         # 将第一行作为标题读写


    [Classifier]
    1  Kubun X                   # 记录类型识别字段(数据区分)
                                 # 1: 数据、2: 尾部

    # 标题固有的记录类型。多格式时也不需要格式应用条件。
    [Title]                      
    1   Kubun      N  "数据区分"
    2   Name       N  "书名"
    3   Publisher  N  "出版社"
    4   Authors    N  "作者"
    5   Price      N  "价格"

    [DataRecord]                 # 数据的记录类型
      Kubun = "1"                # 数据格式的应用条件
    1   Kubun      X             # 数据区分
    2   Name       N             # 书名
    3   Publisher  N             # 出版社
    4   Authors    N             # 作者
    5   Price      N             # 价格

    [TrailerRecord]              # 尾部的记录类型
      Kubun = "2"                # 尾部格式的应用条件
    1   Kubun      X             # 数据区分
    2   RecordNum  X             # 总件数

  .. tip::
    
    想将标题记录的记录类型名从 ``Title`` 更改时，使用 :ref:`data_format-title_type_name指令 <data_format-title_type_name>` 。
    这种情况下，将表示标题记录的记录类型名从 ``Title`` 改为 :ref:`data_format-title_type_name指令 <data_format-title_type_name>` 中设置的值。
