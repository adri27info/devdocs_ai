export function useTextTruncator() {
  const truncText = (text, maxLength = 50) => {
    if (!text) return '';
    return text.length > maxLength ? text.slice(0, maxLength) + ' …' : text;
  };

  return {
    truncText,
  };
}
