// IA Machine CRM — Data (lee desde shared/ cuando esté disponible)

export type Project = "mente-pausada" | "polt-mobilier" | "cerebro";

export interface Contact {
  id: string;
  name: string;
  email: string;
  phone?: string;
  project: Project;
  stage: PipelineStage;
  value: number;
  currency: "USD" | "ARS";
  notes?: string;
  createdAt: string;
  updatedAt: string;
  tags: string[];
}

export type PipelineStage =
  | "nuevo"
  | "calificado"
  | "propuesta"
  | "negociacion"
  | "cerrado-ganado"
  | "cerrado-perdido";

export interface KPIData {
  project: Project;
  today: { sales: number; revenue: number; leads: number };
  week: { sales: number; revenue: number; conversionRate: number; avgOrderValue: number };
  month: { sales: number; revenue: number; goal: number };
  chartData: { date: string; revenue: number; sales: number }[];
}

export const mockContacts: Contact[] = [
  // Mente Pausada
  { id: "mp-001", name: "Ana García", email: "ana@gmail.com", project: "mente-pausada", stage: "cerrado-ganado", value: 149, currency: "USD", notes: "Compró plan Plus. Muy satisfecha.", createdAt: "2026-04-15", updatedAt: "2026-04-15", tags: ["plus", "activo"] },
  { id: "mp-002", name: "Carlos Martínez", email: "carlos@hotmail.com", project: "mente-pausada", stage: "nuevo", value: 99, currency: "USD", notes: "Visitó landing 3 veces. Interesado en Basic.", createdAt: "2026-04-20", updatedAt: "2026-04-20", tags: ["basic", "retargeting"] },
  { id: "mp-003", name: "Valentina López", email: "valen@icloud.com", project: "mente-pausada", stage: "cerrado-ganado", value: 199, currency: "USD", notes: "Compró VIP. Pidió sesión de coaching.", createdAt: "2026-04-18", updatedAt: "2026-04-19", tags: ["vip", "upsell"] },
  { id: "mp-004", name: "Martín Rodríguez", email: "martin@gmail.com", project: "mente-pausada", stage: "propuesta", value: 149, currency: "USD", notes: "En secuencia de email día 7.", createdAt: "2026-04-14", updatedAt: "2026-04-21", tags: ["plus", "email-sequence"] },
  // Polt Mobilier
  { id: "polt-001", name: "Diego Fernández", email: "diego@empresa.com", phone: "+54 11 5555-1234", project: "polt-mobilier", stage: "propuesta", value: 850000, currency: "ARS", notes: "Interesado en escritorio + biblioteca. Enviar cotización.", createdAt: "2026-04-19", updatedAt: "2026-04-21", tags: ["escritorio", "biblioteca", "presupuesto-enviado"] },
  { id: "polt-002", name: "Laura Sánchez", email: "laura@gmail.com", phone: "+54 11 6666-5678", project: "polt-mobilier", stage: "negociacion", value: 1200000, currency: "ARS", notes: "Quiere walk-in closet completo. Esperando confirmación de medidas.", createdAt: "2026-04-10", updatedAt: "2026-04-20", tags: ["closet", "alta-prioridad"] },
  { id: "polt-003", name: "Roberto Pérez", email: "rperez@outlook.com", project: "polt-mobilier", stage: "nuevo", value: 400000, currency: "ARS", notes: "Preguntó por WhatsApp sobre mesas de comedor.", createdAt: "2026-04-21", updatedAt: "2026-04-21", tags: ["mesa", "nuevo-lead"] },
  { id: "polt-004", name: "Sofía Castro", email: "sofia@yahoo.com", project: "polt-mobilier", stage: "cerrado-ganado", value: 650000, currency: "ARS", notes: "Cerró cocina completa. En producción.", createdAt: "2026-04-05", updatedAt: "2026-04-12", tags: ["cocina", "en-produccion"] },
  // Cerebro
  { id: "cer-001", name: "Oportunidad: SaaS análisis de ads", email: "n/a", project: "cerebro", stage: "calificado", value: 5000, currency: "USD", notes: "Mercado $2B. Competencia alta pero nicho de PyMEs sin resolver.", createdAt: "2026-04-17", updatedAt: "2026-04-17", tags: ["saas", "ads", "potencial-alto"] },
  { id: "cer-002", name: "Oportunidad: Agencia IA para coaches", email: "n/a", project: "cerebro", stage: "propuesta", value: 3000, currency: "USD", notes: "Modelo de servicio mensual. Baja competencia en LATAM.", createdAt: "2026-04-21", updatedAt: "2026-04-21", tags: ["agencia", "coaches", "latam"] },
];

export const mockKPIs: Record<Project, KPIData> = {
  "mente-pausada": {
    project: "mente-pausada",
    today: { sales: 2, revenue: 298, leads: 14 },
    week: { sales: 11, revenue: 1547, conversionRate: 6.8, avgOrderValue: 140.6 },
    month: { sales: 34, revenue: 4891, goal: 5000 },
    chartData: [
      { date: "15 Abr", revenue: 199, sales: 1 }, { date: "16 Abr", revenue: 298, sales: 2 },
      { date: "17 Abr", revenue: 448, sales: 3 }, { date: "18 Abr", revenue: 99, sales: 1 },
      { date: "19 Abr", revenue: 547, sales: 4 }, { date: "20 Abr", revenue: 149, sales: 1 },
      { date: "21 Abr", revenue: 298, sales: 2 },
    ],
  },
  "polt-mobilier": {
    project: "polt-mobilier",
    today: { sales: 0, revenue: 0, leads: 1 },
    week: { sales: 1, revenue: 650000, conversionRate: 22, avgOrderValue: 650000 },
    month: { sales: 3, revenue: 2100000, goal: 3000000 },
    chartData: [
      { date: "15 Abr", revenue: 0, sales: 0 }, { date: "16 Abr", revenue: 400000, sales: 1 },
      { date: "17 Abr", revenue: 0, sales: 0 }, { date: "18 Abr", revenue: 1050000, sales: 1 },
      { date: "19 Abr", revenue: 0, sales: 0 }, { date: "20 Abr", revenue: 650000, sales: 1 },
      { date: "21 Abr", revenue: 0, sales: 0 },
    ],
  },
  cerebro: {
    project: "cerebro",
    today: { sales: 0, revenue: 0, leads: 0 },
    week: { sales: 0, revenue: 0, conversionRate: 0, avgOrderValue: 0 },
    month: { sales: 0, revenue: 0, goal: 1000 },
    chartData: Array(7).fill(null).map((_, i) => ({ date: `${15 + i} Abr`, revenue: 0, sales: 0 })),
  },
};

export const stageLabels: Record<PipelineStage, string> = {
  nuevo: "Nuevo", calificado: "Calificado", propuesta: "Propuesta",
  negociacion: "Negociación", "cerrado-ganado": "Cerrado ✓", "cerrado-perdido": "Perdido ✗",
};

export const stageColors: Record<PipelineStage, string> = {
  nuevo: "bg-slate-500", calificado: "bg-blue-500", propuesta: "bg-yellow-500",
  negociacion: "bg-orange-500", "cerrado-ganado": "bg-green-500", "cerrado-perdido": "bg-red-500",
};

export const projectLabels: Record<Project, string> = {
  "mente-pausada": "Mente Pausada", "polt-mobilier": "Polt Mobilier", cerebro: "Cerebro",
};

export const projectColors: Record<Project, string> = {
  "mente-pausada": "text-purple-400", "polt-mobilier": "text-amber-400", cerebro: "text-emerald-400",
};
