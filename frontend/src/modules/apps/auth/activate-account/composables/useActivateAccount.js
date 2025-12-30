import { watch, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { createActivateAccountFactory } from '@/modules/apps/auth/activate-account/factories/activateAccountFactory';
import { useFetcher } from '@/modules/shared/common/composables/utils/useFetcher';
import { useActivateAccountValidations } from '@/modules/apps/auth/activate-account/composables/useActivateAccountValidations';

export function useActivateAccount() {
  const router = useRouter();

  const activateAccountFactory = reactive(createActivateAccountFactory());

  const { fetch } = useFetcher();
  const { validateEmail, validateActivationCode, validateFieldsActivateAccount } =
    useActivateAccountValidations();

  const handleActivateAccount = async () => {
    if (!validateFieldsActivateAccount(activateAccountFactory)) return;

    const result = await fetch({
      app: 'auth',
      action: 'activateAccount',
      params: {
        email: activateAccountFactory.email,
        activationCode: activateAccountFactory.activationCode,
      },
    });

    if (result.success) {
      await router.push({ name: 'login' });
    }
  };

  watch(
    () => activateAccountFactory.email,
    () => {
      validateEmail(activateAccountFactory);
    },
  );

  watch(
    () => activateAccountFactory.activationCode,
    () => {
      validateActivationCode(activateAccountFactory);
    },
  );

  return {
    activateAccountFactory,

    handleActivateAccount,
  };
}
