import api from './client';
import type { Content } from '../types';

export const getContents = (params?: Record<string, string | number>) =>
  api.get<Content[]>('/content', { params }).then(r => r.data);
export const getContent = (id: number) => api.get<Content>(`/content/${id}`).then(r => r.data);
export const updateContent = (id: number, data: Partial<Content>) => api.put<Content>(`/content/${id}`, data).then(r => r.data);
export const updateContentStatus = (id: number, data: { status: string; review_notes?: string }) =>
  api.patch(`/content/${id}/status`, data).then(r => r.data);
export const regenerateContent = (id: number) => api.post(`/content/${id}/regenerate`).then(r => r.data);
