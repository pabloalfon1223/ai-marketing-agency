# Tarea Diaria: Generar 10 Ideas de Contenido

## Instrucciones para Claude

Todos los dias a las 7:00 AM (hora Argentina), ejecuta lo siguiente:

1. Lee el archivo `backend/app/daily_content.py` para obtener el prompt template
2. Si hay clientes en la base de datos, genera contenido personalizado para cada uno
3. Si no hay clientes, genera contenido generico de marketing digital

### Genera exactamente 10 piezas de contenido LISTAS PARA PUBLICAR:

**Distribucion:**
- 3 Instagram (1 carrusel, 1 reel, 1 story)
- 2 LinkedIn (1 post, 1 articulo corto)
- 2 Twitter/X (1 hilo, 1 post)
- 1 TikTok (guion de video)
- 1 Blog (articulo completo)
- 1 Email (newsletter)

**Cada pieza debe incluir:**
- Titulo/Hook
- Texto COMPLETO listo para copiar y pegar
- Hashtags (10-15)
- Call to Action
- Horario sugerido de publicacion
- Descripcion visual detallada
- Especificaciones de formato

### Output
Guarda el resultado en `output/contenido-diario-YYYY-MM-DD.md` con formato legible.
Tambien guardalo en la base de datos del sistema via la API si el backend esta corriendo.
