import asyncio
from playwright.async_api import async_playwright
from gologin import GoLogin

async def main():
    gl = GoLogin({
		"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWQ0ZDk5NmRmMjM4ODYyMGI1NTQ4YjQiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NWQ0ZWQ5N2Y1MDU4YWQyNWEyOTFmZjgifQ.bhB8vm_ewPd31dtqcwJsLALgeKH1JJsYpIWt-LM3jsk",
		"profile_id": "65d4d997df2388620b554962",
		})

    debugger_address = gl.start()
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://"+debugger_address)
        default_context = browser.contexts[0]
        page = default_context.pages[0]
        await page.goto('https://gologin.com')
        await asyncio.sleep(1000)
        await page.screenshot(path="gologin.png")
        await page.close()
    gl.stop()

asyncio.get_event_loop().run_until_complete(main())
