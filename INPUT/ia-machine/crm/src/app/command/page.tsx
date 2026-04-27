"use client";
export const dynamic = "force-dynamic";
import { useState, useEffect, useCallback } from "react";
import {
  AlertTriangle, CheckCircle2, Clock, Play, Zap, Bot,
  ChevronDown, ChevronUp, RefreshCw, Circle, ArrowRight
} from "lucide-react";
import { getProjects, getAgents, startRun, finishRun } from "@/lib/db";
import type { Project, Agent } from "@/lib/supabase";

// ── Types ────────────────────────────────────────────────────────────────────

type TaskPriority = "critica" | "alta" | "media";
type TaskType = "blocker" | "agente" | "manual" | "pendiente";

interface Task {
  id: string;
  project_id: string;
  title: string;
  description: string;
  priority: TaskPriority;
  type: TaskType;
  agent_id?: string;       // si tiene agente que puede ejecutarlo
  can_auto: boolean;       // puede ejecutarse automáticamente
  done: boolean;
}

// ── Priority meta ────────────────────────────────────────────────────────────

const PRIORITY_META: Record<TaskPriority, { label: string; color: string; bg: string; order: number }> = {
  critica: { label: "Crítica", color: "text-red-400", bg: "bg-red-500/10 border-red-500/20", order: 0 },
  alta:    { label: "Alta",    color: "text-amber-400", bg: "bg-amber-500/10 border-amber-500/20", order: 1 },
  media:   { label: "Media",  color: "text-blue-400", bg: "bg-blue-500/10 border-blue-500/20", order: 2 },
};

const PROJECT_META: Record<string, { label: string; dot: string; accent: string }> = {
  "mente-pausada": { label: "Mente Pausada", dot: "bg-violet-400", accent: "text-violet-300" },
  "polt-mobilier": { label: "Polt Mobilier",  dot: "bg-amber-400",  accent: "text-amber-300"  },
  "cerebro":        { label: "Cerebro",        dot: "bg-cyan-400",   accent: "text-cyan-300"   },
};

const TYPE_ICONS: Record<TaskType, React.ElementType> = {
  blocker:  AlertTriangle,
  agente:   Bot,
  manual:   Circle,
  pendiente: Clock,
};

// ── Build task list from projects + agents ────────────────────────────────────

function buildTasks(projects: Project[], agents: Agent[]): Task[] {
  const tasks: Task[] = [];

  for (const p of projects) {
    const meta = PROJECT_META[p.id];
    if (!meta) continue;

    // Blockers → tareas críticas
    for (const b of p.blockers) {
      tasks.push({
        id: `blocker-${p.id}-${b.slice(0, 20)}`,
        project_id: p.id,
        title: b,
        description: "Blocker activo que frena el avance del proyecto. Requiere tu acción o decisión.",
        priority: "critica",
        type: "blocker",
        can_auto: false,
        done: false,
      });
    }

    // Pending tasks del proyecto
    for (const t of p.pending_tasks) {
      tasks.push({
        id: `task-${p.id}-${t.slice(0, 20)}`,
        project_id: p.id,
        title: t,
        description: "Tarea pendiente del proyecto.",
        priority: p.blockers.length > 0 ? "alta" : "media",
        type: "pendiente",
        can_auto: false,
        done: false,
      });
    }
  }

  // Agentes deshabilitados → tareas para activar
  for (const a of agents.filter((ag) => !ag.enabled)) {
    const projectMeta = PROJECT_META[a.project_id ?? ""];
    if (!projectMeta) continue;
    tasks.push({
      id: `agent-enable-${a.id}`,
      project_id: a.project_id ?? "",
      title: `Activar agente: ${a.name}`,
      description: a.description ?? `Activar este agente para que empiece a trabajar automáticamente. Schedule: ${a.schedule ?? "Manual"}.`,
      priority: "alta",
      type: "agente",
      agent_id: a.id,
      can_auto: true,
      done: false,
    });
  }

  // Agentes habilitados con runs pendientes → sugerir ejecución
  for (const a of agents.filter((ag) => ag.enabled && ag.status === "idle" && ag.runs_total === 0)) {
    const projectMeta = PROJECT_META[a.project_id ?? ""];
    if (!projectMeta) continue;
    tasks.push({
      id: `agent-run-${a.id}`,
      project_id: a.project_id ?? "",
      title: `Primera ejecución: ${a.name}`,
      description: `Este agente está activo pero nunca fue ejecutado. Ejecutalo para verificar que funciona.`,
      priority: "media",
      type: "agente",
      agent_id: a.id,
      can_auto: true,
      done: false,
    });
  }

  return tasks.sort((a, b) =>
    PRIORITY_META[a.priority].order - PRIORITY_META[b.priority].order
  );
}

// ── Task Card ─────────────────────────────────────────────────────────────────

function TaskCard({
  task, agents, onComplete, onRun, running,
}: {
  task: Task;
  agents: Agent[];
  onComplete: (id: string) => void;
  onRun: (task: Task) => Promise<void>;
  running: boolean;
}) {
  const [expanded, setExpanded] = useState(false);
  const pMeta = PRIORITY_META[task.priority];
  const projectMeta = PROJECT_META[task.project_id];
  const TypeIcon = TYPE_ICONS[task.type];
  const agent = agents.find((a) => a.id === task.agent_id);

  return (
    <div className={`rounded-xl border ${pMeta.bg} transition-all ${task.done ? "opacity-40" : ""}`}>
      <div className="flex items-start gap-3 p-4">
        {/* Checkbox */}
        <button
          onClick={() => onComplete(task.id)}
          className={`mt-0.5 w-5 h-5 rounded-md border flex items-center justify-center shrink-0 transition-all ${task.done ? "border-emerald-500 bg-emerald-500/20" : "border-white/20 hover:border-white/40"}`}
        >
          {task.done && <CheckCircle2 size={12} className="text-emerald-400" />}
        </button>

        {/* Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2 mb-1">
            <div className="flex items-center gap-2 flex-wrap">
              <TypeIcon size={12} className={pMeta.color} />
              <span className={`text-sm font-medium ${task.done ? "line-through text-white/30" : "text-white"}`}>{task.title}</span>
            </div>
            <div className="flex items-center gap-1.5 shrink-0">
              <span className={`text-[10px] px-2 py-0.5 rounded-full border ${pMeta.bg} ${pMeta.color} font-medium`}>
                {pMeta.label}
              </span>
              {projectMeta && (
                <span className="flex items-center gap-1 text-[10px] text-white/30">
                  <span className={`w-1.5 h-1.5 rounded-full ${projectMeta.dot}`} />
                  {projectMeta.label}
                </span>
              )}
            </div>
          </div>

          {/* Description toggle */}
          <button
            onClick={() => setExpanded(!expanded)}
            className="flex items-center gap-1 text-[11px] text-white/30 hover:text-white/50 transition-colors"
          >
            {expanded ? <ChevronUp size={10} /> : <ChevronDown size={10} />}
            {expanded ? "Ocultar detalle" : "Ver detalle"}
          </button>

          {expanded && (
            <p className="text-xs text-white/40 mt-2 leading-relaxed">{task.description}</p>
          )}

          {/* Agent info */}
          {agent && expanded && (
            <div className="mt-2 px-3 py-2 rounded-lg bg-white/5 border border-white/[0.07]">
              <p className="text-[10px] text-white/30 mb-0.5">Agente asociado</p>
              <p className="text-xs text-white/60">{agent.name}</p>
              {agent.schedule && <p className="text-[10px] text-white/30">{agent.schedule}</p>}
            </div>
          )}
        </div>

        {/* Action button */}
        {!task.done && task.can_auto && (
          <button
            onClick={() => onRun(task)}
            disabled={running}
            className="shrink-0 flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-violet-600 hover:bg-violet-700 text-white text-xs font-medium transition-colors disabled:opacity-50"
          >
            {running
              ? <><RefreshCw size={10} className="animate-spin" /> Ejecutando</>
              : <><Play size={10} /> Ejecutar</>
            }
          </button>
        )}
        {!task.done && !task.can_auto && (
          <div className="shrink-0 flex items-center gap-1 text-[10px] text-white/25 px-2">
            <ArrowRight size={10} />
            <span>Manual</span>
          </div>
        )}
      </div>
    </div>
  );
}

// ── Summary bar ───────────────────────────────────────────────────────────────

function SummaryBar({ tasks }: { tasks: Task[] }) {
  const total = tasks.length;
  const done = tasks.filter((t) => t.done).length;
  const criticas = tasks.filter((t) => t.priority === "critica" && !t.done).length;
  const autoRun = tasks.filter((t) => t.can_auto && !t.done).length;

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
      {[
        { label: "Total tareas", value: total, icon: Clock, color: "text-white/60" },
        { label: "Críticas activas", value: criticas, icon: AlertTriangle, color: "text-red-400" },
        { label: "Auto-ejecutables", value: autoRun, icon: Zap, color: "text-violet-400" },
        { label: "Completadas", value: done, icon: CheckCircle2, color: "text-emerald-400" },
      ].map((s) => (
        <div key={s.label} className="rounded-xl border border-white/[0.07] bg-white/[0.02] p-4">
          <div className="flex items-center gap-2 mb-1">
            <s.icon size={13} className={s.color} />
            <span className="text-[10px] text-white/30 uppercase tracking-wider">{s.label}</span>
          </div>
          <p className="text-2xl font-bold text-white">{s.value}</p>
        </div>
      ))}
    </div>
  );
}

// ── Main ─────────────────────────────────────────────────────────────────────

export default function CommandPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [runningIds, setRunningIds] = useState<Set<string>>(new Set());
  const [filterProject, setFilterProject] = useState<string>("all");
  const [filterPriority, setFilterPriority] = useState<string>("all");

  const load = useCallback(async () => {
    const [p, a] = await Promise.all([getProjects(), getAgents()]);
    setProjects(p);
    setAgents(a);
    setTasks((prev) => {
      const built = buildTasks(p, a);
      // Preserve done state
      const doneIds = new Set(prev.filter((t) => t.done).map((t) => t.id));
      return built.map((t) => ({ ...t, done: doneIds.has(t.id) }));
    });
    setLoading(false);
  }, []);

  useEffect(() => {
    load();
    const interval = setInterval(load, 60000);
    return () => clearInterval(interval);
  }, [load]);

  function markDone(id: string) {
    setTasks((prev) => prev.map((t) => t.id === id ? { ...t, done: !t.done } : t));
  }

  async function runTask(task: Task) {
    if (!task.agent_id || runningIds.has(task.id)) return;
    setRunningIds((prev) => new Set(prev).add(task.id));

    const runId = await startRun(task.agent_id, task.project_id, "manual");
    setTimeout(async () => {
      const logs = [
        `[${new Date().toLocaleTimeString("es-AR", { hour: "2-digit", minute: "2-digit" })}] Ejecutado desde Command Center`,
        `[${new Date().toLocaleTimeString("es-AR", { hour: "2-digit", minute: "2-digit" })}] Completado ✓`,
      ];
      await finishRun(runId, task.agent_id!, "success", { source: "command" }, logs);
      setRunningIds((prev) => { const s = new Set(prev); s.delete(task.id); return s; });
      markDone(task.id);
      await load();
    }, 3000);
  }

  async function runAllAuto() {
    const autoTasks = tasks.filter((t) => t.can_auto && !t.done && t.agent_id);
    for (const t of autoTasks) {
      await runTask(t);
      await new Promise((r) => setTimeout(r, 500));
    }
  }

  const filtered = tasks.filter((t) => {
    if (filterProject !== "all" && t.project_id !== filterProject) return false;
    if (filterPriority !== "all" && t.priority !== filterPriority) return false;
    return true;
  });

  const projectIds = ["all", ...Array.from(new Set(tasks.map((t) => t.project_id)))];

  if (loading) return (
    <div className="flex items-center justify-center h-64">
      <div className="w-6 h-6 border-2 border-violet-500 border-t-transparent rounded-full animate-spin" />
    </div>
  );

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-white">Command Center</h1>
          <p className="text-sm text-white/30 mt-0.5">Tareas urgentes · Aprobá, ejecutá, automatizá</p>
        </div>
        <div className="flex gap-2">
          <button onClick={load} className="p-2 rounded-lg bg-white/5 hover:bg-white/10 border border-white/[0.07] transition-colors">
            <RefreshCw size={13} className="text-white/50" />
          </button>
          <button
            onClick={runAllAuto}
            disabled={tasks.filter((t) => t.can_auto && !t.done).length === 0}
            className="flex items-center gap-2 px-4 py-2 bg-violet-600 hover:bg-violet-700 text-white text-sm rounded-lg transition-colors disabled:opacity-40"
          >
            <Zap size={13} />
            Ejecutar todas las auto ({tasks.filter((t) => t.can_auto && !t.done).length})
          </button>
        </div>
      </div>

      {/* Summary */}
      <SummaryBar tasks={tasks} />

      {/* Filters */}
      <div className="flex gap-3 flex-wrap">
        <div className="flex gap-1 p-1 bg-white/5 rounded-lg border border-white/[0.07]">
          {projectIds.map((pid) => (
            <button
              key={pid}
              onClick={() => setFilterProject(pid)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs transition-all ${filterProject === pid ? "bg-violet-600 text-white" : "text-white/50 hover:text-white"}`}
            >
              {pid !== "all" && PROJECT_META[pid] && (
                <span className={`w-1.5 h-1.5 rounded-full ${PROJECT_META[pid].dot}`} />
              )}
              {pid === "all" ? "Todos" : PROJECT_META[pid]?.label ?? pid}
            </button>
          ))}
        </div>
        <div className="flex gap-1 p-1 bg-white/5 rounded-lg border border-white/[0.07]">
          {(["all", "critica", "alta", "media"] as const).map((p) => (
            <button
              key={p}
              onClick={() => setFilterPriority(p)}
              className={`px-3 py-1.5 rounded-md text-xs transition-all ${filterPriority === p ? "bg-violet-600 text-white" : "text-white/50 hover:text-white"}`}
            >
              {p === "all" ? "Todas" : PRIORITY_META[p].label}
            </button>
          ))}
        </div>
      </div>

      {/* Task list */}
      <div className="space-y-2">
        {filtered.length === 0 && (
          <div className="text-center py-16 text-sm text-white/30">
            <CheckCircle2 size={32} className="text-emerald-500/30 mx-auto mb-3" />
            Sin tareas para los filtros seleccionados
          </div>
        )}
        {filtered.map((task) => (
          <TaskCard
            key={task.id}
            task={task}
            agents={agents}
            onComplete={markDone}
            onRun={runTask}
            running={runningIds.has(task.id)}
          />
        ))}
      </div>
    </div>
  );
}
