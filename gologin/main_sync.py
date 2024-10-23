from selenium_driverless.sync import webdriver
from gologin import GoLogin
from gologin import getRandomPort

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

with webdriver.Chrome(options=options) as driver:
    driver.get('http://nowsecure.nl#relax')
    driver.sleep(1000)
    driver.wait_for_cdp("Page.domContentEventFired", timeout=15)

    title = driver.title
    url = driver.current_url
    source = driver.page_source
    print(title)