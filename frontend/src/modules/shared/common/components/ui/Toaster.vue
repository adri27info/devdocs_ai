<template>
  <section
    v-for="(group, position) in groupedToasts"
    :key="position"
    class="w-full sm:w-[550px] absolute z-10"
    :class="toastConfig.position[position] || toastConfig.position['top-right']"
  >
    <div class="flex flex-col gap-6">
      <div
        v-for="toast in group"
        :key="toast.id"
        :class="[
          'w-full min-h-24 p-1 rounded border-3 flex flex-row items-center justify-between bg-white shadow-md',
          toastConfig.borderColors[toast.type] || toastConfig.borderColors.default,
          toast.state === 'leaving' ? 'toast-leave' : 'toast-appear',
        ]"
      >
        <div class="m-auto flex flex-col items-center justify-center gap-2 text-center">
          <component
            :is="toastConfig.icons[toast.type] || toastConfig.icons.default"
            class="h-6 w-6"
            :class="toastConfig.iconColors[toast.type] || toastConfig.iconColors.default"
          />
          <p
            class="text-base m-0 break-words whitespace-normal font-semibold"
            :class="toastConfig.textColors[toast.type] || toastConfig.textColors.default"
          >
            <span v-for="(line, idx) in toast.message.split('\n')" :key="idx">
              {{ line }} <br />
            </span>
          </p>
        </div>

        <button class="self-start" @click="removeToast(toast.id)">
          <XMarkIcon class="h-5 w-5 text-black" />
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { XMarkIcon } from '@heroicons/vue/24/outline';
import { useToast } from '@/modules/shared/common/composables/utils/ui/useToast';

const { groupedToasts, removeToast, toastConfig } = useToast();
</script>

<style scoped>
.toast-appear {
  animation: toastFadeScaleIn 0.3s ease-out;
}

.toast-leave {
  animation: toastFadeScaleOut 0.3s ease-in forwards;
}

@keyframes toastFadeScaleIn {
  0% {
    opacity: 0;
    transform: scale(0.95);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes toastFadeScaleOut {
  0% {
    opacity: 1;
    transform: scale(1);
  }
  100% {
    opacity: 0;
    transform: scale(0.95);
  }
}
</style>
