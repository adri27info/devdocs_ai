import { CoreService } from '@/modules/shared/common/services/core/coreService';

export class NotificationService extends CoreService {
  getNotifications({ type = null }) {
    const params = {};

    if (type) params.type = type;

    return this.axios.get('/notifications/', {
      headers: this._getHeaders(),
      params,
    });
  }

  deleteNotification(id) {
    return this.axios.delete(`/notifications/${id}/`, {
      headers: this._getHeaders(),
    });
  }
}
