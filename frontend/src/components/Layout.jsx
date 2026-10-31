import { useEffect, useState } from "react";
import { vehicleLabel } from "../stitch/dom.js";

const NAV_ITEMS = [
  { page: "dashboard", path: "dashboard", icon: "speed", title: "Dashboard" },
  { page: "vehicle", path: "vehicle", icon: "directions_car", title: "Vehicle Information" },
  { page: "symptoms", path: "diagnosis", icon: "troubleshoot", title: "Start Diagnosis" },
  { page: "history", path: "history", icon: "history", title: "Diagnosis History" },
  { page: "safety_guide", path: "safety-guide", icon: "health_and_safety", title: "Safety Guide" },
];

const ACTIVE_CLASS =
  "bg-primary-container text-on-primary shadow-[0_4px_12px_rgba(37,99,235,0.25)]";
const INACTIVE_CLASS =
  "text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface transition-all";

export default function Layout({
  page,
  setPage,
  vehicle,
  historyCount = 0,
  onSearch,
  toast,
  onToast,
  children,
}) {
  const [searchValue, setSearchValue] = useState("");
  const [localToast, setLocalToast] = useState(null);

  useEffect(() => {
    if (!toast) return undefined;
    setLocalToast(toast);
    const timer = setTimeout(() => setLocalToast(null), 4200);
    return () => clearTimeout(timer);
  }, [toast]);

  const showToast = (message) => {
    if (onToast) onToast(message);
    else setLocalToast(message);
  };

  const navigate = (nextPage) => {
    if (nextPage) setPage(nextPage);
  };

  const submitSearch = (event) => {
    if (event.key !== "Enter") return;
    event.preventDefault();
    const query = searchValue.trim();
    if (query) {
      onSearch?.(query);
      setPage("symptoms");
    }
  };

  return (
    <>
      <aside className="fixed left-0 top-0 h-full w-20 bg-surface-container-lowest z-50 hidden md:flex flex-col items-center py-space-md shadow-[0_1px_8px_rgba(0,0,0,0.04)] justify-between no-print">
        <div className="flex flex-col items-center w-full gap-space-lg">
          <button
            className="flex items-center justify-center w-12 h-12 rounded-xl bg-primary text-on-primary shadow-[0_4px_12px_rgba(0,74,198,0.25)]"
            type="button"
            onClick={() => navigate("dashboard")}
            title="Auto Sage home"
            aria-label="Auto Sage home"
          >
            <span className="material-symbols-outlined text-[28px]">token</span>
          </button>
          <nav
            className="flex flex-col items-center gap-space-sm w-full px-space-xs"
            aria-label="Primary"
          >
            {NAV_ITEMS.map((item) => {
              const active = item.page === page;
              return (
                <a
                  key={item.path}
                  aria-current={active ? "page" : undefined}
                  className={`group relative flex items-center justify-center w-12 h-12 rounded-xl transition-all ${
                    active ? ACTIVE_CLASS : INACTIVE_CLASS
                  }`}
                  href={`#${item.path}`}
                  title={item.title}
                  onClick={(event) => {
                    event.preventDefault();
                    navigate(item.page);
                  }}
                >
                  <span className="material-symbols-outlined text-[22px]">{item.icon}</span>
                  {item.page === "history" && historyCount > 0 && (
                    <span className="absolute -right-1 -top-1 min-w-[17px] h-[17px] px-1 rounded-full bg-primary text-on-primary text-[9px] font-bold flex items-center justify-center">
                      {historyCount > 9 ? "9+" : historyCount}
                    </span>
                  )}
                </a>
              );
            })}
          </nav>
        </div>
        <div className="flex flex-col items-center w-full pb-space-xs">
          <div
            className="flex items-center justify-center w-10 h-10 rounded-xl text-on-surface-variant hover:text-primary transition-colors cursor-default"
            title="Auto Sage Local KBS Engine Active"
          >
            <span className="material-symbols-outlined text-[20px]">verified_user</span>
          </div>
        </div>
      </aside>

      <div className="md:pl-20 pb-16 md:pb-0">
        <header className="fixed top-0 left-0 md:left-20 right-0 h-16 bg-surface-container-lowest/90 backdrop-blur-xl z-40 shadow-[0_1px_8px_rgba(0,0,0,0.04)] no-print">
          <div className="h-16 w-full px-space-lg flex items-center justify-between gap-space-md">
            <div className="flex items-center gap-space-lg min-w-0">
              <button
                className="flex items-center gap-space-sm px-space-md py-space-xs bg-surface-container-low rounded-lg hover:bg-surface-container transition-colors"
                type="button"
                onClick={() => navigate("vehicle")}
                title="Vehicle details"
              >
                <span className="material-symbols-outlined text-primary text-[20px]">
                  directions_car
                </span>
                <span className="font-headline-sm text-headline-sm text-on-surface truncate max-w-[15rem]">
                  {vehicleLabel(vehicle)}
                </span>
                <span className="material-symbols-outlined text-on-surface-variant text-[18px]">
                  expand_more
                </span>
              </button>
              <div className="h-6 w-px bg-surface-variant hidden md:block shrink-0" />
              <span className="font-headline-sm text-headline-sm text-on-surface-variant truncate hidden lg:inline-block">
                Auto Sage Diagnostic Studio
              </span>
            </div>
            <div className="flex items-center gap-space-md shrink-0">
              <div className="relative flex items-center hidden sm:flex">
                <span className="material-symbols-outlined absolute left-3 text-on-surface-variant text-[18px] pointer-events-none">
                  search
                </span>
                <input
                  className="w-64 lg:w-80 h-9 pl-9 pr-space-md rounded-full bg-surface-container-low text-body-sm font-body-sm text-on-surface placeholder:text-on-surface-variant focus:outline-none focus:bg-surface-container-lowest focus:ring-2 focus:ring-primary/20 transition-all"
                  placeholder="Search symptoms or faults..."
                  type="text"
                  value={searchValue}
                  onChange={(event) => setSearchValue(event.target.value)}
                  onKeyDown={submitSearch}
                  aria-label="Search symptoms or faults"
                />
              </div>
              <button
                type="button"
                onClick={() => navigate("symptoms")}
                className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-primary text-on-primary font-headline-sm text-xs hover:bg-primary/90 shadow-sm transition-all"
              >
                <span className="material-symbols-outlined text-[16px]">add_circle</span>
                <span>New Diagnosis</span>
              </button>
            </div>
          </div>
        </header>

        <main className="w-full pt-16 bg-background min-h-screen">
          {children}
        </main>
      </div>

      <nav
        className="md:hidden fixed bottom-0 left-0 right-0 h-16 bg-surface-container-lowest z-50 flex items-center justify-around shadow-[0_-1px_8px_rgba(0,0,0,0.06)] no-print"
        aria-label="Mobile"
      >
        {NAV_ITEMS.filter((item) => item.page).map((item) => (
          <button
            key={item.path}
            type="button"
            title={item.title}
            aria-label={item.title}
            onClick={() => navigate(item.page)}
            className={`flex items-center justify-center w-11 h-11 rounded-xl ${
              item.page === page ? ACTIVE_CLASS : INACTIVE_CLASS
            }`}
          >
            <span className="material-symbols-outlined text-[22px]">{item.icon}</span>
          </button>
        ))}
      </nav>

      {localToast && (
        <div className="fixed bottom-5 right-5 z-[80] max-w-sm rounded-xl bg-inverse-surface text-inverse-on-surface px-space-md py-space-sm shadow-xl flex items-start gap-space-sm no-print">
          <span className="material-symbols-outlined text-primary-fixed text-[20px]">
            info
          </span>
          <span className="font-body-sm text-body-sm leading-relaxed">{localToast}</span>
          <button
            type="button"
            className="text-inverse-on-surface/70 hover:text-inverse-on-surface"
            onClick={() => setLocalToast(null)}
            aria-label="Dismiss message"
          >
            <span className="material-symbols-outlined text-[18px]">close</span>
          </button>
        </div>
      )}
    </>
  );
}
