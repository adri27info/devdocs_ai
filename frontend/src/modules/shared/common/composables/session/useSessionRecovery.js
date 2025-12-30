import { ResponseApiHelper } from '@/modules/shared/common/helpers/api/responses/responseApiHelper';
import { useRequestBuilder } from '@/modules/shared/common/composables/api/request/useRequestBuilder';
import { useSessionErrorHandler } from '@/modules/shared/common/composables/session/useSessionErrorHandler';
import { useSessionForceLogout } from '@/modules/shared/common/composables/session/useSessionForceLogout';
import { authStore } from '@/modules/apps/auth/stores/authStore';

export function useSessionRecovery() {
  const OPERATION_LOGOUT = ResponseApiHelper.OPS.NAMES.LOGOUT;

  const storeAuth = authStore();

  const { executeAndValidateRequest } = useRequestBuilder();
  const { forceLogoutAndMarkSession } = useSessionForceLogout();
  const { handleStatusError } = useSessionErrorHandler();

  const processRecoveryFlow = async ({
    operation,
    expectedStatus,
    requestFn,
    valueClearSession,
    baseOperation,
    fnToRetry,
  }) => {
    try {
      const { isValid, expectedContent } = await executeAndValidateRequest(
        operation,
        expectedStatus,
        requestFn,
      );

      if (isValid) {
        storeAuth.shouldClearSession = valueClearSession;

        if (baseOperation === OPERATION_LOGOUT) return storeAuth.logoutUser();
        if (fnToRetry) return fnToRetry();

        return;
      }

      return handleStatusError(expectedContent?.error?.MESSAGE);
    } catch {
      return forceLogoutAndMarkSession();
    }
  };

  return { processRecoveryFlow };
}
