import React, { useState } from 'react';
import { loadStripe } from '@stripe/stripe-js';

const stripePromise = loadStripe(process.env.REACT_APP_STRIPE_PUBLIC_KEY || '');

export const MentePausadaLanding: React.FC = () => {
  const [selectedTier, setSelectedTier] = useState<'basic' | 'plus' | 'vip'>('plus');
  const [loading, setLoading] = useState(false);
  const [email, setEmail] = useState('');

  const tiers = {
    basic: {
      name: 'Premium',
      price: 99,
      description: 'Ebook + audios + comunidad',
      features: [
        '✓ Ebook completo (80 págs)',
        '✓ 25 audios (micro-prácticas)',
        '✓ Acceso comunidad privada 6 meses',
        '✓ Guía de hábitos PDF',
      ],
      cta: 'Obtener ahora'
    },
    plus: {
      name: 'Premium Plus',
      price: 149,
      description: 'Todo + plantillas + email semanal',
      popular: true,
      features: [
        '✓ Todo Premium +',
        '✓ 5 plantillas Notion',
        '✓ Email semanal 6 meses',
        '✓ Q&A mensual en vivo',
      ],
      cta: 'Comprar ahora'
    },
    vip: {
      name: 'Premium VIP',
      price: 199,
      description: 'Máximo acceso + 1-on-1 coaching',
      features: [
        '✓ Todo Premium Plus +',
        '✓ Dashboard privado',
        '✓ Chat prioritario (48hs)',
        '✓ Sesión 1-on-1 coaching',
      ],
      cta: 'Acceso VIP'
    }
  };

  const handleCheckout = async (tier: string) => {
    if (!email) {
      alert('Por favor ingresa tu email');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('/api/v1/create-checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tier,
          email,
          product: 'mente-pausada-ebook'
        })
      });

      const { sessionId } = await response.json();
      const stripe = await stripePromise;
      await stripe?.redirectToCheckout({ sessionId });
    } catch (error) {
      console.error('Error:', error);
      alert('Error al procesar. Intenta de nuevo.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#F5F0E8] to-white">
      {/* Header */}
      <header className="px-6 py-8 text-center">
        <h1 className="text-4xl md:text-5xl font-light mb-3" style={{ color: '#3D3D3D' }}>
          Mente Pausada
        </h1>
        <p className="text-lg" style={{ color: '#5C5C5C' }}>
          Aprende a calmarte en 1 minuto. Para personas ocupadas que necesitan paz.
        </p>
      </header>

      {/* Problem */}
      <section className="px-6 py-12 max-w-2xl mx-auto text-center">
        <p className="text-xl mb-6" style={{ color: '#3D3D3D' }}>
          Estás siempre acelerado/a. Sientes que no puedes parar. La ansiedad te domina.
        </p>
        <p className="text-lg" style={{ color: '#5C5C5C' }}>
          No necesitas más tiempo, necesitas técnicas que funcionen <strong>YA</strong>.
        </p>
      </section>

      {/* Testimonials */}
      <section className="px-6 py-12 max-w-4xl mx-auto">
        <div className="grid md:grid-cols-3 gap-6">
          {[
            { text: '"En 1 minuto mi respiración cambió. Es increíble."', author: 'María, 32' },
            { text: '"Ahora puedo parar antes de explotar. Gracias."', author: 'Juan, 38' },
            { text: '"No creía que los audios funcionaran. Me equivocaba."', author: 'Ana, 28' }
          ].map((testimonial, i) => (
            <div key={i} className="p-6 rounded-lg" style={{ backgroundColor: '#E8DCC8' }}>
              <p className="italic mb-3">{testimonial.text}</p>
              <p className="font-semibold" style={{ color: '#7D8B75' }}>— {testimonial.author}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Email + Pricing */}
      <section className="px-6 py-12 max-w-4xl mx-auto">
        <div className="mb-8 text-center">
          <input
            type="email"
            placeholder="Tu email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="px-4 py-3 border-2 rounded-lg w-full md:w-96 mb-6"
            style={{ borderColor: '#A8B5A0' }}
          />
        </div>

        {/* Pricing Cards */}
        <div className="grid md:grid-cols-3 gap-6">
          {(Object.entries(tiers) as any[]).map(([key, tier]) => (
            <div
              key={key}
              className={`rounded-lg p-8 relative transition-transform hover:scale-105 ${
                tier.popular ? 'ring-2' : ''
              }`}
              style={{
                backgroundColor: tier.popular ? '#A8B5A0' : '#F5F0E8',
                ringColor: '#7D8B75'
              }}
            >
              {tier.popular && (
                <div className="absolute top-3 right-3 text-sm font-bold px-3 py-1 rounded" style={{ backgroundColor: '#E8DCC8' }}>
                  Popular
                </div>
              )}
              <h3 className="text-2xl font-semibold mb-2" style={{ color: '#3D3D3D' }}>
                {tier.name}
              </h3>
              <p className="text-sm mb-4" style={{ color: '#5C5C5C' }}>
                {tier.description}
              </p>
              <div className="mb-6">
                <span className="text-4xl font-bold" style={{ color: '#3D3D3D' }}>
                  ${tier.price}
                </span>
                <span style={{ color: '#5C5C5C' }}> USD</span>
              </div>
              <ul className="mb-8 space-y-2">
                {tier.features.map((feature: string, i: number) => (
                  <li key={i} style={{ color: '#3D3D3D' }}>
                    {feature}
                  </li>
                ))}
              </ul>
              <button
                onClick={() => {
                  setSelectedTier(key as any);
                  handleCheckout(key);
                }}
                disabled={loading}
                className="w-full py-3 rounded-lg font-semibold transition-opacity disabled:opacity-50"
                style={{
                  backgroundColor: '#7D8B75',
                  color: 'white'
                }}
              >
                {loading ? 'Procesando...' : tier.cta}
              </button>
            </div>
          ))}
        </div>
      </section>

      {/* FAQ */}
      <section className="px-6 py-12 max-w-2xl mx-auto">
        <h2 className="text-3xl font-light mb-8 text-center" style={{ color: '#3D3D3D' }}>
          Preguntas frecuentes
        </h2>
        <div className="space-y-6">
          {[
            { q: '¿Hay garantía?', a: '30 días de garantía 100% dinero de vuelta. Sin preguntas.' },
            { q: '¿Es para mí si no medito?', a: 'Especialmente para ti. No necesitas experiencia, es fácil.' },
            { q: '¿Cuánto tiempo toman los audios?', a: 'Entre 1 y 10 minutos cada uno. Puedes hacerlos en cualquier lugar.' },
            { q: '¿Acceso de por vida?', a: 'Sí. Una compra, acceso permanente al ebook y audios.' }
          ].map((faq, i) => (
            <div key={i}>
              <h4 className="font-semibold mb-2" style={{ color: '#3D3D3D' }}>
                {faq.q}
              </h4>
              <p style={{ color: '#5C5C5C' }}>{faq.a}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Disclaimer */}
      <footer className="px-6 py-8 text-center" style={{ color: '#5C5C5C' }}>
        <p className="text-sm">
          Mente Pausada no reemplaza terapia profesional.
          Si experimentas crisis, contacta a profesionales.
        </p>
      </footer>
    </div>
  );
};
