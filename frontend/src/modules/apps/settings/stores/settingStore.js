import { reactive, toRefs } from 'vue';
import { defineStore } from 'pinia';
import { createPaymentFactory } from '@/modules/apps/settings/payment/factories/paymentFactory';
import { useSessionCleaner } from '@/modules/shared/common/composables/session/useSessionCleaner';
import { useDelay } from '@/modules/shared/common/composables/utils/useDelay';
import { useRequestHandler } from '@/modules/shared/common/composables/api/request/useRequestHandler';
import { SettingService } from '@/modules/apps/settings/services/settingService';
import { coreStore } from '@/modules/shared/common/stores/core/coreStore';

export const settingStore = defineStore(
  'settingStore',
  () => {
    const settingService = new SettingService();

    const storeCore = coreStore();

    const paymentFactory = reactive(createPaymentFactory());
    const loadersRefs = toRefs(storeCore.loaders);

    const { delay } = useDelay();
    const { clearSessionIsNeeded } = useSessionCleaner();
    const { handleAPIRequest } = useRequestHandler();

    const getPaymentSession = () => {
      return handleAPIRequest({
        actions: {
          afterRequest: data => {
            if (data?.checkout_url) {
              paymentFactory.checkoutUrl = data.checkout_url;
            }
          },
          onFinally: async () => {
            clearSessionIsNeeded();
          },
        },
        request: () => settingService.getPaymentSession(),
        expectedStatus: 201,
        operation: 'PAYMENT_SESSION',
        fnToRetry: () => getPaymentSession(),
        allowRetry: true,
      });
    };

    const getPaymentStatus = sessionId => {
      return handleAPIRequest({
        actions: {
          beforeRequest: () => {
            loadersRefs.paymentStatus.value = true;
          },
          afterRequest: data => {
            if (data?.payment_status) {
              paymentFactory.status = data.payment_status;
            }
          },
          onFinally: async () => {
            clearSessionIsNeeded();
            await delay();
            loadersRefs.paymentStatus.value = false;
          },
        },
        request: () => settingService.getPaymentStatus(sessionId),
        expectedStatus: 200,
        operation: 'PAYMENT_STATUS',
        fnToRetry: () => getPaymentStatus(sessionId),
        allowRetry: true,
      });
    };

    const getPaymentInvoice = () => {
      return handleAPIRequest({
        actions: {
          beforeRequest: () => {
            loadersRefs.paymentInvoice.value = true;
          },
          afterRequest: data => {
            if (data?.invoice) {
              paymentFactory.invoice = data.invoice;
            }
          },
          onFinally: async () => {
            clearSessionIsNeeded();
            await delay();
            loadersRefs.paymentInvoice.value = false;
          },
        },
        request: () => settingService.getPaymentInvoice(),
        expectedStatus: 200,
        operation: 'PAYMENT_INVOICE',
        fnToRetry: () => getPaymentInvoice(),
        allowRetry: true,
      });
    };

    return {
      paymentFactory,

      getPaymentSession,
      getPaymentStatus,
      getPaymentInvoice,
    };
  },
  {
    persist: {
      pick: ['paymentFactory.status'],
      storage: localStorage,
    },
  },
);
