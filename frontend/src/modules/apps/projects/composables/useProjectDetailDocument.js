import { ref, reactive, watch, onMounted, nextTick } from 'vue';
import { createProjectDocumentFactory } from '@/modules/apps/projects/factories/projectDocumentFactory';
import { createProjectDocumentVoteFactory } from '@/modules/apps/projects/factories/projectDocumentVoteFactory';
import { FORMATS } from '@/modules/shared/common/constants/apps/projects/formats';
import { RATING_PROJECT_DOCUMENTS_OPTIONS } from '@/modules/shared/common/constants/apps/projects/rating';
import { useFetcher } from '@/modules/shared/common/composables/utils/useFetcher';
import { useModal } from '@/modules/shared/common/composables/utils/ui/useModal';
import { useProjectDetailDocumentReset } from '@/modules/apps/projects/composables/useProjectDetailDocumentReset';
import { useProjectDetailDocumentValidations } from '@/modules/apps/projects/composables/useProjectDetailDocumentValidations';

export function useProjectDetailDocument(projectId) {
  const shouldValidate = ref(true);
  const selectedDocumentFormatOption = ref(null);
  const currentVotingDocumentId = ref(null);
  const projectDocumentFactory = reactive(createProjectDocumentFactory());
  const projectDocumentVoteFactory = reactive(createProjectDocumentVoteFactory());

  const { isOpen, close, open } = useModal();
  const { fetch } = useFetcher();

  const { resetProjectDocumentFactory, resetProjectDocumentVoteFactory } =
    useProjectDetailDocumentReset();

  const { validateBodyPrompt, validateRating, validateFieldsProjectDocumentation } =
    useProjectDetailDocumentValidations();

  const handleProjectDocument = async () => {
    if (!validateFieldsProjectDocumentation(selectedDocumentFormatOption, projectDocumentFactory))
      return;

    if (selectedDocumentFormatOption.value) {
      projectDocumentFactory.format = selectedDocumentFormatOption.value.value;
    }

    const result = await fetch({
      app: 'project',
      action: 'createProjectDocument',
      params: {
        projectId: projectId,
        format: projectDocumentFactory.format,
        bodyPrompt: projectDocumentFactory.bodyPrompt,
      },
    });

    if (result?.success) {
      shouldValidate.value = false;
      resetProjectDocumentState(projectDocumentFactory);

      await fetch({
        app: 'llm',
        hideSuccess: true,
      });

      await fetch({
        app: 'project',
        action: 'documentList',
        params: projectId,
        hideSuccess: true,
      });

      nextTick(() => {
        shouldValidate.value = true;
      });
    }
  };

  const submitVote = async () => {
    if (!validateRating(projectDocumentVoteFactory)) return;

    const result = await fetch({
      app: 'project',
      action: 'voteProjectDocument',
      params: {
        documentId: currentVotingDocumentId.value,
        rating: projectDocumentVoteFactory.rating,
      },
    });

    closeModal();

    if (result?.success) {
      await fetch({
        app: 'project',
        action: 'documentList',
        params: projectId,
        hideSuccess: true,
      });
    }
  };

  const openDocument = url => {
    window.open(url, '_blank');
  };

  const resetProjectDocumentState = projectDocumentFactory => {
    resetProjectDocumentFactory(projectDocumentFactory);
    selectedDocumentFormatOption.value = null;
  };

  const openModal = documentId => {
    currentVotingDocumentId.value = documentId;
    open();
  };

  const closeModal = () => {
    close();
    currentVotingDocumentId.value = null;
    resetProjectDocumentVoteState(projectDocumentVoteFactory);
  };

  const resetProjectDocumentVoteState = projectDocumentVoteFactory => {
    resetProjectDocumentVoteFactory(projectDocumentVoteFactory);
  };

  watch(
    () => projectDocumentFactory.bodyPrompt,
    () => {
      if (!shouldValidate.value) return;
      validateBodyPrompt(projectDocumentFactory);
    },
  );

  watch(
    () => projectDocumentVoteFactory.rating,
    newVal => {
      if (newVal) {
        projectDocumentVoteFactory.ratingError = '';
      }
    },
  );

  onMounted(async () => {
    await fetch({
      app: 'llm',
      hideSuccess: true,
    });

    await fetch({
      app: 'project',
      action: 'documentList',
      params: projectId,
      hideSuccess: true,
    });
  });

  return {
    documentFormatOptions: FORMATS,
    rateOptions: RATING_PROJECT_DOCUMENTS_OPTIONS,
    selectedDocumentFormatOption,
    projectDocumentFactory,
    projectDocumentVoteFactory,
    isOpen,

    handleProjectDocument,
    submitVote,
    openDocument,
    openModal,
    closeModal,
  };
}
