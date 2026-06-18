"""
Visual audit of each mobile page — check for layout, readability, spacing issues.
Takes screenshots AND inspects computed styles.
"""
import asyncio
import os
import json
from playwright.async_api import async_playwright

FRONTEND = "https://frontend-next-xi-six.vercel.app"
EMAIL = "demo@farm.com"
PASSWORD = "demo123456"

async def visual_check(page, name, url, screenshot_path):
    """Deep visual analysis of a page."""
    await page.goto(url, wait_until="networkidle", timeout=30000)
    await page.wait_for_timeout(2500)
    
    issues = []
    
    # 1. Screenshot for visual inspection
    await page.screenshot(path=screenshot_path, full_page=True)
    
    # 2. Check for elements that overflow horizontally (even slightly)
    overflow = await page.evaluate("""() => {
        const results = [];
        document.querySelectorAll('div, section, table, pre, code, blockquote').forEach(el => {
            const r = el.getBoundingClientRect();
            const cs = window.getComputedStyle(el);
            if (r.right > window.innerWidth + 2) {
                results.push({
                    tag: el.tagName,
                    cls: el.className.substring(0, 40),
                    width: Math.round(r.width),
                    right: Math.round(r.right),
                    overflow: cs.overflowX,
                    wordBreak: cs.wordBreak,
                    whiteSpace: cs.whiteSpace
                });
            }
        });
        return results;
    }""")
    for o in overflow:
        issues.append(f"Overflow element: {o['tag']}.{o['cls']} (width={o['width']}px, right={o['right']}px)")
    
    # 3. Check text readability — min font size for body text
    tiny_text = await page.evaluate("""() => {
        const issues = [];
        document.querySelectorAll('p, span, h1, h2, h3, h4, h5, h6, td, li, label, a').forEach(el => {
            if (!el.textContent || el.textContent.trim().length === 0) return;
            const fs = parseFloat(window.getComputedStyle(el).fontSize);
            const lh = parseFloat(window.getComputedStyle(el).lineHeight);
            if (fs < 11 && fs > 0) {
                issues.push({
                    tag: el.tagName,
                    txt: el.textContent.trim().substring(0, 30),
                    fontSize: fs,
                    lineHeight: lh
                });
            }
        });
        return issues.slice(0, 5);
    }""")
    for t in tiny_text:
        issues.append(f"Tiny text (< 11px): {t['tag']} '{t['txt']}' = {t['fontSize']}px")
    
    # 4. Check for horizontal scroll triggers
    scrollWidth = await page.evaluate("document.documentElement.scrollWidth")
    clientWidth = await page.evaluate("document.documentElement.clientWidth")
    if scrollWidth > clientWidth + 5:
        issues.append(f"Page horizontally scrollable: scrollWidth={scrollWidth}px > clientWidth={clientWidth}px")
    
    # 5. Check for overlapping content (elements stacking on top of each other)
    overlaps = await page.evaluate("""() => {
        const results = [];
        const els = Array.from(document.querySelectorAll('div, section'));
        for (let i = 0; i < els.length && i < 50; i++) {
            const r = els[i].getBoundingClientRect();
            if (r.width <= 0 || r.height <= 0) continue;
            if (r.left < -10 || r.right > window.innerWidth + 10) {
                results.push({
                    tag: els[i].tagName,
                    cls: els[i].className.substring(0, 40),
                    left: Math.round(r.left),
                    right: Math.round(r.right),
                    width: Math.round(r.width)
                });
            }
        }
        return results;
    }""")
    for o in overlaps:
        issues.append(f"Positioning issue: {o['tag']}.{o['cls']} at left={o['left']}px, right={o['right']}px")
    
    # 6. Check for long unbroken text
    long_text = await page.evaluate("""() => {
        const results = [];
        document.querySelectorAll('p, td, li, span').forEach(el => {
            const text = el.textContent || '';
            if (text.length > 200) {
                const cs = window.getComputedStyle(el);
                results.push({
                    tag: el.tagName,
                    textLen: text.length,
                    width: Math.round(el.getBoundingClientRect().width),
                    wordBreak: cs.wordBreak,
                    overflowWrap: cs.overflowWrap
                });
            }
        });
        return results.slice(0, 3);
    }""")
    for t in long_text:
        issues.append(f"Long text ({t['textLen']} chars, {t['width']}px wide, wordBreak={t['wordBreak']})")
    
    # 7. Check chart/graph elements that might overflow
    charts = await page.evaluate("""() => {
        const results = [];
        document.querySelectorAll('.recharts-wrapper, svg, canvas').forEach(el => {
            const r = el.getBoundingClientRect();
            if (r.width > window.innerWidth + 10) {
                results.push({tag: el.tagName, width: Math.round(r.width), src: el.className.substring(0, 30)});
            }
        });
        return results;
    }""")
    for c in charts:
        issues.append(f"Chart overflow: {c['tag']} {c['src']} = {c['width']}px wide")
    
    # 8. Check contrast ratio of main text
    contrast = await page.evaluate("""() => {
        const results = [];
        document.querySelectorAll('p, h1, h2, h3, a').forEach(el => {
            const cs = window.getComputedStyle(el);
            const color = cs.color;
            const bg = cs.backgroundColor;
            results.push({
                tag: el.tagName,
                color: color,
                bg: bg,
                fontSize: cs.fontSize
            });
        });
        return results.slice(0, 5);
    }""")
    for c in contrast:
        issues.append(f"Contrast: {c['tag']} text={c['color']} bg={c['bg']} fs={c['fontSize']}")
    
    # 9. Check form inputs have labels (accessibility)
    inputs = await page.evaluate("""() => {
        const results = [];
        document.querySelectorAll('input, select, textarea').forEach(el => {
            if (el.type === 'hidden' || el.type === 'submit') return;
            const hasLabel = el.labels && el.labels.length > 0;
            const hasPlaceholder = !!el.placeholder;
            const hasAriaLabel = !!el.getAttribute('aria-label');
            const name = el.name || el.id || '';
            const type = el.type || '';
            if (!hasLabel && !hasPlaceholder && !hasAriaLabel) {
                results.push({tag: el.tagName, type: type, name: name});
            }
        });
        return results;
    }""")
    for inp in inputs:
        issues.append(f"Input without label/placeholder/aria: {inp['tag']} type={inp['type']} name={inp['name']}")
    
    # 10. Check touch-action properties
    touch = await page.evaluate("""() => {
        const results = [];
        document.querySelectorAll('div, button, a, input, select, textarea').forEach(el => {
            const cs = window.getComputedStyle(el);
            if (cs.touchAction && cs.touchAction !== 'auto') {
                results.push({tag: el.tagName, touchAction: cs.touchAction});
            }
        });
        return results.slice(0, 3);
    }""")
    # touch-action is fine — just informational
    
    return issues

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
        print(f"Logged in: {page.url}\n")
        
        all_issues = {}
        screenshots = []
        
        pages = [
            ("Login", "/login", "login.png"),
            ("Register", "/register", "register.png"),
            ("Dashboard", "/", "dashboard.png"),
            ("Advisor", "/advisor", "advisor.png"),
            ("Disease Scanner", "/disease-scanner", "disease.png"),
            ("Market", "/market", "market.png"),
            ("Risk", "/risk", "risk.png"),
            ("Yield", "/yield", "yield.png"),
            ("Chatbot", "/chatbot", "chatbot.png"),
            ("Feedback", "/feedback", "feedback.png"),
        ]
        
        for name, path, screenshot in pages:
            issues = await visual_check(page, name, f"{FRONTEND}{path}", screenshot)
            all_issues[name] = issues
            screenshots.append(screenshot)
        
        # Summary
        total = sum(len(v) for v in all_issues.values())
        print(f"Total visual issues: {total}")
        for name, issues in all_issues.items():
            count = len(issues)
            status = "OK" if count == 0 else f"{count} ISSUES"
            print(f"  {name}: {status}")
            for i in issues:
                safe = i.encode('ascii', errors='replace').decode('ascii')
                print(f"    - {safe}")
        
        await browser.close()
        print(f"\nScreenshots: {os.path.join(os.getcwd(), 'frontend-next')}")

if __name__ == "__main__":
    asyncio.run(main())
