import { useResponseHandler } from '@/modules/shared/common/composables/api/responses/useResponseHandler';
import { authStore } from '@/modules/apps/auth/stores/authStore';
import { coreStore } from '@/modules/shared/common/stores/core/coreStore';

export function useSessionLogout() {
  const storeAuth = authStore();
  const storeCore = coreStore();

  const { handleResult } = useResponseHandler();

  const handleLogout = async () => {
    resetLogoutValues({ logoutDisabledBtnValue: true, logoutRedirectValue: true });

    const result = await storeAuth.logoutUser();
    handleResult(result);
  };

  const resetLogoutValues = ({ logoutDisabledBtnValue, logoutRedirectValue }) => {
    storeCore.btnDisablers.logoutBtn = logoutDisabledBtnValue;
    storeCore.redirects.logout = logoutRedirectValue;
  };

  return {
    handleLogout,
    resetLogoutValues,
  };
}
