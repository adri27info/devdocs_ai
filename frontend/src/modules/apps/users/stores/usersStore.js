import { reactive, toRefs } from 'vue';
import { defineStore } from 'pinia';
import { createUsersFactory } from '@/modules/apps/users/factories/usersFactory';
import { useSessionCleaner } from '@/modules/shared/common/composables/session/useSessionCleaner';
import { useRequestHandler } from '@/modules/shared/common/composables/api/request/useRequestHandler';
import { useDelay } from '@/modules/shared/common/composables/utils/useDelay';
import { UsersService } from '@/modules/apps/users/services/usersService';
import { coreStore } from '@/modules/shared/common/stores/core/coreStore';

export const usersStore = defineStore('usersStore', () => {
  const usersService = new UsersService();
  const storeCore = coreStore();

  const usersFactory = reactive(createUsersFactory());

  const loadersRefs = toRefs(storeCore.loaders);

  const { delay } = useDelay();
  const { clearSessionIsNeeded } = useSessionCleaner();
  const { handleAPIRequest } = useRequestHandler();

  const getUsers = () => {
    return handleAPIRequest({
      actions: {
        beforeRequest: () => {
          loadersRefs.overview.value = true;
        },
        afterRequest: data => {
          if (data?.users?.list) {
            Object.assign(usersFactory, data.users);
          }
        },
        onFinally: async () => {
          clearSessionIsNeeded();
          await delay();
          loadersRefs.overview.value = false;
        },
      },
      request: () => usersService.getUsers(),
      expectedStatus: 200,
      operation: 'USERS_LIST',
      fnToRetry: () => getUsers(),
      allowRetry: true,
    });
  };

  return {
    usersFactory,

    getUsers,
  };
});
