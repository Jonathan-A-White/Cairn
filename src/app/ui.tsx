import type {
  ButtonHTMLAttributes,
  InputHTMLAttributes,
  ReactNode,
  SelectHTMLAttributes,
  TextareaHTMLAttributes,
} from "react";

type Variant = "primary" | "secondary" | "ghost" | "danger";

const variants: Record<Variant, string> = {
  primary:
    "bg-cairn-neon text-cairn-void font-semibold shadow-emit hover:shadow-emit-strong",
  secondary:
    "bg-cairn-panel text-cairn-ink border border-cairn-trace hover:border-cairn-neon-soft",
  ghost: "bg-transparent text-cairn-dim hover:text-cairn-ink",
  danger: "bg-cairn-danger/20 text-cairn-danger-ink border border-cairn-danger",
};

export function Button({
  variant = "primary",
  className = "",
  children,
  ...rest
}: ButtonHTMLAttributes<HTMLButtonElement> & { variant?: Variant }) {
  return (
    <button
      className={`rounded-lg px-4 py-2 font-medium transition-colors active:opacity-80 disabled:opacity-40 disabled:shadow-none ${variants[variant]} ${className}`}
      {...rest}
    >
      {children}
    </button>
  );
}

const fieldClass =
  "w-full rounded-lg border border-cairn-trace bg-cairn-panel px-3 py-2 text-cairn-ink outline-none transition-colors focus:border-cairn-neon focus:shadow-emit";

export function TextInput(props: InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      {...props}
      className={`${fieldClass} ${props.className ?? ""}`}
    />
  );
}

export function TextArea(props: TextareaHTMLAttributes<HTMLTextAreaElement>) {
  return (
    <textarea
      {...props}
      className={`${fieldClass} ${props.className ?? ""}`}
    />
  );
}

export function Select(props: SelectHTMLAttributes<HTMLSelectElement>) {
  return (
    <select
      {...props}
      className={`rounded-lg border border-cairn-trace bg-cairn-panel px-2 py-2 text-cairn-ink outline-none transition-colors focus:border-cairn-neon ${props.className ?? ""}`}
    />
  );
}

/** A component soldered to the board: panel fill, trace hairline, corner pads. */
export function Card({
  children,
  className = "",
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <div
      className={`etched rounded-xl border border-cairn-trace bg-cairn-panel p-4 shadow-trace ${className}`}
    >
      {children}
    </div>
  );
}

export function Screen({
  title,
  children,
  action,
}: {
  title: string;
  children: ReactNode;
  action?: ReactNode;
}) {
  return (
    <div className="mx-auto min-h-full w-full max-w-2xl px-4 pb-28 pt-4">
      <header className="app-chrome mb-4 flex items-center justify-between gap-2">
        <h1 className="glow flex items-center gap-2 text-xl font-semibold uppercase tracking-[0.18em] text-cairn-neon">
          <span
            aria-hidden
            className="inline-block h-1.5 w-1.5 animate-pad-pulse rounded-full bg-cairn-neon"
          />
          {title}
        </h1>
        {action}
      </header>
      {children}
    </div>
  );
}

export function EmptyHint({ children }: { children: ReactNode }) {
  return (
    <p className="rounded-xl border border-dashed border-cairn-trace px-4 py-8 text-center text-cairn-dim">
      {children}
    </p>
  );
}

export function ErrorNote({ children }: { children: ReactNode }) {
  return (
    <p className="rounded-lg border border-cairn-danger bg-cairn-danger/15 px-3 py-2 text-sm text-cairn-danger-ink">
      {children}
    </p>
  );
}
