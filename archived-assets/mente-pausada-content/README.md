# Contenido Mente Pausada - Histórico

**Fecha de centralización:** 2026-04-18  
**Origen:** Sesiones de Cowork anteriores  
**Status:** Archive + Referencia

---

## 📄 Archivos Disponibles

| Archivo | Descripción | Tipo | Contenido |
|---------|-------------|------|-----------|
| `contenido-mente-pausada-6piezas.docx` | 6 piezas de contenido generadas | DOCX | Textos de posts, historias, copy |
| `mente-pausada-blueprint.docx` | Blueprint del producto/servicio | DOCX | Estrategia, positioning, oferta |
| `tabla-contenido-mente-pausada.xlsx` | Tabla con calendarios y estructura | XLSX | Fechas, formatos, categorías |

---

## 🎯 Cómo Usar

### Para generar NUEVO contenido:
1. Lee `mente-pausada-blueprint.docx` para entender la estrategia
2. Usa `tabla-contenido-mente-pausada.xlsx` como referencia de estructura
3. Ejecuta la tarea automática: **`daily-content-ideas` (7 AM)**

### Para entender el producto:
→ Lee `mente-pausada-blueprint.docx`

### Para entender el calendario/estructura:
→ Abre `tabla-contenido-mente-pausada.xlsx`

### Para ver ejemplos de contenido:
→ Abre `contenido-mente-pausada-6piezas.docx`

---

## 🔄 Contenido AUTOMATIZADO

La tarea diaria `daily-content-ideas` (7 AM) genera 10 piezas nuevas cada día.  
Los archivos aquí son de sesiones anteriores - son referencia histórica.

**Para nuevo contenido:**
- Espera el reporte automático de 7 AM
- O ejecuta skill `generador-mente-pausada` manualmente

---

## 📊 Integración Actual

```
Contenido generado → Google Sheets (lectura/escritura)
                 → Buffer (posts automáticos)
                 → Dashboard Mente Pausada (analytics)
```

---

## 🔗 Referencias

- **Perfil del Proyecto:** `backend/app/brands/mente_pausada.py`
- **Proceso Completo:** `PROCESS_MENTE_PAUSADA.md`
- **Tarea Automática:** `.claude/scheduled-tasks/daily-content-ideas/`

---

*Último actualizado: 2026-04-18*
