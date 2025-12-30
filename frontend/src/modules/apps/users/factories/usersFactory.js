export function createUserFactory() {
  return {
    id: '',
    first_name: '',
    last_name: '',
    email: '',
    attachment: '',
    role: {
      id: '',
      name: '',
    },
  };
}

export function createUserStatsFactory() {
  return {
    plan_type: {
      id: '',
      name: '',
      max_projects: '',
      max_users: '',
      can_invite: false,
      is_private_allowed: false,
    },
    projects: [],
  };
}

export function createUserSessionActivityFactory() {
  return {
    list: [],
  };
}

export function createUsersFactory() {
  return {
    list: [],
  };
}
