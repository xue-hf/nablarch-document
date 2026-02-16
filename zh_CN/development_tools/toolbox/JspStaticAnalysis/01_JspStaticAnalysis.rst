.. _jsp_static_analysis_tool:

=====================================
Jakarta Server Pages静态分析工具
=====================================

.. contents:: 目录
  :depth: 2
  :local:

----
概要
----

规定JSP中允许使用的语法和标签，并检查仅使用了允许的语法和标签。
这样可以确保以下事项。

* 由于限定了使用的语法和标签，可提高可维护性。
* 通过限定可使用的语法和标签，可以检测出消毒(sanitizing)遗漏。

本工具用于对JSP编译成功的文件进行检查。
因此，对于JSP编译不通过的文件（例如taglib的结束标签不存在等），本工具无法正确解析JSP文件。

本工具包含在nablarch-testing-XXX.jar中。

----
规格
----

允许标签的指定方法
===========================

本工具通过在配置文件中定义 **JSP中允许使用的语法和标签** ，来指出使用了配置文件中未定义的语法和标签的位置。
检查结果以HTML或XML格式输出。

本工具可指定的语法和标签如下所示。

* XML注释
* HTML注释 [#html_comment]_
* EL表达式
* 声明
* 表达式
* 脚本小程序(scriptlet)
* 指令(directive)
* 动作标签(action tag)
* 自定义标签(custom tag)

本工具无法指定HTML标签等上述以外的语法和标签。

本工具将以下位置作为检查对象外。除此以外的位置始终进行检查。

* 允许使用的标签的属性

以下举例说明禁止EL表达式时的检查结果。

* 在允许使用的标签的属性中指定EL表达式时，不会指出。 ::

    <jsp:include page="${ Expression }" />

* 在允许使用的标签的主体(body)中指定EL表达式时，会指出。 ::
     
    <jsp:text> 
       ${ Expression }
    </jsp:text>

* 在HTML标签的属性中指定EL表达式时，会指出。 ::

    <td height="${ Expression }"> </td>

* 在HTML标签的主体中指定EL表达式时，会指出。 ::

    <td> ${ Expression } </td>

* 在JavaScript中指定EL表达式时，会指出。 ::

    function samplefunc() {
        var id = ${user.id}
    }

配置文件的记述方法请参阅 :ref:`01_customJspAnalysis` 。

.. [#html_comment]

  即使将HTML注释设置为不可用，以下注释也不会作为错误被检测出来。

  * 条件注释(由IE解释的条件注释)
  * 用于加载业务画面创建支援工具的注释

  这些注释是在浏览器切换CSS或使用业务画面创建支援工具时必须使用的注释，因此不适合作为错误检测。



检查对象文件的指定方法
===============================
检查对象的文件（目录）作为启动参数指定给本工具。
如果指定了目录，则会递归地检查目标文件（默认扩展名为jsp的文件，根据设置可添加扩展名）。

检查对象的文件（部署到生产环境的文件）和
检查对象外的文件（测试用文件等不部署到生产环境的文件）
可能会混合存在于检查对象目录中。
在这种情况下，可以使用排除文件设置来禁用对不需要的文件进行检查。

检查对象的文件（目录）、检查对象外文件（目录）的设置方法请参阅 :ref:`01_customJspAnalysisProp`

将目标文件内的一部分强制设为检查对象外的方法
===================================================================
在架构师创建的JSP或标签文件等中，可能由于不得已的情况需要使用不允许的标签。
例如，将应用程序开发者创建JSP文件时不希望被使用的标签隐藏在架构师创建的标签文件内等情况。

在这种情况下，可以使用强制禁用特定位置检查的功能。
要禁用特定位置的检查，需要在该行的正上方记述禁用检查的JSP注释。
禁用注释会成为本工具检查对象外的标签。因此，即使将JSP注释设置为不可用也不会成为错误。

禁用JSP注释需遵循以下规则记述。

* 在同一行记述注释的开始标签和结束标签
* 注释必须以 **suppress jsp check** 开头

  **suppress jsp check**  之后可以记述任意注释。
  在任意注释部分记述禁用检查的理由比较好



以下示例::

  <%@tag import="java.util.regex.Pattern" %>
  <%@tag import="java.util.regex.Matcher" %>
  <%@taglib prefix="n" uri="http://tis.co.jp/nablarch" %>

  <%-- suppress jsp check:在服务器端进行判断，需要嵌入body的class中 --%>
  <%!
    static class UserAgent { 
    }
  %>

---------
前提条件
---------

* 已从原型(archetype)完成空白项目的生成。


---------
使用方法
---------

配置文件的存在确认
======================

确认tools项目的static-analysis/jspanalysis目录中存在本工具执行所需的以下文件。

* :download:`config.txt<../tools/JspStaticAnalysis/config.txt>` … Jakarta Server Pages静态分析工具配置文件
* :download:`transform-to-html.xsl<../tools/JspStaticAnalysis/transform-to-html.xsl>` … 将解析结果的XML转换为HTML时的定义文件

这些文件的详细说明请参阅 :doc:`02_JspStaticAnalysisInstall` 。


Ant任务定义文件确认
===========================

确认tools项目的nablarch-tools.xml中存在以下定义。

.. code-block:: xml

  <project name="Nablarch Toolbox">
    <!-- 中略 -->
    <target name="analyzeJsp" depends="analyzeJspOutputXml" description="进行JSP解析，输出HTML报告。">
      <java classname="nablarch.test.tool.sanitizingcheck.HtmlConvert" dir="${nablarch.tools.dir}" fork="true">
        <arg value="${jspanalysis.xmloutput}" />
        <arg value="${jspanalysis.xsl}" />
        <arg value="${jspanalysis.htmloutput}" />
        <classpath>
          <path refid="classpath.common" />
        </classpath>
      </java>
    </target>

    <target name="analyzeJspOutputXml" description="进行JSP解析，输出XML报告。">
      <java classname="nablarch.test.tool.sanitizingcheck.SanitizingCheckTask" dir="${nablarch.tools.dir}" fork="true">
        <arg value="${jspanalysis.checkjspdir}" />
        <arg value="${jspanalysis.xmloutput}" />
        <arg value="${jspanalysis.checkconfig}" />
        <arg value="${jspanalysis.charset}" />
        <arg value="${jspanalysis.lineseparator}" />
        <arg value="${jspanalysis.additionalexts}" />
        <!-- 在Jakarta Server Pages静态分析工具中，"用正则表达式设置要设为检查对象外的目录（文件）名"的项目。
             如果在parent项目的pom.xml中启用本值，请解除注释。
        <arg value="${jspanalysis.excludePatterns}" />
        -->
        <classpath>
          <path refid="classpath.common" />
        </classpath>
      </java>
    </target>
    <!-- 中略 -->
  </project>


确认要检查的目标所在项目的pom.xml
===========================================================================================

确认要检查的目标所在项目的pom.xml中存在以下记述。

.. code-block:: xml

  <properties>
    <!-- 中略 -->
    <!-- 在Jakarta Server Pages静态分析工具中，"用正则表达式设置要设为检查对象外的目录（文件）名"的项目。
         要启用本设置时，也需要解除tools目录中nablarch-tools.xml中设置的注释。
    <jspanalysis.excludePatterns></jspanalysis.excludePatterns>
    -->
    <!-- 中略 -->
  </properties>
  
  <!-- 中略 -->
  
  <build>
    <!-- 中略 -->
    <plugins>
      <!-- 中略 -->
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-antrun-plugin</artifactId>
      </plugin>
      <!-- 中略 -->
    </plugins>
  </build>

.. tip::
    
    Jakarta Server Pages静态分析工具的设置值记述在nablarch-archetype-parent的pom.xml中。
    
    .. code-block:: xml
    
      <properties>
        <!-- 中略 -->
        <!-- Jakarta Server Pages静态分析工具的设置项目 -->
        <jspanalysis.checkjspdir>${project.basedir}/src/main/webapp</jspanalysis.checkjspdir>
        <jspanalysis.xmloutput>${project.basedir}/target/jspanalysis-result.xml</jspanalysis.xmloutput>
        <jspanalysis.checkconfig>${nablarch.tools.dir}/static-analysis/jspanalysis/config.txt</jspanalysis.checkconfig>
        <jspanalysis.charset>UTF-8</jspanalysis.charset>
        <jspanalysis.lineseparator>\n</jspanalysis.lineseparator>
        <jspanalysis.htmloutput>${project.basedir}/target/jspanalysis-result.html</jspanalysis.htmloutput>
        <jspanalysis.xsl>${nablarch.tools.dir}/static-analysis/jspanalysis/transform-to-html.xsl</jspanalysis.xsl>
        <jspanalysis.additionalexts>tag</jspanalysis.additionalexts>
      </properties>
      
    关于各设置项目，请参阅 :doc:`02_JspStaticAnalysisInstall` 。
      


.. _01_customJspAnalysis:

Jakarta Server Pages静态分析工具配置文件的记述方法
========================================================

为了反映项目的规范，需要更改配置文件。

.. important::
  开发时不能根据应用程序程序员的情况更改设置。

在配置文件中按照下表记载允许使用的语法和标签的列表。
以"--"开头的行作为注释行。

================= ============================================== ========================================================  
语法或标签         JSP中的使用示例                                   配置文件中的记述方法                           
================= ============================================== ======================================================== 
XML注释           <%-- comment --%>                               <%--
HTML注释          <!-- comment -->                                <!--
EL表达式          ${10 mod 4}                                     ${
声明              <%! int i = 0; %>                               <%!
表达式            <%= map.size() %>                               <%=
脚本小程序         <%  String name = null; %>                      <%
指令              <%@ taglib prefix="n" uri=  |br|               从"<%@"开始到第一个空格为止的 |br|
                  "http://tis.co.jp/nablarch" %>                 部分记述。

                                                                 例：） <%@ taglib
动作标签          <jsp:attribute name="attrName" />              从"<jsp:"开始到第一个空格为止的 |br|
                                                                 部分记述。|br|
                                                                 如果只设置了"<jsp:"，|br|
                                                                 则所有动作标签都可以使用。

                                                                 例：） <jsp:attribute

自定义标签        <n:error name="attrName" />                    设置方法与动作标签相同。

================= ============================================== ======================================================== 


默认设置如下所示。 ::

  <n:
  <c:
  <%--
  <%@ include
  <%@ page
  <%@ tag
  <%@ taglib
  <jsp:include
  <jsp:directive.include
  <jsp:directive.page
  <jsp:directive.tag
  <jsp:param
  <jsp:params
  <jsp:attribute


默认设置中排除的语法和标签如下所示。

这些是具有与Nablarch自定义标签相同功能或可能成为安全漏洞的语法和标签。 ::

  <!--
  <%!
  ${
  <%
  <%@ attribute
  <%@ variable
  <jsp:declaration
  <jsp:expression
  <jsp:scriptlet
  <jsp:directive.attribute
  <jsp:directive.variable
  <jsp:body
  <jsp:element
  <jsp:doBody
  <jsp:forward
  <jsp:getProperty
  <jsp:invoke
  <jsp:output
  <jsp:plugin
  <jsp:fallback
  <jsp:root
  <jsp:setProperty
  <jsp:text
  <jsp:useBean

pom.xml的修正
============================================

按照执行环境修改pom.xml中记述的属性。

详细请参阅 :ref:`01_customJspAnalysisProp`


执行方法
=========

将当前目录设置为解析对象目录，执行verify阶段。

以下示例。

.. code-block:: text
                
  cd XXX-web              
  mvn verify -DskipTests=true


.. _01_outputJspAnalysis:


输出结果确认方法
=================

* JSP解析(HTML报告输出)

  进行JSP检查，将检查结果输出为HTML。

  默认设置中，输出到target/jspanalysis-result.html。

  输出目标可以通过 pom.xml 的 jspanalysis.htmloutput 属性的设置进行更改。

  输出内容示例如下。

  .. image:: ./_image/how-to-trace-jsp.png
     :scale: 70

  在上述示例中，指出内容有2种，各指出内容的处理方法如下。

  * 使用了不允许的标签时。

    会显示"语法或标签名" + "指出位置" is forbidden.这样的错误内容。
    请使用项目规范中允许使用的语法和标签进行处理。


* JSP解析(XML报告输出)

  进行JSP检查，将检查结果输出为XML。

  XML的输出目标在 pom.xml 的 jspanalysis.xmloutput 属性中指定。

  输出的XML经过XSLT等格式化后，可以创建任意报告。

  输出的XML格式如下。

  ======  ===============================
  元素名  说明
  ======  ===============================
  result  根节点
  item    为每个JSP创建的节点
  path    表示该JSP路径的节点
  errors  表示该JSP指出的节点
  error   各个指出内容
  ======  ===============================

  .. code-block:: xml
        
   <?xml version="1.0" encoding="UTF-8" standalone="no"?>
   <result>
     <item>
       <path>C:\tisdev\workspace\Nablarch_sample\web\management\user\USER-001.jsp</path>
       <errors>
         <error>&lt;!-- (at line=17 column=6) is forbidden.</error>
         <error>&lt;c:if (at line=121 column=2) is forbidden.</error>
         <error>&lt;!-- (at line=150 column=8) is forbidden.</error>
         <error>&lt;!-- (at line=151 column=8) is forbidden.</error>
         <error>&lt;!-- (at line=160 column=8) is forbidden.</error>
       </errors>
     </item>
     <item>
       <path>C:\tisdev\workspace\Nablarch_sample\web\management\user\USER-002.jsp</path>
       <errors>
         <error>&lt;!-- (at line=20 column=10) is forbidden.</error>
         <error>&lt;c:if (at line=152 column=46) is forbidden.</error>
       </errors>
     </item>
     <item>
       <path>C:\tisdev\workspace\Nablarch_sample\web\management\user\USER-004.jsp</path>
       <errors>
         <error>&lt;!-- (at line=16 column=10) is forbidden.</error>
       </errors>
     </item>
   </result>

.. tip::

 本工具的执行不应交由应用程序开发者，而应在Jenkins等CI服务器上定期执行，
 始终确保没有使用不允许的标签。


.. |br| raw:: html

  <br />
