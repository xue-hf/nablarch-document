更新功能实现示例
=====================================================================

输入画面的初始显示
---------------------------------------------------------------------
.. code-block:: java

  // 当浏览器被直接关闭等情况时，会话可能会残留，因此需要删除
  SessionUtil.delete(ctx, "project");

  // 更新对象数据的获取处理省略

  // 将更新对象数据保存到会话存储中
  SessionUtil.put(ctx, "project", project);

  // 从Entity转换为Form
  ProjectForm form = BeanUtil.createAndCopy(ProjectForm.class, project);

  // 将更新对象数据设置到请求作用域
  context.setRequestScopedVar("form", form);

从输入画面跳转到确认画面
---------------------------------------------------------------------
.. code-block:: java

  // 从请求作用域获取输入信息
  ProjectForm form = context.getRequestScopedVar("form");

  // 从会话存储获取更新对象数据
  Project project = SessionUtil.get(context, "project");

  // 用输入信息覆盖更新对象数据
  BeanUtil.copy(form, project);

从确认画面返回输入画面
---------------------------------------------------------------------
.. code-block:: java

  // 从会话存储获取更新对象数据
  Project project = SessionUtil.get(ctx, "project");

  // 从Entity转换为Form
  ProjectForm form = BeanUtil.createAndCopy(ProjectForm.class, project);

  // 将更新对象数据设置到请求作用域
  context.setRequestScopedVar("form", form);

执行更新处理
---------------------------------------------------------------------
.. code-block:: java

  // 从会话存储获取更新对象数据
  Project project = SessionUtil.get(ctx, "project");

  // 更新处理省略

  // 从会话存储删除更新对象数据
  SessionUtil.delete(ctx, "project");
