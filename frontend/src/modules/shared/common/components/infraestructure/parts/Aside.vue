<template>
  <aside
    class="w-full sm:w-56 shrink-0 flex flex-wrap flex-row sm:flex-col items-center justify-around sm:justify-start gap-3 p-5 border-black border-b-2 sm:border-r-2 sm:border-b-0"
  >
    <MenuOptions
      :items="menuAsideItems"
      :divisor="false"
      item-classes="aside-custom-hover bg-white text-white sm:text-black w-28 sm:w-full flex flex-row items-center justify-center sm:justify-start gap-2 border-black border-b-0 sm:border-b-2 rounded-2xl sm:rounded-none p-3"
      router-link-classes="flex flex-row items-center justify-center sm:justify-start gap-2"
      icon-classes="h-6 w-6 sm:h-5 sm:w-5 text-white sm:text-black"
      span-classes="hidden sm:block"
      order="icon-first"
    />
  </aside>
</template>

<script setup>
import { useAside } from '@/modules/shared/common/composables/core/infraestructure/parts/aside/useAside';
import MenuOptions from '@/modules/shared/common/components/ui/MenuOptions.vue';

const { menuAsideItems } = useAside();
</script>
