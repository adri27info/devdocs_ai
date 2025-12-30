<template>
  <div class="w-full">
    <section
      class="w-full p-2.5 flex flex-col justify-between items-center text-center gap-10 my-15"
    >
      <h1 class="text-3xl font-bold">AI-Powered Technical Documentation</h1>
      <p class="text-lg max-w-3xl">
        Share your code with our AI-powered platform and instantly receive clean, accurate, and
        beautifully structured technical documentation. It’s the fastest way to keep your projects
        documented, understandable, and ready to share.
      </p>
      <RouterLink
        :to="{ name: 'login' }"
        class="btn btn-dark flex flex-row items-center justify-center gap-2"
      >
        <span>Get started</span>
        <ArrowRightIcon class="h-4.5 w-4.5 mt-1 text-white" />
      </RouterLink>
    </section>

    <hr class="border-1" />

    <section
      class="w-full p-2.5 flex flex-col justify-between items-center text-center gap-10 my-15"
    >
      <div>
        <h1 class="text-3xl font-bold mb-8">Simple and Transparent Plans. Choose it and enjoy.</h1>
        <p class="text-lg">
          Start for free and upgrade whenever you need more tools for your team.
        </p>
        <p class="text-xl font-bold">A single payment forever</p>
      </div>

      <div
        class="w-full flex flex-col md:flex-row justify-center items-center md:items-stretch gap-10 md:gap-20"
      >
        <div
          class="border-2 rounded-2xl w-full sm:w-120 flex flex-col justify-between items-center py-15 sm:py-8"
          v-for="(plan, planIndex) in plans"
          :key="planIndex"
        >
          <div class="mb-7 w-full">
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

          <div
            v-if="plan.popular"
            class="text-white bg-cyan-600 hover:bg-cyan-700 rounded-2xl p-3 flex flex-row justify-center items-center gap-2 mb-5"
          >
            <component :is="plan.badge.icon" class="h-4 w-4" />
            <p>{{ plan.badge.text }}</p>
          </div>

          <RouterLink
            :to="{ name: 'login' }"
            class="btn btn-dark flex flex-row items-center justify-center gap-2"
          >
            <span>{{ plan.btnText }}</span>
            <ArrowRightIcon class="h-4.5 w-4.5 mt-1 text-white" />
          </RouterLink>
        </div>
      </div>
    </section>

    <hr class="border-1" />

    <section
      class="w-full p-2.5 flex flex-col justify-between items-center text-center gap-10 my-15"
    >
      <div class="flex flex-col justify-center items-center gap-10 w-full">
        <h1 class="text-3xl font-bold">How it works the system.</h1>
        <p class="text-lg max-w-3xl">
          Discover all the tools that DevDocs AI puts at your disposal to create exceptional
          technical documentation.
        </p>
        <div
          class="w-full flex flex-col lg:flex-row justify-between items-center lg:items-stretch gap-3"
        >
          <div
            v-for="(step, index) in steps"
            :key="index"
            class="w-full lg:w-100 rounded p-10 border-2 shadow-2xs flex flex-col justify-center items-center gap-4"
          >
            <component :is="step.icon" class="h-8 w-8 text-black" />
            <h2 class="text-xl font-bold">{{ step.title }}</h2>
            <p class="text-base">{{ step.description }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ArrowRightIcon } from '@heroicons/vue/24/outline';
import { useHome } from '@/modules/apps/home/composables/useHome';

const { plans, steps, getFeatureClasses } = useHome();
</script>

<style scoped></style>
