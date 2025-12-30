import { ref, reactive, watch } from 'vue';
import { createBasicProfileFactory } from '@/modules/apps/projects/factories/projectBasicFactory';
import { PRIVACY_OPTIONS } from '@/modules/shared/common/constants/apps/projects/privacy_options';
import { useProjectReset } from '@/modules/apps/projects/composables/useProjectReset';
import { useModal } from '@/modules/shared/common/composables/utils/ui/useModal';
import { useFetcher } from '@/modules/shared/common/composables/utils/useFetcher';
import { useProjectCreateValidations } from '@/modules/apps/projects/composables/useProjectCreateValidations';

export function useProjectCreate() {
  const selectedOption = ref(null);
  const basicProfileCreateFactory = reactive(createBasicProfileFactory());

  const { isOpen, close, open } = useModal();
  const { resetBasicProfileFactory } = useProjectReset();
  const { fetch } = useFetcher();

  const { validateName, validateDescription, validateFieldsProjectCreate } =
    useProjectCreateValidations();

  const handleCreateProject = async () => {
    if (!validateFieldsProjectCreate(selectedOption, basicProfileCreateFactory)) return;

    if (selectedOption.value) {
      if (selectedOption.value.value === 'public') {
        basicProfileCreateFactory.privacy = 'public';
      } else {
        basicProfileCreateFactory.privacy = 'private';
      }
    }

    const result = await fetch({
      app: 'project',
      action: 'create',
      params: {
        name: basicProfileCreateFactory.name,
        description: basicProfileCreateFactory.description,
        privacy: basicProfileCreateFactory.privacy,
        users: basicProfileCreateFactory.users,
      },
    });

    closeModal();

    if (result?.success) {
      await fetch({
        app: 'project',
        action: 'list',
        hideSuccess: true,
      });
    }
  };

  const openModal = async () => {
    resetCreateProjectUIState();
    open();

    await fetch({
      app: 'users',
      hideSuccess: true,
    });
  };

  const closeModal = () => {
    close();
    resetCreateProjectUIState();
  };

  const resetCreateProjectUIState = () => {
    resetBasicProfileFactory(basicProfileCreateFactory);
    selectedOption.value = null;
  };

  watch(
    () => basicProfileCreateFactory.name,
    () => {
      validateName(basicProfileCreateFactory);
    },
  );

  watch(
    () => basicProfileCreateFactory.description,
    () => {
      validateDescription(basicProfileCreateFactory);
    },
  );

  return {
    options: PRIVACY_OPTIONS,
    selectedOption,
    basicProfileCreateFactory,
    isOpen,

    validateName,
    validateDescription,
    handleCreateProject,
    openModal,
    closeModal,
  };
}
