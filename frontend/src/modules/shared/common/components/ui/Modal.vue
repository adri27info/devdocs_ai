<template>
  <div v-if="show" class="w-full fixed inset-0 bg-black/70 flex items-center justify-center z-50">
    <div
      class="bg-white rounded-xl shadow-lg w-[90%] max-w-md p-6 relative max-h-[90vh] overflow-y-auto"
    >
      <XMarkIcon class="h-5 w-5 text-black absolute top-3 right-3" @click="close" />
      <slot name="modal-content" />
    </div>
  </div>
</template>

<script setup>
import { XMarkIcon } from '@heroicons/vue/24/outline';

defineProps({
  show: Boolean,
});

const emits = defineEmits(['close']);

const close = () => {
  emits('close');
};
</script>

<style scoped></style>
