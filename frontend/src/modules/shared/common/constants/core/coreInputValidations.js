export const VALIDATIONS = {
  REQUIRED: field => `${field} is required.`,
  BLANK: field => `${field} may not be blank.`,
  MAX_LENGTH: (field, max) => `${field} cannot exceed ${max} characters.`,
  EMAIL_INVALID: 'Enter a valid email address.',
  ATTACHMENT_MAX_SIZE: max => `The file must not exceed ${max} MB.`,
  ATTACHMENT_TYPE: 'Only JPG and PNG images are allowed.',
};
