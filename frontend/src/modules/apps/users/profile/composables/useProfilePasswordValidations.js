import { ERRORS } from '@/modules/shared/common/constants/apps/user/password_errors';
import { CoreInputValidator } from '@/modules/shared/common/validators/core/coreInputValidator';

export function useProfilePasswordValidations() {
  const validateCurrentPassword = profilePasswordFactory => {
    return (profilePasswordFactory.currentPasswordError = CoreInputValidator.validatePassword({
      password: profilePasswordFactory.currentPassword,
      additionalValidations: false,
    }));
  };

  const validateNewPassword = profilePasswordFactory => {
    return (profilePasswordFactory.newPasswordError = CoreInputValidator.validatePassword({
      password: profilePasswordFactory.newPassword,
    }));
  };

  const validateConfirmNewPassword = profilePasswordFactory => {
    return (profilePasswordFactory.confirmNewPasswordError = CoreInputValidator.validatePassword({
      password: profilePasswordFactory.confirmNewPassword,
    }));
  };

  const validatePasswords = profilePasswordFactory => {
    const validations = [
      validateCurrentPassword(profilePasswordFactory),
      validateNewPassword(profilePasswordFactory),
      validateConfirmNewPassword(profilePasswordFactory),
    ];

    const noErrors = validations.every(result => !result);

    profilePasswordFactory.passwordsMatch =
      profilePasswordFactory.newPassword === profilePasswordFactory.confirmNewPassword;

    if (!profilePasswordFactory.passwordsMatch) {
      profilePasswordFactory.passwordMatchError = ERRORS.NOT_MATCH;
      profilePasswordFactory.newPasswordError = '';
      profilePasswordFactory.confirmNewPasswordError = '';
    } else {
      profilePasswordFactory.passwordMatchError = '';
    }

    return noErrors && profilePasswordFactory.passwordsMatch;
  };

  return {
    validateCurrentPassword,
    validateNewPassword,
    validateConfirmNewPassword,
    validatePasswords,
  };
}
