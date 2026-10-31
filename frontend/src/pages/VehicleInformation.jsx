import { useEffect, useMemo, useState } from "react";
import Stepper from "../components/Stepper.jsx";
import { vehicleLabel, vehicleSecondary } from "../stitch/dom.js";

const PROFILE_KEY = "auto_sage_vehicle_profiles";
const ENERGY_TYPES = [
  "Gasoline",
  "Diesel",
  "Hybrid",
  "Plug-in hybrid",
  "Battery electric",
  "Other / not sure",
];
const TRANSMISSIONS = [
  "Automatic",
  "Manual",
  "CVT",
  "Dual-clutch",
  "Other / not sure",
];

function readProfiles() {
  try {
    const parsed = JSON.parse(localStorage.getItem(PROFILE_KEY) || "[]");
    return Array.isArray(parsed) ? parsed.filter((item) => item && item.make && item.model) : [];
  } catch {
    return [];
  }
}

function emptyVehicle(initial) {
  return {
    year: initial?.year || "",
    make: initial?.make || "",
    model: initial?.model || "",
    engine: initial?.engine || "",
    energy: initial?.energy || "Gasoline",
    transmission: initial?.transmission || "Automatic",
    odometer: initial?.odometer || "",
  };
}

export default function VehicleInformation({ initialVehicle, onComplete, onSkip, onBack }) {
  const [vehicle, setVehicle] = useState(() => emptyVehicle(initialVehicle));
  const [profiles, setProfiles] = useState(readProfiles);
  const [error, setError] = useState("");

  useEffect(() => {
    setVehicle(emptyVehicle(initialVehicle));
  }, [initialVehicle]);

  const maxValidYear = new Date().getFullYear() + 1;
  const yearNumber = Number(vehicle.year);
  const isYearValid =
    String(vehicle.year).trim() &&
    Number.isInteger(yearNumber) &&
    yearNumber >= 1950 &&
    yearNumber <= maxValidYear;

  const canContinue = useMemo(
    () => vehicle.make.trim() && vehicle.model.trim() && isYearValid,
    [vehicle, isYearValid]
  );

  const update = (field) => (event) => {
    setVehicle((current) => ({ ...current, [field]: event.target.value }));
    setError("");
  };

  const saveProfile = () => {
    if (!canContinue) return;
    const next = [
      vehicle,
      ...profiles.filter(
        (item) =>
          !(
            item.make === vehicle.make &&
            item.model === vehicle.model &&
            String(item.year) === String(vehicle.year)
          )
      ),
    ].slice(0, 6);
    setProfiles(next);
    try {
      localStorage.setItem(PROFILE_KEY, JSON.stringify(next));
    } catch {
      // The active form still works if profile storage is blocked.
    }
  };

  const submit = (event) => {
    event.preventDefault();
    if (!canContinue) {
      if (!vehicle.make.trim() || !vehicle.model.trim()) {
        setError("Make and model are required before saving.");
      } else if (!isYearValid) {
        setError(`Please enter a valid 4-digit model year between 1950 and ${maxValidYear}.`);
      } else {
        setError("Make, model, and valid model year are required.");
      }
      return;
    }
    const cleaned = {
      ...vehicle,
      year: String(vehicle.year).trim(),
      make: vehicle.make.trim(),
      model: vehicle.model.trim(),
      engine: vehicle.engine.trim(),
      odometer: String(vehicle.odometer).trim(),
    };
    saveProfile();
    onComplete(cleaned);
  };

  return (
    <div className="w-full p-space-lg max-w-[1500px] mx-auto flex flex-col gap-space-lg">
      <Stepper currentStep={1} />

      <div className="flex flex-col md:flex-row md:items-end justify-between gap-space-md">
        <div className="space-y-space-xs">
          <div className="flex items-center gap-space-xs text-body-sm text-on-surface-variant">
            <span>Diagnostics</span>
            <span className="material-symbols-outlined text-[16px]">chevron_right</span>
            <span className="text-primary font-headline-sm">Vehicle Information</span>
          </div>
          <h1 className="font-headline-lg text-headline-lg text-on-surface tracking-tight uppercase">
            Vehicle Information
          </h1>
          <p className="font-body-md text-body-md text-on-surface-variant max-w-2xl">
            Vehicle details label this local session and its report. The KBS evaluates
            observable symptoms against diagnostic rules across automotive systems.
          </p>
        </div>
        <div className="flex items-center gap-space-sm">
          {onSkip && (
            <button
              className="inline-flex items-center gap-space-xs px-space-md py-space-xs rounded-xl bg-surface-container text-on-surface text-body-md font-headline-sm shadow-sm hover:bg-surface-container-high transition-all"
              type="button"
              onClick={onSkip}
            >
              Skip vehicle details
              <span className="material-symbols-outlined text-[18px]">skip_next</span>
            </button>
          )}
          <button
            className="inline-flex items-center gap-space-xs px-space-md py-space-xs rounded-xl bg-surface-container-lowest text-on-surface text-body-md font-headline-sm shadow-sm hover:bg-surface-container transition-all"
            type="button"
            onClick={onBack}
          >
            <span className="material-symbols-outlined text-[18px]">arrow_back</span>
            Back
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-space-lg items-start">
        <form
          className="lg:col-span-8 bg-surface-container-lowest rounded-xl shadow-sm p-space-lg space-y-space-lg"
          onSubmit={submit}
        >
          <div className="flex items-start justify-between gap-space-md border-b border-surface-container pb-space-md">
            <div className="flex items-center gap-space-sm">
              <span className="p-2 rounded-lg bg-surface-container text-primary">
                <span className="material-symbols-outlined text-[22px]">directions_car</span>
              </span>
              <div>
                <h2 className="font-headline-md text-headline-md text-on-surface">
                  Primary Vehicle Specs
                </h2>
                <p className="font-body-sm text-body-sm text-on-surface-variant">
                  Required fields are used only as session labels.
                </p>
              </div>
            </div>
            <span className="font-label-caps text-label-caps px-2 py-1 rounded-full bg-primary-fixed text-on-primary-fixed uppercase tracking-wider">
              Required
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-space-md">
            <Field label="Vehicle Make" htmlFor="make">
              <input
                id="make"
                className="w-full h-10 px-space-sm rounded-lg bg-surface-container-low text-body-md text-on-surface focus:outline-none focus:ring-2 focus:ring-primary/20"
                placeholder="e.g. Toyota"
                value={vehicle.make}
                onChange={update("make")}
                autoComplete="organization"
              />
            </Field>
            <Field label="Vehicle Model" htmlFor="model">
              <input
                id="model"
                className="w-full h-10 px-space-sm rounded-lg bg-surface-container-low text-body-md text-on-surface focus:outline-none focus:ring-2 focus:ring-primary/20"
                placeholder="e.g. Corolla"
                value={vehicle.model}
                onChange={update("model")}
                autoComplete="off"
              />
            </Field>
            <Field label="Model Year" htmlFor="year">
              <input
                id="year"
                className="w-full h-10 px-space-sm rounded-lg bg-surface-container-low text-body-md text-on-surface focus:outline-none focus:ring-2 focus:ring-primary/20"
                placeholder="e.g. 2018"
                inputMode="numeric"
                value={vehicle.year}
                onChange={update("year")}
                autoComplete="off"
              />
            </Field>
            <Field label="Engine / Drivetrain" htmlFor="engine">
              <input
                id="engine"
                className="w-full h-10 px-space-sm rounded-lg bg-surface-container-low text-body-md text-on-surface focus:outline-none focus:ring-2 focus:ring-primary/20"
                placeholder="e.g. 2.0L I4 or AWD"
                value={vehicle.engine}
                onChange={update("engine")}
              />
            </Field>
            <Field label="Fuel / Energy Type" htmlFor="energy">
              <select
                id="energy"
                className="w-full h-10 px-space-sm rounded-lg bg-surface-container-low text-body-md text-on-surface focus:outline-none focus:ring-2 focus:ring-primary/20"
                value={vehicle.energy}
                onChange={update("energy")}
              >
                {ENERGY_TYPES.map((item) => (
                  <option key={item} value={item}>{item}</option>
                ))}
              </select>
            </Field>
            <Field label="Transmission" htmlFor="transmission">
              <select
                id="transmission"
                className="w-full h-10 px-space-sm rounded-lg bg-surface-container-low text-body-md text-on-surface focus:outline-none focus:ring-2 focus:ring-primary/20"
                value={vehicle.transmission}
                onChange={update("transmission")}
              >
                {TRANSMISSIONS.map((item) => (
                  <option key={item} value={item}>{item}</option>
                ))}
              </select>
            </Field>
            <Field label="Odometer (optional)" htmlFor="odometer">
              <input
                id="odometer"
                className="w-full h-10 px-space-sm rounded-lg bg-surface-container-low text-body-md text-on-surface focus:outline-none focus:ring-2 focus:ring-primary/20"
                placeholder="e.g. 84,000 km"
                value={vehicle.odometer}
                onChange={update("odometer")}
              />
            </Field>
          </div>

          <div className="rounded-xl bg-surface-container-low p-space-md flex items-start gap-space-sm">
            <span className="material-symbols-outlined text-primary text-[20px] mt-0.5">info</span>
            <div className="font-body-sm text-body-sm text-on-surface-variant">
              <span className="font-headline-sm text-on-surface">No vehicle bus connection.</span>{" "}
              Auto Sage does not read OBD-II, CAN, VIN, or live sensor data. Specs
              are stored locally for session labelling and reports only.
            </div>
          </div>

          {error && (
            <div className="rounded-lg bg-error-container px-space-md py-space-sm text-on-error-container font-body-sm text-body-sm">
              {error}
            </div>
          )}

          <div className="flex flex-wrap items-center justify-between gap-space-sm pt-space-xs">
            <button
              className="inline-flex items-center gap-space-xs px-space-md py-space-xs rounded-lg bg-surface-container text-on-surface text-body-md font-headline-sm hover:bg-surface-container-high transition-all"
              type="button"
              onClick={saveProfile}
              disabled={!canContinue}
            >
              <span className="material-symbols-outlined text-[18px]">bookmark_add</span>
              Save local profile
            </button>
            <div className="flex items-center gap-space-sm">
              {onSkip && (
                <button
                  className="inline-flex items-center gap-space-xs px-space-md py-space-xs rounded-lg bg-surface-container text-on-surface text-body-md font-headline-sm hover:bg-surface-container-high transition-all"
                  type="button"
                  onClick={onSkip}
                >
                  Skip
                </button>
              )}
              <button
                className="inline-flex items-center gap-space-xs px-space-md py-space-xs rounded-lg bg-surface-container-lowest text-on-surface-variant text-body-md font-headline-sm hover:bg-surface-container transition-all"
                type="button"
                onClick={onBack}
              >
                Cancel
              </button>
              <button
                className="inline-flex items-center gap-space-sm px-space-lg py-space-sm rounded-full bg-primary-container text-on-primary text-body-md font-headline-sm shadow-md hover:bg-primary transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                type="submit"
                disabled={!canContinue}
              >
                Save &amp; Continue to Symptoms
                <span className="material-symbols-outlined text-[18px]">arrow_forward</span>
              </button>
            </div>
          </div>
        </form>

        <aside className="lg:col-span-4 space-y-space-md">
          <section className="bg-surface-container-lowest rounded-xl shadow-sm p-space-lg space-y-space-md">
            <div className="flex items-center gap-space-sm">
              <span className="material-symbols-outlined text-primary text-[20px]">garage</span>
              <h2 className="font-headline-sm text-headline-sm text-on-surface">Active Session</h2>
            </div>
            <div className="rounded-xl bg-surface-container-low p-space-md">
              <div className="font-headline-md text-headline-md text-on-surface">
                {vehicleLabel(vehicle)}
              </div>
              <div className="font-body-sm text-body-sm text-on-surface-variant mt-1">
                {vehicleSecondary(vehicle)}
              </div>
            </div>
            <div className="space-y-2 font-body-sm text-body-sm text-on-surface-variant">
              <div className="flex items-start gap-1.5">
                <span className="material-symbols-outlined text-primary text-[16px]">lock</span>
                Stored in this browser only.
              </div>
              <div className="flex items-start gap-1.5">
                <span className="material-symbols-outlined text-primary text-[16px]">science</span>
                Used as a report label, not as a matching rule.
              </div>
              <div className="flex items-start gap-1.5">
                <span className="material-symbols-outlined text-primary text-[16px]">fact_check</span>
                Dataset labels remain the only evidence source.
              </div>
            </div>
          </section>

          <section className="bg-surface-container-lowest rounded-xl shadow-sm p-space-lg space-y-space-sm">
            <div className="flex items-center justify-between gap-space-sm">
              <div className="flex items-center gap-space-sm">
                <span className="material-symbols-outlined text-primary text-[20px]">switch_account</span>
                <h2 className="font-headline-sm text-headline-sm text-on-surface">
                  Local Profiles
                </h2>
              </div>
              <span className="font-label-caps text-label-caps text-on-surface-variant">
                {profiles.length} saved
              </span>
            </div>
            {profiles.length === 0 ? (
              <p className="font-body-sm text-body-sm text-on-surface-variant rounded-lg bg-surface-container-low p-space-sm">
                Saved profiles appear here for quick reuse on this device.
              </p>
            ) : (
              <div className="space-y-space-sm">
                {profiles.map((profile, index) => (
                  <button
                    key={`${profile.make}-${profile.model}-${profile.year}-${index}`}
                    className="w-full text-left rounded-lg bg-surface-container-low p-space-sm hover:bg-surface-container transition-all"
                    type="button"
                    onClick={() => setVehicle(emptyVehicle(profile))}
                  >
                    <div className="font-headline-sm text-[13px] text-on-surface">
                      {vehicleLabel(profile)}
                    </div>
                    <div className="font-body-sm text-[11px] text-on-surface-variant truncate">
                      {vehicleSecondary(profile)}
                    </div>
                  </button>
                ))}
              </div>
            )}
          </section>
        </aside>
      </div>
    </div>
  );
}

function Field({ label, htmlFor, children }) {
  return (
    <div className="space-y-1">
      <label
        htmlFor={htmlFor}
        className="block font-label-caps text-label-caps uppercase tracking-wider text-on-surface-variant"
      >
        {label}
      </label>
      {children}
    </div>
  );
}
