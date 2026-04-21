export interface Potencial {
  id: number;
  nombre: string;
  mueble: string;
  celular?: string;
  fecha: string; // ISO date
  estado: 'SIN_RESPUESTA' | 'ESPERAMOS_RESPUESTA' | 'COTIZACION_ENVIADA' | 'CLIENTE' | 'CERRAR' | 'RECONTACTAR';
  quien_lo_tiene?: string;
  fecha_seguimiento?: string; // ISO date
  prioridad: 'ALTA' | 'MEDIA' | 'BAJA';
  created_at: string; // ISO datetime
  updated_at: string; // ISO datetime
}

export interface PotencialListResponse {
  total: number;
  items: Potencial[];
}

export const potencialesAPI = {
  list: async (filterEstado?: string, filterPrioridad?: string): Promise<PotencialListResponse> => {
    const params = new URLSearchParams();
    if (filterEstado) params.append('estado', filterEstado);
    if (filterPrioridad) params.append('prioridad', filterPrioridad);
    const res = await fetch(`/api/v1/potenciales?${params}`);
    return res.json();
  },

  getById: async (id: number): Promise<Potencial> => {
    const res = await fetch(`/api/v1/potenciales/${id}`);
    return res.json();
  },

  create: async (data: Omit<Potencial, 'id' | 'created_at' | 'updated_at'>): Promise<Potencial> => {
    const res = await fetch('/api/v1/potenciales', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return res.json();
  },

  update: async (id: number, data: Partial<Potencial>): Promise<Potencial> => {
    const res = await fetch(`/api/v1/potenciales/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return res.json();
  },

  delete: async (id: number): Promise<void> => {
    await fetch(`/api/v1/potenciales/${id}`, { method: 'DELETE' });
  },
};
