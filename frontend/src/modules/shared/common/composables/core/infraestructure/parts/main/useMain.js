import { computed } from 'vue';
import { useRoute } from 'vue-router';

export function useMain() {
  const route = useRoute();

  const showAside = computed(() => !!route.meta.showAside);

  const mainItemsClass = computed(() =>
    route.meta.layoutCenter ? 'items-center sm:items-start ' : '',
  );

  const mainJustifyClass = computed(() =>
    route.meta.layoutCenter ? 'justify-start sm:justify-center' : 'justify-start',
  );

  return {
    showAside,
    mainJustifyClass,
    mainItemsClass,
  };
}
