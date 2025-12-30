import { ref, reactive, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { PRIVACY_OPTIONS } from '@/modules/shared/common/constants/apps/projects/privacy_options';
import { createBasicProfileFactory } from '@/modules/apps/projects/factories/projectBasicFactory';
import { useFetcher } from '@/modules/shared/common/composables/utils/useFetcher';
import { useModal } from '@/modules/shared/common/composables/utils/ui/useModal';
import { useProjectDetailDataValidations } from '@/modules/apps/projects/composables/useProjectDetailDataValidations';
import { projectStore } from '@/modules/apps/projects/stores/projectStore';

export function useProjectDetailData(id) {
  const router = useRouter();
  const storeProject = projectStore();

  const selectedOption = ref(null);
  const basicProfileUpdateFactory = reactive(createBasicProfileFactory());

  const { isOpen, close, open } = useModal();
  const { fetch } = useFetcher();

  const { validateName, validateDescription, validateFieldsProjecUpdate } =
    useProjectDetailDataValidations();

  const handleUpdateProject = async () => {
    if (!validateFieldsProjecUpdate(selectedOption, basicProfileUpdateFactory)) return;

    if (selectedOption.value) {
      if (selectedOption.value.value === 'public') {
        basicProfileUpdateFactory.privacy = 'public';
      } else {
        basicProfileUpdateFactory.privacy = 'private';
      }
    }

    const result = await fetch({
      app: 'project',
      action: 'update',
      params: {
        id: id,
        name: basicProfileUpdateFactory.name,
        description: basicProfileUpdateFactory.description,
        privacy: basicProfileUpdateFactory.privacy,
        users_to_exclude: basicProfileUpdateFactory.users_to_exclude,
        users_to_add: basicProfileUpdateFactory.users_to_add,
      },
    });

    if (result?.success) {
      await fetch({
        app: 'project',
        action: 'id',
        params: { projectId: id },
        hideSuccess: true,
      });
    }
  };

  const deleteProject = async () => {
    const result = await fetch({
      app: 'project',
      action: 'delete',
      params: {
        id: id,
      },
    });

    if (result?.success) {
      closeModal();
      router.push({ name: 'projects' });
    } else {
      closeModal();
    }
  };

  const openModal = () => {
    open();
  };

  const closeModal = () => {
    close();
  };

  watch(
    () => basicProfileUpdateFactory.name,
    () => {
      validateName(basicProfileUpdateFactory);
    },
  );

  watch(
    () => basicProfileUpdateFactory.description,
    () => {
      validateDescription(basicProfileUpdateFactory);
    },
  );

  watch(
    () => storeProject.projectFactory,
    project => {
      basicProfileUpdateFactory.name = project.name;
      basicProfileUpdateFactory.description = project.description;
      basicProfileUpdateFactory.privacy = project.privacy;
      selectedOption.value = PRIVACY_OPTIONS.find(opt => opt.value === project.privacy);

      basicProfileUpdateFactory.users_to_exclude = [];
      basicProfileUpdateFactory.users_to_add = [];
    },
    { immediate: true, deep: true },
  );

  onMounted(async () => {
    await fetch({
      app: 'project',
      action: 'id',
      params: { projectId: id },
      hideSuccess: true,
    });

    await fetch({
      app: 'users',
      hideSuccess: true,
    });
  });

  return {
    isOpen,
    options: PRIVACY_OPTIONS,
    selectedOption,
    basicProfileUpdateFactory,

    deleteProject,
    handleUpdateProject,
    openModal,
    closeModal,
  };
}
