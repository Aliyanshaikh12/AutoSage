export async function exportElementToPdf(element, filename = "Auto_Sage_Diagnostic_Report.pdf") {
  if (!element) {
    window.print();
    return { ok: false, fallback: true, error: "No element provided for export." };
  }

  try {
    const html2pdfModule = await import("html2pdf.js");
    const html2pdf = html2pdfModule.default || html2pdfModule;

    const opt = {
      margin: [10, 10, 12, 10],
      filename,
      image: { type: "jpeg", quality: 0.98 },
      html2canvas: {
        scale: 2,
        useCORS: true,
        letterRendering: true,
        logging: false,
      },
      jsPDF: { unit: "mm", format: "a4", orientation: "portrait" },
      pagebreak: { mode: ["css", "legacy"] },
    };

    await html2pdf().set(opt).from(element).save();
    return { ok: true, fallback: false, filename };
  } catch (err) {
    // Graceful fallback to browser print dialog
    window.print();
    return {
      ok: false,
      fallback: true,
      error: err?.message || "Client-side PDF module error; opened browser print dialog instead.",
    };
  }
}
