import { reactive, toRefs } from 'vue';
import { defineStore } from 'pinia';
import { useSessionCleaner } from '@/modules/shared/common/composables/session/useSessionCleaner';
import { useRequestHandler } from '@/modules/shared/common/composables/api/request/useRequestHandler';
import { useDelay } from '@/modules/shared/common/composables/utils/useDelay';
import { createProjectFactory } from '@/modules/apps/projects/factories/projectFactory';
import { createProjectsListFactory } from '@/modules/apps/projects/factories/projectListFactory';
import { createProjectDocumentsListFactory } from '@/modules/apps/projects/factories/projectDocumentListFactory';
import { ProjectService } from '@/modules/apps/projects/services/projectService';
import { coreStore } from '@/modules/shared/common/stores/core/coreStore';

export const projectStore = defineStore('projectStore', () => {
  const projectService = new ProjectService();
  const storeCore = coreStore();

  const projectFactory = reactive(createProjectFactory());
  const projectsListFactory = reactive(createProjectsListFactory());
  const projectDocumentsListFactory = reactive(createProjectDocumentsListFactory());

  const loadersRefs = toRefs(storeCore.loaders);
  const btnRefs = toRefs(storeCore.btnDisablers);

  const { delay } = useDelay();
  const { clearSessionIsNeeded } = useSessionCleaner();
  const { handleAPIRequest } = useRequestHandler();

  const getProjects = (privacy, name) => {
    return handleAPIRequest({
      actions: {
        beforeRequest: () => {
          loadersRefs.projects.value = true;
        },
        afterRequest: data => {
          if (data?.projects?.list) {
            Object.assign(projectsListFactory, data.projects);
          }
        },
        onFinally: async () => {
          clearSessionIsNeeded();
          await delay();
          loadersRefs.projects.value = false;
        },
      },
      request: () => projectService.getProjects(privacy, name),
      expectedStatus: 200,
      operation: 'PROJECTS_LIST',
      fnToRetry: () => getProjects(privacy, name),
      allowRetry: true,
    });
  };

  const getProject = id => {
    return handleAPIRequest({
      actions: {
        beforeRequest: () => {
          loadersRefs.project.value = true;
        },
        afterRequest: data => {
          if (data?.project) {
            Object.assign(projectFactory, data.project);
          }
        },
        onFinally: async () => {
          clearSessionIsNeeded();
          await delay();
          loadersRefs.project.value = false;
        },
      },
      request: () => projectService.getProject(id),
      expectedStatus: 200,
      operation: 'PROJECT_RETRIEVE',
      fnToRetry: () => getProject(id),
      allowRetry: true,
    });
  };

  const createProject = (name, description, privacy, users) => {
    return handleAPIRequest({
      actions: {
        beforeRequest: () => {
          loadersRefs.projectCreate.value = true;
          btnRefs.projectCreateBtn.value = true;
        },
        onFinally: async () => {
          clearSessionIsNeeded();
          await delay();
          loadersRefs.projectCreate.value = false;
          btnRefs.projectCreateBtn.value = false;
        },
      },
      request: () => projectService.createProject(name, description, privacy, users),
      expectedStatus: 201,
      operation: 'PROJECT_CREATE',
      fnToRetry: () => createProject(name, description, privacy, users),
      allowRetry: true,
    });
  };

  const createProjectDocument = (projectId, format, bodyPrompt) => {
    return handleAPIRequest({
      actions: {
        beforeRequest: () => {
          loadersRefs.projectDocumentCreate.value = true;
          btnRefs.projectDocumentCreateBtn.value = true;
        },
        onFinally: async () => {
          clearSessionIsNeeded();
          await delay();
          loadersRefs.projectDocumentCreate.value = false;
          btnRefs.projectDocumentCreateBtn.value = false;
        },
      },
      request: () => projectService.createProjectDocument(projectId, format, bodyPrompt),
      expectedStatus: 201,
      operation: 'PROJECT_DOCUMENT_CREATE',
      fnToRetry: () => createProjectDocument(projectId, format, bodyPrompt),
      allowRetry: true,
    });
  };

  const voteProjectDocument = (documentId, rating) => {
    return handleAPIRequest({
      actions: {
        beforeRequest: () => {
          loadersRefs.projectDocumentVote.value = true;
          btnRefs.projectDocumentVoteBtn.value = true;
        },
        onFinally: async () => {
          clearSessionIsNeeded();
          await delay();
          loadersRefs.projectDocumentVote.value = false;
          btnRefs.projectDocumentVoteBtn.value = false;
        },
      },
      request: () => projectService.voteProjectDocument(documentId, rating),
      expectedStatus: 201,
      operation: 'PROJECT_DOCUMENT_VOTE',
      fnToRetry: () => voteProjectDocument(documentId, rating),
      allowRetry: true,
    });
  };

  const getProjectDocuments = projectId => {
    return handleAPIRequest({
      actions: {
        beforeRequest: () => {
          loadersRefs.projectDocumentsList.value = true;
        },
        afterRequest: data => {
          if (data?.documents?.list) {
            Object.assign(projectDocumentsListFactory, data.documents);
          }
        },
        onFinally: async () => {
          clearSessionIsNeeded();
          await delay();
          loadersRefs.projectDocumentsList.value = false;
        },
      },
      request: () => projectService.getProjectDocuments(projectId),
      expectedStatus: 200,
      operation: 'PROJECT_DOCUMENT_LIST',
      fnToRetry: () => getProjectDocuments(projectId),
      allowRetry: true,
    });
  };

  const updateProject = (id, name, description, privacy, users_to_exclude, users_to_add) => {
    return handleAPIRequest({
      actions: {
        beforeRequest: () => {
          loadersRefs.projectUpdate.value = true;
          btnRefs.projectUpdateBtn.value = true;
        },
        onFinally: async () => {
          clearSessionIsNeeded();
          await delay();
          loadersRefs.projectUpdate.value = false;
          btnRefs.projectUpdateBtn.value = false;
        },
      },
      request: () =>
        projectService.updateProject(
          id,
          name,
          description,
          privacy,
          users_to_exclude,
          users_to_add,
        ),
      expectedStatus: 200,
      operation: 'PROJECT_UPDATE',
      fnToRetry: () =>
        updateProject(id, name, description, privacy, users_to_exclude, users_to_add),
      allowRetry: true,
    });
  };

  const deleteProject = id => {
    return handleAPIRequest({
      actions: {
        beforeRequest: () => {
          loadersRefs.projectDelete.value = true;
          btnRefs.projectDeleteBtn.value = true;
        },
        onFinally: async () => {
          clearSessionIsNeeded();
          await delay();
          loadersRefs.projectDelete.value = false;
          btnRefs.projectDeleteBtn.value = false;
        },
      },
      request: () => projectService.deleteProject(id),
      expectedStatus: 200,
      operation: 'PROJECT_DELETE',
      fnToRetry: () => deleteProject(id),
      allowRetry: true,
    });
  };

  const confirmInvitationCode = invitationCode => {
    return handleAPIRequest({
      actions: {
        beforeRequest: () => {
          btnRefs.projectConfirmBtn.value = true;
        },
        onFinally: async () => {
          clearSessionIsNeeded();
          await delay();
          btnRefs.projectConfirmBtn.value = false;
        },
      },
      request: () => projectService.confirmInvitationCode(invitationCode),
      expectedStatus: 200,
      operation: 'PROJECT_CONFIRM',
      fnToRetry: () => confirmInvitationCode(invitationCode),
      allowRetry: true,
    });
  };

  const addUser = (projectsSelected, user) => {
    return handleAPIRequest({
      actions: {
        beforeRequest: () => {
          loadersRefs.projectAddUser.value = true;
          btnRefs.projectAddUserBtn.value = true;
        },
        onFinally: async () => {
          clearSessionIsNeeded();
          await delay();
          loadersRefs.projectAddUser.value = false;
          btnRefs.projectAddUserBtn.value = false;
        },
      },
      request: () => projectService.addUser(projectsSelected, user),
      expectedStatus: 200,
      operation: 'PROJECT_ADD_USER',
      fnToRetry: () => addUser(projectsSelected, user),
      allowRetry: true,
    });
  };

  return {
    projectsListFactory,
    projectFactory,
    projectDocumentsListFactory,

    getProjects,
    getProject,
    createProject,
    createProjectDocument,
    voteProjectDocument,
    getProjectDocuments,
    updateProject,
    deleteProject,
    confirmInvitationCode,
    addUser,
  };
});
