.. _web_front_controller:

Webフロントコントローラ
==================================================

.. contents:: 目录
  :depth: 3
  :local:

ウェブ应用におけるhandler队列の実行の起点となるクラス。

本クラスを使用することで、クライアントから受け取ったリクエストに対する処理をhandler队列に委譲できる。

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web</artifactId>
  </dependency>

handler队列を設定する
--------------------------------------------------
リクエストに対する処理をhandler队列に委譲するための手順を示す。

コンポーネント設定ファイルに設定する
  :java:extdoc:`WebFrontController <nablarch.fw.web.servlet.WebFrontController>` をコンポーネント設定ファイルに設定し、
  :java:extdoc:`handlerQueue <nablarch.fw.HandlerQueueManager.setHandlerQueue(java.util.Collection)>` プロパティに
  应用で使用するハンドラを順番に追加していく。

  コンポーネント設定ファイルの設定例を以下に示す。

  ポイント
   * コンポーネント名は **webFrontController** とすること。

  .. code-block:: xml

    <component name="webFrontController" class="nablarch.fw.web.servlet.WebFrontController">
      <property name="handlerQueue">
        <list>
          <component class="nablarch.fw.web.handler.HttpCharacterEncodingHandler"/>
          <component class="nablarch.fw.handler.GlobalErrorHandler"/>

          <!-- 省略 -->

        </list>
      </property>
    </component>

サーブレットフィルタを設定する
  :java:extdoc:`RepositoryBasedWebFrontController <nablarch.fw.web.servlet.RepositoryBasedWebFrontController>`
  をサーブレットフィルタとして `web.xml` に設定する。
  このフィルタによって、クライアントから受け取ったリクエストに対する処理は、先ほどSystem Repositoryに登録したhandler队列へ委譲される。

  `web.xml` への設定例を以下に示す。

  ポイント
   * System Repositoryを初期化するため、 :ref:`nablarch_servlet_context_listener` をリスナーとして設定すること。

  .. code-block:: xml

    <context-param>
      <param-name>di.config</param-name>
      <param-value>web-boot.xml</param-value>
    </context-param>

    <listener>
      <listener-class>nablarch.fw.web.servlet.NablarchServletContextListener</listener-class>
    </listener>

    <filter>
      <filter-name>entryPoint</filter-name>
      <filter-class>nablarch.fw.web.servlet.RepositoryBasedWebFrontController</filter-class>
    </filter>

    <filter-mapping>
      <filter-name>entryPoint</filter-name>
      <url-pattern>/action/*</url-pattern>
    </filter-mapping>

.. _change_web_front_controller_name:

委譲するWebフロントコントローラの名前を変更する
--------------------------------------------------

  ウェブ应用をベースとした应用において一部のリクエストをRESTfulウェブサービスとして処理したい場合など、
  ウェブ应用とウェブサービスを併用したい場合が考えられる。
  そのような場合は、ハンドラ構成の異なるWebフロントコントローラを複数個定義する必要がある。
  :java:extdoc:`RepositoryBasedWebFrontController <nablarch.fw.web.servlet.RepositoryBasedWebFrontController>` はデフォルトでは
  ``webFrontController`` という名前でSystem Repositoryが委譲するWebフロントコントローラを取得する。
  `web.xml` に初期化パラメータを設定することで、System Repositoryから取得するWebフロントコントローラの名前を変更することができる。

  ウェブ应用用とRESTfulウェブサービス用2つのハンドラ構成を持つWebフロントコントローラの設定例を以下に示す。

  まず、コンポーネント定義で、ウェブ应用用のハンドラ構成をもったWebフロントコントローラを ``webFrontController`` という名前で定義し、
  RESTfulウェブサービス用のハンドラ構成をもったWebフロントコントローラを ``webFrontController`` と異なるコンポーネント名で定義する。

  .. code-block:: xml

    <component name="webFrontController"
              class="nablarch.fw.web.servlet.WebFrontController">
      <property name="handlerQueue">
        <list>
          <!-- ウェブ应用用のハンドラ構成 -->
        </list>
      </property>
    </component>

    <component name="jaxrsController"
              class="nablarch.fw.web.servlet.WebFrontController">
      <property name="handlerQueue">
        <list>
          <!-- RESTfulウェブサービス用のハンドラ構成 -->
        </list>
      </property>
    </component>

  次に `web.xml` に上記で設定したWebフロントコントローラを使用するためのサーブレットフィルタを設定する。

  ポイント
   * ``<init-param>`` を使い ``controllerName`` というパラメータにSystem Repositoryから取得する際のコントローラ名を設定する。
   * ``<filter-mapping>`` でそれぞれのWebフロントコントローラが処理対象とするURLのパターンを設定する。

  .. code-block:: xml

    <context-param>
      <param-name>di.config</param-name>
      <param-value>web-boot.xml</param-value>
    </context-param>

    <listener>
      <listener-class>nablarch.fw.web.servlet.NablarchServletContextListener</listener-class>
    </listener>

    <filter>
      <filter-name>webEntryPoint</filter-name>
      <filter-class>nablarch.fw.web.servlet.RepositoryBasedWebFrontController</filter-class>
    </filter>
    <filter>
      <filter-name>jaxrsEntryPoint</filter-name>
      <filter-class>nablarch.fw.web.servlet.RepositoryBasedWebFrontController</filter-class>
      <init-param>
        <param-name>controllerName</param-name>
        <param-value>jaxrsController</param-value>
      </init-param>
    </filter>

    <filter-mapping>
      <filter-name>webEntryPoint</filter-name>
      <url-pattern>/action/*</url-pattern>
      <url-pattern>/</url-pattern>
    </filter-mapping>
    <filter-mapping>
      <filter-name>jaxrsEntryPoint</filter-name>
      <url-pattern>/api/*</url-pattern>
    </filter-mapping>

