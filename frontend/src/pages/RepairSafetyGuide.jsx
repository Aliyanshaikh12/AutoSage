import { RecommendedChecks } from "../components/Evidence.jsx";

const GENERAL = [
  "Park on level ground, set the parking brake, and chock the wheels before inspecting anything.",
  "Let the engine and cooling system cool fully before touching the radiator, hoses, or exhaust.",
  "Never work under a vehicle supported only by a jack — use rated axle stands.",
  "Disconnect the negative battery terminal before working on starter or charging wiring.",
  "Do not drive the vehicle if braking feels abnormal, steering is unstable, or a fuel leak is present.",
  "If you are unsure about any check, stop and consult a qualified mechanic.",
];

export default function RepairSafetyGuide({ match, diagnosisResult, onBack }) {
  const matches = match ? [match] : diagnosisResult?.matches || [];
  return (
    <div className="w-full px-space-md md:px-space-lg py-space-md flex flex-col gap-space-lg max-w-[1100px] mx-auto">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-space-md">
        <h1 className="font-headline-lg text-headline-lg text-on-surface tracking-tight uppercase">Inspection &amp; Safety Guide</h1>
        <button type="button" onClick={onBack} className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-lg bg-surface-container hover:bg-surface-container-high text-on-surface font-headline-sm text-body-md self-start">
          <span className="material-symbols-outlined text-[18px]">arrow_back</span>Back
        </button>
      </div>

      <section className="bg-surface-container-lowest rounded-xl shadow-sm p-space-md">
        <h2 className="font-label-caps text-label-caps text-on-surface-variant mb-space-sm">GENERAL SAFETY PRECAUTIONS</h2>
        <ul className="space-y-2">
          {GENERAL.map((g) => (
            <li key={g} className="flex gap-space-xs text-[13px] text-on-surface">
              <span className="material-symbols-outlined text-primary text-[18px]">shield</span>
              {g}
            </li>
          ))}
        </ul>
        {diagnosisResult?.safety_note && (
          <p className="mt-space-sm rounded-lg bg-error-container/60 text-on-error-container p-space-sm text-[13px]">
            {diagnosisResult.safety_note}
          </p>
        )}
      </section>

      {matches.map((m) => (
        <section key={m.rule_id} className="bg-surface-container-lowest rounded-xl shadow-sm p-space-md">
          <h2 className="font-headline-sm text-headline-sm text-on-surface">{m.title || m.possible_fault}</h2>
          <p className="font-mono text-[11px] text-on-surface-variant mb-space-sm">{m.rule_id}</p>
          <RecommendedChecks steps={m.diagnosis_steps} />
          {m.safety_warning && <p className="mt-space-sm text-[12px] text-error">{m.safety_warning}</p>}
        </section>
      ))}

      <p className="font-body-sm text-[11px] text-on-surface-variant">
        Inspection steps come from the Automotive Faults Dataset (Obike &amp; Obot, CC BY 4.0). The general
        precautions above are standard workshop practice. Auto Sage does not provide repair costs or part numbers.
      </p>
    </div>
  );
}
