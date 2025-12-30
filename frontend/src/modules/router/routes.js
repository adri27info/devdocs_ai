import {
  guestMeta,
  userOnlyMeta,
  userAdminMeta,
  adminMeta,
} from '@/modules/shared/common/constants/utils/routeMeta';
import HomeView from '@/modules/apps/home/views/HomeView.vue';
import LoginView from '@/modules/apps/auth/login/views/LoginView.vue';
import RegisterView from '@/modules/apps/auth/register/views/RegisterView.vue';
import ActivateAccountView from '@/modules/apps/auth/activate-account/views/ActivateAccountView.vue';
import ResendActivationCodeView from '@/modules/apps/auth/resend-activation-code/views/ResendActivationCodeView.vue';
import ResetPasswordView from '@/modules/apps/auth/reset-password/views/ResetPasswordView.vue';
import AssistanceView from '@/modules/apps/auth/assistance/views/AssistanceView.vue';
import DashboardView from '@/modules/apps/users/dashboard/views/DashboardView.vue';
import DashboardCheckoutView from '@/modules/apps/users/dashboard/views/DashboardCheckoutView.vue';
import UserProfileView from '@/modules/apps/users/profile/views/ProfileView.vue';
import OverviewView from '@/modules/apps/users/overview/views/OverviewView.vue';
import ProjectListView from '@/modules/apps/projects/views/ProjectListView.vue';
import ProjectDetailView from '@/modules/apps/projects/views/ProjectDetailView.vue';
import LLMView from '@/modules/apps/llm/views/LLMView.vue';
import NotificationView from '@/modules/apps/notifications/views/NotificationView.vue';
import NotificationInformationView from '@/modules/apps/notifications/information/views/NotificationInformationView.vue';
import NotificationActionRequiredView from '@/modules/apps/notifications/action-required/views/NotificationActionRequiredView.vue';
import NotificationResetView from '@/modules/apps/notifications/reset/views/NotificationResetView.vue';
import SettingListView from '@/modules/apps/settings/views/SettingListView.vue';
import PaymentView from '@/modules/apps/settings/payment/views/PaymentView.vue';
import SettingsProfileView from '@/modules/apps/settings/profile/views/ProfileView.vue';
import AdminPanelView from '@/modules/apps/users/admin/panel/views/PanelView.vue';
import SessionActivityView from '@/modules/apps/users/admin/session-activity/views/SessionActivityView.vue';

export const routes = [
  // GUEST ROUTES
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: guestMeta,
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: guestMeta,
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
    meta: guestMeta,
  },
  {
    path: '/activate-account',
    name: 'activate-account',
    component: ActivateAccountView,
    meta: guestMeta,
  },
  {
    path: '/resend-activation-code',
    name: 'resend-activation-code',
    component: ResendActivationCodeView,
    meta: guestMeta,
  },
  {
    path: '/reset-password',
    name: 'reset-password',
    component: ResetPasswordView,
    meta: guestMeta,
  },
  {
    path: '/assistance',
    name: 'assistance',
    component: AssistanceView,
    meta: guestMeta,
  },
  // USER ROUTES
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView,
    meta: userOnlyMeta,
  },
  {
    path: '/dashboard/checkout',
    name: 'dashboard-checkout',
    component: DashboardCheckoutView,
    meta: userOnlyMeta,
  },
  {
    path: '/overview',
    name: 'overview',
    component: OverviewView,
    meta: userOnlyMeta,
  },
  {
    path: '/projects',
    name: 'projects',
    component: ProjectListView,
    meta: userOnlyMeta,
  },
  {
    path: '/projects/:id',
    name: 'projects-detail',
    component: ProjectDetailView,
    props: true,
    meta: userOnlyMeta,
  },
  {
    path: '/llm',
    name: 'llm',
    component: LLMView,
    meta: userOnlyMeta,
  },
  {
    path: '/settings',
    name: 'settings',
    component: SettingListView,
    meta: userOnlyMeta,
  },
  {
    path: '/settings/payment',
    name: 'settings-payment',
    component: PaymentView,
    meta: userOnlyMeta,
  },
  {
    path: '/settings/profile',
    name: 'settings-profile',
    component: SettingsProfileView,
    meta: userOnlyMeta,
  },
  {
    path: '/notifications/action-required',
    name: 'notifications-action-required',
    component: NotificationActionRequiredView,
    meta: userOnlyMeta,
  },
  // USER AND ADMIN ROUTES
  {
    path: '/profile',
    name: 'profile',
    component: UserProfileView,
    meta: userAdminMeta,
  },
  {
    path: '/notifications',
    name: 'notifications',
    component: NotificationView,
    meta: userAdminMeta,
  },
  {
    path: '/notifications/information',
    name: 'notifications-information',
    component: NotificationInformationView,
    meta: userAdminMeta,
  },
  // ADMIN ROUTES
  {
    path: '/notifications/reset',
    name: 'notifications-reset',
    component: NotificationResetView,
    meta: adminMeta,
  },
  {
    path: '/panel',
    name: 'panel',
    component: AdminPanelView,
    meta: adminMeta,
  },
  {
    path: '/session-activity',
    name: 'session-activity',
    component: SessionActivityView,
    meta: adminMeta,
  },
];
