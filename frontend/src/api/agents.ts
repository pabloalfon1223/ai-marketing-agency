import api from './client';
import type { AgentStatus, Task, AgentLog } from '../types';

export const getAgentsStatus = () => api.get<AgentStatus[]>('/agents/status').then(r => r.data);
export const runAgent = (data: { agent_type: string; task_type: string; project_id?: number; campaign_id?: number; input_data?: string }) =>
  api.post<Task>('/agents/run', data).then(r => r.data);
export const getTasks = (params?: Record<string, string | number>) =>
  api.get<Task[]>('/tasks', { params }).then(r => r.data);
export const getTask = (id: number) => api.get<Task>(`/tasks/${id}`).then(r => r.data);
export const retryTask = (id: number) => api.post<Task>(`/tasks/${id}/retry`).then(r => r.data);
export const getTaskLogs = (id: number) => api.get<AgentLog[]>(`/tasks/${id}/logs`).then(r => r.data);
export const getAnalyticsOverview = () => api.get('/analytics/overview').then(r => r.data);
export const getAgentAnalytics = () => api.get('/analytics/agents').then(r => r.data);
