import { createRouter, createWebHistory } from 'vue-router';
import { routes } from '@/modules/router/routes';
import { ROLES } from '@/modules/shared/common/constants/utils/roles';
import { REDIRECTION_ROUTES } from '@/modules/shared/common/constants/utils/redirection_routes';
import { authStore } from '@/modules/apps/auth/stores/authStore';
import { userStore } from '@/modules/apps/users/stores/userStore';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const storeAuth = authStore();
  const storeUser = userStore();

  if (storeAuth.isAuthenticated && !storeUser.userFactory.id) {
    await storeUser.getUserId();
  }

  const userRole = storeUser.userFactory.role.name;
  const requiresAuth = to.meta.requiresAuth === true;
  const allowedRoles = to.meta.roles;

  if (requiresAuth && !storeAuth.isAuthenticated) {
    return next({ name: REDIRECTION_ROUTES.DEFAULT });
  }

  if (requiresAuth && !allowedRoles.includes(userRole)) {
    return next({
      name:
        userRole === ROLES.ADMIN
          ? REDIRECTION_ROUTES.ADMIN_AFTER_LOGIN
          : REDIRECTION_ROUTES.USER_AFTER_LOGIN,
    });
  }

  if (!requiresAuth && storeAuth.isAuthenticated) {
    if (userRole === ROLES.ADMIN) return next({ name: REDIRECTION_ROUTES.ADMIN_AFTER_LOGIN });
    if (userRole === ROLES.USER) return next({ name: REDIRECTION_ROUTES.USER_AFTER_LOGIN });
  }

  return next();
});

export default router;
