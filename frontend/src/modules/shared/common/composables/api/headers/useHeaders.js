import { CoreParamErrorValidator } from '@/modules/shared/common/validators/core/coreParamErrorValidator';

export function useHeaders() {
  const headerTypes = ['json', 'form'];

  const headers = {
    json: {
      // Only in endpoints with json content required
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
    form: {
      // Only for endpoints requiring multipart/form-data
      // Content-Type is NOT set manually; Axios handles it automatically
      Accept: 'application/json',
    },
  };

  function getHeaders(headerType) {
    CoreParamErrorValidator.validateParam(headerType, headerTypes);
    return headers[headerType];
  }

  return { getHeaders };
}
