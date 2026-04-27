"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard, KanbanSquare, Bot, Users,
  Terminal, Zap, LogOut, FileText
} from "lucide-react";
import { supabase } from "@/lib/supabase";
import { useRouter } from "next/navigation";

const PROJECT_DOTS: Record<string, string> = {
  "mente-pausada": "bg-violet-400",
  "polt-mobilier":  "bg-amber-400",
  "cerebro":        "bg-cyan-400",
};

const nav = [
  { href: "/", label: "Control Center", icon: LayoutDashboard },
  { href: "/command", label: "Command", icon: Terminal, badge: "urgente" },
  { href: "/contenido", label: "Contenido", icon: FileText },
  { href: "/agents", label: "Agentes", icon: Bot },
  { href: "/pipeline", label: "Pipeline", icon: KanbanSquare },
  { href: "/contacts", label: "Contactos", icon: Users },
];

const projects = [
  { id: "mente-pausada", label: "Mente Pausada", pct: 80 },
  { id: "polt-mobilier",  label: "Polt Mobilier",  pct: 50 },
  { id: "cerebro",        label: "Cerebro",         pct: 0  },
];

export default function Sidebar() {
  const path = usePathname();
  const router = useRouter();

  async function handleLogout() {
    await supabase.auth.signOut();
    router.push("/login");
  }

  return (
    <aside className="w-56 min-h-screen bg-white/[0.02] border-r border-white/[0.06] flex flex-col shrink-0">
      {/* Logo */}
      <div className="px-5 py-5 border-b border-white/[0.06]">
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-violet-600 to-indigo-600 flex items-center justify-center">
            <Zap size={14} className="text-white" />
          </div>
          <div>
            <p className="text-sm font-bold text-white leading-none">IA Machine</p>
            <p className="text-[10px] text-white/30 mt-0.5">Control Center</p>
          </div>
        </div>
      </div>

      {/* Nav */}
      <nav className="p-3 space-y-0.5 border-b border-white/[0.06]">
        {nav.map(({ href, label, icon: Icon, badge }) => {
          const active = path === href;
          return (
            <Link
              key={href}
              href={href}
              className={`flex items-center justify-between px-3 py-2 rounded-lg text-sm transition-all ${
                active
                  ? "bg-violet-600/20 text-violet-300 font-medium"
                  : "text-white/50 hover:text-white hover:bg-white/5"
              }`}
            >
              <span className="flex items-center gap-3">
                <Icon size={15} />
                {label}
              </span>
              {badge && (
                <span className="text-[9px] px-1.5 py-0.5 rounded-full bg-red-500/20 text-red-400 border border-red-500/20 font-medium">
                  {badge}
                </span>
              )}
            </Link>
          );
        })}
      </nav>

      {/* Projects */}
      <div className="p-3 flex-1">
        <p className="text-[10px] text-white/20 uppercase tracking-wider px-3 mb-2">Proyectos</p>
        <div className="space-y-1">
          {projects.map((p) => (
            <div key={p.id} className="px-3 py-2.5 rounded-lg hover:bg-white/5 transition-colors cursor-default">
              <div className="flex items-center justify-between mb-1.5">
                <div className="flex items-center gap-2">
                  <span className={`w-1.5 h-1.5 rounded-full ${PROJECT_DOTS[p.id]}`} />
                  <span className="text-xs text-white/50">{p.label}</span>
                </div>
                <span className="text-[10px] text-white/25">{p.pct}%</span>
              </div>
              <div className="w-full h-0.5 bg-white/[0.06] rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full ${PROJECT_DOTS[p.id].replace("bg-", "bg-").replace("-400", "-500")}`}
                  style={{ width: `${p.pct}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-white/[0.06] space-y-2">
        <div className="flex items-center gap-2 px-2 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/15">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
          <span className="text-[10px] text-emerald-400 font-medium">Sistema activo</span>
        </div>
        <button
          onClick={handleLogout}
          className="w-full flex items-center gap-2 px-2 py-1.5 rounded-lg text-white/30 hover:text-white/60 hover:bg-white/5 transition-colors text-xs"
        >
          <LogOut size={12} />
          Cerrar sesión
        </button>
      </div>
    </aside>
  );
}
