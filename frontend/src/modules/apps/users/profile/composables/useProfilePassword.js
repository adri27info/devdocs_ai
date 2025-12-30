import { ref, reactive, watch, nextTick } from 'vue';
import { createProfilePasswordFactory } from '@/modules/apps/users/profile/factories/profilePasswordFactory';
import { useFormPasswordFieldProps } from '@/modules/shared/common/composables/forms/useFormPasswordFieldsProps';
import { useProfilePasswordReset } from '@/modules/apps/users/profile/composables/useProfilePasswordReset';
import { useFetcher } from '@/modules/shared/common/composables/utils/useFetcher';
import { useProfilePasswordValidations } from '@/modules/apps/users/profile/composables/useProfilePasswordValidations';
import { userStore } from '@/modules/apps/users/stores/userStore';

export function useProfilePassword() {
  const storeUser = userStore();

  const shouldValidate = ref(true);
  const profilePasswordFactory = reactive(createProfilePasswordFactory());

  const {
    validateCurrentPassword,
    validateNewPassword,
    validateConfirmNewPassword,
    validatePasswords,
  } = useProfilePasswordValidations();

  const { passwordProps: newPasswordProps, togglePasswordVisibility: toggleNewPasswordVisibility } =
    useFormPasswordFieldProps(profilePasswordFactory, 'newPasswordVisible');

  const {
    passwordProps: confirmNewPasswordProps,
    togglePasswordVisibility: toggleConfirmNewPasswordVisibility,
  } = useFormPasswordFieldProps(profilePasswordFactory, 'confirmNewPasswordVisible');

  const {
    passwordProps: currentPasswordProps,
    togglePasswordVisibility: toggleCurrentPasswordVisibility,
  } = useFormPasswordFieldProps(profilePasswordFactory, 'currentPasswordVisible');

  const { resetProfilePasswordFactory } = useProfilePasswordReset();
  const { fetch } = useFetcher();

  const handleProfilePassword = async () => {
    if (!validatePasswords(profilePasswordFactory)) return;

    const result = await fetch({
      app: 'user',
      action: 'updateProfilePassword',
      params: {
        id: storeUser.userFactory.id,
        currentPassword: profilePasswordFactory.currentPassword,
        newPassword: profilePasswordFactory.newPassword,
      },
    });

    if (result?.success) {
      shouldValidate.value = false;

      resetProfilePasswordFactory(profilePasswordFactory);

      nextTick(() => {
        shouldValidate.value = true;
      });
    }
  };

  watch(
    () => profilePasswordFactory.currentPassword,
    () => {
      if (!shouldValidate.value) return;
      validateCurrentPassword(profilePasswordFactory);
    },
  );

  watch(
    () => profilePasswordFactory.newPassword,
    () => {
      if (!shouldValidate.value) return;
      validateNewPassword(profilePasswordFactory);
    },
  );

  watch(
    () => profilePasswordFactory.confirmNewPassword,
    () => {
      if (!shouldValidate.value) return;
      validateConfirmNewPassword(profilePasswordFactory);
    },
  );

  return {
    profilePasswordFactory,
    currentPasswordProps,
    newPasswordProps,
    confirmNewPasswordProps,

    handleProfilePassword,
    toggleCurrentPasswordVisibility,
    toggleNewPasswordVisibility,
    toggleConfirmNewPasswordVisibility,
  };
}
