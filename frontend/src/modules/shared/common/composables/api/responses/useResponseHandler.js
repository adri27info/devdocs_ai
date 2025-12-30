import { useToast } from '@/modules/shared/common/composables/utils/ui/useToast';
import { useSessionCleaner } from '@/modules/shared/common/composables/session/useSessionCleaner';

export function useResponseHandler() {
  const LOGOUT_MESSAGE = 'Logout successfully.';

  const { showToast } = useToast();
  const { clearSession } = useSessionCleaner();

  const handleResult = (result, { hideSuccess = false } = {}) => {
    if (!result) return;

    if (result.success && (!hideSuccess || result.message === LOGOUT_MESSAGE)) {
      showToast(result.message, 'success');
    }

    if (!result.success) {
      showToast(result.messageError, 'error');
      if (!result.allowRetry) clearSession();
    }
  };

  return { handleResult };
}
