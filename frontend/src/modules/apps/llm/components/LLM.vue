<template>
  <section class="w-full p-8">
    <Loader :loading="storeCore.loaders.llm" />

    <div v-if="!storeCore.loaders.llm" class="w-full">
      <div class="w-full mb-8 flex flex-col items-center justify-center gap-2 text-center">
        <h1 class="text-xl font-semibold mb-2">LLM</h1>
        <p class="text-base">
          {{
            storeLLM.llmFactory.id
              ? "Here's an overview of your LLM"
              : 'LLM data cannot be displayed'
          }}
        </p>
      </div>

      <div v-if="storeLLM.llmFactory.id" class="w-full text-center">
        <div class="w-full flex justify-center items-start">
          <div class="w-full p-5 rounded-2xl border-2 bg-white shadow-sm">
            <div class="hidden xl:block overflow-x-auto">
              <table class="border-separate border-spacing-0 border border-gray-400 w-full mb-5">
                <thead>
                  <tr class="bg-gray-900 text-white">
                    <th
                      v-for="key in visibleKeys"
                      :key="key"
                      class="py-3 px-4 font-semibold text-sm border border-gray-400 text-center"
                    >
                      {{ formatKey(key) }}
                    </th>
                  </tr>
                </thead>

                <tbody>
                  <tr>
                    <td
                      v-for="key in visibleKeys"
                      :key="key"
                      class="py-4 px-4 border border-gray-400 align-middle min-w-[200px] whitespace-nowrap"
                    >
                      <div class="flex flex-col justify-center items-center gap-1 text-center">
                        <template v-if="key === 'attachment' && isUrl(storeLLM.llmFactory[key])">
                          <SkeletonLoader
                            :src="storeLLM.llmFactory[key]"
                            type="llm"
                            wrapper-classes="w-12 h-12 rounded-full overflow-hidden cursor-pointer"
                            alt="llm attachment"
                          />
                        </template>

                        <template v-else-if="isUrl(storeLLM.llmFactory[key])">
                          <a
                            :href="storeLLM.llmFactory[key]"
                            target="_blank"
                            class="text-blue-600 underline"
                          >
                            {{ storeLLM.llmFactory[key] }}
                          </a>
                        </template>

                        <template v-else>
                          {{ storeLLM.llmFactory[key] }}
                        </template>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div class="xl:hidden flex flex-col text-center gap-4">
              <div
                v-for="key in visibleKeys"
                :key="key"
                class="flex flex-col border-1 border-black rounded-lg p-3 bg-gray-50 items-center"
              >
                <div class="bg-gray-900 w-full mb-2 p-2">
                  <span class="text-base text-white text-center">{{ formatKey(key) }}</span>
                </div>

                <span class="mt-1 flex flex-col justify-center items-center gap-1 text-center">
                  <template v-if="key === 'attachment' && isUrl(storeLLM.llmFactory[key])">
                    <SkeletonLoader
                      :src="storeLLM.llmFactory[key]"
                      type="llm"
                      wrapper-classes="w-12 h-12 rounded-full overflow-hidden cursor-pointer"
                      alt="llm attachment"
                    />
                  </template>

                  <template v-else-if="isUrl(storeLLM.llmFactory[key])">
                    <a
                      :href="storeLLM.llmFactory[key]"
                      target="_blank"
                      class="text-blue-600 underline text-center"
                    >
                      {{ storeLLM.llmFactory[key] }}
                    </a>
                  </template>

                  <template v-else>
                    {{ storeLLM.llmFactory[key] }}
                  </template>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useLLM } from '@/modules/apps/llm/composables/useLLM';
import { coreStore } from '@/modules/shared/common/stores/core/coreStore';
import { llmStore } from '@/modules/apps/llm/stores/llmStore';
import Loader from '@/modules/shared/common/components/ui/Loader.vue';
import SkeletonLoader from '@/modules/shared/common/components/ui/SkeletonLoader.vue';

const storeCore = coreStore();
const storeLLM = llmStore();

const { isUrl, formatKey, visibleKeys } = useLLM();
</script>

<style scoped></style>
