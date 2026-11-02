import { useCallback, useSyncExternalStore } from "react";

interface Settings {
  model: string;
  topK: number;
}

const STORAGE_KEY = "rag-settings";
// Default to Qwen 3.8 27B on Groq for ultra-fast LPU inference (500+ tok/s)
const DEFAULTS: Settings = { model: "qwen/qwen3.8-27b", topK: 5 };

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
      // If previous stored model is not in current lineup, default to Qwen
      if (!MODEL_OPTIONS.some((m) => m.value === parsed.model)) {
        parsed.model = "qwen/qwen3.8-27b";
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

// Active models: Groq Cloud LPU (ultra-fast inference)
export const MODEL_OPTIONS = [
  { label: "Qwen 3.8 27B",       hint: "Groq 800 tok/s", value: "qwen/qwen3.8-27b" },
  { label: "GPT-OSS 120B",       hint: "Groq 120B",      value: "openai/gpt-oss-120b" },
  { label: "GPT-OSS 20B",        hint: "Groq 20B",       value: "openai/gpt-oss-20b" },
] as const;
