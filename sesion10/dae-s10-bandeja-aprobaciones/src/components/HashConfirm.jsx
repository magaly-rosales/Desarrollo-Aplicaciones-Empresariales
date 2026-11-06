import { useState } from "react";
import Button from "./Button";

// Confirmation for destructive plans: the person must type the exact plan hash.
export default function HashConfirm({ hash, onConfirm }) {
  const [typed, setTyped] = useState("");
  const matches = typed === hash;

  return (
    <div className="hash-confirm">
      <label>
        Hash del plan
        <input
          type="text"
          autoComplete="off"
          spellCheck={false}
          value={typed}
          onChange={(event) => setTyped(event.target.value)}
        />
      </label>
      <Button variant="danger" disabled={!matches} onClick={() => onConfirm()}>
        Aprobar
      </Button>
    </div>
  );
}