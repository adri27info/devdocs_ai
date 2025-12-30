import { PLANS } from '@/modules/shared/common/constants/utils/plans';
import { STEPS } from '@/modules/shared/common/constants/apps/home/steps';

export function useHome() {
  const getFeatureClasses = feature => {
    return {
      icon: feature.type === 'success' ? 'h-4 w-4 text-success' : 'h-4 w-4 text-neutral',
      text:
        feature.type === 'success'
          ? 'text-base font-semibold'
          : 'text-base font-semibold line-through text-neutral',
    };
  };

  return {
    plans: PLANS,
    steps: STEPS,

    getFeatureClasses,
  };
}
