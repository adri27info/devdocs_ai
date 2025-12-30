import { watch } from 'vue';
import { settingStore } from '@/modules/apps/settings/stores/settingStore';
import { useFetcher } from '@/modules/shared/common/composables/utils/useFetcher';

export function usePayment() {
  const storeSetting = settingStore();

  const { fetch } = useFetcher();

  watch(
    () => storeSetting.paymentFactory.invoice.id,
    async invoiceId => {
      if (!invoiceId) {
        await fetch({
          app: 'setting',
          action: 'invoice',
          hideSuccess: true,
        });
      }
    },
    { immediate: true },
  );
}
