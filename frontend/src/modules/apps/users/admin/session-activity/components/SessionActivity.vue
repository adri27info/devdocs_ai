<template>
  <section class="w-full p-8">
    <Loader :loading="storeCore.loaders.sessionActivity" />

    <div v-if="!storeCore.loaders.sessionActivity" class="w-full">
      <div class="w-full mb-8 flex flex-col items-center justify-center gap-2 text-center">
        <h1 class="text-xl font-semibold mb-2">Session Activity</h1>
        <p class="text-base">
          {{
            storeUser.userSessionActivityFactory.list.length
              ? "Here's an overview of the session activity"
              : 'Session activity cannot be displayed'
          }}
        </p>
      </div>

      <div v-if="storeUser.userSessionActivityFactory.list.length" class="w-full text-center">
        <div class="w-full flex justify-center items-start">
          <div class="w-full p-5 rounded-2xl border-2 bg-white shadow-sm">
            <div class="hidden xl:block overflow-x-auto">
              <table class="border-separate border-spacing-0 border border-gray-400 w-full mb-5">
                <thead>
                  <tr class="bg-gray-900 text-white">
                    <th class="py-3 px-4 font-semibold text-sm border border-gray-400 text-center">
                      User
                    </th>
                    <th class="py-3 px-4 font-semibold text-sm border border-gray-400 text-center">
                      Email
                    </th>
                    <th class="py-3 px-4 font-semibold text-sm border border-gray-400 text-center">
                      Role
                    </th>
                    <th class="py-3 px-4 font-semibold text-sm border border-gray-400 text-center">
                      Session Start
                    </th>
                    <th class="py-3 px-4 font-semibold text-sm border border-gray-400 text-center">
                      Session End
                    </th>
                    <th class="py-3 px-4 font-semibold text-sm border border-gray-400 text-center">
                      Revoked At
                    </th>
                  </tr>
                </thead>

                <tbody>
                  <tr
                    v-for="(activity, index) in storeUser.userSessionActivityFactory.list.filter(
                      a => a.user,
                    )"
                    :key="index"
                  >
                    <td class="py-4 px-4 border border-gray-400 text-center">
                      <div class="flex flex-col items-center">
                        <SkeletonLoader
                          :src="activity.user.attachment"
                          type="user"
                          wrapper-classes="w-12 h-12 rounded-full overflow-hidden cursor-pointer"
                          alt="user attachment"
                        />
                      </div>
                    </td>

                    <td class="py-4 px-4 border border-gray-400 text-center">
                      {{ activity.user.email }}
                    </td>

                    <td class="py-4 px-4 border border-gray-400 text-center capitalize">
                      {{ activity.user.role.name }}
                    </td>

                    <td class="py-4 px-4 border border-gray-400 text-center">
                      {{ formatDate(activity.created_at) }}
                    </td>

                    <td class="py-4 px-4 border border-gray-400 text-center">
                      {{ formatDate(activity.expires_at) }}
                    </td>

                    <td class="py-4 px-4 border border-gray-400 text-center">
                      {{ formatDate(activity.blacklisted_at) }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div class="xl:hidden flex flex-col text-center gap-4">
              <div
                v-for="(activity, index) in storeUser.userSessionActivityFactory.list.filter(
                  a => a.user,
                )"
                :key="index"
                class="flex flex-col items-center border rounded-lg p-4 bg-gray-50 gap-3"
              >
                <div class="mt-2 w-12 h-12 rounded-full overflow-hidden">
                  <SkeletonLoader
                    :src="activity.user.attachment"
                    type="user"
                    wrapper-classes="w-12 h-12 rounded-full overflow-hidden cursor-pointer"
                    alt="user attachment"
                  />
                </div>

                <div class="flex flex-col gap-1 text-center w-full">
                  <span class="text-sm text-gray-700 capitalize">
                    <strong>Role:</strong> {{ activity.user.role.name }}
                  </span>
                  <span class="text-sm text-gray-700">
                    <strong>Email:</strong> {{ activity.user.email }}
                  </span>
                  <span class="text-sm text-gray-700">
                    <strong>Session Start:</strong> {{ formatDate(activity.created_at) }}
                  </span>
                  <span class="text-sm text-gray-700">
                    <strong>Session End:</strong> {{ formatDate(activity.expires_at) }}
                  </span>
                  <span class="text-sm text-gray-700">
                    <strong>Revoked At:</strong> {{ formatDate(activity.blacklisted_at) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useSessionActivity } from '@/modules/apps/users/admin/session-activity/composables/useSessionActivity';
import { coreStore } from '@/modules/shared/common/stores/core/coreStore';
import { userStore } from '@/modules/apps/users/stores/userStore';
import Loader from '@/modules/shared/common/components/ui/Loader.vue';
import SkeletonLoader from '@/modules/shared/common/components/ui/SkeletonLoader.vue';

const storeCore = coreStore();
const storeUser = userStore();

const { formatDate } = useSessionActivity();
</script>

<style scoped></style>
