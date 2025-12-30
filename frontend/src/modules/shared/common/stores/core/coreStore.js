import { reactive } from 'vue';
import { defineStore } from 'pinia';
import {
  createLoadersFactory,
  createRedirectsFactory,
  createBtnDisablerFactory,
} from '@/modules/shared/common/factories/core/coreFactory';

export const coreStore = defineStore('coreStore', () => {
  const loaders = reactive(createLoadersFactory());
  const redirects = reactive(createRedirectsFactory());
  const btnDisablers = reactive(createBtnDisablerFactory());

  return {
    loaders,
    redirects,
    btnDisablers,
  };
});
