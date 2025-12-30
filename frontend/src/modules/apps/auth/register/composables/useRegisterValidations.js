import { CoreInputValidator } from '@/modules/shared/common/validators/core/coreInputValidator';

export function useRegisterValidations() {
  const validateFirstName = registerFactory => {
    return (registerFactory.firstNameError = CoreInputValidator.validateFirstName(
      registerFactory.firstName,
    ));
  };

  const validateLastName = registerFactory => {
    return (registerFactory.lastNameError = CoreInputValidator.validateLastName(
      registerFactory.lastName,
    ));
  };

  const validateEmail = registerFactory => {
    return (registerFactory.emailError = CoreInputValidator.validateEmail(registerFactory.email));
  };

  const validatePassword = registerFactory => {
    return (registerFactory.passwordError = CoreInputValidator.validatePassword({
      password: registerFactory.password,
    }));
  };

  const validateAttachment = registerFactory => {
    return (registerFactory.attachmentError = CoreInputValidator.validateAttachment(
      registerFactory.attachment,
    ));
  };

  const validateFieldsRegister = registerFactory => {
    const validations = [
      validateFirstName(registerFactory),
      validateLastName(registerFactory),
      validateEmail(registerFactory),
      validatePassword(registerFactory),
      validateAttachment(registerFactory),
    ];

    return validations.every(result => !result);
  };

  return {
    validateFirstName,
    validateLastName,
    validateEmail,
    validatePassword,
    validateAttachment,
    validateFieldsRegister,
  };
}
