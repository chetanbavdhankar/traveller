import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(locale="en-US", timezone_id="Europe/London")
        page = await context.new_page()
        print("Visiting flights...")
        await page.goto("https://www.google.com/travel/flights?q=Flights+from+LHR+to+WAW+on+2026-03-28", wait_until="networkidle")
        
        try:
            print("Checking consent...")
            await page.wait_for_selector("text=\"Reject all\"", timeout=3000)
            await page.click("text=\"Reject all\"")
            print("Clicked reject all")
            await page.wait_for_timeout(3000)
        except Exception as e:
            print("No consent button found or clicked", e)
            
        print("Dumping HTML...")
        html = await page.content()
        with open("google_dump_postconsent.html", "w", encoding="utf-8") as f:
            f.write(html)
        await browser.close()
        print("Done")

asyncio.run(main())
