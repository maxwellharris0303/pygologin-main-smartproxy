from selenium_driverless import webdriver
from selenium_driverless.types.by import By
import asyncio
from gologin import GoLogin
from gologin import getRandomPort


async def main():
    random_port = getRandomPort()
    gl = GoLogin({
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWQ0ZDk5NmRmMjM4ODYyMGI1NTQ4YjQiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NWQ0ZWQ5N2Y1MDU4YWQyNWEyOTFmZjgifQ.bhB8vm_ewPd31dtqcwJsLALgeKH1JJsYpIWt-LM3jsk",
        "profile_id": "65d59db36956dab03499bc72",
        "port": random_port
    })
    debugger_address = gl.start()
    print(debugger_address)
    options = webdriver.ChromeOptions()
    options.debugger_address = debugger_address
    async with webdriver.Chrome(options=options) as driver:
        await driver.get('http://nowsecure.nl#relax')
        await driver.sleep(1000)
        await driver.wait_for_cdp("Page.domContentEventFired", timeout=15)
        
        # wait 10s for elem to exist
        elem = await driver.find_element(By.XPATH, '/html/body/div[2]/div/main/p[2]/a', timeout=10)
        await elem.click(move_to=True)

        alert = await driver.switch_to.alert
        print(alert.text)
        await alert.accept()

        print(await driver.title)


asyncio.run(main())
