import { ref, watch, computed } from 'vue';
import { LIST_OPTIONS } from '@/modules/shared/common/constants/apps/projects/list_options';
import { useFetcher } from '@/modules/shared/common/composables/utils/useFetcher';
import { useDebounce } from '@/modules/shared/common/composables/utils/useDebounce';

export function useProjectList() {
  const searchQuery = ref('');
  const selectedMenuItem = ref('All projects');

  const { fetch } = useFetcher();
  const debouncedSearch = useDebounce(searchQuery, 500);

  const fetchProjects = async () => {
    const params = {};

    if (debouncedSearch.value.trim()) {
      params.name = debouncedSearch.value.trim();
    } else if (selectedMenuItem.value !== 'All projects') {
      params.privacy = selectedMenuItem.value.toLowerCase();
    }

    await fetch({
      app: 'project',
      action: 'list',
      hideSuccess: true,
      params,
    });
  };

  const handleMenuClick = async item => {
    selectedMenuItem.value = item.name;
    searchQuery.value = '';

    await fetchProjects();
  };

  const menuProjectsItems = computed(() =>
    LIST_OPTIONS.map(item => ({
      ...item,
      activeInGeneral: selectedMenuItem.value === item.name,
    })),
  );

  watch(debouncedSearch, fetchProjects, { immediate: true });

  watch(searchQuery, value => {
    if (value.trim()) {
      selectedMenuItem.value = 'All projects';
    }
  });

  return {
    menuProjectsItems,
    selectedMenuItem,
    searchQuery,

    handleMenuClick,
  };
}
