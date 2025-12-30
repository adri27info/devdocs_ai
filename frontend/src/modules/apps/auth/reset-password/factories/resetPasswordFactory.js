export function createResetPasswordFactory() {
  return {
    email: '',
    emailError: '',
  };
}

export function createResetPasswordConfirmFactory() {
  return {
    newPassword: '',
    newPasswordError: '',
    confirmNewPassword: '',
    confirmNewPasswordError: '',
    passwordMatchError: '',
    passwordsMatch: true,
    newPasswordVisible: false,
    confirmNewPasswordVisible: false,
  };
}
