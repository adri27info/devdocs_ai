<template>
  <section class="w-full p-8">
    <Loader :loading="storeCore.loaders.overview" />

    <div v-if="!storeCore.loaders.overview" class="w-full">
      <div class="w-full mb-5 flex flex-col items-center justify-center gap-2">
        <h1 class="text-xl font-semibold mb-2">Overview</h1>
        <p class="text-base">
          {{ filteredUsers.length ? `Total users: ${filteredUsers.length}` : 'No users' }}
        </p>
      </div>

      <div v-if="filteredUsers.length" class="w-full">
        <div v-for="user in filteredUsers" :key="user.id" class="p-2">
          <div
            class="w-full flex flex-col lg:flex-row items-center justify-between gap-5 lg:gap-0 mb-6 rounded-2xl border-2"
          >
            <div class="flex flex-col w-full lg:w-72 items-center justify-center gap-3">
              <div class="mt-3">
                <SkeletonLoader
                  :src="user.attachment"
                  type="user"
                  wrapper-classes="w-24 h-24 rounded-full overflow-hidden cursor-pointer object-cover"
                  alt="user attachment"
                />
              </div>
              <div class="text-center w-full p-2">
                <h1 class="font-bold">{{ user.first_name }} {{ user.last_name }}</h1>
                <h1 class="font-semibold">{{ user.email }}</h1>
              </div>
            </div>

            <div class="w-full lg:w-72 text-center">
              <button
                type="button"
                class="mb-3 lg:mb-0 btn"
                :class="isFreePlan ? 'bg-gray-300 text-gray-600 cursor-not-allowed' : 'btn-dark'"
                :disabled="isFreePlan"
                @click="openModal(user.id)"
              >
                Add user to project
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <Modal :show="isOpen" @close="closeModal">
      <template #modal-content>
        <div class="w-full flex flex-col justify-center items-center gap-3">
          <Loader :loading="storeCore.loaders.projects" />

          <div v-if="!storeCore.loaders.projects" class="w-full">
            <div class="w-full flex flex-row justify-center items-center gap-1 my-4">
              <h1 class="text-xl font-semibold">Projects</h1>
            </div>

            <p
              v-if="!storeProject.projectsListFactory.list.length"
              class="text-base text-center my-6"
            >
              You dont have projects yet.
            </p>

            <div v-else class="w-full flex flex-col items-center justify-center gap-4">
              <p class="text-base text-center mb-2">
                Select the project to which you want to add the user.
              </p>

              <form
                method="post"
                class="w-full flex flex-col justify-center items-center gap-4 rounded sm:border-1 p-0 sm:p-2 mb-5"
                @submit.prevent="handleAddUserProject"
              >
                <div
                  class="w-full max-h-[220px] overflow-y-auto border border-gray-300 rounded p-2"
                >
                  <div
                    v-for="project in storeProject.projectsListFactory.list"
                    :key="project.id"
                    class="w-full flex flex-col sm:flex-row items-center justify-between px-2 py-2 border-b border-black gap-7 sm:gap-0 last:border-b-0 last:mb-0 hover:bg-gray-100 transition-colors duration-200"
                  >
                    <div class="w-full flex items-center justify-between my-2">
                      <div class="w-full flex flex-col items-start justify-cenceter gap-2">
                        <h1 class="font-semibold">{{ truncText(project.name, 20) }}</h1>
                        <div
                          class="bg-gray-600 w-24 flex flex-row items-center justify-center gap-1 rounded p-1"
                        >
                          <component
                            :is="project.privacy === 'public' ? LockOpenIcon : LockClosedIcon"
                            class="h-4 w-4"
                            :class="project.privacy === 'public' ? 'text-success' : 'text-error'"
                          />
                          <span class="text-white">
                            {{ project.privacy.charAt(0).toUpperCase() + project.privacy.slice(1) }}
                          </span>
                        </div>
                      </div>

                      <input
                        type="checkbox"
                        :value="project.id"
                        v-model="overviewFactory.projects_selected"
                        class="flex-shrink-0"
                      />
                    </div>
                  </div>
                </div>

                <div class="w-full flex flex-col justify-center items-center gap-4">
                  <Loader :loading="storeCore.loaders.projectAddUser" />
                  <button
                    type="submit"
                    class="!w-[280px] btn btn-dark mt-4"
                    :class="{ disabled: storeCore.btnDisablers.projectAddUserBtn }"
                  >
                    Add user
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </template>
    </Modal>
  </section>
</template>

<script setup>
import { LockOpenIcon, LockClosedIcon } from '@heroicons/vue/24/outline';
import { useOverview } from '@/modules/apps/users/overview/composables/useOverview';
import { useTextTruncator } from '@/modules/shared/common/composables/utils/useTextTruncator';
import { coreStore } from '@/modules/shared/common/stores/core/coreStore';
import { projectStore } from '@/modules/apps/projects/stores/projectStore';
import Loader from '@/modules/shared/common/components/ui/Loader.vue';
import SkeletonLoader from '@/modules/shared/common/components/ui/SkeletonLoader.vue';
import Modal from '@/modules/shared/common/components/ui/Modal.vue';

const storeCore = coreStore();
const storeProject = projectStore();

const { truncText } = useTextTruncator();
const {
  overviewFactory,
  isFreePlan,
  isOpen,
  filteredUsers,
  openModal,
  closeModal,
  handleAddUserProject,
} = useOverview();
</script>

<style scoped></style>
