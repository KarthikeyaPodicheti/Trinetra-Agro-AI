import asyncio, asyncpg

async def test():
    # Pooler URL with URL-encoded @ (k%40R527...) 
    url = 'postgresql://postgres.jqbmrpvuruluxjooxzrg:k%2540R527844539255@aws-0-ap-south-1.pooler.supabase.com:6543/postgres'
    try:
        conn = await asyncio.wait_for(asyncpg.connect(url, timeout=10), timeout=15)
        ver = await conn.fetchval('SELECT version()')
        print(f'SUPABASE_POOLER_OK: {ver[:60]}')
        await conn.close()
    except Exception as e:
        print(f'SUPABASE_POOLER_FAIL: {e}')

asyncio.run(test())
