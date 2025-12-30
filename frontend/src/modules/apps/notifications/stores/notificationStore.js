import { reactive, toRefs } from 'vue';
import { defineStore } from 'pinia';
import { createNotificationsFactory } from '@/modules/apps/notifications/factories/notificationFactory';
import { NotificationService } from '@/modules/apps/notifications/services/notificationService';
import { useSessionCleaner } from '@/modules/shared/common/composables/session/useSessionCleaner';
import { useRequestHandler } from '@/modules/shared/common/composables/api/request/useRequestHandler';
import { useDelay } from '@/modules/shared/common/composables/utils/useDelay';
import { coreStore } from '@/modules/shared/common/stores/core/coreStore';

export const notificationStore = defineStore('notificationStore', () => {
  const notificationService = new NotificationService();
  const storeCore = coreStore();

  const notificationsFactory = reactive(createNotificationsFactory());

  const loadersRefs = toRefs(storeCore.loaders);
  const btnRefs = toRefs(storeCore.btnDisablers);

  const { delay } = useDelay();
  const { clearSessionIsNeeded } = useSessionCleaner();
  const { handleAPIRequest } = useRequestHandler();

  const getNotifications = type => {
    return handleAPIRequest({
      actions: {
        beforeRequest: () => {
          loadersRefs.notifications.value = true;
        },
        afterRequest: data => {
          if (data?.notifications?.list) {
            Object.assign(notificationsFactory, data.notifications);
          }
        },
        onFinally: async () => {
          clearSessionIsNeeded();
          await delay();
          loadersRefs.notifications.value = false;
        },
      },
      request: () => notificationService.getNotifications(type),
      expectedStatus: 200,
      operation: 'NOTIFICATIONS_LIST',
      fnToRetry: () => getNotifications(type),
      allowRetry: true,
    });
  };

  const deleteNotification = id => {
    return handleAPIRequest({
      actions: {
        beforeRequest: () => {
          loadersRefs.notificationDelete.value = true;
          btnRefs.notificationDeleteBtn.value = true;
        },
        onFinally: async () => {
          clearSessionIsNeeded();
          await delay();
          loadersRefs.notificationDelete.value = false;
          btnRefs.notificationDeleteBtn.value = false;
        },
      },
      request: () => notificationService.deleteNotification(id),
      expectedStatus: 200,
      operation: 'NOTIFICATION_DELETE',
      fnToRetry: () => deleteNotification(id),
      allowRetry: true,
    });
  };

  return {
    notificationsFactory,

    getNotifications,
    deleteNotification,
  };
});
