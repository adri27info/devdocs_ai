import { computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { settingStore } from '@/modules/apps/settings/stores/settingStore';
import { useFetcher } from '@/modules/shared/common/composables/utils/useFetcher';

export function useDashboardCheckout() {
  const storeSetting = settingStore();
  const route = useRoute();
  const router = useRouter();

  const { fetch } = useFetcher();

  const isCanceled = computed(() => storeSetting.paymentFactory.status === 'canceled');
  const session = computed(() => route.query.session_id);
  const hasSessionId = computed(() => !!session.value);

  watch(
    hasSessionId,
    async value => {
      if (!value) {
        router.replace({ name: 'dashboard' });
      } else {
        storeSetting.paymentFactory.sessionId = session.value;

        await fetch({
          app: 'setting',
          action: 'status',
          params: { sessionId: storeSetting.paymentFactory.sessionId },
          hideSuccess: true,
        });
      }
    },
    { immediate: true },
  );

  return {
    isCanceled,
  };
}
