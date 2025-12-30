export function useMenuOption(order, divisor) {
  function getTemplateOrder() {
    return order === 'icon-first' ? 'icon-first' : 'default';
  }

  function showDivisor() {
    return !!divisor;
  }

  return {
    getTemplateOrder,
    showDivisor,
  };
}
