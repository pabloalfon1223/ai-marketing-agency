"use client";
export const dynamic = "force-dynamic";
import { useState, useEffect } from "react";
import { getContacts, updateContactStage } from "@/lib/db";
import type { Contact, PipelineStage } from "@/lib/supabase";
import { Plus, DollarSign, User } from "lucide-react";

type ProjectId = "mente-pausada" | "polt-mobilier" | "cerebro";

const STAGES: PipelineStage[] = ["nuevo", "calificado", "propuesta", "negociacion", "cerrado-ganado", "cerrado-perdido"];
const PROJECTS: ProjectId[] = ["mente-pausada", "polt-mobilier", "cerebro"];

const projectLabels: Record<ProjectId, string> = {
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
  return currency === "USD" ? `$${n}` : `$${(n / 1000).toFixed(0)}k`;
}

function ContactCard({ contact, onMove }: { contact: Contact; onMove: (id: string, stage: PipelineStage) => void }) {
  return (
    <div className="bg-white/[0.04] border border-white/[0.07] rounded-lg p-3 cursor-grab hover:bg-white/[0.07] transition-colors group">
      <div className="flex items-start justify-between gap-2 mb-2">
        <div className="flex items-center gap-2 min-w-0">
          <div className="w-6 h-6 rounded-full bg-violet-600/30 flex items-center justify-center text-violet-300 text-xs font-bold shrink-0">
            {contact.name[0]}
          </div>
          <span className="text-sm text-white font-medium truncate">{contact.name}</span>
        </div>
        <span className="text-sm font-bold text-emerald-400 shrink-0">{fmt(contact.value, contact.currency)}</span>
      </div>
      {contact.notes && <p className="text-xs text-white/30 mb-2 line-clamp-2">{contact.notes}</p>}
      <div className="flex flex-wrap gap-1 mb-2">
        {contact.tags.slice(0, 2).map((t) => (
          <span key={t} className="text-[10px] bg-white/5 text-white/40 px-1.5 py-0.5 rounded">{t}</span>
        ))}
      </div>
      <div className="hidden group-hover:flex gap-1 mt-1">
        {STAGES.filter((s) => s !== contact.stage).slice(0, 3).map((s) => (
          <button
            key={s}
            onClick={() => onMove(contact.id, s)}
            className="text-[9px] px-1.5 py-0.5 rounded bg-white/5 text-white/40 hover:text-white hover:bg-violet-600/30 transition-colors"
          >
            → {stageLabels[s]}
          </button>
        ))}
      </div>
    </div>
  );
}

export default function PipelinePage() {
  const [contacts, setContacts] = useState<Contact[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeProject, setActiveProject] = useState<ProjectId>("mente-pausada");

  useEffect(() => {
    getContacts().then((data) => { setContacts(data); setLoading(false); }).catch(() => setLoading(false));
  }, []);

  const filtered = contacts.filter((c) => c.project_id === activeProject);
  const totalValue = filtered.filter((c) => c.stage === "cerrado-ganado").reduce((sum, c) => sum + c.value, 0);
  const currency = activeProject === "polt-mobilier" ? "ARS" : "USD";

  async function moveContact(id: string, newStage: PipelineStage) {
    setContacts((prev) => prev.map((c) => (c.id === id ? { ...c, stage: newStage } : c)));
    await updateContactStage(id, newStage);
  }

  return (
    <div className="max-w-full space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-white">Pipeline de Ventas</h1>
          <p className="text-sm text-white/40 mt-0.5">
            Cerrado: {currency === "USD" ? `$${totalValue}` : `$${(totalValue / 1000).toFixed(0)}k ARS`}
          </p>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex gap-1 p-1 bg-white/5 rounded-xl border border-white/[0.07]">
            {PROJECTS.map((p) => (
              <button
                key={p}
                onClick={() => setActiveProject(p)}
                className={`px-4 py-1.5 rounded-lg text-sm transition-all ${activeProject === p ? "bg-violet-600 text-white font-medium" : "text-white/50 hover:text-white"}`}
              >
                {projectLabels[p]}
              </button>
            ))}
          </div>
          <button className="flex items-center gap-2 px-4 py-2 bg-violet-600 hover:bg-violet-700 text-white text-sm rounded-lg transition-colors">
            <Plus size={14} /> Nuevo Lead
          </button>
        </div>
      </div>

      {loading ? (
        <div className="text-center text-sm text-white/30 py-20">Cargando pipeline...</div>
      ) : (
        <div className="flex gap-3 overflow-x-auto pb-4">
          {STAGES.map((stage) => {
            const stageContacts = filtered.filter((c) => c.stage === stage);
            const stageValue = stageContacts.reduce((sum, c) => sum + c.value, 0);
            return (
              <div key={stage} className="shrink-0 w-64">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <span className={`w-2 h-2 rounded-full ${stageColors[stage]}`} />
                    <span className="text-sm font-medium text-white/80">{stageLabels[stage]}</span>
                    <span className="text-xs bg-white/5 text-white/40 px-1.5 py-0.5 rounded-full">{stageContacts.length}</span>
                  </div>
                  <div className="flex items-center gap-1 text-xs text-white/30">
                    <DollarSign size={10} />
                    {currency === "USD" ? stageValue : `${(stageValue / 1000).toFixed(0)}k`}
                  </div>
                </div>
                <div className="space-y-2 min-h-[100px] bg-white/[0.01] rounded-xl p-2 border border-white/[0.04]">
                  {stageContacts.map((c) => <ContactCard key={c.id} contact={c} onMove={moveContact} />)}
                  {stageContacts.length === 0 && (
                    <div className="flex flex-col items-center justify-center h-20 text-white/15 text-xs gap-1">
                      <User size={16} /><span>Sin contactos</span>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}

      <div className="flex gap-4 p-4 rounded-xl border border-white/[0.07] bg-white/[0.02]">
        {STAGES.map((stage) => (
          <div key={stage} className="flex-1 text-center">
            <p className="text-lg font-bold text-white">{filtered.filter((c) => c.stage === stage).length}</p>
            <p className="text-[10px] text-white/30 mt-0.5">{stageLabels[stage]}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
