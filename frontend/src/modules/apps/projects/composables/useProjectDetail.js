import { ref, computed } from 'vue';
import { MENU_PROJECT_DETAIL_ITEMS } from '@/modules/shared/common/constants/apps/projects/items_detail';

export function useProjectDetail() {
  const selectedMenuItem = ref('Generate documentation');

  const menuProjectItems = computed(() =>
    MENU_PROJECT_DETAIL_ITEMS.map(item => ({
      ...item,
      activeInGeneral: selectedMenuItem.value === item.name,
    })),
  );

  const handleMenuClick = item => {
    selectedMenuItem.value = item.name;
  };

  return {
    menuProjectItems,
    selectedMenuItem,

    handleMenuClick,
  };
}
