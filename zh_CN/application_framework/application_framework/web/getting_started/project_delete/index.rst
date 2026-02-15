.. _`project_delete`:

创建删除功能
==========================================
基于Example应用程序讲解删除功能。

功能说明
  1. 点击项目一览的项目ID。

    .. image:: ../images/project_delete/project_delete_list.png
      :scale: 80

  2. 点击详情画面的变更按钮。

    .. image:: ../images/project_delete/project_delete_detail.png
      :scale: 80

  3. 点击更新画面上的删除按钮。

    .. image:: ../images/project_delete/project_delete_update.png
      :scale: 80

  4. 显示完成画面。

    .. image:: ../images/project_delete/project_delete_complete.png
      :scale: 80

执行删除
-----------
按以下顺序说明删除功能的基本实现方法。

  #. :ref:`在更新画面上创建删除按钮<project_delete-update>`
  #. :ref:`创建执行删除的业务Action方法<project_delete-delete_action>`
  #. :ref:`创建删除完成画面<project_delete-complete>`

.. _`project_delete-update`:

在更新画面上创建删除按钮
  在更新画面上创建删除按钮。
  关于更新画面的创建说明，请参考 :ref:`创建显示更新画面的业务Action方法<project_update-create_edit_action>` 及
  :ref:`创建更新画面的JSP<project_update-create_update_jsp>` 。

.. _`project_delete-delete_action`:

创建执行删除的业务Action方法
  创建从数据库删除目标项目的业务Action方法。

  ProjectAction.java
    .. code-block:: java

      @OnDoubleSubmission
      public HttpResponse delete(HttpRequest request, ExecutionContext context) {

          // 显示更新画面时会话中存储了项目信息
          Project project = SessionUtil.delete(context, "project");
          UniversalDao.delete(project);

          return new HttpResponse(303, "redirect://completeOfDelete");
      }

  实现要点
    * 以主键为条件的删除，可以通过将设置了主键的Entity作为参数执行 :java:extdoc:`UniversalDao#delete <nablarch.common.dao.UniversalDao.delete(T)>`
      来实现，无需创建SQL。

  .. tip::

    :ref:`universal_dao` 仅提供以主键为条件的删除功能。以主键以外为条件进行删除时，需要另行创建SQL执行。
    关于SQL的执行方法请参考 :ref:`指定SQLID执行SQL<database-execute_sqlid>` 。

.. _`project_delete-complete`:

创建删除完成画面
  显示删除完成画面。
  关于完成画面的创建说明，请参考 :ref:`创建显示完成画面的业务Action方法<project_update-create_complete_action>` 及
  :ref:`创建更新完成画面<project_update-create_success_jsp>` 。

删除功能讲解完毕。

:ref:`返回Getting Started TOP页 <getting_started>`
