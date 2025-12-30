import { CoreInputValidator } from '@/modules/shared/common/validators/core/coreInputValidator';

export function useProjectCreateValidations() {
  const OPTION_ERROR = 'Please select an valid option';

  const validateName = basicProfileCreateFactory => {
    return (basicProfileCreateFactory.nameError = CoreInputValidator.validateName(
      basicProfileCreateFactory.name,
    ));
  };

  const validateDescription = basicProfileCreateFactory => {
    return (basicProfileCreateFactory.descriptionError = CoreInputValidator.validateDescription(
      basicProfileCreateFactory.description,
    ));
  };

  const validatePrivacy = (selectedOption, basicProfileCreateFactory) => {
    if (!selectedOption.value || selectedOption.value.value === '') {
      basicProfileCreateFactory.privacyError = OPTION_ERROR;
      return basicProfileCreateFactory.privacyError;
    }

    basicProfileCreateFactory.privacyError = '';
    return '';
  };

  const validateFieldsProjectCreate = (selectedOption, basicProfileCreateFactory) => {
    const validations = [
      validateName(basicProfileCreateFactory),
      validateDescription(basicProfileCreateFactory),
      validatePrivacy(selectedOption, basicProfileCreateFactory),
    ];
    return validations.every(result => !result);
  };

  return {
    validateName,
    validateDescription,
    validateFieldsProjectCreate,
  };
}
