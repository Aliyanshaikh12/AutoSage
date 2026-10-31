import { useCallback, useState } from "react";
import Layout from "./components/Layout.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import VehicleInformation from "./pages/VehicleInformation.jsx";
import SymptomSelection from "./pages/SymptomSelection.jsx";
import FollowUpQuestions from "./pages/FollowUpQuestions.jsx";
import DiagnosisResults from "./pages/DiagnosisResults.jsx";
import FaultDetails from "./pages/FaultDetails.jsx";
import RepairMitigationGuide from "./pages/RepairMitigationGuide.jsx";
import SafetyGuide from "./pages/SafetyGuide.jsx";
import History from "./pages/History.jsx";
import DiagnosticReport from "./pages/DiagnosticReport.jsx";
import {
  buildReviewPayloadFromEntry,
  readHistoryRecords,
  saveDiagnosisToHistory,
} from "./utils/historyStorage.js";

const PAGES = {
  DASHBOARD: "dashboard",
  VEHICLE: "vehicle",
  SYMPTOMS: "symptoms",
  QUESTIONS: "questions",
  RESULTS: "results",
  FAULT_DETAILS: "fault_details",
  REPAIR_GUIDE: "repair_guide",
  SAFETY_GUIDE: "safety_guide",
  HISTORY: "history",
  REPORT: "report",
};

export default function App() {
  const [page, setPage] = useState(PAGES.DASHBOARD);
  const [vehicleInfo, setVehicleInfo] = useState(null);
  const [categoryId, setCategoryId] = useState(null);
  const [selectedSymptomIds, setSelectedSymptomIds] = useState([]);
  const [questionsContext, setQuestionsContext] = useState(null);
  const [diagnosisResult, setDiagnosisResult] = useState(null);
  const [reviewedTimestamp, setReviewedTimestamp] = useState(null);
  const [faultDetailMatch, setFaultDetailMatch] = useState(null);
  const [toast, setToast] = useState(null);
  const [historyCount, setHistoryCount] = useState(() => readHistoryRecords().records.length);
  const [searchQuery, setSearchQuery] = useState("");

  const startNewDiagnosis = useCallback((nextCategoryId = null) => {
    setCategoryId(typeof nextCategoryId === "string" ? nextCategoryId : null);
    setSelectedSymptomIds([]);
    setQuestionsContext(null);
    setDiagnosisResult(null);
    setReviewedTimestamp(null);
    setFaultDetailMatch(null);
    setPage(PAGES.VEHICLE);
  }, []);

  const handleProceedToQuestions = useCallback((ctx) => {
    setQuestionsContext(ctx);
    setCategoryId(ctx.categoryId);
    setSelectedSymptomIds(ctx.symptomIds);
    setPage(PAGES.QUESTIONS);
  }, []);

  const handleDiagnosisComplete = useCallback(
    (result, followUpAnswers = {}) => {
      const enriched = {
        ...result,
        vehicle: vehicleInfo || null,
        follow_up_answers: followUpAnswers,
      };
      setDiagnosisResult(enriched);
      setReviewedTimestamp(null);
      setFaultDetailMatch(null);
      const save = saveDiagnosisToHistory({
        categoryId: enriched.category_id,
        categoryName: enriched.category_name,
        symptomIds: enriched.selected_symptoms || [],
        symptomLabels: (enriched.selected_symptom_details || []).map((s) => s.label || s.text),
        vehicleInfo: enriched.vehicle,
        followUpAnswers,
        result: enriched,
      });
      if (save.saved) setHistoryCount(save.records.length);
      else if (save.error) setToast(`Result shown but not saved to history: ${save.error}`);
      setPage(PAGES.RESULTS);
    },
    [vehicleInfo]
  );

  const openHistoryRecord = useCallback((entry) => {
    const payload = buildReviewPayloadFromEntry(entry);
    if (!payload) {
      setToast("This history record could not be opened.");
      return;
    }
    setDiagnosisResult(payload);
    setVehicleInfo(entry.vehicleInfo || payload.vehicle || null);
    setCategoryId(payload.category_id || entry.categoryId || null);
    setSelectedSymptomIds(Array.isArray(payload.selected_symptoms) ? payload.selected_symptoms : []);
    setReviewedTimestamp(entry.timestamp || null);
    setFaultDetailMatch(null);
    setPage(PAGES.RESULTS);
  }, []);

  const openReportFromHistory = useCallback((entry) => {
    const payload = buildReviewPayloadFromEntry(entry);
    if (!payload) {
      setToast("This history record could not be opened as a report.");
      return;
    }
    setDiagnosisResult(payload);
    setVehicleInfo(entry.vehicleInfo || payload.vehicle || null);
    setCategoryId(payload.category_id || entry.categoryId || null);
    setSelectedSymptomIds(Array.isArray(payload.selected_symptoms) ? payload.selected_symptoms : []);
    setReviewedTimestamp(entry.timestamp || null);
    setFaultDetailMatch(null);
    setPage(PAGES.REPORT);
  }, []);

  const navigate = useCallback(
    (next) => {
      if (next === PAGES.SYMPTOMS) {
        startNewDiagnosis(categoryId);
        return;
      }
      if (next === PAGES.QUESTIONS) {
        if (!categoryId || !selectedSymptomIds.length) {
          setToast("Select a problem category and symptoms first.");
          return;
        }
        setPage(PAGES.QUESTIONS);
        return;
      }
      if (next === PAGES.REPORT && !diagnosisResult) {
        const latest = readHistoryRecords().records[0];
        if (latest) {
          const payload = buildReviewPayloadFromEntry(latest);
          if (payload) {
            setDiagnosisResult(payload);
            setReviewedTimestamp(latest.timestamp || null);
            setPage(PAGES.REPORT);
            return;
          }
        }
        setToast("Run a diagnosis before opening a diagnostic report.");
        return;
      }
      if ((next === PAGES.RESULTS || next === PAGES.FAULT_DETAILS || next === PAGES.REPAIR_GUIDE) && !diagnosisResult) {
        setToast("Run a diagnosis first.");
        return;
      }
      if (next === "settings" || next === "signout" || !next) {
        setToast("Auto Sage runs locally. There are no accounts or settings to change.");
        return;
      }
      setPage(next);
    },
    [categoryId, diagnosisResult, startNewDiagnosis]
  );

  return (
    <Layout
      page={page}
      setPage={navigate}
      vehicle={vehicleInfo}
      historyCount={historyCount}
      toast={toast}
      onToast={setToast}
      onSearch={(q) => {
        setSearchQuery(q);
        setPage(PAGES.SYMPTOMS);
      }}
    >
      {page === PAGES.DASHBOARD && (
        <Dashboard
          onStartDiagnosis={startNewDiagnosis}
          onOpenVehicle={() => setPage(PAGES.VEHICLE)}
          onOpenHistoryRecord={openHistoryRecord}
          onOpenHistory={() => setPage(PAGES.HISTORY)}
          onOpenSafetyGuide={() => setPage(PAGES.SAFETY_GUIDE)}
          vehicleInfo={vehicleInfo}
          historyCount={historyCount}
        />
      )}

      {page === PAGES.VEHICLE && (
        <VehicleInformation
          initialVehicle={vehicleInfo}
          onComplete={(info) => {
            setVehicleInfo(info);
            setPage(PAGES.SYMPTOMS);
          }}
          onSkip={() => setPage(PAGES.SYMPTOMS)}
          onBack={() => setPage(PAGES.SYMPTOMS)}
        />
      )}

      {page === PAGES.SYMPTOMS && (
        <SymptomSelection
          categoryId={categoryId}
          onCategoryChange={(id) => {
            setCategoryId(id);
            setSelectedSymptomIds([]);
          }}
          selectedSymptomIds={selectedSymptomIds}
          setSelectedSymptomIds={setSelectedSymptomIds}
          vehicleInfo={vehicleInfo}
          onEditVehicle={() => setPage(PAGES.VEHICLE)}
          onProceedToQuestions={handleProceedToQuestions}
          onDiagnosisComplete={handleDiagnosisComplete}
          onBack={() => setPage(PAGES.DASHBOARD)}
          initialSearchQuery={searchQuery}
          onSearchClear={() => setSearchQuery("")}
        />
      )}

      {page === PAGES.QUESTIONS && (
        <FollowUpQuestions
          categoryId={categoryId || questionsContext?.categoryId}
          categoryName={questionsContext?.categoryName}
          selectedSymptomIds={selectedSymptomIds}
          selectedSymptoms={questionsContext?.symptoms || []}
          vehicleInfo={vehicleInfo}
          onDiagnosisComplete={handleDiagnosisComplete}
          onBack={() => setPage(PAGES.SYMPTOMS)}
          onNavigateStep={navigate}
        />
      )}

      {page === PAGES.RESULTS && diagnosisResult && (
        <DiagnosisResults
          results={diagnosisResult}
          vehicleInfo={vehicleInfo}
          reviewedTimestamp={reviewedTimestamp}
          onModifySymptoms={() => setPage(PAGES.SYMPTOMS)}
          onNewDiagnosis={() => startNewDiagnosis(null)}
          onOpenFaultDetails={(m) => {
            setFaultDetailMatch(m);
            setPage(PAGES.FAULT_DETAILS);
          }}
          onViewRepairGuide={(m) => {
            setFaultDetailMatch(m || null);
            setPage(PAGES.REPAIR_GUIDE);
          }}
          onViewReport={() => setPage(PAGES.REPORT)}
        />
      )}

      {page === PAGES.FAULT_DETAILS && diagnosisResult && (
        <FaultDetails
          match={faultDetailMatch || diagnosisResult.matches?.[0] || null}
          onBackToResults={() => setPage(PAGES.RESULTS)}
          onViewRepairGuide={() => setPage(PAGES.REPAIR_GUIDE)}
        />
      )}

      {page === PAGES.REPAIR_GUIDE && (
        <RepairMitigationGuide
          match={faultDetailMatch}
          diagnosisResult={diagnosisResult}
          onBack={() => setPage(diagnosisResult ? PAGES.RESULTS : PAGES.DASHBOARD)}
          onStartReEvaluation={() => startNewDiagnosis(diagnosisResult?.category_id)}
        />
      )}

      {page === PAGES.SAFETY_GUIDE && (
        <SafetyGuide
          onBack={() => setPage(diagnosisResult ? PAGES.RESULTS : PAGES.DASHBOARD)}
        />
      )}

      {page === PAGES.HISTORY && (
        <History
          onOpenRecord={openHistoryRecord}
          onOpenReport={openReportFromHistory}
          onStartNewDiagnosis={() => startNewDiagnosis(null)}
          onHistoryCountChange={setHistoryCount}
        />
      )}

      {page === PAGES.REPORT && diagnosisResult && (
        <DiagnosticReport
          results={diagnosisResult}
          vehicleInfo={vehicleInfo}
          reviewedTimestamp={reviewedTimestamp}
          onBackToResults={() => setPage(PAGES.RESULTS)}
        />
      )}
    </Layout>
  );
}
