import asyncio
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("1. Loading login page...")
        await page.goto('https://frontend-next-xi-six.vercel.app/login', timeout=30000)
        print(f"   Page title: {await page.title()}")
        
        print("2. Filling credentials...")
        await page.fill('input[type="email"]', 'demo@farm.com')
        await page.fill('input[type="password"]', 'demo123456')
        
        print("3. Clicking Sign In...")
        await page.click('button[type="submit"]')
        
        # Wait for navigation
        await asyncio.sleep(3)
        
        url = page.url
        print(f"4. Current URL after redirect: {url}")
        
        cookies = await page.context.cookies()
        for c in cookies:
            print(f"   Cookie: {c['name']}={c['value'][:30]}... domain={c['domain']} secure={c.get('secure')}")
        
        # Check if login was successful
        if '/login' not in url:
            print("SUCCESS - Dashboard loaded!")
        else:
            print("FAILED - Still on login page")
            
        await browser.close()

asyncio.run(test())
