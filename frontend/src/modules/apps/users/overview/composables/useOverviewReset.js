import { createOverviewFactory } from '@/modules/apps/users/overview/factories/overviewFactory';

export function useOverviewReset() {
  const resetOverviewFactory = overviewFactory => {
    Object.assign(overviewFactory, createOverviewFactory());
  };

  return { resetOverviewFactory };
}
