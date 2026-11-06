// Reusable button: variant -> CSS class, content via children,
// type="button" by default, and every other prop forwarded to <button>.
export default function Button({ variant = "primary", children, ...rest }) {
  return (
    <button type="button" {...rest} className={`btn btn-${variant}`}>
      {children}
    </button>
  );
}