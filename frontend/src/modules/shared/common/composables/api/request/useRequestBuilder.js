import { ResponseApiHelper } from '@/modules/shared/common/helpers/api/responses/responseApiHelper';

export function useRequestBuilder() {
  const executeAndValidateRequest = async (operation, expectedStatus, requestFn) => {
    const expectedContent = ResponseApiHelper.getContent(operation, expectedStatus);
    const matched = expectedContent?.matched;

    const response = await requestFn();
    const actualStatus = response?.status;
    const data = response?.data;
    const actualMessage = response?.data?.message;

    const statusMatches = matched?.STATUS?.includes(actualStatus);
    const messageMatches = actualMessage === matched?.MESSAGE;
    const isValid = statusMatches && messageMatches;

    return {
      isValid,
      expectedContent,
      actualMessage,
      data,
    };
  };

  return {
    executeAndValidateRequest,
  };
}
