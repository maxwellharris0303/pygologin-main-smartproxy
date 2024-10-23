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


async def on_request(params, global_conn):
    url = params["request"]["url"]
    method = params["request"]["method"]
    if "product?" in url and method == "GET":
        headers = params["request"]["headers"]
        print("=========================")
        headers['Host'] = 'bck.hermes.com'
        for header_name, header_value in headers.items():
            print(f"'{header_name}' : '{header_value}'")
        print("=========================")
        with open('data.json', 'w') as json_file:
            json.dump(headers, json_file)
        
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


async def main():
    random_port = getRandomPort()
    gl = GoLogin({
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWQ0ZDk5NmRmMjM4ODYyMGI1NTQ4YjQiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NWQ0ZWQ5N2Y1MDU4YWQyNWEyOTFmZjgifQ.bhB8vm_ewPd31dtqcwJsLALgeKH1JJsYpIWt-LM3jsk",
        "profile_id": "65d4d997df2388620b554964",
        "port": random_port
	})
    debugger_address = gl.start()
    print(debugger_address)
    # gl.startRemote()
    # print(gl.startRemote())
    # await asyncio.sleep(10000)
    options = webdriver.ChromeOptions()
    options.debugger_address = debugger_address

    async with webdriver.Chrome(max_ws_size=2 ** 30, options=options) as driver:
        driver.base_target.socket.on_closed.append(lambda code, reason: print(f"chrome exited"))

        global_conn = driver.base_target
        await global_conn.execute_cdp_cmd("Fetch.enable",
                                          cmd_args={"patterns": [{"requestStage": "Response", "urlPattern": "*"}]}, timeout=3)
        await global_conn.add_cdp_listener("Fetch.requestPaused", lambda data: on_request(data, global_conn))

        await driver.get("https://hermes.com", timeout=60, wait_load=False)
        await asyncio.sleep(10)

        page_height_driver = await driver.execute_script("return document.documentElement.clientHeight")
        page_width_driver = await driver.execute_script("return document.documentElement.clientWidth")
        print(page_height_driver, page_width_driver)

        # print(page_height_driver, page_width_driver)

        pointer = await driver.current_pointer
        await pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))
        await pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))
        await pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))
        await pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))
        await pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))
        await pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))
        try:
            accept_cookies_button = await driver.find_element(By.CSS_SELECTOR, "button[id=\"onetrust-accept-btn-handler\"]")
            await accept_cookies_button.click(move_to=True)
        except:
            pass
        # await asyncio.sleep(1000)
        menu_pictures = await driver.find_elements(By.CSS_SELECTOR, "picture[class=\"media-wrap media-wrap-square\"]")
        print(len(menu_pictures))
        await driver.execute_script("arguments[0].scrollIntoView();", menu_pictures[1])
        await menu_pictures[random.randint(0, 7)].click(move_to=True)
        await asyncio.sleep(5)
        try:
            product = await driver.find_element(By.CSS_SELECTOR, "span[class=\"product-item-name\"]")
            await product.click(move_to=True)
        except:
            await asyncio.sleep(5)
            product = await driver.find_element(By.CSS_SELECTOR, "span[class=\"product-item-name\"]")
            await product.click(move_to=True)
        await asyncio.sleep(7)
        try:
            add_to_cart_button = await driver.find_element(By.CSS_SELECTOR, "button[data-testid=\"Add to cart\"]")
        except:
            try:
                await asyncio.sleep(7)
                product = await driver.find_element(By.CSS_SELECTOR, "span[class=\"product-item-name\"]")
                await product.click(move_to=True)
            except:
                pass

        while True:
            # time.sleep(10) # no. cloudflare would hang
            await asyncio.sleep(120)

            pointer = await driver.current_pointer
            await pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))
            await pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))
            await pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))
            await pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))
            await pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))
            await pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))

            partner_products_element = await driver.find_element(By.CSS_SELECTOR, "h-product-page-grid[id=\"product-page-cross-sell-perfect-partner\"]")
            partner_products = await partner_products_element.find_elements(By.TAG_NAME, "li")
            print(len(partner_products))
            await partner_products[random.randint(0, len(partner_products) - 1)].click(move_to=True)
            print("new product")


asyncio.run(main())