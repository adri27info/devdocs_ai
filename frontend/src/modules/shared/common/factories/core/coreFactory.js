export function createLoadersFactory() {
  return {
    routerBlock: false,
    login: false,
    register: false,
    activateAccount: false,
    resendActivationCode: false,
    resetPassword: false,
    resetPasswordConfirm: false,
    profileUserInit: false,
    profileUser: false,
    profileUserPassword: false,
    dashboard: false,
    overview: false,
    assistance: false,
    projects: false,
    project: false,
    projectCreate: false,
    projectUpdate: false,
    projectDelete: false,
    projectAddUser: false,
    projectDocumentCreate: false,
    projectDocumentVote: false,
    projectDocumentsList: false,
    notifications: false,
    notificationDelete: false,
    llm: false,
    paymentStatus: false,
    paymentPollingStatus: false,
    paymentInvoice: false,
    sessionActivity: false,
    delete: false,
  };
}

export function createRedirectsFactory() {
  return {
    logout: false,
  };
}

export function createBtnDisablerFactory() {
  return {
    loginBtn: false,
    registerBtn: false,
    activateAccountBtn: false,
    resendActivationCodeBtn: false,
    logoutBtn: false,
    resetPasswordBtn: false,
    resetPasswordConfirmBtn: false,
    profileUserBtn: false,
    profileUserPasswordBtn: false,
    projectCreateBtn: false,
    projectUpdateBtn: false,
    projectDeleteBtn: false,
    projectConfirmBtn: false,
    projectAddUserBtn: false,
    projectDocumentCreateBtn: false,
    projectDocumentVoteBtn: false,
    notificationDeleteBtn: false,
    assistanceBtn: false,
    resetBtn: false,
    deleteBtn: false,
  };
}
