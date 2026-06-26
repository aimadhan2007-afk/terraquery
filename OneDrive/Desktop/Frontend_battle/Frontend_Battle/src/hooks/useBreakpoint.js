import { useEffect, useState } from 'react';

export function useBreakpoint(query) {
  const getMatch = () => window.matchMedia(query).matches;
  const [matches, setMatches] = useState(() => (typeof window === 'undefined' ? false : getMatch()));

  useEffect(() => {
    const mediaQuery = window.matchMedia(query);
    const handleChange = () => setMatches(mediaQuery.matches);
    handleChange();
    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, [query]);

  return matches;
}