<template>
  <section class="w-full p-8">
    <div class="w-full mb-8 flex flex-col items-center justify-center gap-2 text-center">
      <h1 class="text-xl font-semibold mb-2">Settings</h1>
      <p class="text-base">Manage your account settings and preferences</p>
    </div>

    <div class="w-full p-5 rounded-2xl border-2 bg-white shadow-sm">
      <div class="flex flex-col sm:flex-row w-full justify-between gap-3">
        <MenuOptions
          :items="menuSettingsItems"
          item-classes="general-custom-hover flex-1 flex flex-col justify-center items-center bg-gray-900 hover:bg-gray-800 text-white rounded-lg p-2 transition"
          router-link-classes="w-full flex flex-col items-center justify-center gap-1 text-center"
          icon-classes="h-6 w-6 text-white"
        />
      </div>
    </div>
  </section>
</template>

<script setup>
import { useSetting } from '@/modules/apps/settings/composables/useSetting';
import MenuOptions from '@/modules/shared/common/components/ui/MenuOptions.vue';

const { menuSettingsItems } = useSetting();
</script>

<style scoped></style>
