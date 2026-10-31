export default function Stepper({ currentStep = 1, onStepClick }) {
  const steps = [
    { number: 1, id: "01", label: "Vehicle Info", page: "vehicle" },
    { number: 2, id: "02", label: "Symptoms", page: "symptoms" },
    { number: 3, id: "03", label: "Follow-Up Questions", page: "questions" },
    { number: 4, id: "04", label: "Diagnosis Results", page: "results" },
    { number: 5, id: "05", label: "Report & Resolution", page: "report" },
  ];

  return (
    <section className="w-full bg-surface-container-lowest rounded-xl p-space-sm md:p-space-md shadow-sm no-print mb-space-md">
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-space-sm relative">
        {steps.map((s) => {
          const isActive = s.number === currentStep;
          const isCompleted = s.number < currentStep;
          const isClickable = isCompleted && onStepClick;

          let containerClass = "bg-surface-container-low text-on-surface-variant";
          let badgeClass = "bg-surface-container-high text-on-surface-variant";
          let labelCaps = "text-outline";

          if (isActive) {
            containerClass = "bg-primary-fixed/30 text-on-surface relative overflow-hidden border border-primary/20";
            badgeClass = "bg-primary-container text-on-primary shadow-sm";
            labelCaps = "text-primary font-bold";
          } else if (isCompleted) {
            containerClass = "bg-surface-container-low text-on-surface hover:bg-surface-container cursor-pointer transition-colors";
            badgeClass = "bg-primary/20 text-primary";
            labelCaps = "text-on-surface-variant font-medium";
          }

          return (
            <div
              key={s.id}
              onClick={() => isClickable && onStepClick(s.page)}
              className={`flex items-center gap-space-sm p-space-sm rounded-lg transition-all ${containerClass}`}
              role={isClickable ? "button" : undefined}
              tabIndex={isClickable ? 0 : undefined}
            >
              <div
                className={`w-9 h-9 rounded-lg flex items-center justify-center shrink-0 font-headline-sm text-[13px] ${badgeClass}`}
              >
                {isCompleted ? (
                  <span className="material-symbols-outlined text-[18px]">check</span>
                ) : (
                  s.id
                )}
              </div>
              <div className="min-w-0">
                <span className={`block font-label-caps text-[10px] uppercase tracking-wider ${labelCaps}`}>
                  {isActive ? "Active Step" : isCompleted ? "Completed" : `Step ${s.number}`}
                </span>
                <span className="block font-headline-sm text-[13px] truncate font-semibold">
                  {s.label}
                </span>
              </div>
              {isActive && (
                <div className="absolute right-0 top-0 bottom-0 w-1 bg-primary-container" />
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
}
