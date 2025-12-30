import {
  STATUSES,
  PERMISSIONS,
  OPS,
  OPS_RESPONSES,
} from '@/modules/shared/common/constants/api/responses/responseApiConstants';
import { CoreParamErrorValidator } from '@/modules/shared/common/validators/core/coreParamErrorValidator';

class ResponseApiHelperClass {
  constructor() {
    this.STATUSES = STATUSES;
    this.PERMISSIONS = PERMISSIONS;
    this.OPS = OPS;
    this.OPS_RESPONSES = OPS_RESPONSES;
  }

  getContent(operation, expectedStatus) {
    CoreParamErrorValidator.validateParam(operation, Object.keys(this.OPS.NAMES));

    const entry = this.OPS_RESPONSES[operation];
    if (!entry) return null;

    const { SUCCESS, ERROR } = entry;
    let matched = null;

    if (Array.isArray(SUCCESS?.STATUS) && SUCCESS.STATUS.includes(expectedStatus)) {
      matched = SUCCESS;
    } else if (Array.isArray(ERROR?.STATUS) && ERROR.STATUS.includes(expectedStatus)) {
      matched = ERROR;
    }

    return { success: SUCCESS, error: ERROR, matched };
  }
}

export const ResponseApiHelper = new ResponseApiHelperClass();
