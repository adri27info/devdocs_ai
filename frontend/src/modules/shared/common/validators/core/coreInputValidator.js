import { REQUIREMENTS } from '@/modules/shared/common/constants/core/coreInputRequeriments';
import { VALIDATIONS } from '@/modules/shared/common/constants/core/coreInputValidations';
import { useInputTextValidator } from '@/modules/shared/common/composables/forms/useInputTextValidator';

class CoreInputValidatorClass {
  constructor() {
    this.REQ = REQUIREMENTS;
    this.VAL = VALIDATIONS;
    this.inputTextValidator = useInputTextValidator(this.VAL).validateText;
  }

  validateEmail(email) {
    const err = this.inputTextValidator('Email', email, this.REQ.EMAIL.MAX_LENGTH);
    if (err) return err;

    if (!this.REQ.EMAIL.REGEX.test(email)) return this.VAL.EMAIL_INVALID;

    return '';
  }

  validatePassword({ password, additionalValidations = true }) {
    const err = this.inputTextValidator('Password', password, this.REQ.PASSWORD.MAX_LENGTH);
    if (err) return err;

    if (additionalValidations) {
      for (const rule of this.REQ.PASSWORD.PATTERNS) {
        if (!rule.regex.test(password)) return rule.message;
      }
    }

    return '';
  }

  validateActivationCode(code) {
    return this.inputTextValidator('Activation code', code, this.REQ.ACTIVATION_CODE.MAX_LENGTH);
  }

  validateConfirmationCode(code) {
    return this.inputTextValidator(
      'Confirmation code',
      code,
      this.REQ.CONFIRMATION_CODE.MAX_LENGTH,
    );
  }

  validateInvitationCode(code) {
    return this.inputTextValidator('Invitation code', code, this.REQ.INVITATION_CODE.MAX_LENGTH);
  }

  validateBodyPrompt(prompt) {
    return this.inputTextValidator('Body prompt', prompt, this.REQ.BODY_PROMPT.MAX_LENGTH);
  }

  validateName(name) {
    return this.inputTextValidator('Name', name, this.REQ.NAME.MAX_LENGTH);
  }

  validateFirstName(firstName) {
    return this.inputTextValidator('First name', firstName, this.REQ.FIRST_NAME.MAX_LENGTH);
  }

  validateLastName(lastName) {
    return this.inputTextValidator('Last name', lastName, this.REQ.LAST_NAME.MAX_LENGTH);
  }

  validateDescription(value) {
    return this.inputTextValidator('Description', value, this.REQ.DESCRIPTION.MAX_LENGTH);
  }

  validateMessageReason(value) {
    return this.inputTextValidator('Message reason', value, this.REQ.GENERAL.TEXT.MAX_LENGTH);
  }

  validateAttachment(file) {
    if (!file) return '';

    if (file.size > this.REQ.ATTACHMENT.MAX_SIZE_MB * 1024 * 1024)
      return this.VAL.ATTACHMENT_MAX_SIZE(this.REQ.ATTACHMENT.MAX_SIZE_MB);

    if (!this.REQ.ATTACHMENT.ALLOWED_TYPES.includes(file.type)) return this.VAL.ATTACHMENT_TYPE;

    return '';
  }
}

export const CoreInputValidator = new CoreInputValidatorClass();
