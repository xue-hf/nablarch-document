以数据库为输入的 Chunk 步骤
======================================================
.. contents:: 目录
  :depth: 3
  :local:
  
从数据库中提取处理对象数据时，不要使用 Jakarta Batch 提供的 reader，
而应实现本功能提供的 :java:extdoc:`BaseDatabaseItemReader <nablarch.fw.batch.ee.chunk.BaseDatabaseItemReader>` 。

通过实现 :java:extdoc:`BaseDatabaseItemReader <nablarch.fw.batch.ee.chunk.BaseDatabaseItemReader>` ，
可以使用 reader 专用的数据库连接来提取数据。
这样，即使在事务控制时会自动关闭游标的数据库中，
也能够实现以数据库为输入的 Chunk 步骤。

以下展示实现示例。

.. code-block:: java

  @Dependent
  @Named
  public class EmployeeSearchReader extends BaseDatabaseItemReader {
  
    /** 从数据库获取的结果(用于资源释放) */
    private DeferredEntityList<EmployeeForm> list;

    /** 保存从数据库获取结果的迭代器 */
    private Iterator<EmployeeForm> iterator;

    /** 进度管理 Bean */
    private final ProgressManager progressManager;

    /**
     * 构造函数。
     * @param progressManager 进度管理 Bean
     */
    @Inject
    public EmployeeSearchReader(ProgressManager progressManager) {
      this.progressManager = progressManager;
    }
  
    /**
     * 实现 BaseDatabaseItemReader 提供的 doOpen，从数据库中提取处理对象数据。
     * 获取大量数据时，为避免堆内存压力，请进行延迟加载
     */
    @Override
    public void doOpen(Serializable checkpoint) throws Exception {
      progressManager.setInputCount(
          UniversalDao.countBySqlFile(EmployeeForm.class, "SELECT_EMPLOYEE"));

      list = (DeferredEntityList<EmployeeForm>) UniversalDao.defer()
              .findAllBySqlFile(EmployeeForm.class, "SELECT_EMPLOYEE");
      iterator = list.iterator();
    }

    /**
     * 在 readItem 中，返回下一条记录。
     * 注意，当数据不存在或已处理到最后时返回 null。
     */
    @Override
    public Object readItem() {
        if (iterator.hasNext()) {
            return iterator.next();
        }
        return null;
    }

    /**
     * 需要释放资源时，实现 doClose。
     */
    @Override
    public void doClose() throws Exception {
        list.close();
    }
  }
