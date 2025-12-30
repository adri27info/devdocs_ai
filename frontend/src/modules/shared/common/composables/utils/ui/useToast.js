import { ref, computed } from 'vue';
import { ToasterHelper } from '@/modules/shared/common/helpers/utils/ui/toasterHelper';

let toastId = 0;

const toasts = ref([]);

const groupedToasts = computed(() => {
  const groups = {};

  toasts.value.forEach(toast => {
    const pos = toast.position || 'top-right';
    if (!groups[pos]) groups[pos] = [];
    groups[pos].push(toast);
  });

  return groups;
});

export function useToast() {
  const showToast = (message, type, duration = 3000, position = 'top-right', state = 'showing') => {
    const id = ++toastId;
    toasts.value.push({ id, message, type, position, state });

    window.scrollTo({ top: 0, behavior: 'smooth' });

    setTimeout(() => {
      removeToast(id);
    }, duration);
  };

  const removeToast = id => {
    const toast = toasts.value.find(t => t.id === id);
    if (!toast) return;

    toast.state = 'leaving';

    setTimeout(() => {
      toasts.value = toasts.value.filter(t => t.id !== id);
    }, 300);
  };

  return {
    toasts,
    groupedToasts,
    toastConfig: ToasterHelper.getToastConfig(),
    showToast,
    removeToast,
  };
}
