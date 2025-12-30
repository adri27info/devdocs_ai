<template>
  <Header>
    <template #header-content>
      <div class="w-40">
        <img class="w-full object-cover" alt="Logo DevDocs AI" :src="logo" />
      </div>
      <div class="flex flex-col lg:flex-row justify-between items-center gap-3 sm:gap-5 mb-10">
        <RouterLink :to="{ name: 'home' }" class="btn btn-info">Home</RouterLink>
        <RouterLink :to="{ name: 'login' }" class="btn btn-primary">Login</RouterLink>
        <RouterLink :to="{ name: 'register' }" class="btn btn-secondary">Register</RouterLink>
        <RouterLink :to="{ name: 'assistance' }" class="btn btn-dark">Assistance</RouterLink>
      </div>
    </template>
  </Header>
</template>

<script setup>
import { useEnvironment } from '@/modules/shared/common/composables/utils/ui/useEnvironment';
import Header from '@/modules/shared/common/components/infraestructure/parts/headers/base/Header.vue';

const { logo } = useEnvironment();
</script>

<style scoped></style>
