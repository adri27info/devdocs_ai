import { useExtractErrors } from '@/modules/shared/common/composables/errors/useExtractErrors';
import { useTypeCheck } from '@/modules/shared/common/composables/utils/useTypeCheck';

export function useFormatErrors() {
  const { extractError } = useExtractErrors();
  const { isType, isInstanceOf } = useTypeCheck();

  const formatError = error => {
    if (!error) return '';

    if (isType(error, 'string')) return error;

    const processed = extractError(error);

    if (isInstanceOf(processed, Array)) {
      if (processed.length === 0) return '';
      if (processed.length === 1) return processed[0];
      return processed.join('\n');
    }

    return processed;
  };

  return {
    formatError,
  };
}
