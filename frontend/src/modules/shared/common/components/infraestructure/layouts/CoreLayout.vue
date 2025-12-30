<template>
  <component :is="currentHeader" />
  <Main>
    <template #main-content>
      <slot name="main-content" />
    </template>
  </Main>
  <Footer />
</template>

<script setup>
import { useCoreLayout } from '@/modules/shared/common/composables/core/infraestructure/layouts/useCoreLayout';
import Main from '@/modules/shared/common/components/infraestructure/parts/Main.vue';
import Footer from '@/modules/shared/common/components/infraestructure/parts/Footer.vue';

const { currentHeader } = useCoreLayout();
</script>

<style scoped></style>
