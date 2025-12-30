import { CoreParamErrorHelper } from '@/modules/shared/common/helpers/core/exceptions/coreParamErrorHelper';

export class CoreError extends Error {
  constructor(message) {
    const messageStr = CoreParamErrorHelper.validateAndStringify(message);
    super(messageStr);

    this.name = 'CoreError';
    this.response = {
      data: message?.constructor === Object ? message : { detail: messageStr },
    };
  }
}
