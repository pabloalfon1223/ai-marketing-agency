"""
Stripe checkout endpoints for Mente Pausada
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import stripe
import os
from app.models import Purchase
from app.database import get_db
from typing import Optional

router = APIRouter()

# Initialize Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_ENDPOINT_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
DOMAIN = os.getenv("DOMAIN_URL", "http://localhost:3000")

PRODUCTS = {
    "basic": {
        "name": "Mente Pausada - Premium",
        "price": 9900,  # $99 USD in cents
        "description": "Ebook + audios + comunidad"
    },
    "plus": {
        "name": "Mente Pausada - Premium Plus",
        "price": 14900,  # $149 USD in cents
        "description": "Todo Premium + plantillas + email semanal"
    },
    "vip": {
        "name": "Mente Pausada - Premium VIP",
        "price": 19900,  # $199 USD in cents
        "description": "Todo Premium Plus + coaching 1-on-1"
    }
}


@router.post("/create-checkout")
async def create_checkout(
    tier: str,
    email: str,
    product: str = "mente-pausada-ebook",
    db: AsyncSession = Depends(get_db)
):
    """Create Stripe checkout session"""

    if tier not in PRODUCTS:
        raise HTTPException(status_code=400, detail="Invalid tier")

    try:
        product_info = PRODUCTS[tier]

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": product_info["name"],
                            "description": product_info["description"],
                        },
                        "unit_amount": product_info["price"],
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            customer_email=email,
            success_url=f"{DOMAIN}/success?session_id={{CHECKOUT_SESSION_ID}}&tier={tier}",
            cancel_url=f"{DOMAIN}/landing?tier={tier}",
            metadata={
                "email": email,
                "tier": tier,
                "product": product
            }
        )

        return {"sessionId": session.id}

    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/webhook/stripe")
async def stripe_webhook(request, db: AsyncSession = Depends(get_db)):
    """Handle Stripe webhook events"""

    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_ENDPOINT_SECRET
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle checkout.session.completed
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        email = session.get("customer_email")
        metadata = session.get("metadata", {})

        # Create purchase record
        purchase = Purchase(
            email=email,
            product=metadata.get("product", "mente-pausada-ebook"),
            amount=session["amount_total"] / 100,  # Convert from cents to dollars
            currency="USD",
            payment_method="stripe",
            payment_id=session["payment_intent"],
            status="completed",
            email_sequence_status="pending",
            source=metadata.get("source", "stripe")
        )

        db.add(purchase)
        await db.commit()

    return {"status": "ok"}


@router.get("/checkout/success")
async def checkout_success(session_id: str, tier: str, db: AsyncSession = Depends(get_db)):
    """Verify successful purchase and return download link"""

    try:
        session = stripe.checkout.Session.retrieve(session_id)

        if session.payment_status != "paid":
            raise HTTPException(status_code=400, detail="Payment not completed")

        email = session.customer_email

        # Return download/access details
        return {
            "status": "success",
            "email": email,
            "tier": tier,
            "download_link": f"/api/v1/download/mente-pausada-{tier}",
            "next_steps": [
                "Check your email for access instructions",
                "You'll receive the first email in the sequence",
                "Access the community link"
            ]
        }

    except stripe.error.InvalidRequestError:
        raise HTTPException(status_code=400, detail="Invalid session")
