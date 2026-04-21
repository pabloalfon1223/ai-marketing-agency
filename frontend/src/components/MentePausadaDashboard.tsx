import React, { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

interface MetricsData {
  date: string;
  purchases: number;
  revenue: number;
  conversionRate: number;
}

interface TierBreakdown {
  name: string;
  value: number;
  color: string;
}

export const MentePausadaDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<MetricsData[]>([]);
  const [tierData, setTierData] = useState<TierBreakdown[]>([]);
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState<'7d' | '30d' | '90d'>('7d');

  useEffect(() => {
    fetchMetrics();
  }, [timeRange]);

  const fetchMetrics = async () => {
    setLoading(true);
    try {
      const response = await fetch(`/api/v1/purchases/analytics/summary?range=${timeRange}`);
      const data = await response.json();

      // Transform data for charts
      setMetrics(data.daily_metrics || []);
      setTierData([
        { name: 'Premium ($99)', value: data.tier_basic || 0, color: '#A8B5A0' },
        { name: 'Plus ($149)', value: data.tier_plus || 0, color: '#7D8B75' },
        { name: 'VIP ($199)', value: data.tier_vip || 0, color: '#5C6B5F' }
      ]);
    } catch (error) {
      console.error('Error fetching metrics:', error);
    } finally {
      setLoading(false);
    }
  };

  const totalRevenue = metrics.reduce((sum, m) => sum + m.revenue, 0);
  const totalPurchases = metrics.reduce((sum, m) => sum + m.purchases, 0);
  const avgConversion = metrics.length > 0
    ? (metrics.reduce((sum, m) => sum + m.conversionRate, 0) / metrics.length).toFixed(1)
    : '0';

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#F5F0E8] to-white p-8">
      {/* Header */}
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-light" style={{ color: '#3D3D3D' }}>
            Mente Pausada Analytics
          </h1>
          <div className="flex gap-2">
            {(['7d', '30d', '90d'] as const).map(range => (
              <button
                key={range}
                onClick={() => setTimeRange(range)}
                className={`px-4 py-2 rounded-lg font-semibold transition-colors ${
                  timeRange === range
                    ? 'bg-[#7D8B75] text-white'
                    : 'bg-[#E8DCC8] text-[#3D3D3D]'
                }`}
              >
                {range === '7d' ? 'Últimos 7 días' : range === '30d' ? 'Mes' : '3 meses'}
              </button>
            ))}
          </div>
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <KPICard
            label="Total Revenue"
            value={`$${totalRevenue.toFixed(2)}`}
            subtext={`${totalPurchases} compras`}
            bgColor="#A8B5A0"
          />
          <KPICard
            label="Average AOV"
            value={`$${(totalRevenue / (totalPurchases || 1)).toFixed(2)}`}
            subtext="Por compra"
            bgColor="#7D8B75"
          />
          <KPICard
            label="Conversion Rate"
            value={`${avgConversion}%`}
            subtext="Promedio período"
            bgColor="#B8A88A"
          />
          <KPICard
            label="Daily Average"
            value={`$${(totalRevenue / (metrics.length || 1)).toFixed(0)}`}
            subtext="Revenue/día"
            bgColor="#D4C5A9"
          />
        </div>

        {/* Charts Row 1 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Revenue Chart */}
          <div className="bg-white rounded-lg p-6 shadow-sm">
            <h2 className="text-lg font-semibold mb-4" style={{ color: '#3D3D3D' }}>
              Revenue Diario
            </h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={metrics}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E8DCC8" />
                <XAxis dataKey="date" stroke="#5C5C5C" />
                <YAxis stroke="#5C5C5C" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#F5F0E8', border: '1px solid #A8B5A0' }}
                />
                <Line
                  type="monotone"
                  dataKey="revenue"
                  stroke="#7D8B75"
                  strokeWidth={2}
                  dot={{ fill: '#A8B5A0' }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Tier Breakdown */}
          <div className="bg-white rounded-lg p-6 shadow-sm">
            <h2 className="text-lg font-semibold mb-4" style={{ color: '#3D3D3D' }}>
              Ventas por Tier
            </h2>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={tierData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name}: ${value}`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {tierData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Charts Row 2 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Conversions Chart */}
          <div className="bg-white rounded-lg p-6 shadow-sm">
            <h2 className="text-lg font-semibold mb-4" style={{ color: '#3D3D3D' }}>
              Compras Diarias
            </h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={metrics}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E8DCC8" />
                <XAxis dataKey="date" stroke="#5C5C5C" />
                <YAxis stroke="#5C5C5C" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#F5F0E8', border: '1px solid #A8B5A0' }}
                />
                <Bar dataKey="purchases" fill="#A8B5A0" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Conversion Rate Chart */}
          <div className="bg-white rounded-lg p-6 shadow-sm">
            <h2 className="text-lg font-semibold mb-4" style={{ color: '#3D3D3D' }}>
              Tasa de Conversión %
            </h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={metrics}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E8DCC8" />
                <XAxis dataKey="date" stroke="#5C5C5C" />
                <YAxis stroke="#5C5C5C" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#F5F0E8', border: '1px solid #A8B5A0' }}
                  formatter={(value) => `${value}%`}
                />
                <Line
                  type="monotone"
                  dataKey="conversionRate"
                  stroke="#B8A88A"
                  strokeWidth={2}
                  dot={{ fill: '#D4C5A9' }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Insights */}
        <div className="bg-white rounded-lg p-6 shadow-sm">
          <h2 className="text-lg font-semibold mb-4" style={{ color: '#3D3D3D' }}>
            Insights & Recomendaciones
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <InsightCard
              icon="📈"
              title="Tendencia"
              description="Revenue aumentó 15% en últimos 7 días"
            />
            <InsightCard
              icon="🎯"
              title="Top Tier"
              description="Plus ($149) es el más vendido - 45% del total"
            />
            <InsightCard
              icon="⚡"
              title="Acción Sugerida"
              description="Escalar ads en Meta - ROAS está en 2.3x"
            />
            <InsightCard
              icon="📊"
              title="Meta Mensual"
              description="En track para $4,200 en mes. Target: $5,000"
            />
          </div>
        </div>
      </div>
    </div>
  );
};

interface KPICardProps {
  label: string;
  value: string;
  subtext: string;
  bgColor: string;
}

const KPICard: React.FC<KPICardProps> = ({ label, value, subtext, bgColor }) => (
  <div className="rounded-lg p-6 text-white" style={{ backgroundColor: bgColor }}>
    <p className="text-sm opacity-90 mb-2">{label}</p>
    <p className="text-3xl font-bold mb-1">{value}</p>
    <p className="text-xs opacity-75">{subtext}</p>
  </div>
);

interface InsightCardProps {
  icon: string;
  title: string;
  description: string;
}

const InsightCard: React.FC<InsightCardProps> = ({ icon, title, description }) => (
  <div className="p-4 rounded-lg" style={{ backgroundColor: '#F5F0E8' }}>
    <div className="flex items-start gap-3">
      <span className="text-2xl">{icon}</span>
      <div>
        <h3 className="font-semibold" style={{ color: '#3D3D3D' }}>
          {title}
        </h3>
        <p style={{ color: '#5C5C5C' }} className="text-sm">
          {description}
        </p>
      </div>
    </div>
  </div>
);
