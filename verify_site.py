import asyncio
from playwright.async_api import async_playwright
import os

async def verify():
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={'width': 1280, 'height': 1800})
        page = await context.new_page()
        
        url = "https://sarathi1010-alfo.github.io/skyspace-airport/"
        print(f"Navigating to {url}")
        await page.goto(url, wait_until="networkidle")
        
        # Verify Sections
        sections = ['#home', '#services', '#why-us', '#stats', '#about', '#testimonials', '#faq', '#contact']
        for section in sections:
            is_visible = await page.is_visible(section)
            print(f"Section {section} visible: {is_visible}")
            if not is_visible:
                print(f"Warning: {section} not found!")

        # Take Desktop Screenshot
        os.makedirs("outputs/verification", exist_ok=True)
        await page.screenshot(path="outputs/verification/desktop.png", full_page=True)
        print("Desktop screenshot saved.")

        # Test Navigation (Desktop)
        await page.click("nav a[href='#services']")
        # wait a bit for scroll
        await asyncio.sleep(1)
        # Check if scrolled (simulated)
        
        # Verify Mobile
        mobile_context = await browser.new_context(
            viewport={'width': 375, 'height': 812},
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1"
        )
        mobile_page = await mobile_context.new_page()
        await mobile_page.goto(url, wait_until="networkidle")
        
        # Verify Mobile Menu Button
        is_menu_btn_visible = await mobile_page.is_visible("#mobile-menu-btn")
        print(f"Mobile menu button visible: {is_menu_btn_visible}")
        
        # Click mobile menu
        await mobile_page.click("#mobile-menu-btn")
        await asyncio.sleep(0.5)
        is_menu_open = await mobile_page.is_visible("#mobile-menu:not(.hidden)")
        print(f"Mobile menu opened: {is_menu_open}")
        
        await mobile_page.screenshot(path="outputs/verification/mobile.png")
        print("Mobile screenshot saved.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify())
