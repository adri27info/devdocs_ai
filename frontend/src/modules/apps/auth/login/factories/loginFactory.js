export function createLoginFactory() {
  return {
    email: '',
    password: '',
    emailError: '',
    passwordError: '',
    passwordVisible: false,
    rememberMe: false,
  };
}
