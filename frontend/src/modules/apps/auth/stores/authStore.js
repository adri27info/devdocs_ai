import { ref, toRefs } from 'vue';
import { defineStore } from 'pinia';
import { AuthService } from '@/modules/apps/auth/services/authService';
import { useDelay } from '@/modules/shared/common/composables/utils/useDelay';
import { useSessionCleaner } from '@/modules/shared/common/composables/session/useSessionCleaner';
import { useRequestHandler } from '@/modules/shared/common/composables/api/request/useRequestHandler';
import { coreStore } from '@/modules/shared/common/stores/core/coreStore';
import { userStore } from '@/modules/apps/users/stores/userStore';

export const authStore = defineStore(
  'authStore',
  () => {
    const authService = new AuthService();

    const storeCore = coreStore();
    const storeUser = userStore();

    const shouldClearSession = ref(false);
    const isAuthenticated = ref(false);

    const loadersRefs = toRefs(storeCore.loaders);
    const btnRefs = toRefs(storeCore.btnDisablers);

    const { delay } = useDelay();
    const { clearSessionIsNeeded } = useSessionCleaner();
    const { handleAPIRequest } = useRequestHandler();

    const loginUser = (email, password, rememberMe) => {
      return handleAPIRequest({
        checkAuth: false,
        actions: {
          beforeRequest: () => {
            loadersRefs.login.value = true;
            btnRefs.loginBtn.value = true;
          },
          afterRequest: data => {
            isAuthenticated.value = true;

            if (data?.user) {
              Object.assign(storeUser.userFactory, data.user);
            }
          },
          onFinally: async () => {
            await delay();
            loadersRefs.login.value = false;
            btnRefs.loginBtn.value = false;
          },
        },
        request: () => authService.loginUser(email, password, rememberMe),
        expectedStatus: 200,
        operation: 'LOGIN',
        keepAliveApp: false,
      });
    };

    const registerUser = (firstName, lastName, email, password, attachment) => {
      return handleAPIRequest({
        checkAuth: false,
        actions: {
          beforeRequest: () => {
            loadersRefs.register.value = true;
            btnRefs.registerBtn.value = true;
          },
          onFinally: async () => {
            await delay();
            loadersRefs.register.value = false;
            btnRefs.registerBtn.value = false;
          },
        },
        request: () => authService.registerUser(firstName, lastName, email, password, attachment),
        expectedStatus: 201,
        operation: 'REGISTER',
        keepAliveApp: false,
      });
    };

    const activateUserAccount = (email, activationCode) => {
      return handleAPIRequest({
        checkAuth: false,
        actions: {
          beforeRequest: () => {
            loadersRefs.activateAccount.value = true;
            btnRefs.activateAccountBtn.value = true;
          },
          onFinally: async () => {
            await delay();
            loadersRefs.activateAccount.value = false;
            btnRefs.activateAccountBtn.value = false;
          },
        },
        request: () => authService.activateUserAccount(email, activationCode),
        expectedStatus: 200,
        operation: 'ACTIVATE_ACCOUNT',
        keepAliveApp: false,
      });
    };

    const resendUserActivationCode = email => {
      return handleAPIRequest({
        checkAuth: false,
        actions: {
          beforeRequest: () => {
            loadersRefs.resendActivationCode.value = true;
            btnRefs.resendActivationCodeBtn.value = true;
          },
          onFinally: async () => {
            await delay();
            loadersRefs.resendActivationCode.value = false;
            btnRefs.resendActivationCodeBtn.value = false;
          },
        },
        request: () => authService.resendUserActivationCode(email),
        expectedStatus: 200,
        operation: 'RESEND_ACTIVATION_CODE',
        keepAliveApp: false,
      });
    };

    const logoutUser = () => {
      return handleAPIRequest({
        actions: {
          beforeRequest: () => {
            shouldClearSession.value = false;
          },
          afterRequest: () => {
            shouldClearSession.value = true;
          },
          onFinally: () => clearSessionIsNeeded(),
        },
        request: () => authService.logoutUser(),
        expectedStatus: 200,
        operation: 'LOGOUT',
        customExpectedMessage: 'Logged out successfully.',
      });
    };

    const resetUserPassword = email => {
      return handleAPIRequest({
        checkAuth: false,
        actions: {
          beforeRequest: () => {
            loadersRefs.resetPassword.value = true;
            btnRefs.resetPasswordBtn.value = true;
          },
          onFinally: async () => {
            await delay();
            loadersRefs.resetPassword.value = false;
            btnRefs.resetPasswordBtn.value = false;
          },
        },
        request: () => authService.resetUserPassword(email),
        expectedStatus: 200,
        operation: 'RESET_PASSWORD',
        keepAliveApp: false,
      });
    };

    const resetUserPasswordConfirm = (uid, token, password) => {
      return handleAPIRequest({
        checkAuth: false,
        actions: {
          beforeRequest: () => {
            loadersRefs.resetPasswordConfirm.value = true;
            btnRefs.resetPasswordConfirmBtn.value = true;
          },
          onFinally: async () => {
            await delay();
            loadersRefs.resetPasswordConfirm.value = false;
            btnRefs.resetPasswordConfirmBtn.value = false;
          },
        },
        request: () => authService.resetUserPasswordConfirm(uid, token, password),
        expectedStatus: 200,
        operation: 'RESET_PASSWORD_CONFIRM',
        keepAliveApp: false,
      });
    };

    const assistanceUser = (email, type, resetReason, messageReason) => {
      return handleAPIRequest({
        checkAuth: false,
        actions: {
          beforeRequest: () => {
            loadersRefs.assistance.value = true;
            btnRefs.assistanceBtn.value = true;
          },
          onFinally: async () => {
            await delay();
            loadersRefs.assistance.value = false;
            btnRefs.assistanceBtn.value = false;
          },
        },
        request: () => authService.assistanceUser(email, type, resetReason, messageReason),
        expectedStatus: 201,
        operation: 'ASSISTANCE',
        keepAliveApp: false,
      });
    };

    return {
      isAuthenticated,
      shouldClearSession,

      loginUser,
      registerUser,
      activateUserAccount,
      resendUserActivationCode,
      logoutUser,
      resetUserPassword,
      resetUserPasswordConfirm,
      assistanceUser,
    };
  },
  {
    persist: {
      pick: ['isAuthenticated'],
      storage: localStorage,
    },
  },
);
