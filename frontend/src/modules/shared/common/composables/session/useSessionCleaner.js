import { authStore } from '@/modules/apps/auth/stores/authStore';

export function useSessionCleaner() {
  const storeAuth = authStore();

  const clearSession = () => {
    storeAuth.isAuthenticated = false;
  };

  const clearSessionIsNeeded = () => {
    if (storeAuth.shouldClearSession) {
      clearSession();
      storeAuth.shouldClearSession = false;
    }
  };

  return {
    clearSession,
    clearSessionIsNeeded,
  };
}
