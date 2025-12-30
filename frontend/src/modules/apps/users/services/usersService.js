import { CoreService } from '@/modules/shared/common/services/core/coreService';

export class UsersService extends CoreService {
  getUsers() {
    return this.axios.get(`/users/`, {
      headers: this._getHeaders(),
    });
  }
}
