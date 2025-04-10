from sanic import Blueprint
from controllers.purchase_controller import PurchaseController

purchase_blueprint = Blueprint("purchase", url_prefix="/purchases")

@purchase_blueprint.post("")
async def create_purchase(request):
    return await PurchaseController.create_purchase(request)

@purchase_blueprint.get("")
async def list_purchases(request):
    return await PurchaseController.list_purchases(request)

@purchase_blueprint.get("/<purchase_id>")
async def get_purchase(request, purchase_id: str):
    return await PurchaseController.get_purchase(request, purchase_id)

@purchase_blueprint.put("/<purchase_id>")
async def update_purchase(request, purchase_id: str):
    return await PurchaseController.update_purchase(request, purchase_id)

@purchase_blueprint.delete("/<purchase_id>")
async def delete_purchase(request, purchase_id: str):
    return await PurchaseController.delete_purchase(request, purchase_id)