<template>
  <section class="w-full p-4 sm:p-8">
    <Loader :loading="storeCore.loaders.profileUserInit" />

    <div v-if="!storeCore.loaders.profileUserInit" class="w-full">
      <div class="w-full mb-5 flex flex-col items-center justify-center gap-2">
        <h1 class="text-xl font-semibold mb-2">Edit profile</h1>
        <p class="text-base">
          {{
            storeUser.userFactory.id
              ? 'Update your personal information'
              : 'User data cannot be displayed'
          }}
        </p>
      </div>

      <div v-if="storeUser.userFactory.id" class="w-full">
        <div class="w-full rounded-2xl p-3 flex flex-col items-center justify-center gap-3 mb-10">
          <form
            method="post"
            enctype="multipart/form-data"
            @submit.prevent="handleProfile"
            class="w-full flex flex-col justify-center items-center gap-5 rounded-2xl border-2 p-3"
          >
            <div class="w-full flex flex-col justify-between items-center gap-2">
              <SkeletonLoader
                :src="avatarSrc"
                type="user"
                wrapper-classes="w-36 h-36 rounded-full overflow-hidden cursor-pointer object-cover mb-3"
                alt="user profile attachment"
              />

              <input
                hidden
                type="file"
                name="attachment"
                id="attachment"
                ref="attachmentInputRef"
                @change="setAttachment"
              />
              <div
                class="w-full p-2 border-1 flex flex-col sm:flex-row justify-between items-center gap-2"
              >
                <label for="attachment" class="!w-full btn btn-neutral cursor-pointer">
                  Change Foto
                </label>
                <span class="w-full p-2 text-center">
                  {{ truncatedAttachmentName }}
                </span>
              </div>
              <button type="button" @click="resetAttachment">
                <ArrowPathIcon class="h-5 w-5 text-black" />
              </button>

              <p
                v-if="profileFactory.attachmentError"
                class="w-full text-error font-bold text-center"
              >
                {{ profileFactory.attachmentError }}
              </p>
            </div>

            <div class="w-full flex flex-col md:flex-row justify-between items-center gap-4">
              <div
                class="flex flex-col items-center justify-center gap-2 w-full md:flex-1 text-center"
              >
                <label for="first-name" class="font-semibold"> Firstname </label>
                <input
                  type="text"
                  name="first-name"
                  id="first-name"
                  class="w-full p-2 border-1 rounded text-center"
                  placeholder="Enter your first name"
                  v-model="profileFactory.firstName"
                />
                <p v-if="profileFactory.firstNameError" class="w-full text-error font-bold">
                  {{ profileFactory.firstNameError }}
                </p>
              </div>

              <div
                class="flex flex-col items-center justify-center gap-2 w-full md:flex-1 text-center"
              >
                <label for="last-name" class="font-semibold"> Lastname </label>
                <input
                  type="text"
                  name="last-name"
                  id="last-name"
                  class="w-full p-2 border-1 rounded text-center"
                  placeholder="Enter your last name"
                  v-model="profileFactory.lastName"
                />
                <p v-if="profileFactory.lastNameError" class="w-full text-error font-bold">
                  {{ profileFactory.lastNameError }}
                </p>
              </div>
            </div>

            <div class="w-full flex flex-col justify-center items-center gap-6">
              <Loader :loading="storeCore.loaders.profileUser" />
              <button
                type="submit"
                class="w-full sm:!w-[380px] btn btn-dark mt-2"
                :class="{ disabled: storeCore.btnDisablers.profileUserBtn }"
              >
                Update profile
              </button>
            </div>
          </form>
        </div>

        <div class="w-full mb-5 flex flex-col items-center justify-center gap-2">
          <p class="text-base">Update your password</p>
        </div>

        <div
          class="bg-white w-full rounded-2xl p-3 flex flex-col items-center justify-center gap-3"
        >
          <form
            method="post"
            @submit.prevent="handleProfilePassword"
            class="w-full flex flex-col justify-center items-center gap-5 rounded-2xl border-2 p-3"
          >
            <div class="w-full flex flex-col justify-center items-center gap-2">
              <div class="w-full flex flex-row justify-center items-center gap-1">
                <label class="font-bold" for="current-password">Current password</label>
                <span class="text-error mt-1">*</span>
              </div>
              <div class="flex items-center border rounded w-full p-2 relative">
                <input
                  class="flex-1 text-center outline-none py-2"
                  id="current-password"
                  placeholder="Enter your current password"
                  v-model="profilePasswordFactory.currentPassword"
                  :type="currentPasswordProps.type"
                />
                <button
                  type="button"
                  class="absolute right-2"
                  @click="toggleCurrentPasswordVisibility"
                >
                  <component :is="currentPasswordProps.icon" class="h-5 w-5 text-black" />
                </button>
              </div>
              <p
                v-if="profilePasswordFactory.currentPasswordError"
                class="w-full text-error font-bold text-center"
              >
                {{ profilePasswordFactory.currentPasswordError }}
              </p>
            </div>

            <div class="w-full flex flex-col justify-center items-center gap-2">
              <div class="w-full flex flex-row justify-center items-center gap-1">
                <label class="font-bold" for="new-password">New password</label>
                <span class="text-error mt-1">*</span>
              </div>
              <div class="flex items-center border rounded w-full p-2 relative">
                <input
                  class="flex-1 text-center outline-none py-2"
                  id="new-password"
                  placeholder="Enter your new password"
                  v-model="profilePasswordFactory.newPassword"
                  :type="newPasswordProps.type"
                />
                <button type="button" class="absolute right-2" @click="toggleNewPasswordVisibility">
                  <component :is="newPasswordProps.icon" class="h-5 w-5 text-black" />
                </button>
              </div>
              <p
                v-if="profilePasswordFactory.newPasswordError"
                class="w-full text-error font-bold text-center"
              >
                {{ profilePasswordFactory.newPasswordError }}
              </p>
            </div>

            <div class="w-full flex flex-col justify-center items-center gap-2">
              <div class="w-full flex flex-row justify-center items-center gap-1">
                <label class="font-bold" for="confirm-new-password">Confirm new password</label>
                <span class="text-error mt-1">*</span>
              </div>
              <div class="flex items-center border rounded w-full p-2 relative">
                <input
                  class="flex-1 text-center outline-none py-2"
                  id="confirm-new-password"
                  placeholder="Confirm your new password"
                  v-model="profilePasswordFactory.confirmNewPassword"
                  :type="confirmNewPasswordProps.type"
                />
                <button
                  type="button"
                  class="absolute right-2"
                  @click="toggleConfirmNewPasswordVisibility"
                >
                  <component
                    :is="confirmNewPasswordProps.icon"
                    class="h-5 w-5 text-black stroke-current"
                  />
                </button>
              </div>
              <p
                v-if="profilePasswordFactory.confirmNewPasswordError"
                class="w-full text-error font-bold text-center"
              >
                {{ profilePasswordFactory.confirmNewPasswordError }}
              </p>
              <p
                v-if="profilePasswordFactory.passwordMatchError"
                class="w-full text-error font-bold text-center"
              >
                {{ profilePasswordFactory.passwordMatchError }}
              </p>
            </div>

            <div class="w-full flex flex-col justify-center items-center gap-6">
              <Loader :loading="storeCore.loaders.profileUserPassword" />
              <button
                type="submit"
                class="w-full sm:!w-[380px] btn btn-dark mt-2"
                :class="{ disabled: storeCore.btnDisablers.profileUserPasswordBtn }"
              >
                Update password
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ArrowPathIcon } from '@heroicons/vue/24/outline';
import { coreStore } from '@/modules/shared/common/stores/core/coreStore';
import { userStore } from '@/modules/apps/users/stores/userStore';
import { useProfile } from '@/modules/apps/users/profile/composables/useProfile';
import { useProfilePassword } from '@/modules/apps/users/profile/composables/useProfilePassword';
import Loader from '@/modules/shared/common/components/ui/Loader.vue';
import SkeletonLoader from '@/modules/shared/common/components/ui/SkeletonLoader.vue';

const storeCore = coreStore();
const storeUser = userStore();

const {
  profileFactory,
  attachmentInputRef,
  truncatedAttachmentName,
  avatarSrc,
  handleProfile,
  setAttachment,
  resetAttachment,
} = useProfile();

const {
  profilePasswordFactory,
  currentPasswordProps,
  newPasswordProps,
  confirmNewPasswordProps,
  handleProfilePassword,
  toggleCurrentPasswordVisibility,
  toggleNewPasswordVisibility,
  toggleConfirmNewPasswordVisibility,
} = useProfilePassword();
</script>

<style scoped></style>
