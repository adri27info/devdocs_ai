<template>
  <ResetPasswordForm
    v-if="!hasResetParams"
    :loader="storeCore.loaders.resetPassword"
    :disabled-btn="storeCore.btnDisablers.resetPasswordBtn"
  />
  <ResetPasswordConfirmForm
    v-else
    :loader="storeCore.loaders.resetPasswordConfirm"
    :disabled-btn="storeCore.btnDisablers.resetPasswordConfirmBtn"
  />
</template>

<script setup>
import { useResetPasswordQueryParams } from '@/modules/apps/auth/reset-password/composables/useResetPasswordQueryParams';
import { coreStore } from '@/modules/shared/common/stores/core/coreStore';
import ResetPasswordForm from '@/modules/apps/auth/reset-password/components/ResetPasswordForm.vue';
import ResetPasswordConfirmForm from '@/modules/apps/auth/reset-password/components/ResetPasswordConfirmForm.vue';

const storeCore = coreStore();

const { hasResetParams } = useResetPasswordQueryParams();
</script>
