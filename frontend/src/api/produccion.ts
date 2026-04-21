export interface Produccion {
  id: number;
  cliente: string;
  celular?: string;
  descripcion_breve?: string;
  estado: 'PLANIFICACIÓN' | 'CARPINTERIA' | 'LAQUEADO' | 'RETIRO PARA REMODELAR' | 'PENDIENTE' | 'POST VENTA' | 'FIDELIZACION' | 'FINALIZADO';
  created_at: string; // ISO datetime
  updated_at: string; // ISO datetime
}

export interface ProduccionListResponse {
  total: number;
  items: Produccion[];
}

export const produccionAPI = {
  list: async (filterEstado?: string): Promise<ProduccionListResponse> => {
    const params = new URLSearchParams();
    if (filterEstado) params.append('estado', filterEstado);
    const res = await fetch(`/api/v1/produccion?${params}`);
    return res.json();
  },

  getById: async (id: number): Promise<Produccion> => {
    const res = await fetch(`/api/v1/produccion/${id}`);
    return res.json();
  },

  create: async (data: Omit<Produccion, 'id' | 'created_at' | 'updated_at'>): Promise<Produccion> => {
    const res = await fetch('/api/v1/produccion', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return res.json();
  },

  update: async (id: number, data: Partial<Produccion>): Promise<Produccion> => {
    const res = await fetch(`/api/v1/produccion/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return res.json();
  },

  delete: async (id: number): Promise<void> => {
    await fetch(`/api/v1/produccion/${id}`, { method: 'DELETE' });
  },
};
