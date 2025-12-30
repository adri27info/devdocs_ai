import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue';
import { ArrowDownIcon, ArrowUpIcon } from '@heroicons/vue/24/outline';

export function useSelect(props, emit) {
  const selectedOption = ref(props.modelValue);
  const showOptions = ref(false);
  const hoverOption = ref(null);
  const dropdownRef = ref(null);

  const selectedOptionText = computed(() => selectedOption.value?.text || '');
  const iconComponent = computed(() => (showOptions.value ? ArrowUpIcon : ArrowDownIcon));

  const toggleDropdown = () => {
    showOptions.value = !showOptions.value;
  };

  const selectOption = option => {
    selectedOption.value = option;
    showOptions.value = false;

    emit('update:modelValue', option);

    if (props.error === 'Please select an valid option' && option.value !== '') {
      emit('update:error', '');
    }
  };

  const handleClickOutside = event => {
    if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
      showOptions.value = false;
    }
  };

  watch(
    () => props.modelValue,
    newVal => {
      selectedOption.value = newVal;
    },
  );

  onMounted(() => {
    document.addEventListener('click', handleClickOutside);
  });

  onBeforeUnmount(() => {
    document.removeEventListener('click', handleClickOutside);
  });

  return {
    showOptions,
    selectedOption,
    hoverOption,
    dropdownRef,
    selectedOptionText,
    iconComponent,

    toggleDropdown,
    selectOption,
  };
}
