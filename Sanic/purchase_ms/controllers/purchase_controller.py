from sanic.response import json
from schemas.purchase_schema import PurchaseCreateSchema, PurchaseUpdateSchema, PurchaseResponseSchema
from services.purchase_service import PurchaseService
from uuid import UUID

class PurchaseController:
    @staticmethod
    async def create_purchase(request):
        try:
            data = PurchaseCreateSchema(**request.json).dict()
            purchase = await PurchaseService.create_purchase(data)
            return json(PurchaseResponseSchema(**purchase.to_dict()).dict(), status=201)
        except Exception as e:
            return json({"error": str(e)}, status=400)

    @staticmethod
    async def list_purchases(request):
        try:
            purchases = await PurchaseService.list_purchases()
            return json([PurchaseResponseSchema(**p.to_dict()).dict() for p in purchases])
        except Exception as e:
            return json({"error": str(e)}, status=500)

    @staticmethod
    async def get_purchase(request, purchase_id: str):
        try:
            purchase_id = UUID(purchase_id)
            purchase = await PurchaseService.get_purchase(str(purchase_id))
            if purchase:
                return json(PurchaseResponseSchema(**purchase.to_dict()).dict())
            else:
                return json({"error": "Purchase not found"}, status=404)
        except ValueError:
            return json({"error": "Invalid purchase ID"}, status=400)
        except Exception as e:
            return json({"error": str(e)}, status=500)

    @staticmethod
    async def update_purchase(request, purchase_id: str):
        try:
            purchase_id = UUID(purchase_id)
            data = PurchaseUpdateSchema(**request.json).dict(exclude_unset=True)
            purchase = await PurchaseService.update_purchase(str(purchase_id), data)
            if purchase:
                return json(PurchaseResponseSchema(**purchase.to_dict()).dict())
            else:
                return json({"error": "Purchase not found"}, status=404)
        except ValueError:
            return json({"error": "Invalid purchase ID"}, status=400)
        except Exception as e:
            return json({"error": str(e)}, status=400)

    @staticmethod
    async def delete_purchase(request, purchase_id: str):
        try:
            purchase_id = UUID(purchase_id)
            success = await PurchaseService.delete_purchase(str(purchase_id))
            if success:
                return json({"message": "Purchase deleted"}, status=200)
            else:
                return json({"error": "Purchase not found"}, status=404)
        except ValueError:
            return json({"error": "Invalid purchase ID"}, status=400)
        except Exception as e:
            return json({"error": str(e)}, status=500)