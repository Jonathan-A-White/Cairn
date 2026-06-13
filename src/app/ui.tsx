import type {
  ButtonHTMLAttributes,
  InputHTMLAttributes,
  ReactNode,
  TextareaHTMLAttributes,
} from "react";

type Variant = "primary" | "secondary" | "ghost" | "danger";

const variants: Record<Variant, string> = {
  primary: "bg-cairn-ink text-white",
  secondary: "bg-white text-cairn-ink border border-gray-300",
  ghost: "bg-transparent text-cairn-ink",
  danger: "bg-red-600 text-white",
};

export function Button({
  variant = "primary",
  className = "",
  children,
  ...rest
}: ButtonHTMLAttributes<HTMLButtonElement> & { variant?: Variant }) {
  return (
    <button
      className={`rounded-lg px-4 py-2 font-medium tap-hover active:opacity-80 disabled:opacity-40 ${variants[variant]} ${className}`}
      {...rest}
    >
      {children}
    </button>
  );
}

export function TextInput(props: InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      {...props}
      className={`w-full rounded-lg border border-gray-300 px-3 py-2 outline-none focus:border-cairn-ink ${props.className ?? ""}`}
    />
  );
}

export function TextArea(props: TextareaHTMLAttributes<HTMLTextAreaElement>) {
  return (
    <textarea
      {...props}
      className={`w-full rounded-lg border border-gray-300 px-3 py-2 outline-none focus:border-cairn-ink ${props.className ?? ""}`}
    />
  );
}

export function Card({
  children,
  className = "",
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <div className={`rounded-xl bg-white p-4 shadow-sm ${className}`}>
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
        <h1 className="text-xl font-semibold text-cairn-ink">{title}</h1>
        {action}
      </header>
      {children}
    </div>
  );
}

export function EmptyHint({ children }: { children: ReactNode }) {
  return <p className="py-8 text-center text-gray-500">{children}</p>;
}

export function ErrorNote({ children }: { children: ReactNode }) {
  return (
    <p className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">
      {children}
    </p>
  );
}
