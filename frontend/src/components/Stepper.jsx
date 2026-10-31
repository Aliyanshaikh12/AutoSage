export default function Stepper({ currentStep = 1, onStepClick }) {
  const steps = [
    { number: 1, id: "01", label: "Vehicle Info", page: "vehicle" },
    { number: 2, id: "02", label: "Symptoms", page: "symptoms" },
    { number: 3, id: "03", label: "Diagnostic Inquiry", page: "questions" },
    { number: 4, id: "04", label: "Diagnosis Results", page: "results" },
    { number: 5, id: "05", label: "Report & Resolution", page: "report" },
  ];

  return (
    <section className="w-full bg-surface-container-lowest rounded-2xl p-2.5 sm:p-3 shadow-sm no-print mb-4 border border-surface-container">
      <div className="flex sm:grid sm:grid-cols-5 gap-2 overflow-x-auto scrollbar-none pb-1 sm:pb-0">
        {steps.map((s) => {
          const isActive = s.number === currentStep;
          const isCompleted = s.number < currentStep;
          const isClickable = isCompleted && onStepClick;

          let containerClass = "bg-surface-container-low text-on-surface-variant border border-transparent";
          let badgeClass = "bg-surface-container-high text-on-surface-variant";
          let labelCaps = "text-outline";

          if (isActive) {
            containerClass = "bg-primary/10 text-on-surface relative overflow-hidden border border-primary/30 shadow-xs";
            badgeClass = "bg-primary text-on-primary shadow-sm";
            labelCaps = "text-primary font-bold";
          } else if (isCompleted) {
            containerClass = "bg-surface-container-low text-on-surface hover:bg-surface-container cursor-pointer transition-colors border border-surface-container";
            badgeClass = "bg-emerald-100 text-emerald-800";
            labelCaps = "text-emerald-700 font-semibold";
          }

          return (
            <div
              key={s.id}
              onClick={() => isClickable && onStepClick(s.page)}
              className={`flex items-center gap-2.5 p-2 sm:p-2.5 rounded-xl transition-all shrink-0 min-w-[145px] sm:min-w-0 ${containerClass}`}
              role={isClickable ? "button" : undefined}
              tabIndex={isClickable ? 0 : undefined}
            >
              <div
                className={`w-7 h-7 sm:w-8 sm:h-8 rounded-lg flex items-center justify-center shrink-0 text-xs font-bold ${badgeClass}`}
              >
                {isCompleted ? (
                  <span className="material-symbols-outlined text-[16px]">check</span>
                ) : (
                  s.id
                )}
              </div>
              <div className="min-w-0 flex-1">
                <span className={`block text-[10px] uppercase tracking-wider ${labelCaps}`}>
                  {isActive ? "Current" : isCompleted ? "Completed" : `Step ${s.number}`}
                </span>
                <span className="block text-xs sm:text-[13px] truncate font-semibold">
                  {s.label}
                </span>
              </div>
              {isActive && (
                <div className="absolute right-0 top-0 bottom-0 w-1 bg-primary" />
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
}
