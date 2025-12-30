export const REQUIREMENTS = {
  GENERAL: { TEXT: { MAX_LENGTH: 100 } },
  NAME: { MAX_LENGTH: 35 },
  FIRST_NAME: { MAX_LENGTH: 20 },
  LAST_NAME: { MAX_LENGTH: 50 },
  DESCRIPTION: { MAX_LENGTH: 255 },
  ACTIVATION_CODE: { MAX_LENGTH: 5 },
  CONFIRMATION_CODE: { MAX_LENGTH: 6 },
  INVITATION_CODE: { MAX_LENGTH: 12 },
  BODY_PROMPT: { MAX_LENGTH: 15000 },
  EMAIL: { MAX_LENGTH: 254, REGEX: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/ },
  PASSWORD: {
    MAX_LENGTH: 128,
    PATTERNS: [
      { regex: /^[\s\S]{8,20}$/, message: 'Password must be between 8 and 20 characters long.' },
      { regex: /[A-Z]/, message: 'Password must contain at least one uppercase letter.' },
      { regex: /\d/, message: 'Password must contain at least one number.' },
      { regex: /[\W_]/, message: 'Password must contain at least one special character.' },
      { regex: /^\S+$/, message: 'Password cannot contain spaces.' },
    ],
  },
  ATTACHMENT: { MAX_SIZE_MB: 5, ALLOWED_TYPES: ['image/jpeg', 'image/png'] },
};
