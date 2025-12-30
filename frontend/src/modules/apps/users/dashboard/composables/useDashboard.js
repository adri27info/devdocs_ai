import { ref, onMounted, watch, computed } from 'vue';
import { PLAN_TYPES } from '@/modules/shared/common/constants/apps/projects/plan_types';
import { userStore } from '@/modules/apps/users/stores/userStore';
import { settingStore } from '@/modules/apps/settings/stores/settingStore';
import { coreStore } from '@/modules/shared/common/stores/core/coreStore';
import { useModal } from '@/modules/shared/common/composables/utils/ui/useModal';
import { useFetcher } from '@/modules/shared/common/composables/utils/useFetcher';

export function useDashboard() {
  const storeUser = userStore();
  const storeSetting = settingStore();
  const storeCore = coreStore();

  const manuallyClosed = ref(false);

  const { isOpen, close, open } = useModal();
  const { fetch } = useFetcher();

  const userPlanName = computed(() => storeUser.userStatsFactory.plan_type.name.toLowerCase());

  const isFreePlan = computed(() => userPlanName.value === PLAN_TYPES.FREE.name);

  const subscriptionText = computed(() => {
    return userPlanName.value === PLAN_TYPES.FREE.name
      ? PLAN_TYPES.FREE.subscription
      : PLAN_TYPES.PREMIUM.subscription;
  });

  const planUsageWidth = computed(() => {
    switch (userPlanName.value) {
      case PLAN_TYPES.FREE.name:
        return PLAN_TYPES.FREE.planUsageWidth;
      case PLAN_TYPES.PREMIUM.name:
        return PLAN_TYPES.PREMIUM.planUsageWidth;
      default:
        return PLAN_TYPES.BASE.planUsageWidth;
    }
  });

  const upgradePlan = async () => {
    await fetch({
      app: 'setting',
      action: 'session',
      hideSuccess: true,
    });
  };

  const pollPaymentStatus = async () => {
    const checkStatus = async () => {
      if (!storeSetting.paymentFactory.sessionId || !storeSetting.paymentFactory.status) return;

      await fetch({
        app: 'setting',
        action: 'status',
        params: { sessionId: storeSetting.paymentFactory.sessionId },
        hideSuccess: true,
      });

      if (storeSetting.paymentFactory.status === 'requires_capture') {
        storeCore.loaders.paymentPollingStatus = true;
        setTimeout(checkStatus, 30000);
      } else if (storeSetting.paymentFactory.status === 'succeeded') {
        storeCore.loaders.paymentPollingStatus = false;

        await fetch({
          app: 'user',
          action: 'stats',
          hideSuccess: true,
        });
      }
    };

    checkStatus();
  };

  const isCurrentPlan = planName => planName.toLowerCase().includes(userPlanName.value);

  const planBorderClass = planName =>
    isCurrentPlan(planName) ? 'border-gray-900' : 'border-gray-300';

  const closeModal = () => {
    manuallyClosed.value = true;
    close();
  };

  const openModal = () => {
    manuallyClosed.value = false;
    open();
  };

  watch(
    () => storeSetting.paymentFactory.checkoutUrl,
    newUrl => {
      if (newUrl) {
        window.location.href = newUrl;
      }
    },
  );

  watch(
    () => storeCore.loaders.paymentPollingStatus,
    val => {
      if (val) {
        if (!manuallyClosed.value) open();
      } else {
        close();
        manuallyClosed.value = false;
      }
    },
    { immediate: true },
  );

  onMounted(async () => {
    await fetch({
      app: 'user',
      action: 'stats',
      hideSuccess: true,
    });

    if (isFreePlan.value && storeSetting.paymentFactory.status === 'requires_capture') {
      pollPaymentStatus();
    }
  });

  return {
    subscriptionText,
    isFreePlan,
    planUsageWidth,
    isOpen,
    manuallyClosed,

    openModal,
    closeModal,
    isCurrentPlan,
    planBorderClass,
    upgradePlan,
  };
}
