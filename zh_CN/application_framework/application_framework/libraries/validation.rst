.. _validation:

输入值校验
==================================================
提供用于验证从客户端发送的用户输入值以及通过系统间协作从外部系统发送的值是否合理的功能。

输入值校验主要进行以下检查：

* 输入值是否为合理的格式（例如，位数、字符种类等检查）
* 是否符合系统状态（例如，账户重复注册检查）

※关于输入值校验出错时显示的消息的定义方法，请参考 :doc:`message` 。

Nablarch提供以下两种验证功能：

.. toctree::
  :maxdepth: 1

  符合Jakarta EE的Jakarta Bean Validation标准的验证功能 (Bean Validation) <validation/bean_validation>
  Nablarch独有的验证功能 (Nablarch Validation) <validation/nablarch_validation>

虽然使用任一功能都可以进行输入值校验，但出于以下原因，建议使用符合Jakarta EE标准的功能：

* Jakarta Bean Validation在Jakarta EE中有规范定义，相关信息丰富。
* 开发者无需学习Nablarch独有的验证使用方法。

.. tip::
 关于 :ref:`bean_validation` 和 :ref:`nablarch_validation` 提供的功能差异，请参考 :ref:`validation-functional_comparison` 。

.. toctree::
  :hidden:

  validation/functional_comparison
