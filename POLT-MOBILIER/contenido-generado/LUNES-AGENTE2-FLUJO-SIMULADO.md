# AGENTE 2: FLUJO SIMULADO — IDEA #1 PLACAR ✅

**Status**: SIMULACIÓN DEL FLUJO COMPLETO  
**Entrada**: PROMPT JSON (de AGENTE 1)  
**Salida**: MP4 completamente editado y listo

---

## 🎬 AGENTE 2 — FLUJO STEP BY STEP

### INPUT
```json
PROMPT JSON de AGENTE 1
├─ formato: "reel"
├─ duracion_segundos: 25
├─ escenas: [4 escenas con prompts de imagen]
├─ audio: {mood: "inspirador, moderno, cálido"}
└─ color_scheme: {primario, secundario, acentos}
```

---

## [STEP 1] IMAGE GENERATOR (2-3 minutos)

### Procesamiento por Escena

```
ESCENA 1: Placar desorganizado (4 seg)
├─ Prompt: "Placar desorganizado, ropa colgando caóticamente..."
├─ API: Freepik (intento 1)
│   └─ Status: ✅ Generada
│   └─ Tamaño: 1080x1920
│   └─ Archivo: image_1.jpg (320 KB)
├─ Validación: ✅ Imagen válida (JPEG, color OK)
└─ Resultado: 1 imagen lista

ESCENA 2: Placar organizado (8 seg)
├─ Prompt: "Placar piso a techo en madera clara, abierto..."
├─ API: Freepik
│   └─ Status: ✅ Generada
│   └─ Archivo: image_2.jpg (385 KB)
└─ Resultado: 1 imagen lista

ESCENA 3: Cliente feliz (7 seg)
├─ Prompt: "Cliente mujer (30s, pareja) sonriendo ampliamente..."
├─ API: Freepik
│   └─ Status: ✅ Generada
│   └─ Archivo: image_3.jpg (342 KB)
└─ Resultado: 1 imagen lista

ESCENA 4: CTA Sticker (6 seg)
├─ Tipo: Graphic (generado, no IA)
├─ Contenido: "Presupuesto sin compromiso"
├─ Color: #1A1816 fondo + #C4A882 texto
└─ Archivo: image_4.jpg (128 KB)
```

### Output Step 1
```
/agente-video-editor-output/lunes-1-placar/images/
├── image_1.jpg (Placar caos)
├── image_2.jpg (Placar organizado)
├── image_3.jpg (Cliente feliz)
└── image_4.jpg (CTA sticker)

Total: 4 imágenes ✅
Peso total: ~1.2 MB
```

---

## [STEP 2] VIDEO COMPOSITOR — Remotion React (30 segundos)

### Generación Dinámica de Componentes

```typescript
// Video.tsx (GENERADO AUTOMÁTICAMENTE)
import { Composition } from 'remotion';
import { TextOverlay } from './TextOverlay';
import { Watermark } from './Watermark';

export const PoltReel = () => (
  <Composition
    id="reel-placar"
    component={VideoContent}
    durationInFrames={750}     // 25 seg @ 30fps
    fps={30}
    width={1080}
    height={1920}
    defaultProps={{
      scenes: [
        {
          numero: 1,
          duracion: 4,
          imagen: './images/image_1.jpg',
          texto: 'El espacio no funciona',
          transicion: 'fade',
          duracion_transicion: 0.5
        },
        // ... 3 escenas más
      ],
      watermark: {
        text: 'POLT MOBILIER',
        position: 'bottom-right',
        opacity: 0.8
      }
    }}
  />
);

// VideoContent.tsx
export const VideoContent = ({ scenes, watermark }) => (
  <AbsoluteFill>
    {scenes.map((scene, i) => (
      <Scene
        key={i}
        {...scene}
        startFrame={calculateStartFrame(scene)}
        durationFrames={scene.duracion * 30}
      >
        <Img src={scene.imagen} />
        {scene.efecto && <ApplyEffect tipo={scene.efecto} />}
        <TextOverlay {...scene} />
        <Transicion tipo={scene.transicion} />
      </Scene>
    ))}
    <Watermark {...watermark} />
  </AbsoluteFill>
);
```

### Componentes Utilizados
- ✅ TextOverlay.tsx (fade in/out, posicionamiento)
- ✅ Watermark.tsx (POLT MOBILIER, color scheme)
- ✅ Transiciones: fade, slide_left, zoom_slow
- ✅ Efectos: Ken Burns (pan_derecha slow)

### Output Step 2
```
✅ Video.tsx generado correctamente
✅ VideoContent.tsx con lógica de scenes
✅ Imports de componentes configurados
✅ Timing total: 4 + 8 + 7 + 6 = 25 segundos
✅ Color scheme Polt integrado
```

---

## [STEP 3] VIDEO RENDERER — Remotion CLI (3-5 minutos)

### Ejecución

```bash
remotion render src/Video.tsx \
  --composition reel-placar \
  --codec h264 \
  --output video_raw.webm \
  --timeout 600

# Progreso:
# Frame 0 / 750 ...
# Frame 100 / 750 (13%)
# Frame 250 / 750 (33%)
# Frame 500 / 750 (67%)
# Frame 750 / 750 (100%) ✅

# Output:
# ✅ video_raw.webm (45 MB) generado en 4 min
# ✅ Duración: 25 segundos @ 30fps
# ✅ Resolución: 1080x1920
# ✅ Watermark: visible en esquina inferior derecha
# ✅ Audio: fade in/out sincronizado
# ✅ Transiciones: suaves sin glitches
```

### Output Step 3
```
/agente-video-editor-output/lunes-1-placar/
└── video_raw.webm (45 MB)
    ├─ Duración: 25.0 seg
    ├─ Resolución: 1080x1920
    ├─ Watermark: ✅ POLT MOBILIER visible
    ├─ Audio: ✅ Sincronizado (fade 0.5s c/lado)
    ├─ Transiciones: ✅ Suaves
    └─ Calidad: ✅ Alta (WebM H.264 ready)
```

---

## [STEP 4] CONVERTER — FFmpeg H.264 (1-2 minutos)

### Comando FFmpeg

```bash
ffmpeg -i video_raw.webm \
  -c:v libx264 \
  -crf 18 \
  -preset medium \
  -c:a aac \
  -b:a 128k \
  -pix_fmt yuv420p \
  -movflags +faststart \
  reel_placar_lunes_14abril.mp4

# Progress:
# Duration: 00:00:25.00, start: 0.000000, bitrate: 4500 kb/s
# frame=  750 fps= 45 q=-1.0 Lsize=N/A time=00:00:25.00 bitrate=N/A
# ✅ Conversión completada en 1.2 min
```

### Especificaciones Finales

```
✅ Codec: H.264 (máxima compatibilidad)
✅ Bitrate: 5.8 Mbps (balanceado)
✅ Frame rate: 30 fps
✅ Resolución: 1080x1920 (vertical Instagram)
✅ Audio: AAC 128 kbps (con fade in/out)
✅ Formato: MP4
✅ Flag: faststart (streaming compatible)
✅ Tamaño final: 42 MB
✅ Color space: yuv420p (máxima compatibilidad)
```

### Output Step 4
```
/agente-video-editor-output/lunes-1-placar/
├── video_raw.webm (45 MB) — Intermedio
└── reel_placar_lunes_14abril.mp4 (42 MB) ✅ FINAL
```

---

## [STEP 5] VALIDATION — ffprobe Quality Checks (<1 minuto)

### Validaciones Automáticas

```bash
ffprobe reel_placar_lunes_14abril.mp4 -show_format -show_streams

# Duración: 25.20 segundos (25.00 target ±0.5s) ✅
# Resolución: 1080x1920 ✅
# Codec: h264 (avc1) ✅
# Frame rate: 30 fps ✅
# Bitrate: 5.8 Mbps (5-8 Mbps range) ✅
# Audio tracks: 1 ✅
# Audio codec: aac ✅
# Audio bitrate: 128 kbps ✅
# File size: 42 MB (5-100 MB range OK) ✅
# Watermark: visible ✅
```

### Checklist Final

```
[✓] Todas las 4 imágenes procesadas
[✓] Componente Remotion sin errores
[✓] Video renderizado 25 segundos
[✓] MP4 exportado 1080x1920
[✓] Watermark POLT MOBILIER visible
[✓] Audio sincronizado (fade in/out)
[✓] Transiciones suaves (sin glitches)
[✓] Tamaño < 100 MB (Instagram OK)
[✓] Archivo nomenclatura descriptiva
[✓] Ready to publish = TRUE
```

---

## 📊 OUTPUT FINAL

```
📹 reel_placar_lunes_14abril.mp4
   ├─ Duración: 25.2 segundos
   ├─ Resolución: 1080x1920 (vertical)
   ├─ Tamaño: 42 MB
   ├─ Codec: H.264 MP4
   ├─ Watermark: POLT MOBILIER (inferior derecha, 80% opacidad)
   ├─ Audio: Inspirador, fade in/out 0.5s
   ├─ Texto overlay: 3 líneas con animación fade
   ├─ Transiciones: fade, slide left, zoom slow
   ├─ Color scheme: Polt integrado (#1A1816, #F5F0EB, #C4A882)
   ├─ Formato: Instagram native (faststart compatible)
   └─ ✅ LISTO PARA PUBLICAR EN INSTAGRAM
```

### JSON Output AGENTE 2

```json
{
  "status": "success",
  "file": "/agente-video-editor-output/lunes-1-placar/reel_placar_lunes_14abril.mp4",
  "duration": "25.2s",
  "resolution": "1080x1920",
  "filesize": "42 MB",
  "watermark": "POLT MOBILIER",
  "audio_status": "synchronized",
  "transitions": "3 (fade, slide_left, zoom_slow)",
  "color_scheme": "Polt brand integrated",
  "validation_checks": "10/10 PASSED",
  "ready_to_publish": true,
  "estimated_engagement": "high",
  "processing_time_seconds": 610,
  "timestamp": "2026-04-14T11:18:00Z"
}
```

---

## ⏱️ TIEMPOS TOTALES

| Paso | Tarea | Tiempo |
|------|-------|--------|
| 1 | Generate images (Freepik API × 4) | 2-3 min |
| 2 | Create Remotion component (dinámico) | <1 min |
| 3 | Render video (Remotion CLI) | 3-5 min |
| 4 | Convert MP4 (FFmpeg) | 1-2 min |
| 5 | Validate output (ffprobe) | <1 min |
| **TOTAL** | **Full workflow** | **7-12 min** |

**Comparación**: 
- CapCut manual: 30-40 minutos
- AGENTE 2 automático: 7-12 minutos
- **Ahorro: 73-80%**

---

## 📁 ARCHIVOS GENERADOS

```
/agente-video-editor-output/lunes-1-placar/
├── images/
│   ├── image_1.jpg (Placar caos)
│   ├── image_2.jpg (Placar organizado)
│   ├── image_3.jpg (Cliente feliz)
│   └── image_4.jpg (CTA sticker)
├── src/
│   ├── Video.tsx (generado dinámicamente)
│   ├── VideoContent.tsx
│   ├── TextOverlay.tsx
│   └── Watermark.tsx
├── video_raw.webm (intermedio Remotion)
├── reel_placar_lunes_14abril.mp4ᐃ (FINAL ✅)
├── agente2_report.json (validación)
└── processing_log.txt (detalles completos)
```

---

## 🚀 RESULTADO FINAL

**AGENTE 2 completó el flujo completo:**

✅ 4 imágenes generadas por IA (Freepik)  
✅ Video compuesto con Remotion (React components)  
✅ Texto overlay con fade animations  
✅ Watermark POLT integrado  
✅ Audio sincronizado con fade in/out  
✅ Transiciones suaves entre escenas  
✅ MP4 optimizado para Instagram (faststart, H.264)  
✅ Validación completa (10/10 checks)  
✅ Ready to publish = TRUE

---

## 👉 SIGUIENTE PASO

El MP4 está listo para publicar. Próxima etapa:

**AGENTE 3** (Scheduler & Publisher):
```
1. Carga MP4 a Instagram (Reels)
2. Agrega caption (de AGENTE 1)
3. Agrega hashtags (de AGENTE 1)
4. Programa publicación: 
   - HOY 6 PM
   - MAÑANA 9 AM
   - MAÑANA 9 PM
5. Retorna: Post ID + URL público
```

---

*Simulación AGENTE 2: Flujo Completo*  
*Timestamp: 2026-04-14*  
*Status: ✅ VIDEO LISTO PARA PUBLICAR*
