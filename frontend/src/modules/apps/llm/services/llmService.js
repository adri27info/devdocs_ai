import { CoreService } from '@/modules/shared/common/services/core/coreService';

export class LLMService extends CoreService {
  getLLM() {
    return this.axios.get('/llm/', {
      headers: this._getHeaders(),
    });
  }
}
