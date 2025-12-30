import { useToast } from '@/modules/shared/common/composables/utils/ui/useToast';
import { useSessionCleaner } from '@/modules/shared/common/composables/session/useSessionCleaner';
import { authStore } from '@/modules/apps/auth/stores/authStore';

export function useSessionChecker() {
  const storeAuth = authStore();
  const { clearSession } = useSessionCleaner();
  const { showToast } = useToast();

  const checkIsAuthenticated = (message = 'You are not logged in.', toastType = 'error') => {
    if (!storeAuth.isAuthenticated) {
      clearSession();
      showToast(message, toastType);
      return false;
    }
    return true;
  };

  return { checkIsAuthenticated };
}
