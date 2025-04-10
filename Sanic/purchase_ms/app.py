# app.py

from sanic import Sanic
from routes.purchase_routes import purchase_blueprint
from database.db import init_db

app = Sanic("PurchaseService")

@app.before_server_start
async def setup_db(app, loop):
    await init_db()

app.blueprint(purchase_blueprint)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)