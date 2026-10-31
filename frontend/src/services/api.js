const EXPLICIT_API_URL =
  typeof import.meta !== "undefined" &&
  typeof import.meta.env?.VITE_API_URL === "string" &&
  import.meta.env.VITE_API_URL.trim()
    ? import.meta.env.VITE_API_URL.trim().replace(/\/+$/, "")
    : null;

export const API_BASE = EXPLICIT_API_URL || "/api";

async function request(path, options = {}) {
  const { headers, ...rest } = options;
  let response;
  try {
    response = await fetch(`${API_BASE}${path}`, {
      ...rest,
      headers: {
        ...(rest.body !== undefined ? { "Content-Type": "application/json" } : {}),
        ...headers,
      },
    });
  } catch {
    throw new Error(
      "Cannot reach the Auto Sage backend. Make sure the Flask server is running on http://127.0.0.1:5000."
    );
  }
  let data = null;
  try {
    data = await response.json();
  } catch {
    data = null;
  }
  if (!response.ok) {
    const message =
      data && typeof data.message === "string" && data.message.trim()
        ? data.message.trim()
        : response.status === 502
        ? "The backend is not responding. Start the Flask server and try again."
        : `Request failed (HTTP ${response.status}).`;
    const error = new Error(message);
    error.status = response.status;
    throw error;
  }
  if (data === null) throw new Error("The backend returned an unreadable response.");
  return data;
}

export function checkHealth() {
  return request("/health");
}

export async function getCategories() {
  const data = await request("/categories");
  return Array.isArray(data.categories) ? data.categories : [];
}

export async function getSymptoms(categoryId) {
  const query = categoryId ? `?category=${encodeURIComponent(categoryId)}` : "";
  const data = await request(`/symptoms${query}`);
  return Array.isArray(data.symptoms) ? data.symptoms : [];
}

export function getKnowledgeBase() {
  return request("/knowledge-base");
}

export function getFollowUpQuestions(categoryId, symptomIds, options = {}) {
  return request("/follow-up-questions", {
    method: "POST",
    body: JSON.stringify({ category_id: categoryId, symptom_ids: symptomIds }),
    signal: options.signal,
  });
}

export function diagnose(categoryId, symptomIds, followUpAnswers = {}, options = {}) {
  return request("/diagnose", {
    method: "POST",
    body: JSON.stringify({
      category_id: categoryId,
      symptom_ids: symptomIds,
      follow_up_answers: followUpAnswers,
    }),
    signal: options.signal,
  });
}

export function flowchartUrl(flowchartId) {
  return `${API_BASE}/flowcharts/${encodeURIComponent(flowchartId)}`;
}
