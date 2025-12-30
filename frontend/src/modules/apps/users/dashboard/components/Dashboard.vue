<template>
  <section class="w-full p-8">
    <Loader :loading="storeCore.loaders.dashboard" />

    <div v-if="!storeCore.loaders.dashboard" class="w-full">
      <div class="w-full mb-8 flex flex-col items-center justify-center gap-2 text-center">
        <h1 class="text-xl font-semibold mb-2">Welcome back! 👋</h1>
        <p class="text-base">
          {{
            storeUser.userStatsFactory.plan_type.id
              ? "Here's an overview of your account and usage"
              : 'Projects cannot be displayed'
          }}
        </p>
      </div>

      <div v-if="storeUser.userStatsFactory.plan_type.id" class="w-full">
        <div
          class="w-full flex flex-col items-center justify-center gap-3 p-2 rounded-2xl border-2 mb-8"
        >
          <div class="w-full flex flex-col items-center justify-center p-2">
            <div class="w-full flex flex-row items-center justify-between">
              <div class="flex flex-row items-center justify-between gap-3">
                <BookOpenIcon class="h-4 w-4 mt-0.5" />
                <p>Plan</p>
              </div>
              <p>{{ storeUser.userStatsFactory.plan_type.name }}</p>
            </div>

            <div class="w-full bg-gray-300 h-3 rounded-full mt-2">
              <div class="bg-gray-900 h-3 rounded-full" :style="{ width: planUsageWidth }"></div>
            </div>
          </div>

          <div class="w-full flex flex-col items-center justify-center p-2">
            <div class="w-full flex flex-row items-center justify-between">
              <div class="flex flex-row items-center justify-between gap-3">
                <FolderIcon class="h-4 w-4" />
                <p>Projects created</p>
              </div>
              <p>
                {{ storeUser.userStatsFactory.owned_projects.length }}/{{
                  storeUser.userStatsFactory.plan_type.max_projects
                }}
              </p>
            </div>

            <div class="w-full bg-gray-300 h-3 rounded-full mt-2">
              <div
                class="bg-gray-900 h-3 rounded-full"
                :style="{
                  width: `${(storeUser.userStatsFactory.owned_projects.length / storeUser.userStatsFactory.plan_type.max_projects) * 100}%`,
                }"
              ></div>
            </div>
          </div>

          <div class="w-full flex flex-col items-center justify-center p-2">
            <div class="w-full flex flex-row items-center justify-between">
              <div class="flex flex-row items-center justify-between gap-3">
                <FolderIcon class="h-4 w-4" />
                <p>Projects you're involved in</p>
              </div>
              <p>
                {{ storeUser.userStatsFactory.involved_projects.length }}
              </p>
            </div>

            <div class="w-full bg-gray-300 h-3 rounded-full mt-2">
              <div
                class="bg-gray-900 h-3 rounded-full"
                :style="{
                  width: `${(storeUser.userStatsFactory.involved_projects.length / storeUser.userStatsFactory.involved_projects.length) * 100}%`,
                }"
              ></div>
            </div>
          </div>
        </div>

        <div class="w-full mb-8 flex flex-col items-center justify-center gap-2 text-center">
          <h1 class="text-xl font-semibold mb-2">Your subscription</h1>
          <p class="text-base whitespace-pre-line">{{ subscriptionText }}</p>
        </div>

        <div
          v-if="manuallyClosed && storeCore.loaders.paymentPollingStatus"
          class="w-full flex items-center justify-center mb-3"
        >
          <button type="button" class="mb-3 btn btn-dark" @click="openModal">
            Check payment status
          </button>
        </div>

        <div class="w-full flex flex-col xl:flex-row items-center justify-around gap-3 p-2 mb-8">
          <div
            class="border-2 rounded-2xl w-full sm:max-w-md flex flex-col justify-between items-center py-15 sm:py-8 min-h-220"
            v-for="(plan, planIndex) in plans"
            :key="planIndex"
            :class="planBorderClass(plan.name)"
          >
            <div
              v-if="isCurrentPlan(plan.name)"
              class="bg-cyan-600 rounded-2xl p-2 text-white mb-8 w-36 text-center"
            >
              <p>Current plan</p>
            </div>

            <div class="mb-7 w-full text-center">
              <h2 class="text-2xl font-bold mb-2">{{ plan.name }}</h2>
              <p class="text-gray-600 font-semibold mb-2">{{ plan.description }}</p>
              <span class="text-3xl font-bold">{{ plan.price }}</span>
            </div>

            <div
              class="flex flex-col justify-center items-center gap-3 mb-10 w-full"
              v-for="(feature, featureIndex) in plan.features"
              :key="featureIndex"
            >
              <div
                class="w-full flex flex-col sm:flex-row items-center justify-center gap-2 text-center"
              >
                <component :is="feature.icon" :class="getFeatureClasses(feature).icon" />
                <span :class="getFeatureClasses(feature).text">{{ feature.text }}</span>
              </div>
            </div>
          </div>
        </div>

        <div v-if="isFreePlan" class="flex flex-row items-center justify-center">
          <button type="button" class="mb-3 lg:mb-0 btn btn-dark" @click="upgradePlan">
            Upgrade to premium
          </button>
        </div>
        <div v-else class="flex flex-row items-center justify-center">
          <RouterLink :to="{ name: 'settings-payment' }" class="btn btn-dark">
            Watch payment invoice
          </RouterLink>
        </div>
      </div>
    </div>

    <Modal :show="isOpen" @close="closeModal">
      <template #modal-content>
        <div class="w-full flex flex-col items-center justify-center gap-4">
          <h1 class="text-xl font-semibold mb-2">Processing payment</h1>
          <p class="text-base text-center mb-2">
            Please wait a moment while we confirm your subscription.
          </p>
          <Loader :loading="storeCore.loaders.paymentPollingStatus" />
        </div>
      </template>
    </Modal>
  </section>
</template>

<script setup>
import { BookOpenIcon, FolderIcon } from '@heroicons/vue/24/outline';
import { useHome } from '@/modules/apps/home/composables/useHome';
import { useDashboard } from '@/modules/apps/users/dashboard/composables/useDashboard';
import { userStore } from '@/modules/apps/users/stores/userStore';
import { coreStore } from '@/modules/shared/common/stores/core/coreStore';
import Modal from '@/modules/shared/common/components/ui/Modal.vue';
import Loader from '@/modules/shared/common/components/ui/Loader.vue';

const storeUser = userStore();
const storeCore = coreStore();

const { plans, getFeatureClasses } = useHome();

const {
  subscriptionText,
  isFreePlan,
  planUsageWidth,
  isOpen,
  manuallyClosed,
  openModal,
  closeModal,
  isCurrentPlan,
  planBorderClass,
  upgradePlan,
} = useDashboard();
</script>

<style scoped></style>
