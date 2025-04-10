from models.purchase import Purchase
from database.db import get_db_connection
import logging

logging.basicConfig(level=logging.DEBUG)

class PurchaseService:
    @staticmethod
    async def create_purchase(data: dict) -> Purchase:
        try:
            purchase = Purchase(
                name=data["name"],
                amount=data["amount"],
                commission_rate=data["commission_rate"]
            )

            async with await get_db_connection() as db:
                await db.execute(
                    """
                    INSERT INTO purchases (id, name, amount, commission_rate, commission)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        purchase.id,
                        purchase.name,
                        purchase.amount,
                        purchase.commission_rate,
                        purchase.commission,
                    ),
                )
                await db.commit()

            logging.debug(f"Compra creada: {purchase.to_dict()}")
            return purchase

        except Exception as e:
            logging.error(f"Error al crear la compra: {e}")
            raise

    @staticmethod
    async def get_purchase(purchase_id: str) -> Purchase:
        try:
            async with await get_db_connection() as db:
                cursor = await db.execute(
                    "SELECT id, name, amount, commission_rate, commission FROM purchases WHERE id = ?",
                    (purchase_id,),
                )
                row = await cursor.fetchone()

                if row:
                    purchase = Purchase(
                        id=row[0],
                        name=row[1],
                        amount=row[2],
                        commission_rate=row[3],
                    )
                    logging.debug(f"Compra obtenida: {purchase.to_dict()}")
                    return purchase
                else:
                    logging.warning(f"No se encontró la compra con ID: {purchase_id}")
                    return None

        except Exception as e:
            logging.error(f"Error al obtener la compra: {e}")
            raise

    @staticmethod
    async def list_purchases() -> list:
        try:
            async with await get_db_connection() as db:
                cursor = await db.execute(
                    "SELECT id, name, amount, commission_rate, commission FROM purchases"
                )
                rows = await cursor.fetchall()

                purchases = [
                    Purchase(
                        id=row[0],
                        name=row[1],
                        amount=row[2],
                        commission_rate=row[3],
                    )
                    for row in rows
                ]

                logging.debug(f"Lista de compras obtenida: {[p.to_dict() for p in purchases]}")
                return purchases

        except Exception as e:
            logging.error(f"Error al listar las compras: {e}")
            raise

    @staticmethod
    async def update_purchase(purchase_id: str, data: dict) -> Purchase:
        try:
            purchase = await PurchaseService.get_purchase(purchase_id)
            if not purchase:
                logging.warning(f"No se encontró la compra con ID: {purchase_id}")
                return None

            for key, value in data.items():
                setattr(purchase, key, value)

            purchase.commission = purchase.calculate_commission()

            async with await get_db_connection() as db:
                await db.execute(
                    """
                    UPDATE purchases
                    SET name = ?, amount = ?, commission_rate = ?, commission = ?
                    WHERE id = ?
                    """,
                    (
                        purchase.name,
                        purchase.amount,
                        purchase.commission_rate,
                        purchase.commission,
                        purchase_id,
                    ),
                )
                await db.commit()

            logging.debug(f"Compra actualizada: {purchase.to_dict()}")
            return purchase

        except Exception as e:
            logging.error(f"Error al actualizar la compra: {e}")
            raise

    @staticmethod
    async def delete_purchase(purchase_id: str) -> bool:
        try:
            async with await get_db_connection() as db:
                result = await db.execute(
                    "DELETE FROM purchases WHERE id = ?", (purchase_id,)
                )
                await db.commit()

                if result.rowcount > 0:
                    logging.debug(f"Compra eliminada con ID: {purchase_id}")
                    return True
                else:
                    logging.warning(f"No se encontró la compra con ID: {purchase_id}")
                    return False

        except Exception as e:
            logging.error(f"Error al eliminar la compra: {e}")
            raise