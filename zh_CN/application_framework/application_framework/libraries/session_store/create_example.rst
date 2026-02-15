.. _`create_example`:

注册功能实现示例
=====================================================================

输入画面的初始显示
---------------------------------------------------------------------
.. code-block:: java

  // 当浏览器被直接关闭等情况时，会话可能会残留，因此需要删除
  SessionUtil.delete(ctx, "project");

从输入画面跳转到确认画面
---------------------------------------------------------------------
.. code-block:: java

  // 从请求作用域获取输入信息
  ProjectForm form = context.getRequestScopedVar("form");

  // 从Form转换为Entity
  Project project = BeanUtil.createAndCopy(Project.class, form);

  // 将输入信息保存到会话存储中
  SessionUtil.put(ctx, "project", project);

从确认画面返回输入画面
---------------------------------------------------------------------
.. code-block:: java

  // 从会话存储获取输入信息
  Project project = SessionUtil.get(ctx, "project");

  // 从Entity转换为Form
  ProjectForm form = BeanUtil.createAndCopy(ProjectForm.class, project);

  // 将输入信息设置到请求作用域
  context.setRequestScopedVar("form", form);

  // 从会话存储删除输入信息
  SessionUtil.delete(ctx, "project");

执行注册处理
---------------------------------------------------------------------
.. code-block:: java

  // 从会话存储获取输入信息
  Project project = SessionUtil.get(ctx, "project");

  // 注册处理省略

  // 从会话存储删除输入信息
  SessionUtil.delete(ctx, "project");
