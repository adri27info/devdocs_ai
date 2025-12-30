import { watch, reactive } from 'vue';
import { createNotificationActionRequiredFactory } from '@/modules/apps/notifications/action-required/factories/useActionRequiredFactory';
import { CoreInputValidator } from '@/modules/shared/common/validators/core/coreInputValidator';
import { useNotificationActionRequiredReset } from '@/modules/apps/notifications/action-required/composables/useNotificationActionRequiredReset';
import { useFetcher } from '@/modules/shared/common/composables/utils/useFetcher';
import { notificationStore } from '@/modules/apps/notifications/stores/notificationStore';

export function useNotificationActionRequired() {
  const storeNotification = notificationStore();

  const notificationActionRequiredFactory = reactive({});

  const projectConfirmLoaders = reactive({});

  const { fetch } = useFetcher();
  const { resetNotificationActionRequiredFactory } = useNotificationActionRequiredReset();

  const confirmProjectInvitationCode = async notificationId => {
    const state = ensureState(notificationId);

    if (validateInvitationCode(notificationId)) return;

    ensureLoader(notificationId);
    projectConfirmLoaders[notificationId] = true;

    try {
      const result = await fetch({
        app: 'project',
        action: 'confirmInvitationCode',
        params: { invitationCode: state.invitationCode },
      });

      if (result?.success) {
        const delResult = await fetch({
          app: 'notification',
          action: 'delete',
          params: { id: notificationId },
        });

        if (delResult?.success) {
          resetNotificationActionRequiredFactory(state);

          await fetch({
            app: 'notification',
            action: 'list',
            params: { type: 'action_required' },
            hideSuccess: true,
          });
        }
      }
    } finally {
      projectConfirmLoaders[notificationId] = false;
    }
  };

  const ensureState = notificationId => {
    const id = String(notificationId);

    if (!notificationActionRequiredFactory[id]) {
      notificationActionRequiredFactory[id] = createNotificationActionRequiredFactory();
    }

    return notificationActionRequiredFactory[id];
  };

  const ensureLoader = notificationId => {
    if (!(notificationId in projectConfirmLoaders)) {
      projectConfirmLoaders[notificationId] = false;
    }
  };

  const validateInvitationCode = notificationId => {
    ensureState(notificationId);
    const state = notificationActionRequiredFactory[notificationId];

    return (state.invitationCodeError = CoreInputValidator.validateInvitationCode(
      state.invitationCode,
    ));
  };

  watch(
    () => storeNotification.notificationsFactory.list,
    list => {
      list.forEach(n => {
        ensureState(n.id);
        ensureLoader(n.id);
      });
    },
    { immediate: true },
  );

  return {
    notificationActionRequiredFactory,
    projectConfirmLoaders,

    validateInvitationCode,
    confirmProjectInvitationCode,
  };
}
