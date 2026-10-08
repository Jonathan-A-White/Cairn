import { NavLink, Outlet } from "react-router-dom";
import { UpdateBanner } from "./UpdateBanner";

const tabs = [
  { to: "/", label: "Home", end: true },
  { to: "/search", label: "Search", end: false },
  { to: "/trips", label: "Trips", end: false },
  { to: "/people", label: "People", end: false },
  { to: "/settings", label: "Settings", end: false },
];

export function Layout() {
  return (
    <div className="min-h-full">
      <UpdateBanner />
      <Outlet />
      {/* The nav reads as a board edge connector: a lit bus along the top rule,
          each tab a contact finger that energises when active. */}
      <nav className="bottom-nav app-chrome fixed inset-x-0 bottom-0 z-10 flex border-t border-cairn-trace bg-cairn-panel">
        <span
          aria-hidden
          className="pointer-events-none absolute inset-x-0 -top-px h-px bg-gradient-to-r from-transparent via-cairn-neon to-transparent opacity-60"
        />
        {tabs.map((tab) => (
          <NavLink
            key={tab.to}
            to={tab.to}
            end={tab.end}
            className={({ isActive }) =>
              `relative flex flex-1 flex-col items-center gap-1 py-2 text-[0.65rem] uppercase tracking-[0.15em] transition-colors ${
                isActive
                  ? "glow font-semibold text-cairn-neon"
                  : "text-cairn-dim"
              }`
            }
          >
            {({ isActive }) => (
              <>
                <span
                  aria-hidden
                  className={`h-1 w-1 rounded-full transition-all ${
                    isActive
                      ? "animate-pad-pulse bg-cairn-neon shadow-emit"
                      : "bg-cairn-trace"
                  }`}
                />
                {tab.label}
              </>
            )}
          </NavLink>
        ))}
      </nav>
    </div>
  );
}
