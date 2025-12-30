<template>
  <Loader :loading="storeCore.loaders.project" />

  <div v-if="!storeCore.loaders.project" class="w-full">
    <div v-if="!storeProject.projectFactory.id" class="w-full">
      <p class="text-center">Project data cannot be displayed</p>
    </div>

    <div v-else class="w-full flex flex-col items-center justify-center gap-4">
      <div
        class="w-full flex flex-col items-center justify-center gap-2 border-2 border-black rounded-lg p-2"
      >
        <div class="w-full flex flex-col items-center justify-center gap-1">
          <h1 class="text-lg font-semibold mb-2">Information</h1>
          <InformationCircleIcon class="w-6 h-6" />
        </div>

        <hr class="w-full border-1 mb-3" />

        <div class="w-full flex flex-col items-center gap-8 p-4">
          <div class="w-full max-w-3xl flex flex-col justify-between gap-6">
            <div
              class="w-full flex flex-col items-center justify-center rounded-lg border-1 shadow-sm gap-3 p-4"
            >
              <span
                class="w-full bg-gray-900 text-white text-base text-center font-medium rounded-lg p-2"
              >
                Name
              </span>
              <span class="text-lg font-semibold text-gray-900 text-center">
                {{ storeProject.projectFactory.name }}
              </span>
            </div>

            <div
              class="w-full flex flex-col items-center justify-center rounded-lg border-1 shadow-sm gap-3 p-4"
            >
              <span
                class="w-full bg-gray-900 text-white text-base text-center font-medium rounded-lg p-2"
              >
                Description
              </span>
              <span class="text-lg font-semibold text-gray-900 text-center">
                {{ storeProject.projectFactory.description }}
              </span>
            </div>

            <div
              class="w-full max-w-3xl flex flex-col lg:flex-row justify-between rounded-lg gap-3"
            >
              <div
                class="flex-1 flex flex-col items-center justify-center gap-2 p-4 bg-white border-1 rounded-lg shadow-sm"
              >
                <span
                  class="w-full bg-gray-900 text-white text-base text-center font-medium rounded-lg p-2"
                >
                  Privacy
                </span>
                <span class="text-lg font-semibold text-gray-900 text-center">
                  {{ storeProject.projectFactory.privacy }}
                </span>
              </div>

              <div
                class="flex-1 flex flex-col items-center justify-center gap-2 p-4 bg-white border-1 rounded-lg shadow-sm"
              >
                <span
                  class="w-full bg-gray-900 text-white text-base text-center font-medium rounded-lg p-2"
                >
                  Created
                </span>
                <span class="text-lg font-semibold text-gray-900 text-center">
                  {{ storeProject.projectFactory.created_at }}
                </span>
              </div>

              <div
                class="flex-1 flex flex-col items-center justify-center gap-2 p-4 bg-white border-1 rounded-lg shadow-sm"
              >
                <span
                  class="w-full bg-gray-900 text-white text-base text-center font-medium rounded-lg p-2"
                >
                  Last updated
                </span>
                <span class="text-lg font-semibold text-gray-900 text-center">
                  {{ storeProject.projectFactory.updated_at }}
                </span>
              </div>
            </div>

            <div
              class="w-full flex flex-col items-center justify-center rounded-lg border-1 shadow-sm gap-3 p-4"
            >
              <span
                class="w-full bg-gray-900 text-white text-base text-center font-medium rounded-lg p-2"
              >
                Users
              </span>
              <span class="text-lg font-semibold text-gray-900 text-center">
                {{
                  storeProject.projectFactory.users.length
                    ? `Total users: ${storeProject.projectFactory.users.length}`
                    : 'No users'
                }}
              </span>

              <div v-if="storeProject.projectFactory.users.length" class="w-full">
                <div
                  v-for="user in storeProject.projectFactory.users"
                  :key="user.id"
                  class="w-full flex flex-col items-center justify-center p-2 border-b border-black gap-4 sm:gap-0 min-h-[50px] last:border-b-0 last:mb-0 mb-4 hover:bg-gray-100 transition-colors duration-200"
                >
                  <div class="flex flex-col items-center justify-center gap-3">
                    <SkeletonLoader
                      :src="user.attachment"
                      type="user"
                      wrapper-classes="w-10 h-10 rounded-full overflow-hidden object-cover flex-shrink-0"
                      alt="user attachment"
                    />

                    <p class="font-semibold text-gray-900 text-center">
                      {{ user.first_name }} {{ user.last_name }}
                    </p>
                    <p class="font-medium text-gray-700 text-center">
                      {{ user.email }}
                    </p>
                    <p
                      class="font-semibold bg-gray-900 text-white text-center capitalize w-30 p-2 rounded-lg"
                    >
                      {{ user.role_project.name }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div
        class="w-full flex flex-col items-center justify-center gap-2 border-2 border-black rounded-lg p-2"
      >
        <div class="w-full flex flex-col items-center justify-center gap-1">
          <h1 class="text-lg font-semibold mb-2">Edit project</h1>
          <PencilIcon class="w-6 h-6" />
        </div>

        <hr class="w-full border-1 mb-3" />

        <div class="w-full flex flex-col items-center gap-8 p-4">
          <div class="w-full max-w-3xl flex flex-col justify-between gap-6">
            <form
              method="post"
              class="w-full flex flex-col justify-center items-center gap-5 rounded-lg sm:border-1 p-4"
              @submit.prevent="handleUpdateProject"
            >
              <div class="w-full flex flex-col justify-center items-center gap-3">
                <div class="w-full flex flex-row justify-center items-center gap-1">
                  <label class="font-bold" for="project-name">Name</label>
                  <span class="text-error mt-1">*</span>
                </div>
                <input
                  class="w-full p-2 border-1 rounded text-center"
                  type="text"
                  name="projectName"
                  id="project-name"
                  placeholder="Enter project name"
                  v-model="basicProfileUpdateFactory.name"
                />
                <p
                  v-if="basicProfileUpdateFactory.nameError"
                  class="w-full text-error text-center font-bold"
                >
                  {{ basicProfileUpdateFactory.nameError }}
                </p>
              </div>
              <div class="w-full flex flex-col justify-center items-center gap-3">
                <div class="w-full flex flex-row justify-center items-center gap-1">
                  <label class="font-bold" for="project-description">Description</label>
                  <span class="text-error mt-1">*</span>
                </div>
                <textarea
                  class="border rounded w-full p-2 text-center resize-none min-h-24"
                  name="projectDescription"
                  id="project-description"
                  placeholder="Enter project description"
                  v-model="basicProfileUpdateFactory.description"
                ></textarea>
                <p
                  v-if="basicProfileUpdateFactory.descriptionError"
                  class="w-full text-error text-center font-bold"
                >
                  {{ basicProfileUpdateFactory.descriptionError }}
                </p>
              </div>
              <div class="w-full flex flex-col justify-center items-center gap-3">
                <div class="w-full flex flex-row justify-center items-center gap-1">
                  <label class="font-bold" for="name">Privacy</label>
                  <span class="text-error mt-1">*</span>
                </div>
                <Select
                  v-model="selectedOption"
                  :options="options"
                  :error="basicProfileUpdateFactory.privacyError"
                  @update:error="basicProfileUpdateFactory.privacyError = $event"
                  placeholder="Select an option"
                />
              </div>

              <div class="w-full flex flex-col justify-center items-center gap-5 mt-2">
                <label class="font-bold" for="project-users">Users</label>

                <div
                  v-if="
                    storeProject.projectFactory.users.length &&
                    storeProject.projectFactory.users.some(u => u.id !== storeUser.userFactory.id)
                  "
                  class="w-full"
                >
                  <p class="w-full text-center font-medium text-gray-700 mb-3">
                    Select users to exclude from this project
                  </p>

                  <div
                    class="w-full max-h-[220px] overflow-y-auto border border-gray-300 rounded p-2"
                  >
                    <div
                      v-for="user in storeProject.projectFactory.users.filter(
                        u => u.role_project.name === 'member',
                      )"
                      :key="user.id"
                      class="w-full flex flex-col sm:flex-row items-center justify-between p-2 border-b border-black gap-4 sm:gap-0 min-h-[50px] last:border-b-0 last:mb-0 mb-4 hover:bg-gray-100 transition-colors duration-200"
                    >
                      <div class="flex flex-col sm:flex-row items-center gap-4">
                        <SkeletonLoader
                          :src="user.attachment"
                          type="user"
                          wrapper-classes="w-10 h-10 rounded-full overflow-hidden object-cover flex-shrink-0"
                          alt="user attachment"
                        />
                        <div class="flex flex-col text-center sm:text-left justify-center">
                          <p class="font-semibold">{{ user.first_name }} {{ user.last_name }}</p>
                          <p class="text-sm text-gray-600">{{ user.email }}</p>
                        </div>
                      </div>

                      <input
                        type="checkbox"
                        :value="user.id"
                        v-model="basicProfileUpdateFactory.users_to_exclude"
                        class="flex-shrink-0"
                      />
                    </div>
                  </div>
                </div>

                <Loader :loading="storeCore.loaders.overview" />

                <div v-if="!storeCore.loaders.overview" class="w-full">
                  <div
                    v-if="storeUsers.usersFactory.list.length"
                    class="w-full flex flex-col justify-center items-center gap-3-"
                  >
                    <p class="w-full text-center font-medium text-gray-700 mb-3">
                      Select users to include in this project
                    </p>

                    <div
                      class="w-full max-h-[220px] overflow-y-auto border border-gray-300 rounded p-2"
                    >
                      <div
                        v-for="user in storeUsers.usersFactory.list.filter(
                          u => !storeProject.projectFactory.users.some(pu => pu.id === u.id),
                        )"
                        :key="user.id"
                        class="w-full flex flex-col sm:flex-row items-center justify-between p-2 border-b border-black gap-4 sm:gap-0 min-h-[50px] last:border-b-0 last:mb-0 mb-4 hover:bg-gray-100 transition-colors duration-200"
                      >
                        <div class="flex flex-col sm:flex-row items-center gap-4">
                          <SkeletonLoader
                            :src="user.attachment"
                            type="user"
                            wrapper-classes="w-10 h-10 rounded-full overflow-hidden object-cover flex-shrink-0"
                            alt="user attachment"
                          />
                          <div class="flex flex-col text-center sm:text-left justify-center">
                            <p class="font-semibold">{{ user.first_name }} {{ user.last_name }}</p>
                            <p class="text-sm text-gray-600">{{ user.email }}</p>
                          </div>
                        </div>

                        <input
                          type="checkbox"
                          :value="user.id"
                          v-model="basicProfileUpdateFactory.users_to_add"
                          class="flex-shrink-0"
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="w-full flex flex-col justify-center items-center gap-4">
                <Loader :loading="storeCore.loaders.projectUpdate" />
                <button
                  type="submit"
                  class="!w-full sm:!w-[280px] btn btn-dark mt-4"
                  :class="{ disabled: storeCore.btnDisablers.projectUpdateBtn }"
                >
                  Update project
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

      <div
        class="w-full flex flex-col items-center justify-center gap-2 border-2 border-black rounded-lg p-2"
      >
        <div class="w-full flex flex-col items-center justify-center gap-1">
          <h1 class="text-lg font-semibold mb-2">Delete project</h1>
          <TrashIcon class="w-6 h-6" />
        </div>

        <hr class="w-full border-1 mb-3" />

        <div class="flex flex-col items-center justify-center gap-6">
          <p class="text-base text-center mt-4">
            Permanently delete this project and all associated data.
          </p>
          <p class="text-base text-center">
            This action cannot be undone. This will permanently delete the project
            <span class="text-base font-semibold"> {{ storeProject.projectFactory.name }} </span>
            and remove all associated data.
          </p>
          <button
            type="button"
            class="!w-full sm:!w-[280px] p-2 btn btn-danger mt-4"
            @click="openModal"
          >
            Delete Profile
          </button>
        </div>
      </div>
    </div>
  </div>

  <Modal :show="isOpen" @close="closeModal">
    <template #modal-content>
      <div class="w-full flex flex-col items-center justify-center gap-4">
        <h2 class="text-lg font-semibold text-error">Confirm Project Deletion</h2>
        <p class="text-center text-base">
          Are you sure you want to permanently delete this project?
        </p>

        <Loader :loading="storeCore.loaders.projectDelete" />

        <div class="flex gap-3 mt-4 w-full">
          <button
            type="button"
            class="!w-full sm:!w-[280px] p-2 btn btn-secondary mt-4"
            @click="closeModal"
          >
            Cancel
          </button>

          <button
            type="button"
            @click="deleteProject"
            class="!w-full sm:!w-[280px] p-2 btn btn-danger mt-4"
            :class="{ disabled: storeCore.btnDisablers.projectDeleteBtn }"
          >
            Delete
          </button>
        </div>
      </div>
    </template>
  </Modal>
</template>

<script setup>
import { InformationCircleIcon, PencilIcon, TrashIcon } from '@heroicons/vue/24/outline';
import { useProjectDetailData } from '@/modules/apps/projects/composables/useProjectDetailData';
import { coreStore } from '@/modules/shared/common/stores/core/coreStore';
import { userStore } from '@/modules/apps/users/stores/userStore';
import { usersStore } from '@/modules/apps/users/stores/usersStore';
import { projectStore } from '@/modules/apps/projects/stores/projectStore';
import Loader from '@/modules/shared/common/components/ui/Loader.vue';
import SkeletonLoader from '@/modules/shared/common/components/ui/SkeletonLoader.vue';
import Select from '@/modules/shared/common/components/ui/Select.vue';
import Modal from '@/modules/shared/common/components/ui/Modal.vue';

const props = defineProps({
  id: {
    type: String,
    required: true,
  },
});

const storeCore = coreStore();
const storeUser = userStore();
const storeUsers = usersStore();
const storeProject = projectStore();

const {
  isOpen,
  options,
  selectedOption,
  basicProfileUpdateFactory,

  handleUpdateProject,
  deleteProject,
  openModal,
  closeModal,
} = useProjectDetailData(props.id);
</script>

<style scoped></style>
