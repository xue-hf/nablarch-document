.. _nablarch_batch_multiple_process:

驻留型Batch应用的多Process化
======================================================================
基本与 :ref:`基于数据库队列的多进程消息处理<db_messaging-multiple_process>`
的机制相同，具体可参考该部分内容。

但需注意，由于 Action 的实现方式与基于数据库队列的消息处理有所不同，
以下提供使用 DatabaseRecordReader 时 Action 的实现示例。

此外，若自行实现了 Reader，建议参考下方示例，加悲观锁之后再提取待处理数据。

  .. code-block:: java
  
    /**
     * Process ID。
     *
     * 本例中，基于UUID生成Process ID。
     */
    private final String processId = UUID.randomUUID()
                                         .toString();

    @Override
    public DatabaseRecordReader createReader(ExecutionContext context) {
        final Map<String, String> param = new HashMap<>();
        param.put("processId", processId);
        
        // 创建用于提取当前进程已加悲观锁的未处理数据的 DatabaseRecordReader
        final DatabaseRecordReader reader = new DatabaseRecordReader();
        final ParameterizedSqlPStatement statement =
            DbConnectionContext.getConnection()
                               .prepareParameterizedSqlStatementBySqlId(
                                   FileCreateRequest.class.getName() + "#GET_MISHORI_FILE_INFO");
        reader.setStatement(statement, param);
        
        // 注册 DatabaseRecordReader 在提取数据前执行的回调处理，用于执行悲观锁 SQL。
        // 注意：该处理必须在独立事务中执行。
        databaseRecordReader.setListener(new DatabaseRecordListener() {
          @Override
          public void beforeReadRecords() {
            new SimpleDbTransactionExecutor<Void>(SystemRepository.get("myTran")) {
              @Override
              public Void execute(final AppDbConnection connection) {
                final ParameterizedSqlPStatement statement = connection.
                    prepareParameterizedSqlStatementBySqlId(
                        FileCreateRequest.class.getName() + "#MARK_UNPROCESSED_DATA");
                statement.executeUpdateByMap(param);
                return null;
              }
            }.doTransaction();
          }
        });
        
        return reader;
    }
  



