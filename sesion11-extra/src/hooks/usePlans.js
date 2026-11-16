import { useCallback, useEffect, useState } from "react";

const LOADING = { status: "loading", plans: [], error: null };

// Loads the agent plans with the three states of a request: loading, ready and error.
export default function usePlans(fetchPlans) {
  const [state, setState] = useState(LOADING);
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    // Set to true by the cleanup: an old response must never touch the state
    let cancelled = false;
    setState(LOADING);

    fetchPlans().then(
      (plans) => {
        if (!cancelled) setState({ status: "ready", plans, error: null });
      },
      (error) => {
        if (!cancelled) setState({ status: "error", plans: [], error });
      }
    );

    return () => {
      cancelled = true;
    };
  }, [fetchPlans, attempt]);

  // Same identity on every render
  const reload = useCallback(() => setAttempt((n) => n + 1), []);

  return { ...state, reload };
}