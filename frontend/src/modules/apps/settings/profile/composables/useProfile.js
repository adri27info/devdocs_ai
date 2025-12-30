import { reactive, watch, computed } from 'vue';
import { createProfileDeleteFactory } from '@/modules/apps/settings/profile/factories/profileFactory';
import { useModal } from '@/modules/shared/common/composables/utils/ui/useModal';
import { useProfileReset } from '@/modules/apps/settings/profile/composables/useProfileReset';
import { useFetcher } from '@/modules/shared/common/composables/utils/useFetcher';
import { useProfileValidations } from '@/modules/apps/settings/profile/composables/useProfileValidations';
import { userStore } from '@/modules/apps/users/stores/userStore';

export function useProfile() {
  const ACTION = 'delete';

  const storeUser = userStore();

  const profileDeleteFactory = reactive(createProfileDeleteFactory());

  const { fetch } = useFetcher();
  const { validateConfirmationCode } = useProfileValidations();
  const { resetProfileDeleteFactory } = useProfileReset();
  const { isOpen, open, close } = useModal();

  const isDeleteDisabled = computed(() => {
    return profileDeleteFactory.confirmationCode.trim().toLowerCase() !== ACTION;
  });

  const deleteProfileAccount = async () => {
    if (validateConfirmationCode(profileDeleteFactory)) return;

    if (profileDeleteFactory.confirmationCode === ACTION) {
      await fetch({
        app: 'user',
        action: 'delete',
        params: {
          id: storeUser.userFactory.id,
          confirmationCode: profileDeleteFactory.confirmationCode,
        },
      });

      closeModal();
    }
  };

  const openModal = () => {
    resetProfileDeleteFactory(profileDeleteFactory);
    open();
  };

  const closeModal = () => {
    close();
    resetProfileDeleteFactory(profileDeleteFactory);
  };

  watch(
    () => profileDeleteFactory.confirmationCode,
    () => {
      validateConfirmationCode(profileDeleteFactory);
    },
  );

  return {
    profileDeleteFactory,
    isOpen,
    isDeleteDisabled,

    openModal,
    closeModal,
    deleteProfileAccount,
  };
}
