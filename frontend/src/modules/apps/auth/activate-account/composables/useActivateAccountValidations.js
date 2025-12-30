import { CoreInputValidator } from '@/modules/shared/common/validators/core/coreInputValidator';

export function useActivateAccountValidations() {
  const validateEmail = activateAccountFactory => {
    return (activateAccountFactory.emailError = CoreInputValidator.validateEmail(
      activateAccountFactory.email,
    ));
  };

  const validateActivationCode = activateAccountFactory => {
    return (activateAccountFactory.activationCodeError = CoreInputValidator.validateActivationCode(
      activateAccountFactory.activationCode,
    ));
  };

  const validateFieldsActivateAccount = activateAccountFactory => {
    const validations = [
      validateEmail(activateAccountFactory),
      validateActivationCode(activateAccountFactory),
    ];
    return validations.every(result => !result);
  };

  return {
    validateEmail,
    validateActivationCode,
    validateFieldsActivateAccount,
  };
}
