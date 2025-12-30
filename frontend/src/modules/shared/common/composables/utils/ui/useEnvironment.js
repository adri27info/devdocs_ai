export function useEnvironment() {
  return {
    apiBackend: import.meta.env.VITE_BACKEND_URL,
    logo: import.meta.env.VITE_LOGO_URL,
    imageNotFound: import.meta.env.VITE_IMAGE_NOT_FOUND_URL,
    llm: import.meta.env.VITE_LLM_URL,
    userProfile: import.meta.env.VITE_USER_PROFILE_IMAGE,
  };
}
