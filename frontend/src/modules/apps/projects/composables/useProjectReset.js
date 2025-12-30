import { createBasicProfileFactory } from '@/modules/apps/projects/factories/projectBasicFactory';

export function useProjectReset() {
  const resetBasicProfileFactory = basicProfileCreateFactory => {
    Object.assign(basicProfileCreateFactory, createBasicProfileFactory());
  };

  return { resetBasicProfileFactory };
}
