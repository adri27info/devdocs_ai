import { ref, watch } from 'vue';

export function useDebounce(value, delay = 500) {
  let timeout;

  const debouncedValue = ref(value.value);

  watch(value, newVal => {
    clearTimeout(timeout);

    timeout = setTimeout(() => {
      debouncedValue.value = newVal;
    }, delay);
  });

  return debouncedValue;
}
