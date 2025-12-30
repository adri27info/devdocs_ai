<template>
  <div class="w-full flex flex-col justify-center items-center text-center gap-5">
    <div class="w-full mt-10">
      <h1 class="text-3xl font-bold mb-5">Create an account</h1>
      <p class="text-lg">Enter your details to get started</p>
    </div>

    <form
      method="post"
      enctype="multipart/form-data"
      @submit.prevent="handleRegister"
      class="w-full sm:w-[480px] flex flex-col justify-center items-center gap-7 rounded sm:border-1 p-2 mb-10"
    >
      <div class="w-full flex flex-col justify-center items-center gap-2">
        <div class="w-full flex flex-row justify-center items-center gap-1">
          <label class="font-bold" for="first-name">First name</label>
          <span class="text-error mt-1">*</span>
        </div>
        <input
          class="w-full p-2 border-1 rounded text-center"
          type="text"
          name="first-name"
          id="first-name"
          placeholder="Enter your first name"
          v-model="registerFactory.firstName"
        />
        <p v-if="registerFactory.firstNameError" class="w-full text-error font-bold">
          {{ registerFactory.firstNameError }}
        </p>
      </div>

      <div class="w-full flex flex-col justify-center items-center gap-2">
        <div class="w-full flex flex-row justify-center items-center gap-1">
          <label class="font-bold" for="last-name">Last name</label>
          <span class="text-error mt-1">*</span>
        </div>
        <input
          class="w-full p-2 border-1 rounded text-center"
          type="text"
          name="last-name"
          id="last-name"
          placeholder="Enter your last name"
          v-model="registerFactory.lastName"
        />
        <p v-if="registerFactory.lastNameError" class="w-full text-error font-bold">
          {{ registerFactory.lastNameError }}
        </p>
      </div>

      <div class="w-full flex flex-col justify-center items-center gap-2">
        <div class="w-full flex flex-row justify-center items-center gap-1">
          <label class="font-bold" for="email">Email</label>
          <span class="text-error mt-1">*</span>
        </div>
        <input
          class="w-full p-2 border-1 rounded text-center"
          type="text"
          name="email"
          id="email"
          placeholder="Enter your email"
          v-model="registerFactory.email"
        />
        <p v-if="registerFactory.emailError" class="w-full text-error font-bold">
          {{ registerFactory.emailError }}
        </p>
      </div>

      <div class="w-full flex flex-col justify-center items-center gap-2">
        <div class="w-full flex flex-row justify-center items-center gap-1">
          <label class="font-bold" for="password">Password</label>
          <span class="text-error mt-1">*</span>
        </div>
        <div class="flex items-center border rounded w-full p-2 relative">
          <input
            class="flex-1 text-center outline-none"
            placeholder="Enter your password"
            v-model="registerFactory.password"
            :type="passwordProps.type"
          />

          <button type="button" class="absolute right-2" @click="togglePasswordVisibility">
            <component :is="passwordProps.icon" class="h-5 w-5" />
          </button>
        </div>
        <p v-if="registerFactory.passwordError" class="w-full text-error font-bold">
          {{ registerFactory.passwordError }}
        </p>
      </div>

      <div class="w-full flex flex-col justify-center items-center gap-2">
        <div class="w-full flex flex-row justify-center items-center gap-1">
          <label class="font-bold" for="attachment">Attachment</label>
        </div>

        <div class="w-full flex flex-col justify-between items-center gap-2">
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
              Choose File
            </label>
            <span class="w-full p-2">
              {{ truncatedAttachmentName }}
            </span>
          </div>
          <button type="button" @click="resetAttachment">
            <ArrowPathIcon class="h-5 w-5 text-black" />
          </button>
        </div>

        <p v-if="registerFactory.attachmentError" class="w-full text-error font-bold">
          {{ registerFactory.attachmentError }}
        </p>
      </div>

      <div class="w-full">
        <RouterLink :to="{ name: 'activate-account' }" class="font-bold">
          Got your code? Activate your account
        </RouterLink>
        <Loader :loading="storeCore.loaders.register" />
      </div>

      <div class="w-full flex flex-col justify-center items-center gap-4">
        <button
          type="submit"
          class="!w-[280px] btn btn-dark"
          :class="{ disabled: storeCore.btnDisablers.registerBtn }"
        >
          Create account
        </button>
        <RouterLink :to="{ name: 'login' }" class="font-bold">
          Already have an account? Sign in
        </RouterLink>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ArrowPathIcon } from '@heroicons/vue/24/outline';
import { useRegister } from '@/modules/apps/auth/register/composables/useRegister';
import { coreStore } from '@/modules/shared/common/stores/core/coreStore';
import Loader from '@/modules/shared/common/components/ui/Loader.vue';

const storeCore = coreStore();

const {
  registerFactory,
  attachmentInputRef,
  passwordProps,
  truncatedAttachmentName,

  handleRegister,
  togglePasswordVisibility,
  setAttachment,
  resetAttachment,
} = useRegister();
</script>

<style scoped></style>
