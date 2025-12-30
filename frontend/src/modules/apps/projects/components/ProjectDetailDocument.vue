<template>
  <div class="w-full">
    <div class="w-full p-5 rounded-2xl border-2 bg-white shadow-sm mb-5">
      <div class="w-full mb-8 flex flex-col items-center justify-center gap-2 text-center">
        <div class="w-full flex flex-col items-center justify-center gap-3 mb-5">
          <h1 class="text-lg font-semibold">Paste code</h1>
          <CommandLineIcon class="w-6 h-6" />
          <p class="text-base">Paste your code to generate programming documentation</p>
          <hr class="w-full border-1" />
        </div>

        <form
          method="post"
          class="w-full flex flex-col justify-center items-center gap-4 rounded sm:border-1 p-2 my-5"
          @submit.prevent="handleProjectDocument"
        >
          <div class="w-full flex flex-col justify-center items-center gap-3 mb-4">
            <div class="w-full flex flex-row justify-center items-center gap-1">
              <label class="font-bold" for="name">Format</label>
              <span class="text-error mt-1">*</span>
            </div>
            <Select
              v-model="selectedDocumentFormatOption"
              :options="documentFormatOptions"
              :error="projectDocumentFactory.formatError"
              @update:error="projectDocumentFactory.formatError = $event"
              placeholder="Select an option"
            />
          </div>

          <div class="w-full flex flex-col justify-center items-center gap-3">
            <div class="w-full flex flex-row justify-center items-center gap-1">
              <label class="font-bold" for="body-prompt">Body prompt</label>
              <span class="text-error mt-1">*</span>
            </div>

            <Loader :loading="storeCore.loaders.llm" />

            <div v-if="!storeCore.loaders.llm" class="w-full">
              <div class="w-full flex flex-col items-center justify-center gap-2 text-center">
                <p v-if="!storeLLM.llmFactory.id" class="text-base mb-2">
                  LLM tokens cannot be displayed
                </p>

                <div
                  v-else
                  class="flex flex-col lg:flex-row items-center justify-center gap-4 my-3"
                >
                  <div
                    class="w-64 rounded-2xl p-2 bg-gradient-to-r from-purple-600 to-blue-500 text-white font-bold shadow-lg"
                  >
                    <span>Max tokens per day: {{ storeLLM.llmFactory.max_tokens_per_day }}</span>
                  </div>

                  <div
                    class="w-64 rounded-2xl p-2 bg-gradient-to-r from-purple-600 to-blue-500 text-white font-bold shadow-lg"
                  >
                    <span
                      >Tokens used today: {{ storeLLM.llmFactory.tokens_per_day_used_today }}</span
                    >
                  </div>
                </div>
              </div>
            </div>

            <textarea
              class="border rounded w-full p-2 text-center resize-none min-h-96 mt-3"
              name="bodyPrompt"
              id="body-prompt"
              placeholder="Paste your code"
              v-model="projectDocumentFactory.bodyPrompt"
            ></textarea>

            <p
              v-if="projectDocumentFactory.bodyPromptError"
              class="w-full text-error text-center font-bold"
            >
              {{ projectDocumentFactory.bodyPromptError }}
            </p>
          </div>

          <div class="w-full flex flex-col justify-center items-center gap-4 mb-5">
            <Loader :loading="storeCore.loaders.projectDocumentCreate" />

            <button
              type="submit"
              class="!w-[280px] btn btn-dark mt-4"
              :class="{ disabled: storeCore.btnDisablers.projectDocumentCreateBtn }"
            >
              Generate documentation
            </button>
          </div>
        </form>
      </div>
    </div>

    <div class="w-full p-5 rounded-2xl border-2 bg-white shadow-sm mb-5">
      <div class="w-full flex flex-col items-center justify-center gap-3 mb-8">
        <h1 class="text-lg font-semibold">Documents</h1>
        <ClipboardDocumentListIcon class="w-6 h-6" />
        <p class="text-base">History</p>
        <hr class="w-full border-1" />
      </div>

      <Loader :loading="storeCore.loaders.projectDocumentsList" />

      <div v-if="!storeCore.loaders.projectDocumentsList" class="w-full">
        <div v-if="!storeProject.projectDocumentsListFactory.list.length" class="w-full">
          <p class="text-center">Documents cannot be displayed</p>
        </div>

        <div v-else class="w-full flex flex-col items-center justify-center gap-4">
          <div class="hidden xl:block overflow-x-auto w-full">
            <table class="border-separate border-spacing-0 border border-gray-400 w-full mb-5">
              <thead>
                <tr class="bg-gray-900 text-white">
                  <th class="py-3 px-4 font-semibold text-sm border border-gray-400 text-center">
                    User
                  </th>
                  <th class="py-3 px-4 font-semibold text-sm border border-gray-400 text-center">
                    Created
                  </th>
                  <th class="py-3 px-4 font-semibold text-sm border border-gray-400 text-center">
                    Updated
                  </th>
                  <th class="py-3 px-4 font-semibold text-sm border border-gray-400 text-center">
                    Rating
                  </th>
                  <th class="py-3 px-4 font-semibold text-sm border border-gray-400 text-center">
                    File
                  </th>
                </tr>
              </thead>

              <tbody>
                <tr v-for="doc in storeProject.projectDocumentsListFactory.list" :key="doc.id">
                  <td class="py-4 px-4 border border-gray-400 text-center">
                    <div class="flex flex-col items-center">
                      <SkeletonLoader
                        :src="doc.user_attachment"
                        type="user"
                        wrapper-classes="w-12 h-12 rounded-full overflow-hidden cursor-pointer"
                        alt="user attachment"
                      />
                    </div>
                  </td>

                  <td class="py-4 px-4 border border-gray-400 text-center">
                    {{ doc.created_at }}
                  </td>

                  <td class="py-4 px-4 border border-gray-400 text-center">
                    {{ doc.updated_at }}
                  </td>

                  <td class="py-4 px-4 border border-gray-400 text-center">
                    <div
                      v-if="!doc.voted_user_ids.includes(storeUser.userFactory.id)"
                      class="w-full"
                    >
                      <div class="flex flex-row items-center justify-center gap-2">
                        <div v-for="i in 5" :key="i">
                          <StarIcon
                            class="w-5 h-5"
                            :class="i <= doc.average_stars ? 'text-yellow-500' : 'text-gray-700'"
                          />
                        </div>
                      </div>

                      <button
                        type="button"
                        class="p-2 btn btn-dark mt-4"
                        @click="openModal(doc.id, i)"
                      >
                        Vote
                      </button>
                    </div>
                    <div v-else class="w-full flex flex-row items-center justify-center gap-2">
                      <div v-for="i in 5" :key="i">
                        <StarIcon
                          class="w-5 h-5"
                          :class="i <= doc.average_stars ? 'text-yellow-500' : 'text-gray-700'"
                        />
                      </div>
                    </div>
                  </td>

                  <td class="py-4 px-4 border border-gray-400 text-center">
                    <DocumentTextIcon
                      class="w-6 h-6 text-center m-auto cursor-pointer"
                      @click="openDocument(doc.attachment)"
                    />
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="xl:hidden flex flex-col text-center gap-4 w-full">
            <div
              v-for="doc in storeProject.projectDocumentsListFactory.list"
              :key="doc.id"
              class="flex flex-col items-center justify-center border rounded-lg p-3 bg-gray-50 gap-3"
            >
              <div class="flex flex-col items-center">
                <SkeletonLoader
                  :src="doc.user_attachment"
                  type="user"
                  wrapper-classes="w-12 h-12 rounded-full overflow-hidden cursor-pointer"
                  alt="user attachment"
                />
              </div>

              <span class="text-sm text-gray-700">
                <strong>Created:</strong> {{ doc.created_at }}
              </span>

              <span class="text-sm text-gray-700">
                <strong>Updated:</strong> {{ doc.updated_at }}
              </span>

              <div class="flex flex-col items-center justify-center gap-3">
                <span class="text-sm text-gray-700">
                  <strong>Rating:</strong>
                </span>

                <div
                  v-if="!doc.voted_user_ids.includes(storeUser.userFactory.id)"
                  class="w-full flex flex-col items-center justify-center"
                >
                  <div class="flex flex-row items-center justify-center gap-2">
                    <div v-for="i in 5" :key="i">
                      <StarIcon
                        class="w-5 h-5"
                        :class="i <= doc.average_stars ? 'text-yellow-500' : 'text-gray-700'"
                      />
                    </div>
                  </div>

                  <button type="button" class="p-2 btn btn-dark mt-4" @click="openModal(doc.id, i)">
                    Vote
                  </button>
                </div>
                <div v-else class="w-full flex flex-row items-center justify-center gap-2">
                  <div v-for="i in 5" :key="i">
                    <StarIcon
                      class="w-5 h-5"
                      :class="i <= doc.average_stars ? 'text-yellow-500' : 'text-gray-700'"
                    />
                  </div>
                </div>
              </div>

              <div class="flex flex-row items-center justify-center gap-1">
                <span class="text-sm text-gray-700">
                  <strong>File:</strong>
                </span>
                <DocumentTextIcon
                  class="w-6 h-6 text-gray-700 cursor-pointer"
                  @click="openDocument(doc.attachment)"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <Modal :show="isOpen" @close="closeModal">
      <template #modal-content>
        <div class="w-full flex flex-col items-center justify-center gap-4">
          <h2 class="text-lg font-semibold">Vote document</h2>
          <p class="text-center text-base mb-3">
            Please rate the quality of the generated information in this document by selecting one
            option
          </p>

          <div class="w-full flex flex-col items-center justify-center gap-3 mb-3">
            <label
              v-for="option in rateOptions"
              :key="option.value"
              class="flex flex-row items-center justify-center gap-2 cursor-pointer w-48 p-2 rounded-md border border-gray-300 hover:bg-gray-100 transition"
            >
              <input
                type="radio"
                name="document-rating"
                :value="option.value"
                v-model="projectDocumentVoteFactory.rating"
                class="cursor-pointer"
              />
              <span class="text-center inline-block w-20">{{ option.text }}</span>
            </label>

            <p
              v-if="projectDocumentVoteFactory.ratingError"
              class="w-full text-error text-center font-bold mt-3"
            >
              {{ projectDocumentVoteFactory.ratingError }}
            </p>
          </div>

          <Loader :loading="storeCore.loaders.projectDocumentVote" />

          <button
            type="button"
            @click="submitVote"
            class="!w-full sm:!w-[280px] p-2 btn btn-dark mt-4"
            :class="{ disabled: storeCore.btnDisablers.projectDocumentVoteBtn }"
          >
            Vote
          </button>
        </div>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import {
  CommandLineIcon,
  ClipboardDocumentListIcon,
  DocumentTextIcon,
  StarIcon,
} from '@heroicons/vue/24/outline';
import { useProjectDetailDocument } from '@/modules/apps/projects/composables/useProjectDetailDocument';
import { coreStore } from '@/modules/shared/common/stores/core/coreStore';
import { llmStore } from '@/modules/apps/llm/stores/llmStore';
import { projectStore } from '@/modules/apps/projects/stores/projectStore';
import { userStore } from '@/modules/apps/users/stores/userStore';
import Select from '@/modules/shared/common/components/ui/Select.vue';
import Loader from '@/modules/shared/common/components/ui/Loader.vue';
import SkeletonLoader from '@/modules/shared/common/components/ui/SkeletonLoader.vue';
import Modal from '@/modules/shared/common/components/ui/Modal.vue';

const props = defineProps({
  id: {
    type: String,
    required: true,
  },
});

const storeCore = coreStore();
const storeLLM = llmStore();
const storeProject = projectStore();
const storeUser = userStore();

const {
  documentFormatOptions,
  rateOptions,
  selectedDocumentFormatOption,
  projectDocumentFactory,
  projectDocumentVoteFactory,
  isOpen,

  handleProjectDocument,
  submitVote,
  openDocument,
  openModal,
  closeModal,
} = useProjectDetailDocument(props.id);
</script>

<style scoped></style>
