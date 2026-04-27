"use client";
import { useState, useEffect } from "react";
import { Check, Star, ChevronDown, Flame, Shield, Clock } from "lucide-react";

const HOTMART_BASIC = "https://pay.hotmart.com/XXXXXXXX?off=basic";
const HOTMART_PLUS  = "https://pay.hotmart.com/XXXXXXXX?off=plus";
const HOTMART_VIP   = "https://pay.hotmart.com/XXXXXXXX?off=vip";

const PARTICLES = Array.from({ length: 18 }, (_, i) => ({
  id: i,
  size: Math.random() * 4 + 2,
  left: Math.random() * 100,
  delay: Math.random() * 12,
  duration: Math.random() * 10 + 12,
}));

const testimonials = [
  { name: "María G.", city: "Buenos Aires", text: "Llevaba 3 años sin poder desconectarme al dormir. En la semana 1 ya notaba diferencia. No es magia, es práctica.", stars: 5 },
  { name: "Carlos R.", city: "México DF", text: "Compré con desconfianza. Pensé que era otro libro de autoayuda. Me equivoqué completamente.", stars: 5 },
  { name: "Sofía M.", city: "Madrid", text: "El audio de 4 minutos para el loop de pensamientos es lo que más uso. Lo tengo en favoritos.", stars: 5 },
  { name: "Diego F.", city: "Bogotá", text: "Trabajo en finanzas, siempre con la cabeza a mil. Esto me cambió la relación con el final del día.", stars: 5 },
  { name: "Laura P.", city: "Santiago", text: "No creía que la meditación era para mí. Mente Pausada me demostró que lo que hacía antes no era meditación.", stars: 5 },
  { name: "Andrés T.", city: "Montevideo", text: "Mi terapeuta me lo recomendó como complemento. Funciona perfecto junto al proceso profesional.", stars: 5 },
];

const faqs = [
  { q: "¿Tengo que tener experiencia en meditación?", a: "No. Está diseñado específicamente para personas que nunca meditaron o que lo intentaron y lo dejaron. Los audios más cortos son de 3 minutos." },
  { q: "¿En cuánto tiempo veo resultados?", a: "Muchas personas reportan mejoras en la calidad del sueño y el nivel de estrés en la primera semana. No prometemos curas, prometemos práctica repetible." },
  { q: "¿Es solo para ansiedad?", a: "No. El sistema trabaja el ruido mental cotidiano: loops de pensamientos, dificultad para desconectarse, estrés acumulado por trabajo o rutina." },
  { q: "¿Cómo accedo después de comprar?", a: "Inmediatamente. Hotmart te envía el acceso a tu email. Podés ver el ebook y los audios desde cualquier dispositivo." },
  { q: "¿Tiene garantía?", a: "7 días de garantía sin preguntas. Si no estás satisfecho, te devolvemos el 100%. Hotmart gestiona la garantía automáticamente." },
  { q: "¿Cuál es la diferencia entre los planes?", a: "Basic: ebook + 7 audios. Plus: todo lo anterior + 14 audios extra + comunidad. VIP: todo lo anterior + sesión 1:1 de 45 min + recursos premium." },
];

function Stars({ n }: { n: number }) {
  return <div className="flex gap-0.5">{Array.from({ length: n }).map((_, i) => <Star key={i} size={13} fill="#A84028" color="#A84028" />)}</div>;
}

function CountdownTimer() {
  const [time, setTime] = useState({ h: 11, m: 47, s: 33 });
  useEffect(() => {
    const t = setInterval(() => {
      setTime(prev => {
        let { h, m, s } = prev;
        s--; if (s < 0) { s = 59; m--; } if (m < 0) { m = 59; h--; } if (h < 0) { h = 23; m = 59; s = 59; }
        return { h, m, s };
      });
    }, 1000);
    return () => clearInterval(t);
  }, []);
  const pad = (n: number) => String(n).padStart(2, "0");
  return (
    <div className="flex items-center gap-2 sans">
      {[{ v: time.h, l: "hs" }, { v: time.m, l: "min" }, { v: time.s, l: "seg" }].map(({ v, l }, i) => (
        <div key={i} className="flex items-center gap-2">
          <div className="text-center">
            <div className="bg-[#1A1816] text-[#F5EDD8] font-bold text-xl px-3 py-1.5 rounded-lg min-w-[48px]">{pad(v)}</div>
            <div className="text-[9px] text-[#F5EDD8]/50 mt-0.5 uppercase tracking-wider">{l}</div>
          </div>
          {i < 2 && <span className="text-[#F5EDD8]/60 font-bold text-xl mb-4">:</span>}
        </div>
      ))}
    </div>
  );
}

function FAQ({ q, a }: { q: string; a: string }) {
  const [open, setOpen] = useState(false);
  return (
    <div className={`border rounded-2xl transition-all duration-300 overflow-hidden ${open ? "border-[#A84028]/40 bg-[#A84028]/5" : "border-[#1A1816]/10 bg-white/50"}`}>
      <button onClick={() => setOpen(!open)} className="w-full flex items-center justify-between gap-4 p-6 text-left">
        <span className="text-[#1A1816] font-medium text-sm leading-snug">{q}</span>
        <ChevronDown size={18} className={`text-[#A84028] shrink-0 transition-transform duration-300 ${open ? "rotate-180" : ""}`} />
      </button>
      {open && <p className="px-6 pb-6 text-[#1A1816]/60 text-sm leading-relaxed">{a}</p>}
    </div>
  );
}

export default function Landing() {
  return (
    <main className="min-h-screen overflow-x-hidden">

      {/* URGENCY BAR */}
      <div className="bg-[#1A1816] text-[#F5EDD8] text-center py-2.5 px-4 sans text-xs flex items-center justify-center gap-3 flex-wrap">
        <Flame size={13} className="text-[#A84028]" />
        <span>Oferta por tiempo limitado — el precio sube en:</span>
        <CountdownTimer />
      </div>

      {/* NAV */}
      <nav className="sticky top-0 z-50 bg-[#F5EDD8]/95 backdrop-blur border-b border-[#A84028]/10 px-6 py-4 flex items-center justify-between">
        <span className="text-[#A84028] font-bold tracking-widest text-xs sans uppercase">Mente Pausada</span>
        <a href="#precios" className="sans text-xs bg-[#A84028] text-[#F5EDD8] px-4 py-2 rounded-full hover:bg-[#8a3320] transition-colors font-medium">
          Quiero empezar →
        </a>
      </nav>

      {/* HERO — terracota diagonal */}
      <section className="clip-diagonal bg-[#A84028] text-[#F5EDD8] pt-20 pb-40 px-6 relative overflow-hidden min-h-[85vh] flex items-center">
        {/* Particles */}
        {PARTICLES.map(p => (
          <span key={p.id} className="particle" style={{
            width: p.size, height: p.size,
            left: `${p.left}%`, bottom: "-10px",
            animationDelay: `${p.delay}s`,
            animationDuration: `${p.duration}s`,
            opacity: 0.4,
          }} />
        ))}
        <div className="max-w-3xl mx-auto text-center relative z-10">
          <p className="sans text-[#F5EDD8]/60 text-[11px] tracking-[0.4em] uppercase mb-8">Protocolo guiado de 7 días</p>
          <h1 className="text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-bold leading-[0.95] mb-6">
            Tu cerebro no tiene<br />
            botón de apagado.
          </h1>
          <p className="text-2xl sm:text-3xl md:text-4xl italic font-normal text-[#F5EDD8]/70 mb-10">
            <span className="shimmer font-bold not-italic">Ruido Mental Cero</span> sí lo crea.
          </p>
          <p className="sans text-[#F5EDD8]/60 text-sm mb-10 max-w-md mx-auto">
            El sistema simple para personas con la mente que no para. Sin misticismo. Sin terapia larga. Sin excusas.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a href={HOTMART_PLUS} target="_blank" rel="noopener noreferrer"
              className="sans font-bold bg-[#F5EDD8] text-[#A84028] px-8 py-4 rounded-full text-base hover:bg-white hover:scale-105 transition-all shadow-xl shadow-[#1A1816]/30">
              Quiero empezar — $149 USD
            </a>
            <a href="#que-incluye"
              className="sans font-medium border border-[#F5EDD8]/30 text-[#F5EDD8]/80 px-8 py-4 rounded-full text-base hover:border-[#F5EDD8]/60 hover:text-[#F5EDD8] transition-all">
              Ver qué incluye ↓
            </a>
          </div>
          <p className="sans text-[#F5EDD8]/40 text-xs mt-6">+2.400 personas ya encontraron su pausa · Garantía 7 días</p>
        </div>
      </section>

      {/* DOLOR — crema */}
      <section className="bg-[#F5EDD8] py-24 px-6 -mt-2">
        <div className="max-w-2xl mx-auto text-center mb-14">
          <p className="sans text-[#A84028] text-[11px] tracking-[0.4em] uppercase mb-4">¿Te resulta conocido?</p>
          <h2 className="text-4xl sm:text-5xl font-bold text-[#1A1816] leading-tight">
            El ruido mental te está<br />
            <em className="text-[#A84028] not-italic italic">robando la vida</em>
          </h2>
          <p className="text-[#1A1816]/50 mt-4">Tu esfuerzo por calmarte siempre es en vano. La mente nunca se detiene.</p>
        </div>
        <div className="max-w-3xl mx-auto grid sm:grid-cols-2 gap-4">
          {[
            { icon: "🌙", text: "Te acostás y tu cabeza empieza a repasar todo lo que pasó y lo que puede pasar mañana." },
            { icon: "😮‍💨", text: "Sabés que «tenés que relajarte» pero no sabés cómo. Respirar hondo no alcanza." },
            { icon: "🧘", text: "Probaste meditar, lo dejaste. Sentías que lo hacías mal o que no era para vos." },
            { icon: "💼", text: "El estrés del trabajo se te pega al cuerpo y llega al fin de semana contigo." },
          ].map((item) => (
            <div key={item.icon} className="flex gap-4 p-6 rounded-2xl bg-white border border-[#A84028]/10 hover:border-[#A84028]/30 hover:shadow-md transition-all">
              <span className="text-2xl shrink-0">{item.icon}</span>
              <p className="text-[#1A1816]/70 text-sm leading-relaxed">{item.text}</p>
            </div>
          ))}
        </div>
        <p className="text-center text-[#1A1816]/40 text-sm italic mt-10 max-w-md mx-auto">
          Y está más cerca de lo que creés.
        </p>
      </section>

      {/* SOLUCIÓN — terracota diagonal inversa */}
      <section className="clip-diagonal-rev bg-[#A84028] text-[#F5EDD8] py-32 px-6 relative overflow-hidden">
        {PARTICLES.slice(0, 8).map(p => (
          <span key={p.id} className="particle" style={{ width: p.size, height: p.size, left: `${p.left}%`, bottom: "-10px", animationDelay: `${p.delay + 2}s`, animationDuration: `${p.duration}s`, opacity: 0.3 }} />
        ))}
        <div className="max-w-2xl mx-auto text-center relative z-10">
          <p className="sans text-[#F5EDD8]/50 text-[11px] tracking-[0.4em] uppercase mb-4">La solución</p>
          <h2 className="text-4xl sm:text-5xl font-bold mb-4">
            Ruido Mental<br /><em className="italic font-normal text-[#F5EDD8]/80">Cero</em>
          </h2>
          <p className="text-[#F5EDD8]/70 text-lg mb-6">No es motivación. Es un sistema que entrena tu cerebro para silenciar el ruido — en 7 noches.</p>
          <a href="#que-incluye" className="sans inline-block text-sm text-[#F5EDD8]/60 hover:text-[#F5EDD8] transition-colors">¿Qué incluye? ↓</a>
        </div>
      </section>

      {/* QUÉ INCLUYE — crema */}
      <section id="que-incluye" className="bg-[#F5EDD8] py-24 px-6">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-14">
            <p className="sans text-[#A84028] text-[11px] tracking-[0.4em] uppercase mb-4">Qué incluye</p>
            <h2 className="text-4xl sm:text-5xl font-bold text-[#1A1816]">No es un libro más<br /><em className="italic text-[#A84028]">de autoayuda</em></h2>
          </div>
          <div className="grid sm:grid-cols-2 gap-6">
            {[
              { icon: "📖", num: "01", title: "Ebook Ruido Mental Cero", desc: "El framework completo en 3 fases: Reconocer, Pausar, Anclar. Sin rodeos, sin relleno. 90 minutos de lectura." },
              { icon: "🎧", num: "02", title: "7 audios guiados base", desc: "De 3 a 12 minutos. Para el momento exacto: antes de dormir, en crisis, en pausa de trabajo. Ya están ahí cuando los necesitás." },
              { icon: "⚡", num: "03", title: "Protocolo PAUSA de 4 min", desc: "El audio más usado del sistema. Para cuando el loop de pensamientos no para. Funciona en el trabajo, el auto, el baño." },
              { icon: "🗓️", num: "04", title: "Guía de práctica 21 días", desc: "Sistema de hábitos progresivos para que no lo dejes en la semana 1. Sin apps. Sin suscripciones adicionales." },
            ].map((item) => (
              <div key={item.num} className="group p-7 rounded-3xl border border-[#A84028]/10 bg-white hover:border-[#A84028]/30 hover:shadow-lg transition-all">
                <div className="flex items-start justify-between mb-4">
                  <span className="text-3xl">{item.icon}</span>
                  <span className="sans text-[#A84028]/30 text-xs font-bold">{item.num}</span>
                </div>
                <h3 className="text-[#1A1816] font-bold text-lg mb-2">{item.title}</h3>
                <p className="text-[#1A1816]/55 text-sm leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
          <div className="mt-8 p-6 rounded-2xl bg-[#A84028]/8 border border-[#A84028]/20 text-center">
            <p className="text-[#A84028] font-bold sans">Acceso inmediato después de la compra</p>
            <p className="text-[#1A1816]/50 text-sm sans mt-1">Todo en tu email en segundos. Desde cualquier dispositivo. De por vida.</p>
          </div>
        </div>
      </section>

      {/* TESTIMONIOS — oscuro con partículas */}
      <section className="bg-[#1A1816] py-24 px-6 relative overflow-hidden">
        {PARTICLES.map(p => (
          <span key={p.id} className="particle" style={{ width: p.size * 0.7, height: p.size * 0.7, left: `${p.left}%`, bottom: "-5px", animationDelay: `${p.delay}s`, animationDuration: `${p.duration + 5}s`, opacity: 0.2 }} />
        ))}
        <div className="max-w-5xl mx-auto relative z-10">
          <div className="text-center mb-14">
            <p className="sans text-[#A84028] text-[11px] tracking-[0.4em] uppercase mb-4">Lo que dicen</p>
            <h2 className="text-4xl sm:text-5xl font-bold text-[#F5EDD8]">Personas reales,<br /><em className="italic text-[#C4A882]">resultados reales</em></h2>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {testimonials.map((t) => (
              <div key={t.name} className="p-6 rounded-2xl border border-[#F5EDD8]/8 bg-[#F5EDD8]/4 hover:bg-[#F5EDD8]/7 transition-colors">
                <Stars n={t.stars} />
                <p className="text-[#F5EDD8]/75 text-sm leading-relaxed mt-3 mb-4 italic">«{t.text}»</p>
                <div>
                  <p className="text-[#C4A882] text-sm font-bold sans">{t.name}</p>
                  <p className="text-[#F5EDD8]/30 text-xs sans">{t.city}</p>
                </div>
              </div>
            ))}
          </div>
          <div className="flex justify-center mt-10 gap-8 text-center">
            {[["2.400+", "personas"], ["4.9/5", "valoración"], ["7 días", "garantía"]].map(([v, l]) => (
              <div key={l}>
                <p className="text-3xl font-bold text-[#F5EDD8]">{v}</p>
                <p className="text-[#F5EDD8]/40 text-xs sans uppercase tracking-wider mt-1">{l}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* PRECIOS */}
      <section id="precios" className="bg-[#F5EDD8] py-24 px-6">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-6">
            <p className="sans text-[#A84028] text-[11px] tracking-[0.4em] uppercase mb-4">Elegí tu nivel</p>
            <h2 className="text-4xl sm:text-5xl font-bold text-[#1A1816]">Invertí una vez.<br /><em className="italic text-[#A84028]">Usalo siempre.</em></h2>
          </div>
          <div className="flex items-center justify-center gap-2 mb-12">
            <Clock size={14} className="text-[#A84028]" />
            <span className="sans text-sm text-[#1A1816]/60">Precio especial termina en:</span>
            <CountdownTimer />
          </div>
          <div className="grid sm:grid-cols-3 gap-6">

            {/* BASIC */}
            <div className="p-8 rounded-3xl border border-[#1A1816]/10 bg-white flex flex-col">
              <p className="sans text-xs text-[#A84028]/60 uppercase tracking-wider mb-2">Basic</p>
              <div className="mb-1">
                <span className="text-4xl font-bold text-[#1A1816]">$99</span>
                <span className="text-[#1A1816]/40 text-sm sans ml-2">USD</span>
              </div>
              <p className="sans text-xs text-[#1A1816]/40 mb-6">pago único · acceso de por vida</p>
              <ul className="space-y-3 flex-1 mb-8">
                {["Ebook Ruido Mental Cero", "7 audios guiados (3-12 min)", "Protocolo PAUSA 4 min", "Guía de práctica 21 días", "Acceso inmediato"].map(i => (
                  <li key={i} className="flex gap-2.5 text-sm text-[#1A1816]/70">
                    <Check size={14} className="text-[#A84028] shrink-0 mt-0.5" />{i}
                  </li>
                ))}
              </ul>
              <a href={HOTMART_BASIC} target="_blank" rel="noopener noreferrer"
                className="sans text-center text-sm font-medium border-2 border-[#A84028]/30 text-[#A84028] py-3.5 rounded-full hover:border-[#A84028] hover:bg-[#A84028]/5 transition-all">
                Empezar con Basic
              </a>
            </div>

            {/* PLUS — destacado */}
            <div className="p-8 rounded-3xl border-2 border-[#A84028] bg-[#A84028] flex flex-col text-[#F5EDD8] relative shadow-2xl shadow-[#A84028]/30 scale-105">
              <div className="absolute -top-4 left-1/2 -translate-x-1/2">
                <span className="sans text-[10px] font-bold text-[#A84028] bg-[#F5EDD8] px-4 py-1.5 rounded-full uppercase tracking-wider shadow-md">⭐ Más elegido</span>
              </div>
              <p className="sans text-xs text-[#F5EDD8]/60 uppercase tracking-wider mb-2">Plus</p>
              <div className="mb-1">
                <span className="text-4xl font-bold">$149</span>
                <span className="text-[#F5EDD8]/50 text-sm sans ml-2">USD</span>
              </div>
              <p className="sans text-xs text-[#F5EDD8]/50 mb-6">pago único · acceso de por vida</p>
              <ul className="space-y-3 flex-1 mb-8">
                {["Todo lo de Basic", "14 audios extra por situación", "Audios de insomnio, trabajo y crisis", "Comunidad privada de práctica", "Actualizaciones futuras incluidas"].map(i => (
                  <li key={i} className="flex gap-2.5 text-sm text-[#F5EDD8]/85">
                    <Check size={14} className="text-[#F5EDD8] shrink-0 mt-0.5" />{i}
                  </li>
                ))}
              </ul>
              <a href={HOTMART_PLUS} target="_blank" rel="noopener noreferrer"
                className="sans text-center text-sm font-bold bg-[#F5EDD8] text-[#A84028] py-3.5 rounded-full hover:bg-white hover:scale-105 transition-all shadow-lg">
                Quiero el Plus — $149
              </a>
            </div>

            {/* VIP */}
            <div className="p-8 rounded-3xl border border-[#1A1816]/10 bg-white flex flex-col">
              <p className="sans text-xs text-[#A84028]/60 uppercase tracking-wider mb-2">VIP</p>
              <div className="mb-1">
                <span className="text-4xl font-bold text-[#1A1816]">$199</span>
                <span className="text-[#1A1816]/40 text-sm sans ml-2">USD</span>
              </div>
              <p className="sans text-xs text-[#1A1816]/40 mb-6">pago único · acceso de por vida</p>
              <ul className="space-y-3 flex-1 mb-8">
                {["Todo lo de Plus", "Sesión 1:1 de 45 minutos", "Diagnóstico de tu patrón de ruido", "Recursos avanzados premium", "Soporte directo prioritario"].map(i => (
                  <li key={i} className="flex gap-2.5 text-sm text-[#1A1816]/70">
                    <Check size={14} className="text-[#A84028] shrink-0 mt-0.5" />{i}
                  </li>
                ))}
              </ul>
              <a href={HOTMART_VIP} target="_blank" rel="noopener noreferrer"
                className="sans text-center text-sm font-medium border-2 border-[#A84028]/30 text-[#A84028] py-3.5 rounded-full hover:border-[#A84028] hover:bg-[#A84028]/5 transition-all">
                Quiero el VIP
              </a>
            </div>
          </div>

          {/* Garantías */}
          <div className="flex flex-wrap justify-center gap-6 mt-10">
            {[
              { icon: <Shield size={16} />, text: "7 días de garantía total" },
              { icon: <Check size={16} />, text: "Acceso inmediato por Hotmart" },
              { icon: <Clock size={16} />, text: "De por vida, sin suscripción" },
            ].map(({ icon, text }) => (
              <div key={text} className="flex items-center gap-2 sans text-sm text-[#1A1816]/50">
                <span className="text-[#A84028]">{icon}</span>{text}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="bg-[#1A1816] py-24 px-6 relative overflow-hidden">
        {PARTICLES.slice(0, 6).map(p => (
          <span key={p.id} className="particle" style={{ width: p.size * 0.5, height: p.size * 0.5, left: `${p.left}%`, bottom: "-5px", animationDelay: `${p.delay + 3}s`, animationDuration: `${p.duration + 3}s`, opacity: 0.15 }} />
        ))}
        <div className="max-w-2xl mx-auto relative z-10">
          <div className="text-center mb-12">
            <p className="sans text-[#A84028] text-[11px] tracking-[0.4em] uppercase mb-4">Preguntas</p>
            <h2 className="text-4xl font-bold text-[#F5EDD8]">Todo lo que querés saber</h2>
          </div>
          <div className="space-y-3">
            {faqs.map((f) => <FAQ key={f.q} q={f.q} a={f.a} />)}
          </div>
        </div>
      </section>

      {/* CTA FINAL — terracota */}
      <section className="bg-[#A84028] py-24 px-6 text-center relative overflow-hidden">
        {PARTICLES.map(p => (
          <span key={p.id} className="particle" style={{ width: p.size, height: p.size, left: `${p.left}%`, bottom: "-10px", animationDelay: `${p.delay}s`, animationDuration: `${p.duration}s`, opacity: 0.35 }} />
        ))}
        <div className="max-w-2xl mx-auto relative z-10">
          <p className="sans text-[#F5EDD8]/50 text-[11px] tracking-[0.4em] uppercase mb-6">¿Listo para empezar?</p>
          <h2 className="text-4xl sm:text-5xl font-bold text-[#F5EDD8] mb-4">
            Tu mente no necesita parar.<br />
            <em className="italic font-normal text-[#F5EDD8]/70">Necesita aprender a pausar.</em>
          </h2>
          <p className="sans text-[#F5EDD8]/60 mb-10 max-w-md mx-auto text-sm">
            5 minutos al día. 21 días de práctica. Sin apps, sin suscripciones, sin excusas.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a href={HOTMART_PLUS} target="_blank" rel="noopener noreferrer"
              className="sans font-bold bg-[#F5EDD8] text-[#A84028] px-8 py-4 rounded-full text-base hover:bg-white hover:scale-105 transition-all shadow-xl">
              Empezar ahora — $149 USD
            </a>
            <a href={HOTMART_BASIC} target="_blank" rel="noopener noreferrer"
              className="sans font-medium border border-[#F5EDD8]/30 text-[#F5EDD8]/80 px-8 py-4 rounded-full text-base hover:border-[#F5EDD8]/60 hover:text-[#F5EDD8] transition-all">
              O empezar con Basic — $99
            </a>
          </div>
          <p className="sans text-[#F5EDD8]/30 text-xs mt-6">7 días de garantía · Acceso inmediato · Sin riesgos</p>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="bg-[#1A1816] py-8 px-6 text-center border-t border-[#F5EDD8]/5">
        <p className="sans text-[#F5EDD8]/25 text-xs">© 2026 Mente Pausada — Este producto no reemplaza atención psicológica o psiquiátrica profesional.</p>
        <p className="sans text-[#F5EDD8]/15 text-xs mt-1">
          Consultas: <a href="mailto:lucasjolivera3@gmail.com" className="hover:text-[#A84028] transition-colors">lucasjolivera3@gmail.com</a>
        </p>
      </footer>

    </main>
  );
}
