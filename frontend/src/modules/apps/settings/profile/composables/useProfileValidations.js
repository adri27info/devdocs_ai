import { CoreInputValidator } from '@/modules/shared/common/validators/core/coreInputValidator';

export function useProfileValidations() {
  const validateConfirmationCode = profileDeleteFactory => {
    return (profileDeleteFactory.confirmationCodeError =
      CoreInputValidator.validateConfirmationCode(profileDeleteFactory.confirmationCode));
  };

  return {
    validateConfirmationCode,
  };
}
