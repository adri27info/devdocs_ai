import { InvalidCoreParamTypeError } from '@/modules/shared/common/exceptions/invalidCoreParamTypeError';
import { MissingCoreParamError } from '@/modules/shared/common/exceptions/missingCoreParamError';
import { useTypeCheck } from '@/modules/shared/common/composables/utils/useTypeCheck';

class CoreParamErrorValidatorClass {
  constructor() {
    const { isType } = useTypeCheck();
    this.isType = isType;
  }

  validateParam(param, allowedValues = null) {
    if (!this.isType(param, 'string')) {
      throw new InvalidCoreParamTypeError();
    }

    if (!param.trim()) {
      throw new MissingCoreParamError();
    }

    if (allowedValues && !allowedValues.includes(param)) {
      throw new InvalidCoreParamTypeError(
        `Invalid value: ${param}. Valid options are: ${allowedValues.join(', ')}`,
      );
    }
  }
}

export const CoreParamErrorValidator = new CoreParamErrorValidatorClass();
