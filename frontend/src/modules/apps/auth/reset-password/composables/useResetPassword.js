import { reactive, watch } from 'vue';
import { useRouter } from 'vue-router';
import { createResetPasswordFactory } from '@/modules/apps/auth/reset-password/factories/resetPasswordFactory';
import { useFetcher } from '@/modules/shared/common/composables/utils/useFetcher';
import { useResetPasswordValidations } from '@/modules/apps/auth/reset-password/composables/useResetPasswordValidations';

export function useResetPassword() {
  const router = useRouter();

  const resetPasswordFactory = reactive(createResetPasswordFactory());

  const { fetch } = useFetcher();
  const { validateEmail } = useResetPasswordValidations();

  const handleResetPassword = async () => {
    validateEmail(resetPasswordFactory);

    if (resetPasswordFactory.emailError) return;

    const result = await fetch({
      app: 'auth',
      action: 'resetPassword',
      params: {
        email: resetPasswordFactory.email,
      },
    });

    if (result.success) {
      await router.push({ name: 'login' });
    }
  };

  watch(
    () => resetPasswordFactory.email,
    () => {
      validateEmail(resetPasswordFactory);
    },
  );

  return {
    resetPasswordFactory,

    handleResetPassword,
  };
}
