import { createProjectDocumentFactory } from '@/modules/apps/projects/factories/projectDocumentFactory';
import { createProjectDocumentVoteFactory } from '@/modules/apps/projects/factories/projectDocumentVoteFactory';

export function useProjectDetailDocumentReset() {
  const resetProjectDocumentFactory = projectDocumentFactory => {
    Object.assign(projectDocumentFactory, createProjectDocumentFactory());
  };

  const resetProjectDocumentVoteFactory = projectDocumentVoteFactory => {
    Object.assign(projectDocumentVoteFactory, createProjectDocumentVoteFactory());
  };

  return { resetProjectDocumentFactory, resetProjectDocumentVoteFactory };
}
