<template>
  <section class="w-full p-8">
    <Loader :loading="storeCore.loaders.paymentInvoice" />

    <div
      v-if="!storeCore.loaders.paymentInvoice"
      class="w-full flex flex-col items-center justify-center gap-3 text-center"
    >
      <div class="w-full mb-8 flex flex-col items-center justify-center gap-2 text-center">
        <h1 class="text-xl font-semibold mb-6">Payment invoice information</h1>

        <div
          v-if="
            !storeSetting.paymentFactory.invoice.id ||
            !storeSetting.paymentFactory.invoice.attachment
          "
        >
          <p class="text-base">The invoice cannot be displayed</p>
        </div>

        <div v-else class="overflow-auto border-2 border-black p-1 w-full">
          <div class="w-full lg:w-200 m-auto">
            <SkeletonLoader
              :src="storeSetting.paymentFactory.invoice.attachment"
              :rounded="false"
              wrapper-classes="w-full h-full"
              type="imageNotFound"
              alt="payment invoice attachment"
            />
          </div>
        </div>
      </div>

      <RouterLink :to="{ name: 'settings' }" class="btn btn-dark"> Back to settings </RouterLink>
    </div>
  </section>
</template>

<script setup>
import { usePayment } from '@/modules/apps/settings/payment/composables/usePayment';
import { settingStore } from '@/modules/apps/settings/stores/settingStore';
import { coreStore } from '@/modules/shared/common/stores/core/coreStore';
import Loader from '@/modules/shared/common/components/ui/Loader.vue';
import SkeletonLoader from '@/modules/shared/common/components/ui/SkeletonLoader.vue';

const storeSetting = settingStore();
const storeCore = coreStore();

usePayment();
</script>

<style scoped></style>
