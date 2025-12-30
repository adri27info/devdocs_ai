<template>
  <section class="w-full p-3 sm:p-8">
    <div class="w-full mb-8 flex flex-col items-center justify-center gap-2 text-center">
      <h1 class="text-xl font-semibold mb-2">Profile</h1>
      <p class="text-base">This section allows you to remove your user profile.</p>
    </div>

    <div
      class="w-full mt-10 flex flex-col items-center justify-center gap-3 p-2 sm:p-4 bg-white border-black border-2 rounded-xl"
    >
      <div class="w-full rounded-xl flex flex-col items-center justify-center gap-4">
        <h1 class="text-lg font-semibold mb-2">Danger zone</h1>
        <p class="text-base text-justify">
          Deleting your profile is permanent and cannot be undone. All your projects, data and
          configuration will be permanently removed.
        </p>
        <p class="text-base text-justify">
          To continue, click <span class="font-semibold text-error">Delete Profile</span> and
          confirm by typing
          <span class="font-mono bg-gray-100 px-2 py-0.5 rounded text-error">delete</span>. This
          action cannot be undone.
        </p>

        <button
          type="button"
          class="!w-full sm:!w-[280px] p-2 btn btn-danger mt-4"
          @click="openModal"
        >
          Delete Profile
        </button>

        <RouterLink :to="{ name: 'settings' }" class="!w-full sm:!w-[280px] p-2 btn btn-dark">
          Back to settings
        </RouterLink>
      </div>
    </div>

    <Modal :show="isOpen" @close="closeModal">
      <template #modal-content>
        <div class="flex flex-col items-center gap-4">
          <h2 class="text-lg font-semibold text-error">Confirm Profile Deletion</h2>
          <p class="text-center text-base">
            This action will permanently delete your profile and all associated data.
          </p>

          <div class="w-full flex flex-col justify-center items-center gap-2">
            <input
              class="border border-black rounded-lg p-2 w-full text-center focus:outline-none focus:ring-0 focus:border-black"
              type="text"
              name="confirmationCode"
              id="confirmationCode"
              placeholder="Type 'delete' to confirm"
              v-model="profileDeleteFactory.confirmationCode"
            />
            <p
              v-if="profileDeleteFactory.confirmationCodeError"
              class="w-full text-error text-center font-bold"
            >
              {{ profileDeleteFactory.confirmationCodeError }}
            </p>
          </div>

          <Loader :loading="storeCore.loaders.delete" />

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
              @click="deleteProfileAccount"
              class="!w-full sm:!w-[280px] p-2 btn btn-danger mt-4"
              :class="{ disabled: isDeleteDisabled || storeCore.btnDisablers.deleteBtn }"
            >
              Delete
            </button>
          </div>
        </div>
      </template>
    </Modal>
  </section>
</template>

<script setup>
import { useProfile } from '@/modules/apps/settings/profile/composables/useProfile';
import { coreStore } from '@/modules/shared/common/stores/core/coreStore';
import Modal from '@/modules/shared/common/components/ui/Modal.vue';
import Loader from '@/modules/shared/common/components/ui/Loader.vue';

const storeCore = coreStore();

const {
  profileDeleteFactory,
  isOpen,
  isDeleteDisabled,
  openModal,
  closeModal,
  deleteProfileAccount,
} = useProfile();
</script>

<style scoped></style>
