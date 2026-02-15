符合 Jakarta Batch 的 Batch 应用的悲观锁
============================================================
本节展示在符合 Jakarta Batch 的 Batch 应用中实现悲观锁的示例。
参考以下示例进行实现，可以缩短锁时间，减少对其他进程的影响。

要点
 * 在 `ItemReader` 中仅获取处理对象记录的主键。
 * 在 `ItemProcessor` 中根据主键获取处理对象记录并进行悲观锁。
   关于使用 :ref:`universal_dao` 的悲观锁，请参考 :ref:`universal_dao_jpa_pessimistic_lock` 。

.. code-block:: java

  @Dependent
  @Named
  public class SampleReader extends AbstractItemReader {

      private DeferredEntityList<ProjectId> list;

      private Iterator<ProjectId> iterator;

      @Override
      public void open(Serializable checkpoint) throws Exception {

          // 搜索条件的获取处理省略

          list = (DeferredEntityList<ProjectId>) UniversalDao.defer()
                  .findAllBySqlFile(ProjectId.class, "GET_ID", condition);
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

  @Dependent
  @Named
  public class SampleProcessor implements ItemProcessor {

      @Override
      public Object processItem(Object item) {
          final Project project =
                  UniversalDao.findBySqlFile(Project.class, "FIND_BY_ID_WITH_LOCK", item);

          // 业务处理省略

          return project;
      }
  }

  @Dependent
  @Named
  public class SampleWriter extends AbstractItemWriter {

      @Override
      public void writeItems(List<Object> items) {
          UniversalDao.batchUpdate(items);
      }
  }
