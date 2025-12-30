export function createBasicProfileFactory() {
  return {
    name: '',
    nameError: '',
    description: '',
    descriptionError: '',
    privacy: '',
    privacyError: '',
    users: [],
    users_to_exclude: [],
    users_to_add: [],
  };
}
