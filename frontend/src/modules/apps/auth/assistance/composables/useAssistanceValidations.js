import { CoreInputValidator } from '@/modules/shared/common/validators/core/coreInputValidator';

export function useAssistanceValidations() {
  const OPTION_ERROR = 'Please select an valid option';

  const showOtherReason = option => option?.value === 'info';

  const validateEmail = assistanceFactory => {
    return (assistanceFactory.emailError = CoreInputValidator.validateEmail(
      assistanceFactory.email,
    ));
  };

  const validateType = (selectedOption, assistanceFactory) => {
    if (!selectedOption.value || selectedOption.value.value === '') {
      assistanceFactory.typeError = OPTION_ERROR;
      return assistanceFactory.typeError;
    }

    assistanceFactory.typeError = '';
    return '';
  };

  const validateMessageReason = (selectedOption, assistanceFactory) => {
    if (!showOtherReason(selectedOption.value)) {
      assistanceFactory.messageReasonError = '';
      return '';
    }

    return (assistanceFactory.messageReasonError = CoreInputValidator.validateMessageReason(
      assistanceFactory.messageReason,
    ));
  };

  const validateFieldsAssistance = (selectedOption, assistanceFactory) => {
    const validations = [
      validateEmail(assistanceFactory),
      validateType(selectedOption, assistanceFactory),
      validateMessageReason(selectedOption, assistanceFactory),
    ];
    return validations.every(result => !result);
  };

  return {
    validateEmail,
    validateMessageReason,
    validateFieldsAssistance,
    showOtherReason,
  };
}
