import {
  createLoadersFactory,
  createRedirectsFactory,
  createBtnDisablerFactory,
} from '@/modules/shared/common/factories/core/coreFactory';
import {
  createUserFactory,
  createUserSessionActivityFactory,
  createUsersFactory,
  createUserStatsFactory,
} from '@/modules/apps/users/factories/usersFactory';
import { createLLMFactory } from '@/modules/apps/llm/factories/llmFactory';
import { createPaymentFactory } from '@/modules/apps/settings/payment/factories/paymentFactory';
import { createProjectFactory } from '@/modules/apps/projects/factories/projectFactory';
import { createProjectsListFactory } from '@/modules/apps/projects/factories/projectListFactory';
import { createProjectDocumentsListFactory } from '@/modules/apps/projects/factories/projectDocumentListFactory';
import { createNotificationsFactory } from '@/modules/apps/notifications/factories/notificationFactory';
import { coreStore } from '@/modules/shared/common/stores/core/coreStore';
import { userStore } from '@/modules/apps/users/stores/userStore';
import { usersStore } from '@/modules/apps/users/stores/usersStore';
import { llmStore } from '@/modules/apps/llm/stores/llmStore';
import { settingStore } from '@/modules/apps/settings/stores/settingStore';
import { projectStore } from '@/modules/apps/projects/stores/projectStore';
import { notificationStore } from '@/modules/apps/notifications/stores/notificationStore';

export function useObjectResetter() {
  const storeCore = coreStore();
  const storeUser = userStore();
  const storeUsers = usersStore();
  const storeLLM = llmStore();
  const storeSetting = settingStore();
  const storeProject = projectStore();
  const storeNotification = notificationStore();

  const storesToReset = [
    {
      store: storeCore,
      props: [
        { prop: 'loaders', factory: createLoadersFactory },
        { prop: 'redirects', factory: createRedirectsFactory },
        { prop: 'btnDisablers', factory: createBtnDisablerFactory },
      ],
    },
    {
      store: storeUser,
      props: [
        { prop: 'userFactory', factory: createUserFactory },
        { prop: 'userStatsFactory', factory: createUserStatsFactory },
        { prop: 'userSessionActivityFactory', factory: createUserSessionActivityFactory },
      ],
    },
    {
      store: storeUsers,
      props: [{ prop: 'usersFactory', factory: createUsersFactory }],
    },
    {
      store: storeLLM,
      props: [{ prop: 'llmFactory', factory: createLLMFactory }],
    },
    {
      store: storeSetting,
      props: [{ prop: 'paymentFactory', factory: createPaymentFactory }],
    },
    {
      store: storeProject,
      props: [
        { prop: 'projectFactory', factory: createProjectFactory },
        { prop: 'projectsListFactory', factory: createProjectsListFactory },
        { prop: 'projectDocumentsListFactory', factory: createProjectDocumentsListFactory },
      ],
    },
    {
      store: storeNotification,
      props: [{ prop: 'notificationsFactory', factory: createNotificationsFactory }],
    },
  ];

  const resetObjects = () => {
    storesToReset.forEach(({ store, props }) => {
      props.forEach(({ prop, factory }) => {
        if (store[prop]) {
          Object.assign(store[prop], factory());
        }
      });
    });
  };

  return {
    resetObjects,
  };
}
