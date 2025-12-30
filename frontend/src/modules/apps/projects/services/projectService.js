import { CoreService } from '@/modules/shared/common/services/core/coreService';

export class ProjectService extends CoreService {
  getProjects({ privacy = null, name = null }) {
    const params = {};

    if (privacy) params.privacy = privacy;
    if (name) params.name = name;

    return this.axios.get('/projects/', {
      headers: this._getHeaders(),
      params,
    });
  }

  getProject(id) {
    return this.axios.get(`/projects/${id}/`, {
      headers: this._getHeaders(),
    });
  }

  createProject(name, description, privacy, users) {
    const data = {
      name,
      description,
      privacy,
      ...(users && users.length ? { users } : {}),
    };

    return this.axios.post('/projects/', data, {
      headers: this._getHeaders(),
    });
  }

  createProjectDocument(projectId, format, bodyPrompt) {
    const data = {
      project: projectId,
      body_prompt: bodyPrompt,
      format,
    };

    return this.axios.post('/documents_contexts/', data, {
      headers: this._getHeaders(),
    });
  }

  voteProjectDocument(documentId, rating) {
    const data = {
      document: documentId,
      rating,
    };

    return this.axios.post('/documents_feedbacks/', data, {
      headers: this._getHeaders(),
    });
  }

  getProjectDocuments(projectId = null) {
    const params = {};

    if (projectId) params.project_id = projectId;

    return this.axios.get('/documents/', {
      headers: this._getHeaders(),
      params,
    });
  }

  updateProject(id, name, description, privacy, users_to_exclude, users_to_add) {
    const data = {
      id,
      name,
      description,
      privacy,
      ...(users_to_exclude && users_to_exclude.length ? { users_to_exclude } : {}),
      ...(users_to_add && users_to_add.length ? { users_to_add } : {}),
    };

    return this.axios.put(`/projects/${id}/`, data, {
      headers: this._getHeaders(),
    });
  }

  deleteProject(id) {
    return this.axios.delete(`/projects/${id}/`, {
      headers: this._getHeaders(),
    });
  }

  confirmInvitationCode(invitationCode) {
    const data = {
      invitation_code: invitationCode,
    };

    return this.axios.post(`/projects/confirm-invitation-code/`, data, {
      headers: this._getHeaders(),
    });
  }

  addUser(projectsSelected, user) {
    const data = {
      projects_selected: projectsSelected,
      user,
    };

    return this.axios.post('/projects/add-user/', data, {
      headers: this._getHeaders(),
    });
  }
}
