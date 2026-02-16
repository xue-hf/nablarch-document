==============================================
测试框架
==============================================


.. toctree::
   :maxdepth: 1
   :titlesonly:

   guide/development_guide/05_UnitTestGuide/index
   guide/development_guide/06_TestFWGuide/index
   guide/development_guide/08_TestTools/index

测试实现者使用测试框架实现功能测试时请参考 :ref:`unitTestGuide` ，
进行测试框架导入的架构师请参考 :ref:`testFWGuide` 。

.. important::

  测试框架不支持以下基础设施和库。
  因此，针对使用这些基础设施和库的应用程序的测试，请使用 `JUnit(外部网站、英文) <https://junit.org/junit5/>`_ 等测试框架进行。

  * :ref:`符合Jakarta Batch的批处理应用程序 <jsr352_batch>`

.. important::

  测试框架不支持多线程功能。
  多线程功能的测试请在不使用测试框架的测试（集成测试等）中进行。
