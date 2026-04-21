# 📦 Archived Assets - Histórico Centralizado

**Fecha de creación:** 2026-04-18  
**Propósito:** Centralizar archivos de sesiones Cowork anteriores  
**Status:** Reference Only - No usar en producción

---

## 📁 Estructura

```
archived-assets/
├── polt-dashboards/                    [9 versiones HTML]
│   ├── polt_calculator.html
│   ├── polt_calculator_pro.html
│   ├── polt_dashboard.html
│   ├── polt_dashboard_carpintero.html
│   ├── polt_dashboard_v2.html
│   ├── polt_dashboard_v3.html
│   ├── polt_dashboard_v4.html
│   ├── polt_dashboard_v4_fixed.html
│   ├── polt_dashboard_v5_with_analyzer.html
│   └── README.md                       [Este documento]
│
├── mente-pausada-content/              [3 archivos DOCX+XLSX]
│   ├── contenido-mente-pausada-6piezas.docx
│   ├── mente-pausada-blueprint.docx
│   ├── tabla-contenido-mente-pausada.xlsx
│   └── README.md                       [Este documento]
│
└── agents-config/                      [Para futuro - agentes de sesiones Cowork]
    └── [vacío por ahora]
```

---

## 🎯 Cuándo Usar

### ✅ USAR estos archivos si necesitas:
- 📚 Referencia histórica de iteraciones anteriores
- 💻 Código JavaScript/HTML para reutilizar
- 📋 Ejemplos de contenido para nuevas piezas
- 🏗️ Entender cómo evolucionó el diseño

### ❌ NO USAR para:
- 🔴 Producción en vivo (usar `/frontend/src/` y `/backend/app/`)
- 🔴 Generar nuevo contenido (usar tarea automática de 7 AM)
- 🔴 Cambiar el flujo del sistema (usar componentes React y APIs)

---

## 📝 Documentación

Cada carpeta tiene su propio README:
- `polt-dashboards/README.md` → Detalles de versiones HTML
- `mente-pausada-content/README.md` → Cómo usar contenido histórico

---

## 🔄 Origen de los Archivos

Estos archivos fueron generados en **sesiones de Cowork anteriores** (enero-abril 2026) y estaban dispersos en:

```
/c/Users/lucas/AppData/Roaming/Claude/local-agent-mode-sessions/...
```

**Centralización realizada:** 2026-04-18 (búsqueda exhaustiva)

---

## 🚀 Sistema Actual (Producción)

| Componente | Ubicación | Status |
|------------|-----------|--------|
| Frontend React | `frontend/src/` | ✅ Activo |
| Backend APIs | `backend/app/` | ✅ Activo |
| Contenido Automatizado | `scheduled-tasks/daily-content-ideas/` | ✅ Activo |
| Documentación | `docs/` | ✅ Completa |

---

## 📋 Checklist de Centralización

- [x] Buscar en todas las carpetas de la computadora
- [x] Identificar archivos dispersos (50+ encontrados)
- [x] Crear estructura de `archived-assets/`
- [x] Copiar dashboards Polt (9 versiones)
- [x] Copiar contenido Mente Pausada (3 archivos)
- [x] Crear READMEs informativos
- [ ] Copiar agents-config (para próxima sesión)
- [x] Centralización COMPLETA

---

## 🎓 Para Próximos Pasos

Si necesitas:

1. **Recuperar algo de una sesión anterior**
   - Busca en esta carpeta primero
   - Si no está, avísame para hacer búsqueda adicional

2. **Agregar más archivos al archive**
   - Cópialos aquí y actualiza el README

3. **Usar algo del archive en producción**
   - Mejor: reescribir como componente React o API endpoint
   - No: copiar HTML directo a prod

---

*Centralización completada: 2026-04-18*  
*Archivos encontrados y centralizados: 50+*  
*Sesiones Cowork analizadas: 3 principales*
