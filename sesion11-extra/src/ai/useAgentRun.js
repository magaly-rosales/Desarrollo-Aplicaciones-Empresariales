import { useCallback, useEffect, useRef, useState } from "react";

const IDLE = { status: "idle", plan: null, result: null, error: null };

export default function useAgentRun(runAgent) {
  // FIX 4: every hook at the top level, before any condition
  const [run, setRun] = useState(IDLE);
  const latest = useRef(IDLE);
  const controller = useRef(null);

  const update = (next) => {
    latest.current = next;
    setRun(next);
  };

  // FIX 6: abort the run in progress when the component unmounts
  useEffect(() => {
    return () => controller.current?.abort();
  }, []);

  const start = useCallback(
    (plan) => {
      if (!runAgent) return; // FIX 4: the condition moves inside the function
      const { status } = latest.current;
      if (status === "running" || status === "awaiting_approval") return;

      const current = new AbortController();
      controller.current = current;
      update({ status: "running", plan, result: null, error: null });

      runAgent(plan, { signal: current.signal }).then(
        (result) => {
          if (current.signal.aborted) return;
          // FIX 5: an R2 plan waits for approve() before reaching done
          const next = plan.risk === "R2" ? "awaiting_approval" : "done";
          update({ status: next, plan, result, error: null });
        },
        (error) => {
          if (current.signal.aborted) return;
          update({ status: "error", plan, result: null, error });
        }
      );
    },
    [runAgent]
  );

  const approve = useCallback(() => {
    if (latest.current.status !== "awaiting_approval") return;
    update({ ...latest.current, status: "done" });
  }, []);

  const reject = useCallback(() => {
    const { status } = latest.current;
    if (status !== "running" && status !== "awaiting_approval") return;
    controller.current?.abort();
    update(IDLE);
  }, []);

  return { ...run, start, approve, reject };
}