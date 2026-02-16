.. _database_management:

数据库访问
==================================================
提供连接数据库和执行SQL的功能。

Nablarch提供了以下两种数据库访问功能。

.. toctree::
  :maxdepth: 1

  database/database
  database/universal_dao

无论使用上述哪种功能，都可以执行SQL，但出于以下原因，建议使用 :ref:`通用DAO <universal_dao>` 。

* 能够从Entity自动生成CRUD的SQL语句并执行
* 搜索结果可以作为Bean对象获取，因此可以有效利用IDE的补全功能，提高开发效率

.. important::

  :ref:`通用DAO <universal_dao>` 也是使用 :ref:`JDBC包装器功能 <database>` 来连接数据库和执行SQL的。
  因此，需要使用 :ref:`JDBC包装器功能 <database>` 所需的配置等。

.. tip::
 :ref:`universal_dao` 与Jakarta Persistence的功能对比，请参阅 :ref:`database-functional_comparison` 。

.. toctree::
  :hidden:

  database/functional_comparison
