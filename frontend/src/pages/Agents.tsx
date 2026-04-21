import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Play, RefreshCw, Eye, ChevronDown, ChevronUp } from 'lucide-react';
import Header from '../components/layout/Header';
import Modal from '../components/shared/Modal';
import StatusBadge from '../components/shared/StatusBadge';
import LoadingSpinner from '../components/shared/LoadingSpinner';
import { getAgentsStatus, runAgent, getTasks, retryTask, getTaskLogs } from '../api/agents';
import { formatDateTime, agentDisplayNames } from '../utils/formatters';
import type { Task, AgentLog } from '../types';

const TASK_TYPES: Record<string, string[]> = {
  strategy: ['create_strategy_brief', 'audience_analysis', 'competitor_analysis'],
  content: ['generate_blog_post', 'generate_social_posts', 'generate_email_copy', 'generate_ad_copy'],
  seo: ['keyword_research', 'score_content'],
  social_media: ['create_calendar', 'create_post'],
  email_marketing: ['create_sequence', 'optimize_subject_lines'],
  analytics: ['setup_kpis', 'generate_report'],
  branding: ['define_brand_voice', 'create_guidelines'],
  advertising: ['create_ad_plan', 'create_ad_copy'],
  orchestrator: ['run_full_campaign', 'run_content_workflow'],
};

export default function Agents() {
  const queryClient = useQueryClient();
  const { data: agents, isLoading } = useQuery({ queryKey: ['agents-status'], queryFn: getAgentsStatus });
  const { data: tasks } = useQuery({ queryKey: ['tasks'], queryFn: () => getTasks() });
  const [runModal, setRunModal] = useState(false);
  const [runForm, setRunForm] = useState({ agent_type: 'content', task_type: '', input_data: '' });
  const [logsTaskId, setLogsTaskId] = useState<number | null>(null);
  const { data: logs } = useQuery({
    queryKey: ['task-logs', logsTaskId],
    queryFn: () => getTaskLogs(logsTaskId!),
    enabled: !!logsTaskId,
  });
  const [expandedAgent, setExpandedAgent] = useState<string | null>(null);

  const runMut = useMutation({
    mutationFn: runAgent,
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['tasks', 'agents-status'] }); setRunModal(false); },
  });
  const retryMut = useMutation({
    mutationFn: retryTask,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['tasks'] }),
  });

  function handleRun(e: React.FormEvent) {
    e.preventDefault();
    runMut.mutate({
      agent_type: runForm.agent_type,
      task_type: runForm.task_type || TASK_TYPES[runForm.agent_type]?.[0] || 'default',
      input_data: runForm.input_data || undefined,
    });
  }

  const agentTasks = (agentType: string) => tasks?.filter((t: Task) => t.agent_type === agentType) || [];

  return (
    <>
      <Header title="Agentes IA" />
      <div className="p-6 space-y-6">
        {/* Run Ad-hoc Task Button */}
        <div className="flex justify-end">
          <button onClick={() => setRunModal(true)}
            className="flex items-center gap-2 bg-primary-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-primary-700">
            <Play size={16} /> Ejecutar Tarea
          </button>
        </div>

        {/* Agent Cards Grid */}
        {isLoading ? <LoadingSpinner /> : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {agents?.map((agent: any) => (
              <div key={agent.agent_type} className="bg-white rounded-xl border border-gray-200 overflow-hidden">
                <div className="p-5">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-2">
                      <div className={`w-3 h-3 rounded-full ${agent.tasks_running > 0 ? 'bg-yellow-400 animate-pulse' : 'bg-green-400'}`} />
                      <h3 className="font-semibold text-sm">{agent.display_name}</h3>
                    </div>
                    <StatusBadge status={agent.tasks_running > 0 ? 'busy' : 'idle'} />
                  </div>
                  <p className="text-xs text-gray-500 mb-4">{agent.description}</p>
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-gray-500">Completadas: <span className="font-medium text-gray-700">{agent.tasks_completed}</span></span>
                    <span className="text-gray-500">En curso: <span className="font-medium text-yellow-600">{agent.tasks_running}</span></span>
                  </div>
                </div>
                {/* Expandable task list */}
                <button onClick={() => setExpandedAgent(expandedAgent === agent.agent_type ? null : agent.agent_type)}
                  className="w-full px-5 py-2 bg-gray-50 border-t border-gray-100 text-xs text-gray-500 hover:bg-gray-100 flex items-center justify-center gap-1">
                  {expandedAgent === agent.agent_type ? <><ChevronUp size={12} /> Ocultar tareas</> : <><ChevronDown size={12} /> Ver tareas</>}
                </button>
                {expandedAgent === agent.agent_type && (
                  <div className="border-t border-gray-100 max-h-48 overflow-y-auto">
                    {agentTasks(agent.agent_type).length ? agentTasks(agent.agent_type).slice(0, 10).map((t: Task) => (
                      <div key={t.id} className="px-5 py-2 border-b border-gray-50 flex items-center justify-between text-xs">
                        <div>
                          <span className="font-medium">{t.task_type}</span>
                          <span className="text-gray-400 ml-2">{formatDateTime(t.created_at)}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <StatusBadge status={t.status} />
                          {t.status === 'failed' && (
                            <button onClick={() => retryMut.mutate(t.id)} className="text-primary-600 hover:text-primary-800">
                              <RefreshCw size={12} />
                            </button>
                          )}
                          <button onClick={() => setLogsTaskId(t.id)} className="text-gray-400 hover:text-gray-600">
                            <Eye size={12} />
                          </button>
                        </div>
                      </div>
                    )) : (
                      <p className="px-5 py-3 text-xs text-gray-400">Sin tareas</p>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Run Task Modal */}
      <Modal open={runModal} onClose={() => setRunModal(false)} title="Ejecutar Tarea Ad-hoc">
        <form onSubmit={handleRun} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Agente</label>
            <select value={runForm.agent_type} onChange={e => setRunForm({ ...runForm, agent_type: e.target.value, task_type: '' })}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500">
              {Object.keys(TASK_TYPES).map(a => (
                <option key={a} value={a}>{agentDisplayNames[a] || a}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Tipo de Tarea</label>
            <select value={runForm.task_type} onChange={e => setRunForm({ ...runForm, task_type: e.target.value })}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500">
              <option value="">Seleccionar...</option>
              {(TASK_TYPES[runForm.agent_type] || []).map(t => (
                <option key={t} value={t}>{t}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Instrucciones (JSON o texto)</label>
            <textarea value={runForm.input_data} onChange={e => setRunForm({ ...runForm, input_data: e.target.value })} rows={4}
              placeholder='{"instructions": "Crea contenido para..."}'
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-primary-500" />
          </div>
          <div className="flex justify-end gap-3 pt-2">
            <button type="button" onClick={() => setRunModal(false)} className="px-4 py-2 text-sm text-gray-600">Cancelar</button>
            <button type="submit" className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg text-sm font-medium hover:bg-primary-700">
              <Play size={14} /> Ejecutar
            </button>
          </div>
        </form>
      </Modal>

      {/* Task Logs Modal */}
      <Modal open={!!logsTaskId} onClose={() => setLogsTaskId(null)} title={`Logs - Task #${logsTaskId}`}>
        <div className="max-h-80 overflow-y-auto space-y-2">
          {logs?.length ? logs.map((log: AgentLog) => (
            <div key={log.id} className={`text-xs p-2 rounded font-mono ${
              log.log_level === 'error' ? 'bg-red-50 text-red-700' :
              log.log_level === 'warning' ? 'bg-yellow-50 text-yellow-700' :
              'bg-gray-50 text-gray-700'
            }`}>
              <span className="text-gray-400">[{log.created_at}]</span> {log.message}
            </div>
          )) : (
            <p className="text-sm text-gray-400 text-center py-4">Sin logs disponibles</p>
          )}
        </div>
      </Modal>
    </>
  );
}
