import { CoreInputValidator } from '@/modules/shared/common/validators/core/coreInputValidator';

export function useProfileValidations() {
  const validateFirstName = profileFactory => {
    return (profileFactory.firstNameError = CoreInputValidator.validateFirstName(
      profileFactory.firstName,
    ));
  };

  const validateLastName = profileFactory => {
    return (profileFactory.lastNameError = CoreInputValidator.validateLastName(
      profileFactory.lastName,
    ));
  };

  const validateAttachment = profileFactory => {
    return (profileFactory.attachmentError = CoreInputValidator.validateAttachment(
      profileFactory.attachment,
    ));
  };

  const validateFieldsProfile = profileFactory => {
    const validations = [
      validateFirstName(profileFactory),
      validateLastName(profileFactory),
      validateAttachment(profileFactory),
    ];
    return validations.every(result => !result);
  };

  return {
    validateFirstName,
    validateLastName,
    validateAttachment,
    validateFieldsProfile,
  };
}
