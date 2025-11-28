错误时的跳转目标设置方法  
==================================================

.. _forward_error_page-handler:

在handler中定义通用处理行为  
--------------------------------------------------  
通常，错误发生时的跳转目标是通过在各个Action方法上设置 :ref:`on_error_interceptor` 或 :ref:`on_errors_interceptor` 注解来指定的。

然而，当希望在整个系统中统一错误跳转页面时，如果仅依靠为每个Action方法单独添加注解的方式，可能会导致遗漏或跳转页面配置错误。  
此外，要验证是否所有功能都正确配置了跳转目标，需要逐一检查，这将带来极高的维护成本（且在实践中难以实现）。

因此，在需要系统级统一跳转至通用错误页面的情况下，建议不要在各个Action中单独指定跳转目标，  
而是通过添加一个专门处理错误跳转的handler来统一管理。

以下为示例：  
本例中，当抛出 :java:extdoc:`NoDataException <nablarch.common.dao.NoDataException>` 或 :java:extdoc:`jakarta.persistence.OptimisticLockException` 时，  
将跳转至专用的错误页面。

.. code-block:: java

  public class ExampleErrorForwardHandler implements Handler<Object, Object> {

    @Override
    public Object handle(Object data, ExecutionContext context){
      try{
        return context.handleNext(data);
      } catch (NoDataException e){
        // 当使用Universal DAO时若未找到目标数据，
        // 则跳转至表示“未找到”的错误页面。
        throw  new HttpErrorResponse(
            404, "/WEB-INF/view/common/errorPages/pageNotFoundError.jsp", e);
      } catch (OptimisticLockException e){
        // 当发生乐观锁异常时，
        // 跳转至通知用户“数据已被其他用户修改，无法完成操作”的页面。
        throw  new HttpErrorResponse(
            400, "/WEB-INF/view/common/errorPages/optimisticLockError.jsp", e);
      }
    }
  }

.. _forward_error_page-try_catch:

为一个异常定义多个跳转目标
---------------------------------------------------------
有时需要根据 :java:extdoc:`ApplicationException <nablarch.core.message.ApplicationException>` （业务异常）抛出的具体位置，动态决定错误时的跳转页面。
但由于 :ref:`on_error_interceptor` 机制仅支持为每个异常类配置单一跳转目标，
因此无法直接为 :java:extdoc:`ApplicationException <nablarch.core.message.ApplicationException>` 配置多个不同跳转路径。

在这种情况下，应通过在Action方法中使用 ``try-catch`` 块捕获异常，并手动设置不同的跳转目标。

以下为示例：

.. code-block:: java

    @InjectForm(form = ClientSearchForm.class, prefix = "form")
    @OnError(type = ApplicationException.class, path = "forward://new")
    public HttpResponse list(HttpRequest request, ExecutionContext context) {

      // 省略

      try {
        service.save(entity);
      } catch (ApplicationException e) {
        // 若在save操作中抛出ApplicationException，
        // 则跳转至与其他情况不同的页面。
        throw new HttpErrorResponse("forward://index", e);
      }

      return new HttpResponse("/WEB-INF/view/client/complete.jsp");
    }

