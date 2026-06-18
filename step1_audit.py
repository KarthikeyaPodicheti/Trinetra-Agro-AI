"""
Step 1: Take mobile screenshot of dashboard at iPhone 14 Pro dimensions,
then analyze against UI/UX Pro Max principles.
"""
import asyncio
from playwright.async_api import async_playwright

FRONTEND = "https://frontend-next-xi-six.vercel.app"
EMAIL = "demo@farm.com"
PASSWORD = "demo123456"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(
            viewport={"width": 390, "height": 844},
            device_scale_factor=3,
            is_mobile=True,
            has_touch=True,
        )
        page = await ctx.new_page()
        
        # Login
        await page.goto(f"{FRONTEND}/login", wait_until="networkidle", timeout=30000)
        await page.fill("input[type='email']", EMAIL)
        await page.fill("input[type='password']", PASSWORD)
        await page.click("text=Sign In")
        await page.wait_for_timeout(5000)
        
        print(f"URL after login: {page.url}")
        
        # Navigate to dashboard
        await page.goto(f"{FRONTEND}/", wait_until="networkidle", timeout=15000)
        await page.wait_for_timeout(3000)
        
        # Full page screenshot
        await page.screenshot(path="dashboard_mobile.png", full_page=True)
        print("Dashboard screenshot saved: dashboard_mobile.png")
        
        # Collect UX metrics
        metrics = await page.evaluate("""() => {
            const report = {};
            
            // 1. Touch targets
            const interactive = Array.from(document.querySelectorAll('button, a, input, select, textarea, [role="button"]'));
            const small = interactive.filter(el => {
                const r = el.getBoundingClientRect();
                return (r.height < 42 && r.height > 0) || (r.width < 42 && r.width > 0);
            });
            report.smallTouchTargets = small.length;
            report.totalInteractive = interactive.length;
            
            // 2. Font size consistency
            const texts = Array.from(document.querySelectorAll('p, h1, h2, h3, h4, h5, span, a, li, td, label, div'));
            const fontSizes = {};
            texts.forEach(el => {
                if (!el.textContent || el.textContent.trim().length < 3) return;
                const fs = Math.round(parseFloat(getComputedStyle(el).fontSize));
                fontSizes[fs] = (fontSizes[fs] || 0) + 1;
            });
            report.fontSizes = fontSizes;
            
            // 3. Spacing consistency
            const containers = Array.from(document.querySelectorAll('div[class*="p-"], div[class*="m-"], div[class*="gap-"]'));
            report.containersWithSpacing = containers.length;
            
            // 4. Card shadows & elevation
            const cards = Array.from(document.querySelectorAll('[class*="shadow"], [class*="rounded"]'));
            report.cards = cards.length;
            
            // 5. Color usage
            const greens = Array.from(document.querySelectorAll('[class*="green"], [class*="emerald"]'));
            report.greenElements = greens.length;
            
            // 6. Content density - chars visible
            const bodyText = document.body.innerText.substring(0, 2000);
            report.bodyTextPreview = bodyText;
            
            // 7. Horizontal overflow
            report.scrollWidth = document.documentElement.scrollWidth;
            report.clientWidth = document.documentElement.clientWidth;
            report.hasHorizontalScroll = document.documentElement.scrollWidth > document.documentElement.clientWidth + 2;
            
            return report;
        }""")
        
        print(f"\nUX Metrics:")
        print(f"  Interactive elements: {metrics['totalInteractive']}")
        print(f"  Small touch targets: {metrics['smallTouchTargets']}")
        print(f"  Cards with shadows: {metrics['cards']}")
        print(f"  Has horizontal scroll: {metrics['hasHorizontalScroll']} (scroll={metrics['scrollWidth']}, client={metrics['clientWidth']})")
        print(f"  Font sizes used: {dict(sorted(metrics['fontSizes'].items()))}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
