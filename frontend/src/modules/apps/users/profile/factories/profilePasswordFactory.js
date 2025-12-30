export function createProfilePasswordFactory() {
  return {
    currentPassword: '',
    currentPasswordError: '',
    newPassword: '',
    newPasswordError: '',
    confirmNewPassword: '',
    confirmNewPasswordError: '',
    passwordMatchError: '',
    passwordsMatch: true,
    currentPasswordVisible: false,
    newPasswordVisible: false,
    confirmNewPasswordVisible: false,
  };
}
