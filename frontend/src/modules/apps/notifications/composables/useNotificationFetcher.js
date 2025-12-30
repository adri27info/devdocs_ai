import { ref, onMounted } from 'vue';
import { NOTIFICATION_TYPES } from '@/modules/shared/common/constants/apps/notifications/types';
import { useFetcher } from '@/modules/shared/common/composables/utils/useFetcher';
import { useModal } from '@/modules/shared/common/composables/utils/ui/useModal';

export function useNotificationFetcher(type) {
  const selectedNotificationId = ref(null);

  const { isOpen, close, open } = useModal();
  const { fetch } = useFetcher();

  const fetchNotifications = async type => {
    await fetch({
      app: 'notification',
      action: 'list',
      params: { type: NOTIFICATION_TYPES[type] },
      hideSuccess: true,
    });
  };

  const deleteNotification = async id => {
    const result = await fetch({
      app: 'notification',
      action: 'delete',
      params: { id: id },
    });

    if (result?.success) {
      closeModal();
      await fetchNotifications(type);
    } else {
      closeModal();
    }
  };

  const openModal = id => {
    selectedNotificationId.value = id;
    open();
  };

  const closeModal = () => {
    selectedNotificationId.value = null;
    close();
  };

  onMounted(async () => {
    await fetchNotifications(type);
  });

  return {
    isOpen,
    selectedNotificationId,

    deleteNotification,
    openModal,
    closeModal,
  };
}
