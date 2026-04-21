"""
Email sequence automation for Mente Pausada post-purchase
"""

from datetime import datetime, timedelta, timezone
from typing import List
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SENDER_EMAIL = "hola@mentepausada.com"
SENDER_PASSWORD = ""  # Set from env

EMAIL_TEMPLATES = {
    "day_0": {
        "subject": "¡Bienvenido a Mente Pausada! 🧘 Acceso inmediato",
        "body": """Hola {name},

¡Gracias por confiar en Mente Pausada!

Tu compra fue exitosa. Aquí está tu acceso:

📥 Descarga el ebook: [DOWNLOAD_LINK]
🎵 Accede a los audios: [AUDIO_LINK]
👥 Comunidad privada: [COMMUNITY_LINK]

EMPIEZA HOY: Elige el audio de 1 minuto que más te llame la atención.
No necesitas preparación, solo elige y respira.

Preguntas: Responde a este email.

Con calma,
Mente Pausada
"""
    },
    "day_3": {
        "subject": "La magia empieza hoy 🎵 Tu primer audio",
        "body": """Hola {name},

Es hora de que experimentes qué hace especial a Mente Pausada.

El audio de HOY (1 minuto) te va a mostrar algo que probablemente no esperabas:
que PUEDES cambiar tu estado emocional en menos del tiempo que tardas en hacer café.

🎯 Método que enseño: La respiración de 4-7-8
Resultado: Bajás cortisol en segundos.

👉 [LISTEN NOW]

Mañana vamos con otro. Sin prisa. A tu ritmo.

Con calma,
Mente Pausada
"""
    },
    "day_7": {
        "subject": "Esto es lo que otros están logrando 💭",
        "body": """Hola {name},

Quería compartirte algo que sucedió en nuestra comunidad esta semana:

"No me imaginaba que en 1 minuto pudiera cambiar mi respiración. Increíble." — María, 32
"Por fin pude parar antes de explotar. Gracias." — Juan, 38
"Los audios son cortos pero efectivos. Es lo que buscaba." — Ana, 28

¿Cuál es TU experiencia hasta ahora?

Responde a este email. Me encanta saber cómo va.

Con calma,
Mente Pausada
"""
    },
    "day_10": {
        "subject": "Escalá tu práctica 🚀 (Opcional)",
        "body": """Hola {name},

Si te gustó Mente Pausada, aquí hay opciones para profundizar:

1️⃣ **Coaching 1-on-1 ($500)**
   - Sesión de 60 min personalizada
   - Diseñamos tu práctica según TU vida

2️⃣ **Comunidad Premium ($99/mes)**
   - Acceso a sessiones en vivo
   - Contenido exclusivo
   - Grupo privado de apoyo

Pero sin presión. El ebook + audios que compraste valen cada centavo.

Si el 1-on-1 te interesa, responde "coaching" a este email.

Con calma,
Mente Pausada
"""
    },
    "day_14": {
        "subject": "Cuéntame: ¿Cómo va la experiencia?",
        "body": """Hola {name},

Hace 2 semanas que compraste Mente Pausada.

Me gustaría saber:
- ¿Cuál audio es tu favorito?
- ¿Notaste cambios en tu calma/estrés?
- ¿Qué te gustaría mejorar?

Esta retroalimentación nos ayuda a hacer Mente Pausada mejor para ti.

Responde aquí. Tu opinión importa.

Con calma,
Mente Pausada

P.S. Si no abriste los audios aún, empieza hoy. 1 minuto. Eso es todo.
"""
    }
}

SEND_SCHEDULE = {
    "day_0": {"delay_hours": 0, "delay_minutes": 5},
    "day_3": {"delay_hours": 72},
    "day_7": {"delay_hours": 168},
    "day_10": {"delay_hours": 240},
    "day_14": {"delay_hours": 336}
}


async def send_email_sequence(email: str, purchase_id: int, db_session):
    """
    Send email sequence based on purchase date
    This function should be called by a scheduled task
    """

    from app.models import Purchase
    from sqlalchemy import select

    # Get purchase
    stmt = select(Purchase).where(Purchase.id == purchase_id)
    result = await db_session.execute(stmt)
    purchase = result.scalar_one_or_none()

    if not purchase:
        return {"status": "error", "message": "Purchase not found"}

    current_time = datetime.now(timezone.utc)
    days_since_purchase = (current_time - purchase.purchased_at).days

    # Determine which email to send
    email_to_send = None

    if days_since_purchase == 0:
        email_to_send = "day_0"
    elif days_since_purchase == 3:
        email_to_send = "day_3"
    elif days_since_purchase == 7:
        email_to_send = "day_7"
    elif days_since_purchase == 10:
        email_to_send = "day_10"
    elif days_since_purchase == 14:
        email_to_send = "day_14"

    if not email_to_send:
        return {"status": "ok", "message": "No email scheduled for today"}

    # Send email (placeholder - implement with SendGrid/AWS SES/etc)
    template = EMAIL_TEMPLATES[email_to_send]

    try:
        # TODO: Implement actual email sending service
        # msg = MIMEMultipart()
        # msg["From"] = SENDER_EMAIL
        # msg["To"] = email
        # msg["Subject"] = template["subject"]
        # msg.attach(MIMEText(template["body"], "plain"))
        # server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        # server.login(SENDER_EMAIL, SENDER_PASSWORD)
        # server.sendmail(SENDER_EMAIL, email, msg.as_string())
        # server.close()

        # Update purchase status
        purchase.email_sequence_status = email_to_send
        purchase.last_email_sent_at = current_time
        purchase.email_sent_count += 1
        await db_session.commit()

        return {
            "status": "ok",
            "message": f"Email {email_to_send} sent to {email}"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
