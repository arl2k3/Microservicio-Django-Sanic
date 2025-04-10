import aiosqlite
import logging

logging.basicConfig(level=logging.DEBUG)

DATABASE_PATH = "purchases.db"

async def init_db():
    """
    Inicializa la base de datos creando la tabla 'purchases' si no existe.
    """
    logging.debug("Inicializando base de datos...")
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS purchases (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                amount REAL NOT NULL,
                commission_rate REAL NOT NULL,
                commission REAL NOT NULL
            )
        """)
        await db.commit()
    logging.debug("Base de datos inicializada.")

async def get_db_connection():
    """
    Retorna una nueva conexión a la base de datos.
    """
    logging.debug("Conectando a la base de datos...")
    return aiosqlite.connect(DATABASE_PATH)