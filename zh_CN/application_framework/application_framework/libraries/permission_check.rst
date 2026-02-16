权限检查
=====================================================================
提供检查用户是否拥有使用系统功能的权限的权限检查功能。

Nablarch提供以下两种权限检查功能。

.. toctree::
  :maxdepth: 1

  authorization/permission_check
  authorization/role_check

.. tip::
  **两种功能的区分使用**

  :doc:`authorization/role_check` 简化了权限管理的模型结构，通过将处理与数据的关联部分硬编码，减轻了数据管理的繁琐性。
  因此，适用于权限管理条件基本不变的系统，能够以较低成本快速引入权限管理。
  
  另一方面，对于权限管理条件可能变化的系统，虽然引入成本较高，但能够进行稳健数据管理的 :doc:`authorization/permission_check` 更为适用。
  
  详情请参考各自的说明。
