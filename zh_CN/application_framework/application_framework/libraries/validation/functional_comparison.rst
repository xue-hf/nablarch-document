.. _`validation-functional_comparison`:

Bean Validation与Nablarch Validation的功能比较
----------------------------------------------------------------------------------------------------
这里展示Nablarch提供的验证功能与 |jsr349| 的功能比较。

.. list-table:: 功能比较（○：提供　△：部分提供　×：不提供　－:对象外）
  :header-rows: 1
  :class: something-special-class

  * - 功能
    - Bean |br| Validation
    - Nablarch |br| Validation
    - Jakarta |br| Bean Validation
  * - 可以指定验证目标项目
    - ○ [#property_validation]_
    - ○ |br| :ref:`前往解说 <nablarch_validation-execute>`
    - ○
  * - 可以对具有层次结构的Java Beans对象 |br| 进行验证
    - ○ [#jsr]_
    - ○ |br| :ref:`前往解说 <nablarch_validation-nest_bean>`
    - ○
  * - 可以对方法的参数、返回值进行验证
    - × [#method]_
    - × [#method]_
    - ○
  * - 可以进行关联验证
    - ○ |br| :ref:`前往解说 <bean_validation-correlation_validation>`
    - ○ |br| :ref:`前往解说 <nablarch_validation-correlation_validation>`
    - ○
  * - 可以指定验证的执行顺序
    - × [#order]_
    - ○ |br| :ref:`前往解说 <nablarch_validation-execute>`
    - ○
  * - 可以以特定项目的值为条件 |br| 切换验证项目
    - ○ [#conditional]_
    - ○ |br| :ref:`前往解说 <nablarch_validation-conditional>`
    - ○
  * - 可以在错误消息中使用嵌入参数
    - ○ [#parameter]_ |br| :ref:`前往解说 <message>`
    - ○ |br| :ref:`前往解说 <message>`
    - ○
  * - 可以进行域验证
    - ○ |br| :ref:`前往解说 <bean_validation-domain_validation>`
    - ○ |br| :ref:`前往解说 <nablarch_validation-domain_validation>`
    - ×
  * - 可以进行值的类型转换
    - × [#type_converter]_
    - ○ |br| :ref:`前往解说 <nablarch_validation-definition_validator_convertor>`
    - ×
  * - 可以进行值的规范化
    - × [#normalized]_
    - ○ |br| :ref:`前往解说 <nablarch_validation-definition_validator_convertor>`
    - ×
  * - 可以在错误消息中嵌入项目名
    - ○ |br| :ref:`前往解说 <bean_validation-property_name>`
    - ○ |br| :ref:`前往解说 <nablarch_validation-property_name>`
    - ×

.. [#property_validation] 通过对Form的所有项目进行验证，可以防止接受不正确的输入值。 |br|
    因此，在Bean Validation中，不推荐执行指定项目的验证。 |br|
    如果无论如何都想仅对指定项目进行验证，
    请使用 :java:extdoc:`ValidatorUtil#validate <nablarch.core.validation.ee.ValidatorUtil.validate(java.lang.Object,java.lang.String...)>` 。
    
.. [#jsr] 对应方法遵循 |jsr349| 的规范。
.. [#method] Nablarch在从外部接收数据的时机一定会进行验证，
   因此不支持对方法的参数和返回值进行验证。
.. [#order] 无法控制验证的执行顺序，因此请勿进行依赖验证执行顺序的实现。
   例如，不应期望在每个项目的验证后执行关联验证等。
.. [#conditional]  使用 |jsr349| 的类级别验证功能，通过逻辑切换验证项目。
.. [#parameter] 在Bean Validation中，也可以使用EL表达式嵌入参数。
.. [#type_converter] 在Bean Validation中，属性全部定义为String类型（:ref:`定义为String的理由 <bean_validation-form_property>`），因此不进行类型转换。
   如果需要类型转换，请在验证后使用 :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` 进行类型转换。
.. [#normalized] 规范化不是Bean Validation的功能，而是作为handler提供的。如果需要规范化，请使用 :ref:`normalize_handler` 进行。

.. |jsr349| raw:: html

   <a href="https://jakarta.ee/specifications/bean-validation/" target="_blank">Jakarta Bean Validation(外部站点、英文)</a>

.. |br| raw:: html

   <br />
