import { shallowRef, watch } from 'vue';
import { ROLES } from '@/modules/shared/common/constants/utils/roles';
import { useRoute } from 'vue-router';
import HeaderGuest from '@/modules/shared/common/components/infraestructure/parts/headers/HeaderGuest.vue';
import HeaderUser from '@/modules/shared/common/components/infraestructure/parts/headers/HeaderUser.vue';

export function useCoreLayout() {
  const route = useRoute();
  const currentHeader = shallowRef(null);

  watch(
    () => route.meta.headerType,
    newVal => {
      if (newVal === ROLES.GUEST) currentHeader.value = HeaderGuest;
      else if (newVal === ROLES.USER) currentHeader.value = HeaderUser;
    },
    { immediate: true },
  );

  return { currentHeader };
}
