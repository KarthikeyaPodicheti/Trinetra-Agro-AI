import asyncio
from backend.database.session import get_session_factory
from backend.models import User, Farmer
from sqlalchemy import select

async def main():
    sf = get_session_factory()
    async with sf() as session:
        res = await session.execute(select(User).where(User.email == 'demo@farm.com'))
        demo_user = res.scalar_one_or_none()
        if demo_user is None:
            print("Demo user demo@farm.com not found. Seeding demo user...")
            demo_user = User(
                id='demo-user-0000-0000-000000000001',
                email='demo@farm.com',
                hashed_password='$2b$12$hrdLaTqPg9C7VI48x6atyOnBZ4arlbdHRL7ug3PwRYsYAeQ1LZiAa',
                full_name='Demo Farmer',
                phone='+91-9999999999',
                is_active=True
            )
            session.add(demo_user)
            
            # Check if farmer profile exists
            res_farmer = await session.execute(select(Farmer).where(Farmer.user_id == 'demo-user-0000-0000-000000000001'))
            demo_farmer = res_farmer.scalar_one_or_none()
            if demo_farmer is None:
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
            print("Demo user and farmer profile seeded successfully!")
        else:
            print("Demo user demo@farm.com already exists.")

if __name__ == '__main__':
    asyncio.run(main())
