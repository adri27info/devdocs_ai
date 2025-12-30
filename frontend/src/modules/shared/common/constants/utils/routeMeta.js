export const guestMeta = {
  requiresAuth: false,
  showAside: false,
  layoutCenter: true,
  headerType: 'guest',
};

export const userMeta = {
  requiresAuth: true,
  showAside: true,
  layoutCenter: false,
  headerType: 'user',
};

export const userOnlyMeta = {
  ...userMeta,
  roles: ['user'],
};

export const userAdminMeta = {
  ...userMeta,
  roles: ['user', 'admin'],
};

export const adminMeta = {
  ...userMeta,
  roles: ['admin'],
};
