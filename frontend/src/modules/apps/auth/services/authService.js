import { CoreService } from '@/modules/shared/common/services/core/coreService';

export class AuthService extends CoreService {
  loginUser(email, password, rememberMe = false) {
    const data = { email, password, remember_me: rememberMe };

    return this.axios.post('/auth/login/', data, {
      headers: this._getHeaders(),
    });
  }

  registerUser(firstName, lastName, email, password, attachment = null) {
    const fields = {
      first_name: firstName,
      last_name: lastName,
      email: email,
      password: password,
      ...(attachment ? { attachment } : {}),
    };

    return this.requestUtil.sendData('/auth/register/', fields);
  }

  activateUserAccount(email, activationCode) {
    const data = { email, activation_code: activationCode };

    return this.axios.patch('/auth/activate-user-account/', data, {
      headers: this._getHeaders(),
    });
  }

  resendUserActivationCode(email) {
    const data = { email };

    return this.axios.patch('/auth/resend-user-activation-code/', data, {
      headers: this._getHeaders(),
    });
  }

  resetUserPassword(email) {
    const data = { email };

    return this.axios.post('/auth/reset-password/', data, {
      headers: this._getHeaders(),
    });
  }

  resetUserPasswordConfirm(uid, token, password) {
    const data = { uid, token, password };

    return this.axios.patch('/auth/reset-password/confirm/', data, {
      headers: this._getHeaders(),
    });
  }

  assistanceUser(email, type, resetReason = null, messageReason = null) {
    const data = {
      email,
      type,
      ...(resetReason && { reset_reason: resetReason }),
      ...(messageReason && { message_reason: messageReason }),
    };

    return this.axios.post('/auth/assistance/', data, {
      headers: this._getHeaders(),
    });
  }

  logoutUser() {
    return this.axios.post('/auth/token/revoke/', {
      headers: this._getHeaders(),
    });
  }

  forceLogoutUser() {
    return this.axios.post('/auth/token/force-logout/', {
      headers: this._getHeaders(),
    });
  }

  refreshTokenUser() {
    return this.axios.post('/auth/token/refresh/', {
      headers: this._getHeaders(),
    });
  }

  refreshCSRFTokenUser() {
    return this.axios.get('/auth/token/csrf-refresh/', {
      headers: this._getHeaders(),
    });
  }
}
