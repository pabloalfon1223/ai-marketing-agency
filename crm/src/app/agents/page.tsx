"use client";
export const dynamic = "force-dynamic";
import { useEffect, useState, useCallback } from "react";
import { Bot, Play, Plus, ToggleLeft, ToggleRight, AlertCircle, Clock, CheckCircle, RefreshCw, ChevronDown, ChevronUp } from "lucide-react";
import { getAgents, getRuns, upsertAgent, updateAgentStatus, toggleAgent, startRun, finishRun, subscribeToAgents } from "@/lib/db";
import type { Agent, Run, AgentStatus } from "@/lib/supabase";
import React from "react";

type FilterKey = "all" | "mente-pausada" | "polt-mobilier" | "cerebro" | "global";

const FILTER_LABELS: Record<FilterKey, string> = {
  all: "Todos", "mente-pausada": "Mente Pausada",
  "polt-mobilier": "Polt Mobilier", cerebro: "Cerebro", global: "Global",
};

const STATUS_CONFIG: Record<AgentStatus, { color: string; label: string; icon: React.ComponentType<{ size?: number; className?: string }> }> = {
  idle: { color: "bg-white/5 text-white/40", label: "En espera", icon: Clock },
  running: { color: "bg-violet-500/15 text-violet-300", label: "Ejecutando", icon: RefreshCw },
  active: { color: "bg-emerald-500/15 text-emerald-300", label: "Activo", icon: CheckCircle },
  error: { color: "bg-red-500/15 text-red-300", label: "Error", icon: AlertCircle },
};

const PROJECT_COLORS: Record<string, string> = {
  "mente-pausada": "bg-violet-600/20 text-violet-300",
  "polt-mobilier": "bg-amber-600/20 text-amber-300",
  "cerebro": "bg-cyan-600/20 text-cyan-300",
};

// ── New Agent Modal ────────────────────────────────────────────────────────
function NewAgentModal({ onClose, onCreated }: { onClose: () => void; onCreated: () => void }) {
  const [form, setForm] = useState({
    id: "", name: "", description: "", project_id: "mente-pausada",
    schedule: "Manual", skill_base: "", prompt: "",
  });
  const [saving, setSaving] = useState(false);

  async function handleCreate() {
    if (!form.id || !form.name) return;
    setSaving(true);
    try {
      await upsertAgent({ ...form, status: "idle", enabled: false, runs_total: 0, runs_success: 0 });
      onCreated();
      onClose();
    } finally {
      setSaving(false);
    }
  }

  const field = (key: keyof typeof form, label: string, type: "input" | "select" | "textarea" = "input", opts?: string[]) => (
    <div>
      <label className="text-xs text-white/40 mb-1 block">{label}</label>
      {type === "input" && (
        <input className="w-full px-3 py-2 text-sm rounded-lg bg-white/5 border border-white/10 text-white outline-none focus:border-violet-500"
          value={form[key]} onChange={e => setForm(f => ({ ...f, [key]: e.target.value }))} />
      )}
      {type === "select" && (
        <select className="w-full px-3 py-2 text-sm rounded-lg bg-white/5 border border-white/10 text-white outline-none focus:border-violet-500"
          value={form[key]} onChange={e => setForm(f => ({ ...f, [key]: e.target.value }))}>
          {opts?.map(o => <option key={o} value={o} className="bg-slate-900">{o}</option>)}
        </select>
      )}
      {type === "textarea" && (
        <textarea rows={4} className="w-full px-3 py-2 text-sm rounded-lg bg-white/5 border border-white/10 text-white outline-none focus:border-violet-500 resize-none"
          placeholder="Describí qué debe hacer el agente, qué input necesita y qué output genera..."
          value={form[key]} onChange={e => setForm(f => ({ ...f, [key]: e.target.value }))} />
      )}
    </div>
  );

  return (
    <div className="fixed inset-0 bg-black/70 z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="bg-[#13131f] border border-white/10 rounded-2xl w-full max-w-lg p-6" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-5">
          <h2 className="text-base font-bold text-white">Nuevo Agente</h2>
          <button onClick={onClose} className="text-white/40 hover:text-white text-xl leading-none">×</button>
        </div>
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-3">
            {field("id", "ID único (slug)", "input")}
            {field("name", "Nombre visible", "input")}
          </div>
          {field("description", "Descripción corta", "input")}
          <div className="grid grid-cols-2 gap-3">
            {field("project_id", "Proyecto", "select", ["mente-pausada", "polt-mobilier", "cerebro"])}
            {field("schedule", "Schedule", "select", ["Manual", "07:00 ARG", "08:00 ARG", "09:00 ARG", "17:00 ARG", "Lunes 09:00 ARG", "Viernes 18:00 ARG"])}
          </div>
          {field("skill_base", "Skill base (opcional)", "select", ["", "content-pipeline", "copywriting", "email-sequence", "paid-ads", "mp-scout", "lead-scorer-polt", "market-money-finder"])}
          {field("prompt", "Prompt / Instrucciones", "textarea")}
        </div>
        <div className="flex gap-2 mt-5">
          <button onClick={onClose} className="flex-1 py-2 text-sm rounded-lg bg-white/5 text-white/60 hover:bg-white/10 border border-white/10">Cancelar</button>
          <button onClick={handleCreate} disabled={saving || !form.id || !form.name}
            className="flex-1 py-2 text-sm rounded-lg bg-violet-600 hover:bg-violet-700 text-white disabled:opacity-40 transition-colors">
            {saving ? "Creando..." : "Crear Agente"}
          </button>
        </div>
      </div>
    </div>
  );
}

// ── Agent Card ─────────────────────────────────────────────────────────────
function AgentCard({ agent, onRefresh }: { agent: Agent; onRefresh: () => void }) {
  const [expanded, setExpanded] = useState(false);
  const [runs, setRuns] = useState<Run[]>([]);
  const [running, setRunning] = useState(false);
  const { color, label, icon: StatusIcon } = STATUS_CONFIG[agent.status];
  const successRate = agent.runs_total > 0 ? Math.round((agent.runs_success / agent.runs_total) * 100) : 100;

  async function loadRuns() {
    const r = await getRuns(agent.id, 5);
    setRuns(r);
  }

  async function handleRun() {
    setRunning(true);
    const runId = await startRun(agent.id, agent.project_id, "manual");
    // Simula ejecución — en producción aquí dispararías el Remote Trigger
    setTimeout(async () => {
      const logs = [
        `[${new Date().toLocaleTimeString("es-AR", { hour: "2-digit", minute: "2-digit" })}] Ejecución manual iniciada`,
        `[${new Date().toLocaleTimeString("es-AR", { hour: "2-digit", minute: "2-digit" })}] Procesando...`,
        `[${new Date().toLocaleTimeString("es-AR", { hour: "2-digit", minute: "2-digit" })}] Completado ✓`,
      ];
      await finishRun(runId, agent.id, "success", { triggered: "manual" }, logs);
      setRunning(false);
      onRefresh();
      if (expanded) loadRuns();
    }, 3000);
  }

  async function handleToggle() {
    await toggleAgent(agent.id, !agent.enabled);
    onRefresh();
  }

  return (
    <div className="rounded-xl border border-white/[0.07] bg-white/[0.02] transition-colors">
      <div className="p-4">
        {/* Header */}
        <div className="flex items-start justify-between gap-3 mb-3">
          <div className="flex items-center gap-3 min-w-0">
            <div className="w-9 h-9 rounded-lg bg-violet-600/15 flex items-center justify-center shrink-0">
              <Bot size={15} className="text-violet-400" />
            </div>
            <div className="min-w-0">
              <p className="text-sm font-medium text-white leading-tight">{agent.name}</p>
              <p className="text-xs text-white/40 truncate mt-0.5">{agent.description}</p>
            </div>
          </div>
          <div className="flex flex-col items-end gap-1.5 shrink-0">
            {agent.project_id && (
              <span className={`text-[10px] px-2 py-0.5 rounded-full ${PROJECT_COLORS[agent.project_id] ?? "bg-white/10 text-white/40"}`}>
                {agent.project_id}
              </span>
            )}
            <span className={`flex items-center gap-1 text-[10px] px-2 py-0.5 rounded-full ${color}`}>
              <StatusIcon size={9} className={agent.status === "running" || running ? "animate-spin" : ""} />
              {running ? "Ejecutando" : label}
            </span>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-2 mb-3">
          <div className="text-center p-2 rounded-lg bg-white/[0.03]">
            <p className="text-sm font-bold text-white">{agent.runs_total}</p>
            <p className="text-[10px] text-white/30 mt-0.5">Runs</p>
          </div>
          <div className="text-center p-2 rounded-lg bg-white/[0.03]">
            <p className={`text-sm font-bold ${successRate >= 90 ? "text-emerald-400" : "text-amber-400"}`}>{successRate}%</p>
            <p className="text-[10px] text-white/30 mt-0.5">Éxito</p>
          </div>
          <div className="text-center p-2 rounded-lg bg-white/[0.03]">
            <p className="text-[11px] font-medium text-white">{agent.schedule ?? "Manual"}</p>
            <p className="text-[10px] text-white/30 mt-0.5">Schedule</p>
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center justify-between">
          <button onClick={() => { setExpanded(!expanded); if (!expanded) loadRuns(); }}
            className="flex items-center gap-1 text-[11px] text-white/30 hover:text-white/60 transition-colors">
            {expanded ? <ChevronUp size={11} /> : <ChevronDown size={11} />}
            {expanded ? "Ocultar logs" : "Ver logs"}
          </button>
          <div className="flex gap-2 items-center">
            <button onClick={handleToggle} title={agent.enabled ? "Desactivar" : "Activar"}>
              {agent.enabled
                ? <ToggleRight size={18} className="text-emerald-400 hover:text-emerald-300 transition-colors" />
                : <ToggleLeft size={18} className="text-white/30 hover:text-white/60 transition-colors" />}
            </button>
            <button onClick={handleRun} disabled={running}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-violet-600 hover:bg-violet-700 text-white text-xs transition-colors disabled:opacity-50">
              <Play size={9} /> {running ? "Ejecutando..." : "Ejecutar"}
            </button>
          </div>
        </div>
      </div>

      {/* Logs */}
      {expanded && (
        <div className="border-t border-white/[0.05] px-4 py-3">
          <p className="text-[10px] text-white/30 uppercase tracking-wider mb-2">Últimas ejecuciones</p>
          {runs.length === 0 ? (
            <p className="text-xs text-white/20">Sin ejecuciones registradas</p>
          ) : (
            <div className="space-y-2">
              {runs.map((r) => (
                <div key={r.id} className="space-y-0.5">
                  <div className="flex items-center gap-2">
                    <span className={`text-[9px] px-1.5 py-0.5 rounded ${r.status === "success" ? "bg-emerald-500/15 text-emerald-400" : r.status === "error" ? "bg-red-500/15 text-red-400" : "bg-violet-500/15 text-violet-400"}`}>
                      {r.status}
                    </span>
                    <span className="text-[10px] text-white/30">{new Date(r.started_at).toLocaleString("es-AR")}</span>
                    {r.duration_ms && <span className="text-[10px] text-white/20">{(r.duration_ms / 1000).toFixed(1)}s</span>}
                  </div>
                  {r.logs.slice(-2).map((log: string, i: number) => (
                    <p key={i} className="font-mono text-[10px] text-white/35 pl-2">{log}</p>
                  ))}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────
export default function AgentsPage() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [filter, setFilter] = useState<FilterKey>("all");
  const [showModal, setShowModal] = useState(false);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    const a = await getAgents();
    setAgents(a);
    setLoading(false);
  }, []);

  useEffect(() => {
    load();
    const channel = subscribeToAgents((updated) => setAgents(updated));
    return () => { channel.unsubscribe(); };
  }, [load]);

  const filtered = filter === "all" ? agents
    : filter === "global" ? agents.filter(a => !a.project_id)
    : agents.filter(a => a.project_id === filter);

  const activeCount = agents.filter(a => a.enabled || a.status === "running").length;

  if (loading) return (
    <div className="flex items-center justify-center h-64">
      <div className="w-6 h-6 border-2 border-violet-500 border-t-transparent rounded-full animate-spin" />
    </div>
  );

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      {showModal && <NewAgentModal onClose={() => setShowModal(false)} onCreated={load} />}

      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-white">Agentes IA</h1>
          <p className="text-sm text-white/40 mt-0.5">{activeCount} activos de {agents.length} agentes</p>
        </div>
        <button onClick={() => setShowModal(true)}
          className="flex items-center gap-2 px-4 py-2 rounded-lg bg-violet-600 hover:bg-violet-700 text-white text-sm transition-colors self-start">
          <Plus size={13} /> Nuevo Agente
        </button>
      </div>

      {/* Filters */}
      <div className="flex gap-1 p-1 bg-white/5 rounded-xl border border-white/[0.07] w-fit flex-wrap">
        {(Object.keys(FILTER_LABELS) as FilterKey[]).map((f) => (
          <button key={f} onClick={() => setFilter(f)}
            className={`px-3 py-1.5 rounded-lg text-xs transition-all ${filter === f ? "bg-violet-600 text-white font-medium" : "text-white/50 hover:text-white"}`}>
            {FILTER_LABELS[f]}
          </button>
        ))}
      </div>

      {/* Grid */}
      {filtered.length === 0 ? (
        <div className="text-center py-12 text-white/30 text-sm">
          Sin agentes en esta categoría — <button onClick={() => setShowModal(true)} className="text-violet-400 hover:underline">creá uno</button>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {filtered.map((a) => <AgentCard key={a.id} agent={a} onRefresh={load} />)}
        </div>
      )}
    </div>
  );
}
