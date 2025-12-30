import { reactive, toRefs } from 'vue';
import { defineStore } from 'pinia';
import { LLMService } from '@/modules/apps/llm/services/llmService';
import { createLLMFactory } from '@/modules/apps/llm/factories/llmFactory';
import { useSessionCleaner } from '@/modules/shared/common/composables/session/useSessionCleaner';
import { useRequestHandler } from '@/modules/shared/common/composables/api/request/useRequestHandler';
import { useDelay } from '@/modules/shared/common/composables/utils/useDelay';
import { coreStore } from '@/modules/shared/common/stores/core/coreStore';

export const llmStore = defineStore('llmStore', () => {
  const llmService = new LLMService();
  const storeCore = coreStore();

  const llmFactory = reactive(createLLMFactory());

  const loadersRefs = toRefs(storeCore.loaders);

  const { delay } = useDelay();
  const { clearSessionIsNeeded } = useSessionCleaner();
  const { handleAPIRequest } = useRequestHandler();

  const getLLM = () => {
    return handleAPIRequest({
      actions: {
        beforeRequest: () => {
          loadersRefs.llm.value = true;
        },
        afterRequest: async data => {
          if (data?.llm) {
            Object.assign(llmFactory, data.llm);
          }
        },
        onFinally: async () => {
          clearSessionIsNeeded();
          await delay();
          loadersRefs.llm.value = false;
        },
      },
      request: () => llmService.getLLM(),
      expectedStatus: 200,
      operation: 'LLM',
      fnToRetry: () => getLLM(),
      allowRetry: true,
    });
  };

  return {
    llmFactory,

    getLLM,
  };
});
