import { ERRORS } from '@/modules/shared/common/constants/apps/user/password_errors';
import { CoreInputValidator } from '@/modules/shared/common/validators/core/coreInputValidator';

export function useResetPasswordValidations() {
  const validateEmail = resetPasswordFactory => {
    resetPasswordFactory.emailError = CoreInputValidator.validateEmail(resetPasswordFactory.email);
  };

  const validateNewPassword = resetPasswordConfirmFactory => {
    return (resetPasswordConfirmFactory.newPasswordError = CoreInputValidator.validatePassword({
      password: resetPasswordConfirmFactory.newPassword,
    }));
  };

  const validateConfirmNewPassword = resetPasswordConfirmFactory => {
    return (resetPasswordConfirmFactory.confirmNewPasswordError =
      CoreInputValidator.validatePassword({
        password: resetPasswordConfirmFactory.confirmNewPassword,
      }));
  };

  const validateBothPasswords = resetPasswordConfirmFactory => {
    const validations = [
      validateNewPassword(resetPasswordConfirmFactory),
      validateConfirmNewPassword(resetPasswordConfirmFactory),
    ];
    const noErrors = validations.every(result => !result);

    resetPasswordConfirmFactory.passwordsMatch =
      resetPasswordConfirmFactory.newPassword === resetPasswordConfirmFactory.confirmNewPassword;

    if (!resetPasswordConfirmFactory.passwordsMatch) {
      resetPasswordConfirmFactory.passwordMatchError = ERRORS.NOT_MATCH;
      resetPasswordConfirmFactory.newPasswordError = '';
      resetPasswordConfirmFactory.confirmNewPasswordError = '';
    } else {
      resetPasswordConfirmFactory.passwordMatchError = '';
    }

    return noErrors && resetPasswordConfirmFactory.passwordsMatch;
  };

  return {
    validateEmail,
    validateNewPassword,
    validateConfirmNewPassword,
    validateBothPasswords,
  };
}
