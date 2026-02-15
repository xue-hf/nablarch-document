.. _exclusive_control:

并发控制
=====================================================================

.. contents:: 目录
  :depth: 3
  :local:

该功能对数据库的数据更新进行并发控制。
通过此功能，即使从多个事务（Web或Batch）同时更新数据库的同一数据，
也能保持数据的完整性。

.. _exclusive_control-deprecated:

.. important::
 该功能由于以下原因 **已弃用** 。
 并发控制请使用 :ref:`universal_dao` 。

 * :ref:`universal_dao` 的并发控制比本功能更易于使用。
   请参考 :ref:`universal_dao_jpa_optimistic_lock` 、 :ref:`universal_dao_jpa_pessimistic_lock` 。
 * 当主键定义为非字符串类型时，某些数据库无法使用此功能。
   此功能将所有主键值作为字符串类型( `java.lang.String` )保存。
   当主键的列定义为非字符串类型（char或varchar以外）时，
   某些数据库会因类型不匹配而在SQL语句执行时发生异常。
   例如，像PostgreSQL这样不执行隐式类型转换的数据库会发生此问题。

功能概述
---------------------------------------------------------------------

可以进行乐观锁/悲观锁
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
该功能通过在表中定义版本号列来实现乐观锁/悲观锁。
在本框架中，将定义了版本号列的表称为 **并发控制用表** 。

通过该功能可以实现以下功能。

* :ref:`exclusive_control-optimistic_lock`
* :ref:`exclusive_control-optimistic_lock-bulk`
* :ref:`exclusive_control-pessimistic_lock`

该功能提供的乐观锁/悲观锁由于使用相同的并发控制用表实现，
即使并行使用乐观锁和悲观锁，也能防止同一数据被同时更新。
例如，即使并行运行使用乐观锁的Web和使用悲观锁的Batch，
也能保持数据的完整性。

并发控制用表按并发控制的单位定义，在业务允许的最大单位下定义。
例如，如果业务上允许以"用户"这样大的单位进行锁定，
则在该单位下定义并发控制用表。
但是，单位越大，冲突的可能性越高，
需要注意会导致更新失败（乐观锁情况下）或处理延迟（悲观锁情况下）。

.. tip::
 通常，并发控制用表的单位从业务角度定义。
 例如，如果销售处理和收款处理的更新同时进行，
 则将这些处理相关的表汇总为单位来定义并发控制用表。

 此外，从表设计的角度也可以定义并发控制用表的单位。
 例如，如果表之间的父子关系明确，如头部（父）和明细（子），
 则以父的单位定义并发控制用表。
 如果父子关系不明确，则需要判断哪个作为父，然后定义并发控制用表。

.. important::

 完成并发控制用表的设计后，设计更新顺序。
 通过确定各表的更新顺序，实现死锁预防和更新时的数据完整性保证。
 在数据库中，更新记录会加上行锁，
 如果不确定更新顺序，发生死锁的可能性非常高。

模块列表
---------------------------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-exclusivecontrol</artifactId>
  </dependency>
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-exclusivecontrol-jdbc</artifactId>
  </dependency>

  <!-- 仅在进行乐观锁时 -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web-tag</artifactId>
  </dependency>

使用方法
---------------------------------------------------------------------

.. _exclusive_control-optimistic_setting:

使用并发控制的准备工作
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
要使用并发控制，需要进行 **配置** 和 **创建保存并发控制所需信息的类** 。

配置
 :java:extdoc:`BasicExclusiveControlManager <nablarch.common.exclusivecontrol.BasicExclusiveControlManager>` 的配置添加到组件定义中。

 .. code-block:: xml

  <!-- 组件名称设置为"exclusiveControlManager"。 -->
  <component name="exclusiveControlManager"
             class="nablarch.common.exclusivecontrol.BasicExclusiveControlManager">
      <!-- 乐观锁发生排他错误时使用的消息ID -->
      <property name="optimisticLockErrorMessageId" value="CUST0001" />
  </component>

创建保存并发控制所需信息的类
 创建继承 :java:extdoc:`ExclusiveControlContext <nablarch.common.exclusivecontrol.ExclusiveControlContext>` 的类。
 这个类为每个并发控制用表创建，在调用并发控制API时使用。

 .. code-block:: sql

  -- 并发控制用表
  CREATE TABLE USERS (
      USER_ID CHAR(6) NOT NULL,
      -- 主键以外的业务数据省略。
      VERSION NUMBER(10) NOT NULL,
      PRIMARY KEY (USER_ID)
  )

 .. code-block:: java

  // 对应并发控制用表USERS的类。
  // 继承ExclusiveControlContext。
  public class UsersExclusiveControl extends ExclusiveControlContext {

      // 并发控制用表的主键用枚举类型定义。
      private enum PK { USER_ID }

      // 定义获取主键值的构造函数。
      public UsersExclusiveControl(String userId) {

          // 使用父类的setTableName方法设置表名。
          setTableName("USERS");

          // 使用父类的setVersionColumnName方法设置版本号列名。
          setVersionColumnName("VERSION");

          // 使用父类的setPrimaryKeyColumnNames方法
          // 使用Enum的values方法，设置所有主键的枚举类型。
          setPrimaryKeyColumnNames(PK.values());

          // 使用父类的appendCondition方法添加主键的值。
          appendCondition(PK.USER_ID, userId);
      }
  }

.. _exclusive_control-optimistic_lock:

进行乐观锁
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
乐观锁通过在获取更新目标数据时获取并发控制用表的版本号，
在更新时检查事先获取的并发控制用表的版本号是否已被更新来实现。

乐观锁使用 :java:extdoc:`HttpExclusiveControlUtil <nablarch.common.web.exclusivecontrol.HttpExclusiveControlUtil>` 。

以具有输入→确认→完成的更新功能为例，展示乐观锁的实现示例。

输入画面的初始显示
 .. code-block:: java

  public HttpResponse index(HttpRequest request, ExecutionContext context) {

      // (业务处理)
      // 从请求获取用于获取更新目标数据的主键条件。
      String userId = getUserId(request);

      // (并发控制)
      // 生成主键类，准备版本号。
      // 获取的版本号由框架设置到指定的ExecutionContext中。
      HttpExclusiveControlUtil.prepareVersion(context, new UsersExclusiveControl(userId));

      // (业务处理)
      // 获取更新目标数据，为显示输入画面设置到request scope中。
      context.setRequestScopedVar("user", findUser(userId));

      return new HttpResponse("/input.jsp");
  }

输入画面的确认按钮（输入→确认）
 .. code-block:: java

  @OnErrors({
      @OnError(type = ApplicationException.class, path = "/input.jsp"),
      @OnError(type = OptimisticLockException.class, path = "/error.jsp")
  })
  public HttpResponse confirm(HttpRequest request, ExecutionContext context) {

      // (并发控制)
      // 进行版本号的更新检查。
      // 版本号由框架从指定的HttpRequest中获取。
      // 如果版本号已被更新，会抛出OptimisticLockException，
      // 因此请指定@OnError来指定跳转目标。
      HttpExclusiveControlUtil.checkVersions(request, context);

      // (业务处理)
      // 进行输入数据的检查，为显示确认画面设置到request scope中。
      context.setRequestScopedVar("user", getUser(request));

      return new HttpResponse("/confirm.jsp");
  }

 .. important::
  如果不进行版本号检查( :java:extdoc:`HttpExclusiveControlUtil.checkVersions <nablarch.common.web.exclusivecontrol.HttpExclusiveControlUtil.checkVersions(nablarch.fw.web.HttpRequest,nablarch.fw.ExecutionContext)>` )，
  画面间的版本号将无法继承。

确认画面的更新按钮（确认→完成）
 .. code-block:: java

  @OnErrors({
      @OnError(type = ApplicationException.class, path = "/input.jsp"),
      @OnError(type = OptimisticLockException.class, path = "/error.jsp")
  })
  public HttpResponse update(HttpRequest request, ExecutionContext context) {

      // (并发控制)
      // 进行版本号的更新检查和更新。
      // 版本号由框架从指定的HttpRequest中获取。
      // 如果版本号已被更新，会抛出OptimisticLockException，
      // 因此请指定@OnError来指定跳转目标。
      HttpExclusiveControlUtil.updateVersionsWithCheck(request);

      // (业务处理)
      // 进行输入数据的检查，执行更新处理。
      // 为显示完成画面，将更新数据设置到request scope中。
      User user = getUser(request);
      update(user);
      context.setRequestScopedVar("user", user);

      return new HttpResponse("/complete.jsp");
  }

.. _exclusive_control-optimistic_lock-bulk:

批量更新时进行乐观锁
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
对于批量更新多个记录的特定属性（如逻辑删除标志等）的处理，
有时希望仅对选中的记录进行乐观锁检查。

根据并发控制用表的主键是 **非复合主键** 还是 **复合主键** ，
有两种实现方法。

非复合主键的情况
 以批量删除用户的画面为例，展示非复合主键时的实现示例。
 版本号的获取部分只需调用 :java:extdoc:`HttpExclusiveControlUtil#prepareVersions <nablarch.common.web.exclusivecontrol.HttpExclusiveControlUtil.prepareVersions(nablarch.fw.ExecutionContext,java.util.List)>` ，
 因此省略实现示例。

 .. code-block:: html

  <!-- 画面实现（前后省略） -->
  <tr>
    <th>删除对象</th>
    <th>用户名</th>
  </tr>
  <tr>
    <!-- 通过请求参数 "user.deactivate" 发送用户的主键。 -->
    <td><checkbox name="user.deactivate" value="user001" /></td>
    <td>用户001</td>
  </tr>
  <tr>
    <td><checkbox name="user.deactivate" value="user002" /></td>
    <td>用户002</td>
  </tr>

 .. code-block:: java

  // (并发控制:检查)
  // 仅将请求参数 "user.deactivate" 中设置的用户主键
  // 作为检查对象。
  HttpExclusiveControlUtil.checkVersions(request, context, "user.deactivate");

 .. code-block:: java

  // (并发控制:检查和更新)
  // 仅将请求参数 "user.deactivate" 中设置的用户主键
  // 作为检查和更新的对象。
  HttpExclusiveControlUtil.updateVersionsWithCheck(request, "user.deactivate");

复合主键的情况
 以批量删除用户的画面为例，展示复合主键时的实现示例。
 版本号的获取部分只需调用 :java:extdoc:`HttpExclusiveControlUtil#prepareVersions <nablarch.common.web.exclusivecontrol.HttpExclusiveControlUtil.prepareVersions(nablarch.fw.ExecutionContext,java.util.List)>` ，
 因此省略实现示例。

 .. code-block:: sql

  -- 定义了复合主键的表。
  CREATE TABLE USERS (
      USER_ID CHAR(6) NOT NULL,
      PK2     CHAR(6) NOT NULL,
      PK3     CHAR(6) NOT NULL,
      -- 主键以外的业务数据省略。
      VERSION NUMBER(10) NOT NULL,
      PRIMARY KEY (USER_ID,PK2,PK3)
  )

 .. code-block:: java

  // 对应并发控制用表USERS的类。
  public class UsersExclusiveControl extends ExclusiveControlContext {

      // 并发控制用表的主键用枚举类型定义。
      private enum PK { USER_ID, PK2, PK3 }

      // 定义获取主键值的构造函数，使用父类的方法设置必要信息。
      public UsersExclusiveControl(String userId, String pk2, String pk3) {
          setTableName("USERS");
          setVersionColumnName("VERSION");
          setPrimaryKeyColumnNames(PK.values());
          appendCondition(PK.USER_ID, userId);
          appendCondition(PK.PK2, pk2);
          appendCondition(PK.PK3, pk3);
      }
  }

 .. code-block:: html

  <!-- 画面实现（前后省略） -->
  <tr>
    <th>删除对象</th>
    <th>用户名</th>
  </tr>
  <tr>
    <!--
    通过请求参数 "user.deactivate" 发送用户的主键。
    复合主键时，使用分隔符（任意，但不能是主键的值）
    连接后的字符串指定。
    -->
    <td>
      <input id="checkbox" type="checkbox" name="user.userCompositeKeys"
                                           value="user001,pk2001,pk3001" />
    </td>
    <td>用户001</td>
  </tr>
  <tr>
    <td>
      <input id="checkbox" type="checkbox" name="user.userCompositeKeys"
                                           value="user002,pk2002,pk3002" />
    </td>
    <td>用户002</td>
  </tr>

 .. tip::
  使用对应复合主键的自定义标签和
  :java:extdoc:`CompositeKey<nablarch.common.web.compositekey.CompositeKey>` ，
  可以更简单地处理复合主键。详情请参考 :ref:`tag-composite_key` 。

 .. code-block:: java

  // (并发控制:检查)
  // Form中考虑了分隔符，实现了从请求参数中提取主键的处理。
  User[] deletedUsers = form.getDeletedUsers();

  // 按记录调用检查。
  for(User deletedUser : deletedUsers) {
      HttpExclusiveControlUtil.checkVersion(
          request, context,
          new UsersExclusiveControl(deletedUser.getUserId(),
                                    deletedUser.getPk2(),
                                    deletedUser.getPk3()));
  }

 .. code-block:: java

  // (并发控制:检查和更新)
  User[] deletedUsers = form.getDeletedUsers();

  // 按记录调用检查和更新。
  for(User deletedUser : deletedUsers) {
      HttpExclusiveControlUtil.updateVersionWithCheck(
          request, new ExclusiveUserCondition(deletedUser.getUserId(),
                                              deletedUser.getPk2(),
                                              deletedUser.getPk3()));
  }

.. _exclusive_control-pessimistic_lock:

进行悲观锁
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
悲观锁通过在获取更新目标数据之前更新并发控制用表的版本号来实现。

通过在获取更新目标数据之前更新并发控制用表的版本号，
更新处理的事务提交或回滚之前，并发控制用表的目标行会被锁定。
因此，其他事务的更新处理将等待直到锁被释放。

悲观锁使用 :java:extdoc:`ExclusiveControlUtil#updateVersion <nablarch.common.exclusivecontrol.ExclusiveControlUtil.updateVersion(nablarch.common.exclusivecontrol.ExclusiveControlContext)>` 。

.. code-block:: java

 ExclusiveControlUtil.updateVersion(new UsersExclusiveControl("U00001"));

.. important::
 在批处理中，设置仅获取用于锁定的主键的预处理，
 在本处理中逐个获取锁后再获取、更新数据。
 理由如下。

 * 防止从获取数据到更新之间数据被其他进程更新。
 * 尽量缩短锁定时间，减少对并行处理的影响。

扩展示例
---------------------------------------------------------------------
无。
