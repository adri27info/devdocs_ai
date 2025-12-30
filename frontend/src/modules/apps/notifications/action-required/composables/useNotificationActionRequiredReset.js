import { createNotificationActionRequiredFactory } from '@/modules/apps/notifications/action-required/factories/useActionRequiredFactory';

export function useNotificationActionRequiredReset() {
  const resetNotificationActionRequiredFactory = notificationActionRequiredFactory => {
    Object.assign(notificationActionRequiredFactory, createNotificationActionRequiredFactory());
  };

  return { resetNotificationActionRequiredFactory };
}
