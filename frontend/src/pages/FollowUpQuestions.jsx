import { useEffect, useState, useRef } from "react";
import Stepper from "../components/Stepper.jsx";
import { getFollowUpQuestions, diagnose } from "../services/api.js";
import { vehicleLabel } from "../stitch/dom.js";

export default function FollowUpQuestions({
  categoryId,
  categoryName,
  selectedSymptomIds,
  selectedSymptoms = [],
  vehicleInfo,
  onDiagnosisComplete,
  onBack,
  onNavigateStep,
}) {
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const inFlight = useRef(false);

  useEffect(() => {
    let active = true;
    setLoading(true);
    setError("");

    getFollowUpQuestions(categoryId, selectedSymptomIds)
      .then((data) => {
        if (!active) return;
        const qList = Array.isArray(data.questions) ? data.questions : [];
        setQuestions(qList);
        // Pre-initialize answers as undefined or empty
        const initialAnswers = {};
        qList.forEach((q) => {
          if (q.question_id) initialAnswers[q.question_id] = null;
        });
        setAnswers(initialAnswers);
      })
      .catch((err) => {
        if (!active) return;
        setError(err.message || "Failed to load diagnostic follow-up questions.");
      })
      .finally(() => {
        if (active) setLoading(false);
      });

    return () => {
      active = false;
    };
  }, [categoryId, selectedSymptomIds]);

  const setAnswer = (questionId, value) => {
    setAnswers((prev) => ({
      ...prev,
      [questionId]: prev[questionId] === value ? null : value,
    }));
  };

  const handleDiagnose = async (overrideAnswers = null) => {
    if (inFlight.current) return;
    inFlight.current = true;
    setSubmitting(true);
    setError("");

    const finalAnswers = {};
    const sourceAnswers = overrideAnswers !== null ? overrideAnswers : answers;
    for (const [qid, ans] of Object.entries(sourceAnswers)) {
      if (ans && ans !== "skip") {
        finalAnswers[qid] = ans;
      }
    }

    try {
      const result = await diagnose(categoryId, selectedSymptomIds, finalAnswers);
      onDiagnosisComplete(result, finalAnswers);
    } catch (err) {
      setError(err.message || "Inference engine error during diagnosis.");
      setSubmitting(false);
      inFlight.current = false;
    }
  };

  const answeredCount = Object.values(answers).filter((v) => v !== null && v !== undefined).length;

  return (
    <div className="space-y-space-md">
      <Stepper currentStep={3} onStepClick={onNavigateStep} />

      {/* Header card */}
      <section className="bg-surface-container-lowest rounded-xl p-space-md md:p-space-lg shadow-sm">
        <div className="flex flex-wrap items-center justify-between gap-space-sm pb-space-sm border-b border-outline-variant/10">
          <div>
            <div className="flex items-center gap-2 text-primary font-label-caps text-xs tracking-wider uppercase mb-1">
              <span className="material-symbols-outlined text-[16px]">psychology_alt</span>
              <span>Step 03 &bull; Diagnostic Inquiry</span>
            </div>
            <h1 className="font-display-md text-2xl md:text-3xl font-extrabold text-on-surface">
              Dynamic Follow-Up Questions
            </h1>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            {categoryName && (
              <span className="px-3 py-1 rounded-full text-xs font-medium bg-surface-container-high text-on-surface-variant flex items-center gap-1.5">
                <span className="material-symbols-outlined text-[14px]">category</span>
                {categoryName}
              </span>
            )}
            {vehicleInfo && (
              <span className="px-3 py-1 rounded-full text-xs font-medium bg-primary/10 text-primary flex items-center gap-1.5">
                <span className="material-symbols-outlined text-[14px]">directions_car</span>
                {vehicleLabel(vehicleInfo)}
              </span>
            )}
          </div>
        </div>

        <p className="mt-space-sm text-on-surface-variant text-sm md:text-base leading-relaxed">
          The inference engine has identified candidate fault hypotheses matching your{" "}
          <strong>{selectedSymptomIds.length}</strong> reported symptom
          {selectedSymptomIds.length === 1 ? "" : "s"}. Answering these targeted follow-up questions provides
          corroborating or contradictory evidence to disambiguate the true root cause.
        </p>

        {/* Selected Symptoms Summary Chips */}
        {selectedSymptoms.length > 0 && (
          <div className="mt-space-sm pt-space-xs flex flex-wrap items-center gap-1.5">
            <span className="text-xs font-semibold text-outline mr-1">Reported Symptoms:</span>
            {selectedSymptoms.map((sym) => (
              <span
                key={sym.symptom_id}
                className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-surface-container text-on-surface-variant border border-outline-variant/20"
              >
                <span className="material-symbols-outlined text-[12px] text-primary">check_circle</span>
                {sym.label}
              </span>
            ))}
          </div>
        )}
      </section>

      {/* Main inquiry section */}
      {loading ? (
        <div className="bg-surface-container-lowest rounded-xl p-space-xl shadow-sm text-center">
          <div className="inline-block w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin mb-space-sm" />
          <h2 className="text-base font-semibold text-on-surface">
            Querying Knowledge Base Hypotheses...
          </h2>
          <p className="text-xs text-on-surface-variant mt-1">
            Matching rules and extracting discriminatory follow-up tests for your symptoms.
          </p>
        </div>
      ) : error && questions.length === 0 ? (
        <div className="bg-error-container/20 border border-error/30 rounded-xl p-space-md text-on-error-container">
          <div className="flex items-start gap-3">
            <span className="material-symbols-outlined text-error text-2xl">error</span>
            <div className="flex-1">
              <h2 className="font-bold text-sm">Failed to Load Questions</h2>
              <p className="text-xs mt-1 text-on-surface-variant">{error}</p>
              <div className="mt-4 flex gap-3">
                <button
                  type="button"
                  onClick={() => handleDiagnose({})}
                  className="px-4 py-2 bg-primary text-on-primary rounded-lg text-xs font-semibold hover:bg-primary/90 transition-colors"
                >
                  Proceed with Direct Diagnosis
                </button>
                <button
                  type="button"
                  onClick={onBack}
                  className="px-4 py-2 bg-surface-container text-on-surface-variant rounded-lg text-xs font-semibold hover:bg-surface-container-high transition-colors"
                >
                  Back to Symptoms
                </button>
              </div>
            </div>
          </div>
        </div>
      ) : questions.length === 0 ? (
        <div className="bg-surface-container-lowest rounded-xl p-space-lg shadow-sm text-center space-y-4">
          <div className="w-12 h-12 rounded-full bg-primary/10 text-primary mx-auto flex items-center justify-center">
            <span className="material-symbols-outlined text-2xl">task_alt</span>
          </div>
          <div>
            <h2 className="font-headline-sm text-lg font-bold text-on-surface">
              Direct Evidence Sufficient
            </h2>
            <p className="text-sm text-on-surface-variant max-w-lg mx-auto mt-1">
              The selected symptoms provide sufficient unambiguous evidence for rule evaluation without requiring secondary follow-up inquiry.
            </p>
          </div>
          <div className="pt-2 flex justify-center gap-3">
            <button
              type="button"
              onClick={onBack}
              className="px-4 py-2 bg-surface-container-high text-on-surface rounded-lg text-sm font-semibold hover:bg-surface-container transition-colors"
            >
              Modify Symptoms
            </button>
            <button
              type="button"
              onClick={() => handleDiagnose({})}
              disabled={submitting}
              className="px-6 py-2.5 bg-primary text-on-primary rounded-lg text-sm font-semibold shadow hover:bg-primary/90 transition-colors flex items-center gap-2"
            >
              {submitting ? (
                <>
                  <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Running Inference...
                </>
              ) : (
                <>
                  <span>Run Deterministic Diagnosis</span>
                  <span className="material-symbols-outlined text-[18px]">arrow_forward</span>
                </>
              )}
            </button>
          </div>
        </div>
      ) : (
        <div className="space-y-space-md">
          {error && (
            <div className="bg-error-container/30 border border-error/30 rounded-xl p-space-sm text-xs text-error flex items-center gap-2">
              <span className="material-symbols-outlined text-[16px]">warning</span>
              <span>{error}</span>
            </div>
          )}

          {/* Questions list */}
          <div className="space-y-4">
            {questions.map((q, idx) => {
              const currentAns = answers[q.question_id];
              return (
                <div
                  key={q.question_id || idx}
                  className="bg-surface-container-lowest rounded-xl p-space-md md:p-space-lg shadow-sm border border-outline-variant/10 hover:border-primary/20 transition-all"
                >
                  <div className="flex items-start justify-between gap-3">
                    <div className="flex items-center gap-2 text-xs font-semibold text-outline">
                      <span className="w-6 h-6 rounded-full bg-surface-container-high text-on-surface flex items-center justify-center text-xs font-bold">
                        {idx + 1}
                      </span>
                      <span>INQUIRY TEST {idx + 1} OF {questions.length}</span>
                    </div>

                    {q.relevant_faults && q.relevant_faults.length > 0 && (
                      <span className="text-[11px] px-2 py-0.5 rounded bg-surface-container text-on-surface-variant font-medium">
                        Hypothesis: {q.relevant_faults[0]}
                      </span>
                    )}
                  </div>

                  <h3 className="mt-2 text-base md:text-lg font-semibold text-on-surface">
                    {q.question}
                  </h3>

                  {q.context && (
                    <p className="mt-1 text-xs md:text-sm text-on-surface-variant/90 italic flex items-center gap-1.5">
                      <span className="material-symbols-outlined text-[14px] text-primary shrink-0">info</span>
                      <span>{q.context}</span>
                    </p>
                  )}

                  {/* Options Buttons */}
                  <div className="mt-4 grid grid-cols-3 gap-2 sm:gap-4 max-w-xl">
                    <button
                      type="button"
                      onClick={() => setAnswer(q.question_id, "yes")}
                      className={`flex items-center justify-center gap-2 py-2.5 px-3 rounded-lg text-xs md:text-sm font-semibold transition-all border ${
                        currentAns === "yes"
                          ? "bg-primary text-on-primary border-primary shadow-sm ring-2 ring-primary/30"
                          : "bg-surface-container-low text-on-surface hover:bg-surface-container border-outline-variant/20"
                      }`}
                    >
                      <span className="material-symbols-outlined text-[18px]">
                        {currentAns === "yes" ? "check_circle" : "radio_button_unchecked"}
                      </span>
                      <span>Yes</span>
                    </button>

                    <button
                      type="button"
                      onClick={() => setAnswer(q.question_id, "no")}
                      className={`flex items-center justify-center gap-2 py-2.5 px-3 rounded-lg text-xs md:text-sm font-semibold transition-all border ${
                        currentAns === "no"
                          ? "bg-error text-on-error border-error shadow-sm ring-2 ring-error/30"
                          : "bg-surface-container-low text-on-surface hover:bg-surface-container border-outline-variant/20"
                      }`}
                    >
                      <span className="material-symbols-outlined text-[18px]">
                        {currentAns === "no" ? "cancel" : "radio_button_unchecked"}
                      </span>
                      <span>No</span>
                    </button>

                    <button
                      type="button"
                      onClick={() => setAnswer(q.question_id, "not_sure")}
                      className={`flex items-center justify-center gap-2 py-2.5 px-3 rounded-lg text-xs md:text-sm font-semibold transition-all border ${
                        currentAns === "not_sure"
                          ? "bg-secondary-container text-on-secondary-container border-secondary shadow-sm ring-2 ring-secondary/30"
                          : "bg-surface-container-low text-on-surface hover:bg-surface-container border-outline-variant/20"
                      }`}
                    >
                      <span className="material-symbols-outlined text-[18px]">
                        {currentAns === "not_sure" ? "help" : "radio_button_unchecked"}
                      </span>
                      <span>Not Sure</span>
                    </button>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Action bar */}
          <div className="bg-surface-container-lowest rounded-xl p-space-md shadow-sm flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-3 text-xs text-on-surface-variant w-full sm:w-auto">
              <button
                type="button"
                onClick={onBack}
                className="px-4 py-2 bg-surface-container text-on-surface-variant font-semibold rounded-lg hover:bg-surface-container-high transition-colors flex items-center gap-1.5"
              >
                <span className="material-symbols-outlined text-[16px]">arrow_back</span>
                <span>Back to Symptoms</span>
              </button>
              <span>
                {answeredCount} of {questions.length} question{questions.length === 1 ? "" : "s"} answered
              </span>
            </div>

            <div className="flex items-center gap-3 w-full sm:w-auto justify-end">
              <button
                type="button"
                onClick={() => handleDiagnose({})}
                disabled={submitting}
                className="px-4 py-2 bg-surface-container-high text-on-surface font-semibold rounded-lg hover:bg-surface-container transition-colors text-xs"
                title="Run inference engine with symptom evidence only, without follow-up answers"
              >
                Skip Questions
              </button>

              <button
                type="button"
                onClick={() => handleDiagnose(null)}
                disabled={submitting}
                className="px-6 py-2.5 bg-primary text-on-primary font-semibold rounded-lg shadow hover:bg-primary/90 transition-colors flex items-center gap-2 text-xs md:text-sm disabled:opacity-50"
              >
                {submitting ? (
                  <>
                    <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    <span>Evaluating Inference...</span>
                  </>
                ) : (
                  <>
                    <span>Evaluate Evidence & Diagnose</span>
                    <span className="material-symbols-outlined text-[18px]">arrow_forward</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
