from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from app.models import Purchase
from app.database import get_db

router = APIRouter()


@router.post("/purchases")
async def create_purchase(
    email: str,
    product: str,
    amount: float,
    currency: str = "USD",
    payment_method: str = None,
    payment_id: str = None,
    source: str = None,
    db: AsyncSession = Depends(get_db)
):
    """Create a new purchase for Mente Pausada ebook"""
    try:
        purchase = Purchase(
            email=email,
            product=product,
            amount=amount,
            currency=currency,
            payment_method=payment_method,
            payment_id=payment_id,
            source=source,
            status="completed",
            email_sequence_status="pending"
        )
        db.add(purchase)
        await db.commit()
        await db.refresh(purchase)
        return {"status": "ok", "purchase_id": purchase.id, "email": email}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/purchases/{email}")
async def get_purchase(email: str, db: AsyncSession = Depends(get_db)):
    """Get purchase by email"""
    stmt = select(Purchase).where(Purchase.email == email)
    result = await db.execute(stmt)
    purchase = result.scalar_one_or_none()

    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")

    return {
        "id": purchase.id,
        "email": purchase.email,
        "product": purchase.product,
        "amount": purchase.amount,
        "status": purchase.status,
        "email_sequence_status": purchase.email_sequence_status,
        "purchased_at": purchase.purchased_at
    }


@router.put("/purchases/{purchase_id}/email-status")
async def update_email_status(
    purchase_id: int,
    email_sequence_status: str,
    db: AsyncSession = Depends(get_db)
):
    """Update email sequence status for a purchase"""
    stmt = select(Purchase).where(Purchase.id == purchase_id)
    result = await db.execute(stmt)
    purchase = result.scalar_one_or_none()

    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")

    purchase.email_sequence_status = email_sequence_status
    purchase.last_email_sent_at = datetime.now(timezone.utc)
    purchase.email_sent_count += 1
    purchase.updated_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(purchase)
    return {"status": "ok", "email_sequence_status": purchase.email_sequence_status}


@router.get("/purchases/analytics/summary")
async def get_purchases_summary(db: AsyncSession = Depends(get_db)):
    """Get summary analytics for Mente Pausada sales"""
    result = await db.execute(select(Purchase))
    purchases = result.scalars().all()

    if not purchases:
        return {
            "total_purchases": 0,
            "total_revenue": 0,
            "average_price": 0,
            "last_purchase": None
        }

    total_revenue = sum(p.amount for p in purchases)
    return {
        "total_purchases": len(purchases),
        "total_revenue": total_revenue,
        "average_price": total_revenue / len(purchases),
        "last_purchase": max(p.purchased_at for p in purchases)
    }
