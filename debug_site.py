import asyncio
from playwright.async_api import async_playwright

async def debug_site():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        page.on("console", lambda msg: print(f"PAGE LOG: {msg.text}"))
        page.on("pageerror", lambda exc: print(f"PAGE ERROR: {exc}"))

        url = "https://sarathi1010-alfo.github.io/skyspace-airport/"
        print(f"Opening {url}")
        
        # Add a timeout and wait until load
        try:
            await page.goto(url, wait_until="load", timeout=60000)
            print("Page loaded.")
            
            # Check if tailwind is actually working
            is_tailwind_loaded = await page.evaluate("typeof tailwind !== 'undefined'")
            print(f"Tailwind loaded: {is_tailwind_loaded}")
            
            # Check if my script loaded
            is_script_loaded = await page.evaluate("typeof animateStats !== 'undefined'") # No, animateStats is inside DOMContentLoaded scope
            # Check if navbar exists
            navbar_exists = await page.is_visible("#navbar")
            print(f"Navbar exists: {navbar_exists}")
            
        except Exception as e:
            print(f"Error: {e}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_site())
