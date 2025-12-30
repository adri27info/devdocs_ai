import { watch } from 'vue';
import { useRouter } from 'vue-router';
import { useDelay } from '@/modules/shared/common/composables/utils/useDelay';
import { useObjectResetter } from '@/modules/shared/common/composables/utils/useObjectResetter';
import { authStore } from '@/modules/apps/auth/stores/authStore';

export function useCore() {
  const storeAuth = authStore();
  const router = useRouter();

  const { resetObjects } = useObjectResetter();
  const { delay } = useDelay();

  watch(
    () => storeAuth.isAuthenticated,
    async isAuth => {
      if (!isAuth) {
        await delay();
        router.push({ name: 'login' });
        resetObjects();
      }
    },
  );
}
