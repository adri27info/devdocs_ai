import { CoreInputValidator } from '@/modules/shared/common/validators/core/coreInputValidator';

export function useProjectDetailDataValidations() {
  const OPTION_ERROR = 'Please select an valid option';

  const validateName = basicProfileUpdateFactory => {
    return (basicProfileUpdateFactory.nameError = CoreInputValidator.validateName(
      basicProfileUpdateFactory.name,
    ));
  };

  const validateDescription = basicProfileUpdateFactory => {
    return (basicProfileUpdateFactory.descriptionError = CoreInputValidator.validateDescription(
      basicProfileUpdateFactory.description,
    ));
  };

  const validatePrivacy = (selectedOption, basicProfileUpdateFactory) => {
    if (!selectedOption.value || selectedOption.value.value === '') {
      basicProfileUpdateFactory.privacyError = OPTION_ERROR;
      return basicProfileUpdateFactory.privacyError;
    }

    basicProfileUpdateFactory.privacyError = '';
    return '';
  };

  const validateFieldsProjecUpdate = (selectedOption, basicProfileUpdateFactory) => {
    const validations = [
      validateName(basicProfileUpdateFactory),
      validateDescription(basicProfileUpdateFactory),
      validatePrivacy(selectedOption, basicProfileUpdateFactory),
    ];
    return validations.every(result => !result);
  };

  return {
    validateName,
    validateDescription,
    validateFieldsProjecUpdate,
  };
}
