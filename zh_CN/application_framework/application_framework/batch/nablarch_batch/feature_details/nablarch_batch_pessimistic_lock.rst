.. _nablarch_batch_pessimistic_lock:

Nablarch Batch应用的悲观锁
============================================================
本章节给出了在Nablarch Batch应用中使用悲观锁的实现示例。
参考以下示例进行实现，可以缩短锁定时间，减少对其他进程的影响。

要点
 * 数据读取器只获取数据的主键。
 * 在 `handle` 方法内为数据加悲观锁。
   使用 :ref:`universal_dao` 为数据加悲观锁请参考 :ref:`universal_dao_jpa_pessimistic_lock` 。

.. code-block:: java

  public class SampleAction extends BatchAction<SqlRow> {

      @Override
      public DataReader<SqlRow> createReader(final ExecutionContext ctx) {
          final DatabaseRecordReader reader = new DatabaseRecordReader();
          final SqlPStatement statement = DbConnectionContext.getConnection()
                  .prepareParameterizedSqlStatementBySqlId(
                          Project.class.getName() + "#GET_ID");

          // 省略设置检索条件

          reader.setStatement(statement, condition);
          return reader;
      }

      @Override
      public Result handle(final SqlRow inputData, final ExecutionContext ctx) {
          final Project project =
                  UniversalDao.findBySqlFile(Project.class, "FIND_BY_ID_WITH_LOCK", inputData);

          // 省略业务处理

          UniversalDao.update(project);
          return new Success();
      }
  }

