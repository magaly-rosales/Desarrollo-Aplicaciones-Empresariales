import { useCallback, useEffect, useRef, useState } from "react";

const IDLE = { status: "idle", plan: null, result: null, error: null };

// State machine for running a plan:
// idle -> running -> done (R1) | awaiting_approval -> done (R2, only with approve) | error
export default function useAgentRun(runAgent) {
  // Hooks always at the top level, in the same order (no early return before them)
  const [run, setRun] = useState(IDLE);
  const latest = useRef(IDLE); // most recent state, readable inside the callbacks
  const controller = useRef(null); // AbortController of the current run

  const update = useCallback((next) => {
    latest.current = next;
    setRun(next);
  }, []);

  // On unmount: abort the run in progress
  useEffect(() => {
    return () => controller.current?.abort();
  }, []);

  const start = useCallback(
    (plan) => {
      if (!runAgent) return; // runAgent may be missing for now: stay idle
      const { status } = latest.current;
      if (status === "running" || status === "awaiting_approval") return;

      const current = new AbortController();
      controller.current = current;
      update({ status: "running", plan, result: null, error: null });

      runAgent(plan, { signal: current.signal }).then(
        (result) => {
          if (current.signal.aborted) return;
          // SECURITY RULE: an R2 plan never goes straight to done
          const status = plan.risk === "R2" ? "awaiting_approval" : "done";
          update({ status, plan, result, error: null });
        },
        (error) => {
          if (current.signal.aborted) return;
          update({ status: "error", plan, result: null, error });
        }
      );
    },
    [runAgent, update]
  );

  const approve = useCallback(() => {
    if (latest.current.status !== "awaiting_approval") return;
    update({ ...latest.current, status: "done" });
  }, [update]);

  const reject = useCallback(() => {
    const { status } = latest.current;
    if (status !== "running" && status !== "awaiting_approval") return;
    controller.current?.abort();
    update(IDLE);
  }, [update]);

  return { ...run, start, approve, reject };
}