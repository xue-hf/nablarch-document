=======================
 主数据投入工具
=======================

.. tip::

  使用 :ref:`blank_project` 构建项目时，数据库相关工具会设置 :ref:`gsp-dba-maven-plugin <gsp-maven-plugin>` 。

  因此，向数据库投入主数据推荐使用本工具以外的 :ref:`gsp-dba-maven-plugin  <gsp-maven-plugin>` 。

.. important::

  本工具不支持多线程功能。
  多线程功能的测试请在不使用测试框架的测试(集成测试等)中进行。

.. toctree::
   :maxdepth: 1
   
   ./01_MasterDataSetupTool
   ./02_ConfigMasterDataSetupTool
