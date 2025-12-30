import { reactive, toRefs } from 'vue';
import { defineStore } from 'pinia';
import {
  createUserFactory,
  createUserStatsFactory,
  createUserSessionActivityFactory,
} from '@/modules/apps/users/factories/usersFactory';
import { useSessionCleaner } from '@/modules/shared/common/composables/session/useSessionCleaner';
import { useRequestHandler } from '@/modules/shared/common/composables/api/request/useRequestHandler';
import { useDelay } from '@/modules/shared/common/composables/utils/useDelay';
import { UserService } from '@/modules/apps/users/services/userService';
import { authStore } from '@/modules/apps/auth/stores/authStore';
import { coreStore } from '@/modules/shared/common/stores/core/coreStore';

export const userStore = defineStore('userStore', () => {
  const userService = new UserService();
  const storeAuth = authStore();
  const storeCore = coreStore();

  const userFactory = reactive(createUserFactory());
  const userStatsFactory = reactive(createUserStatsFactory());
  const userSessionActivityFactory = reactive(createUserSessionActivityFactory());

  const loadersRefs = toRefs(storeCore.loaders);
  const btnRefs = toRefs(storeCore.btnDisablers);

  const { delay } = useDelay();
  const { clearSessionIsNeeded } = useSessionCleaner();
  const { handleAPIRequest } = useRequestHandler();

  const getUser = id => {
    return handleAPIRequest({
      actions: {
        afterRequest: data => {
          if (data?.user) {
            Object.assign(userFactory, data.user);
          }
        },
        onFinally: () => clearSessionIsNeeded(),
      },
      request: () => userService.getUser(id),
      expectedStatus: 200,
      operation: 'USER_RETRIEVE',
      fnToRetry: () => getUser(id),
    });
  };

  const getUserId = () => {
    return handleAPIRequest({
      actions: {
        beforeRequest: () => {
          loadersRefs.profileUserInit.value = true;
        },
        afterRequest: async data => {
          if (data?.user?.id) {
            await getUser(data.user.id);
          }
        },
        onFinally: async () => {
          clearSessionIsNeeded();
          await delay();
          loadersRefs.profileUserInit.value = false;
        },
      },
      request: () => userService.getUserId(),
      expectedStatus: 200,
      operation: 'USER_ID',
      fnToRetry: () => getUserId(),
    });
  };

  const getUserStats = () => {
    return handleAPIRequest({
      actions: {
        beforeRequest: () => {
          loadersRefs.dashboard.value = true;
        },
        afterRequest: async data => {
          if (data?.stats) {
            Object.assign(userStatsFactory, data.stats);
          }
        },
        onFinally: async () => {
          clearSessionIsNeeded();
          await delay();
          loadersRefs.dashboard.value = false;
        },
      },
      request: () => userService.getUserStats(),
      expectedStatus: 200,
      operation: 'USER_STATS',
      fnToRetry: () => getUserStats(),
      allowRetry: true,
    });
  };

  const updateUser = (id, firstName, lastName, attachment = null) => {
    return handleAPIRequest({
      actions: {
        beforeRequest: () => {
          loadersRefs.profileUser.value = true;
          btnRefs.profileUserBtn.value = true;
        },
        afterRequest: data => {
          if (data?.user) {
            Object.assign(userFactory, data.user);
          }
        },
        onFinally: async () => {
          clearSessionIsNeeded();
          await delay();
          loadersRefs.profileUser.value = false;
          btnRefs.profileUserBtn.value = false;
        },
      },
      request: () => userService.updateUser(id, firstName, lastName, attachment),
      expectedStatus: 200,
      operation: 'USER_UPDATE',
      fnToRetry: () => updateUser(id, firstName, lastName, attachment),
      allowRetry: true,
    });
  };

  const updateUserPassword = (id, currentPassword, newPassword) => {
    return handleAPIRequest({
      actions: {
        beforeRequest: () => {
          loadersRefs.profileUserPassword.value = true;
          btnRefs.profileUserPasswordBtn.value = true;
        },
        onFinally: async () => {
          clearSessionIsNeeded();
          await delay();
          loadersRefs.profileUserPassword.value = false;
          btnRefs.profileUserPasswordBtn.value = false;
        },
      },
      request: () => userService.updateUserPassword(id, currentPassword, newPassword),
      expectedStatus: 200,
      operation: 'USER_UPDATE_PASSWORD',
      fnToRetry: () => updateUserPassword(id, currentPassword, newPassword),
      allowRetry: true,
    });
  };

  const deleteUser = (id, confirmationCode) => {
    return handleAPIRequest({
      actions: {
        beforeRequest: () => {
          loadersRefs.delete.value = true;
          btnRefs.deleteBtn.value = true;
        },
        afterRequest: () => {
          storeAuth.shouldClearSession = true;
        },
        onFinally: async () => {
          clearSessionIsNeeded();
          await delay();
          loadersRefs.delete.value = false;
          btnRefs.deleteBtn.value = false;
        },
      },
      request: () => userService.deleteUser(id, confirmationCode),
      expectedStatus: 200,
      operation: 'USER_DELETE',
      fnToRetry: () => deleteUser(id, confirmationCode),
      allowRetry: true,
    });
  };

  const resetCache = (email, resetReason) => {
    return handleAPIRequest({
      actions: {
        beforeRequest: () => {
          btnRefs.resetBtn.value = true;
        },
        onFinally: async () => {
          clearSessionIsNeeded();
          await delay();
          btnRefs.resetBtn.value = false;
        },
      },
      request: () => userService.resetCache(email, resetReason),
      expectedStatus: 200,
      operation: 'USER_RESET_CACHE',
      fnToRetry: () => resetCache(email, resetReason),
      allowRetry: true,
    });
  };

  const getSessionActivity = () => {
    return handleAPIRequest({
      actions: {
        beforeRequest: () => {
          loadersRefs.sessionActivity.value = true;
        },
        afterRequest: async data => {
          if (data?.activity.list) {
            Object.assign(userSessionActivityFactory, data.activity);
          }
        },
        onFinally: async () => {
          clearSessionIsNeeded();
          await delay();
          loadersRefs.sessionActivity.value = false;
        },
      },
      request: () => userService.getSessionActivity(),
      expectedStatus: 200,
      operation: 'USER_SESSION_ACTIVITY',
      fnToRetry: () => getSessionActivity(),
      allowRetry: true,
    });
  };

  return {
    userFactory,
    userStatsFactory,
    userSessionActivityFactory,

    getUser,
    getUserId,
    getUserStats,
    updateUser,
    updateUserPassword,
    deleteUser,
    resetCache,
    getSessionActivity,
  };
});
