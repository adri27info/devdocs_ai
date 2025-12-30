import { computed } from 'vue';
import { userStore } from '@/modules/apps/users/stores/userStore';
import {
  InformationCircleIcon,
  ExclamationTriangleIcon,
  ArrowPathIcon,
} from '@heroicons/vue/24/outline';

export function useNotification() {
  const storeUser = userStore();

  const items = [
    {
      name: 'Information',
      routeName: 'notifications-information',
      icon: InformationCircleIcon,
      roles: ['user', 'admin'],
    },
    {
      name: 'Action required',
      routeName: 'notifications-action-required',
      icon: ExclamationTriangleIcon,
      roles: ['user'],
    },
    {
      name: 'Reset cache',
      routeName: 'notifications-reset',
      icon: ArrowPathIcon,
      roles: ['admin'],
    },
  ];

  const menuNotificationItems = computed(() =>
    items
      .filter(item => item.roles.includes(storeUser.userFactory?.role?.name))
      .map(item => ({
        ...item,
      })),
  );

  return {
    menuNotificationItems,
  };
}
