import { CoreInputValidator } from '@/modules/shared/common/validators/core/coreInputValidator';

export function useResendActivationCodeValidations() {
  const validateEmail = resendActivationCodeFactory => {
    return (resendActivationCodeFactory.emailError = CoreInputValidator.validateEmail(
      resendActivationCodeFactory.email,
    ));
  };

  return {
    validateEmail,
  };
}
