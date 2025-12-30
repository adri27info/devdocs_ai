<template>
  <div ref="dropdownRef" class="w-full relative">
    <button
      type="button"
      @click="toggleDropdown"
      class="w-full relative border rounded p-2 flex justify-center items-center"
    >
      <span class="text-center">{{ selectedOptionText || options[0].text }}</span>
      <component :is="iconComponent" class="h-4 w-4 text-black absolute right-2" />
    </button>

    <div
      v-if="showOptions"
      class="w-full bg-gray-100 border rounded p-2 flex flex-col items-center absolute top-full left-0 z-10"
    >
      <span
        v-for="option in options"
        :key="option.value"
        class="w-full text-center p-2 cursor-pointer rounded hover:bg-gray-300"
        :class="{
          'bg-gray-300':
            selectedOption?.value === option.value &&
            (hoverOption === null || hoverOption.value === option.value),
        }"
        @click="selectOption(option)"
        @mouseenter="hoverOption = option"
        @mouseleave="hoverOption = null"
      >
        {{ option.text }}
      </span>
    </div>

    <p v-if="error" class="w-full text-error text-center font-bold mt-3">{{ error }}</p>
  </div>
</template>

<script setup>
import { watch } from 'vue';
import { useSelect } from '@/modules/shared/common/composables/utils/ui/useSelect';

const props = defineProps({
  options: {
    type: Array,
    required: true,
  },
  modelValue: {
    type: Object,
    default: null,
  },
  placeholder: {
    type: String,
    default: 'Select an option',
  },
  error: {
    type: String,
    default: '',
  },
});

const emit = defineEmits(['update:modelValue', 'update:error']);

const {
  showOptions,
  selectedOption,
  hoverOption,
  dropdownRef,
  selectedOptionText,
  iconComponent,
  toggleDropdown,
  selectOption,
} = useSelect(props, emit);

watch(
  () => props.modelValue,
  newVal => {
    selectedOption.value = newVal;
  },
);
</script>

<style scoped></style>
