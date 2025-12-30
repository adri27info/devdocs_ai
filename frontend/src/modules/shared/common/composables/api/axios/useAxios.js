import axios from 'axios';
import { useEnvironment } from '@/modules/shared/common/composables/utils/ui/useEnvironment';
import { useCookie } from '@/modules/shared/common/composables/cookies/useCookie';

export function useAxios() {
  const { apiBackend } = useEnvironment();
  const { getCookie } = useCookie();

  const csrfMethods = ['post', 'put', 'patch', 'delete'];

  const instance = axios.create({
    baseURL: apiBackend,
    withCredentials: true,
  });

  instance.interceptors.request.use(config => {
    const method = config.method?.toLowerCase();

    if (csrfMethods.includes(method)) {
      const csrfToken = getCookie('csrftoken');
      if (csrfToken) {
        config.headers['X-CSRFToken'] = csrfToken;
      }
    }
    return config;
  });

  return instance;
}
