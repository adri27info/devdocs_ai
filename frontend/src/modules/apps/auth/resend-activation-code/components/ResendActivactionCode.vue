<template>
  <div class="w-full flex flex-col justify-center items-center text-center gap-5">
    <div class="w-full mt-10">
      <h1 class="text-3xl font-bold mb-5">Resend activation code</h1>
      <p class="text-lg">Enter your email to receive a new activation code.</p>
    </div>

    <form
      method="post"
      @submit.prevent="handleResendActivationCode"
      class="w-full sm:w-[480px] flex flex-col justify-center items-center gap-7 rounded sm:border-1 p-2 mb-10"
    >
      <div class="w-full flex flex-col justify-center items-center gap-2">
        <div class="w-full flex flex-row justify-center items-center gap-1">
          <label class="font-bold" for="email">Email</label>
          <span class="text-error mt-1">*</span>
        </div>
        <input
          class="w-full p-2 border-1 rounded text-center"
          type="text"
          name="email"
          id="email"
          placeholder="Enter your email"
          v-model="resendActivationCodeFactory.email"
        />
        <p v-if="resendActivationCodeFactory.emailError" class="w-full text-error font-bold">
          {{ resendActivationCodeFactory.emailError }}
        </p>
      </div>

      <div class="w-full">
        <RouterLink :to="{ name: 'activate-account' }" class="font-bold">
          You already have an activation code? Activate your account.
        </RouterLink>
        <Loader :loading="storeCore.loaders.resendActivationCode" />
      </div>

      <div class="w-full flex flex-col justify-center items-center gap-4">
        <button
          type="submit"
          class="!w-[280px] btn btn-dark"
          :class="{ disabled: storeCore.btnDisablers.resendActivationCodeBtn }"
        >
          Resend activation code
        </button>
        <RouterLink :to="{ name: 'login' }" class="font-bold">
          Already have an account? Sign in
        </RouterLink>
      </div>
    </form>
  </div>
</template>

<script setup>
import { useResendActivationCode } from '@/modules/apps/auth/resend-activation-code/composables/useResendActivationCode';
import { coreStore } from '@/modules/shared/common/stores/core/coreStore';
import Loader from '@/modules/shared/common/components/ui/Loader.vue';

const storeCore = coreStore();

const { resendActivationCodeFactory, handleResendActivationCode } = useResendActivationCode();
</script>

<style scoped></style>
