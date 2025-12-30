import { useFormatErrors } from '@/modules/shared/common/composables/errors/useFormatErrors';
import { useExtractErrors } from '@/modules/shared/common/composables/errors/useExtractErrors';
import { useResponseBuilder } from '@/modules/shared/common/composables/api/responses/useResponseBuilder';

export function useSessionErrorHandler() {
  const { getError } = useExtractErrors();
  const { formatError } = useFormatErrors();
  const { errorResponse } = useResponseBuilder();

  const handleError = ({
    error,
    fallbackMessage = 'Unexpected error occurred.',
    allowRetry = false,
  }) => {
    const errorData = error?.response?.data;

    if (errorData) {
      const extracted = getError(errorData);
      const formatted = formatError(extracted);
      return errorResponse(formatted, allowRetry);
    }

    return errorResponse(fallbackMessage, allowRetry);
  };

  const handleStatusError = ({
    message = 'Unexpected status error ocurred.',
    allowRetry = false,
  }) => {
    return errorResponse(message, allowRetry);
  };

  return {
    handleError,
    handleStatusError,
  };
}
