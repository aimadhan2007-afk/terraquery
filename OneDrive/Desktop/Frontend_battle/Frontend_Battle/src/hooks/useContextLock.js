import { useEffect, useRef, useState } from 'react';

export function useContextLock(initialKey = null) {
  const [lockedKey, setLockedKey] = useState(initialKey);
  const previousMode = useRef(null);

  const syncMode = (mode) => {
    previousMode.current = mode;
  };

  useEffect(() => {
    if (previousMode.current === null) return;
  }, []);

  return { lockedKey, setLockedKey, syncMode };
}