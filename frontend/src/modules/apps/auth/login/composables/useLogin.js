import { watch, reactive } from 'vue';
import { REDIRECTION_ROUTES } from '@/modules/shared/common/constants/utils/redirection_routes';
import { ROLES } from '@/modules/shared/common/constants/utils/roles';
import { createLoginFactory } from '@/modules/apps/auth/login/factories/loginFactory';
import { useRouter } from 'vue-router';
import { useLoginValidations } from '@/modules/apps/auth/login/composables/useLoginValidations';
import { useFetcher } from '@/modules/shared/common/composables/utils/useFetcher';
import { useFormPasswordFieldProps } from '@/modules/shared/common/composables/forms/useFormPasswordFieldsProps';
import { userStore } from '@/modules/apps/users/stores/userStore';

export function useLogin() {
  const router = useRouter();
  const storeUser = userStore();

  const loginFactory = reactive(createLoginFactory());

  const { validateEmail, validatePassword, validateFieldsLogin } = useLoginValidations();
  const { fetch } = useFetcher();
  const { passwordProps, togglePasswordVisibility } = useFormPasswordFieldProps(
    loginFactory,
    'passwordVisible',
  );

  const handleLogin = async () => {
    if (!validateFieldsLogin(loginFactory)) return;

    const result = await fetch({
      app: 'auth',
      action: 'login',
      params: {
        email: loginFactory.email,
        password: loginFactory.password,
        rememberMe: loginFactory.rememberMe,
      },
    });

    if (result.success) {
      const redirectRoute =
        storeUser.userFactory.role.name === ROLES.ADMIN
          ? REDIRECTION_ROUTES.ADMIN_AFTER_LOGIN
          : REDIRECTION_ROUTES.USER_AFTER_LOGIN;

      await router.push({ name: redirectRoute });
    }
  };

  watch(
    () => loginFactory.email,
    () => {
      validateEmail(loginFactory);
    },
  );

  watch(
    () => loginFactory.password,
    () => {
      validatePassword(loginFactory);
    },
  );

  return {
    loginFactory,
    passwordProps,

    togglePasswordVisibility,
    handleLogin,
  };
}
