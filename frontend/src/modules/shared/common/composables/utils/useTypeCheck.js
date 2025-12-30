export function useTypeCheck() {
  function isType(value, type) {
    return typeof value === type;
  }

  function isInstanceOf(value, constructor) {
    return value instanceof constructor;
  }

  return {
    isType,
    isInstanceOf,
  };
}
