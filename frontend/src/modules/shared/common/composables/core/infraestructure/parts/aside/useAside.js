import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { userStore } from '@/modules/apps/users/stores/userStore';
import {
  HomeIcon,
  FolderIcon,
  UsersIcon,
  CogIcon,
  ChatBubbleLeftEllipsisIcon,
  BellIcon,
  ClockIcon,
} from '@heroicons/vue/24/outline';

export function useAside() {
  const storeUser = userStore();
  const route = useRoute();

  const items = [
    { name: 'Dashboard', routeName: 'dashboard', icon: HomeIcon, roles: ['user'] },
    { name: 'Users', routeName: 'overview', icon: UsersIcon, roles: ['user'] },
    { name: 'Projects', routeName: 'projects', icon: FolderIcon, roles: ['user'] },
    { name: 'LLM', routeName: 'llm', icon: ChatBubbleLeftEllipsisIcon, roles: ['user'] },
    { name: 'Panel', routeName: 'panel', icon: HomeIcon, roles: ['admin'] },
    { name: 'Session Activity', routeName: 'session-activity', icon: ClockIcon, roles: ['admin'] },
    { name: 'Notifications', routeName: 'notifications', icon: BellIcon, roles: ['user', 'admin'] },
    { name: 'Settings', routeName: 'settings', icon: CogIcon, roles: ['user'] },
  ];

  const menuAsideItems = computed(() =>
    items
      .filter(item => item.roles.includes(storeUser.userFactory?.role?.name))
      .map(item => ({
        ...item,
        activeInAside: route.name?.startsWith(item.routeName),
      })),
  );

  return {
    menuAsideItems,
  };
}
