import { useState, useEffect } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import {
  Zap, Server, Rocket, Settings, CheckCircle, MessageSquare,
  Loader, AlertCircle, Copy, X, RefreshCw, MessageCircle
} from 'lucide-react';
import Header from '../components/layout/Header';
import LoadingSpinner from '../components/shared/LoadingSpinner';
import Modal from '../components/shared/Modal';
import api from '../api/client';
import { useWebSocket } from '../hooks/useWebSocket';

interface CommandResult {
  id: string;
  command: string;
  status: 'pending' | 'success' | 'error';
  result?: any;
  error?: string;
  timestamp: Date;
}

interface DiscordEvent {
  id: string;
  type: 'command' | 'message' | 'reaction' | 'status';
  title: string;
  description?: string;
  timestamp: Date;
}

const COMMANDS = [
  {
    id: 'status',
    name: 'Estado del Sistema',
    icon: Server,
    color: 'bg-blue-500',
    description: 'Verificar estado de todos los agentes',
    action: 'jefe-status'
  },
  {
    id: 'run',
    name: 'Ejecutar Workflow',
    icon: Rocket,
    color: 'bg-green-500',
    description: 'Ejecutar un flujo de trabajo completo',
    action: 'jefe-run',
    needsInput: true
  },
  {
    id: 'dispatch',
    name: 'Enviar Tareas',
    icon: Zap,
    color: 'bg-yellow-500',
    description: 'Distribuir tareas a los agentes',
    action: 'jefe-dispatch',
    needsInput: true
  },
  {
    id: 'build',
    name: 'Construir Contenido',
    icon: Settings,
    color: 'bg-purple-500',
    description: 'Generar nuevo contenido',
    action: 'jefe-build',
    needsInput: true
  },
  {
    id: 'review',
    name: 'Revisar Contenido',
    icon: CheckCircle,
    color: 'bg-orange-500',
    description: 'Revisar y validar contenido existente',
    action: 'jefe-review',
    needsInput: true
  },
  {
    id: 'ask',
    name: 'Hacer Pregunta',
    icon: MessageSquare,
    color: 'bg-indigo-500',
    description: 'Consultar a los agentes sobre algo',
    action: 'jefe-ask',
    needsInput: true
  },
];

export default function Control() {
  const [activeCommand, setActiveCommand] = useState<string | null>(null);
  const [commandInput, setCommandInput] = useState('');
  const [results, setResults] = useState<CommandResult[]>([]);
  const [showResults, setShowResults] = useState(false);
  const [discordEvents, setDiscordEvents] = useState<DiscordEvent[]>([]);
  const { ws } = useWebSocket();

  const { data: status } = useQuery({
    queryKey: ['system-status'],
    queryFn: () => api.get('/health').then(r => r.data),
    refetchInterval: 10000,
  });

  const { data: discordStatus } = useQuery({
    queryKey: ['discord-status'],
    queryFn: () => api.get('/discord/status').then(r => r.data),
    refetchInterval: 15000,
  });

  // Listen for Discord events via WebSocket
  useEffect(() => {
    if (!ws) return;

    const handleMessage = (event: MessageEvent) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'discord_event') {
          const discordEvent: DiscordEvent = {
            id: Date.now().toString(),
            type: data.event_type || 'message',
            title: data.title || 'Discord Event',
            description: data.description,
            timestamp: new Date(),
          };
          setDiscordEvents(prev => [discordEvent, ...prev].slice(0, 50));
        }
      } catch (e) {
        // Ignore parse errors
      }
    };

    ws.addEventListener('message', handleMessage);
    return () => ws.removeEventListener('message', handleMessage);
  }, [ws]);

  const executeMutation = useMutation({
    mutationFn: async (command: string) => {
      const result: CommandResult = {
        id: Date.now().toString(),
        command,
        status: 'pending',
        timestamp: new Date(),
      };
      setResults(prev => [result, ...prev]);
      setShowResults(true);

      try {
        let endpoint = '';
        let payload = {};
        let commandName = '';

        switch (command) {
          case 'jefe-status':
            endpoint = '/agents/status';
            commandName = 'Estado del Sistema';
            break;
          case 'jefe-run':
            endpoint = '/agents/run';
            commandName = 'Ejecutar Workflow';
            payload = parseInput(commandInput) || { agent_type: 'orchestrator', task_type: 'run_full_campaign' };
            break;
          case 'jefe-dispatch':
            endpoint = '/tasks';
            commandName = 'Enviar Tareas';
            payload = parseInput(commandInput) || {};
            break;
          case 'jefe-build':
            endpoint = '/content';
            commandName = 'Construir Contenido';
            payload = parseInput(commandInput) || {};
            break;
          case 'jefe-review':
            endpoint = '/analytics/agents';
            commandName = 'Revisar Contenido';
            payload = parseInput(commandInput) || {};
            break;
          case 'jefe-ask':
            endpoint = '/agents/run';
            commandName = 'Hacer Pregunta';
            payload = parseInput(commandInput) || { agent_type: 'orchestrator', task_type: 'run_full_campaign' };
            break;
          default:
            throw new Error('Comando desconocido');
        }

        // Notify Discord about command execution
        await api.post('/discord/notify', {
          tipo: 'content',
          titulo: `🚀 Comando Ejecutado: ${commandName}`,
          descripcion: `Parámetros: ${JSON.stringify(payload).substring(0, 100)}...`,
        }).catch(() => {/* Discord not available, continue anyway */});

        const response = await api.post(endpoint, payload);

        // Notify Discord about success
        await api.post('/discord/notify', {
          tipo: 'content',
          titulo: `✅ ${commandName} - Exitoso`,
          descripcion: `Resultado: ${typeof response.data === 'string' ? response.data : JSON.stringify(response.data).substring(0, 100)}`,
        }).catch(() => {/* Discord not available */});

        setResults(prev =>
          prev.map(r =>
            r.id === result.id
              ? { ...r, status: 'success', result: response.data }
              : r
          )
        );
      } catch (error: any) {
        const errorMessage = error.response?.data?.detail || error.message;

        // Notify Discord about error
        await api.post('/discord/notify', {
          tipo: 'error',
          titulo: '❌ Error en Ejecución',
          descripcion: errorMessage,
        }).catch(() => {/* Discord not available */});

        setResults(prev =>
          prev.map(r =>
            r.id === result.id
              ? { ...r, status: 'error', error: errorMessage }
              : r
          )
        );
      }
    },
  });

  function parseInput(input: string) {
    try {
      if (!input.trim()) return null;
      return JSON.parse(input);
    } catch {
      return { input_data: input };
    }
  }

  function handleExecuteCommand(commandId: string) {
    const command = COMMANDS.find(c => c.id === commandId);
    if (!command) return;

    setCommandInput('');
    executeMutation.mutate(command.action);
    setActiveCommand(null);
  }

  function clearResults() {
    setResults([]);
  }

  function copyResult(result: any) {
    navigator.clipboard.writeText(JSON.stringify(result, null, 2));
  }

  return (
    <>
      <Header title="Panel de Control" />
      <div className="p-6 space-y-6">
        {/* System Status Banners */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-gradient-to-r from-primary-50 to-primary-100 border border-primary-200 rounded-xl p-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className={`w-3 h-3 rounded-full ${status ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`} />
              <div>
                <p className="text-sm font-semibold text-gray-800">Sistema Backend</p>
                <p className="text-xs text-gray-600">{status?.service || 'AI Marketing Agency'}</p>
              </div>
            </div>
            <span className={`text-xs font-medium px-3 py-1 rounded-full ${status ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
              {status ? 'Activo' : 'Offline'}
            </span>
          </div>

          <div className="bg-gradient-to-r from-indigo-50 to-indigo-100 border border-indigo-200 rounded-xl p-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className={`w-3 h-3 rounded-full ${discordStatus?.connected ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`} />
              <div>
                <p className="text-sm font-semibold text-gray-800">Discord Bot</p>
                <p className="text-xs text-gray-600">{discordStatus?.user ? `Usuario: ${discordStatus.user}` : 'No conectado'}</p>
              </div>
            </div>
            <span className={`text-xs font-medium px-3 py-1 rounded-full ${discordStatus?.connected ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
              {discordStatus?.connected ? `${discordStatus.guilds || 0} servidores` : 'Offline'}
            </span>
          </div>
        </div>

        {/* Commands Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {COMMANDS.map(cmd => {
            const Icon = cmd.icon;
            return (
              <button
                key={cmd.id}
                onClick={() => {
                  if (cmd.needsInput) {
                    setActiveCommand(cmd.id);
                  } else {
                    handleExecuteCommand(cmd.id);
                  }
                }}
                disabled={executeMutation.isPending}
                className="bg-white rounded-xl border border-gray-200 p-5 hover:border-gray-300 hover:shadow-md transition-all group text-left disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <div className={`${cmd.color} p-3 rounded-lg w-fit mb-3 group-hover:scale-110 transition-transform`}>
                  <Icon size={20} className="text-white" />
                </div>
                <h3 className="font-semibold text-gray-900 text-sm mb-1">{cmd.name}</h3>
                <p className="text-xs text-gray-500">{cmd.description}</p>
                {cmd.needsInput && (
                  <p className="text-xs text-primary-600 mt-2">Requiere parámetros →</p>
                )}
              </button>
            );
          })}
        </div>

        {/* Discord Events Panel */}
        {discordEvents.length > 0 && (
          <div className="bg-white rounded-xl border border-gray-200 p-5">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-semibold text-gray-700 flex items-center gap-2">
                <MessageCircle size={16} className="text-indigo-600" /> Eventos de Discord
              </h3>
              <button
                onClick={() => setDiscordEvents([])}
                className="text-xs text-gray-500 hover:text-gray-700 flex items-center gap-1"
              >
                <X size={14} /> Limpiar
              </button>
            </div>
            <div className="space-y-2 max-h-40 overflow-y-auto">
              {discordEvents.map(event => (
                <div
                  key={event.id}
                  className="border border-indigo-100 rounded-lg p-3 bg-indigo-50"
                >
                  <div className="flex items-start justify-between mb-1">
                    <span className="text-xs font-medium text-indigo-700">{event.title}</span>
                    <span className="text-xs text-gray-500">
                      {event.timestamp.toLocaleTimeString()}
                    </span>
                  </div>
                  {event.description && (
                    <p className="text-xs text-gray-600">{event.description}</p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Results Panel */}
        {results.length > 0 && (
          <div className="bg-white rounded-xl border border-gray-200 p-5">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-semibold text-gray-700">Historial de Comandos</h3>
              <button
                onClick={clearResults}
                className="text-xs text-gray-500 hover:text-gray-700 flex items-center gap-1"
              >
                <X size={14} /> Limpiar
              </button>
            </div>
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {results.map(result => (
                <div
                  key={result.id}
                  className={`border rounded-lg p-3 ${
                    result.status === 'pending'
                      ? 'border-yellow-200 bg-yellow-50'
                      : result.status === 'success'
                        ? 'border-green-200 bg-green-50'
                        : 'border-red-200 bg-red-50'
                  }`}
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center gap-2">
                      {result.status === 'pending' && (
                        <Loader size={14} className="animate-spin text-yellow-600" />
                      )}
                      {result.status === 'success' && (
                        <CheckCircle size={14} className="text-green-600" />
                      )}
                      {result.status === 'error' && (
                        <AlertCircle size={14} className="text-red-600" />
                      )}
                      <span className="text-xs font-medium text-gray-700">
                        {result.command}
                      </span>
                    </div>
                    <span className="text-xs text-gray-500">
                      {result.timestamp.toLocaleTimeString()}
                    </span>
                  </div>

                  {result.result && (
                    <div className="relative">
                      <pre className="text-xs bg-gray-900 text-green-400 p-2 rounded overflow-x-auto max-h-32">
                        {JSON.stringify(result.result, null, 2)}
                      </pre>
                      <button
                        onClick={() => copyResult(result.result)}
                        className="absolute top-2 right-2 p-1 bg-gray-800 text-gray-300 hover:text-white rounded"
                        title="Copiar resultado"
                      >
                        <Copy size={12} />
                      </button>
                    </div>
                  )}

                  {result.error && (
                    <p className="text-xs text-red-700 font-mono">{result.error}</p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Command Input Modal */}
      {activeCommand && (
        <Modal
          open={!!activeCommand}
          onClose={() => setActiveCommand(null)}
          title={COMMANDS.find(c => c.id === activeCommand)?.name || 'Comando'}
        >
          <form
            onSubmit={e => {
              e.preventDefault();
              handleExecuteCommand(activeCommand);
            }}
            className="space-y-4"
          >
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Parámetros (JSON)
              </label>
              <textarea
                value={commandInput}
                onChange={e => setCommandInput(e.target.value)}
                placeholder={`{
  "agent_type": "content",
  "task_type": "generate_blog_post"
}`}
                rows={6}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
              <p className="text-xs text-gray-500 mt-2">
                Deja vacío para usar parámetros por defecto
              </p>
            </div>
            <div className="flex justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => setActiveCommand(null)}
                className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900"
              >
                Cancelar
              </button>
              <button
                type="submit"
                disabled={executeMutation.isPending}
                className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg text-sm font-medium hover:bg-primary-700 disabled:opacity-50"
              >
                {executeMutation.isPending ? (
                  <>
                    <RefreshCw size={14} className="animate-spin" /> Ejecutando...
                  </>
                ) : (
                  <>
                    <Zap size={14} /> Ejecutar
                  </>
                )}
              </button>
            </div>
          </form>
        </Modal>
      )}
    </>
  );
}
