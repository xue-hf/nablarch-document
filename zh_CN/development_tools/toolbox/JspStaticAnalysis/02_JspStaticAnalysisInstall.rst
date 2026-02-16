===================================================
Jakarta Server Pages静态分析工具 设置更改指南
===================================================

.. contents:: 目录
  :depth: 2
  :local:

:doc:`index`\ 的设置更改方法说明。

前提条件
--------

* 已从原型(archetype)完成空白项目的生成。


配置文件构成
----------------

配置文件的构成如下表所示。

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 10,13


  * - 文件名
    - 说明

  * - pom.xml
    - 启动所需的设置，以及设置jspanalysis.excludePatterns。

  * - tools/nablarch-tools.xml
    - Ant任务的定义文件 [1]_ 。通常不需要编辑。

  * - tools/static-analysis/jspanalysis/config.txt
    - Jakarta Server Pages静态分析工具配置文件。记述方法请参阅 :ref:`01_customJspAnalysis` 。

  * - tools/static-analysis/jspanalysis/transform-to-html.xsl
    - 将解析结果的XML转换为HTML时的定义文件。|br|
      记述方法请参阅 :ref:`01_outputJspAnalysis` 的"JSP解析(XML报告输出)"。

  * - nablarch-archetype-parent的pom.xml
    - 设置jspanalysis.excludePatterns以外的项目。




.. [1] 由于内部使用Ant而存在。使用者通过Maven执行，通常不需要关注。

.. _01_customJspAnalysisProp:

pom.xml的改写
-----------------------------------------------
按照执行环境修改Jakarta Server Pages静态分析工具用的属性时，如果是修改jspanalysis.excludePatterns则修改执行工具的项目的pom.xml。如果是修改其他项目则修改nablarch-archetype-parent的pom.xml。

================================  ======================================================================================
设置属性                           说明
================================  ======================================================================================
jspanalysis.checkjspdir           设置检查对象JSP目录路径或文件路径。

                                  在CI环境等批量执行检查时，|br|
                                  设置目录路径。

                                  示例::

                                     ./main/web

                                  指定目录时，将递归执行检查。

jspanalysis.xmloutput             设置检查结果XML报告文件的输出路径。

                                  示例::

                                     ./build/reports/jsp/report.xml

jspanalysis.htmloutput            设置检查结果HTML报告文件的输出路径。

                                  示例::

                                     ./build/reports/jsp/report.html

jspanalysis.checkconfig           设置Jakarta Server Pages静态分析工具配置文件的文件路径。

                                  示例::

                                    ./tool/jspanalysis/config.txt

jspanalysis.charset               设置检查对象JSP文件的字符编码。

                                  示例::

                                     utf-8

jspanalysis.lineseparator         设置检查对象JSP文件使用的换行符。|br|
                                  

                                  示例::

                                     \n

jspanalysis.xsl                   设置将检查结果的XML转换为HTML文件时的XSLT |br|
                                  文件路径。

                                  示例::

                                    ./tool/jspanalysis/transform-to-html.xsl

jspanalysis.additionalext         设置作为检查对象的JSP文件的扩展名。

                                  指定多个扩展名时，用逗号(,)分隔。|br|
                                  无论此设置值的内容如何，扩展名为 ``jsp`` 的文件 |br|
                                  必定会成为检查对象。

                                  示例::

                                    tag

jspanalysis.excludePatterns [2]_  用正则表达式设置要设为检查对象外的目录（文件）名。|br|
                                  

                                  设置多个模式时用逗号(,)分隔。

                                  示例::

                                    ui_local,ui_test,ui_test/.*/set.tag
================================  ======================================================================================

.. [2] 本设置默认是注释掉的。要使用本设置时，请解除pom.xml和tools目录的nablarch-tools.xml中的注释。

.. tip::

  文件路径(目录路径)也可以用绝对路径指定。

.. _how_to_setup_ant_view_in_eclipse_jsp_analysis:


.. |br| raw:: html

  <br />
