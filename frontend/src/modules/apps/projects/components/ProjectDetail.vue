<template>
  <section class="w-full p-3 sm:p-8">
    <div class="w-full mb-5 flex flex-col items-center justify-center gap-2">
      <div class="w-full p-5 rounded-2xl border-2 bg-white shadow-sm mb-5">
        <div class="w-full mb-8 flex flex-col items-center justify-center gap-2 text-center">
          <h1 class="text-xl font-semibold mb-2">Project</h1>
          <p class="text-base">Here's an overview of your project</p>
        </div>

        <div class="w-full flex flex-col lg:flex-row justify-center items-center gap-3">
          <MenuOptions
            :items="menuProjectItems"
            item-classes="general-custom-hover w-full lg:flex-1 flex flex-col justify-center items-center bg-gray-900 hover:bg-gray-700 text-white rounded-lg p-2 transition"
            type="button"
            buttonClasses="w-full flex flex-col items-center justify-center gap-2"
            icon-classes="h-6 w-6"
            @click="handleMenuClick"
          />
        </div>
      </div>

      <ProjectDetailDocument v-if="selectedMenuItem === 'Generate documentation'" :id="props.id" />
      <ProjectDetailData v-if="selectedMenuItem === 'Data'" :id="props.id" />
    </div>
  </section>
</template>

<script setup>
import { useProjectDetail } from '@/modules/apps/projects/composables/useProjectDetail';
import MenuOptions from '@/modules/shared/common/components/ui/MenuOptions.vue';
import ProjectDetailData from '@/modules/apps/projects/components/ProjectDetailData.vue';
import ProjectDetailDocument from '@/modules/apps/projects/components/ProjectDetailDocument.vue';

const props = defineProps({
  id: {
    type: String,
    required: true,
  },
});

const { menuProjectItems, selectedMenuItem, handleMenuClick } = useProjectDetail();
</script>

<style scoped></style>
