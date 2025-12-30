<template>
  <div class="w-full flex flex-col justify-center items-center text-center gap-5">
    <div class="w-full mt-10">
      <h1 class="text-3xl font-bold mb-5">Assistance</h1>
      <p class="text-lg">Enter your email and select the issue</p>
    </div>

    <form
      method="post"
      @submit.prevent="handleAssistance"
      class="w-full sm:w-[480px] flex flex-col justify-center items-center gap-7 rounded sm:border-1 p-2 mb-10"
    >
      <div class="w-full flex flex-col justify-center items-center gap-2">
        <div class="w-full flex flex-row justify-center items-center gap-1">
          <label class="font-bold" for="email">Email</label>
          <span class="text-error">*</span>
        </div>
        <input
          class="w-full p-2 border-1 rounded text-center"
          type="text"
          name="email"
          id="email"
          placeholder="Enter your email"
          v-model="assistanceFactory.email"
        />
        <p v-if="assistanceFactory.emailError" class="w-full text-error font-bold">
          {{ assistanceFactory.emailError }}
        </p>
      </div>

      <div class="w-full flex flex-col justify-center items-center gap-4">
        <div class="w-full flex flex-col gap-2">
          <div class="w-full flex flex-row items-center justify-center gap-1">
            <label class="font-bold" for="notificationType">Notification type</label>
            <span class="text-error mt-1">*</span>
          </div>

          <Select
            v-model="selectedOption"
            :options="options"
            :error="assistanceFactory.typeError"
            @update:error="assistanceFactory.typeError = $event"
            placeholder="Select an option"
          />

          <div v-if="showOtherReason(selectedOption)" class="w-full flex flex-col gap-2 mt-2">
            <label class="font-bold" for="messageReason">Describe your issue</label>
            <textarea
              id="messageReason"
              placeholder="Explain your issue..."
              class="border rounded w-full p-2 text-center resize-none min-h-16"
              v-model="assistanceFactory.messageReason"
            ></textarea>
            <p v-if="assistanceFactory.messageReasonError" class="w-full text-error font-bold">
              {{ assistanceFactory.messageReasonError }}
            </p>
          </div>
        </div>
      </div>

      <div class="w-full flex flex-col justify-center items-center gap-2">
        <RouterLink :to="{ name: 'login' }" class="font-bold">
          Issue solved? Go sign in
        </RouterLink>
        <Loader :loading="storeCore.loaders.assistance" />
      </div>

      <div class="w-full flex flex-col justify-center items-center gap-4">
        <button
          type="submit"
          class="!w-[280px] btn btn-dark"
          :class="{ disabled: storeCore.btnDisablers.assistanceBtn }"
        >
          Request assistance
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { useAssistance } from '@/modules/apps/auth/assistance/composables/useAssistance';
import { useAssistanceValidations } from '@/modules/apps/auth/assistance/composables/useAssistanceValidations';
import { coreStore } from '@/modules/shared/common/stores/core/coreStore';
import Loader from '@/modules/shared/common/components/ui/Loader.vue';
import Select from '@/modules/shared/common/components/ui/Select.vue';

const storeCore = coreStore();

const { showOtherReason } = useAssistanceValidations();

const {
  options,
  selectedOption,
  assistanceFactory,

  handleAssistance,
} = useAssistance();
</script>

<style scoped></style>
