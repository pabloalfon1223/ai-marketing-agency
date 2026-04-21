from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from datetime import datetime, timezone
from app.models import Order
from app.database import get_db
from typing import Optional

router = APIRouter()


@router.post("/orders")
async def create_order(
    order_number: str,
    customer_name: str,
    product_type: str,
    product_description: str,
    customer_email: Optional[str] = None,
    customer_phone: Optional[str] = None,
    customer_whatsapp: Optional[str] = None,
    estimated_cost: Optional[float] = None,
    db: AsyncSession = Depends(get_db)
):
    """Create new order for Polt Mobilier"""
    try:
        order = Order(
            order_number=order_number,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            customer_whatsapp=customer_whatsapp,
            product_type=product_type,
            product_description=product_description,
            estimated_cost=estimated_cost,
            order_status="quote_sent"
        )
        db.add(order)
        await db.commit()
        await db.refresh(order)
        return {"status": "ok", "order_id": order.id, "order_number": order_number}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/orders/{order_id}")
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    """Get order by ID"""
    stmt = select(Order).where(Order.id == order_id)
    result = await db.execute(stmt)
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return {
        "id": order.id,
        "order_number": order.order_number,
        "customer_name": order.customer_name,
        "product_type": order.product_type,
        "order_status": order.order_status,
        "estimated_cost": order.estimated_cost,
        "final_cost": order.final_cost,
        "estimated_delivery_date": order.estimated_delivery_date,
        "created_at": order.created_at
    }


@router.put("/orders/{order_id}/status")
async def update_order_status(
    order_id: int,
    order_status: str,
    final_cost: Optional[float] = None,
    estimated_delivery_date: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Update order status and details"""
    stmt = select(Order).where(Order.id == order_id)
    result = await db.execute(stmt)
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.order_status = order_status
    if final_cost:
        order.final_cost = final_cost
    if estimated_delivery_date:
        order.estimated_delivery_date = datetime.fromisoformat(estimated_delivery_date)
    order.updated_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(order)
    return {"status": "ok", "order_status": order.order_status}


@router.get("/orders/list/active")
async def get_active_orders(db: AsyncSession = Depends(get_db)):
    """Get all active orders (in production or awaiting)"""
    stmt = select(Order).where(
        Order.order_status.in_(["quote_accepted", "in_production", "completed"])
    ).order_by(desc(Order.created_at))
    result = await db.execute(stmt)
    orders = result.scalars().all()

    return [
        {
            "id": o.id,
            "order_number": o.order_number,
            "customer_name": o.customer_name,
            "product_type": o.product_type,
            "order_status": o.order_status,
            "estimated_delivery_date": o.estimated_delivery_date,
            "days_until_delivery": (o.estimated_delivery_date - datetime.now(timezone.utc)).days if o.estimated_delivery_date else None
        }
        for o in orders
    ]


@router.get("/orders/analytics/summary")
async def get_orders_summary(db: AsyncSession = Depends(get_db)):
    """Get summary analytics for Polt orders"""
    result = await db.execute(select(Order))
    orders = result.scalars().all()

    if not orders:
        return {
            "total_orders": 0,
            "total_revenue": 0,
            "average_order_value": 0,
            "active_orders": 0
        }

    total_revenue = sum(o.final_cost or o.estimated_cost or 0 for o in orders)
    active = len([o for o in orders if o.order_status in ["quote_accepted", "in_production"]])

    return {
        "total_orders": len(orders),
        "total_revenue": total_revenue,
        "average_order_value": total_revenue / len(orders) if orders else 0,
        "active_orders": active
    }
