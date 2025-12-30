<template>
  <Header>
    <template #header-content>
      <section class="w-full flex flex-col sm:flex-row items-center justify-between">
        <div class="w-35 sm:ml-5.5">
          <img class="w-full object-cover" :src="logo" alt="Logo DevDocs AI" />
        </div>

        <div
          class="relative flex flex-col sm:flex-row justify-between items-center gap-4 mb-5 sm:gap-2 sm:mb-0"
        >
          <div v-if="hasRoleUser">
            <RouterLink
              :to="{ name: 'projects' }"
              class="!w-40 btn btn-secondary flex flex-row items-center justify-center gap-2"
            >
              <FolderIcon class="h-4 w-4 mt-0.5 text-white" />
              <span>New project</span>
            </RouterLink>
          </div>

          <div class="relative flex flex-col items-center justify-center w-32">
            <div
              @click="toggleDropdown"
              class="w-12 h-12 rounded-full cursor-pointer overflow-hidden"
            >
              <SkeletonLoader
                :src="avatarSrc"
                type="user"
                wrapper-classes="w-12 h-12 rounded-full overflow-hidden cursor-pointer"
                alt="user attachment"
              />
            </div>

            <div
              v-show="showDropdown"
              class="w-32 absolute top-full mt-1 border-2 border-black text-black text-center rounded shadow-lg z-10 bg-white"
            >
              <ul>
                <li class="general-custom-hover py-1 border-b-2 border-black cursor-pointer">
                  <RouterLink :to="{ name: 'profile' }" @click="closeDropdown">
                    Profile
                  </RouterLink>
                </li>
                <li>
                  <button
                    type="button"
                    @click="logoutAndCloseDropdown"
                    class="general-custom-hover py-1 cursor-pointer w-full"
                    :class="{ disabled: storeCore.btnDisablers.logoutBtn }"
                  >
                    Sign out
                  </button>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>
    </template>
  </Header>
</template>

<script setup>
import { FolderIcon } from '@heroicons/vue/24/outline';
import { useSessionLogout } from '@/modules/shared/common/composables/session/useSessionLogout';
import { useDropdown } from '@/modules/shared/common/composables/utils/ui/useDropdown';
import { useHeaderUser } from '@/modules/shared/common/composables/core/infraestructure/parts/header/useHeaderUser';
import { useEnvironment } from '@/modules/shared/common/composables/utils/ui/useEnvironment';
import { coreStore } from '@/modules/shared/common/stores/core/coreStore';
import Header from '@/modules/shared/common/components/infraestructure/parts/headers/base/Header.vue';
import SkeletonLoader from '@/modules/shared/common/components/ui/SkeletonLoader.vue';

const storeCore = coreStore();

const { logo } = useEnvironment();
const { handleLogout } = useSessionLogout();
const { showDropdown, toggleDropdown, closeDropdown } = useDropdown();
const { avatarSrc, hasRoleUser, logoutAndCloseDropdown } = useHeaderUser(
  handleLogout,
  closeDropdown,
);
</script>

<style scoped></style>
