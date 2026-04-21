import { useState } from 'react';
import Header from '../components/layout/Header';

export default function Settings() {
  const [apiKey, setApiKey] = useState('');
  const [model, setModel] = useState('claude-sonnet-4-20250514');
  const [saved, setSaved] = useState(false);

  function handleSave(e: React.FormEvent) {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  }

  return (
    <>
      <Header title="Configuracion" />
      <div className="p-6 max-w-2xl">
        <form onSubmit={handleSave} className="bg-white rounded-xl border border-gray-200 p-6 space-y-6">
          <div>
            <h3 className="font-semibold mb-4">API & Modelo</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Anthropic API Key</label>
                <input type="password" value={apiKey} onChange={e => setApiKey(e.target.value)}
                  placeholder="sk-ant-..."
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500" />
                <p className="text-xs text-gray-400 mt-1">Configurar en backend/.env (ANTHROPIC_API_KEY)</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Modelo por defecto</label>
                <select value={model} onChange={e => setModel(e.target.value)}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500">
                  <option value="claude-sonnet-4-20250514">Claude Sonnet 4</option>
                  <option value="claude-opus-4-20250514">Claude Opus 4</option>
                  <option value="claude-haiku-4-5-20251001">Claude Haiku 4.5</option>
                </select>
              </div>
            </div>
          </div>

          <div>
            <h3 className="font-semibold mb-4">Informacion del Sistema</h3>
            <div className="bg-gray-50 rounded-lg p-4 space-y-2 text-sm text-gray-600">
              <p><span className="font-medium">Version:</span> 1.0.0</p>
              <p><span className="font-medium">Backend:</span> Python + FastAPI</p>
              <p><span className="font-medium">IA:</span> Claude API (Anthropic)</p>
              <p><span className="font-medium">Agentes:</span> 9 especializados</p>
              <p><span className="font-medium">Base de datos:</span> SQLite</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button type="submit" className="px-4 py-2 bg-primary-600 text-white rounded-lg text-sm font-medium hover:bg-primary-700">
              Guardar
            </button>
            {saved && <span className="text-sm text-green-600">Guardado correctamente</span>}
          </div>
        </form>
      </div>
    </>
  );
}
