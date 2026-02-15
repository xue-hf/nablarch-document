.. _`data_io-functional_comparison`:

数据绑定与通用数据格式的对比表
----------------------------------------------------------------------------------------------------
本章显示以下功能的对比。

* :ref:`data_bind`
* :ref:`data_format`


.. list-table:: 功能对比(○：提供  △：部分提供  ×：不提供  －:对象外)
  :header-rows: 1
  :class: something-special-class

  * - 功能
    - 数据绑定
    - 通用数据格式

  * - 可以进行CSV的输入输出
    - ○ |br|
      :ref:`前往解说 <data_bind-csv_format>`
    - ○ |br|
      :ref:`前往解说 <data_format-support_type>`

  * - 可以进行每条记录格式不同的 |br| CSV的输入输出
    - × [#csv_multi_format]_
    - ○ |br|
      :ref:`前往解说 <data_format-multi_layout_data>`

  * - 可以设置CSV的定义 |br|
      (可以更改逗号和引号字符等)
    - ○ |br|
      :ref:`前往解说 <data_bind-csv_format>`
    - ○ |br|
      :ref:`前往解说 <data_format-variable_data_directive>`

  * - 可以进行固定长度数据的输入输出
    - ○ |br|
      :ref:`前往解说 <data_bind-fixed_length_format>`
    - ○ |br|
      :ref:`前往解说 <data_format-support_type>`

  * - 可以进行每条记录格式不同的 |br| 固定长度数据的输入输出
    - ○ |br|
      :ref:`前往解说 <data_bind-fixed_length_format-multi_layout>`
    - ○ |br|
      :ref:`前往解说 <data_format-multi_layout_data>`

  * - 可以进行JSON数据的输入输出
    - × [#json_layout]_
    - ○ |br|
      :ref:`前往解说 <data_format-support_type>`

  * - 可以进行XML数据的输入输出
    - × [#xml_layout]_
    - ○ |br|
      :ref:`前往解说 <data_format-support_type>`

  * - 可以在数据输入输出时进行值转换 |br|
      (trim、压缩数值、区域数值的转换等)
    - △ [#converter]_
    - ○ |br|
      :ref:`前往解说 <data_format-value_convertor>`

  * - 可以进行数据的替代字 |br|
      指转换为系统可接受的字符等
    - × [#char_replace]_
    - ○ |br|
      :ref:`前往解说 <data_format-replacement>`

.. [#csv_multi_format] 处理每条记录格式不同的CSV时，使用 :ref:`data_format` 。
.. [#json_layout] JSON数据的输入输出未实现。处理JSON数据时，使用 :ref:`data_format` 或OSS。
.. [#xml_layout] XML数据的输入输出未实现。处理XML数据时，使用 :ref:`data_format` 或Jakarta XML Binding。
.. [#converter] 仅固定长度数据提供trim等转换器。CSV中想转换值时，在输出前和输入后进行转换。
.. [#char_replace] 输入数据的替代字(字符转换)通过创建字符转换用handler来对应。

.. |br| raw:: html

  <br />
