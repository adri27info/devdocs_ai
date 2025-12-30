import { createProfileDeleteFactory } from '@/modules/apps/settings/profile/factories/profileFactory';

export function useProfileReset() {
  const resetProfileDeleteFactory = profileDeleteFactory => {
    Object.assign(profileDeleteFactory, createProfileDeleteFactory());
  };

  return { resetProfileDeleteFactory };
}
