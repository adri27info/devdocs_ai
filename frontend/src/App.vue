<template>
  <CoreLayout>
    <template #main-content>
      <RouterView />
    </template>
  </CoreLayout>
</template>

<script setup>
import { useCore } from '@/modules/shared/common/composables/core/useCore';
import CoreLayout from '@/modules/shared/common/components/infraestructure/layouts/CoreLayout.vue';

useCore();
</script>

<style scoped></style>
