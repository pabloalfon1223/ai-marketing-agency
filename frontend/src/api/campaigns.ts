import api from './client';
import type { Campaign } from '../types';

export const getCampaigns = (projectId?: number) =>
  api.get<Campaign[]>('/campaigns', { params: projectId ? { project_id: projectId } : {} }).then(r => r.data);
export const getCampaign = (id: number) => api.get<Campaign>(`/campaigns/${id}`).then(r => r.data);
export const createCampaign = (data: Partial<Campaign>) => api.post<Campaign>('/campaigns', data).then(r => r.data);
export const updateCampaign = (id: number, data: Partial<Campaign>) => api.put<Campaign>(`/campaigns/${id}`, data).then(r => r.data);
export const deleteCampaign = (id: number) => api.delete(`/campaigns/${id}`);
export const launchCampaign = (id: number) => api.post(`/campaigns/${id}/launch`).then(r => r.data);
