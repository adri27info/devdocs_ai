import { useResponseMessages } from '@/modules/shared/common/composables/api/responses/useResponseMessages';

const { createMessagesWithStatuses } = useResponseMessages();

export const STATUSES = {
  SUCCESS: {
    OK: 200,
    CREATED: 201,
    NO_CONTENT: 204,
  },
  ERROR: {
    BAD_REQUEST: 400,
    NOT_FOUND: 404,
    METHOD_NOT_ALLOWED: 405,
    CONFLICT: 409,
    UNSUPPORTED_MEDIA_TYPE: 415,
    INTERNAL_SERVER_ERROR: 500,
    GATEWAY_TIMEOUT: 504,
  },
  PERMISSION: {
    UNAUTHORIZED: 401,
    FORBIDDEN: 403,
  },
};

export const PERMISSIONS = {
  UNAUTHORIZED: {
    NO_CREDENTIALS: 'Authentication credentials were not provided.',
    EXPIRED_ACCESS: 'Access token is invalid or has expired.',
  },
  FORBIDDEN: {
    INVALID_REFRESH: 'Invalid refresh token: token missing or expired.',
    INVALID_CSRF: 'Invalid csrf token: missing, expired or mismatch.',
  },
};

export const NORMAL_MESSAGES = {
  LOGIN: ['Logged in successfully.', 'Login failed.'],
  REGISTER: ['User registered. Check your email shortly for activation code.', 'Register failed.'],
  ACTIVATE_ACCOUNT: ['User account successfully activated.', 'Activation user account failed.'],
  RESEND_ACTIVATION_CODE: [
    'Activation code has been sent. Check your email.',
    'Failed to resend activation code. Please try again later.',
  ],
  LOGOUT: ['Refresh token has been blacklisted.', 'Logout failed.'],
  RESET_PASSWORD: [
    'Password reset link generated. Check your email.',
    'Failed to send password reset email.',
  ],
  RESET_PASSWORD_CONFIRM: [
    'Password reset successfully. Email will be sent shortly.',
    'Failed to reset password.',
  ],
  ASSISTANCE: [
    'Notification created successfully. The admin will contact you shortly.',
    'Failed to create assistance notification.',
  ],
  USER_ID: ['User id retrieved successfully.', 'Failed to retrieve user id.'],
  USER_STATS: ['User stats retrieved successfully.', 'Failed to retrieve user stats.'],
  USER_RETRIEVE: ['User retrieved successfully.', 'Failed to retrieve user.'],
  USER_UPDATE: ['User updated successfully.', 'Failed to update user.'],
  USER_UPDATE_PASSWORD: ['Password changed successfully.', 'Failed to update password.'],
  USER_DELETE: ['User deleted successfully.', 'Failed to delete user.'],
  USER_RESET_CACHE: ['Cache key reset successfully.', 'Failed to reset cache key.'],
  USER_SESSION_ACTIVITY: [
    'Session activity retrieved successfully.',
    'Failed to retrieve session activity.',
  ],
  USERS_LIST: ['Users listed successfully.', 'Failed to list users.'],
  LLM: ['LLM model retrieved successfully.', 'Failed to retrieve llm model'],
  PROJECTS_LIST: ['Projects listed successfully.', 'Failed to list projects'],
  PROJECT_RETRIEVE: ['Project retrieved successfully.', 'Failed to retrive project'],
  PROJECT_CREATE: ['Project created successfully.', 'Failed to create project'],
  PROJECT_UPDATE: ['Project updated successfully.', 'Failed to update project'],
  PROJECT_DELETE: ['Project deleted successfully.', 'Failed to delete project'],
  PROJECT_CONFIRM: ['Invitation code validated successfully.', 'Failed to confirm invitation code'],
  PROJECT_ADD_USER: ['User added successfully.', 'Failed to add user to the project'],
  PROJECT_DOCUMENT_CREATE: [
    'Documentation generated successfully.',
    'Failed to create documentation',
  ],
  PROJECT_DOCUMENT_VOTE: ['Vote generated successfully.', 'Failed to vote'],
  PROJECT_DOCUMENT_LIST: ['Documents listed successfully.', 'Failed to list documents'],
  NOTIFICATIONS_LIST: ['Notifications listed successfully.', 'Failed to list notifications'],
  NOTIFICATION_DELETE: ['Notification deleted successfully.', 'Failed to delete notification'],
  PAYMENT_SESSION: ['Payment session created successfully.', 'Failed to create payment session.'],
  PAYMENT_STATUS: ['Payment status proccesed successfully.', 'Failed to retrieved payment status.'],
  PAYMENT_INVOICE: ['Invoice retrieved successfully.', 'Failed to retrieve payment invoice.'],
};

const ERROR_MESSAGES = {
  FORCE_LOGOUT: [
    'Authentication cookies cleared.',
    'Failed to clear session cookies during forced logout.',
  ],
  REFRESH_TOKENS: ['Tokens successfully generated.', 'Refresh token refresh failed.'],
  REFRESH_CSRF_TOKEN: ['CSRF token refreshed.', 'CSRF token refresh failed.'],
};

export const NORMAL_FLOW = Object.fromEntries(
  Object.entries(NORMAL_MESSAGES).map(([key, [successMsg, errorMsg]]) => [
    key,
    {
      ...createMessagesWithStatuses({ successMsg, errorMsg }),
      ...(key === 'LOGOUT' ? { SUCCESS_CUSTOM: 'Logout successfully.' } : {}),
    },
  ]),
);

export const ERROR_FLOW = Object.fromEntries(
  Object.entries(ERROR_MESSAGES).map(([key, [successMsg, errorMsg]]) => [
    key,
    createMessagesWithStatuses({ successMsg, errorMsg }),
  ]),
);

export const OPS = {
  NAMES: Object.fromEntries(
    Object.keys(NORMAL_MESSAGES)
      .concat(Object.keys(ERROR_MESSAGES))
      .map(key => [key, key]),
  ),
  NORMAL_FLOW,
  ERROR_FLOW,
};

export const OPS_RESPONSES = Object.fromEntries(
  Object.keys(OPS.NAMES).map(opKey => [opKey, OPS.NORMAL_FLOW[opKey] || OPS.ERROR_FLOW[opKey]]),
);
