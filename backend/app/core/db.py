from prisma import Prisma
import logging

logger = logging.getLogger("welth.db")

db = Prisma()

async def init_db():
    """Establish connection to the database."""
    try:
        if not db.is_connected():
            await db.connect()
            logger.info("Database connection established successfully via Prisma ORM.")
    except Exception as e:
        logger.error(f"Failed to connect to the database: {e}")
        raise

async def close_db():
    """Disconnect from the database."""
    try:
        if db.is_connected():
            await db.disconnect()
            logger.info("Database connection closed.")
    except Exception as e:
        logger.error(f"Error while disconnecting from the database: {e}")
