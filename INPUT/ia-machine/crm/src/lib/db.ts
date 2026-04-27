// Todas las queries del sistema — un solo lugar, fácil de mantener
import { supabase, type Agent, type Project, type Contact, type Run, type InboxItem } from "./supabase";

// ── PROJECTS ──────────────────────────────────────────────────────────────

export async function getProjects(): Promise<Project[]> {
  const { data, error } = await supabase
    .from("projects")
    .select("*")
    .order("priority");
  if (error) throw error;
  return data;
}

export async function getProject(id: string): Promise<Project> {
  const { data, error } = await supabase
    .from("projects")
    .select("*")
    .eq("id", id)
    .single();
  if (error) throw error;
  return data;
}

export async function updateProject(id: string, patch: Partial<Project>) {
  const { error } = await supabase.from("projects").update(patch).eq("id", id);
  if (error) throw error;
}

// ── AGENTS ────────────────────────────────────────────────────────────────

export async function getAgents(projectId?: string): Promise<Agent[]> {
  let q = supabase.from("agents").select("*").order("created_at");
  if (projectId) q = q.eq("project_id", projectId);
  const { data, error } = await q;
  if (error) throw error;
  return data;
}

export async function getAgent(id: string): Promise<Agent> {
  const { data, error } = await supabase
    .from("agents").select("*").eq("id", id).single();
  if (error) throw error;
  return data;
}

// Los agentes se auto-registran — cualquier agente puede crear su propio registro
export async function upsertAgent(agent: Partial<Agent> & { id: string }) {
  const { error } = await supabase
    .from("agents")
    .upsert({ ...agent, updated_at: new Date().toISOString() });
  if (error) throw error;
}

export async function updateAgentStatus(id: string, status: Agent["status"]) {
  const { error } = await supabase
    .from("agents")
    .update({ status, updated_at: new Date().toISOString() })
    .eq("id", id);
  if (error) throw error;
}

export async function toggleAgent(id: string, enabled: boolean) {
  const { error } = await supabase
    .from("agents")
    .update({ enabled, updated_at: new Date().toISOString() })
    .eq("id", id);
  if (error) throw error;
}

// ── RUNS ──────────────────────────────────────────────────────────────────

export async function getRuns(agentId?: string, limit = 20): Promise<Run[]> {
  let q = supabase
    .from("runs")
    .select("*")
    .order("started_at", { ascending: false })
    .limit(limit);
  if (agentId) q = q.eq("agent_id", agentId);
  const { data, error } = await q;
  if (error) throw error;
  return data;
}

// Registra el inicio de un run — el agente llama esto al arrancar
export async function startRun(agentId: string, projectId: string | null, triggeredBy: Run["triggered_by"] = "manual") {
  const { data, error } = await supabase
    .from("runs")
    .insert({ agent_id: agentId, project_id: projectId, triggered_by: triggeredBy, status: "running" })
    .select("id")
    .single();
  if (error) throw error;

  // Marcar agente como running
  await updateAgentStatus(agentId, "running");
  return data.id as string;
}

// Cierra el run con resultado — el agente llama esto al terminar
export async function finishRun(
  runId: string,
  agentId: string,
  status: "success" | "error",
  output: Record<string, unknown>,
  logs: string[],
  errorMsg?: string
) {
  const now = new Date().toISOString();
  const { data: run } = await supabase.from("runs").select("started_at").eq("id", runId).single();
  const durationMs = run ? Date.now() - new Date(run.started_at).getTime() : null;

  await supabase.from("runs").update({
    status, output, logs, error_msg: errorMsg ?? null,
    duration_ms: durationMs, finished_at: now,
  }).eq("id", runId);

  // Actualizar stats del agente
  const agent = await getAgent(agentId);
  await supabase.from("agents").update({
    status: "idle",
    last_run_at: now,
    runs_total: agent.runs_total + 1,
    runs_success: status === "success" ? agent.runs_success + 1 : agent.runs_success,
    updated_at: now,
  }).eq("id", agentId);
}

// ── CONTACTS ─────────────────────────────────────────────────────────────

export async function getContacts(projectId?: string): Promise<Contact[]> {
  let q = supabase.from("contacts").select("*").order("created_at", { ascending: false });
  if (projectId) q = q.eq("project_id", projectId);
  const { data, error } = await q;
  if (error) throw error;
  return data;
}

export async function upsertContact(contact: Partial<Contact> & { project_id: string; name: string }) {
  const { error } = await supabase.from("contacts").upsert({
    ...contact, updated_at: new Date().toISOString(),
  });
  if (error) throw error;
}

export async function updateContactStage(id: string, stage: Contact["stage"]) {
  const { error } = await supabase
    .from("contacts")
    .update({ stage, updated_at: new Date().toISOString() })
    .eq("id", id);
  if (error) throw error;
}

// ── INBOX ─────────────────────────────────────────────────────────────────

export async function getInbox(projectId?: string): Promise<InboxItem[]> {
  let q = supabase
    .from("inbox")
    .select("*")
    .eq("status", "pending")
    .order("created_at", { ascending: false });
  if (projectId) q = q.eq("project_id", projectId);
  const { data, error } = await q;
  if (error) throw error;
  return data;
}

export async function markInboxProcessed(id: string, distributedTo: string) {
  const { error } = await supabase.from("inbox").update({
    status: "distributed",
    distributed_to: distributedTo,
    processed_at: new Date().toISOString(),
  }).eq("id", id);
  if (error) throw error;
}

// ── REALTIME — suscripciones para el dashboard en vivo ───────────────────

export function subscribeToAgents(callback: (agents: Agent[]) => void) {
  return supabase
    .channel("agents-changes")
    .on("postgres_changes", { event: "*", schema: "public", table: "agents" }, async () => {
      const agents = await getAgents();
      callback(agents);
    })
    .subscribe();
}

export function subscribeToRuns(callback: (run: Run) => void) {
  return supabase
    .channel("runs-changes")
    .on("postgres_changes", { event: "INSERT", schema: "public", table: "runs" }, (payload) => {
      callback(payload.new as Run);
    })
    .subscribe();
}
