export function useInputTextValidator(validations) {
  function validateText(fieldName, value, maxLength) {
    if (value === undefined || value === null) {
      return validations.REQUIRED(fieldName);
    }

    if (value.trim() === '') {
      return validations.BLANK(fieldName);
    }

    if (maxLength && value.length > maxLength) {
      return validations.MAX_LENGTH(fieldName, maxLength);
    }

    return '';
  }

  return { validateText };
}
