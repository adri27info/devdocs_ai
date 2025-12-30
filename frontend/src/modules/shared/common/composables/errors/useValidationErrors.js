export function useValidationErrors() {
  const errors = {};

  function addError(field, message) {
    if (!errors[field]) errors[field] = [];

    errors[field].push(message);
  }

  function getErrors() {
    return errors;
  }

  return {
    addError,
    getErrors,
  };
}
