import { CoreService } from '@/modules/shared/common/services/core/coreService';

export class UserService extends CoreService {
  getUser(id) {
    return this.axios.get(`/users/${id}/`, {
      headers: this._getHeaders(),
    });
  }

  getUserId() {
    return this.axios.get('/users/me/', {
      headers: this._getHeaders(),
    });
  }

  getUserStats() {
    return this.axios.get('/users/me/stats/', {
      headers: this._getHeaders(),
    });
  }

  updateUser(id, firstName, lastName, attachment = null) {
    const fields = {
      first_name: firstName,
      last_name: lastName,
      ...(attachment ? { attachment } : {}),
    };

    return this.requestUtil.sendData(`/users/${id}/`, fields, 'patch');
  }

  updateUserPassword(id, currentPassword, newPassword) {
    const data = {
      current_password: currentPassword,
      new_password: newPassword,
    };

    return this.axios.patch(`/users/${id}/change-password/`, data, {
      headers: this._getHeaders(),
    });
  }

  deleteUser(id) {
    return this.axios.delete(`/users/${id}/`, {
      headers: this._getHeaders(),
    });
  }

  resetCache(email, resetReason) {
    const data = {
      email,
      reset_reason: resetReason,
    };

    return this.axios.post(`/administrator/reset-cache/`, data, {
      headers: this._getHeaders(),
    });
  }

  getSessionActivity() {
    return this.axios.get('/administrator/session-activity/', {
      headers: this._getHeaders(),
    });
  }
}
