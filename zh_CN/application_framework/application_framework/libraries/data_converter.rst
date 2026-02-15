.. _data_converter:

访问各种格式的数据
==================================================
提供处理各种格式数据的功能。

Nablarch提供以下2种数据输入输出功能。

.. toctree::
  :maxdepth: 1

  数据绑定(数据与Java Beans对象映射的功能) <data_io/data_bind>
  通用数据格式(基于格式定义文件进行数据输入输出的功能) <data_io/data_format>

.. _data_converter-data_bind_recommend:

使用上述任一功能都可以进行数据访问，
但基于以下理由，建议使用 :ref:`data_bind` 。

* :ref:`data_bind` 可以将数据作为Java Beans对象处理，可以有效利用IDE的补全功能，开发效率好。(也有不会出现项目名称拼写错误等优点）
* :ref:`data_format` 的格式定义复杂难以理解。这会导致学习成本和维护成本变高。

.. important::

  对于 :ref:`data_bind` 无法处理的格式，需要使用 :ref:`data_format` 。

.. tip::

  :ref:`data_bind` 和 :ref:`data_format` 提供的功能差异，请参考 :ref:`data_io-functional_comparison` 。

.. toctree::
  :hidden:

  data_io/functional_comparison


