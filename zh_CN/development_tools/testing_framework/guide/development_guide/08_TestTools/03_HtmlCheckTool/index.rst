.. _html_check_tool:

======================
HTML检查工具
======================

记述HTML检查工具的目的、规格、使用方法。


目的
====

* 防止因结束标签遗漏等语法错误导致向用户显示与预期不同的画面。
* 防止使用项目规范中禁止的标签。


规格
====

对请求单体测试中自动生成的HTML文件执行以下检查，检测到非法HTML时测试失败。
本工具标准集成在请求单体测试中，执行请求单体测试时也会执行本工具。

* 默认\ [#]_\ 遵循HTML4.01进行HTML文件语法检查。\ [#]_\ 
* 检查开始标签・结束标签的描述遗漏。即使HTML4.01规定可以省略的标签，也不允许省略。
* 检查是否未使用设置文件\ [#]_ \中记载的标签・属性。
* 不区分大小写。 例：) <tr>, <TR>, <Tr>, <tR>
* boolean属性可用。 例：) <textarea disabled>
* 属性指定中不允许省略引号。 例：) ○ <table align="center"> × <table align=center>

.. [#] 通过更改设置值，可以自定义检查内容。

.. [#] 部分例外。请参考下一项『\ `与HTML4.01的差异点`_ 』。

.. [#]
  默认设置中，设置了 `W3C官方网站 <https://www.w3.org/TR/html401/>`_ 中不推荐使用的标签・属性(以下简称为"不推荐标签・属性")。
  通过自定义设置文件，可以更改禁止使用的标签・属性。（自定义方法请参考 :ref:`01_custom` 。）

.. tip::

  HTML中直接描述的JavaScript中出现2个以上连续的"-"时，测试将失败。\
  显示导致测试失败的JavaScript实现示例和错误消息如下。
  
  导致测试失败的JavaScript实现示例
  
   .. code-block:: jsp
   
    var message = "--"   // 字符串中「-」连续。
      , count = 10;
    count--;             //  递减运算符中「-」连续。
  
  错误消息
  
   .. code-block:: bash
   
    Lexical error at line 965, column 31.  Encountered: "-" (45), after : "--"

  对应方法

   不要直接在HTML(JSP)中描述JavaScript，而是外部文件化后描述。

.. 错误内容和对应方法请参考javascript编码规范的\
 【JavaScript描述在HTML中时，不要连续描述2个以上「-」（连字符）。】\
 。


与HTML4.01的差异点
------------------

由于当前的Web应用程序通常在客户端动态操作DOM，
本工具允许正文为空的标签。

例如，以下标签不会报错。

.. code-block:: html

  <!-- 空的span标签 -->
  <span id="foo"></span>

  <!-- 无option的select标签 -->
  <select id="bar"></select>  


使用方法
========

前提条件
--------

* 可以执行请求单体测试。

.. _01_custom:

禁用标签・属性的自定义方法
-------------------------------------

使用默认设置时，项目开始时无需进行下述设置更改。

测试项目的自动化测试用设置文件中记述了记述禁用标签・属性的设置文件路径。
由于设置文件路径在htmlCheckerConfig属性中指定，如果将设置文件配置在分发时不同的位置，请修改此属性。 

  .. code-block:: xml

     <component name="httpTestConfiguration" class="nablarch.test.core.http.HttpTestConfiguration">
      
          (省略)

          <property name="htmlCheckerConfig" value="test/resources/httprequesttest/html-check-config.csv" />

          (省略)

     </component>

设置文件（htmlCheckerConfig属性指定的文件）按以下描述方法修改。  

  设置文件每行用逗号分隔记述标签名和属性名。
  一个标签设置多个属性时，记述在多行。
  ::

    body,bgcolor
    body,link
    body,text
    table,align
    table,bgcolor
    td,bgcolor
    td,height
    td,nowrap
    th,bgcolor
    th,height
    th,nowrap
    tr,bgcolor

  此外，如果省略属性栏，则指摘标签本身的使用。
  ::

    body,

  即使省略属性栏，也不能省略逗号。


HTML检查执行与否的设置方法
---------------------------------

通过更改自动化测试用设置文件，可以设置执行请求单体测试时是否执行HTML检查。

checkHtml属性为true时执行HTML检查，为false时不执行。

  .. code-block:: xml

     <component name="httpTestConfiguration" class="nablarch.test.core.http.HttpTestConfiguration">
      
          (省略)

          <property name="checkHtml" value="true" />

          (省略)

     </component>

.. _`customize_html_check`:

HTML检查内容的更改
---------------------------------

通过更改 nablarch.test.core.http.HttpTestConfiguration 类的 htmlChecker 属性，
可以更改执行请求单体测试时执行的HTML检查内容。

例如，始终从<html>标签开始的简单HTML检查类按以下方式实现。

  .. code-block:: java



	public class SimpleHtmlChecker implements HtmlChecker {
	
	    private String encoding;
	    
	    @Override
	    public void checkHtml(File html) throws InvalidHtmlException {
	        StringBuilder sb = new StringBuilder();
	        InputStreamReader reader = null;
	        
	        
	        try {
	            reader = new InputStreamReader(new FileInputStream(html), encoding);

	            char[] buf = new char[1024];
	            int len = 0;
	            while ((len = reader.read(buf)) > 0) {
	                sb.append(buf, 0, len);
	            }
	        } catch (Exception e) {
	            throw new RuntimeException(e);
	        } finally {
	            FileUtil.closeQuietly(reader);
	        }
	        
	        if (!sb.toString().trim().startsWith("<html>")) {
	            throw new InvalidHtmlException("html not starts with <html>");
	        }
	    }
	
	    public void setEncoding(String encoding) {
	        this.encoding = encoding;
	    }
	}



使用上述类执行HTML检查时，按以下方式设置即可。

  .. code-block:: xml
	
	
	  <component name="httpTestConfiguration"
	      class="nablarch.test.core.http.HttpTestConfiguration">
	          (省略)
	    <!-- HTML检查器设置 -->
	    <property name="htmlChecker" ref="htmlChecker" /> 
	  </component>
	
	
	  <component name="htmlChecker" class="nablarch.test.core.http.example.htmlcheck.SimpleHtmlChecker">
	  	<property name="encoding" value="UTF-8"/>
	  </component>  


测试执行时指摘确认方法
------------------------

执行请求单体测试时，如果自动生成的HTML文件中存在指摘，该测试用例将失败。

将如下在JUnit控制台中输出指摘位置和指摘内容。

.. image:: ./_image/how-to-trace-html.png
   :scale: 70

修改作为相应HTML输出来源的JSP，重新执行测试。
