export function useResponseBuilder() {
  const successResponse = message => ({
    success: true,
    message,
  });

  const errorResponse = (messageError, allowRetry) => ({
    success: false,
    messageError,
    allowRetry,
  });

  return { successResponse, errorResponse };
}
