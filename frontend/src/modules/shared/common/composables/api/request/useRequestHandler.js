import { AuthService } from '@/modules/apps/auth/services/authService';
import { ResponseApiHelper } from '@/modules/shared/common/helpers/api/responses/responseApiHelper';
import { useResponseBuilder } from '@/modules/shared/common/composables/api/responses/useResponseBuilder';
import { useSessionErrorHandler } from '@/modules/shared/common/composables/session/useSessionErrorHandler';
import { useSessionChecker } from '@/modules/shared/common/composables/session/useSessionChecker';
import { useSessionRecovery } from '@/modules/shared/common/composables/session/useSessionRecovery';
import { useRequestBuilder } from '@/modules/shared/common/composables/api/request/useRequestBuilder';
import { authStore } from '@/modules/apps/auth/stores/authStore';

export function useRequestHandler() {
  const REFRESH_TOKENS = ResponseApiHelper.OPS.NAMES.REFRESH_TOKENS;
  const REFRESH_CSRF_TOKEN = ResponseApiHelper.OPS.NAMES.REFRESH_CSRF_TOKEN;
  const FORCE_LOGOUT = ResponseApiHelper.OPS.NAMES.FORCE_LOGOUT;
  const UNAUTHORIZED = ResponseApiHelper.STATUSES.PERMISSION.UNAUTHORIZED;
  const FORBIDDEN = ResponseApiHelper.STATUSES.PERMISSION.FORBIDDEN;
  const UNAUTHORIZED_NO_CREDENTIALS = ResponseApiHelper.PERMISSIONS.UNAUTHORIZED.NO_CREDENTIALS;
  const UNAUTHORIZED_EXPIRED_ACCESS = ResponseApiHelper.PERMISSIONS.UNAUTHORIZED.EXPIRED_ACCESS;
  const FORBIDDEN_INVALID_REFRESH = ResponseApiHelper.PERMISSIONS.FORBIDDEN.INVALID_REFRESH;
  const FORBIDDEN_INVALID_CSRF = ResponseApiHelper.PERMISSIONS.FORBIDDEN.INVALID_CSRF;

  const storeAuth = authStore();
  const authService = new AuthService();

  const { successResponse } = useResponseBuilder();
  const { handleError, handleStatusError } = useSessionErrorHandler();
  const { checkIsAuthenticated } = useSessionChecker();
  const { processRecoveryFlow } = useSessionRecovery();
  const { executeAndValidateRequest } = useRequestBuilder();

  const handleAPIRequest = async ({
    checkAuth = true,
    actions = {},
    request = {},
    expectedStatus = 200,
    operation = '',
    customExpectedMessage = '',
    keepAliveApp = true,
    fnToRetry = null,
    allowRetry = false,
  }) => {
    if (checkAuth) {
      if (!checkIsAuthenticated()) return;
    }

    const { beforeRequest, afterRequest, onFinally } = actions;

    try {
      await beforeRequest?.();

      const { isValid, expectedContent, actualMessage, data } = await executeAndValidateRequest(
        operation,
        expectedStatus,
        request,
      );

      if (isValid) {
        await afterRequest?.(data);
        return successResponse(customExpectedMessage || actualMessage);
      }

      return handleStatusError({
        message: expectedContent?.error?.MESSAGE,
        allowRetry: allowRetry,
      });
    } catch (error) {
      if (keepAliveApp) return await handleAPIRequestError(error, operation, fnToRetry, allowRetry);

      return handleError({ error: error, allowRetry: allowRetry });
    } finally {
      await onFinally?.();
    }
  };

  const handleAPIRequestError = async (error, baseOperation, fnToRetry, allowRetry) => {
    const status = error?.response?.status;
    const detail = error?.response?.data?.detail;

    const recoveryMap = [
      {
        status: UNAUTHORIZED,
        details: [UNAUTHORIZED_NO_CREDENTIALS, UNAUTHORIZED_EXPIRED_ACCESS],
        operation: REFRESH_TOKENS,
        expectedStatus: 200,
        valueClearSession: false,
        requestFn: () => authService.refreshTokenUser(),
      },
      {
        status: FORBIDDEN,
        details: [FORBIDDEN_INVALID_CSRF],
        operation: REFRESH_CSRF_TOKEN,
        expectedStatus: 200,
        valueClearSession: false,
        requestFn: () => authService.refreshCSRFTokenUser(),
      },
      {
        status: FORBIDDEN,
        details: [FORBIDDEN_INVALID_REFRESH],
        operation: FORCE_LOGOUT,
        expectedStatus: 200,
        valueClearSession: true,
        requestFn: () => authService.forceLogoutUser(),
      },
    ];

    const recoveryCase = recoveryMap.find(
      item => item.status === status && item.details.includes(detail),
    );

    if (recoveryCase) {
      return processRecoveryFlow({ ...recoveryCase, baseOperation, fnToRetry });
    }

    storeAuth.shouldClearSession = !allowRetry;
    return handleError({ error: error, allowRetry: allowRetry });
  };

  return {
    handleAPIRequest,
    handleAPIRequestError,
  };
}
