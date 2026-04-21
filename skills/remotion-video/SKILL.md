---
name: remotion-video
description: >
  Crea videos con motion graphics usando Remotion (React + código).
  Úsalo cuando el usuario quiera hacer un reel animado, video para Instagram/TikTok,
  carrusel animado, intro/outro, o cualquier video con texto animado y motion graphics.
  Genera el código React completo para Remotion listo para renderizar.
  Aplica el brand kit de cada proyecto (Mente Pausada, Polt Mobilier, Cerebro).
---

# SKILL: Remotion Video Creator

Eres un especialista en producción de video programático con Remotion.
Creás videos de alta calidad con motion graphics usando React, exportables como MP4.

## QUÉ PRODUCE ESTE SKILL

Para cada video entregás:
1. **Código React completo** — componente Remotion listo para renderizar
2. **Estructura de escenas** — qué ocurre en cada momento del video
3. **Especificaciones técnicas** — duración, FPS, resolución
4. **Assets necesarios** — lista de imágenes, fuentes, audios a tener
5. **Comando de render** — para exportar el MP4 final

---

## SETUP (si no está instalado)

```bash
# Crear nuevo proyecto Remotion
bun create video

# O agregar a proyecto existente
npm install remotion @remotion/player @remotion/cli

# Instalar skills de Remotion (best practices para agentes IA)
npx skills add remotion-dev/skills

# Renderizar video
npx remotion render src/index.ts MyComposition output/video.mp4
```

---

## PLANTILLAS POR TIPO DE VIDEO

### 🎬 TIPO 1: REEL DE TEXTO ANIMADO (Mente Pausada / Polt)
**Duración:** 15-30 segundos | **FPS:** 30 | **Resolución:** 1080x1920 (9:16)

```tsx
// src/compositions/TextReel.tsx
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';

interface TextReelProps {
  slides: { text: string; subtitle?: string; duration: number }[];
  brandColor: string;
  bgColor: string;
  fontFamily: string;
}

export const TextReel: React.FC<TextReelProps> = ({ slides, brandColor, bgColor, fontFamily }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  // Calcular qué slide mostrar
  let elapsed = 0;
  let currentSlide = 0;
  let slideStartFrame = 0;
  for (let i = 0; i < slides.length; i++) {
    if (frame < elapsed + slides[i].duration * fps) {
      currentSlide = i;
      slideStartFrame = elapsed;
      break;
    }
    elapsed += slides[i].duration * fps;
  }
  
  const localFrame = frame - slideStartFrame;
  
  // Animación de entrada
  const opacity = spring({ frame: localFrame, fps, config: { damping: 20 } });
  const translateY = interpolate(localFrame, [0, 15], [30, 0], { extrapolateRight: 'clamp' });
  
  return (
    <AbsoluteFill style={{ backgroundColor: bgColor, justifyContent: 'center', alignItems: 'center', padding: 60 }}>
      <div style={{
        opacity,
        transform: `translateY(${translateY}px)`,
        textAlign: 'center',
        fontFamily,
      }}>
        <h1 style={{ color: brandColor, fontSize: 72, fontWeight: 700, lineHeight: 1.2, marginBottom: 20 }}>
          {slides[currentSlide]?.text}
        </h1>
        {slides[currentSlide]?.subtitle && (
          <p style={{ color: '#ffffff', fontSize: 36, fontWeight: 400, opacity: 0.85 }}>
            {slides[currentSlide].subtitle}
          </p>
        )}
      </div>
    </AbsoluteFill>
  );
};
```

---

### 🎬 TIPO 2: CARRUSEL ANIMADO (Polt Mobilier — portfolio)
**Duración:** 30-60 segundos | **FPS:** 30 | **Resolución:** 1080x1080 (1:1)

```tsx
// src/compositions/PortfolioCarrusel.tsx
import { AbsoluteFill, Img, useCurrentFrame, interpolate, spring, Sequence } from 'remotion';

interface ProjectSlide {
  imageUrl: string;
  title: string;
  description: string;
  duration: number; // en segundos
}

export const PortfolioCarrusel: React.FC<{ projects: ProjectSlide[] }> = ({ projects }) => {
  const frame = useCurrentFrame();
  const fps = 30;
  
  return (
    <AbsoluteFill style={{ backgroundColor: '#1A1A1A' }}>
      {projects.map((project, index) => {
        const startFrame = projects.slice(0, index).reduce((acc, p) => acc + p.duration * fps, 0);
        
        return (
          <Sequence key={index} from={startFrame} durationInFrames={project.duration * fps}>
            <AbsoluteFill>
              {/* Imagen de fondo con zoom sutil */}
              <Img
                src={project.imageUrl}
                style={{
                  width: '100%',
                  height: '100%',
                  objectFit: 'cover',
                  transform: `scale(${interpolate(frame - startFrame, [0, project.duration * fps], [1, 1.05])})`,
                }}
              />
              {/* Overlay gradiente */}
              <AbsoluteFill style={{
                background: 'linear-gradient(to top, rgba(0,0,0,0.8) 0%, transparent 60%)',
              }} />
              {/* Texto inferior */}
              <AbsoluteFill style={{ justifyContent: 'flex-end', padding: 60 }}>
                <h2 style={{ color: '#F5EDD8', fontSize: 48, marginBottom: 12 }}>{project.title}</h2>
                <p style={{ color: '#C4A882', fontSize: 28 }}>{project.description}</p>
              </AbsoluteFill>
            </AbsoluteFill>
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
```

---

### 🎬 TIPO 3: HOOK + COPY ANIMADO (Mente Pausada — contenido bienestar)
**Duración:** 20-30 segundos | **FPS:** 30 | **Resolución:** 1080x1920 (9:16)

```tsx
// src/compositions/MentePausadaReel.tsx
import { AbsoluteFill, useCurrentFrame, spring, interpolate, Audio } from 'remotion';

export const MentePausadaReel: React.FC<{
  hook: string;
  lines: string[];
  cta: string;
  audioUrl?: string;
}> = ({ hook, lines, cta, audioUrl }) => {
  const frame = useCurrentFrame();
  const fps = 30;
  
  // Timing de cada sección
  const HOOK_START = 0;
  const HOOK_DURATION = 60; // 2 segundos
  const LINE_DURATION = 45; // 1.5 segundos por línea
  const CTA_START = HOOK_DURATION + lines.length * LINE_DURATION;
  
  const hookOpacity = spring({ frame, fps, config: { damping: 15 } });
  
  const currentLineIndex = Math.floor((frame - HOOK_DURATION) / LINE_DURATION);
  
  return (
    <AbsoluteFill style={{
      backgroundColor: '#1A1816', // Negro profundo Mente Pausada
      justifyContent: 'center',
      alignItems: 'center',
      padding: 80,
    }}>
      {audioUrl && <Audio src={audioUrl} />}
      
      {/* HOOK */}
      {frame < HOOK_DURATION && (
        <div style={{ opacity: hookOpacity, textAlign: 'center' }}>
          <p style={{
            color: '#F5EDD8',
            fontSize: 64,
            fontFamily: 'Cormorant, serif',
            fontStyle: 'italic',
            lineHeight: 1.3,
          }}>
            {hook}
          </p>
        </div>
      )}
      
      {/* LÍNEAS DE COPY */}
      {frame >= HOOK_DURATION && frame < CTA_START && lines[currentLineIndex] && (
        <div style={{
          opacity: spring({ frame: frame - HOOK_DURATION - currentLineIndex * LINE_DURATION, fps }),
          textAlign: 'center',
        }}>
          <p style={{
            color: '#F5EDD8',
            fontSize: 56,
            fontFamily: 'DM Sans, sans-serif',
            lineHeight: 1.4,
          }}>
            {lines[currentLineIndex]}
          </p>
        </div>
      )}
      
      {/* CTA */}
      {frame >= CTA_START && (
        <div style={{ textAlign: 'center' }}>
          <p style={{ color: '#C4A882', fontSize: 48, fontFamily: 'Cormorant, serif', fontStyle: 'italic' }}>
            {cta}
          </p>
          {/* Keyword ManyChat */}
          <div style={{
            marginTop: 30,
            backgroundColor: '#C4A882',
            borderRadius: 12,
            padding: '16px 40px',
          }}>
            <p style={{ color: '#1A1816', fontSize: 42, fontWeight: 700, fontFamily: 'DM Sans' }}>
              PAUSA
            </p>
          </div>
        </div>
      )}
    </AbsoluteFill>
  );
};
```

---

### 🎬 TIPO 4: INTRO/OUTRO DE MARCA
**Duración:** 3-5 segundos | Reutilizable en todos los videos

```tsx
// src/compositions/BrandIntro.tsx
import { AbsoluteFill, useCurrentFrame, spring, interpolate } from 'remotion';

export const BrandIntro: React.FC<{ brand: 'mente-pausada' | 'polt' | 'cerebro' }> = ({ brand }) => {
  const frame = useCurrentFrame();
  const fps = 30;
  
  const configs = {
    'mente-pausada': { name: 'Mente Pausada', color: '#C4A882', bg: '#1A1816' },
    'polt': { name: 'Polt Mobilier', color: '#D4B896', bg: '#2A2420' },
    'cerebro': { name: 'Cerebro', color: '#4A9B7F', bg: '#111820' },
  };
  
  const config = configs[brand];
  const scale = spring({ frame, fps, config: { damping: 14, stiffness: 180 } });
  const opacity = interpolate(frame, [0, 10, 80, 90], [0, 1, 1, 0]);
  
  return (
    <AbsoluteFill style={{ backgroundColor: config.bg, justifyContent: 'center', alignItems: 'center', opacity }}>
      <div style={{ transform: `scale(${scale})`, textAlign: 'center' }}>
        <div style={{
          width: 80, height: 4,
          backgroundColor: config.color,
          margin: '0 auto 20px',
        }} />
        <h1 style={{ color: config.color, fontSize: 72, fontFamily: 'Cormorant, serif', fontStyle: 'italic' }}>
          {config.name}
        </h1>
        <div style={{
          width: 80, height: 4,
          backgroundColor: config.color,
          margin: '20px auto 0',
        }} />
      </div>
    </AbsoluteFill>
  );
};
```

---

## COMPOSICIÓN PRINCIPAL (index.ts)

```tsx
// src/index.ts
import { registerRoot, Composition } from 'remotion';
import { TextReel } from './compositions/TextReel';
import { PortfolioCarrusel } from './compositions/PortfolioCarrusel';
import { MentePausadaReel } from './compositions/MentePausadaReel';
import { BrandIntro } from './compositions/BrandIntro';

registerRoot(() => (
  <>
    <Composition id="TextReel" component={TextReel} durationInFrames={450} fps={30} width={1080} height={1920}
      defaultProps={{ slides: [], brandColor: '#C4A882', bgColor: '#1A1816', fontFamily: 'DM Sans' }} />
    <Composition id="PortfolioCarrusel" component={PortfolioCarrusel} durationInFrames={900} fps={30} width={1080} height={1080}
      defaultProps={{ projects: [] }} />
    <Composition id="MentePausadaReel" component={MentePausadaReel} durationInFrames={600} fps={30} width={1080} height={1920}
      defaultProps={{ hook: '', lines: [], cta: '' }} />
    <Composition id="BrandIntro" component={BrandIntro} durationInFrames={90} fps={30} width={1080} height={1920}
      defaultProps={{ brand: 'mente-pausada' }} />
  </>
));
```

---

## FLUJO DE TRABAJO

```
1. BRIEF → Definir: tipo de video, proyecto, duración, contenido
2. CÓDIGO → Generar componente React con las especificaciones
3. ASSETS → Listar imágenes/audios necesarios
4. PREVIEW → npx remotion preview src/index.ts
5. RENDER → npx remotion render src/index.ts [CompositionID] output/video.mp4
6. PUBLICAR → Subir a Instagram / TikTok
```

---

## COMANDOS ÚTILES

```bash
# Ver preview en browser
npx remotion preview

# Renderizar un video
npx remotion render MyComposition output/video.mp4

# Renderizar con lambda (más rápido)
npx remotion lambda render MyComposition

# Instalar skills de Remotion (best practices)
npx skills add remotion-dev/skills

# Renderizar en calidad alta
npx remotion render MyComposition output/video.mp4 --codec=h264 --crf=18
```

---

## REGLAS DE ANIMACIÓN (de Remotion Skills)

- Usar `spring()` para animaciones naturales (no `interpolate` puro)
- Animar 1 elemento a la vez (no todo junto)
- Duración de transición: 10-20 frames (0.3-0.6 segundos a 30fps)
- Audio: siempre sincronizar texto con narración
- Captions: usar timing exacto del audio
- FPS: 30 para social media (24 para estilo cine)
- Evitar easing lineal — siempre usar `spring` o `bezier`

---

## CHECKLIST ANTES DE ENTREGAR

- [ ] Código compila sin errores (TypeScript válido)
- [ ] Duración y FPS correctos según plataforma
- [ ] Paleta de colores corresponde al brand kit
- [ ] Animaciones fluidas (spring, no lineales)
- [ ] Assets listados claramente
- [ ] Comando de render incluido
- [ ] Preview testeado localmente
