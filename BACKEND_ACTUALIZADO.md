# ✅ ACTUALIZACIÓN BACKEND COMPLETADA - Polt Mobilier

## 📋 Resumen de cambios realizados

### 1. ELIMINACIÓN COMPLETA DE TELEGRAM
- ✅ Removido de `config.py`
- ✅ Removido de `main.py` (importación + router)
- ✅ Removido de `requirements.txt`
- ✅ Actualizado `.env.example`

### 2. IMPLEMENTACIÓN DE GMAIL NOTIFICATIONS
- ✅ Creado `backend/app/services/gmail_notifications.py` con:
  - Notificación cuando POTENCIAL → CLIENTE
  - Alerta cuando PRODUCCIÓN >5 días sin actualizar
  - Confirmación de cambio de estado

### 3. ACTUALIZACIÓN DE MODELOS SQLALCHEMY
- ✅ **Potencial**: campos actualizados
  - Removidos: nota, valor_estimado, orden_id_asignada, sincronizado_sheets
  - Nuevos: celular (renombrado de telefono), prioridad
  - Renombrado: fecha_contacto → fecha
  - Nuevos estados: CLIENTE, CERRAR, RECONTACTAR

- ✅ **Produccion**: estructura simplificada
  - Removidos: orden_id, fecha_inicio, fecha_entrega_est, productor, costo_real, precio_final, notas, potencial_id, sincronizado_sheets
  - Mantenidos: cliente, celular, estado, timestamps
  - Nuevo: descripcion_breve
  - Mantienen los 8 estados válidos

### 4. ESQUEMAS PYDANTIC
- ✅ `backend/app/schemas/potencial.py` con validaciones
- ✅ `backend/app/schemas/produccion.py` con validaciones
- ✅ Actualizado `__init__.py` de schemas

### 5. ENDPOINTS ACTUALIZADOS
- ✅ **potenciales.py**: CRUD + Filtros + Listado paginado
  - POST /api/v1/potenciales (crear)
  - GET /api/v1/potenciales (listar con filtros)
  - GET /api/v1/potenciales/{id} (obtener)
  - PUT /api/v1/potenciales/{id} (actualizar)
  - DELETE /api/v1/potenciales/{id} (eliminar)

- ✅ **produccion.py**: CRUD + Alertas
  - POST /api/v1/produccion (crear)
  - GET /api/v1/produccion (listar)
  - GET /api/v1/produccion/{id} (obtener)
  - PUT /api/v1/produccion/{id} (actualizar)
  - DELETE /api/v1/produccion/{id} (eliminar)
  - GET /api/v1/produccion/alertas/sin-actualizar (alertas)

- ✅ **dashboards.py**: KPIs y estadísticas
  - GET /api/v1/dashboards/potenciales/resumen
  - GET /api/v1/dashboards/potenciales/funnel
  - GET /api/v1/dashboards/potenciales/conversion-rate
  - GET /api/v1/dashboards/potenciales/por-prioridad
  - GET /api/v1/dashboards/produccion/resumen
  - GET /api/v1/dashboards/produccion/alertas
  - GET /api/v1/dashboards/resumen-general

### 6. SINCRONIZACIÓN SHEETS (sheets_sync.py)
- ✅ Cambio de trigger: QUOTE_ACCEPTED → CLIENTE
- ✅ Nuevos campos: CELULAR, PRIORIDAD, FECHA
- ✅ Eliminación de sincronización de campos innecesarios
- ✅ Integración con Gmail notifications al convertir
- ✅ Mantenimiento de todos los 8 estados de PRODUCCION

## 🔧 CONFIGURACIÓN REQUERIDA

### Para Gmail Notifications:
1. Habilitar "App Password" en tu cuenta Google (2FA requerido)
2. Agregar a `.env`:
```
GMAIL_SENDER_EMAIL=tu-email@gmail.com
GMAIL_APP_PASSWORD=tu-app-password
GMAIL_RECIPIENT_EMAIL=email-destino@gmail.com
GMAIL_ENABLED=true
```

### Para Google Sheets:
```
GOOGLE_SHEETS_ID=tu-sheet-id
GOOGLE_CREDENTIALS_PATH=./credentials/google-credentials.json
```

## 📊 FLUJOS PRINCIPALES ACTUALIZADO

### Flujo de Conversión Automática (CRÍTICO):
1. Usuario cambia estado a "CLIENTE" en Sheets o App
2. Cada 10 min: sync detecta cambio
3. Sistema crea automático en PRODUCCION con estado PLANIFICACIÓN
4. Gmail notifica la conversión
5. React actualiza tablas automáticamente

### Flujo de Alertas:
1. Registro en PRODUCCION se crea
2. Si pasa 5 días sin actualizar: alerta (rojo en React)
3. Gmail envía notificación
4. Usuario actualiza → alerta desaparece

## ✨ PRÓXIMOS PASOS

### Frontend (React):
- [ ] Actualizar componentes para nuevos campos
- [ ] Implementar visualización de alertas (>5 días)
- [ ] Responsive design para móvil
- [ ] Integración con Google Sheets en tiempo real

### AppSheets:
- [ ] Crear formulario "Nuevo Potencial"
- [ ] Crear formulario "Actualizar Producción"
- [ ] Conectar a Google Sheets

### Testing:
- [ ] Test end-to-end conversión POTENCIAL → PRODUCCION
- [ ] Verificar notificaciones Gmail
- [ ] Validar sincronización bidireccional Sheets ↔ SQLite

## 📝 NOTAS

- Todos los 8 estados de PRODUCCION se mantienen y sincronizan
- No hay campo "valor_estimado" - focus en tracking, no finanzas
- Telegram completamente removido
- Gmail es el canal de notificaciones
- Conversión CLIENTE→PRODUCCION es 100% automática
- Base de datos SQLite se usa como cache, Google Sheets como fuente de verdad

