import { createApp } from 'vue';
import { createPinia } from 'pinia';
import piniaPersistedState from 'pinia-plugin-persistedstate';
import '@/modules/shared/common/assets/css/main.css';
import router from '@/modules/router';
import App from '@/App.vue';

const pinia = createPinia();
pinia.use(piniaPersistedState);

const app = createApp(App);
app.use(router);
app.use(pinia);
app.mount('#app');
