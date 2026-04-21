# 🤖 Bot de Telegram - Polt Mobilier

## Configuración Rápida

### 1. Actualizar .env

Agregar estas líneas a `backend/.env`:

```bash
TELEGRAM_BOT_TOKEN=8311210301:AAFASEgAyb4ATBbCwuwNDkVdHyn5OmcVkKM
TELEGRAM_CHAT_ID=7644376702
TELEGRAM_ENABLED=true
```

### 2. Instalar Dependencias

```bash
cd backend
pip install aiohttp python-telegram-bot
```

### 3. Reiniciar Backend

```bash
uvicorn app.main:app --reload
```

---

## 🎯 Comandos Disponibles

### `/start`
Mensaje de bienvenida y ayuda inicial

### `/potenciales`
Muestra los últimos 10 potenciales
- Nombre
- Estado
- Valor estimado

### `/produccion`
Muestra las últimas 10 órdenes
- Orden ID
- Cliente
- Estado

### `/stats`
Estadísticas consolidadas
- Total de potenciales
- Conversion rate
- Valor total estimado
- Total de órdenes
- Ingresos totales

### `/ayuda`
Muestra todos los comandos disponibles

---

## 💬 Preguntas Naturales

El bot también responde a preguntas en lenguaje natural:

### Ejemplos:
```
"¿Cuántos potenciales sin respuesta hay?"
→ Responde con el número

"Mostrar potenciales en cotización"
→ Lista los potenciales en estado COTIZACION_ENVIADA

"¿Cuáles son las órdenes entregadas?"
→ Muestra órdenes con estado DELIVERED

"¿Cuál es el total de ingresos?"
→ Suma de todos los precios finales

"¿Cuál es la tasa de conversión?"
→ Potenciales convertidos / Total
```

---

## 📲 Usar el Bot

### En Telegram:

1. Abre el chat del bot
2. Escribe uno de los comandos arriba
3. El bot responde con los datos de la API

**Ejemplo:**
```
Tú: /stats
Bot: 
📊 ESTADÍSTICAS EN VIVO

POTENCIALES:
  Total: 15
  Aceptados: 3
  Conversion Rate: 20.0%
  Valor Estimado: ARS 750,000

PRODUCCIÓN:
  Total Órdenes: 3
  Ingresos: ARS 125,000
```

---

## 🔄 Actualizaciones en Tiempo Real

El bot **consulta en vivo** la base de datos cada vez que:
- Ejecutas un comando
- Haces una pregunta

Entonces siempre ve los datos más recientes.

---

## 📊 Notificaciones Automáticas (Futuro)

Cuando implemente notificaciones, el bot te avisará:
- ✅ Cuando un potencial se convierte a orden
- 🔔 Cuando una orden cambia de estado
- 📈 Resúmenes diarios de ventas

---

## 🧪 Testing

### Probar conexión:

```bash
curl http://localhost:8000/api/v1/telegram/send-test?message="Hola%20desde%20Polt%20Mobilier"
```

Debería recibir un mensaje en Telegram.

---

## 🔐 Seguridad

⚠️ **Tu token está seguro porque:**
- Solo está en `.env` (no en git)
- Solo el servidor lo usa
- Nadie puede acceder a él desde la API

---

## 📝 Notas

- El bot está disponible 24/7 si el backend está corriendo
- Cada respuesta es una consulta en vivo a la BD
- El bot puede manejar múltiples usuarios (si les das acceso)
- Los comandos no modifican datos (solo lectura)

---

## ⚡ Próximas Mejoras

- [ ] Agregar potenciales desde Telegram
- [ ] Actualizar estados desde Telegram
- [ ] Notificaciones automáticas
- [ ] Gráficos inline
- [ ] Exportar a PDF desde Telegram
- [ ] Búsqueda avanzada por filtros

---

## 📞 Soporte

Si el bot no responde:
1. Verificar que backend está corriendo
2. Verificar logs: `TELEGRAM_ENABLED=true`
3. Probar `/stats` (comando más simple)
4. Verificar token en `.env`

¡Listo para usar! 🚀
