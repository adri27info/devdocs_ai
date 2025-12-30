import { useResponseHandler } from '@/modules/shared/common/composables/api/responses/useResponseHandler';
import { authStore } from '@/modules/apps/auth/stores/authStore';
import { userStore } from '@/modules/apps/users/stores/userStore';
import { usersStore } from '@/modules/apps/users/stores/usersStore';
import { settingStore } from '@/modules/apps/settings/stores/settingStore';
import { llmStore } from '@/modules/apps/llm/stores/llmStore';
import { projectStore } from '@/modules/apps/projects/stores/projectStore';
import { notificationStore } from '@/modules/apps/notifications/stores/notificationStore';

export function useFetcher() {
  const storeAuth = authStore();
  const storeUser = userStore();
  const storeUsers = usersStore();
  const storeSetting = settingStore();
  const storeLLM = llmStore();
  const storeProject = projectStore();
  const storeNotification = notificationStore();

  const { handleResult } = useResponseHandler();

  const fetchers = {
    auth: {
      login: ({ email, password, rememberMe }) => storeAuth.loginUser(email, password, rememberMe),
      register: ({ firstName, lastName, email, password, attachment }) =>
        storeAuth.registerUser(firstName, lastName, email, password, attachment),
      activateAccount: ({ email, activationCode }) =>
        storeAuth.activateUserAccount(email, activationCode),
      resendActivationCode: ({ email }) => storeAuth.resendUserActivationCode(email),
      resetPassword: ({ email }) => storeAuth.resetUserPassword(email),
      resetPasswordConfirm: ({ uid, token, password }) =>
        storeAuth.resetUserPasswordConfirm(uid, token, password),
      assistance: ({ email, type, resetReason, messageReason }) =>
        storeAuth.assistanceUser(email, type, resetReason, messageReason),
    },
    user: {
      updateProfile: ({ id, firstName, lastName, attachment }) =>
        storeUser.updateUser(id, firstName, lastName, attachment),
      updateProfilePassword: ({ id, currentPassword, newPassword }) =>
        storeUser.updateUserPassword(id, currentPassword, newPassword),
      delete: ({ id, confirmationCode }) => storeUser.deleteUser(id, confirmationCode),
      resetCache: ({ email, resetReason }) => storeUser.resetCache(email, resetReason),
      stats: () => storeUser.getUserStats(),
      id: () => storeUser.getUserId(),
      sessionActivity: () => storeUser.getSessionActivity(),
    },
    setting: {
      session: () => storeSetting.getPaymentSession(),
      invoice: () => storeSetting.getPaymentInvoice(),
      status: ({ sessionId }) => storeSetting.getPaymentStatus(sessionId),
    },
    project: {
      create: ({ name, description, privacy, users }) =>
        storeProject.createProject(name, description, privacy, users),
      addUser: ({ projectsSelected, user }) => storeProject.addUser(projectsSelected, user),
      id: ({ projectId }) => storeProject.getProject(projectId),
      list: ({ privacy, name }) => storeProject.getProjects({ privacy, name }),
      update: ({ id, name, description, privacy, users_to_exclude, users_to_add }) =>
        storeProject.updateProject(id, name, description, privacy, users_to_exclude, users_to_add),
      delete: ({ id }) => storeProject.deleteProject(id),
      confirmInvitationCode: ({ invitationCode }) =>
        storeProject.confirmInvitationCode(invitationCode),
      createProjectDocument: ({ projectId, format, bodyPrompt }) =>
        storeProject.createProjectDocument(projectId, format, bodyPrompt),
      voteProjectDocument: ({ documentId, rating }) =>
        storeProject.voteProjectDocument(documentId, rating),
      documentList: projectId => storeProject.getProjectDocuments(projectId),
    },
    notification: {
      delete: ({ id }) => storeNotification.deleteNotification(id),
      list: ({ type }) => storeNotification.getNotifications({ type }),
    },
    users: () => storeUsers.getUsers(),
    llm: () => storeLLM.getLLM(),
  };

  const fetch = async ({ app, action, hideSuccess = false, params = {} } = {}) => {
    if (!fetchers[app]) return;

    let fn;

    if (typeof fetchers[app] === 'function') {
      fn = fetchers[app];
    } else if (action && fetchers[app][action]) {
      fn = fetchers[app][action];
    } else {
      return;
    }

    const result = await fn(params);
    handleResult(result, hideSuccess ? { hideSuccess: true } : undefined);

    return result;
  };

  return {
    fetch,
  };
}
