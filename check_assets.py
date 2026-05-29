import asyncio
from playwright.async_api import async_playwright

async def check_assets():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        errors = []
        page.on("pageerror", lambda exc: errors.append(f"JS Error: {exc}"))
        
        failed_requests = []
        page.on("requestfailed", lambda request: failed_requests.append(f"Failed: {request.url}"))
        
        response_errors = []
        page.on("response", lambda response: 
            response_errors.append(f"Error {response.status}: {response.url}") if response.status >= 400 else None)

        url = "https://sarathi1010-alfo.github.io/skyspace-airport/"
        print(f"Checking {url} for asset errors...")
        await page.goto(url, wait_until="networkidle")
        
        if errors:
            print("\n--- JavaScript Errors ---")
            for e in errors: print(e)
        else:
            print("\n✅ No JavaScript runtime errors found.")

        if failed_requests:
            print("\n--- Failed Network Requests ---")
            for f in failed_requests: print(f)
        else:
            print("✅ All network requests succeeded.")

        assets_checked = False
        for r in response_errors:
            if "style.css" in r or "script.js" in r:
                print(f"❌ Critical Asset Error: {r}")
                assets_checked = True
        
        if not assets_checked:
            print("✅ style.css and script.js loaded successfully.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(check_assets())
