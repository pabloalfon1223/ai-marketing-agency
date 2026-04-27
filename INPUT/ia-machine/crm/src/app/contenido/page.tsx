"use client";
export const dynamic = "force-dynamic";
import { useState, useEffect, useCallback } from "react";
import { supabase } from "@/lib/supabase";
import { CheckCircle2, XCircle, Copy, RefreshCw, Film, LayoutGrid, MessageCircle, Mail, Check } from "lucide-react";

interface ContentItem {
  id: string;
  project_id: string;
  agent_id: string;
  format: string;
  platform: string;
  hook: string | null;
  body: string | null;
  cta: string | null;
  visual_prompt: string | null;
  caption: string | null;
  hashtags: string[];
  status: string;
  created_at: string;
}

const PROJECT_META: Record<string, { label: string; dot: string }> = {
  "mente-pausada": { label: "Mente Pausada", dot: "bg-violet-400" },
  "polt-mobilier":  { label: "Polt Mobilier",  dot: "bg-amber-400"  },
  "cerebro":        { label: "Cerebro",         dot: "bg-cyan-400"  },
};

const FORMAT_ICONS: Record<string, React.ElementType> = {
  reel:     Film,
  carrusel: LayoutGrid,
  post:     MessageCircle,
  email:    Mail,
  story:    Film,
};

const STATUS_META: Record<string, { label: string; color: string; bg: string }> = {
  draft:     { label: "Borrador",   color: "text-white/50",   bg: "bg-white/5 border-white/10" },
  approved:  { label: "Aprobado",   color: "text-emerald-400", bg: "bg-emerald-500/10 border-emerald-500/20" },
  published: { label: "Publicado",  color: "text-blue-400",   bg: "bg-blue-500/10 border-blue-500/20" },
  rejected:  { label: "Rechazado",  color: "text-red-400",    bg: "bg-red-500/10 border-red-500/20" },
};

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);
  function copy() {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }
  return (
    <button onClick={copy} className="flex items-center gap-1 text-[10px] px-2 py-1 rounded bg-white/5 hover:bg-white/10 text-white/40 hover:text-white transition-colors">
      {copied ? <><Check size={10} className="text-emerald-400" /> Copiado</> : <><Copy size={10} /> Copiar</>}
    </button>
  );
}

function ContentCard({ item, onStatusChange }: { item: ContentItem; onStatusChange: () => void }) {
  const [updating, setUpdating] = useState(false);
  const FormatIcon = FORMAT_ICONS[item.format] ?? MessageCircle;
  const statusMeta = STATUS_META[item.status] ?? STATUS_META.draft;
  const projectMeta = PROJECT_META[item.project_id];

  async function updateStatus(newStatus: string) {
    setUpdating(true);
    await supabase.from("content_output").update({ status: newStatus }).eq("id", item.id);
    setUpdating(false);
    onStatusChange();
  }

  const fullText = [item.hook, item.body, item.cta, item.caption, item.hashtags?.map((h: string) => `#${h}`).join(" ")].filter(Boolean).join("\n\n");

  return (
    <div className={`rounded-2xl border ${statusMeta.bg} p-5 flex flex-col gap-4`}>
      {/* Header */}
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-white/5 border border-white/[0.07] flex items-center justify-center">
            <FormatIcon size={14} className="text-white/50" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-sm font-semibold text-white capitalize">{item.format}</span>
              <span className="text-[10px] text-white/30">· {item.platform}</span>
            </div>
            <div className="flex items-center gap-1.5 mt-0.5">
              {projectMeta && <span className={`w-1.5 h-1.5 rounded-full ${projectMeta.dot}`} />}
              <span className="text-[10px] text-white/30">{projectMeta?.label ?? item.project_id}</span>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          <span className={`text-[10px] px-2 py-0.5 rounded-full border ${statusMeta.bg} ${statusMeta.color} font-medium`}>
            {statusMeta.label}
          </span>
          <span className="text-[10px] text-white/20">
            {new Date(item.created_at).toLocaleDateString("es-AR")}
          </span>
        </div>
      </div>

      {/* Hook */}
      {item.hook && (
        <div className="space-y-1">
          <p className="text-[10px] text-white/30 uppercase tracking-wider">Hook</p>
          <p className="text-sm text-white font-medium leading-snug">{item.hook}</p>
        </div>
      )}

      {/* Body */}
      {item.body && (
        <div className="space-y-1">
          <p className="text-[10px] text-white/30 uppercase tracking-wider">Contenido</p>
          <p className="text-xs text-white/60 leading-relaxed whitespace-pre-line">{item.body}</p>
        </div>
      )}

      {/* Caption */}
      {item.caption && (
        <div className="space-y-1.5">
          <div className="flex items-center justify-between">
            <p className="text-[10px] text-white/30 uppercase tracking-wider">Caption</p>
            <CopyButton text={item.caption} />
          </div>
          <p className="text-xs text-white/60 leading-relaxed whitespace-pre-line bg-white/[0.02] border border-white/[0.05] rounded-lg p-3">{item.caption}</p>
        </div>
      )}

      {/* Hashtags */}
      {item.hashtags?.length > 0 && (
        <div className="space-y-1.5">
          <div className="flex items-center justify-between">
            <p className="text-[10px] text-white/30 uppercase tracking-wider">Hashtags</p>
            <CopyButton text={item.hashtags.map((h: string) => `#${h}`).join(" ")} />
          </div>
          <div className="flex flex-wrap gap-1">
            {item.hashtags.map((h: string) => (
              <span key={h} className="text-[10px] bg-violet-500/10 text-violet-300/70 border border-violet-500/15 px-1.5 py-0.5 rounded">#{h}</span>
            ))}
          </div>
        </div>
      )}

      {/* CTA */}
      {item.cta && (
        <div className="px-3 py-2 rounded-lg bg-white/[0.03] border border-white/[0.06]">
          <p className="text-[10px] text-white/30 mb-0.5">CTA</p>
          <p className="text-xs text-white/60">{item.cta}</p>
        </div>
      )}

      {/* Visual prompt */}
      {item.visual_prompt && (
        <div className="space-y-1">
          <p className="text-[10px] text-white/30 uppercase tracking-wider">Prompt visual</p>
          <p className="text-xs text-white/40 italic leading-relaxed">{item.visual_prompt}</p>
        </div>
      )}

      {/* Copy all */}
      <div className="flex items-center justify-between pt-1 border-t border-white/[0.05]">
        <CopyButton text={fullText} />
        {/* Approve / Reject */}
        {item.status === "draft" && (
          <div className="flex gap-2">
            <button
              onClick={() => updateStatus("rejected")}
              disabled={updating}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-red-500/10 hover:bg-red-500/20 border border-red-500/20 text-red-400 text-xs transition-colors disabled:opacity-40"
            >
              <XCircle size={12} /> Rechazar
            </button>
            <button
              onClick={() => updateStatus("approved")}
              disabled={updating}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/20 text-emerald-400 text-xs font-medium transition-colors disabled:opacity-40"
            >
              <CheckCircle2 size={12} /> Aprobar
            </button>
          </div>
        )}
        {item.status === "approved" && (
          <button
            onClick={() => updateStatus("published")}
            disabled={updating}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-blue-500/10 hover:bg-blue-500/20 border border-blue-500/20 text-blue-400 text-xs transition-colors disabled:opacity-40"
          >
            <Check size={12} /> Marcar como publicado
          </button>
        )}
      </div>
    </div>
  );
}

export default function ContenidoPage() {
  const [items, setItems] = useState<ContentItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterProject, setFilterProject] = useState("all");
  const [filterStatus, setFilterStatus] = useState("all");

  const load = useCallback(async () => {
    const { data } = await supabase
      .from("content_output")
      .select("*")
      .order("created_at", { ascending: false });
    setItems(data ?? []);
    setLoading(false);
  }, []);

  useEffect(() => { load(); }, [load]);

  const filtered = items.filter((i) => {
    if (filterProject !== "all" && i.project_id !== filterProject) return false;
    if (filterStatus !== "all" && i.status !== filterStatus) return false;
    return true;
  });

  const counts = {
    draft: items.filter((i) => i.status === "draft").length,
    approved: items.filter((i) => i.status === "approved").length,
    published: items.filter((i) => i.status === "published").length,
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-white">Contenido</h1>
          <p className="text-sm text-white/30 mt-0.5">Generado por agentes · Aprobá y publicá</p>
        </div>
        <button onClick={load} className="p-2 rounded-lg bg-white/5 hover:bg-white/10 border border-white/[0.07] transition-colors">
          <RefreshCw size={13} className="text-white/50" />
        </button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-3">
        {[
          { label: "Borradores", value: counts.draft, color: "text-white/60" },
          { label: "Aprobados", value: counts.approved, color: "text-emerald-400" },
          { label: "Publicados", value: counts.published, color: "text-blue-400" },
        ].map((s) => (
          <div key={s.label} className="rounded-xl border border-white/[0.07] bg-white/[0.02] p-4 text-center">
            <p className={`text-2xl font-bold ${s.color}`}>{s.value}</p>
            <p className="text-[10px] text-white/30 mt-0.5">{s.label}</p>
          </div>
        ))}
      </div>

      {/* Filters */}
      <div className="flex gap-3 flex-wrap">
        <div className="flex gap-1 p-1 bg-white/5 rounded-lg border border-white/[0.07]">
          {["all", "mente-pausada", "polt-mobilier", "cerebro"].map((p) => (
            <button key={p} onClick={() => setFilterProject(p)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs transition-all ${filterProject === p ? "bg-violet-600 text-white" : "text-white/50 hover:text-white"}`}>
              {p !== "all" && PROJECT_META[p] && <span className={`w-1.5 h-1.5 rounded-full ${PROJECT_META[p].dot}`} />}
              {p === "all" ? "Todos" : PROJECT_META[p]?.label ?? p}
            </button>
          ))}
        </div>
        <div className="flex gap-1 p-1 bg-white/5 rounded-lg border border-white/[0.07]">
          {["all", "draft", "approved", "published", "rejected"].map((s) => (
            <button key={s} onClick={() => setFilterStatus(s)}
              className={`px-3 py-1.5 rounded-md text-xs transition-all ${filterStatus === s ? "bg-violet-600 text-white" : "text-white/50 hover:text-white"}`}>
              {s === "all" ? "Todos" : STATUS_META[s]?.label ?? s}
            </button>
          ))}
        </div>
      </div>

      {/* Content list */}
      {loading ? (
        <div className="flex justify-center py-20">
          <div className="w-6 h-6 border-2 border-violet-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : filtered.length === 0 ? (
        <div className="text-center py-20 text-sm text-white/30">
          <Film size={32} className="text-white/10 mx-auto mb-3" />
          Sin contenido para los filtros seleccionados
        </div>
      ) : (
        <div className="space-y-4">
          {filtered.map((item) => (
            <ContentCard key={item.id} item={item} onStatusChange={load} />
          ))}
        </div>
      )}
    </div>
  );
}
