import { ref, computed, watch } from 'vue';
import { ROLES } from '@/modules/shared/common/constants/utils/roles';
import { userStore } from '@/modules/apps/users/stores/userStore';

export function useHeaderUser(handleLogout, closeDropdown) {
  const storeUser = userStore();

  const avatarSrc = ref('');

  const hasRoleUser = computed(() => storeUser.userFactory.role.name == ROLES.USER);

  const logoutAndCloseDropdown = async () => {
    await handleLogout();
    closeDropdown();
  };

  watch(
    () => storeUser.userFactory.attachment,
    attachment => {
      avatarSrc.value = attachment;
    },
    { immediate: true },
  );

  return {
    avatarSrc,
    hasRoleUser,

    logoutAndCloseDropdown,
  };
}
