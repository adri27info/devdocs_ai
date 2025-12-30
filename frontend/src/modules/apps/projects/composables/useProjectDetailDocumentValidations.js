import { CoreInputValidator } from '@/modules/shared/common/validators/core/coreInputValidator';

export function useProjectDetailDocumentValidations() {
  const OPTION_ERROR = 'Please select an valid option';
  const RATING_ERROR = 'Please select a rating.';

  const validateBodyPrompt = projectDocumentFactory => {
    return (projectDocumentFactory.bodyPromptError = CoreInputValidator.validateBodyPrompt(
      projectDocumentFactory.bodyPrompt,
    ));
  };

  const validateFormat = (selectedDocumentFormatOption, projectDocumentFactory) => {
    if (!selectedDocumentFormatOption.value || selectedDocumentFormatOption.value.value === '') {
      projectDocumentFactory.formatError = OPTION_ERROR;
      return projectDocumentFactory.formatError;
    }

    projectDocumentFactory.formatError = '';
    return '';
  };

  const validateRating = projectDocumentVoteFactory => {
    if (!projectDocumentVoteFactory.rating) {
      projectDocumentVoteFactory.ratingError = RATING_ERROR;
      return false;
    }

    projectDocumentVoteFactory.ratingError = '';
    return true;
  };

  const validateFieldsProjectDocumentation = (
    selectedDocumentFormatOption,
    projectDocumentFactory,
  ) => {
    const validations = [
      validateBodyPrompt(projectDocumentFactory),
      validateFormat(selectedDocumentFormatOption, projectDocumentFactory),
    ];
    return validations.every(result => !result);
  };

  return {
    validateBodyPrompt,
    validateRating,
    validateFieldsProjectDocumentation,
  };
}
