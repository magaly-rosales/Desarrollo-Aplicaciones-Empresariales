import { useEffect, useState } from "react";

export default function useDebounce(value, delay) {
  const [debounced, setDebounced] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebounced(value);
    }, delay);

    // FIX 1: clear the previous timer on every change and on unmount
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debounced;
}