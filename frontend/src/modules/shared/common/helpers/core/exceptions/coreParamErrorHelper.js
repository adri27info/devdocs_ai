import { CoreParamErrorValidator } from '@/modules/shared/common/validators/core/coreParamErrorValidator';
import { useStringify } from '@/modules/shared/common/composables/utils/useStringify';

class CoreParamErrorHelperClass {
  constructor() {
    this.validator = CoreParamErrorValidator;
  }

  validateAndStringify(message) {
    const { stringify } = useStringify();
    const stringified = stringify(message);

    this.validator.validateParam(stringified);
    return stringified;
  }
}

export const CoreParamErrorHelper = new CoreParamErrorHelperClass();
