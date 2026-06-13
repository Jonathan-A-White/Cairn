import { NavLink, Outlet } from "react-router-dom";

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
      <Outlet />
      <nav className="bottom-nav app-chrome fixed inset-x-0 bottom-0 z-10 flex border-t border-gray-200 bg-white">
        {tabs.map((tab) => (
          <NavLink
            key={tab.to}
            to={tab.to}
            end={tab.end}
            className={({ isActive }) =>
              `flex flex-1 flex-col items-center py-2 text-xs ${
                isActive ? "font-semibold text-cairn-ink" : "text-gray-500"
              }`
            }
          >
            {tab.label}
          </NavLink>
        ))}
      </nav>
    </div>
  );
}
