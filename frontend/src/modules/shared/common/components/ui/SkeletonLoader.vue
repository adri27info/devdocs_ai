<template>
  <div :class="['relative', wrapperClasses]">
    <div
      v-if="!loaded"
      :class="[shimmer ? 'animate-shimmer' : 'bg-gray-300', 'absolute inset-0', 'w-full']"
    ></div>

    <img :src="currentSrc" :alt="alt" :class="imgClasses" @load="handleLoad" @error="handleError" />
  </div>
</template>

<script setup>
import { useSkeletonLoader } from '@/modules/shared/common/composables/utils/ui/useSkeletonLoader';

const props = defineProps({
  src: {
    type: String,
    required: true,
  },
  type: {
    type: String,
    required: true,
  },
  wrapperClasses: {
    type: String,
    required: true,
  },
  alt: {
    type: String,
    default: '',
  },
  delay: {
    type: Number,
    default: 1500,
  },
  shimmer: {
    type: Boolean,
    default: true,
  },
  rounded: {
    type: Boolean,
    default: true,
  },
});

const { loaded, currentSrc, imgClasses, handleLoad, handleError } = useSkeletonLoader(props);
</script>

<style scoped>
@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

.animate-shimmer {
  animation: shimmer 1s linear infinite;
  background: linear-gradient(90deg, #cbd5e1 25%, #f3f4f6 50%, #cbd5e1 75%);
  background-size: 200% 100%;
}
</style>
