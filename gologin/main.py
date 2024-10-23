import asyncio
import base64
import sys
import time
import traceback

from cdp_socket.exceptions import CDPError
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
import random
import json
from gologin import GoLogin
from gologin import getRandomPort
from rearrange_json import change_headers_order
import os
from dotenv import load_dotenv
import json
import requests
import http.cookies
import whisper
import re
import aiohttp
import tempfile
from selenium_driverless.webdriver import Chrome, Target
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

                try:
                    blcoked_message = await content.find_element(By.CSS_SELECTOR, "p[class=\"captcha__human__title no-margin\"]")
                    await driver.quit()
                except:
                    pass


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

async def on_request(params, global_conn, profile_id, driver):
    url = params["request"]["url"]
    method = params["request"]["method"]
    if "product?" in url and method == "GET":
        headers = params["request"]["headers"]
        print("=========================")
        headers['authority'] = 'bck.hermes.com'
        # headers['Accept-Encoding'] = 'gzip, deflate, br'
        headers['accept-language'] = 'en'
        headers['sec-fetch-dest'] = 'empty'
        headers['sec-fetch-mode'] = 'cors'
        headers['sec-fetch-site'] = 'same-site'

        cookie_str = headers['Cookie']

        cookies = http.cookies.SimpleCookie(cookie_str)

        # Create a new cookie string with only _cs_mk and _uetsid
        new_cookie_str = ""
        for cookie in cookies.values():
            cookie_name = cookie.key
            if cookie_name in ["x-xsrf-token", "ECOM_SESS", "correlation_id", "datadome"]:
                new_cookie_str += f"{cookie_name}={cookie.value};"

        # Remove the trailing semicolon if necessary
        if new_cookie_str.endswith(";"):
            new_cookie_str = new_cookie_str[:-1]

        headers['Cookie'] = new_cookie_str
        
        

        TOKEN = os.getenv("TOKEN")
        BASE_URL = os.getenv("BASE_URL")

        headers_get_proxy = {
            'Authorization': f'Bearer {TOKEN}',
            'Content-Type': 'application/json'
        }
        url = f'{BASE_URL}browser/{profile_id}'

        response = requests.get(url, headers=headers_get_proxy)

        json_data = response.json()

        file_name = f'headers/headers-{profile_id}.json'
       
        headers['proxy_host'] = json_data["proxy"]["host"]
        headers['proxy_port'] = json_data["proxy"]["port"]
        headers['proxy_username'] = json_data["proxy"]["username"]
        headers['proxy_password'] = json_data["proxy"]["password"]
        for header_name, header_value in headers.items():
            print(f"'{header_name}' : '{header_value}'")
        print("=========================")
        with open(file_name, 'w') as json_file:
            json.dump(headers, json_file)
        
        new_order = ['authority', 'Accept', 'accept-language', 'Cookie', 'DNT', 'Origin', 'Referer', 'sec-ch-ua', 'sec-ch-ua-mobile',
                    'sec-ch-ua-platform', 'sec-fetch-dest', 'sec-fetch-mode', 'sec-fetch-site', 'User-Agent', 'x-hermes-locale', 'x-xsrf-token', 
                    'proxy_host', 'proxy_port', 'proxy_username', 'proxy_password']  # Desired order of keys
        
        

        change_headers_order(file_name, new_order)
        
    _params = {"requestId": params['requestId']}
    if params.get('responseStatusCode') in [301, 302, 303, 307, 308]:
        # redirected request
        return await global_conn.execute_cdp_cmd("Fetch.continueResponse", _params)
    else:
        try:
            body = await global_conn.execute_cdp_cmd("Fetch.getResponseBody", _params, timeout=1)
        except CDPError as e:
            if e.code == -32000 and e.message == 'Can only get response body on requests captured after headers received.':
                # print(params, "\n", file=sys.stderr)
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
                # print(f"decoding took long: {_time} s")
                aaa = "sdf"
            await global_conn.execute_cdp_cmd("Fetch.fulfillRequest", fulfill_params)
            # print("Mocked response", url)
            if "https://geo.captcha-delivery.com/captcha" in url:
                await asyncio.sleep(5)
                await solve_captcha(driver)


async def main(profile_id):
    random_port = getRandomPort()
    gl = GoLogin({
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWVlNmU3NjZjMTk3MjQ4NDE4OTQyNTEiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NWVlZmRkZTFiZTFhY2JkYWRhZDA3ZjkifQ.WTRnpry8VdJR_xAvJ4y5-USS0ivFx0S-X0-44Noxxyw",
        "profile_id": profile_id,
        "port": random_port
	})
    debugger_address = gl.start()
    print(debugger_address)
    options = webdriver.ChromeOptions()
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.debugger_address = debugger_address

    async with webdriver.Chrome(max_ws_size=2 ** 30, options=options) as driver:
        driver.base_target.socket.on_closed.append(lambda code, reason: print(f"chrome exited"))

        global_conn = driver.base_target
        # await global_conn.execute_cdp_cmd("Fetch.enable",
        #                                   cmd_args={"patterns": [{"requestStage": "Response", "urlPattern": "https://bck.hermes.com/product?*, https://geo.captcha-delivery.com/captcha/*"}]})
        await global_conn.execute_cdp_cmd("Fetch.enable",
                                          cmd_args={"patterns": [
                                              {"requestStage": "Response", "urlPattern": "https://bck.hermes.com/product?*"},
                                              {"requestStage": "Response", "urlPattern": "https://geo.captcha-delivery.com/captcha/*"}
                                              ]})
        await global_conn.add_cdp_listener("Fetch.requestPaused", lambda data: on_request(data, global_conn, profile_id, driver))
        # await global_conn.execute_cdp_cmd("Fetch.disable")
        await driver.get("https://hermes.com", timeout=60, wait_load=True)
        # await driver.get("https://httpbin.org/ip", timeout=60, wait_load=True)
        await asyncio.sleep(30000)

        page_height_driver = await driver.execute_script("return document.documentElement.clientHeight")
        page_width_driver = await driver.execute_script("return document.documentElement.clientWidth")
        print(page_height_driver, page_width_driver)

        # print(page_height_driver, page_width_driver)
        try:
            accept_cookies_button = await driver.find_element(By.CSS_SELECTOR, "button[id=\"onetrust-accept-btn-handler\"]")
            await accept_cookies_button.click(move_to=True)
        except:
            pass
        await driver.save_screenshot('screenshot.png')
        await asyncio.sleep(3)
        # menu_button = await driver.find_element(By.CSS_SELECTOR, "nav[aria-label=\"Navigation menu\"]")
        # await menu_button.click()
        # await asyncio.sleep(3)
        # list_element = await driver.find_element(By.CSS_SELECTOR, "li[class=\"menu-list-item ng-star-inserted\"]")
        # await list_element.click()
        # await asyncio.sleep(3)
        # ul_element = await driver.find_element(By.TAG_NAME, "h-menu-secondary-entry")
        # await ul_element.click()
        # await asyncio.sleep(3)
        # link = await driver.find_element(By.TAG_NAME, "h-menu-link")
        # await link.click()
        await driver.get("https://www.hermes.com/us/en/category/women/ready-wear/spring-summer-collection/#")

        
        await asyncio.sleep(5)
        await driver.save_screenshot('screenshot.png')
        # try:
        #     menu_pictures = await driver.find_elements(By.CSS_SELECTOR, "span[class=\"title-small category-poster-text\"]")
        #     print(len(menu_pictures))
        #     await driver.execute_script("arguments[0].scrollIntoView();", menu_pictures[1])
        #     await asyncio.sleep(3)
        #     await menu_pictures[random.randint(0, len(menu_pictures) - 1)].click(move_to=True)
        #     await asyncio.sleep(5)
        # except:
        #     await asyncio.sleep(10)
        #     menu_pictures = await driver.find_elements(By.CSS_SELECTOR, "span[class=\"title-small category-poster-text\"]")
        #     print(len(menu_pictures))
        #     await driver.execute_script("arguments[0].scrollIntoView();", menu_pictures[1])
        #     await menu_pictures[random.randint(0, len(menu_pictures) - 1)].click(move_to=True)
        #     await asyncio.sleep(5)
        
        # await asyncio.sleep(5)
        try:
            product = await driver.find_element(By.CSS_SELECTOR, "span[class=\"product-item-name\"]")
            await product.click(move_to=True)
        except:
            try:
                await asyncio.sleep(7)
                product = await driver.find_element(By.CSS_SELECTOR, "span[class=\"product-item-name\"]")
                await product.click(move_to=True)
            except:
                await asyncio.sleep(7)
                product = await driver.find_element(By.CSS_SELECTOR, "span[class=\"product-item-name\"]")
                await product.click(move_to=True)
        await asyncio.sleep(7)

        await driver.save_screenshot('screenshot.png')

        try:
            add_to_cart_button = await driver.find_element(By.CSS_SELECTOR, "button[data-testid=\"Add to cart\"]")
        except:
            try:
                await asyncio.sleep(7)
                product = await driver.find_element(By.CSS_SELECTOR, "span[class=\"product-item-name\"]")
                await product.click(move_to=True)
            except:
                pass
        await asyncio.sleep(5)
        await driver.save_screenshot('screenshot.png')
        while True:
            
            # time.sleep(10) # no. cloudflare would hang
            

            pointer = await driver.current_pointer
            await pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))
            await pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))
            await pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))
            await pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))
            await pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))
            await pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))
            try:
                partner_products_element = await driver.find_element(By.CSS_SELECTOR, "h-product-page-grid[id=\"product-page-cross-sell-perfect-partner\"]")
                partner_products = await partner_products_element.find_elements(By.TAG_NAME, "li")
                print(len(partner_products))
                await partner_products[random.randint(0, len(partner_products) - 1)].click(move_to=True)
                print("new product")
            except:
                pass
            await driver.save_screenshot('screenshot.png')
            await asyncio.sleep(60)

def run_bot(profile_id):
    asyncio.run(main(profile_id))