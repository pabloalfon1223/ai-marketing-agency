import { createBrowserClient } from "@supabase/ssr";
import type { SupabaseClient } from "@supabase/supabase-js";

let _client: SupabaseClient | null = null;

export function getSupabaseClient(): SupabaseClient {
  if (!_client) {
    const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
    const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
    if (!url || !anonKey) throw new Error("Supabase env vars not set");
    // createBrowserClient guarda la sesión en cookies — el middleware la puede leer
    _client = createBrowserClient(url, anonKey);
  }
  return _client;
}

export const supabase = new Proxy({} as SupabaseClient, {
  get(_target, prop) {
    return (getSupabaseClient() as unknown as Record<string | symbol, unknown>)[prop];
  },
});

// ── Types ──────────────────────────────────────────────────────────────────

export type AgentStatus = "idle" | "running" | "active" | "error";
export type RunStatus = "running" | "success" | "error";
export type PipelineStage =
  | "nuevo" | "calificado" | "propuesta"
  | "negociacion" | "cerrado-ganado" | "cerrado-perdido";
export type ContentStatus = "draft" | "approved" | "published" | "rejected";
export type InboxStatus = "pending" | "processed" | "distributed";

export interface Project {
  id: string;
  name: string;
  priority: number;
  status_pct: number;
  currency: "USD" | "ARS";
  revenue_month: number;
  revenue_goal: number;
  blockers: string[];
  pending_tasks: string[];
  meta: Record<string, unknown>;
  updated_at: string;
}

export interface Agent {
  id: string;
  name: string;
  description: string | null;
  project_id: string | null;
  status: AgentStatus;
  schedule: string | null;
  trigger_id: string | null;
  skill_base: string | null;
  prompt: string | null;
  enabled: boolean;
  runs_total: number;
  runs_success: number;
  last_run_at: string | null;
  next_run_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface Run {
  id: string;
  agent_id: string;
  project_id: string | null;
  status: RunStatus;
  triggered_by: "manual" | "schedule" | "system";
  input: Record<string, unknown> | null;
  output: Record<string, unknown> | null;
  logs: string[];
  error_msg: string | null;
  duration_ms: number | null;
  started_at: string;
  finished_at: string | null;
}

export interface Contact {
  id: string;
  project_id: string;
  name: string;
  email: string | null;
  phone: string | null;
  stage: PipelineStage;
  value: number;
  currency: "USD" | "ARS";
  notes: string | null;
  tags: string[];
  source: string | null;
  assigned_agent: string | null;
  created_at: string;
  updated_at: string;
}

export interface InboxItem {
  id: string;
  project_id: string | null;
  filename: string;
  file_type: string | null;
  file_path: string | null;
  status: InboxStatus;
  distributed_to: string | null;
  notes: string | null;
  created_at: string;
  processed_at: string | null;
}

export interface ContentOutput {
  id: string;
  project_id: string;
  agent_id: string | null;
  run_id: string | null;
  format: string | null;
  platform: string | null;
  hook: string | null;
  body: string | null;
  cta: string | null;
  visual_prompt: string | null;
  caption: string | null;
  hashtags: string[];
  status: ContentStatus;
  created_at: string;
}
