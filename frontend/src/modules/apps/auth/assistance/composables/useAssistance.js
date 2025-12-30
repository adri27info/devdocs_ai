import { ref, reactive, watch, nextTick } from 'vue';
import { createAssistanceFactory } from '@/modules/apps/auth/assistance/factories/assistanceFactory';
import { ISSUES } from '@/modules/shared/common/constants/apps/auth/assistance/issues';
import { useFetcher } from '@/modules/shared/common/composables/utils/useFetcher';
import { useAssistanceReset } from '@/modules/apps/auth/assistance/composables/useAssistanceReset';
import { useAssistanceValidations } from '@/modules/apps/auth/assistance/composables/useAssistanceValidations';

export function useAssistance() {
  const shouldValidate = ref(true);
  const selectedOption = ref(null);
  const assistanceFactory = reactive(createAssistanceFactory());

  const { fetch } = useFetcher();
  const { resetAssistanceFactory } = useAssistanceReset();
  const { validateEmail, validateMessageReason, validateFieldsAssistance } =
    useAssistanceValidations();

  const handleAssistance = async () => {
    if (!validateFieldsAssistance(selectedOption, assistanceFactory)) return;

    if (selectedOption.value) {
      if (selectedOption.value.value === 'info') {
        assistanceFactory.type = 'info';
        assistanceFactory.resetReason = '';
      } else {
        assistanceFactory.type = 'reset';
        assistanceFactory.resetReason = selectedOption.value.value;
      }
    }

    const result = await fetch({
      app: 'auth',
      action: 'assistance',
      params: {
        email: assistanceFactory.email,
        type: assistanceFactory.type,
        resetReason: assistanceFactory.resetReason,
        messageReason: assistanceFactory.messageReason,
      },
    });

    if (result?.success) {
      shouldValidate.value = false;

      resetAssistanceFactory(assistanceFactory);
      selectedOption.value = null;

      nextTick(() => {
        shouldValidate.value = true;
      });
    }
  };

  watch(
    () => assistanceFactory.email,
    () => {
      if (!shouldValidate.value) return;
      validateEmail(assistanceFactory);
    },
  );

  watch(
    () => assistanceFactory.messageReason,
    () => {
      if (!shouldValidate.value) return;
      validateMessageReason(selectedOption, assistanceFactory);
    },
  );

  return {
    options: ISSUES,
    selectedOption,
    assistanceFactory,

    handleAssistance,
  };
}
