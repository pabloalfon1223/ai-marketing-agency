/**
 * SCRIPT DE NOTIFICACIONES — POLT MOBILIER
 * Pegar en Google Apps Script (script.google.com)
 * Configurar trigger: "ejecutar_diario" → tiempo → cada día → 9 AM
 *
 * Revisa las dos planillas y envía alertas por email cuando hay acciones pendientes
 */

// ─── CONFIGURACIÓN ────────────────────────────────────────
const EMAIL_DESTINO = "tu@email.com";  // Cambiar por tu email
const DIAS_ALERTA_ANTICIPADO = 2;       // Avisar X días antes del próximo paso
const DIAS_SIN_CONTACTO_ALERTA = 7;    // Avisar si un lead lleva X días sin contacto

// IDs de las planillas (tomados de la URL de Google Sheets)
const ID_PLANILLA_POLT = "1h6pi9MBdvTnTCKU3FIsyXkeUiczjAkAVNEzYWfh1Vu4";
// ──────────────────────────────────────────────────────────


function ejecutar_diario() {
  const alertas = [];
  const hoy = new Date();
  hoy.setHours(0, 0, 0, 0);

  try {
    const ss = SpreadsheetApp.openById(ID_PLANILLA_POLT);

    // ── HOJA POTENCIALES CLIENTES ──────────────────────────
    const hojaPotenciales = ss.getSheetByName("Potenciales") || ss.getSheets()[0];
    const datosPotenciales = hojaPotenciales.getDataRange().getValues();
    const headers = datosPotenciales[0].map(h => h.toString().toLowerCase().trim());

    // Buscar columnas clave (flexible según nombres de columna)
    const colNombre = buscarColumna(headers, ["nombre", "cliente", "name"]);
    const colProxPaso = buscarColumna(headers, ["proximo paso", "próximo paso", "next step", "fecha próximo"]);
    const colUltimoContacto = buscarColumna(headers, ["ultimo contacto", "último contacto", "last contact"]);
    const colEstado = buscarColumna(headers, ["estado", "status", "etapa"]);

    for (let i = 1; i < datosPotenciales.length; i++) {
      const fila = datosPotenciales[i];
      const nombre = fila[colNombre] || `Fila ${i + 1}`;
      const estado = colEstado >= 0 ? fila[colEstado] : "";

      // Alerta por próximo paso
      if (colProxPaso >= 0 && fila[colProxPaso] instanceof Date) {
        const fechaPaso = new Date(fila[colProxPaso]);
        fechaPaso.setHours(0, 0, 0, 0);
        const diff = Math.floor((fechaPaso - hoy) / (1000 * 60 * 60 * 24));

        if (diff === 0) {
          alertas.push(`🔴 HOY — Lead: <b>${nombre}</b> | Acción pendiente hoy (${estado})`);
        } else if (diff > 0 && diff <= DIAS_ALERTA_ANTICIPADO) {
          alertas.push(`🟡 EN ${diff} DÍA${diff > 1 ? 'S' : ''} — Lead: <b>${nombre}</b> | Próxima acción el ${formatFecha(fechaPaso)}`);
        } else if (diff < 0) {
          alertas.push(`🔴 VENCIDA — Lead: <b>${nombre}</b> | Acción vencida hace ${Math.abs(diff)} día${Math.abs(diff) > 1 ? 's' : ''}`);
        }
      }

      // Alerta por falta de contacto
      if (colUltimoContacto >= 0 && fila[colUltimoContacto] instanceof Date) {
        const ultimoContacto = new Date(fila[colUltimoContacto]);
        const diasSinContacto = Math.floor((hoy - ultimoContacto) / (1000 * 60 * 60 * 24));

        if (diasSinContacto >= DIAS_SIN_CONTACTO_ALERTA) {
          alertas.push(`⚠️ SIN CONTACTO — Lead: <b>${nombre}</b> | Hace ${diasSinContacto} días sin contacto`);
        }
      }
    }

    // ── HOJA PRODUCCIÓN (clientes activos) ────────────────
    const hojaProduccion = ss.getSheetByName("Produccion") || ss.getSheetByName("Producción") || (ss.getSheets().length > 1 ? ss.getSheets()[1] : null);

    if (hojaProduccion) {
      const datosProduccion = hojaProduccion.getDataRange().getValues();
      const headersProd = datosProduccion[0].map(h => h.toString().toLowerCase().trim());
      const colNombreProd = buscarColumna(headersProd, ["nombre", "cliente", "name"]);
      const colFechaEntrega = buscarColumna(headersProd, ["fecha entrega", "entrega", "delivery"]);
      const colEstadoProd = buscarColumna(headersProd, ["estado", "etapa", "status"]);

      for (let i = 1; i < datosProduccion.length; i++) {
        const fila = datosProduccion[i];
        const nombre = fila[colNombreProd] || `Orden ${i}`;
        const estado = colEstadoProd >= 0 ? fila[colEstadoProd] : "";

        if (colFechaEntrega >= 0 && fila[colFechaEntrega] instanceof Date) {
          const fechaEntrega = new Date(fila[colFechaEntrega]);
          fechaEntrega.setHours(0, 0, 0, 0);
          const diff = Math.floor((fechaEntrega - hoy) / (1000 * 60 * 60 * 24));

          if (diff === 0) {
            alertas.push(`🏠 ENTREGA HOY — Cliente: <b>${nombre}</b> | Estado: ${estado}`);
          } else if (diff > 0 && diff <= 3) {
            alertas.push(`📦 ENTREGA EN ${diff} DÍA${diff > 1 ? 'S' : ''} — Cliente: <b>${nombre}</b> | ${formatFecha(fechaEntrega)}`);
          } else if (diff < 0 && diff >= -3) {
            alertas.push(`⏰ ENTREGA VENCIDA — Cliente: <b>${nombre}</b> | Venció hace ${Math.abs(diff)} día${Math.abs(diff) > 1 ? 's' : ''}`);
          }
        }
      }
    }

  } catch (e) {
    alertas.push(`❌ ERROR al leer planilla: ${e.message}`);
  }

  // ── ENVIAR EMAIL ────────────────────────────────────────
  if (alertas.length > 0) {
    const cuerpo = `
      <h2 style="color:#1A1816; font-family:Arial">☀️ Resumen diario — Polt Mobilier</h2>
      <p style="color:#555; font-family:Arial">Acciones pendientes para hoy, ${formatFecha(new Date())}:</p>
      <ul style="font-family:Arial; line-height:2">
        ${alertas.map(a => `<li>${a}</li>`).join('\n')}
      </ul>
      <br>
      <p style="color:#999; font-size:12px; font-family:Arial">
        Ver planilla: <a href="https://docs.google.com/spreadsheets/d/${ID_PLANILLA_POLT}">Abrir Google Sheets</a>
      </p>
    `;

    GmailApp.sendEmail(EMAIL_DESTINO, `[Polt] ${alertas.length} acciones pendientes — ${formatFecha(new Date())}`, "", {
      htmlBody: cuerpo
    });

    Logger.log(`Email enviado con ${alertas.length} alertas`);
  } else {
    Logger.log("Sin alertas hoy.");
  }
}


// ─── HELPERS ──────────────────────────────────────────────
function buscarColumna(headers, nombres) {
  for (const nombre of nombres) {
    const idx = headers.findIndex(h => h.includes(nombre));
    if (idx >= 0) return idx;
  }
  return -1;
}

function formatFecha(fecha) {
  return fecha.toLocaleDateString('es-AR', { weekday: 'short', day: 'numeric', month: 'long' });
}


/**
 * CÓMO INSTALAR:
 * 1. Abrí tu Google Sheet de Polt Mobilier
 * 2. Extensiones → Apps Script
 * 3. Pegá todo este código
 * 4. Cambiá EMAIL_DESTINO por tu email real
 * 5. Guardá (Ctrl+S)
 * 6. Ejecutá "ejecutar_diario" una vez manualmente para probar
 * 7. Triggers (reloj) → Agregar trigger:
 *    - Función: ejecutar_diario
 *    - Fuente: Tiempo
 *    - Tipo: Día
 *    - Hora: 9:00 AM
 * 8. Listo — todos los días a las 9 AM recibís el resumen
 */
