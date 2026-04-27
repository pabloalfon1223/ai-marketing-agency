"use client";
export const dynamic = "force-dynamic";
import { useEffect, useState, useCallback } from "react";
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import {
  TrendingUp, TrendingDown, DollarSign, Bot, AlertTriangle,
  CheckCircle2, Play, RefreshCw, Zap, Clock, ChevronRight
} from "lucide-react";
import { getProjects, getAgents, getRuns, startRun, finishRun } from "@/lib/db";
import type { Project, Agent, Run } from "@/lib/supabase";

// ── Helpers ──────────────────────────────────────────────────────────────────

function fmt(n: number, currency: string) {
  if (currency === "USD") return `$${n.toLocaleString("en")} USD`;
  return `$${(n / 1000).toFixed(0)}k ARS`;
}

function pct(a: number, b: number) {
  return b > 0 ? Math.min(Math.round((a / b) * 100), 100) : 0;
}

const PROJECT_META: Record<string, { color: string; accent: string; dot: string; label: string }> = {
  "mente-pausada": {
    label: "Mente Pausada",
    color: "border-violet-500/30 bg-violet-500/5",
    accent: "bg-violet-500",
    dot: "bg-violet-400",
  },
  "polt-mobilier": {
    label: "Polt Mobilier",
    color: "border-amber-500/30 bg-amber-500/5",
    accent: "bg-amber-500",
    dot: "bg-amber-400",
  },
  cerebro: {
    label: "Cerebro",
    color: "border-cyan-500/30 bg-cyan-500/5",
    accent: "bg-cyan-500",
    dot: "bg-cyan-400",
  },
};

// ── Project Card ─────────────────────────────────────────────────────────────

function ProjectCard({
  project, agents, runs, onRunAgent,
}: {
  project: Project;
  agents: Agent[];
  runs: Run[];
  onRunAgent: (agent: Agent) => Promise<void>;
}) {
  const meta = PROJECT_META[project.id] ?? PROJECT_META["cerebro"];
  const goalPct = pct(project.revenue_month, project.revenue_goal);
  const activeAgents = agents.filter((a) => a.enabled);
  const runningAgents = agents.filter((a) => a.status === "running");
  const projectRuns = runs.filter((r) => r.project_id === project.id);

  // Chart: agent runs per day last 7 days
  const chartData = Array.from({ length: 7 }, (_, i) => {
    const d = new Date();
    d.setDate(d.getDate() - (6 - i));
    return {
      date: d.toLocaleDateString("es-AR", { day: "2-digit", month: "short" }),
      runs: projectRuns.filter((r) => new Date(r.started_at).toDateString() === d.toDateString()).length,
    };
  });

  return (
    <div className={`rounded-2xl border ${meta.color} p-5 flex flex-col gap-4`}>
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className={`w-2 h-2 rounded-full ${meta.dot} ${runningAgents.length > 0 ? "animate-pulse" : ""}`} />
            <h2 className="text-sm font-bold text-white">{meta.label}</h2>
          </div>
          <p className="text-[11px] text-white/40">
            {activeAgents.length} agentes activos · {runningAgents.length > 0 ? `${runningAgents.length} ejecutando` : "en espera"}
          </p>
        </div>
        <div className="text-right">
          <p className="text-lg font-bold text-white">{fmt(project.revenue_month, project.currency)}</p>
          <p className="text-[11px] text-white/30">de {fmt(project.revenue_goal, project.currency)}</p>
        </div>
      </div>

      {/* Progress bar */}
      <div>
        <div className="flex justify-between text-[10px] text-white/30 mb-1.5">
          <span>Meta mensual</span>
          <span>{goalPct}%</span>
        </div>
        <div className="w-full h-1.5 bg-white/10 rounded-full overflow-hidden">
          <div
            className={`h-full rounded-full transition-all duration-700 ${goalPct >= 80 ? "bg-emerald-500" : goalPct >= 40 ? meta.accent : "bg-red-500"}`}
            style={{ width: `${goalPct}%` }}
          />
        </div>
      </div>

      {/* Mini chart */}
      <div className="h-[70px]">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id={`grad-${project.id}`} x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={meta.dot.replace("bg-", "#").replace("-400", "")} stopOpacity={0.3} />
                <stop offset="95%" stopOpacity={0} />
              </linearGradient>
            </defs>
            <XAxis dataKey="date" hide />
            <YAxis hide />
            <Tooltip
              contentStyle={{ background: "#1a1a2e", border: "1px solid #ffffff15", borderRadius: 6, color: "#fff", fontSize: 11 }}
              labelStyle={{ color: "#ffffff60" }}
            />
            <Area type="monotone" dataKey="runs" stroke="#7c3aed" strokeWidth={1.5} fill={`url(#grad-${project.id})`} />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* Agents */}
      <div className="space-y-1.5">
        <p className="text-[10px] text-white/30 uppercase tracking-wider">Agentes</p>
        {agents.length === 0 && (
          <p className="text-xs text-white/20 py-2 text-center">Sin agentes configurados</p>
        )}
        {agents.slice(0, 4).map((a) => (
          <div key={a.id} className="flex items-center justify-between py-1.5 px-2.5 rounded-lg bg-white/[0.03] border border-white/[0.05] group">
            <div className="flex items-center gap-2 min-w-0">
              <span className={`w-1.5 h-1.5 rounded-full shrink-0 ${a.status === "running" ? "bg-violet-400 animate-pulse" : a.enabled ? "bg-emerald-400" : "bg-white/20"}`} />
              <span className="text-xs text-white/60 truncate">{a.name}</span>
            </div>
            <div className="flex items-center gap-1.5 shrink-0">
              <span className="text-[10px] text-white/20">{a.schedule ?? "Manual"}</span>
              <button
                onClick={() => onRunAgent(a)}
                disabled={a.status === "running"}
                className="opacity-0 group-hover:opacity-100 transition-opacity w-5 h-5 rounded bg-violet-600/30 hover:bg-violet-600 flex items-center justify-center disabled:opacity-30"
              >
                {a.status === "running" ? <RefreshCw size={9} className="text-violet-300 animate-spin" /> : <Play size={9} className="text-white" />}
              </button>
            </div>
          </div>
        ))}
        {agents.length > 4 && (
          <p className="text-[10px] text-white/20 text-right px-1">+{agents.length - 4} más →</p>
        )}
      </div>

      {/* Blockers */}
      {project.blockers.length > 0 && (
        <div className="space-y-1">
          <p className="text-[10px] text-white/30 uppercase tracking-wider">Blockers</p>
          {project.blockers.slice(0, 2).map((b: string, i: number) => (
            <div key={i} className="flex items-start gap-1.5 px-2 py-1.5 rounded-lg bg-red-500/5 border border-red-500/15">
              <AlertTriangle size={10} className="text-red-400 mt-0.5 shrink-0" />
              <span className="text-[11px] text-red-300/70 leading-tight">{b}</span>
            </div>
          ))}
          {project.blockers.length > 2 && (
            <p className="text-[10px] text-white/20 px-1">+{project.blockers.length - 2} más</p>
          )}
        </div>
      )}

      {/* Footer link */}
      <a href="/command" className="flex items-center justify-between px-3 py-2 rounded-lg bg-white/[0.03] hover:bg-white/[0.06] border border-white/[0.05] transition-colors group">
        <span className="text-xs text-white/40 group-hover:text-white/60 transition-colors">Ver tareas pendientes</span>
        <ChevronRight size={12} className="text-white/30 group-hover:text-white/50 transition-colors" />
      </a>
    </div>
  );
}

// ── Recent Activity ──────────────────────────────────────────────────────────

function ActivityFeed({ runs, agents }: { runs: Run[]; agents: Agent[] }) {
  const agentMap = Object.fromEntries(agents.map((a) => [a.id, a.name]));
  return (
    <div className="rounded-2xl border border-white/[0.07] bg-white/[0.02] p-5">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-sm font-semibold text-white">Actividad reciente</h2>
        <a href="/agents" className="text-xs text-violet-400 hover:text-violet-300 transition-colors">Ver todos →</a>
      </div>
      <div className="space-y-2">
        {runs.length === 0 && <p className="text-xs text-white/30 text-center py-4">Sin actividad reciente</p>}
        {runs.slice(0, 8).map((r) => (
          <div key={r.id} className="flex items-center gap-3 py-1.5">
            <span className={`w-1.5 h-1.5 rounded-full shrink-0 ${r.status === "success" ? "bg-emerald-400" : r.status === "error" ? "bg-red-400" : "bg-violet-400 animate-pulse"}`} />
            <span className="text-xs text-white/60 flex-1 truncate">{agentMap[r.agent_id] ?? r.agent_id}</span>
            <span className={`text-[10px] px-1.5 py-0.5 rounded-full ${r.status === "success" ? "bg-emerald-500/15 text-emerald-400" : r.status === "error" ? "bg-red-500/15 text-red-400" : "bg-violet-500/15 text-violet-400"}`}>
              {r.status}
            </span>
            <span className="text-[10px] text-white/20 shrink-0">{new Date(r.started_at).toLocaleTimeString("es-AR", { hour: "2-digit", minute: "2-digit" })}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

// ── Global KPIs ──────────────────────────────────────────────────────────────

function GlobalKPIs({ projects, agents, runs }: { projects: Project[]; agents: Agent[]; runs: Run[] }) {
  const totalRunsToday = runs.filter((r) => new Date(r.started_at).toDateString() === new Date().toDateString()).length;
  const successRate = runs.length > 0 ? Math.round((runs.filter((r) => r.status === "success").length / runs.length) * 100) : 100;
  const activeAgents = agents.filter((a) => a.enabled).length;
  const totalBlockers = projects.reduce((sum, p) => sum + p.blockers.length, 0);

  const cards = [
    { label: "Agentes activos", value: `${activeAgents}`, sub: `de ${agents.length} total`, icon: Bot, trend: activeAgents > 0 ? "up" : "neutral" as const },
    { label: "Runs hoy", value: `${totalRunsToday}`, sub: `${successRate}% éxito`, icon: Zap, trend: "up" as const },
    { label: "Blockers globales", value: `${totalBlockers}`, sub: "a resolver", icon: AlertTriangle, trend: totalBlockers > 0 ? "down" : "up" as const },
    { label: "Proyectos activos", value: `${projects.length}`, sub: "en operación", icon: TrendingUp, trend: "neutral" as const },
  ];

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
      {cards.map((c) => (
        <div key={c.label} className="rounded-xl border border-white/[0.07] bg-white/[0.02] p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-[10px] text-white/30 uppercase tracking-wider">{c.label}</span>
            <c.icon size={13} className="text-white/30" />
          </div>
          <p className="text-xl font-bold text-white">{c.value}</p>
          <div className="flex items-center gap-1 mt-0.5">
            {c.trend === "up" && <TrendingUp size={10} className="text-emerald-400" />}
            {c.trend === "down" && <TrendingDown size={10} className="text-red-400" />}
            <span className="text-[10px] text-white/30">{c.sub}</span>
          </div>
        </div>
      ))}
    </div>
  );
}

// ── Main ─────────────────────────────────────────────────────────────────────

export default function Dashboard() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [runs, setRuns] = useState<Run[]>([]);
  const [loading, setLoading] = useState(true);
  const [runningIds, setRunningIds] = useState<Set<string>>(new Set());

  const load = useCallback(async () => {
    const [p, a, r] = await Promise.all([getProjects(), getAgents(), getRuns(undefined, 30)]);
    setProjects(p);
    setAgents(a);
    setRuns(r);
    setLoading(false);
  }, []);

  useEffect(() => {
    load();
    const interval = setInterval(load, 30000); // refresh cada 30s
    return () => clearInterval(interval);
  }, [load]);

  async function handleRunAgent(agent: Agent) {
    if (runningIds.has(agent.id)) return;
    setRunningIds((prev) => new Set(prev).add(agent.id));
    setAgents((prev) => prev.map((a) => a.id === agent.id ? { ...a, status: "running" } : a));

    const runId = await startRun(agent.id, agent.project_id, "manual");
    setTimeout(async () => {
      const logs = [
        `[${new Date().toLocaleTimeString("es-AR", { hour: "2-digit", minute: "2-digit" })}] Ejecución manual iniciada`,
        `[${new Date().toLocaleTimeString("es-AR", { hour: "2-digit", minute: "2-digit" })}] Procesando...`,
        `[${new Date().toLocaleTimeString("es-AR", { hour: "2-digit", minute: "2-digit" })}] Completado ✓`,
      ];
      await finishRun(runId, agent.id, "success", { triggered: "manual" }, logs);
      setRunningIds((prev) => { const s = new Set(prev); s.delete(agent.id); return s; });
      await load();
    }, 3000);
  }

  if (loading) return (
    <div className="flex items-center justify-center h-64">
      <div className="w-6 h-6 border-2 border-violet-500 border-t-transparent rounded-full animate-spin" />
    </div>
  );

  return (
    <div className="max-w-[1400px] mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-white">Control Center</h1>
          <p className="text-sm text-white/30 mt-0.5">{new Date().toLocaleDateString("es-AR", { dateStyle: "long" })}</p>
        </div>
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-[11px] text-emerald-400 font-medium">Sistema operativo</span>
          </div>
          <button onClick={load} className="p-2 rounded-lg bg-white/5 hover:bg-white/10 border border-white/[0.07] transition-colors">
            <RefreshCw size={13} className="text-white/50" />
          </button>
        </div>
      </div>

      {/* Global KPIs */}
      <GlobalKPIs projects={projects} agents={agents} runs={runs} />

      {/* Projects — los 3 visibles a la vez */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {projects.map((p) => (
          <ProjectCard
            key={p.id}
            project={p}
            agents={agents.filter((a) => a.project_id === p.id)}
            runs={runs}
            onRunAgent={handleRunAgent}
          />
        ))}
      </div>

      {/* Activity feed */}
      <ActivityFeed runs={runs} agents={agents} />
    </div>
  );
}
