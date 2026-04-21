export interface PotencialesResumen {
  total: number;
  SIN_RESPUESTA: number;
  ESPERAMOS_RESPUESTA: number;
  COTIZACION_ENVIADA: number;
  CLIENTE: number;
  CERRAR: number;
  RECONTACTAR: number;
}

export interface FunnelData {
  SIN_RESPUESTA: number;
  ESPERAMOS_RESPUESTA: number;
  COTIZACION_ENVIADA: number;
  CLIENTE: number;
}

export interface ProduccionResumen {
  total: number;
  PLANIFICACIÓN: number;
  CARPINTERIA: number;
  LAQUEADO: number;
  'RETIRO PARA REMODELAR': number;
  PENDIENTE: number;
  'POST VENTA': number;
  FIDELIZACION: number;
  FINALIZADO: number;
  finalizados: number;
  alertas_sin_actualizar: number;
}

export interface PrioridadDistribucion {
  ALTA: number;
  MEDIA: number;
  BAJA: number;
}

export const dashboardsAPI = {
  // Potenciales endpoints
  potencialesResumen: async (): Promise<PotencialesResumen> => {
    const res = await fetch('/api/v1/dashboards/potenciales/resumen');
    return res.json();
  },

  funnelPotenciales: async (): Promise<FunnelData> => {
    const res = await fetch('/api/v1/dashboards/potenciales/funnel');
    return res.json();
  },

  conversionRate: async () => {
    const res = await fetch('/api/v1/dashboards/potenciales/conversion-rate');
    return res.json();
  },

  prioridadDistribucion: async (): Promise<PrioridadDistribucion> => {
    const res = await fetch('/api/v1/dashboards/potenciales/por-prioridad');
    return res.json();
  },

  // Producción endpoints
  produccionResumen: async (): Promise<ProduccionResumen> => {
    const res = await fetch('/api/v1/dashboards/produccion/resumen');
    return res.json();
  },

  produccionAlertas: async (dias?: number) => {
    const params = new URLSearchParams();
    if (dias) params.append('dias', dias.toString());
    const res = await fetch(`/api/v1/dashboards/produccion/alertas?${params}`);
    return res.json();
  },

  // General summary
  resumenGeneral: async () => {
    const res = await fetch('/api/v1/dashboards/resumen-general');
    return res.json();
  },
};
