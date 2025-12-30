import { ref, watch, reactive, computed } from 'vue';
import { useRouter } from 'vue-router';
import { createRegisterFactory } from '@/modules/apps/auth/register/factories/registerFactory';
import { CoreInputValidator } from '@/modules/shared/common/validators/core/coreInputValidator';
import { useTextTruncator } from '@/modules/shared/common/composables/utils/useTextTruncator';
import { useFetcher } from '@/modules/shared/common/composables/utils/useFetcher';
import { useRegisterValidations } from '@/modules/apps/auth/register/composables/useRegisterValidations';
import { useFormPasswordFieldProps } from '@/modules/shared/common/composables/forms/useFormPasswordFieldsProps';

export function useRegister() {
  const router = useRouter();

  const registerFactory = reactive(createRegisterFactory());
  const attachmentInputRef = ref(null);

  const {
    validateFirstName,
    validateLastName,
    validateEmail,
    validatePassword,
    validateAttachment,
    validateFieldsRegister,
  } = useRegisterValidations();

  const { passwordProps, togglePasswordVisibility } = useFormPasswordFieldProps(
    registerFactory,
    'passwordVisible',
  );

  const { fetch } = useFetcher();
  const { truncText } = useTextTruncator();

  const truncatedAttachmentName = computed(() =>
    registerFactory.attachment ? truncText(registerFactory.attachment.name, 20) : 'No file chosen',
  );

  const handleRegister = async () => {
    if (!validateFieldsRegister(registerFactory)) return;

    const result = await fetch({
      app: 'auth',
      action: 'register',
      params: {
        firstName: registerFactory.firstName,
        lastName: registerFactory.lastName,
        email: registerFactory.email,
        password: registerFactory.password,
        attachment: registerFactory.attachment,
      },
    });

    if (result.success) {
      await router.push({ name: 'activate-account' });
    }
  };

  const setAttachment = e => {
    registerFactory.attachment = e?.target?.files?.[0] || null;
  };

  const resetAttachment = () => {
    if (registerFactory.attachment) {
      registerFactory.attachment = '';
      registerFactory.attachmentError = '';
    }

    if (attachmentInputRef.value) {
      attachmentInputRef.value.value = '';
    }
  };

  watch(
    () => registerFactory.firstName,
    () => {
      validateFirstName(registerFactory);
    },
  );

  watch(
    () => registerFactory.lastName,
    () => {
      validateLastName(registerFactory);
    },
  );

  watch(
    () => registerFactory.email,
    () => {
      validateEmail(registerFactory);
    },
  );

  watch(
    () => registerFactory.password,
    () => {
      validatePassword(registerFactory);
    },
  );

  watch(
    () => registerFactory.attachment,
    () => {
      validateAttachment(registerFactory);
    },
  );

  watch(
    () => registerFactory.attachment,
    newFile => {
      if (newFile) {
        registerFactory.attachmentError = CoreInputValidator.validateAttachment(newFile);
      }
    },
  );

  return {
    registerFactory,
    attachmentInputRef,
    passwordProps,
    truncatedAttachmentName,

    handleRegister,
    togglePasswordVisibility,
    setAttachment,
    resetAttachment,
  };
}
