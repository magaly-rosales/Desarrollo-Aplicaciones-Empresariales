import { useEffect, useState } from "react";

// Returns the "calm" value: the last `value` that stayed unchanged for `delay` ms.
export default function useDebounce(value, delay) {
  const [debounced, setDebounced] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay);

    // Cleanup: runs before the effect repeats and on unmount, so no timer stays alive
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debounced;
}