import { useTypeCheck } from '@/modules/shared/common/composables/utils/useTypeCheck';

export function useExtractErrors() {
  const { isType, isInstanceOf } = useTypeCheck();

  function extractError(errors) {
    if (!errors || !isType(errors, 'object')) return [];

    const messages = [];

    function recurse(value) {
      if (isType(value, 'string')) {
        messages.push(value);
      } else if (isInstanceOf(value, Array)) {
        value.forEach(recurse);
      } else if (isType(value, 'object') && value !== null) {
        Object.values(value).forEach(recurse);
      }
    }

    recurse(errors);
    return messages.filter(msg => msg !== null && msg !== undefined);
  }

  function getError(errors) {
    const result = extractError(errors);
    return result.length === 1 ? result[0] : result;
  }

  return {
    extractError,
    getError,
  };
}
