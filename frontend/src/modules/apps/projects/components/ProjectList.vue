<template>
  <section class="w-full p-8">
    <div class="w-full bg-white">
      <div class="w-full mb-5 flex flex-col items-center justify-center gap-2">
        <h1 class="text-xl font-semibold mb-2">Projects</h1>
        <p class="text-base">
          {{
            storeProject.projectsListFactory.list.length
              ? `Total projects: ${storeProject.projectsListFactory.list.length}`
              : 'No projects'
          }}
        </p>
      </div>

      <div class="w-full mb-5 flex flex-col items-center justify-center gap-2">
        <div class="w-full p-5 rounded-2xl border-2 bg-white shadow-sm">
          <div class="w-full flex flex-col items-center justify-center mt-3 mb-6">
            <button type="button" class="btn btn-secondary" @click="openModal">
              Create new project
            </button>
          </div>

          <div class="w-full flex flex-col lg:flex-row justify-center items-center gap-3">
            <MenuOptions
              :items="menuProjectsItems"
              item-classes="general-custom-hover w-full lg:flex-1 flex flex-col justify-center items-center bg-gray-900 hover:bg-gray-700 text-white rounded-lg p-2 transition"
              type="button"
              buttonClasses="w-full flex flex-col items-center justify-center gap-2"
              icon-classes="h-6 w-6"
              @click="handleMenuClick"
            />
          </div>
        </div>

        <input
          type="text"
          name="projects"
          id="projects"
          placeholder="Search project by name..."
          class="w-full lg:w-130 p-2 rounded border-2 text-center block m-auto mt-10 mb-5"
          v-model="searchQuery"
        />

        <Loader :loading="storeCore.loaders.projects" />

        <div v-if="!storeCore.loaders.projects" class="w-full">
          <div v-if="storeProject.projectsListFactory.list.length" class="w-full">
            <div class="w-full flex flex-col 2xl:flex-row items-center justify-center gap-4 mt-10">
              <div
                v-for="project in storeProject.projectsListFactory.list"
                :key="project.id"
                class="w-full xl:w-170 2xl:w-120 min-h-48 flex flex-col items-center justify-between rounded-2xl border-2 p-3 mt-3"
              >
                <div class="w-full flex flex-col gap-2 items-center justify-between">
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

                <p class="w-full mt-6 text-center">
                  {{ truncText(project.description, 20) }}
                </p>

                <hr class="w-full my-5" />

                <div class="w-full flex flex-col 2xl:flex-row items-center justify-between gap-3">
                  <div class="flex flex-row items-center justify-center gap-1 order-2 2xl:order-1">
                    <CalendarDaysIcon class="h-4 w-4" />
                    <span>{{ project.created_at }}</span>
                  </div>

                  <div
                    class="flex flex-col xl:flex-row items-center justify-center gap-1 order-1 2xl:order-2"
                  >
                    <RouterLink
                      :to="{ name: 'projects-detail', params: { id: project.id } }"
                      class="flex flex-row items-center justify-center gap-1 px-3 py-1 bg-gray-900 hover:bg-gray-700 text-white rounded-full transition"
                    >
                      <EyeIcon class="h-4 w-4 mt-0.5" />
                      <span>View</span>
                    </RouterLink>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <Modal :show="isOpen" @close="closeModal">
      <template #modal-content>
        <div class="w-full flex flex-col items-center justify-center gap-4">
          <h1 class="text-xl font-semibold mb-2">Project</h1>
          <p class="text-base text-center mb-2">Fill the form to create new project.</p>

          <form
            method="post"
            class="w-full flex flex-col justify-center items-center gap-4 rounded sm:border-1 p-2 mb-5"
            @submit.prevent="handleCreateProject"
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
                v-model="basicProfileCreateFactory.name"
              />
              <p
                v-if="basicProfileCreateFactory.nameError"
                class="w-full text-error text-center font-bold"
              >
                {{ basicProfileCreateFactory.nameError }}
              </p>
            </div>
            <div class="w-full flex flex-col justify-center items-center gap-3">
              <div class="w-full flex flex-row justify-center items-center gap-1">
                <label class="font-bold" for="project-description">Description</label>
                <span class="text-error mt-1">*</span>
              </div>
              <textarea
                class="border rounded w-full p-2 text-center resize-none min-h-16"
                name="projectDescription"
                id="project-description"
                placeholder="Enter project description"
                v-model="basicProfileCreateFactory.description"
              ></textarea>
              <p
                v-if="basicProfileCreateFactory.descriptionError"
                class="w-full text-error text-center font-bold"
              >
                {{ basicProfileCreateFactory.descriptionError }}
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
                :error="basicProfileCreateFactory.privacyError"
                @update:error="basicProfileCreateFactory.privacyError = $event"
                placeholder="Select an option"
              />
            </div>
            <div class="w-full flex flex-col justify-center items-center gap-3">
              <div class="w-full flex flex-row justify-center items-center gap-1">
                <label class="font-bold" for="project-users">Users</label>
              </div>

              <Loader :loading="storeCore.loaders.overview" />

              <div v-if="!storeCore.loaders.overview" class="w-full">
                <p v-if="!storeUsers.usersFactory.list.length" class="text-base text-center mb-3">
                  No users
                </p>

                <div
                  v-else
                  class="w-full max-h-[220px] overflow-y-auto border border-gray-300 rounded p-2"
                >
                  <div
                    v-for="user in storeUsers.usersFactory.list.filter(
                      u => u.id !== storeUser.userFactory.id,
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
                      v-model="basicProfileCreateFactory.users"
                      class="flex-shrink-0"
                    />
                  </div>
                </div>
              </div>
            </div>
            <div class="w-full flex flex-col justify-center items-center gap-4">
              <Loader :loading="storeCore.loaders.projectCreate" />
              <button
                type="submit"
                class="!w-[280px] btn btn-dark mt-4"
                :class="{ disabled: storeCore.btnDisablers.projectCreateBtn }"
              >
                Create project
              </button>
            </div>
          </form>
        </div>
      </template>
    </Modal>
  </section>
</template>

<script setup>
import { CalendarDaysIcon, EyeIcon, LockOpenIcon, LockClosedIcon } from '@heroicons/vue/24/outline';
import { useTextTruncator } from '@/modules/shared/common/composables/utils/useTextTruncator';
import { useProjectList } from '@/modules/apps/projects/composables/useProjectList';
import { useProjectCreate } from '@/modules/apps/projects/composables/useProjectCreate';
import { coreStore } from '@/modules/shared/common/stores/core/coreStore';
import { userStore } from '@/modules/apps/users/stores/userStore';
import { usersStore } from '@/modules/apps/users/stores/usersStore';
import { projectStore } from '@/modules/apps/projects/stores/projectStore';
import Loader from '@/modules/shared/common/components/ui/Loader.vue';
import MenuOptions from '@/modules/shared/common/components/ui/MenuOptions.vue';
import Modal from '@/modules/shared/common/components/ui/Modal.vue';
import Select from '@/modules/shared/common/components/ui/Select.vue';
import SkeletonLoader from '@/modules/shared/common/components/ui/SkeletonLoader.vue';

const storeCore = coreStore();
const storeUser = userStore();
const storeUsers = usersStore();
const storeProject = projectStore();

const { truncText } = useTextTruncator();

const { menuProjectsItems, searchQuery, handleMenuClick } = useProjectList();
const {
  options,
  selectedOption,
  basicProfileCreateFactory,
  isOpen,
  openModal,
  closeModal,
  handleCreateProject,
} = useProjectCreate();
</script>

<style scoped></style>
