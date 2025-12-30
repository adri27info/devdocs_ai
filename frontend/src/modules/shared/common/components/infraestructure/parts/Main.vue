<template>
  <main
    class="min-h-screen flex flex-col sm:flex-row relative overflow-x-hidden"
    :class="[mainJustifyClass, mainItemsClass]"
  >
    <Aside v-if="showAside" />
    <div class="w-full sm:flex-1 sm:w-0">
      <slot name="main-content" />
    </div>
    <Toaster />
  </main>
</template>

<script setup>
import { useMain } from '@/modules/shared/common/composables/core/infraestructure/parts/main/useMain';
import Aside from '@/modules/shared/common/components/infraestructure/parts/Aside.vue';
import Toaster from '@/modules/shared/common/components/ui/Toaster.vue';

const { showAside, mainJustifyClass, mainItemsClass } = useMain();
</script>
