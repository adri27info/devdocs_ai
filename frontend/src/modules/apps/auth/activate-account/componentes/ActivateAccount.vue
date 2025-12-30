<template>
  <div class="w-full flex flex-col justify-center items-center text-center gap-5">
    <div class="w-full mt-10">
      <h1 class="text-3xl font-bold mb-5">Activate an account</h1>
      <p class="text-lg">Enter your details to activated the account</p>
    </div>

    <form
      method="post"
      @submit.prevent="handleActivateAccount"
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
          v-model="activateAccountFactory.email"
        />
        <p v-if="activateAccountFactory.emailError" class="w-full text-error font-bold">
          {{ activateAccountFactory.emailError }}
        </p>
      </div>

      <div class="w-full flex flex-col justify-center items-center gap-2">
        <div class="w-full flex flex-row justify-center items-center gap-1">
          <label class="font-bold" for="activationCode">Activation code</label>
          <span class="text-error mt-1">*</span>
        </div>
        <input
          class="w-full p-2 border-1 rounded text-center"
          type="text"
          name="activationCode"
          id="activationCode"
          placeholder="Enter your activation code"
          v-model="activateAccountFactory.activationCode"
        />
        <p v-if="activateAccountFactory.activationCodeError" class="w-full text-error font-bold">
          {{ activateAccountFactory.activationCodeError }}
        </p>
      </div>

      <div class="w-full flex flex-col justify-center items-center gap-2">
        <RouterLink :to="{ name: 'register' }" class="font-bold">
          Don’t have an account? Create one to start.
        </RouterLink>
        <RouterLink :to="{ name: 'resend-activation-code' }" class="font-bold">
          Do you need a new activation code?
        </RouterLink>
        <Loader :loading="storeCore.loaders.activateAccount" />
      </div>

      <div class="w-full flex flex-col justify-center items-center gap-4">
        <button
          type="submit"
          class="!w-[280px] btn btn-dark"
          :class="{ disabled: storeCore.btnDisablers.activateAccountBtn }"
        >
          Activate account
        </button>
        <RouterLink :to="{ name: 'login' }" class="font-bold">
          Already have an account? Sign in
        </RouterLink>
      </div>
    </form>
  </div>
</template>

<script setup>
import { useActivateAccount } from '@/modules/apps/auth/activate-account/composables/useActivateAccount';
import { coreStore } from '@/modules/shared/common/stores/core/coreStore';
import Loader from '@/modules/shared/common/components/ui/Loader.vue';

const storeCore = coreStore();

const { activateAccountFactory, handleActivateAccount } = useActivateAccount();
</script>

<style scoped></style>
