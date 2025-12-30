import { ref, reactive, computed, watch } from 'vue';
import { createProfileFactory } from '@/modules/apps/users/profile/factories/profileFactory';
import { CoreInputValidator } from '@/modules/shared/common/validators/core/coreInputValidator';
import { useProfileValidations } from '@/modules/apps/users/profile/composables/useProfileValidations';
import { useTextTruncator } from '@/modules/shared/common/composables/utils/useTextTruncator';
import { useFetcher } from '@/modules/shared/common/composables/utils/useFetcher';
import { userStore } from '@/modules/apps/users/stores/userStore';

export function useProfile(closeDropdown) {
  const storeUser = userStore();

  const profileFactory = reactive(createProfileFactory());
  const attachmentInputRef = ref(null);
  const avatarSrc = ref('');

  const { fetch } = useFetcher();
  const { truncText } = useTextTruncator();

  const { validateFirstName, validateLastName, validateAttachment, validateFieldsProfile } =
    useProfileValidations();

  const truncatedAttachmentName = computed(() =>
    profileFactory.attachment ? truncText(profileFactory.attachment.name, 20) : 'No file chosen',
  );

  const handleProfile = async () => {
    if (!validateFieldsProfile(profileFactory)) return;

    await fetch({
      app: 'user',
      action: 'updateProfile',
      params: {
        id: storeUser.userFactory.id,
        firstName: profileFactory.firstName,
        lastName: profileFactory.lastName,
        attachment: profileFactory.attachment,
      },
    });
  };

  const handleCloseDropdown = async () => {
    closeDropdown();
  };

  const setAttachment = e => {
    profileFactory.attachment = e?.target?.files?.[0] || null;
  };

  const resetAttachment = () => {
    if (profileFactory.attachment) {
      profileFactory.attachment = '';
      profileFactory.attachmentError = '';
    }

    if (attachmentInputRef.value) {
      attachmentInputRef.value.value = '';
    }
  };

  watch(
    () => profileFactory.firstName,
    () => {
      validateFirstName(profileFactory);
    },
  );

  watch(
    () => profileFactory.lastName,
    () => {
      validateLastName(profileFactory);
    },
  );

  watch(
    () => profileFactory.attachment,
    () => {
      validateAttachment(profileFactory);
    },
  );

  watch(
    () => profileFactory.attachment,
    newFile => {
      if (newFile) {
        profileFactory.attachmentError = CoreInputValidator.validateAttachment(newFile);
      }
    },
  );

  watch(
    () => storeUser.userFactory,
    user => {
      profileFactory.firstName = user.first_name;
      profileFactory.lastName = user.last_name;
      avatarSrc.value = user.attachment;
    },
    { immediate: true, deep: true },
  );

  return {
    profileFactory,
    attachmentInputRef,
    truncatedAttachmentName,
    avatarSrc,

    handleCloseDropdown,
    handleProfile,
    setAttachment,
    resetAttachment,
  };
}
