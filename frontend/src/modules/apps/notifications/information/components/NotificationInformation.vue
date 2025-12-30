<template>
  <section class="w-full p-3 sm:p-8">
    <Loader :loading="storeCore.loaders.notifications" />

    <div
      v-if="!storeCore.loaders.notifications"
      class="w-full flex flex-col items-center justify-center gap-3 text-center"
    >
      <div class="w-full mb-8 flex flex-col items-center justify-center gap-2 text-center">
        <div class="w-full mb-5 flex flex-col items-center justify-center gap-2 text-center">
          <h1 class="text-xl font-semibold mb-2">Information notifications</h1>
          <p class="text-base">
            {{
              storeNotification.notificationsFactory.list.length
                ? "Here's an overview of your information notifications"
                : 'Information notifications cannot be displayed'
            }}
          </p>
        </div>

        <div
          v-if="storeNotification.notificationsFactory.list.length"
          class="w-full flex flex-col items-center rounded-2xl border-2 gap-4"
        >
          <div
            v-for="notification in storeNotification.notificationsFactory.list"
            :key="notification.id"
            class="w-full flex flex-col items-center justify-center rounded-2xl p-2"
          >
            <div
              class="w-full flex flex-col xl:flex-row items-center justify-center xl:justify-around gap-2 rounded-2xl border-2 p-2 min-h-36"
            >
              <div class="w-full flex flex-col items-center xl:items-start justify-center gap-6">
                <div class="w-full flex flex-col xl:flex-row items-center justify-start gap-2">
                  <InformationCircleIcon class="h-6 w-6" />
                  <p class="text-base">
                    {{ notification.message_reason }}
                  </p>
                </div>

                <div
                  class="flex flex-col xl:flex-row items-center justify-center sm:justify-start gap-4"
                >
                  <SkeletonLoader
                    :src="notification.sender.attachment"
                    type="user"
                    wrapper-classes="w-10 h-10 rounded-full overflow-hidden object-cover flex-shrink-0"
                    alt="user attachment"
                  />
                  <div class="w-full flex flex-col items-center xl:items-start justify-center">
                    <p class="text-base font-semibold">
                      {{ notification.sender.first_name }} {{ notification.sender.last_name }}
                    </p>
                    <p class="text-base">({{ notification.sender.email }})</p>
                  </div>
                </div>
              </div>
              <div>
                <button
                  type="button"
                  class="p-2 btn btn-danger mt-4"
                  @click="openModal(notification.id)"
                >
                  Delete Notification
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <RouterLink :to="{ name: 'notifications' }" class="btn btn-dark">
        Back to notifications
      </RouterLink>
    </div>

    <Modal :show="isOpen" @close="closeModal">
      <template #modal-content>
        <div class="w-full flex flex-col items-center justify-center gap-4">
          <h2 class="text-lg font-semibold text-error">Confirm Notification Deletion</h2>
          <p class="text-center text-base">
            Are you sure you want to permanently delete this notification?
          </p>

          <Loader :loading="storeCore.loaders.notificationDelete" />

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
              @click="deleteNotification(selectedNotificationId)"
              class="!w-full sm:!w-[280px] p-2 btn btn-danger mt-4"
              :class="{ disabled: storeCore.btnDisablers.notificationDeleteBtn }"
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
import { InformationCircleIcon } from '@heroicons/vue/24/outline';
import { useNotificationFetcher } from '@/modules/apps/notifications/composables/useNotificationFetcher';
import { notificationStore } from '@/modules/apps/notifications/stores/notificationStore';
import { coreStore } from '@/modules/shared/common/stores/core/coreStore';
import Loader from '@/modules/shared/common/components/ui/Loader.vue';
import SkeletonLoader from '@/modules/shared/common/components/ui/SkeletonLoader.vue';
import Modal from '@/modules/shared/common/components/ui/Modal.vue';

const storeNotification = notificationStore();
const storeCore = coreStore();

const { isOpen, selectedNotificationId, deleteNotification, openModal, closeModal } =
  useNotificationFetcher('INFORMATION');
</script>

<style scoped></style>
