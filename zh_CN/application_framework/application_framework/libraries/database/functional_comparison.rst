.. _`database-functional_comparison`:

通用DAO与Jakarta Persistence的功能比较
----------------------------------------------------------------------------------------------------
本章展示以下功能的比较。

* :ref:`通用DAO <universal_dao>`
* |JSR317|

.. important::

  通用DAO仅支持JPA定义的注解中， :ref:`universal_dao_jpa_annotations` 中记述的部分。
  此处未记述的注解相关功能无法使用。

.. list-table:: 功能比较（○：提供　△：部分提供　×：不提供　－:对象外）
  :header-rows: 1
  :class: something-special-class

  * - 功能
    - 通用DAO
    - Jakarta Persistence

  * - 可以处理关联关系(Relationship) |br|
    - × [#relation]_
    - ○

  * - 可以基于Entity执行CRUD |br|
      无需创建SQL即可执行CRUD的SQL
    - ○ |br| :ref:`前往解说 <universal_dao-execute_crud_sql>`
    - ○

  * - 可以将搜索结果作为Java Beans对象获取
    - ○ |br| :ref:`前往解说 <universal_dao-bean_mapping>`
    - ○

  * - 可以执行任意SQL语句
    - ○ |br| :ref:`前往解说 <universal_dao-sql_file>`
    - ○

  * - 可以动态组装SQL
    - △ [#criteria]_ |br| :ref:`前往解说 <universal_dao-sql_file>`
    - ○

  * - 可以执行批处理
    - ○ |br| :ref:`前往解说 <universal_dao-batch_execute>`
    - ×

  * - 获取大量数据时可以进行延迟加载 |br|
      （不压迫堆而处理大量数据）
    - ○ |br| :ref:`前往解说 <universal_dao-lazy_load>`
    - ×

  * - 可以进行分页用的范围指定搜索
    - ○ |br| :ref:`前往解说 <universal_dao-paging>`
    - ○

  * - 可以生成代理键的值
    - ○ |br| :ref:`前往解说 <universal_dao-generate_surrogate_key>`
    - ○

  * - Entity状态反映到数据库时可以 |br| 执行Jakarta Bean Validation
    - × [#validaiton]_
    - ○

  * - 可以在数据库访问前后 |br| 执行任意处理（回调调用）
    - × [#callback]_
    - ○

  * - 可以进行并发控制
    - △ [#lock]_ |br| :ref:`前往解说(乐观锁) <universal_dao_jpa_optimistic_lock>` |br| :ref:`前往解说(悲观锁) <universal_dao_jpa_pessimistic_lock>`
    - ○

.. [#relation] 有关联关系的表搜索可以通过创建SQL来对应。登记、更新、删除则通过每次调用各表所需的处理来对应。
.. [#criteria] 通用DAO中，条件和排序项目可以动态组装。详细内容请参阅 :ref:`SQL的动态组装 <database-variable_condition>`
.. [#validaiton] Nablarch在接受外部数据时实施校验，仅在没有校验错误时才转换为Entity并保存到数据库。
.. [#callback] 需要任意处理时，可以通过在调用通用DAO的一侧进行处理来对应。
.. [#lock] 通用DAO仅支持乐观锁。不支持悲观锁及Jakarta Persistence中定义的搜索时锁模式指定等。（悲观锁可以通过使用 ``select for update`` 等实现。）

.. |jsr317| raw:: html

   <a href="https://jakarta.ee/specifications/persistence/" target="_blank">Jakarta Persistence(外部站点，英语)</a>

.. |br| raw:: html

  <br />
