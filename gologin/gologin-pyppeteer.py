import time
import asyncio
import pyppeteer
from sys import platform
from gologin import GoLogin

async def main():
	gl = GoLogin({
		"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWQ0ZDk5NmRmMjM4ODYyMGI1NTQ4YjQiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NWQ0ZWQ5N2Y1MDU4YWQyNWEyOTFmZjgifQ.bhB8vm_ewPd31dtqcwJsLALgeKH1JJsYpIWt-LM3jsk",
		"profile_id": "65d4d997df2388620b55495e",
		})

	debugger_address = gl.start()
	browser = await pyppeteer.connect(browserURL="http://"+debugger_address, defaultViewport=None)
	page = await browser.newPage()
	await gl.normalizePageView(page)
	await page.goto('https://hermes.com')
	await asyncio.sleep(100)
	await page.screenshot({'path': 'gologin.png'})
	await browser.close()
	gl.stop()

asyncio.get_event_loop().run_until_complete(main())
