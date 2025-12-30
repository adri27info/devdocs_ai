import { watch, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { createResendActivationCodeFactory } from '@/modules/apps/auth/resend-activation-code/factories/resendActivationCodeFactory';
import { useFetcher } from '@/modules/shared/common/composables/utils/useFetcher';
import { useResendActivationCodeValidations } from '@/modules/apps/auth/resend-activation-code/composables/useResendActivationCodeValidations';

export function useResendActivationCode() {
  const router = useRouter();

  const resendActivationCodeFactory = reactive(createResendActivationCodeFactory());

  const { fetch } = useFetcher();
  const { validateEmail } = useResendActivationCodeValidations();

  const handleResendActivationCode = async () => {
    validateEmail(resendActivationCodeFactory);

    if (resendActivationCodeFactory.emailError) return;

    const result = await fetch({
      app: 'auth',
      action: 'resendActivationCode',
      params: {
        email: resendActivationCodeFactory.email,
      },
    });

    if (result.success) {
      await router.push({ name: 'activate-account' });
    }
  };

  watch(
    () => resendActivationCodeFactory.email,
    () => {
      validateEmail(resendActivationCodeFactory);
    },
  );

  return {
    resendActivationCodeFactory,

    handleResendActivationCode,
  };
}
