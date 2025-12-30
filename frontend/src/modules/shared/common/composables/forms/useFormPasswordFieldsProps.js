import { computed } from 'vue';
import { EyeIcon, EyeSlashIcon } from '@heroicons/vue/24/outline';
import { INPUT_TYPES } from '@/modules/shared/common/constants/utils/inputTypes';

export function useFormPasswordFieldProps(form, visibleKey = 'passwordVisible') {
  const { TEXT, PASSWORD } = INPUT_TYPES;

  const passwordProps = computed(() => ({
    type: form[visibleKey] ? TEXT : PASSWORD,
    icon: form[visibleKey] ? EyeIcon : EyeSlashIcon,
  }));

  const togglePasswordVisibility = () => {
    form[visibleKey] = !form[visibleKey];
  };

  return { passwordProps, togglePasswordVisibility };
}
