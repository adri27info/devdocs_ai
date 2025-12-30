<template>
  <div v-if="loading" class="mt-5">
    <div
      class="h-6 w-6 m-auto border-2 border-blue-500 border-t-transparent rounded-full animate-spin"
    ></div>
  </div>
</template>

<script setup>
defineProps({
  loading: Boolean,
});
</script>
