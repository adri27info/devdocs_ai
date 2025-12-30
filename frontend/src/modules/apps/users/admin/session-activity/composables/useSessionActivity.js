import { onMounted } from 'vue';
import { useFetcher } from '@/modules/shared/common/composables/utils/useFetcher';

export function useSessionActivity() {
  const { fetch } = useFetcher();

  const formatDate = datetimeStr => {
    const [date, time] = datetimeStr.split(' ');
    return `${date} - ${time}`;
  };

  onMounted(async () => {
    await fetch({
      app: 'user',
      action: 'sessionActivity',
      hideSuccess: true,
    });
  });

  return {
    formatDate,
  };
}
