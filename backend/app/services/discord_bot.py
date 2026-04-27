import discord
from discord import app_commands
from discord.ext import commands, tasks
import aiohttp
import asyncio
import logging
import os
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

BACKEND_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")

# IDs de canales (se cargan desde .env)
CHANNEL_IDS = {
    "cerebro":       int(os.getenv("DISCORD_CEREBRO_CHANNEL", "0")),
    "mente_pausada": int(os.getenv("DISCORD_MENTE_PAUSADA_CHANNEL", "0")),
    "polt_mobilier": int(os.getenv("DISCORD_POLT_MOBILIER_CHANNEL", "0")),
    "sistema_jefe":  int(os.getenv("DISCORD_SISTEMA_JEFE_CHANNEL", "0")),
    "pruebas":       int(os.getenv("DISCORD_PRUEBAS_CHANNEL", "0")),
}

EMOJIS = {
    "ok":      "✅",
    "error":   "❌",
    "warn":    "⚠️",
    "brain":   "🧠",
    "pause":   "🧘",
    "chair":   "🪑",
    "gear":    "⚙️",
    "money":   "💰",
    "content": "📝",
    "rocket":  "🚀",
    "clock":   "🕐",
    "fire":    "🔥",
}


class AIMarketingBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        logger.info("✅ Discord slash commands sincronizados")

    async def on_ready(self):
        logger.info(f"✅ Discord Bot conectado como {self.user}")
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="el sistema IA 👁️"
            )
        )
        await self.send_to_channel(
            "sistema_jefe",
            f"{EMOJIS['rocket']} **AI Marketing Agency online**\n"
            f"Bot activo | {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
            f"Usá `/jefe-status` para ver el estado del sistema."
        )

    # ─── Método helper para enviar mensajes a canales ─────────────────────────

    async def send_to_channel(self, canal: str, mensaje: str, embed: discord.Embed = None):
        channel_id = CHANNEL_IDS.get(canal, 0)
        if not channel_id:
            logger.warning(f"Canal '{canal}' no configurado en .env")
            return
        channel = self.get_channel(channel_id)
        if channel:
            await channel.send(content=mensaje, embed=embed)
        else:
            logger.warning(f"No se encontró el canal {canal} (ID: {channel_id})")

    # ─── Helper para llamar al backend FastAPI ────────────────────────────────

    async def call_api(self, method: str, endpoint: str, data: dict = None) -> dict:
        url = f"{BACKEND_URL}/api/v1{endpoint}"
        try:
            async with aiohttp.ClientSession() as session:
                if method == "GET":
                    async with session.get(url) as r:
                        return await r.json()
                elif method == "POST":
                    async with session.post(url, json=data) as r:
                        return await r.json()
        except Exception as e:
            logger.error(f"Error llamando API {endpoint}: {e}")
            return {"error": str(e)}


bot = AIMarketingBot()


# ═══════════════════════════════════════════════════════════════════════════════
# SLASH COMMANDS
# ═══════════════════════════════════════════════════════════════════════════════

@bot.tree.command(name="jefe-status", description="Ver el estado completo del sistema")
async def jefe_status(interaction: discord.Interaction):
    await interaction.response.defer()

    # Obtener estado real del backend
    health = await bot.call_api("GET", "/health")
    clients = await bot.call_api("GET", "/clients")
    projects = await bot.call_api("GET", "/projects")
    content_list = await bot.call_api("GET", "/content")

    n_clients  = len(clients) if isinstance(clients, list) else "?"
    n_projects = len(projects) if isinstance(projects, list) else "?"
    n_content  = len(content_list) if isinstance(content_list, list) else "?"
    api_ok     = "error" not in health

    embed = discord.Embed(
        title="⚙️ Estado del Sistema — AI Marketing Agency",
        color=discord.Color.green() if api_ok else discord.Color.red(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(
        name="🔧 Backend API",
        value=f"{EMOJIS['ok']} Online" if api_ok else f"{EMOJIS['error']} Offline",
        inline=True
    )
    embed.add_field(name="👥 Clientes", value=str(n_clients), inline=True)
    embed.add_field(name="📁 Proyectos", value=str(n_projects), inline=True)
    embed.add_field(name="📝 Contenidos", value=str(n_content), inline=True)
    embed.add_field(
        name="🧠 CEREBRO",
        value=f"{EMOJIS['ok']} Activo — Scanner de oportunidades",
        inline=False
    )
    embed.add_field(
        name="🧘 MENTE PAUSADA",
        value=f"{EMOJIS['ok']} Activo — Pipeline de contenido",
        inline=False
    )
    embed.add_field(
        name="🪑 POLT MOBILIER",
        value=f"{EMOJIS['ok']} Activo — Gestión de cliente",
        inline=False
    )
    embed.set_footer(text="Usá /jefe-run, /jefe-dispatch, /jefe-review para más acciones")

    await interaction.followup.send(embed=embed)


# ─────────────────────────────────────────────────────────────────────────────

@bot.tree.command(name="jefe-run", description="Ejecutar un workflow de una marca")
@app_commands.describe(
    workflow="Workflow a ejecutar",
    marca="Marca objetivo"
)
@app_commands.choices(workflow=[
    app_commands.Choice(name="Generar contenido diario", value="daily_content"),
    app_commands.Choice(name="Analytics del día",        value="daily_analytics"),
    app_commands.Choice(name="Scanner de oportunidades", value="cerebro_scan"),
    app_commands.Choice(name="Digest semanal",           value="weekly_digest"),
])
@app_commands.choices(marca=[
    app_commands.Choice(name="Mente Pausada",  value="mente_pausada"),
    app_commands.Choice(name="Polt Mobilier",  value="polt_mobilier"),
    app_commands.Choice(name="CEREBRO",        value="cerebro"),
    app_commands.Choice(name="Todas",          value="all"),
])
async def jefe_run(
    interaction: discord.Interaction,
    workflow: str,
    marca: str = "all"
):
    await interaction.response.defer()

    workflows_labels = {
        "daily_content":   f"{EMOJIS['content']} Generación de contenido diario",
        "daily_analytics": f"📊 Analytics del día",
        "cerebro_scan":    f"{EMOJIS['brain']} Scanner de oportunidades CEREBRO",
        "weekly_digest":   f"📋 Digest semanal",
    }
    label = workflows_labels.get(workflow, workflow)

    embed = discord.Embed(
        title=f"{EMOJIS['rocket']} Ejecutando workflow",
        description=f"**{label}**\nMarca: `{marca}`",
        color=discord.Color.blue(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="Estado", value=f"{EMOJIS['clock']} En progreso...", inline=False)
    msg = await interaction.followup.send(embed=embed)

    # Llamar al backend según el workflow
    result = {}
    if workflow == "daily_content":
        result = await bot.call_api("POST", "/agents/run", {
            "agent": "content_agent",
            "brand": marca,
            "task": "generate_daily_content"
        })
    elif workflow == "daily_analytics":
        result = await bot.call_api("POST", "/agents/run", {
            "agent": "analytics_agent",
            "brand": marca,
            "task": "daily_report"
        })
    elif workflow == "cerebro_scan":
        result = await bot.call_api("POST", "/agents/run", {
            "agent": "strategy",
            "brand": "cerebro",
            "task": "scan_opportunities"
        })
    elif workflow == "weekly_digest":
        result = await bot.call_api("POST", "/agents/run", {
            "agent": "orchestrator",
            "brand": marca,
            "task": "weekly_digest"
        })

    ok = "error" not in result
    embed.color = discord.Color.green() if ok else discord.Color.red()
    embed.set_field_at(
        0,
        name="Estado",
        value=f"{EMOJIS['ok']} Completado" if ok else f"{EMOJIS['error']} Error: {result.get('error', '?')}",
        inline=False
    )
    if ok and result:
        output = str(result.get("result", result))[:800]
        embed.add_field(name="Output", value=f"```{output}```", inline=False)

    await msg.edit(embed=embed)

    # Notificar en canal correspondiente
    canal_map = {
        "mente_pausada": "mente_pausada",
        "polt_mobilier": "polt_mobilier",
        "cerebro":       "cerebro",
        "all":           "sistema_jefe",
    }
    canal = canal_map.get(marca, "sistema_jefe")
    if ok:
        await bot.send_to_channel(
            canal,
            f"{EMOJIS['ok']} **{label}** completado por {interaction.user.mention}"
        )


# ─────────────────────────────────────────────────────────────────────────────

@bot.tree.command(name="jefe-dispatch", description="Despachar una tarea a un agente específico")
@app_commands.describe(
    agente="Agente a usar",
    tarea="Descripción de la tarea"
)
@app_commands.choices(agente=[
    app_commands.Choice(name="🧠 Cerebro Scanner",       value="cerebro_scanner"),
    app_commands.Choice(name="📝 Content Director MP",   value="content_agent"),
    app_commands.Choice(name="📊 Daily Analytics",       value="analytics_agent"),
    app_commands.Choice(name="🪑 Polt Contenido",        value="polt_contenido"),
    app_commands.Choice(name="🔄 Self Improver",         value="self_improver"),
    app_commands.Choice(name="🎯 Strategy",              value="strategy"),
    app_commands.Choice(name="📣 Social Media",          value="social_media"),
    app_commands.Choice(name="✍️  Copywriter",            value="branding"),
])
async def jefe_dispatch(
    interaction: discord.Interaction,
    agente: str,
    tarea: str
):
    await interaction.response.defer()

    embed = discord.Embed(
        title=f"{EMOJIS['gear']} Despachando tarea al agente `{agente}`",
        description=f"**Tarea:** {tarea}",
        color=discord.Color.orange(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="Estado", value=f"{EMOJIS['clock']} Procesando...", inline=False)
    msg = await interaction.followup.send(embed=embed)

    result = await bot.call_api("POST", "/agents/run", {
        "agent": agente,
        "task": tarea,
        "context": f"Despachado por {interaction.user.name} vía Discord"
    })

    ok = "error" not in result
    output = str(result.get("result", result.get("error", result)))[:1000]

    embed.color = discord.Color.green() if ok else discord.Color.red()
    embed.set_field_at(
        0,
        name="Estado",
        value=f"{EMOJIS['ok']} Completado" if ok else f"{EMOJIS['error']} Error",
        inline=False
    )
    embed.add_field(
        name="Resultado",
        value=f"```{output}```" if output else "Sin output",
        inline=False
    )
    await msg.edit(embed=embed)


# ─────────────────────────────────────────────────────────────────────────────

@bot.tree.command(name="jefe-review", description="Revisar los últimos contenidos generados")
@app_commands.describe(
    cantidad="Cuántos items revisar",
    marca="Filtrar por marca"
)
@app_commands.choices(marca=[
    app_commands.Choice(name="Todas",         value="all"),
    app_commands.Choice(name="Mente Pausada", value="mente_pausada"),
    app_commands.Choice(name="Polt Mobilier", value="polt_mobilier"),
    app_commands.Choice(name="CEREBRO",       value="cerebro"),
])
async def jefe_review(
    interaction: discord.Interaction,
    cantidad: int = 5,
    marca: str = "all"
):
    await interaction.response.defer()

    content_list = await bot.call_api("GET", "/content")

    if "error" in content_list:
        await interaction.followup.send(f"{EMOJIS['error']} Error al obtener contenidos: {content_list['error']}")
        return

    items = content_list if isinstance(content_list, list) else []
    if marca != "all":
        items = [c for c in items if marca in str(c.get("brand", "")).lower()]
    items = items[:cantidad]

    if not items:
        await interaction.followup.send(f"{EMOJIS['warn']} No hay contenidos para revisar.")
        return

    embed = discord.Embed(
        title=f"📋 Últimos {len(items)} contenidos — {marca}",
        color=discord.Color.purple(),
        timestamp=datetime.utcnow()
    )
    for item in items:
        title   = item.get("title", "Sin título")[:50]
        status  = item.get("status", "?")
        brand   = item.get("brand", "?")
        created = item.get("created_at", "")[:10] if item.get("created_at") else "?"
        status_emoji = EMOJIS["ok"] if status == "published" else EMOJIS["clock"]
        embed.add_field(
            name=f"{status_emoji} {title}",
            value=f"Marca: `{brand}` | Estado: `{status}` | Fecha: {created}",
            inline=False
        )

    await interaction.followup.send(embed=embed)


# ─────────────────────────────────────────────────────────────────────────────

@bot.tree.command(name="jefe-build", description="Construir un nuevo componente del sistema")
@app_commands.describe(
    componente="Qué querés construir",
    descripcion="Descripción detallada de lo que necesitás"
)
@app_commands.choices(componente=[
    app_commands.Choice(name="📧 Secuencia de email",   value="email_sequence"),
    app_commands.Choice(name="📱 Post redes sociales",  value="social_post"),
    app_commands.Choice(name="🎬 Guion de video/reel",  value="video_script"),
    app_commands.Choice(name="📊 Estrategia de ads",    value="ads_strategy"),
    app_commands.Choice(name="🔍 Análisis SEO",         value="seo_analysis"),
    app_commands.Choice(name="💡 Ideas de contenido",   value="content_ideas"),
    app_commands.Choice(name="📋 Plan de contenido",    value="content_plan"),
])
async def jefe_build(
    interaction: discord.Interaction,
    componente: str,
    descripcion: str
):
    await interaction.response.defer()

    agent_map = {
        "email_sequence": "email_marketing",
        "social_post":    "social_media",
        "video_script":   "content_agent",
        "ads_strategy":   "ads_strategy",
        "seo_analysis":   "seo",
        "content_ideas":  "content_agent",
        "content_plan":   "orchestrator",
    }
    agente = agent_map.get(componente, "strategy")

    embed = discord.Embed(
        title=f"{EMOJIS['fire']} Construyendo: `{componente}`",
        description=f"**Brief:** {descripcion[:300]}",
        color=discord.Color.gold(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="Agente", value=f"`{agente}`", inline=True)
    embed.add_field(name="Estado", value=f"{EMOJIS['clock']} Generando...", inline=True)
    msg = await interaction.followup.send(embed=embed)

    result = await bot.call_api("POST", "/agents/run", {
        "agent": agente,
        "task": descripcion,
        "type": componente,
        "context": f"Build pedido por {interaction.user.name} vía Discord"
    })

    ok = "error" not in result
    output = str(result.get("result", result.get("error", "")))

    embed.color = discord.Color.green() if ok else discord.Color.red()
    embed.set_field_at(1, name="Estado", value=f"{EMOJIS['ok']} Listo" if ok else f"{EMOJIS['error']} Error", inline=True)

    # Si el output es largo, partirlo en chunks de 1000 chars
    if output:
        chunks = [output[i:i+1000] for i in range(0, min(len(output), 3000), 1000)]
        for i, chunk in enumerate(chunks):
            embed.add_field(
                name=f"Resultado {'(cont.)' if i > 0 else ''}",
                value=f"```{chunk}```",
                inline=False
            )
    await msg.edit(embed=embed)


# ─────────────────────────────────────────────────────────────────────────────

@bot.tree.command(name="ask", description="Hacerle una pregunta directa al sistema de IA")
@app_commands.describe(pregunta="Tu pregunta o instrucción")
async def ask(interaction: discord.Interaction, pregunta: str):
    await interaction.response.defer()

    result = await bot.call_api("POST", "/agents/run", {
        "agent": "strategy",
        "task": pregunta,
        "context": f"Pregunta directa de {interaction.user.name} vía Discord"
    })

    ok = "error" not in result
    output = str(result.get("result", result.get("error", "Sin respuesta")))[:3000]

    embed = discord.Embed(
        title=f"💬 Respuesta del sistema",
        description=f"**Pregunta:** {pregunta[:200]}",
        color=discord.Color.blue() if ok else discord.Color.red(),
        timestamp=datetime.utcnow()
    )
    # Partir en chunks si es largo
    chunks = [output[i:i+1000] for i in range(0, len(output), 1000)]
    for i, chunk in enumerate(chunks[:3]):
        embed.add_field(
            name="Respuesta" if i == 0 else "(continúa)",
            value=chunk,
            inline=False
        )
    await interaction.followup.send(embed=embed)


# ─────────────────────────────────────────────────────────────────────────────

@bot.tree.command(name="crm", description="Ver el estado del CRM (clientes y pipeline)")
@app_commands.describe(vista="Qué querés ver")
@app_commands.choices(vista=[
    app_commands.Choice(name="Clientes activos",    value="clients"),
    app_commands.Choice(name="Pipeline de ventas",  value="pipeline"),
    app_commands.Choice(name="Nuevos potenciales",  value="potenciales"),
    app_commands.Choice(name="Producción activa",   value="produccion"),
])
async def crm(interaction: discord.Interaction, vista: str = "clients"):
    await interaction.response.defer()

    endpoint_map = {
        "clients":     "/clients",
        "pipeline":    "/projects",
        "potenciales": "/potenciales",
        "produccion":  "/produccion",
    }
    data = await bot.call_api("GET", endpoint_map.get(vista, "/clients"))

    items = data if isinstance(data, list) else []

    embed = discord.Embed(
        title=f"📊 CRM — {vista.replace('_', ' ').title()}",
        description=f"Total: **{len(items)}** registros",
        color=discord.Color.teal(),
        timestamp=datetime.utcnow()
    )
    for item in items[:10]:
        name   = item.get("name") or item.get("title") or item.get("nombre") or str(item.get("id", "?"))
        status = item.get("status") or item.get("estado") or "activo"
        embed.add_field(name=name[:50], value=f"`{status}`", inline=True)

    if len(items) > 10:
        embed.set_footer(text=f"Mostrando 10 de {len(items)}. Abrí el CRM para ver todos.")

    await interaction.followup.send(embed=embed)


# ═══════════════════════════════════════════════════════════════════════════════
# NOTIFICACIONES PROACTIVAS (funciones llamadas desde el backend)
# ═══════════════════════════════════════════════════════════════════════════════

async def notify_new_content(brand: str, title: str, preview: str = ""):
    canal_map = {
        "mente_pausada": "mente_pausada",
        "polt_mobilier": "polt_mobilier",
        "cerebro":       "cerebro",
    }
    canal = canal_map.get(brand, "sistema_jefe")
    emoji = {"mente_pausada": "🧘", "polt_mobilier": "🪑", "cerebro": "🧠"}.get(brand, "📝")
    await bot.send_to_channel(
        canal,
        f"{emoji} **Nuevo contenido generado**\n"
        f"**Título:** {title}\n"
        f"{preview[:200] + '...' if len(preview) > 200 else preview}"
    )


async def notify_new_lead(nombre: str, fuente: str, valor: str = ""):
    await bot.send_to_channel(
        "polt_mobilier",
        f"{EMOJIS['money']} **Nuevo potencial cliente**\n"
        f"**Nombre:** {nombre}\n"
        f"**Fuente:** {fuente}\n"
        f"{'**Valor:** ' + valor if valor else ''}"
    )


async def notify_opportunity(titulo: str, descripcion: str, potencial_usd: str = ""):
    await bot.send_to_channel(
        "cerebro",
        f"{EMOJIS['fire']} **Oportunidad detectada por CEREBRO**\n"
        f"**{titulo}**\n"
        f"{descripcion[:300]}\n"
        f"{'💵 Potencial: ' + potencial_usd if potencial_usd else ''}"
    )


async def notify_error(servicio: str, error: str):
    await bot.send_to_channel(
        "sistema_jefe",
        f"{EMOJIS['error']} **Error en {servicio}**\n```{error[:500]}```"
    )


async def notify_daily_digest(resumen: str):
    await bot.send_to_channel(
        "sistema_jefe",
        f"📋 **Digest diario — {datetime.now().strftime('%d/%m/%Y')}**\n{resumen[:1500]}"
    )


# ═══════════════════════════════════════════════════════════════════════════════
# RUNNER — para iniciar el bot como tarea asyncio
# ═══════════════════════════════════════════════════════════════════════════════

async def run_discord_bot():
    token = os.getenv("DISCORD_BOT_TOKEN", "")
    if not token:
        logger.warning("⚠️ DISCORD_BOT_TOKEN no configurado — bot Discord desactivado")
        return
    try:
        await bot.start(token)
    except Exception as e:
        logger.error(f"Error iniciando Discord bot: {e}")


def start_bot_background():
    """Inicia el bot en el event loop de asyncio como background task."""
    loop = asyncio.get_event_loop()
    loop.create_task(run_discord_bot())
    logger.info("✅ Discord bot iniciado en background")
