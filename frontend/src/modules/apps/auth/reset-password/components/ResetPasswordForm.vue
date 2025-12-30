<template>
  <div class="w-full flex flex-col justify-center items-center text-center gap-5">
    <div class="w-full mt-10">
      <h1 class="text-3xl font-bold mb-5">Reset your password</h1>
      <p class="text-lg">Enter your email and we'll send you a reset link</p>
    </div>

    <form
      method="post"
      @submit.prevent="handleResetPassword"
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
          id="email"
          placeholder="Enter your email"
          v-model="resetPasswordFactory.email"
        />
        <p v-if="resetPasswordFactory.emailError" class="w-full text-error font-bold">
          {{ resetPasswordFactory.emailError }}
        </p>
      </div>

      <div class="w-full flex flex-col justify-center items-center gap-2">
        <RouterLink :to="{ name: 'login' }" class="font-bold">
          Remember your password? Sign in
        </RouterLink>
        <Loader :loading="loader" />
      </div>

      <div class="w-full flex flex-col justify-center items-center gap-4">
        <button type="submit" class="!w-[280px] btn btn-dark" :class="{ disabled: disabledBtn }">
          Send reset link
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { useResetPassword } from '@/modules/apps/auth/reset-password/composables/useResetPassword';
import Loader from '@/modules/shared/common/components/ui/Loader.vue';

defineProps({
  loader: {
    type: Boolean,
    required: true,
  },
  disabledBtn: {
    type: Boolean,
    required: true,
  },
});

const { resetPasswordFactory, handleResetPassword } = useResetPassword();
</script>
