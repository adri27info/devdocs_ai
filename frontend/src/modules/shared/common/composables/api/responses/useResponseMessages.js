import { STATUSES } from '@/modules/shared/common/constants/api/responses/responseApiConstants';

export function useResponseMessages() {
  const createMessagesWithStatuses = ({ successMsg, errorMsg }) => ({
    SUCCESS: {
      STATUS: Object.values(STATUSES.SUCCESS),
      MESSAGE: successMsg,
    },
    ERROR: {
      STATUS: Object.values(STATUSES.ERROR),
      MESSAGE: errorMsg,
    },
  });

  return { createMessagesWithStatuses };
}
