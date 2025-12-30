import { useTypeCheck } from '@/modules/shared/common/composables/utils/useTypeCheck';

export function useStringify() {
  const { isType } = useTypeCheck();

  const stringify = value => {
    if (isType(value, 'string')) {
      return value;
    }
    return JSON.stringify(value, null, 2);
  };

  return {
    stringify,
  };
}
