export function createPaymentFactory() {
  return {
    checkoutUrl: '',
    sessionId: '',
    status: '',
    invoice: {
      id: '',
      attachment: '',
      created_at: '',
      user: '',
      plan_type: '',
    },
  };
}
