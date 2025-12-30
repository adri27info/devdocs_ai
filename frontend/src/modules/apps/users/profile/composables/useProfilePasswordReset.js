import { createProfilePasswordFactory } from '@/modules/apps/users/profile/factories/profilePasswordFactory';

export function useProfilePasswordReset() {
  const resetProfilePasswordFactory = profilePasswordFactory => {
    Object.assign(profilePasswordFactory, createProfilePasswordFactory());
  };

  return { resetProfilePasswordFactory };
}
