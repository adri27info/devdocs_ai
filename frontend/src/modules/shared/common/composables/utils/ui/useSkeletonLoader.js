import { ref, computed, watch, onMounted, onUnmounted } from 'vue';
import { useEnvironment } from '@/modules/shared/common/composables/utils/ui/useEnvironment';

const cachedImages = new Set();

export function useSkeletonLoader(props) {
  const loaded = ref(false);
  const currentSrc = ref(props.src);

  let timeoutId;

  const { userProfile, imageNotFound, llm } = useEnvironment();

  const fallbackMap = {
    user: userProfile,
    imageNotFound: imageNotFound,
    llm: llm,
  };

  const imgClasses = computed(() => [
    'w-full',
    'h-full',
    'object-cover',
    props.rounded ? 'rounded-full' : 'rounded-none',
  ]);

  const defaultFallback = async () => {
    const fallback = fallbackMap[props.type];
    return fallback;
  };

  const handleLoad = () => {
    clearTimeout(timeoutId);

    setTimeout(() => {
      loaded.value = true;
      cachedImages.add(currentSrc.value);
    }, props.delay);
  };

  const handleError = async () => {
    clearTimeout(timeoutId);

    const fallbackUrl = await defaultFallback();

    if (fallbackUrl && fallbackUrl !== currentSrc.value) {
      currentSrc.value = fallbackUrl;
    } else {
      loaded.value = false;
    }
  };

  const startTimeout = () => {
    clearTimeout(timeoutId);

    timeoutId = setTimeout(() => {
      if (!loaded.value) {
        handleError();
      }
    }, props.delay + 3500);
  };

  const checkCached = src => {
    if (cachedImages.has(src)) {
      loaded.value = true;
      return true;
    }

    const img = new Image();
    img.src = src;

    if (img.complete && img.naturalWidth !== 0) {
      loaded.value = true;
      cachedImages.add(src);
      return true;
    }

    return false;
  };

  watch(
    () => props.src,
    newSrc => {
      currentSrc.value = newSrc;

      if (!checkCached(newSrc)) {
        loaded.value = false;
        startTimeout();
      }
    },
    { immediate: true },
  );

  onMounted(() => startTimeout());
  onUnmounted(() => clearTimeout(timeoutId));

  return {
    loaded,
    currentSrc,
    imgClasses,

    handleLoad,
    handleError,
  };
}
