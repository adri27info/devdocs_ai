import { watch, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { createResetPasswordConfirmFactory } from '@/modules/apps/auth/reset-password/factories/resetPasswordFactory';
import { useResetPasswordQueryParams } from '@/modules/apps/auth/reset-password/composables/useResetPasswordQueryParams';
import { useFormPasswordFieldProps } from '@/modules/shared/common/composables/forms/useFormPasswordFieldsProps';
import { useResetPasswordValidations } from '@/modules/apps/auth/reset-password/composables/useResetPasswordValidations';
import { useFetcher } from '@/modules/shared/common/composables/utils/useFetcher';

export function useResetPasswordConfirm() {
  const router = useRouter();

  const resetPasswordConfirmFactory = reactive(createResetPasswordConfirmFactory());

  const { fetch } = useFetcher();
  const { uid, token } = useResetPasswordQueryParams();

  const { passwordProps: newPasswordProps, togglePasswordVisibility: toggleNewPasswordVisibility } =
    useFormPasswordFieldProps(resetPasswordConfirmFactory, 'newPasswordVisible');

  const {
    passwordProps: confirmNewPasswordProps,
    togglePasswordVisibility: toggleConfirmNewPasswordVisibility,
  } = useFormPasswordFieldProps(resetPasswordConfirmFactory, 'confirmNewPasswordVisible');

  const { validateNewPassword, validateConfirmNewPassword, validateBothPasswords } =
    useResetPasswordValidations();

  const handleResetPasswordConfirm = async () => {
    if (!validateBothPasswords(resetPasswordConfirmFactory)) return;

    const result = await fetch({
      app: 'auth',
      action: 'resetPasswordConfirm',
      params: {
        uid: uid.value,
        token: token.value,
        password: resetPasswordConfirmFactory.newPassword,
      },
    });

    if (result.success) {
      await router.push({ name: 'login' });
    }
  };

  watch(
    () => resetPasswordConfirmFactory.newPassword,
    () => {
      validateNewPassword(resetPasswordConfirmFactory);
    },
  );

  watch(
    () => resetPasswordConfirmFactory.confirmNewPassword,
    () => {
      validateConfirmNewPassword(resetPasswordConfirmFactory);
    },
  );

  return {
    resetPasswordConfirmFactory,
    newPasswordProps,
    confirmNewPasswordProps,

    toggleNewPasswordVisibility,
    toggleConfirmNewPasswordVisibility,
    handleResetPasswordConfirm,
  };
}
