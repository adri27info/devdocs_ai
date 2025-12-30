<template>
  <div class="w-full flex flex-col justify-center items-center text-center gap-5">
    <div class="w-full mt-10">
      <h1 class="text-3xl font-bold mb-5">Set new password</h1>
      <p class="text-lg">Enter your new password below</p>
    </div>

    <form
      method="post"
      @submit.prevent="handleResetPasswordConfirm"
      class="w-full sm:w-[480px] flex flex-col justify-center items-center gap-7 rounded sm:border-1 p-2 mb-10"
    >
      <div class="w-full flex flex-col justify-center items-center gap-2">
        <div class="w-full flex flex-row justify-center items-center gap-1">
          <label class="font-bold" for="new-password">New password</label>
          <span class="text-error mt-1">*</span>
        </div>
        <div class="flex items-center border rounded w-full p-2 relative">
          <input
            class="flex-1 text-center outline-none py-2"
            id="new-password"
            placeholder="Enter your new password"
            v-model="resetPasswordConfirmFactory.newPassword"
            :type="newPasswordProps.type"
          />
          <button type="button" class="absolute right-2" @click="toggleNewPasswordVisibility">
            <component :is="newPasswordProps.icon" class="h-5 w-5 text-black" />
          </button>
        </div>
        <p v-if="resetPasswordConfirmFactory.newPasswordError" class="w-full text-error font-bold">
          {{ resetPasswordConfirmFactory.newPasswordError }}
        </p>
      </div>

      <div class="w-full flex flex-col justify-center items-center gap-2">
        <div class="w-full flex flex-row justify-center items-center gap-1">
          <label class="font-bold" for="confirm-new-password">Confirm new password</label>
          <span class="text-error mt-1">*</span>
        </div>
        <div class="flex items-center border rounded w-full p-2 relative">
          <input
            class="flex-1 text-center outline-none py-2"
            id="confirm-new-password"
            placeholder="Confirm your new password"
            v-model="resetPasswordConfirmFactory.confirmNewPassword"
            :type="confirmNewPasswordProps.type"
          />
          <button
            type="button"
            class="absolute right-2"
            @click="toggleConfirmNewPasswordVisibility"
          >
            <component
              :is="confirmNewPasswordProps.icon"
              class="h-5 w-5 text-black stroke-current"
            />
          </button>
        </div>
        <p
          v-if="resetPasswordConfirmFactory.confirmNewPasswordError"
          class="w-full text-error font-bold"
        >
          {{ resetPasswordConfirmFactory.confirmNewPasswordError }}
        </p>
        <p
          v-if="resetPasswordConfirmFactory.passwordMatchError"
          class="w-full text-error font-bold"
        >
          {{ resetPasswordConfirmFactory.passwordMatchError }}
        </p>
        <Loader :loading="loader" />
      </div>

      <div class="w-full flex flex-col justify-center items-center gap-4">
        <button type="submit" class="!w-[280px] btn btn-dark" :class="{ disabled: disabledBtn }">
          Reset password
        </button>
        <RouterLink :to="{ name: 'login' }" class="font-bold">
          Remember your password? Sign in
        </RouterLink>
      </div>
    </form>
  </div>
</template>

<script setup>
import { useResetPasswordConfirm } from '@/modules/apps/auth/reset-password/composables/useResetPasswordConfirm';
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

const {
  resetPasswordConfirmFactory,
  newPasswordProps,
  confirmNewPasswordProps,
  toggleNewPasswordVisibility,
  toggleConfirmNewPasswordVisibility,
  handleResetPasswordConfirm,
} = useResetPasswordConfirm();
</script>
