import { ref, reactive, computed, watch, onMounted } from 'vue';
import { createOverviewFactory } from '@/modules/apps/users/overview/factories/overviewFactory';
import { useFetcher } from '@/modules/shared/common/composables/utils/useFetcher';
import { useModal } from '@/modules/shared/common/composables/utils/ui/useModal';
import { useOverviewReset } from '@/modules/apps/users/overview/composables/useOverviewReset';
import { userStore } from '@/modules/apps/users/stores/userStore';
import { usersStore } from '@/modules/apps/users/stores/usersStore';

export function useOverview() {
  const storeUser = userStore();
  const storeUsers = usersStore();

  const selectedUserId = ref(null);
  const isFreePlan = ref(false);
  const overviewFactory = reactive(createOverviewFactory());

  const { fetch } = useFetcher();
  const { isOpen, close, open } = useModal();
  const { resetOverviewFactory } = useOverviewReset();

  const filteredUsers = computed(() => {
    return storeUsers.usersFactory.list.filter(user => user.id !== storeUser.userFactory.id);
  });

  const fetchProjectList = async () => {
    await fetch({
      app: 'project',
      action: 'list',
      hideSuccess: true,
    });
  };

  const handleAddUserProject = async () => {
    const result = await fetch({
      app: 'project',
      action: 'addUser',
      params: {
        projectsSelected: overviewFactory.projects_selected,
        user: selectedUserId.value,
      },
    });

    closeModal();

    if (result?.success) {
      await fetchProjectList();
    }
  };

  const openModal = async id => {
    resetOverviewState(id);
    open();

    await fetchProjectList();
  };

  const closeModal = () => {
    close();
    resetOverviewState();
  };

  const resetOverviewState = (id = null) => {
    resetOverviewFactory(overviewFactory);
    selectedUserId.value = id;
  };

  watch(
    () => storeUser.userStatsFactory,
    newStats => {
      const planName = newStats.plan_type.name.toLowerCase();
      isFreePlan.value = planName === 'free';
    },
    { immediate: true, deep: true },
  );

  onMounted(async () => {
    await fetch({
      app: 'users',
      hideSuccess: true,
    });

    await fetch({
      app: 'user',
      action: 'stats',
      hideSuccess: true,
    });
  });

  return {
    overviewFactory,
    isFreePlan,
    isOpen,
    selectedUserId,
    filteredUsers,

    openModal,
    closeModal,
    handleAddUserProject,
  };
}
