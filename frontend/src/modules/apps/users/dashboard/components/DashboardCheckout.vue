<template>
  <section class="w-full p-8">
    <Loader :loading="storeCore.loaders.paymentStatus" />

    <div
      v-if="!storeCore.loaders.paymentStatus"
      class="w-full flex flex-col items-center justify-center gap-3 text-center"
    >
      <h1 class="text-xl font-semibold mb-4">Dashboard payment information</h1>

      <p v-if="!storeSetting.paymentFactory.status" class="text-base text-center mb-5">
        The payment status has not been initialized yet. Please try again or check your Stripe
        checkout session.
      </p>

      <p v-else-if="isCanceled" class="text-base text-center mb-5">
        Unfortunately, your recent payment attempt on Stripe could not be completed. This may have
        been caused by a temporary issue with the payment process. Rest assured, no charges have
        been made to your account. You can try upgrading to the premium plan again at any time by
        clicking the “Upgrade to Premium” button on your dashboard.
      </p>

      <p v-else class="text-base text-center mb-5">
        Congratulations! Your payment has been successfully processed on Stripe, and your account
        has been upgraded to the premium plan. You now have access to all premium features and
        updates. Thank you for upgrading!
      </p>

      <p v-if="isCanceled" class="text-error mb-5 font-semibold">Payment failed. Try again</p>
      <p v-else-if="storeSetting.paymentFactory.status" class="text-success font-bold mb-5">
        Your premium plan is now active.
      </p>

      <RouterLink :to="{ name: 'dashboard' }" class="btn btn-dark"> Back to dashboard </RouterLink>
    </div>
  </section>
</template>

<script setup>
import { useDashboardCheckout } from '@/modules/apps/users/dashboard/composables/useDashboardCheckout';
import { settingStore } from '@/modules/apps/settings/stores/settingStore';
import { coreStore } from '@/modules/shared/common/stores/core/coreStore';
import Loader from '@/modules/shared/common/components/ui/Loader.vue';

const storeSetting = settingStore();
const storeCore = coreStore();

const { isCanceled } = useDashboardCheckout();
</script>

<style scoped></style>
