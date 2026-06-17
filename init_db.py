import asyncio
from sqlalchemy import text
from backend.database.session import get_engine, Base
from backend.models import User, Farmer

async def init_models():
    engine = get_engine()
    print("Initializing SQLite database tables...")
    async with engine.begin() as conn:
        # Drop existing tables if they exist
        await conn.run_sync(Base.metadata.drop_all)
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    
    # Now let's insert the seed data
    from backend.database.session import get_session_factory
    
    session_factory = get_session_factory()
    async with session_factory() as session:
        # Create the demo user
        demo_user = User(
            id='demo-user-0000-0000-000000000001',
            email='demo@farm.com',
            hashed_password='$2b$12$hrdLaTqPg9C7VI48x6atyOnBZ4arlbdHRL7ug3PwRYsYAeQ1LZiAa',
            full_name='Demo Farmer',
            phone='+91-9999999999',
            is_active=True
        )
        session.add(demo_user)
        
        # Create the demo farmer profile
        demo_farmer = Farmer(
            id='demo-farmer-0000-0000-000000000001',
            user_id='demo-user-0000-0000-000000000001',
            soil_type='Black Soil',
            land_size_acres=5.0,
            budget_inr=50000.0,
            location='Telangana, India',
            crops=['rice', 'wheat'],
            irrigation_type='Drip Irrigation',
            experience_years=10
        )
        session.add(demo_farmer)
        await session.commit()
    print("Database tables created and seeded successfully!")

if __name__ == "__main__":
    asyncio.run(init_models())
