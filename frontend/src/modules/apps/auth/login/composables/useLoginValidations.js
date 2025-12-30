import { CoreInputValidator } from '@/modules/shared/common/validators/core/coreInputValidator';

export function useLoginValidations() {
  const validateEmail = loginFactory => {
    return (loginFactory.emailError = CoreInputValidator.validateEmail(loginFactory.email));
  };

  const validatePassword = loginFactory => {
    return (loginFactory.passwordError = CoreInputValidator.validatePassword({
      password: loginFactory.password,
      additionalValidations: false,
    }));
  };

  const validateFieldsLogin = loginFactory => {
    const validations = [validateEmail(loginFactory), validatePassword(loginFactory)];
    return validations.every(result => !result);
  };

  return {
    validateEmail,
    validatePassword,
    validateFieldsLogin,
  };
}
