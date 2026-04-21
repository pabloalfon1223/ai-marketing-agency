import api from './client';

export interface FunnelData {
  [status: string]: number;
}

export interface ValueByStatus {
  [status: string]: number;
}

export interface ConversionRateData {
  total: number;
  quote_accepted: number;
  conversion_rate: number;
}

export interface TimelineItem {
  orden_id: string;
  cliente: string;
  mueble: string;
  estado: string;
  fecha_inicio: string;
  fecha_entrega_est?: string;
  dias_produccion?: number;
}

export interface IngresosData {
  total_ingresos: number;
  currency: string;
}

export interface DashboardSummary {
  total_potenciales: number;
  total_produccion: number;
  conversion_rate: number;
  total_estimated_value: number;
  total_ingresos: number;
  currency: string;
}

export const dashboardsAPI = {
  funnelPotenciales: () =>
    api.get<FunnelData>('/dashboards/potenciales/funnel').then(r => r.data),

  valueByStatus: () =>
    api.get<ValueByStatus>('/dashboards/potenciales/value-by-status').then(r => r.data),

  conversionRate: () =>
    api.get<ConversionRateData>('/dashboards/potenciales/conversion-rate').then(r => r.data),

  timelineProduccion: () =>
    api.get<TimelineItem[]>('/dashboards/produccion/timeline').then(r => r.data),

  ingresosTotal: () =>
    api.get<IngresosData>('/dashboards/produccion/ingresos').then(r => r.data),

  summary: () =>
    api.get<DashboardSummary>('/dashboards/summary').then(r => r.data),
};
