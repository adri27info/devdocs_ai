import { computed, onMounted } from 'vue';
import { PATTERNS } from '@/modules/shared/common/constants/apps/llm/patterns';
import { useTypeCheck } from '@/modules/shared/common/composables/utils/useTypeCheck';
import { useFetcher } from '@/modules/shared/common/composables/utils/useFetcher';
import { llmStore } from '@/modules/apps/llm/stores/llmStore';

export function useLLM() {
  const storeLLM = llmStore();

  const { isType } = useTypeCheck();
  const { fetch } = useFetcher();

  const visibleKeys = computed(() => {
    if (!storeLLM.llmFactory) return [];

    const keys = Object.keys(storeLLM.llmFactory).filter(key => key !== 'id');
    const attachmentIndex = keys.indexOf('attachment');

    if (attachmentIndex > -1) {
      keys.splice(attachmentIndex, 1);
      keys.unshift('attachment');
    }

    return keys;
  });

  const replaceUnderscore = () => ' ';
  const capitalizeChar = char => char.toUpperCase();
  const isUrl = value => isType(value, 'string') && PATTERNS.HTTP.test(value);

  const formatKey = key =>
    key
      .replace(PATTERNS.UNDERSCORE, replaceUnderscore)
      .replace(PATTERNS.WORD_START, capitalizeChar);

  onMounted(async () => {
    await fetch({
      app: 'llm',
      hideSuccess: true,
    });
  });

  return {
    visibleKeys,

    isUrl,
    formatKey,
  };
}
