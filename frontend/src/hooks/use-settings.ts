import { useCallback, useSyncExternalStore } from "react";

interface Settings {
  model: string;
  topK: number;
}

const STORAGE_KEY = "rag-settings";
// WHY gpt-5-mini as default: best speed/quality/cost balance on OpenAI's
// current lineup (April 2026) — ~250 tok/s streaming, $0.25/$2.00 per 1M,
// 400K context. Small enough to feel instant in chat, capable enough for
// RAG answers grounded in retrieved context.
const DEFAULTS: Settings = { model: "gemini-3.1-flash-lite", topK: 5 };

// BUG FIX: useSyncExternalStore compares snapshots with Object.is().
// BEFORE: getSnapshot() returned a new object on every call, causing
//         infinite re-renders because Object.is({}, {}) is always false.
// AFTER:  Cache the last parsed value and only create a new object when
//         the raw JSON string actually changes.
let _cachedRaw: string | null = null;
let _cachedSettings: Settings = DEFAULTS;

function getSnapshot(): Settings {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw !== _cachedRaw) {
      _cachedRaw = raw;
      const parsed = raw ? JSON.parse(raw) : {};
      // Auto-migrate old/deprecated models (gpt-5-mini, gemini-2.5-flash, gemini-2.0-flash) to gemini-3.1-flash-lite
      if (
        parsed.model === "gpt-5-mini" ||
        parsed.model === "gemini-2.5-flash" ||
        parsed.model === "gemini-2.0-flash" ||
        !MODEL_OPTIONS.some((m) => m.value === parsed.model)
      ) {
        parsed.model = "gemini-3.1-flash-lite";
      }
      _cachedSettings = raw ? { ...DEFAULTS, ...parsed } : DEFAULTS;
    }
    return _cachedSettings;
  } catch {
    return DEFAULTS;
  }
}

let listeners: Array<() => void> = [];
function subscribe(cb: () => void) {
  listeners.push(cb);
  return () => {
    listeners = listeners.filter((l) => l !== cb);
  };
}
function emitChange() {
  listeners.forEach((l) => l());
}

export function useSettings() {
  const settings = useSyncExternalStore(subscribe, getSnapshot, () => DEFAULTS);

  const update = useCallback((patch: Partial<Settings>) => {
    const next = { ...getSnapshot(), ...patch };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
    emitChange();
  }, []);

  return { settings, update };
}

// WHY this lineup: Google AI Studio Gemini 3.1 Flash Lite is our active free-tier
// production default. Also includes Gemini 3.1 Preview, OpenAI, and local Ollama.
export const MODEL_OPTIONS = [
  { label: "Gemini 3.1 Flash",   hint: "recommended", value: "gemini-3.1-flash-lite" },
  { label: "Gemini 3.1 Preview", hint: "preview",     value: "gemini-3.1-flash-lite-preview" },
  { label: "GPT-5 Mini",         hint: "openai",      value: "gpt-5-mini" },
  { label: "GPT-5.4 Nano",       hint: "fastest",     value: "gpt-5.4-nano" },
  { label: "GPT-5.4",            hint: "premium",     value: "gpt-5.4" },
  { label: "GPT-4.1 Mini",       hint: "1M ctx",      value: "gpt-4.1-mini" },
  { label: "Llama 3",            hint: "local",       value: "llama3" },
] as const;
