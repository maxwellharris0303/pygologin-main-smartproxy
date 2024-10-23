import base64
import sys
import time
import traceback

from cdp_socket.exceptions import CDPError
from selenium_driverless import webdriver
import whisper
import re
import aiohttp
import tempfile
import asyncio
from selenium_driverless import webdriver
from selenium_driverless.webdriver import Chrome, Target
from selenium_driverless.types.by import By
from selenium_driverless.types.webelement import NoSuchElementException
import typing

async def download_audio(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                # 创建临时文件
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                    # 从响应中读取音频数据并写入临时文件
                    audio_data = await response.read()
                    tmp_file.write(audio_data)
                    # 获取临时文件的路径
                    tmp_file_path = tmp_file.name
                print("Audio file downloaded successfully.")
                return tmp_file_path
            else:
                print(f"Failed to download audio file: {response.status}")
                return None

async def solve_captcha(driver: typing.Union[Chrome, Target]):
    try:
        # noinspection PyTypeChecker
        iframes = await driver.find_elements(By.TAG_NAME, 'iframe')
        # Get the src attribute of the iframe
        print(len(iframes))
        for iframe in iframes:
            iframe_src = await iframe.get_attribute('src')
            if iframe_src.startswith('https://geo.captcha-delivery.com/captcha/'):
                print('click')
                content = await iframe.content_document

                # click use audio captcha button
                captcha_audio_button = await content.find_element(By.ID, 'captcha__audio__button')
                await captcha_audio_button.click()

                # find audio element
                audio_element = await content.find_element(By.XPATH, '//audio[@class="audio-captcha-track"]')

                # find audio url
                audio_url = await audio_element.get_attribute('src')
                print('Audio src is: ' + audio_url)

                # download audio file
                audio_file_path = await download_audio(audio_url)
                print('Audio path is: ' + audio_file_path)
                
                # use whisper to transcribe speech to text
                model = whisper.load_model("base")
                result = model.transcribe(audio_file_path, fp16=False)
                matches = re.findall(r'\d', result['text'])
                solution = matches[-6:]
                print(solution)

                # enter solution
                for i in range(6):
                    audio_input = (await content.find_elements(By.XPATH, '//input[@class="audio-captcha-inputs"]'))[i]
                    await audio_input.click()  # Ensure the input field is focused
                    # await asyncio.sleep(0.1)  # Add a small delay if necessary
                    await audio_input.write(solution[i])

                print('Captcha Solved!')
                await asyncio.sleep(5)
            else:
                print('No captcha found!')
    except NoSuchElementException:
        print('No captcha found!')

async def on_request(params, global_conn, driver):
    url = params["request"]["url"]
    _params = {"requestId": params['requestId']}
    if params.get('responseStatusCode') in [301, 302, 303, 307, 308]:
        # redirected request
        return await global_conn.execute_cdp_cmd("Fetch.continueResponse", _params)
    else:
        try:
            body = await global_conn.execute_cdp_cmd("Fetch.getResponseBody", _params, timeout=1)
        except CDPError as e:
            if e.code == -32000 and e.message == 'Can only get response body on requests captured after headers received.':
                print(params, "\n", file=sys.stderr)
                traceback.print_exc()
                await global_conn.execute_cdp_cmd("Fetch.continueResponse", _params)
            else:
                raise e
        else:
            start = time.perf_counter()
            body_decoded = base64.b64decode(body['body'])

            # modify body here

            body_modified = base64.b64encode(body_decoded).decode("ascii")
            fulfill_params = {"responseCode": 200, "body": body_modified, "responseHeaders": params["responseHeaders"]}
            fulfill_params.update(_params)
            if params["responseStatusText"] != "":
                # empty string throws "Invalid http status code or phrase"
                fulfill_params["responsePhrase"] = params["responseStatusText"]

            _time = time.perf_counter() - start
            if _time > 0.01:
                print(f"decoding took long: {_time} s")
            await global_conn.execute_cdp_cmd("Fetch.fulfillRequest", fulfill_params)
            print("Mocked response", url)
            await asyncio.sleep(5)
            await solve_captcha(driver)
            # await driver.refresh()
            # await asyncio.sleep(5)
            # await solve_captcha(driver)
            # await driver.quit()


async def main():
    async with webdriver.Chrome(max_ws_size=2 ** 30) as driver:
        driver.base_target.socket.on_closed.append(lambda code, reason: print(f"chrome exited"))

        
        global_conn = driver.base_target
        await global_conn.execute_cdp_cmd("Fetch.enable",
                                          cmd_args={"patterns": [{"requestStage": "Response", "urlPattern": "https://geo.captcha-delivery.com/captcha/*"}]})
        await global_conn.add_cdp_listener("Fetch.requestPaused", lambda data: on_request(data, global_conn, driver))

        await driver.get("https://hermes.com", timeout=60, wait_load=False)
        while True:
            # time.sleep(10) # no. cloudflare would hang
            await asyncio.sleep(10)


asyncio.run(main())