import { createAssistanceFactory } from '@/modules/apps/auth/assistance/factories/assistanceFactory';

export function useAssistanceReset() {
  const resetAssistanceFactory = assistanceFactory => {
    Object.assign(assistanceFactory, createAssistanceFactory());
  };

  return { resetAssistanceFactory };
}
