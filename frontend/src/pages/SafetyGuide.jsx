import { useState } from "react";

const SAFETY_SECTIONS = [
  {
    id: "braking",
    title: "Braking & Hydraulic Control Subsystem",
    icon: "disc_full",
    riskLevel: "Critical",
    summary:
      "Braking anomalies represent the highest immediate life-safety hazard. Any loss of pedal resistance or fluid pressure compromises stopping distance.",
    rules: [
      {
        hazard: "Sinking Brake Pedal (Internal Master Cylinder Bypass)",
        risk: "Critical",
        directive:
          "CEASE DRIVING IMMEDIATELY. If the brake pedal slowly creeps to the floorboard at a stoplight, the primary or secondary piston cup has ruptured. Do not drive to a shop; arrange a flatbed tow truck.",
      },
      {
        hazard: "Hard Brake Pedal (Loss of Vacuum Assist)",
        risk: "High",
        directive:
          "Stopping distance will increase by 300% to 400%. If driving is unavoidable to clear traffic, apply heavy continuous two-foot pressure and downshift transmission. Do not exceed 25 km/h.",
      },
      {
        hazard: "Brake Fluid Handling Precautions",
        risk: "Moderate",
        directive:
          "DOT 3/4 brake fluid is glycol-based and strips automotive paint instantly upon contact. It is hygroscopic (absorbs moisture). Wear nitrile gloves and eye protection; flush splashes immediately with cold water.",
      },
    ],
  },
  {
    id: "steering",
    title: "Steering, Suspension & Tire Dynamics",
    icon: "tire_repair",
    riskLevel: "Critical",
    summary:
      "Steering instability or catastrophic joint failure can cause sudden departure from the roadway at highway speeds.",
    rules: [
      {
        hazard: "Excessive Steering Free Play or Tie Rod Slop",
        risk: "Critical",
        directive:
          "If steering wheel has more than 1 inch (25 mm) of free play before road wheels turn, outer tie rod end or steering rack mounts may be detached. Do not drive at highway speeds.",
      },
      {
        hazard: "Severe Front-End Vibration / Death Wobble",
        risk: "High",
        directive:
          "Immediately decelerate smoothly without slamming on brakes. Hold steering wheel firmly with both hands. Inspect for missing lug nuts, separated tire belts, or sheared ball joint pinch bolts.",
      },
      {
        hazard: "Spring Compression Hazards",
        risk: "Critical",
        directive:
          "NEVER loosen MacPherson strut center damper nuts or coil springs without a commercial wall-mounted hydraulic spring compressor. Stored kinetic energy can cause fatal trauma.",
      },
    ],
  },
  {
    id: "overheating",
    title: "Engine Overheating & Thermal Hazards",
    icon: "thermostat",
    riskLevel: "High",
    summary:
      "Operating an overheated engine causes warped aluminum cylinder heads, blown head gaskets, and permanent cylinder wall scoring.",
    rules: [
      {
        hazard: "High-Pressure Scalding Steam Release",
        risk: "Critical",
        directive:
          "NEVER open a radiator cap or pressurized coolant expansion tank on a hot engine! Pressurized coolant can exceed 120°C (250°F) and will flash to steam instantly, causing severe 3rd-degree burns.",
      },
      {
        hazard: "Temperature Gauge in the Red Zone",
        risk: "High",
        directive:
          "Pull over safely within 60 seconds, turn off engine, but leave ignition ON so electric cooling fans can dissipate convective heat soak. Turn cabin heater to maximum heat and blower to full to assist cooling.",
      },
      {
        hazard: "Cold Water Addition to Hot Block",
        risk: "Moderate",
        directive:
          "Never pour cold water into an overheated engine cooling system. Thermal shock will immediately crack the cast iron or aluminum engine block.",
      },
    ],
  },
  {
    id: "fuel",
    title: "Fuel Delivery & Flammable Vapor Hazards",
    icon: "local_gas_station",
    riskLevel: "Critical",
    summary:
      "Automotive gasoline and pressurized direct-injection rails operate up to 2,500 psi and ignite readily from static sparks.",
    rules: [
      {
        hazard: "Fuel Odor or Active Puddle Under Vehicle",
        risk: "Critical",
        directive:
          "SHUT OFF ENGINE IMMEDIATELY. Do not use cell phones, key fobs, or operate electric switches near the vehicle. Gasoline vapors are heavier than air and collect near ground level.",
      },
      {
        hazard: "Gasoline Direct Injection (GDI) High-Pressure Rails",
        risk: "Critical",
        directive:
          "GDI fuel rails operate between 500 and 2,500 psi (35 to 170 bar). High-pressure liquid fuel injection into skin causes severe tissue necrosis. Always relieve fuel pressure before loosening fittings.",
      },
    ],
  },
  {
    id: "electrical",
    title: "Battery, Alternator & High-Voltage Systems",
    icon: "bolt",
    riskLevel: "High",
    summary:
      "12V lead-acid batteries emit explosive hydrogen gas, while hybrid/EV traction batteries carry lethal 400V to 800V DC voltages.",
    rules: [
      {
        hazard: "Lead-Acid Battery Hydrogen Explosion Risk",
        risk: "High",
        directive:
          "Charging batteries release hydrogen and oxygen gas. Always connect jumper cables positive-to-positive first, and connect the final ground clamp to unpainted engine metal AWAY from the battery.",
      },
      {
        hazard: "High-Voltage Orange Cables (Hybrid / EV)",
        risk: "Critical",
        directive:
          "NEVER touch, probe, or cut bright ORANGE high-voltage wiring harnesses. Voltages exceeding 60V DC are considered lethal. High-voltage servicing requires Class 0 (1,000V rated) insulating gloves.",
      },
      {
        hazard: "Wrench Short Circuit Across Battery Terminals",
        risk: "Moderate",
        directive:
          "Remove rings, watches, and metal jewelry before working near the battery. A short circuit will heat metal red-hot in 2 seconds, causing deep contact burns.",
      },
    ],
  },
  {
    id: "warnings",
    title: "Instrument Cluster Warnings & Triage Directives",
    icon: "warning",
    riskLevel: "High",
    summary:
      "Dashboard indicator lamps communicate immediate urgency through standardized ISO colors: Red (Stop), Amber (Caution), and Green/Blue (Informational).",
    rules: [
      {
        hazard: "Flashing Check Engine Light (Active Catalytic Damage)",
        risk: "High",
        directive:
          "A flashing MIL indicates severe unburned fuel misfires entering the catalytic converter. Catalytic temperatures can exceed 900°C, causing underbody fire. Reduce speed and stop driving.",
      },
      {
        hazard: "Red Oil Pressure Warning Lamp",
        risk: "Critical",
        directive:
          "STOP ENGINE IMMEDIATELY within 10 seconds. Red oil lamp indicates zero hydrodynamic oil pressure to crankshaft bearings. Continued operation destroys engine within 60 seconds.",
      },
      {
        hazard: "Red Brake System Warning Lamp",
        risk: "Critical",
        directive:
          "Indicates dangerously low brake fluid level or hydraulic circuit pressure imbalance. Test pedal feel carefully; do not drive if pedal feels spongy or sinks.",
      },
    ],
  },
];

export default function SafetyGuide({ onBack }) {
  const [activeSection, setActiveSection] = useState("all");

  const visibleSections =
    activeSection === "all"
      ? SAFETY_SECTIONS
      : SAFETY_SECTIONS.filter((s) => s.id === activeSection);

  return (
    <div className="w-full px-space-md md:px-space-lg py-space-md flex flex-col gap-space-lg max-w-[1400px] mx-auto pb-24">
      {/* Header */}
      <section className="bg-surface-container-lowest rounded-xl shadow-sm p-space-md md:p-space-lg border border-surface-container">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-space-sm pb-space-sm border-b border-surface-container">
          <div>
            <div className="flex items-center gap-2 text-primary font-label-caps text-xs tracking-wider uppercase mb-1">
              <span className="material-symbols-outlined text-[18px]">health_and_safety</span>
              <span>Automotive Workshop Standards</span>
            </div>
            <h1 className="font-headline-lg text-2xl md:text-3xl font-extrabold text-on-surface uppercase tracking-tight">
              Vehicle Inspection &amp; Workshop Safety Guide
            </h1>
          </div>
          {onBack && (
            <button
              type="button"
              onClick={onBack}
              className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-lg bg-surface-container hover:bg-surface-container-high text-on-surface font-headline-sm text-xs self-start sm:self-auto"
            >
              <span className="material-symbols-outlined text-[16px]">arrow_back</span>
              <span>Back to Previous Page</span>
            </button>
          )}
        </div>

        <p className="mt-space-sm text-on-surface-variant text-sm md:text-base leading-relaxed max-w-4xl">
          Automotive diagnosis involves mechanical, hydraulic, high-temperature, and electrical hazards.
          This guide formalizes standardized workshop safety protocols across all 8 supported vehicle subsystems
          to prevent personal injury and avoid accidental vehicle damage.
        </p>

        {/* Risk Level Legend */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 mt-space-md">
          <div className="p-2.5 rounded-lg bg-red-50 text-red-950 border border-red-200 text-xs">
            <strong className="block text-red-900 font-bold uppercase text-[10px]">Critical Safety</strong>
            <span>Immediate halt of operation; flatbed tow truck recommended.</span>
          </div>
          <div className="p-2.5 rounded-lg bg-amber-50 text-amber-950 border border-amber-200 text-xs">
            <strong className="block text-amber-900 font-bold uppercase text-[10px]">High Risk</strong>
            <span>Severe mechanical damage or partial loss of control risk.</span>
          </div>
          <div className="p-2.5 rounded-lg bg-yellow-50 text-yellow-950 border border-yellow-200 text-xs">
            <strong className="block text-yellow-900 font-bold uppercase text-[10px]">Moderate Risk</strong>
            <span>Inspect within 500 km; avoid aggressive driving loads.</span>
          </div>
          <div className="p-2.5 rounded-lg bg-slate-50 text-slate-900 border border-slate-200 text-xs">
            <strong className="block text-slate-700 font-bold uppercase text-[10px]">Low Risk</strong>
            <span>Address during next scheduled oil/filter service.</span>
          </div>
        </div>
      </section>

      {/* Subsystem filter tabs */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-1 no-print">
        <button
          type="button"
          onClick={() => setActiveSection("all")}
          className={`px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition-all ${
            activeSection === "all"
              ? "bg-primary-container text-on-primary"
              : "bg-surface-container text-on-surface hover:bg-surface-container-high"
          }`}
        >
          All Subsystems ({SAFETY_SECTIONS.length})
        </button>
        {SAFETY_SECTIONS.map((sec) => (
          <button
            key={sec.id}
            type="button"
            onClick={() => setActiveSection(sec.id)}
            className={`px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition-all flex items-center gap-1 ${
              activeSection === sec.id
                ? "bg-primary-container text-on-primary"
                : "bg-surface-container text-on-surface hover:bg-surface-container-high"
            }`}
          >
            <span className="material-symbols-outlined text-[14px]">{sec.icon}</span>
            <span>{sec.title.split("&")[0].trim()}</span>
          </button>
        ))}
      </div>

      {/* Safety Section Cards */}
      <div className="space-y-space-md">
        {visibleSections.map((sec) => (
          <article
            key={sec.id}
            className="bg-surface-container-lowest rounded-xl shadow-sm p-space-md md:p-space-lg border border-surface-container"
          >
            <div className="flex items-start justify-between gap-3 border-b border-surface-container pb-2 mb-3">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-lg bg-primary/10 text-primary flex items-center justify-center shrink-0">
                  <span className="material-symbols-outlined text-[20px]">{sec.icon}</span>
                </div>
                <div>
                  <h2 className="text-base md:text-lg font-bold text-on-surface">{sec.title}</h2>
                  <p className="text-xs text-on-surface-variant">{sec.summary}</p>
                </div>
              </div>
              <span
                className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase shrink-0 border ${
                  sec.riskLevel === "Critical"
                    ? "bg-red-100 text-red-800 border-red-300"
                    : "bg-amber-100 text-amber-800 border-amber-300"
                }`}
              >
                {sec.riskLevel} Priority
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-space-sm">
              {sec.rules.map((rule, idx) => (
                <div
                  key={idx}
                  className="p-space-sm rounded-lg bg-surface-container-low border border-surface-container flex flex-col justify-between"
                >
                  <div>
                    <div className="flex items-center justify-between gap-2 mb-1">
                      <strong className="text-xs font-bold text-on-surface">{rule.hazard}</strong>
                      <span
                        className={`text-[9px] font-bold uppercase px-1.5 py-0.2 rounded shrink-0 ${
                          rule.risk === "Critical"
                            ? "bg-red-200 text-red-900"
                            : rule.risk === "High"
                            ? "bg-amber-200 text-amber-900"
                            : "bg-slate-200 text-slate-800"
                        }`}
                      >
                        {rule.risk}
                      </span>
                    </div>
                    <p className="text-xs text-on-surface-variant leading-relaxed">{rule.directive}</p>
                  </div>
                </div>
              ))}
            </div>
          </article>
        ))}
      </div>

      {/* General Golden Rules Card */}
      <section className="bg-surface-container-low rounded-xl p-space-md border border-surface-container text-xs text-on-surface-variant space-y-2">
        <h3 className="font-bold text-on-surface text-sm flex items-center gap-1.5">
          <span className="material-symbols-outlined text-primary text-[18px]">verified</span>
          General Automotive Workshop Golden Rules
        </h3>
        <ul className="grid grid-cols-1 md:grid-cols-2 gap-2 list-disc pl-4">
          <li>Park on level ground, set parking brake firmly, and chock the wheels before lifting.</li>
          <li>Never work beneath a vehicle supported only by a hydraulic jack; always use rated jack stands.</li>
          <li>Disconnect the negative battery terminal before servicing starter or alternator wiring.</li>
          <li>Always wear ANSI Z87.1 certified eye protection when working near battery acid or underbody rust.</li>
          <li>Use properly calibrated torque wrenches on wheel lug nuts, caliper bolts, and head bolts.</li>
          <li>If any diagnostic step is outside your mechanical expertise, escalate to an ASE Master Technician.</li>
        </ul>
      </section>
    </div>
  );
}
