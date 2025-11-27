.. _nablarch_batch_retention_state:

在Batch应用的运行过程中保存状态
==================================================
在Batch应用运行过程中会存在需要保存状态的情况。
例如，Batch Action执行过程中需要保存登录条目数和更新条目数的情况。
这种情况下，可通过在Batch Action内部保持状态来实现。

下面是一个保存了登录条目数的Action样例。

对于以多线程方式执行的批处理，需要由应用侧确保其线程安全。
在本例中，使用 :java:extdoc:`AtomicInteger <java.util.concurrent.atomic.AtomicInteger>` 以实现保证。

.. code-block:: java

  public class BatchActionSample extends BatchAction<Object> {
      
      /** 登录条目数 */
      private AtomicInteger insertedCount = new AtomicInteger(0);

      @Override
      public Result handle(final Object inputData, final ExecutionContext ctx) {
          // 业务处理
          
          // 增加登录条目数
          insertedCount.incrementAndGet();
          
          return new Result.Success();
      }
  }

.. tip::

  使用 :java:extdoc:`ExecutionContext <nablarch.fw.ExecutionContext>` 的scope(作用域)同样能实现上面的效果。
  但是使用 :java:extdoc:`ExecutionContext <nablarch.fw.ExecutionContext>` 时、
  存在难以明确其保存了哪些值的缺点。
  因此，建议不要使用 :java:extdoc:`ExecutionContext <nablarch.fw.ExecutionContext>` 而是像上述实现示例那样，在Batch Action保持状态。

  此外，使用 :java:extdoc:`ExecutionContext <nablarch.fw.ExecutionContext>` 的时候、其作用域可以参照下方理解：

  :请求作用域(request scope): 每个线程单独保存状态的区域
  :会话作用域(session scope): 保存Batch整体状态的区域

