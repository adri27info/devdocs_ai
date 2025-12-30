import { reactive, onMounted } from 'vue';
import { useFetcher } from '@/modules/shared/common/composables/utils/useFetcher';

export function useNotificationReset() {
  const resetLoaders = reactive({});

  const { fetch } = useFetcher();

  const resetCache = async (notificationId, email, resetReason) => {
    ensureLoader(notificationId);

    resetLoaders[notificationId] = true;

    try {
      const result = await fetch({
        app: 'user',
        action: 'resetCache',
        params: {
          email: email,
          resetReason: resetReason,
        },
      });

      if (result?.success) {
        const delResult = await fetch({
          app: 'notification',
          action: 'delete',
          params: {
            id: notificationId,
          },
        });

        if (delResult?.success) {
          await fetch({
            app: 'notification',
            action: 'list',
            params: { type: 'reset' },
            hideSuccess: true,
          });
        }
      }
    } finally {
      resetLoaders[notificationId] = false;
    }
  };

  const ensureLoader = notificationId => {
    if (!(notificationId in resetLoaders)) {
      resetLoaders[notificationId] = false;
    }
  };

  onMounted(async () => {
    await fetch({
      app: 'notification',
      action: 'list',
      params: { type: 'reset' },
      hideSuccess: true,
    });
  });

  return {
    resetLoaders,

    resetCache,
  };
}
