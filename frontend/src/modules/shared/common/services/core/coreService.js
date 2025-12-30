import { useAxios } from '@/modules/shared/common/composables/api/axios/useAxios';
import { useHeaders } from '@/modules/shared/common/composables/api/headers/useHeaders';
import { useRequestSendData } from '@/modules/shared/common/composables/api/request/useRequestSendData';

export class CoreService {
  constructor() {
    this.axios = useAxios();
    this.headersUtil = useHeaders();
    this.requestUtil = useRequestSendData(this.axios, this._getHeaders.bind(this));
  }

  _getHeaders(headerType = 'json') {
    return this.headersUtil.getHeaders(headerType);
  }
}
