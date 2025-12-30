import { AuthService } from '@/modules/apps/auth/services/authService';
import { ResponseApiHelper } from '@/modules/shared/common/helpers/api/responses/responseApiHelper';
import { useResponseBuilder } from '@/modules/shared/common/composables/api/responses/useResponseBuilder';
import { authStore } from '@/modules/apps/auth/stores/authStore';

export function useSessionForceLogout() {
  const CUSTOM_LOGOUT_MESSAGE = ResponseApiHelper.OPS.NORMAL_FLOW.LOGOUT.SUCCESS_CUSTOM;

  const storeAuth = authStore();
  const authService = new AuthService();

  const { successResponse } = useResponseBuilder();

  const forceLogoutAndMarkSession = async () => {
    try {
      await authService.forceLogoutUser();
      storeAuth.shouldClearSession = true;
      return successResponse(CUSTOM_LOGOUT_MESSAGE);
    } catch {
      storeAuth.shouldClearSession = true;
      return successResponse(CUSTOM_LOGOUT_MESSAGE);
    }
  };

  return {
    forceLogoutAndMarkSession,
  };
}
