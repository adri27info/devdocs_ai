import { computed } from 'vue';
import { useRoute } from 'vue-router';

export function useResetPasswordQueryParams() {
  const route = useRoute();

  const uid = computed(() => route.query.uid);
  const token = computed(() => route.query.token);

  const hasResetParams = computed(
    () => !!uid.value?.toString().trim() && !!token.value?.toString().trim(),
  );

  return { uid, token, hasResetParams };
}
