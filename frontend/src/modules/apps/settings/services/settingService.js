import { CoreService } from '@/modules/shared/common/services/core/coreService';

export class SettingService extends CoreService {
  getPaymentSession() {
    return this.axios.post('/payments/checkout_session/', {
      headers: this._getHeaders(),
    });
  }

  getPaymentStatus(sessionId) {
    return this.axios.get('/payments/status/', {
      headers: this._getHeaders(),
      params: { session_id: sessionId },
    });
  }

  getPaymentInvoice() {
    return this.axios.get('/invoices/', {
      headers: this._getHeaders(),
    });
  }
}
