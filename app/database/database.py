from app.database.connection import Settings

settings = Settings()

async def init_db():
    await settings.initialize_database()
