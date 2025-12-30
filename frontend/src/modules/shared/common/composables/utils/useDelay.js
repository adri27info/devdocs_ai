export function useDelay() {
  const delay = (ms = 1500) => {
    return new Promise(resolve => {
      setTimeout(resolve, ms);
    });
  };

  return { delay };
}
