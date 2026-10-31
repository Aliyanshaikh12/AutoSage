import { spawn } from "node:child_process";
import fs from "node:fs";
import http from "node:http";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(__dirname, "..");
const backendAppPath = path.join(projectRoot, "backend", "app.py");

let backendProcess = null;
let startupPromise = null;
let activeLogger = null;

function checkBackendHealth(timeoutMs = 700) {
  return new Promise((resolve) => {
    const req = http.get(
      {
        hostname: "127.0.0.1",
        port: 5000,
        path: "/api/health",
        timeout: timeoutMs,
      },
      (res) => {
        res.resume();
        resolve(res.statusCode === 200);
      }
    );
    req.on("error", () => resolve(false));
    req.on("timeout", () => {
      req.destroy();
      resolve(false);
    });
  });
}

function resolvePythonCommand() {
  const candidates = [
    path.join(projectRoot, ".venv", "Scripts", "python.exe"),
    path.join(projectRoot, "backend", ".venv", "Scripts", "python.exe"),
    path.join(projectRoot, ".venv", "bin", "python"),
    path.join(projectRoot, "backend", ".venv", "bin", "python"),
  ];
  for (const candidate of candidates) {
    if (fs.existsSync(candidate)) {
      return candidate;
    }
  }
  return process.platform === "win32" ? "python" : "python3";
}

function stopManagedBackend() {
  if (backendProcess && !backendProcess.killed) {
    try {
      backendProcess.kill();
    } catch {
      // Ignore cleanup errors on shutdown.
    }
  }
  backendProcess = null;
}

process.once("exit", stopManagedBackend);

function ensureBackendRunning(logger = activeLogger) {
  if (startupPromise) {
    return startupPromise;
  }

  startupPromise = (async () => {
    try {
      if (await checkBackendHealth()) {
        return true;
      }

      if (!fs.existsSync(backendAppPath)) {
        logger?.warn?.(
          `[auto-sage] Backend script not found at ${backendAppPath}`
        );
        return false;
      }

      const pythonCmd = resolvePythonCommand();
      logger?.info?.(
        `[auto-sage] Starting Flask backend (${pythonCmd} backend/app.py)...`
      );

      const child = spawn(pythonCmd, [backendAppPath], {
        cwd: projectRoot,
        env: {
          ...process.env,
          AUTO_SAGE_NO_RELOADER: "1",
          PYTHONUNBUFFERED: "1",
        },
        stdio: ["ignore", "pipe", "pipe"],
        windowsHide: true,
      });

      backendProcess = child;
      child.stdout?.resume();
      child.stderr?.on("data", (chunk) => {
        const text = String(chunk).trim();
        if (
          text &&
          (text.includes("Traceback") ||
            text.includes("Error") ||
            text.includes("Exception"))
        ) {
          logger?.error?.(`[auto-sage:flask] ${text}`);
        }
      });

      child.on("error", (err) => {
        logger?.error?.(
          `[auto-sage] Failed to start Flask backend: ${err.message}`
        );
        if (backendProcess === child) {
          backendProcess = null;
        }
      });

      child.on("exit", () => {
        if (backendProcess === child) {
          backendProcess = null;
        }
      });

      const deadline = Date.now() + 6000;
      while (Date.now() < deadline) {
        if (child.exitCode !== null) {
          break;
        }
        if (await checkBackendHealth(500)) {
          logger?.info?.(
            "[auto-sage] Flask backend ready at http://127.0.0.1:5000"
          );
          return true;
        }
        await new Promise((resolve) => setTimeout(resolve, 150));
      }

      return await checkBackendHealth(500);
    } finally {
      startupPromise = null;
    }
  })();

  return startupPromise;
}

function createApiProxyConfig() {
  return {
    "/api": {
      target: "http://127.0.0.1:5000",
      changeOrigin: true,
      configure(proxy) {
        proxy.on("error", (_err, _req, res) => {
          ensureBackendRunning();
          if (res && !res.headersSent && typeof res.writeHead === "function") {
            res.writeHead(502, { "Content-Type": "text/plain" });
            res.end("Auto Sage backend is starting...");
          }
        });
      },
    },
  };
}

function autoSageBackendPlugin() {
  const attachLifecycle = async (server) => {
    activeLogger = server.config?.logger || console;
    server.httpServer?.once("close", stopManagedBackend);
    await ensureBackendRunning(activeLogger);
  };

  return {
    name: "auto-sage-flask-backend",
    configureServer: attachLifecycle,
    configurePreviewServer: attachLifecycle,
  };
}

export default defineConfig({
  plugins: [react(), autoSageBackendPlugin()],
  server: {
    host: "127.0.0.1",
    port: 5173,
    strictPort: true,
    proxy: createApiProxyConfig(),
  },
  preview: {
    host: "127.0.0.1",
    port: 4173,
    strictPort: true,
    proxy: createApiProxyConfig(),
  },
});
