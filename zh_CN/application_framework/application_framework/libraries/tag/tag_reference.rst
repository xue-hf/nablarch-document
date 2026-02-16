.. _tag_reference:

==================================================
标签参考
==================================================

| 本参考描述了Nablarch提供的标签及其属性。
| 关于各标签的使用方法和使用示例等详细信息，请参阅 :ref:`tag` 。

表单
 | :ref:`tag-form_tag` (表单)

.. _tag_reference_input:

输入
 | :ref:`tag-text_tag` (文本)
 | :ref:`tag-search_tag` (搜索文本)
 | :ref:`tag-tel_tag` (电话号码)
 | :ref:`tag-url_tag` (URL)
 | :ref:`tag-email_tag` (邮件地址)
 | :ref:`tag-date_tag` (日期)
 | :ref:`tag-month_tag` (月)
 | :ref:`tag-week_tag` (周)
 | :ref:`tag-time_tag` (时间)
 | :ref:`tag-datetimeLocal_tag` (本地日期时间)
 | :ref:`tag-number_tag` (数值)
 | :ref:`tag-range_tag` (范围)
 | :ref:`tag-color_tag` (颜色)
 | :ref:`tag-textarea_tag` (文本区域)
 | :ref:`tag-password_tag` (密码)
 | :ref:`tag-radio_tag` (单选按钮)
 | :ref:`tag-checkbox_tag` (复选框)
 | :ref:`tag-file_tag` (文件)
 | :ref:`tag-plain_hidden_tag` (hidden)
 | :ref:`tag-select_tag` (下拉框)
 | :ref:`tag-composite_key_radio_button_tag` (对应复合键的单选按钮)
 | :ref:`tag-composite_key_checkbox_tag` (对应复合键的复选框)
 | :ref:`tag-radio_buttons_tag` (多个单选按钮)
 | :ref:`tag-checkboxes_tag` (多个复选框)
 | :ref:`tag-code_select_tag` (代码值的下拉框)
 | :ref:`tag-code_checkbox_tag` (代码值的复选框)
 | :ref:`tag-code_radio_buttons_tag` (代码值的多个单选按钮)
 | :ref:`tag-code_checkboxes_tag` (代码值的多个复选框)
 | :ref:`tag-hidden_tag` (hidden加密)
 | :ref:`tag-hidden_store_tag` (HIDDEN存储)

.. _tag_reference_submit:

提交
 表单的提交
  | :ref:`tag-submit_tag` (input标签的按钮)
  | :ref:`tag-button_tag` (button标签的按钮)
  | :ref:`tag-submit_link_tag` (链接)

 打开别窗口提交(弹出窗口)
  | :ref:`tag-popup_submit_tag` (input标签的按钮)
  | :ref:`tag-popup_button_tag` (button标签的按钮)
  | :ref:`tag-popup_link_tag` (链接)

 用于下载的提交
  | :ref:`tag-download_submit_tag` (input标签的按钮)
  | :ref:`tag-download_button_tag` (button标签的按钮)
  | :ref:`tag-download_link_tag` (链接)

 提交控制
  | :ref:`tag-param_tag` (指定提交时添加的参数)
  | :ref:`tag-change_param_name_tag` (弹出窗口提交时更改参数名)

.. _tag_reference_output:

输出
 值
  | :ref:`tag-write_tag` (对象的值)
  | :ref:`tag-pretty_print_tag` (对象的值。仅不转义修饰系HTML(如b标签等))
  | :ref:`tag-raw_write_tag` (对象的值。不进行HTML转义)
  | :ref:`tag-code_tag` (代码值)
  | :ref:`tag-csp_nonce_tag` (Content Security Policy的nonce值)
 消息
  | :ref:`tag-message_tag` (消息)
 错误
  | :ref:`tag-errors_tag` (错误消息一览显示)
  | :ref:`tag-error_tag` (错误消息个别显示)

指定URI的HTML标签(添加上下文路径和URL重写)
 | :ref:`tag-a_tag`
 | :ref:`tag-img_tag`
 | :ref:`tag-link_tag`
 | :ref:`tag-script_tag`

工具
 | :ref:`tag-no_cache_tag` (抑制浏览器缓存)
 | :ref:`tag-set_tag` (设置变量值)
 | :ref:`tag-include_tag` (包含)
 | :ref:`tag-include_param_tag` (指定包含时添加的参数)
 | :ref:`tag-confirmation_page_tag` (输入画面和确认画面共用)
 | :ref:`tag-ignore_confirmation_tag` (部分禁用确认画面的画面状态)
 | :ref:`tag-for_input_page_tag` (仅输入画面输出body)
 | :ref:`tag-for_confirmation_page_tag` (仅确认画面输出body)

通用属性
========================
在各自定义标签定义中引用此处定义的通用属性。

.. _tag-generic_attributes_tag:

所有HTML标签
-------------------------

.. table::
   :class: tag-reference

   ============================= ==========================================================================================
   属性                          说明
   ============================= ==========================================================================================
   id                            XHTML的id属性。
   cssClass                      XHTML的class属性。
   style                         XHTML的style属性。
   title                         XHTML的title属性。
   lang                          XHTML的lang属性。
   xmlLang                       XHTML的xml:lang属性。
   dir                           XHTML的dir属性。
   onclick                       XHTML的onclick属性。
   ondblclick                    XHTML的ondblclick属性。
   onmousedown                   XHTML的onmousedown属性。
   onmouseup                     XHTML的onmouseup属性。
   onmouseover                   XHTML的onmouseover属性。
   onmousemove                   XHTML的onmousemove属性。
   onmouseout                    XHTML的onmouseout属性。
   onkeypress                    XHTML的onkeypress属性。
   onkeydown                     XHTML的onkeydown属性。
   onkeyup                       XHTML的onkeyup属性。
   ============================= ==========================================================================================

.. _tag-focus_attributes_tag:

可获取焦点的HTML标签
--------------------------------------------------

.. table::
   :class: tag-reference

   ============================= ==========================================================================================
   属性                          说明
   ============================= ==========================================================================================
   accesskey                     XHTML的accesskey属性。
   tabindex                      XHTML的tabindex属性。
   onfocus                       XHTML的onfocus属性。
   onblur                        XHTML的onblur属性。
   ============================= ==========================================================================================

.. _tag-dynamic_attributes_tag:

动态属性的使用
--------------------------------------------------

在可使用动态属性的标签中，也可以设置未定义的属性。

单独属性
======================================================

.. _tag-form_tag:

form标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference
      
   ====================================== ==========================================================================================
   属性                                     说明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`      
   name                                   XHTML的name属性。
   action                                 XHTML的action属性。
   method                                 XHTML的method属性。
                                          默认为 ``post`` 。
   enctype                                XHTML的enctype属性。
   onsubmit                               XHTML的onsubmit属性。
   onreset                                XHTML的onreset属性。
   accept                                 XHTML的accept属性。
   acceptCharset                          XHTML的accept-charset属性。
   target                                 XHTML的target属性。
   autocomplete                           HTML5的autocomplete属性。
   windowScopePrefixes                    窗口作用域变量的前缀。
                                          指定多个时用逗号分隔。
                                          将匹配指定前缀的请求参数作为hidden标签输出。
   useToken                               是否设置令牌。
                                          设置令牌时为 ``true`` ，不设置时为 ``false`` 。
                                          默认为 ``false`` 。
                                          指定 :ref:`tag-confirmation_page_tag` 时，默认为 ``true`` 。
   secure                                 URI是否改为https。
                                          改为https时为 ``true`` ，不改为 ``false`` 。
   preventPostResubmit                    是否使用POST重发防止功能。
                                          默认为 ``false`` 。
                                          使用时为 ``true`` ，不使用时为 ``false`` 。
   ====================================== ==========================================================================================

.. _tag-text_tag:

text标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference
      
   ====================================== ====================================================================================================================
   属性                                   说明
   ====================================== ====================================================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``必须``                          XHTML的name属性。显示值时，如未指定value属性，则也用于XHTML的value属性
   value                                  XHTML的value属性。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   readonly                               XHTML的readonly属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   size                                   XHTML的size属性。
   maxlength                              XHTML的maxlength属性。
   onselect                               XHTML的onselect属性。
   onchange                               XHTML的onchange属性。
   autocomplete                           HTML5的autocomplete属性。
   autofocus                              HTML5的autofocus属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   placeholder                            HTML5的placeholder属性。
   errorCss                               用于错误级别消息的CSS类名。
                                          默认为 ``nablarch_error`` 。
   nameAlias                              设置name属性的别名。
                                          指定多个时用逗号分隔。
   valueFormat                            输出时的格式。
                                          指定内容请参阅 :ref:`tag-format_value` 。
   ====================================== ====================================================================================================================

.. _tag-search_tag:

search标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference
      
   ====================================== ====================================================================================================================
   属性                                   说明
   ====================================== ====================================================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``必须``                          XHTML的name属性。显示值时，如未指定value属性，则也用于XHTML的value属性
   value                                  XHTML的value属性。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   autocomplete                           HTML5的autocomplete属性。
   autofocus                              HTML5的autofocus属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   errorCss                               用于错误级别消息的CSS类名。
                                          默认为 ``nablarch_error`` 。
   nameAlias                              设置name属性的别名。
                                          指定多个时用逗号分隔。
   valueFormat                            输出时的格式。
                                          指定内容请参阅 :ref:`tag-format_value` 。
   ====================================== ====================================================================================================================

.. _tag-tel_tag:

tel标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference
      
   ====================================== ====================================================================================================================
   属性                                   说明
   ====================================== ====================================================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``必须``                          XHTML的name属性。显示值时，如未指定value属性，则也用于XHTML的value属性
   value                                  XHTML的value属性。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   autocomplete                           HTML5的autocomplete属性。
   autofocus                              HTML5的autofocus属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   errorCss                               用于错误级别消息的CSS类名。
                                          默认为 ``nablarch_error`` 。
   nameAlias                              设置name属性的别名。
                                          指定多个时用逗号分隔。
   valueFormat                            输出时的格式。
                                          指定内容请参阅 :ref:`tag-format_value` 。
   ====================================== ====================================================================================================================

.. _tag-url_tag:

url标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference
      
   ====================================== ====================================================================================================================
   属性                                   说明
   ====================================== ====================================================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``必须``                          XHTML的name属性。显示值时，如未指定value属性，则也用于XHTML的value属性
   value                                  XHTML的value属性。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   autocomplete                           HTML5的autocomplete属性。
   autofocus                              HTML5的autofocus属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   errorCss                               用于错误级别消息的CSS类名。
                                          默认为 ``nablarch_error`` 。
   nameAlias                              设置name属性的别名。
                                          指定多个时用逗号分隔。
   valueFormat                            输出时的格式。
                                          指定内容请参阅 :ref:`tag-format_value` 。
   ====================================== ====================================================================================================================

.. _tag-email_tag:

email标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference
      
   ====================================== ====================================================================================================================
   属性                                   说明
   ====================================== ====================================================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``必须``                          XHTML的name属性。显示值时，如未指定value属性，则也用于XHTML的value属性
   value                                  XHTML的value属性。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   autocomplete                           HTML5的autocomplete属性。
   autofocus                              HTML5的autofocus属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   errorCss                               用于错误级别消息的CSS类名。
                                          默认为 ``nablarch_error`` 。
   nameAlias                              设置name属性的别名。
                                          指定多个时用逗号分隔。
   valueFormat                            输出时的格式。
                                          指定内容请参阅 :ref:`tag-format_value` 。
   ====================================== ====================================================================================================================

.. _tag-date_tag:

date标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference
      
   ====================================== ====================================================================================================================
   属性                                   说明
   ====================================== ====================================================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``必须``                          XHTML的name属性。显示值时，如未指定value属性，则也用于XHTML的value属性
   value                                  XHTML的value属性。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   autocomplete                           HTML5的autocomplete属性。
   autofocus                              HTML5的autofocus属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   errorCss                               用于错误级别消息的CSS类名。
                                          默认为 ``nablarch_error`` 。
   nameAlias                              设置name属性的别名。
                                          指定多个时用逗号分隔。
   valueFormat                            输出时的格式。
                                          指定内容请参阅 :ref:`tag-format_value` 。
   ====================================== ====================================================================================================================

.. _tag-month_tag:

month标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference
      
   ====================================== ====================================================================================================================
   属性                                   说明
   ====================================== ====================================================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``必须``                          XHTML的name属性。显示值时，如未指定value属性，则也用于XHTML的value属性
   value                                  XHTML的value属性。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   autocomplete                           HTML5的autocomplete属性。
   autofocus                              HTML5的autofocus属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   errorCss                               用于错误级别消息的CSS类名。
                                          默认为 ``nablarch_error`` 。
   nameAlias                              设置name属性的别名。
                                          指定多个时用逗号分隔。
   valueFormat                            输出时的格式。
                                          指定内容请参阅 :ref:`tag-format_value` 。
   ====================================== ====================================================================================================================

.. _tag-week_tag:

week标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference
      
   ====================================== ====================================================================================================================
   属性                                   说明
   ====================================== ====================================================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``必须``                          XHTML的name属性。显示值时，如未指定value属性，则也用于XHTML的value属性
   value                                  XHTML的value属性。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   autocomplete                           HTML5的autocomplete属性。
   autofocus                              HTML5的autofocus属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   errorCss                               用于错误级别消息的CSS类名。
                                          默认为 ``nablarch_error`` 。
   nameAlias                              设置name属性的别名。
                                          指定多个时用逗号分隔。
   valueFormat                            输出时的格式。
                                          指定内容请参阅 :ref:`tag-format_value` 。
   ====================================== ====================================================================================================================

.. _tag-time_tag:

time标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference
      
   ====================================== ====================================================================================================================
   属性                                   说明
   ====================================== ====================================================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``必须``                          XHTML的name属性。显示值时，如未指定value属性，则也用于XHTML的value属性
   value                                  XHTML的value属性。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   autocomplete                           HTML5的autocomplete属性。
   autofocus                              HTML5的autofocus属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   errorCss                               用于错误级别消息的CSS类名。
                                          默认为 ``nablarch_error`` 。
   nameAlias                              设置name属性的别名。
                                          指定多个时用逗号分隔。
   valueFormat                            输出时的格式。
                                          指定内容请参阅 :ref:`tag-format_value` 。
   ====================================== ====================================================================================================================

.. _tag-datetimeLocal_tag:

datetimeLocal标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference
      
   ====================================== ====================================================================================================================
   属性                                   说明
   ====================================== ====================================================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``必须``                          XHTML的name属性。显示值时，如未指定value属性，则也用于XHTML的value属性
   value                                  XHTML的value属性。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   autocomplete                           HTML5的autocomplete属性。
   autofocus                              HTML5的autofocus属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   errorCss                               用于错误级别消息的CSS类名。
                                          默认为 ``nablarch_error`` 。
   nameAlias                              设置name属性的别名。
                                          指定多个时用逗号分隔。
   valueFormat                            输出时的格式。
                                          指定内容请参阅 :ref:`tag-format_value` 。
   ====================================== ====================================================================================================================

.. _tag-number_tag:

number标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference
      
   ====================================== ====================================================================================================================
   属性                                   说明
   ====================================== ====================================================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``必须``                          XHTML的name属性。显示值时，如未指定value属性，则也用于XHTML的value属性
   value                                  XHTML的value属性。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   autocomplete                           HTML5的autocomplete属性。
   autofocus                              HTML5的autofocus属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   errorCss                               用于错误级别消息的CSS类名。
                                          默认为 ``nablarch_error`` 。
   nameAlias                              设置name属性的别名。
                                          指定多个时用逗号分隔。
   valueFormat                            输出时的格式。
                                          指定内容请参阅 :ref:`tag-format_value` 。
   ====================================== ====================================================================================================================

.. _tag-range_tag:

range标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference
      
   ====================================== ====================================================================================================================
   属性                                   说明
   ====================================== ====================================================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``必须``                          XHTML的name属性。显示值时，如未指定value属性，则也用于XHTML的value属性
   value                                  XHTML的value属性。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   autocomplete                           HTML5的autocomplete属性。
   autofocus                              HTML5的autofocus属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   errorCss                               用于错误级别消息的CSS类名。
                                          默认为 ``nablarch_error`` 。
   nameAlias                              设置name属性的别名。
                                          指定多个时用逗号分隔。
   valueFormat                            输出时的格式。
                                          指定内容请参阅 :ref:`tag-format_value` 。
   ====================================== ====================================================================================================================

.. _tag-color_tag:

color标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference
      
   ====================================== ====================================================================================================================
   属性                                   说明
   ====================================== ====================================================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``必须``                          XHTML的name属性。显示值时，如未指定value属性，则也用于XHTML的value属性
   value                                  XHTML的value属性。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   autocomplete                           HTML5的autocomplete属性。
   autofocus                              HTML5的autofocus属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   errorCss                               用于错误级别消息的CSS类名。
                                          默认为 ``nablarch_error`` 。
   nameAlias                              设置name属性的别名。
                                          指定多个时用逗号分隔。
   valueFormat                            输出时的格式。
                                          指定内容请参阅 :ref:`tag-format_value` 。
   ====================================== ====================================================================================================================

.. _tag-textarea_tag:

textarea标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference
         
   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``必须``                          XHTML的name属性。
   rows ``必须``                          XHTML的rows属性。
   cols ``必须``                          XHTML的cols属性。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   readonly                               XHTML的readonly属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   onselect                               XHTML的onselect属性。
   onchange                               XHTML的onchange属性。
   autofocus                              HTML5的autofocus属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   placeholder                            HTML5的placeholder属性。
   maxlength                              HTML5的maxlength属性。
   errorCss                               用于错误级别消息的CSS类名。
                                          默认为 ``nablarch_error`` 。
   nameAlias                              设置name属性的别名。
                                          指定多个时用逗号分隔。
   ====================================== ==========================================================================================

.. _tag-password_tag:

password标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference
            
   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``必须``                          XHTML的name属性。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   readonly                               XHTML的readonly属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   size                                   XHTML的size属性。
   maxlength                              XHTML的maxlength属性。
   onselect                               XHTML的onselect属性。
   onchange                               XHTML的onchange属性。
   autocomplete                           HTML5的autocomplete属性。
   autofocus                              HTML5的autofocus属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   placeholder                            HTML5的placeholder属性。
   restoreValue                           输入画面重新显示时是否恢复输入数据。
                                          恢复时为 ``true`` ，不恢复时为 ``false`` 。
                                          默认为 ``false`` 。
   replacement                            确认画面用输出时的替换字符。
                                          默认为 ``*`` 。
   errorCss                               用于错误级别消息的CSS类名。
                                          默认为 ``nablarch_error`` 。
   nameAlias                              设置name属性的别名。
                                          指定多个时用逗号分隔。
   ====================================== ==========================================================================================

.. _tag-radio_tag:

radioButton标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`
   :ref:`tag-focus_attributes_tag`
   name ``必须``                          XHTML的name属性。
   value ``必须``                         XHTML的value属性。
   label ``必须``                         标签。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   onchange                               XHTML的onchange属性。
   autofocus                              HTML5的autofocus属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   errorCss                               用于错误级别消息的CSS类名。
                                          默认为 ``nablarch_error`` 。
   nameAlias                              设置name属性的别名。
                                          指定多个时用逗号分隔。
   ====================================== ==========================================================================================

.. _tag-checkbox_tag:

checkbox标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``必须``                          XHTML的name属性。
   value                                  XHTML的value属性。
                                          选中时使用的值。
                                          默认为 ``1`` 。
   autofocus                              HTML5的autofocus属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   label                                  选中时使用的标签。
                                          在输入画面中显示此标签。
   useOffValue                            是否使用未选中时的值设置。
                                          默认为 ``true`` 。
   offLabel                               未选中时使用的标签。
   offValue                               未选中时使用的值。
                                          默认为 ``0`` 。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   onchange                               XHTML的onchange属性。
   errorCss                               用于错误级别消息的CSS类名。
                                          默认为 ``nablarch_error`` 。
   nameAlias                              设置name属性的别名。
                                          指定多个时用逗号分隔。
   ====================================== ==========================================================================================
 
.. _tag-composite_key_checkbox_tag:

compositeKeyCheckbox标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``必须``                          XHTML的name属性。
   valueObject ``必须``                   代替XHTML的value属性使用的对象。
                                          需要具有keyNames属性指定的属性。
   keyNames ``必须``                      复合键的键名。
                                          以逗号分隔指定键名。
   namePrefix ``必须``                    展开到请求参数时使用的前缀。
                                          与通常的name属性不同，将与此名称和\
                                          keyNames属性指定的键名匹配的值与通常的name属性一样处理。
                                          例如在namePrefix属性中指定 ``form`` 、keyNames属性中指定 ``key1`` 、 ``key2`` 时，\
                                          显示时使用 ``form.key1`` 、 ``form.key2`` \
                                          中包含的值输出此复选框的值。
                                          此外，在提交请求的处理中，\
                                          可从 ``form.key1`` 、 ``form.key2`` 这一请求参数中获取选中的值。
                                          另外，name属性有一个特殊约束，必须与namePrefix属性和keyNames属性指定的\
                                          键组合使用不同的名称。\
                                          实现时请充分注意这一点。
   autofocus                              HTML5的autofocus属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   label                                  选中时使用的标签。
                                          在输入画面中显示此标签。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   onchange                               XHTML的onchange属性。
   errorCss                               用于错误级别消息的CSS类名。
                                          默认为 ``nablarch_error`` 。
   nameAlias                              设置name属性的别名。
                                          指定多个时用逗号分隔。
   ====================================== ==========================================================================================

.. _tag-composite_key_radio_button_tag:

compositeKeyRadioButton标签
---------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``必须``                          XHTML的name属性。
   valueObject ``必须``                   代替XHTML的value属性使用的对象。
                                          需要具有keyNames属性指定的属性。
   keyNames ``必须``                      复合键的键名。
                                          以逗号分隔指定键名。
   namePrefix ``必须``                    展开到请求参数时使用的前缀。
                                          与通常的name属性不同，将与此名称和\
                                          keyNames属性指定的键名匹配的值与通常的name属性一样处理。
                                          例如在namePrefix属性中指定 ``form`` 、keyNames属性中指定 ``key1`` 、 ``key2`` 时，\
                                          显示时使用 ``form.key1`` 、 ``form.key2`` \
                                          中包含的值输出此复选框的值。
                                          此外，在提交请求的处理中，\
                                          可从 ``form.key1`` 、 ``form.key2`` 这一请求参数中获取选中的值。
                                          另外，name属性有一个特殊约束，必须与namePrefix属性和keyNames属性指定的\
                                          键组合使用不同的名称。\
                                          实现时请充分注意这一点。
   autofocus                              HTML5的autofocus属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   label                                  选中时使用的标签。
                                          在输入画面中显示此标签。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   onchange                               XHTML的onchange属性。
   errorCss                               用于错误级别消息的CSS类名。
                                          默认为 ``nablarch_error`` 。
   nameAlias                              设置name属性的别名。
                                          指定多个时用逗号分隔。
   ====================================== ==========================================================================================

.. _tag-file_tag:

file标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``必须``                          XHTML的name属性。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   readonly                               XHTML的readonly属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   size                                   XHTML的size属性。
   maxlength                              XHTML的maxlength属性。
   onselect                               XHTML的onselect属性。
   onchange                               XHTML的onchange属性。
   accept                                 XHTML的accept属性。
   autofocus                              HTML5的autofocus属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   multiple                               HTML5的multiple属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   errorCss                               用于错误级别消息的CSS类名。
                                          默认为 ``nablarch_error`` 。
   nameAlias                              设置name属性的别名。
                                          指定多个时用逗号分隔。
   ====================================== ==========================================================================================

.. _tag-hidden_tag:

hidden标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

不输出HTML标签，而将值输出到窗口作用域。

.. important::

  窗口作用域已弃用。
  详情请参阅 :ref:`tag-window_scope` 。

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``必须``                          XHTML的name属性。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   ====================================== ==========================================================================================

.. _tag-plain_hidden_tag:

plainHidden标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``必须``                          XHTML的name属性。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   ====================================== ==========================================================================================

.. _tag-hidden_store_tag:

hiddenStore标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`
   :ref:`tag-focus_attributes_tag`
   name ``必须``                          XHTML的name属性。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   ====================================== ==========================================================================================

.. _tag-select_tag:

select标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference

   ====================================== ======================================================================================================================
   属性                                   说明
   ====================================== ======================================================================================================================
   :ref:`tag-generic_attributes_tag`    
   name ``必须``                          XHTML的name属性。
   listName ``必须``                      选项列表的名称。
                                          自定义标签使用此名称从请求作用域获取选项列表。
                                          如从请求作用域获取的选项列表为空，则画面中不显示任何内容。
   elementLabelProperty ``必须``          从列表元素获取标签的属性名。
   elementValueProperty ``必须``          从列表元素获取值的属性名。
   size                                   XHTML的size属性。
   multiple                               XHTML的multiple属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   tabindex                               XHTML的tabindex属性。
   onfocus                                XHTML的onfocus属性。
   onblur                                 XHTML的onblur属性。
   onchange                               XHTML的onchange属性。
   autofocus                              HTML5的autofocus属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   elementLabelPattern                    用于格式化标签的模式。
                                          占位符如下所示。
                                          ``$LABEL$`` : 标签
                                          ``$VALUE$`` : 值
                                          默认为 ``$LABEL$`` 。
   listFormat                             列表显示时使用的格式。
                                          指定以下之一。
                                          br(br标签)
                                          div(div标签)
                                          span(span标签)
                                          ul(ul标签)
                                          ol(ol标签)
                                          sp(空格分隔)
                                          默认为br。
   withNoneOption                         是否在列表开头添加"未选择"选项。
                                          添加时为 ``true`` ，不添加时为 ``false`` 。
                                          默认为 ``false`` 。
   noneOptionLabel                        在列表开头添加"未选择"选项时使用的标签。
                                          此属性仅在withNoneOption指定为 ``true`` 时有效。
                                          默认为 ``""``。
   errorCss                               用于错误级别消息的CSS类名。
                                          默认为 ``nablarch_error`` 。
   nameAlias                              设置name属性的别名。
                                          指定多个时用逗号分隔。
   ====================================== ======================================================================================================================

.. _tag-radio_buttons_tag:

radioButtons标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference

   ====================================== ======================================================================================================================
   属性                                   说明
   ====================================== ======================================================================================================================
   :ref:`tag-generic_attributes_tag`      id属性不能指定。
   :ref:`tag-focus_attributes_tag`        accesskey属性不能指定。
   name ``必须``                          XHTML的name属性。
   listName ``必须``                      选项列表的名称。
                                          自定义标签使用此名称从请求作用域获取选项列表。
                                          如从请求作用域获取的选项列表为空，则画面中不显示任何内容。
   elementLabelProperty ``必须``          从列表元素获取标签的属性名。
   elementValueProperty ``必须``          从列表元素获取值的属性名。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   onchange                               XHTML的onchange属性。
   autofocus                              HTML5的autofocus属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
                                          仅在选项中的第一个元素输出autofocus属性。
   elementLabelPattern                    用于格式化标签的模式。
                                          占位符如下所示。
                                          ``$LABEL$`` : 标签
                                          ``$VALUE$`` : 值
                                          默认为 ``$LABEL$`` 。
   listFormat                             列表显示时使用的格式。
                                          指定以下之一。
                                          br(br标签)
                                          div(div标签)
                                          span(span标签)
                                          ul(ul标签)
                                          ol(ol标签)
                                          sp(空格分隔)
                                          默认为br。
   errorCss                               用于错误级别消息的CSS类名。
                                          默认为 ``nablarch_error`` 。
   nameAlias                              设置name属性的别名。
                                          指定多个时用逗号分隔。
   ====================================== ======================================================================================================================

.. _tag-checkboxes_tag:

checkboxes标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`      id属性不能指定。
   :ref:`tag-focus_attributes_tag`        accesskey属性不能指定。
   name ``必须``                          XHTML的name属性。
   listName ``必须``                      选项列表的名称。
                                          自定义标签使用此名称从请求作用域获取选项列表。
                                          如从请求作用域获取的选项列表为空，则画面中不显示任何内容。
   elementLabelProperty ``必须``          从列表元素获取标签的属性名。
   elementValueProperty ``必须``          从列表元素获取值的属性名。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   onchange                               XHTML的onchange属性。
   autofocus                              HTML5的autofocus属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
                                          仅在选项中的第一个元素输出autofocus属性。
   elementLabelPattern                    用于格式化标签的模式。
                                          占位符如下所示。
                                          ``$LABEL$`` : 标签
                                          ``$VALUE$`` : 值
                                          默认为 ``$LABEL$`` 。
   listFormat                             列表显示时使用的格式。
                                          指定以下之一。
                                          br(br标签)
                                          div(div标签)
                                          span(span标签)
                                          ul(ul标签)
                                          ol(ol标签)
                                          sp(空格分隔)
                                          默认为br。
   errorCss                               用于错误级别消息的CSS类名。
                                          默认为 ``nablarch_error`` 。
   nameAlias                              设置name属性的别名。
                                          指定多个时用逗号分隔。
   ====================================== ==========================================================================================

.. _tag-submit_tag:

submit标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name                                   XHTML的name属性。
   type ``必须``                          XHTML的type属性。
   uri ``必须``                           URI。
                                          请参阅 :ref:`tag-specify_uri` 。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   value                                  XHTML的value属性。
   src                                    XHTML的src属性。
   alt                                    XHTML的alt属性。
   usemap                                 XHTML的usemap属性。
   align                                  XHTML的align属性。
   autofocus                              HTML5的autofocus属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   allowDoubleSubmission                  是否允许双重提交。
                                          允许时为 ``true`` ，不允许时为 ``false`` 。
                                          默认为 ``true`` 。
   secure                                 URI是否改为https。
                                          改为https时为 ``true`` ，不改为 ``false`` 。
   displayMethod                          根据授权判断和服务提供可否判断的结果进行显示控制时的显示方法。
                                          指定以下之一。
                                          NODISPLAY (不显示)
                                          DISABLED (禁用)
                                          NORMAL (正常显示)
   suppressDefaultSubmit                  是否抑制在onclick属性中设置默认生成的提交用函数调用。
                                          抑制时为 ``true`` ，不抑制时为 ``false`` 。
                                          默认为 ``false`` 。
   ====================================== ==========================================================================================

.. _tag-button_tag:

button标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name                                   XHTML的name属性。
   uri ``必须``                           URI。
                                          请参阅 :ref:`tag-specify_uri` 。
   value                                  XHTML的value属性。
   type                                   XHTML的type属性。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   autofocus                              HTML5的autofocus属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   allowDoubleSubmission                  是否允许双重提交。
                                          允许时为 ``true`` ，不允许时为 ``false`` 。
                                          默认为 ``true`` 。
   secure                                 URI是否改为https。
                                          改为https时为 ``true`` ，不改为 ``false`` 。
   displayMethod                          根据授权判断和服务提供可否判断的结果进行显示控制时的显示方法。
                                          指定以下之一。
                                          NODISPLAY (不显示)
                                          DISABLED (禁用)
                                          NORMAL (正常显示)
   suppressDefaultSubmit                  是否抑制在onclick属性中设置默认生成的提交用函数调用。
                                          抑制时为 ``true`` ，不抑制时为 ``false`` 。
                                          默认为 ``false`` 。
   ====================================== ==========================================================================================

.. _tag-submit_link_tag:

submitLink标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name                                   XHTML的name属性。
   uri ``必须``                           URI。
                                          请参阅 :ref:`tag-specify_uri` 。
   shape                                  XHTML的shape属性。
   coords                                 XHTML的coords属性。
   allowDoubleSubmission                  是否允许双重提交。
                                          允许时为 ``true`` ，不允许时为 ``false`` 。
                                          默认为 ``true`` 。
   secure                                 URI是否改为https。
                                          改为https时为 ``true`` ，不改为 ``false`` 。
   displayMethod                          根据授权判断和服务提供可否判断的结果进行显示控制时的显示方法。
                                          指定以下之一。
                                          NODISPLAY (不显示)
                                          DISABLED (禁用)
                                          NORMAL (正常显示)
   suppressDefaultSubmit                  是否抑制在onclick属性中设置默认生成的提交用函数调用。
                                          抑制时为 ``true`` ，不抑制时为 ``false`` 。
                                          默认为 ``false`` 。
   ====================================== ==========================================================================================

.. _tag-popup_submit_tag:

popupSubmit标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name                                   XHTML的name属性。
   type ``必须``                          XHTML的type属性。
   uri ``必须``                           URI。
                                          请参阅 :ref:`tag-specify_uri` 。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   value                                  XHTML的value属性。
   src                                    XHTML的src属性。
   alt                                    XHTML的alt属性。
   usemap                                 XHTML的usemap属性。
   align                                  XHTML的align属性。
   autofocus                              HTML5的autofocus属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   secure                                 URI是否改为https。
                                          改为https时为 ``true`` ，不改为 ``false`` 。
   popupWindowName                        弹出窗口的窗口名称。
                                          打开新窗口时指定为window.open函数的第2个参数(JavaScript)。
   popupOption                            弹出窗口的选项信息。
                                          打开新窗口时指定为window.open函数的第3个参数(JavaScript)。
   displayMethod                          根据授权判断和服务提供可否判断的结果进行显示控制时的显示方法。
                                          指定以下之一。
                                          NODISPLAY (不显示)
                                          DISABLED (禁用)
                                          NORMAL (正常显示)
   suppressDefaultSubmit                  是否抑制在onclick属性中设置默认生成的提交用函数调用。
                                          抑制时为 ``true`` ，不抑制时为 ``false`` 。
                                          默认为 ``false`` 。
   ====================================== ==========================================================================================

.. _tag-popup_button_tag:

popupButton标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name                                   XHTML的name属性。
   uri ``必须``                           URI。
                                          请参阅 :ref:`tag-specify_uri` 。
   value                                  XHTML的value属性。
   type                                   XHTML的type属性。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   autofocus                              HTML5的autofocus属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   secure                                 URI是否改为https。
                                          改为https时为 ``true`` ，不改为 ``false`` 。
   popupWindowName                        弹出窗口的窗口名称。
                                          打开新窗口时指定为window.open函数的第2个参数(JavaScript)。
   popupOption                            弹出窗口的选项信息。
                                          打开新窗口时指定为window.open函数的第3个参数(JavaScript)。
   displayMethod                          根据授权判断和服务提供可否判断的结果进行显示控制时的显示方法。
                                          指定以下之一。
                                          NODISPLAY (不显示)
                                          DISABLED (禁用)
                                          NORMAL (正常显示)
   suppressDefaultSubmit                  是否抑制在onclick属性中设置默认生成的提交用函数调用。
                                          抑制时为 ``true`` ，不抑制时为 ``false`` 。
                                          默认为 ``false`` 。
   ====================================== ==========================================================================================

.. _tag-popup_link_tag:

popupLink标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name                                   XHTML的name属性。
   uri ``必须``                           URI。
                                          请参阅 :ref:`tag-specify_uri` 。
   shape                                  XHTML的shape属性。
   coords                                 XHTML的coords属性。
   secure                                 URI是否改为https。
                                          改为https时为 ``true`` ，不改为 ``false`` 。
   popupWindowName                        弹出窗口的窗口名称。
                                          打开新窗口时指定为window.open函数的第2个参数(JavaScript)。
   popupOption                            弹出窗口的选项信息。
                                          打开新窗口时指定为window.open函数的第3个参数(JavaScript)。
   displayMethod                          根据授权判断和服务提供可否判断的结果进行显示控制时的显示方法。
                                          指定以下之一。
                                          NODISPLAY (不显示)
                                          DISABLED (禁用)
                                          NORMAL (正常显示)
   suppressDefaultSubmit                  是否抑制在onclick属性中设置默认生成的提交用函数调用。
                                          抑制时为 ``true`` ，不抑制时为 ``false`` 。
                                          默认为 ``false`` 。
   ====================================== ==========================================================================================

.. _tag-download_submit_tag:

downloadSubmit标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name                                   XHTML的name属性。
   type ``必须``                          XHTML的type属性。
   uri ``必须``                           URI。
                                          请参阅 :ref:`tag-specify_uri` 。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   value                                  XHTML的value属性。
   src                                    XHTML的src属性。
   alt                                    XHTML的alt属性。
   usemap                                 XHTML的usemap属性。
   align                                  XHTML的align属性。
   autofocus                              HTML5的autofocus属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   allowDoubleSubmission                  是否允许双重提交。
                                          允许时为 ``true`` ，不允许时为 ``false`` 。
                                          默认为 ``true`` 。
   secure                                 URI是否改为https。
                                          改为https时为 ``true`` ，不改为 ``false`` 。
   displayMethod                          根据授权判断和服务提供可否判断的结果进行显示控制时的显示方法。
                                          指定以下之一。
                                          NODISPLAY (不显示)
                                          DISABLED (禁用)
                                          NORMAL (正常显示)
   suppressDefaultSubmit                  是否抑制在onclick属性中设置默认生成的提交用函数调用。
                                          抑制时为 ``true`` ，不抑制时为 ``false`` 。
                                          默认为 ``false`` 。
   ====================================== ==========================================================================================

.. _tag-download_button_tag:

downloadButton标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name                                   XHTML的name属性。
   uri ``必须``                           URI。
                                          请参阅 :ref:`tag-specify_uri` 。
   value                                  XHTML的value属性。
   type                                   XHTML的type属性。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   autofocus                              HTML5的autofocus属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   allowDoubleSubmission                  是否允许双重提交。
                                          允许时为 ``true`` ，不允许时为 ``false`` 。
                                          默认为 ``true`` 。
   secure                                 URI是否改为https。
                                          改为https时为 ``true`` ，不改为 ``false`` 。
   displayMethod                          根据授权判断和服务提供可否判断的结果进行显示控制时的显示方法。
                                          指定以下之一。
                                          NODISPLAY (不显示)
                                          DISABLED (禁用)
                                          NORMAL (正常显示)
   suppressDefaultSubmit                  是否抑制在onclick属性中设置默认生成的提交用函数调用。
                                          抑制时为 ``true`` ，不抑制时为 ``false`` 。
                                          默认为 ``false`` 。
   ====================================== ==========================================================================================

.. _tag-download_link_tag:

downloadLink标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name                                   XHTML的name属性。
   uri ``必须``                           URI。
                                          请参阅 :ref:`tag-specify_uri` 。
   shape                                  XHTML的shape属性。
   coords                                 XHTML的coords属性。
   allowDoubleSubmission                  是否允许双重提交。
                                          允许时为 ``true`` ，不允许时为 ``false`` 。
                                          默认为 ``true`` 。
   secure                                 URI是否改为https。
                                          改为https时为 ``true`` ，不改为 ``false`` 。
   displayMethod                          根据授权判断和服务提供可否判断的结果进行显示控制时的显示方法。
                                          指定以下之一。
                                          NODISPLAY (不显示)
                                          DISABLED (禁用)
                                          NORMAL (正常显示)
   suppressDefaultSubmit                  是否抑制在onclick属性中设置默认生成的提交用函数调用。
                                          抑制时为 ``true`` ，不抑制时为 ``false`` 。
                                          默认为 ``false`` 。
   ====================================== ==========================================================================================

.. _tag-param_tag:

param标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：否

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   paramName ``必须``                     提交时使用的参数名称。
   name                                   用于获取值的名称。
                                          引用请求作用域等作用域上的对象时指定。
                                          指定name属性或value属性之一。
   value                                  值。
                                          用于直接指定值。
                                          指定name属性或value属性之一。
   ====================================== ==========================================================================================

.. _tag-change_param_name_tag:

changeParamName标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：否

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   paramName ``必须``                     提交时使用的参数名称。
   inputName ``必须``                     作为更改来源的原画面的input元素的name属性。
   ====================================== ==========================================================================================

.. _tag-a_tag:

a标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   charset                                XHTML的charset属性。
   type                                   XHTML的type属性。
   name                                   XHTML的name属性。
   href                                   XHTML的href属性。
                                          请参阅 :ref:`tag-specify_uri` 。
   hreflang                               XHTML的hreflang属性。
   rel                                    XHTML的rel属性。
   rev                                    XHTML的rev属性。
   shape                                  XHTML的shape属性。
   coords                                 XHTML的coords属性。
   target                                 XHTML的target属性。
   secure                                 URI是否改为https。
                                          改为https时为 ``true`` ，不改为 ``false`` 。
   ====================================== ==========================================================================================

.. _tag-img_tag:

img标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   src ``必须``                           XHTML的charsrc属性。
                                          请参阅 :ref:`tag-specify_uri` 。
   alt ``必须``                           XHTML的alt属性。
   name                                   XHTML的name属性。
   longdesc                               XHTML的longdesc属性。
   height                                 XHTML的height属性。
   width                                  XHTML的width属性。
   usemap                                 XHTML的usemap属性。
   ismap                                  XHTML的ismap属性。
   align                                  XHTML的align属性。
   border                                 XHTML的border属性。
   hspace                                 XHTML的hspace属性。
   vspace                                 XHTML的vspace属性。
   secure                                 URI是否改为https。
                                          改为https时为 ``true`` ，不改为 ``false`` 。
   ====================================== ==========================================================================================

.. _tag-link_tag:

link标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   charset                                XHTML的charset属性。
   href                                   XHTML的href属性。
                                          请参阅 :ref:`tag-specify_uri` 。
   hreflang                               XHTML的hreflang属性。
   type                                   XHTML的type属性。
   rel                                    XHTML的rel属性。
   rev                                    XHTML的rev属性。
   media                                  XHTML的media属性。
   target                                 XHTML的target属性。
   secure                                 URI是否改为https。
                                          改为https时为 ``true`` ，不改为 ``false`` 。
   ====================================== ==========================================================================================

.. _tag-script_tag:

script标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   type ``必须``                          XHTML的type属性。
   id                                     XHTML的id属性。
   charset                                XHTML的charset属性。
   language                               XHTML的language属性。
   src                                    XHTML的src属性。
                                          请参阅 :ref:`tag-specify_uri` 。
   defer                                  XHTML的defer属性。
   xmlSpace                               XHTML的xml:space属性。
   secure                                 URI是否改为https。
                                          改为https时为 ``true`` ，不改为 ``false`` 。
   ====================================== ==========================================================================================

.. _tag-errors_tag:

errors标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：否

.. table::
   :class: tag-reference

   ====================================== =================================================================================================
   属性                                   说明
   ====================================== =================================================================================================
   cssClass                               列表显示中ul标签使用的CSS类名。
                                          默认为 ``nablarch_errors`` 。
   infoCss                                用于信息级别消息的CSS类名。
                                          默认为 ``nablarch_info`` 。
   warnCss                                用于警告级别消息的CSS类名。
                                          默认为 ``nablarch_warn`` 。
   errorCss                               用于错误级别消息的CSS类名。
                                          默认为 ``nablarch_error`` 。
   filter                                 列表中包含的消息的过滤条件。
                                          指定以下之一。
                                          all(显示所有消息)
                                          global(仅显示与输入项目不对应的消息)
                                          默认为 ``all`` 。
                                          指定global时，\
                                          去除包含 :java:extdoc:`ValidationResultMessage<nablarch.core.validation.ValidationResultMessage>`\
                                          属性名的消息后输出。
   ====================================== =================================================================================================

.. _tag-error_tag:

error标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：否

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   name ``必须``                          显示错误消息的输入项目的name属性。
   errorCss                               用于错误级别消息的CSS类名。
                                          默认为 ``nablarch_error`` 。
   messageFormat                          消息显示时使用的格式。
                                          指定以下之一。
                                          div(div标签)
                                          span(span标签)
                                          默认为div。
   ====================================== ==========================================================================================

.. _tag-no_cache_tag:

noCache标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：否

无属性。

.. _tag-code_select_tag:

codeSelect标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   name ``必须``                          XHTML的name属性。
   codeId ``必须``                        代码ID。
   size                                   XHTML的size属性。
   multiple                               XHTML的multiple属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   tabindex                               XHTML的tabindex属性。
   onfocus                                XHTML的onfocus属性。
   onblur                                 XHTML的onblur属性。
   onchange                               XHTML的onchange属性。
   autofocus                              HTML5的autofocus属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   pattern                                使用的模式的列名。
                                          默认为未指定。
   optionColumnName                       获取的选项名称的列名。
   labelPattern                           格式化标签的模式。
                                          占位符如下所示。
                                          ``$NAME$`` : 对应代码值的代码名称
                                          ``$SHORTNAME$`` : 对应代码值的代码的简称
                                          ``$OPTIONALNAME$`` : 对应代码值的代码的选项名称
                                          ``$VALUE$``: 代码值
                                          使用 ``$OPTIONALNAME$`` 时必须指定optionColumnName属性。
                                          默认为 ``$NAME$`` 。
   listFormat                             列表显示时使用的格式。
                                          指定以下之一。
                                          br(br标签)
                                          div(div标签)
                                          span(span标签)
                                          ul(ul标签)
                                          ol(ol标签)
                                          sp(空格分隔)
                                          默认为br。
   withNoneOption                         是否在列表开头添加"未选择"选项。
                                          添加时为 ``true`` ，不添加时为 ``false`` 。
                                          默认为 ``false`` 。
   noneOptionLabel                        在列表开头添加"未选择"选项时使用的标签。
                                          此属性仅在withNoneOption指定为 ``true`` 时有效。
                                          默认为 ``""`` 。
   errorCss                               用于错误级别消息的CSS类名。
                                          默认为 ``nablarch_error`` 。
   nameAlias                              设置name属性的别名。
                                          指定多个时用逗号分隔。
   ====================================== ==========================================================================================


.. _tag-code_radio_buttons_tag:

codeRadioButtons标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`      id属性不能指定。
   :ref:`tag-focus_attributes_tag`        accesskey属性不能指定。
   name ``必须``                          XHTML的name属性。
   codeId ``必须``                        代码ID。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   onchange                               XHTML的onchange属性。
   autofocus                              HTML5的autofocus属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
                                          仅在选项中的第一个元素输出autofocus属性。
   pattern                                使用的模式的列名。
                                          默认为未指定。
   optionColumnName                       获取的选项名称的列名。
   labelPattern                           格式化标签的模式。
                                          占位符如下所示。
                                          ``$NAME$`` : 对应代码值的代码名称
                                          ``$SHORTNAME$`` : 对应代码值的代码的简称
                                          ``$OPTIONALNAME$`` : 对应代码值的代码的选项名称
                                          ``$VALUE$``: 代码值
                                          使用 ``$OPTIONALNAME$`` 时必须指定optionColumnName属性。
                                          默认为 ``$NAME$`` 。
   listFormat                             列表显示时使用的格式。
                                          指定以下之一。 
                                          br(br标签)
                                          div(div标签)
                                          span(span标签)
                                          ul(ul标签)
                                          ol(ol标签)
                                          sp(空格分隔) 
                                          默认为br。
   errorCss                               用于错误级别消息的CSS类名。
                                          默认为 ``nablarch_error`` 。
   nameAlias                              设置name属性的别名。
                                          指定多个时用逗号分隔。
   ====================================== ==========================================================================================

.. _tag-code_checkboxes_tag:

codeCheckboxes标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`      id属性不能指定。
   :ref:`tag-focus_attributes_tag`        accesskey属性不能指定。
   name ``必须``                          XHTML的name属性。
   codeId ``必须``                        代码ID。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   onchange                               XHTML的onchange属性。
   autofocus                              HTML5的autofocus属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
                                          仅在选项中的第一个元素输出autofocus属性。
   pattern                                使用的模式的列名。
                                          默认为未指定。
   optionColumnName                       获取的选项名称的列名。
   labelPattern                           格式化标签的模式。
                                          占位符如下所示。
                                          ``$NAME$`` : 对应代码值的代码名称
                                          ``$SHORTNAME$`` : 对应代码值的代码的简称
                                          ``$OPTIONALNAME$`` : 对应代码值的代码的选项名称
                                          ``$VALUE$``: 代码值
                                          使用 ``$OPTIONALNAME$`` 时必须指定optionColumnName属性。
                                          默认为 ``$NAME$`` 。
   listFormat                             列表显示时使用的格式。
                                          指定以下之一。 
                                          br(br标签)
                                          div(div标签)
                                          span(span标签)
                                          ul(ul标签)
                                          ol(ol标签)
                                          sp(空格分隔) 
                                          默认为br。
   errorCss                               用于错误级别消息的CSS类名。
                                          默认为 ``nablarch_error`` 。
   nameAlias                              设置name属性的别名。
                                          指定多个时用逗号分隔。
   ====================================== ==========================================================================================

.. _tag-code_checkbox_tag:

codeCheckbox标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``必须``                          XHTML的name属性。
   value                                  XHTML的value属性。
                                          选中时使用的代码值。
                                          默认为 ``1`` 。
   autofocus                              HTML5的autofocus属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   codeId ``必须``                        代码ID。
   optionColumnName                       获取的选项名称的列名。
   labelPattern                           格式化标签的模式。
                                          占位符如下所示。
                                          ``$NAME$`` : 对应代码值的代码名称
                                          ``$SHORTNAME$`` : 对应代码值的代码的简称
                                          ``$OPTIONALNAME$`` : 对应代码值的代码的选项名称
                                          ``$VALUE$``: 代码值
                                          使用 ``$OPTIONALNAME$`` 时必须指定optionColumnName属性。
                                          默认为 ``$NAME$`` 。
   offCodeValue                           未选中时使用的代码值。
                                          如未指定offCodeValue属性，
                                          从codeId属性的值中搜索未选中时使用的代码值。
                                          搜索结果为2件且1件为value属性的值时，
                                          将剩余的1件作为未选中的代码值使用。
                                          搜索未找到时，使用默认值 ``0`` 。
   disabled                               XHTML的disabled属性 (:ref:`逻辑属性 <boolean_attribute>`) 。
   onchange                               XHTML的onchange属性。
   errorCss                               用于错误级别消息的CSS类名。
                                          默认为 ``nablarch_error`` 。
   nameAlias                              设置name属性的别名。
                                          指定多个时用逗号分隔。
   ====================================== ==========================================================================================

.. _tag-code_tag:

code标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：可

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   name                                   从变量作用域获取显示目标的代码值时使用的名称
                                          省略时，显示按代码ID属性和pattern属性筛选的代码列表。
   codeId ``必须``                        代码ID。
   pattern                                使用的模式的列名。
                                          默认为未指定。
   optionColumnName                       获取的选项名称的列名。
   labelPattern                           格式化标签的模式。
                                          占位符如下所示。
                                          ``$NAME$`` : 对应代码值的代码名称
                                          ``$SHORTNAME$`` : 对应代码值的代码的简称
                                          ``$OPTIONALNAME$`` : 对应代码值的代码的选项名称
                                          ``$VALUE$``: 代码值
                                          使用 ``$OPTIONALNAME$`` 时必须指定optionColumnName属性。
                                          默认为 ``$NAME$`` 。
   listFormat                             列表显示时使用的格式。
                                          指定以下之一。 
                                          br(br标签)
                                          div(div标签)
                                          span(span标签)
                                          ul(ul标签)
                                          ol(ol标签)
                                          sp(空格分隔) 
                                          默认为br。
   ====================================== ==========================================================================================

.. _tag-csp_nonce_tag:

cspNonce标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：否

进行 :ref:`在安全处理程序中生成nonce的设置<content_security_policy>` 时，输出生成的nonce。

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   sourceFormat                           控制输出nonce时的格式。
                                          输出时作为前缀添加 ``nonce-`` 时为 ``true`` ，
                                          不添加时为 ``false`` 。添加前缀时用于meta元素。
                                          默认为 ``false`` 。
   ====================================== ==========================================================================================

.. _tag-message_tag:

message标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：否

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   messageId ``必须``                     消息ID。
   option0～option9                       消息格式中使用的索引为0～9的可选参数。
                                          最多可指定10个可选参数。
   language                               消息的语言。
                                          默认为线程上下文中设置的语言。
   var                                    存储到请求作用域时使用的变量名。
                                          指定var属性时不输出消息而设置到请求作用域。
                                          设置到请求作用域时不进行HTML转义和HTML格式化。
   htmlEscape                             是否进行HTML转义。
                                          进行HTML转义时为 ``true`` ，不进行时为 ``false`` 。
                                          默认为 ``true`` 。
   withHtmlFormat                         是否进行HTML格式化(换行和半角空格转换)。
                                          HTML格式化仅在执行HTML转义时有效。
                                          默认为 ``true`` 。
   ====================================== ==========================================================================================

.. _tag-write_tag:

write标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：否

.. table::
   :class: tag-reference

   ====================================== ======================================================================================================================
   属性                                   说明
   ====================================== ======================================================================================================================
   name                                   从变量作用域获取显示目标值时使用的名称。不能与value属性同时指定。
   value                                  显示目标的值。用于直接指定值。不能与name属性同时指定。
   withHtmlFormat                         是否进行HTML格式化(换行和半角空格转换)。
                                          HTML格式化仅在执行HTML转义时有效。
                                          默认为 ``true`` 。
   valueFormat                            输出时的格式。
                                          指定内容请参阅 :ref:`tag-format_value` 。
   ====================================== ======================================================================================================================


.. _tag-pretty_print_tag:

prettyPrint标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：否

.. important::

  此标签已弃用，请勿使用。
  详情请参阅 :ref:`不推荐使用prettyPrint标签的理由 <tag-pretty_print_tag-deprecated>` 。

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   name ``必须``                          从变量作用域获取显示目标值时使用的名称
   ====================================== ==========================================================================================



.. _tag-raw_write_tag:

rawWrite标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：否

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   name ``必须``                          从变量作用域获取显示目标值时使用的名称
   ====================================== ==========================================================================================


.. _tag-set_tag:

set标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：否

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   var ``必须``                           存储到请求作用域时使用的变量名。
   name                                   用于获取值的名称。指定name属性或value属性之一。
   value                                  值。用于直接指定值。指定name属性或value属性之一。
   scope                                  设置存储变量的作用域。
                                          可指定的作用域如下所示。
                                          page: 页面作用域
                                          request: 请求作用域
                                          默认为请求作用域。
   bySingleValue                          是否将对应于name属性的值作为单一值获取。
                                          默认为 ``true`` 。
   ====================================== ==========================================================================================

.. _tag-include_tag:

include标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：否

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   path ``必须``                          要包含的资源的路径。
   ====================================== ==========================================================================================

.. _tag-include_param_tag:

includeParam标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：否

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   paramName ``必须``                     包含时使用的参数名称。
   name                                   用于获取值的名称。指定name属性或value属性之一。
   value                                  值。用于直接指定值。指定name属性或value属性之一。
   ====================================== ==========================================================================================

.. _tag-confirmation_page_tag:

confirmationPage标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：否

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   说明
   ====================================== ==========================================================================================
   path                                   转发目标（输入画面）的路径。
   ====================================== ==========================================================================================

.. _tag-ignore_confirmation_tag:

ignoreConfirmation标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：否

无属性。

.. _tag-for_input_page_tag:

forInputPage标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：否

无属性。
 
.. _tag-for_confirmation_page_tag:

forConfirmationPage标签
-------------------------

:ref:`动态属性的使用可否 <tag-dynamic_attributes_tag>` ：否

无属性。
