import { ref } from 'vue';

export function useDropdown() {
  const showDropdown = ref(false);

  const toggleDropdown = () => {
    showDropdown.value = !showDropdown.value;
  };

  const closeDropdown = () => {
    showDropdown.value = false;
  };

  return {
    showDropdown,

    toggleDropdown,
    closeDropdown,
  };
}
