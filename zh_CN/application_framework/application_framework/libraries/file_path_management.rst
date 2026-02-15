.. _file_path_management:

文件路径管理
==================================================
.. contents:: 目录
  :depth: 3
  :local:

提供管理系统中使用的文件输入输出目标目录和扩展名的功能。


功能概述
--------------------------------------------------

可以使用逻辑名管理目录和扩展名
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
可以使用逻辑名来管理目录和扩展名。

在进行文件输入输出等功能中，只需指定逻辑名即可实现对相应目录下文件的输入输出。

详情请参考 :ref:`file_path_management-definition`

模块列表
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core</artifactId>
  </dependency>

使用方法
--------------------------------------------------

.. _file_path_management-definition:

设置目录和扩展名
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
在 :java:extdoc:`FilePathSetting <nablarch.core.util.FilePathSetting>` 中设置目录和扩展名，
并在组件配置文件中定义。

以下展示示例。

要点
  * :java:extdoc:`FilePathSetting <nablarch.core.util.FilePathSetting>` 的组件名称需为 ``filePathSetting``
  * 在 :java:extdoc:`basePathSettings <nablarch.core.util.FilePathSetting.setBasePathSettings(java.util.Map)>` 中设置目录
  * 在 :java:extdoc:`fileExtensions <nablarch.core.util.FilePathSetting.setFileExtensions(java.util.Map)>` 中设置扩展名
  * 对一个目录设置多个扩展名时，需设置多个逻辑名
  * 无扩展名的文件，省略该逻辑名的扩展名设置
  * 可使用 ``file`` 和 ``classpath`` 两种scheme。省略时为 ``classpath``
  * 使用 ``classpath`` scheme时，该路径必须作为目录存在。（无法指定jar等归档文件内的路径）
  * 路径中不能包含空格。（无法指定包含空格的路径）

  .. important::

    使用classpath scheme时，在某些Web应用服务器中无法使用本功能。
    这是因为Web应用服务器使用独立的文件系统来管理类路径下的资源等。

    例如，在Jboss和Wildfly中，类路径下的资源由称为vfs的虚拟文件系统管理，
    因此无法使用classpath scheme。

    因此，建议使用file scheme而非classpath scheme。



.. code-block:: xml

  <component name="filePathSetting" class="nablarch.core.util.FilePathSetting">
    <!-- 目录设置 -->
    <property name="basePathSettings">
      <map>
        <entry key="csv-input" value="file:/var/nablarch/input" />
        <entry key="csv-output" value="file:/var/nablarch/output" />

        <entry key="dat-input" value="file:/var/nablarch/input" />
        <entry key="fixed-file-input" value="file:/var/nablarch/input" />
      </map>
    </property>

    <!-- 扩展名设置 -->
    <property name="fileExtensions">
      <map>
        <entry key="csv-input" value="csv" />
        <entry key="csv-output" value="csv" />

        <entry key="dat-input" value="dat" />

        <!-- fixed-file-input无扩展名，因此不进行扩展名设置 -->
      </map>
    </property>

  </component>

获取逻辑名表示的文件路径
--------------------------------------------------
使用 :java:extdoc:`FilePathSetting <nablarch.core.util.FilePathSetting>` 获取对应逻辑名的文件路径。


以下展示若干使用示例。

.. code-block:: java

  // /var/nablarch/input/users.csv
  File users = filePathSetting.getFileWithoutCreate("csv-input", "users")

  //  /var/nablarch/output
  File csvOutputDir = filePathSetting.getBaseDirectory("csv-output");

  // /var/nablarch/input/users
  File users = filePathSetting.getFileWithoutCreate("fixed-file-input", "users")

