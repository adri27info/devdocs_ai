<template>
  <div
    v-for="item in items"
    :key="item.name"
    :class="[itemClasses, item.activeInAside || item.activeInGeneral ? 'active' : '']"
  >
    <RouterLink v-if="type === 'link'" :to="{ name: item.routeName }" :class="routerLinkClasses">
      <template v-if="getTemplateOrder() === 'default'">
        <span :class="spanClasses">{{ item.name }}</span>
        <hr v-if="showDivisor()" class="w-full bg-white m-1" />
        <component :is="item.icon" :class="iconClasses" />
      </template>

      <template v-else>
        <component :is="item.icon" :class="iconClasses" />
        <hr v-if="showDivisor()" class="w-full bg-white m-1" />
        <span :class="spanClasses">{{ item.name }}</span>
      </template>
    </RouterLink>

    <button v-else type="button" :class="buttonClasses" @click="$emit('click', item)">
      <span :class="spanClasses">{{ item.name }}</span>
      <hr v-if="showDivisor()" class="w-full bg-white m-1" />
      <component :is="item.icon" :class="iconClasses" />
    </button>
  </div>
</template>

<script setup>
import { useMenuOption } from '@/modules/shared/common/composables/utils/ui/useMenuOption';

const props = defineProps({
  items: { type: Array, required: true },
  itemClasses: { type: String, default: '' },
  routerLinkClasses: { type: String, default: '' },
  buttonClasses: { type: String, default: '' },
  iconClasses: { type: String, default: '' },
  spanClasses: { type: String, default: '' },
  type: { type: String, default: 'link' },
  order: { type: String, default: 'default' },
  divisor: { type: Boolean, default: true },
});

defineEmits(['click']);

const { getTemplateOrder, showDivisor } = useMenuOption(props.order, props.divisor);
</script>
