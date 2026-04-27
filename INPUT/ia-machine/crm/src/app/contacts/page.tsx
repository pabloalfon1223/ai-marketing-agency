"use client";
export const dynamic = "force-dynamic";
import { useState, useEffect } from "react";
import { getContacts } from "@/lib/db";
import type { Contact, PipelineStage } from "@/lib/supabase";
import { Search } from "lucide-react";

type ProjectFilter = "mente-pausada" | "polt-mobilier" | "cerebro" | "all";

const projectLabels: Record<string, string> = {
  "mente-pausada": "Mente Pausada",
  "polt-mobilier": "Polt Mobilier",
  cerebro: "Cerebro",
};

const stageLabels: Record<PipelineStage, string> = {
  nuevo: "Nuevo",
  calificado: "Calificado",
  propuesta: "Propuesta",
  negociacion: "Negociación",
  "cerrado-ganado": "Cerrado ✓",
  "cerrado-perdido": "Perdido ✗",
};

const stageColors: Record<PipelineStage, string> = {
  nuevo: "bg-slate-500",
  calificado: "bg-blue-500",
  propuesta: "bg-yellow-500",
  negociacion: "bg-orange-500",
  "cerrado-ganado": "bg-green-500",
  "cerrado-perdido": "bg-red-500",
};

function fmt(n: number, currency: string) {
  return currency === "USD" ? `$${n}` : `$${(n / 1000).toFixed(0)}k ARS`;
}

export default function ContactsPage() {
  const [contacts, setContacts] = useState<Contact[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [project, setProject] = useState<ProjectFilter>("all");

  useEffect(() => {
    getContacts().then((data) => { setContacts(data); setLoading(false); }).catch(() => setLoading(false));
  }, []);

  const filtered = contacts.filter((c) => {
    const matchProject = project === "all" || c.project_id === project;
    const matchSearch =
      c.name.toLowerCase().includes(search.toLowerCase()) ||
      (c.email ?? "").toLowerCase().includes(search.toLowerCase());
    return matchProject && matchSearch;
  });

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <div>
        <h1 className="text-xl font-bold text-white">Contactos</h1>
        <p className="text-sm text-white/40 mt-0.5">{filtered.length} contactos</p>
      </div>

      <div className="flex gap-3 flex-wrap">
        <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-white/5 border border-white/[0.07] flex-1 min-w-[200px]">
          <Search size={14} className="text-white/40" />
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Buscar por nombre o email..."
            className="bg-transparent text-sm text-white placeholder-white/30 outline-none flex-1"
          />
        </div>
        <div className="flex gap-1 p-1 bg-white/5 rounded-lg border border-white/[0.07]">
          {(["all", "mente-pausada", "polt-mobilier", "cerebro"] as ProjectFilter[]).map((p) => (
            <button
              key={p}
              onClick={() => setProject(p)}
              className={`px-3 py-1.5 rounded-md text-xs transition-all ${project === p ? "bg-violet-600 text-white" : "text-white/50 hover:text-white"}`}
            >
              {p === "all" ? "Todos" : projectLabels[p]}
            </button>
          ))}
        </div>
      </div>

      <div className="rounded-xl border border-white/[0.07] bg-white/[0.02] overflow-hidden">
        <div className="grid grid-cols-[2fr_2fr_1fr_1fr_1fr] gap-4 px-4 py-3 border-b border-white/[0.06] text-[10px] text-white/30 uppercase tracking-wider">
          <span>Contacto</span><span>Proyecto</span><span>Valor</span><span>Etapa</span><span>Tags</span>
        </div>
        <div className="divide-y divide-white/[0.04]">
          {loading && (
            <div className="px-4 py-12 text-center text-sm text-white/30">Cargando...</div>
          )}
          {!loading && filtered.map((c) => (
            <div key={c.id} className="grid grid-cols-[2fr_2fr_1fr_1fr_1fr] gap-4 px-4 py-3 hover:bg-white/[0.02] transition-colors items-center">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-violet-600/20 flex items-center justify-center text-violet-300 text-sm font-bold shrink-0">
                  {c.name[0]}
                </div>
                <div className="min-w-0">
                  <p className="text-sm text-white font-medium truncate">{c.name}</p>
                  <p className="text-xs text-white/30 truncate">{c.email ?? "—"}</p>
                </div>
              </div>
              <span className="text-xs text-white/50">{projectLabels[c.project_id] ?? c.project_id}</span>
              <span className="text-sm font-medium text-white">{fmt(c.value, c.currency)}</span>
              <span className={`text-[10px] px-2 py-0.5 rounded-full text-white w-fit ${stageColors[c.stage]}`}>
                {stageLabels[c.stage]}
              </span>
              <div className="flex gap-1 flex-wrap">
                {c.tags.slice(0, 1).map((t) => (
                  <span key={t} className="text-[10px] bg-white/5 text-white/40 px-1.5 py-0.5 rounded">{t}</span>
                ))}
              </div>
            </div>
          ))}
          {!loading && filtered.length === 0 && (
            <div className="px-4 py-12 text-center text-sm text-white/30">Sin contactos para los filtros seleccionados.</div>
          )}
        </div>
      </div>
    </div>
  );
}
