import asyncio
import base64
import hashlib
import json
import random
import re
import secrets
import string
import time
import typing
import uuid
from datetime import datetime

import aiomisc
import httpx
import nopecha
import numpy as np
import requests
import tls_client
from playwright.async_api import async_playwright
from redis import Redis

nopecha.api_key = "slx9du0do2_5RZ2F3RL"

database = Redis(host="85.202.203.139", password="jew1339", port=6379, db=8)
workers: list[typing.Union["BrowserHSWEngine"]] = []
version = re.findall(r'v1/([A-Za-z0-9]+)/static', httpx.get(
    'https://hcaptcha.com/1/api.js?render=explicit&onload=hcaptchaOnLoad').text)[1]


class Tile(object):
    image_id: str
    image_index: int
    image_content: bytes

    def __init__(self, image_id: str, image_index: int, image_content: bytes):
        self.selected = False
        self.image_id = image_id
        self.image_content = image_content
        self.image_index = image_index


__CONFIG__ = json.loads(open("config.json").read())
auth_token = __CONFIG__["anty-token"]


class Anty:
    def __init__(self) -> None:
        self.session = requests.Session()

    def login(self) -> None:
        self.session.headers.update({'Authorization': f'Bearer {auth_token}'})

    def create_profile_and_send_id(self):
        payload = json.dumps({
            "name": "browser",
            "platform": "linux",
            "browserType": "anty",
            "mainWebsite": "none",
            "doNotTrack": 1,
            "ports": {
                "mode": "real"
            },
            "useragent": {
                "mode": "manual",
                "value": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
            },
            "webrtc": {
                "mode": "modified"
            },
            "canvas": {
                "mode": "noise"
            },
            "webgl": {
                "mode": "noise"
            },
            "webglInfo": {
                "mode": "real"
            },
            "geolocation": {
                "mode": "auto",
            },
            "cpu": {
                "mode": "manual",
                "value": 8
            },
            "memory": {
                "mode": "manual",
                "value": 8
            },
            "timezone": {
                "mode": "auto",
                "value": None
            },
            "locale": {
                "mode": "auto",
                "value": None
            }
        })
        response = self.session.post('https://anty-api.com/browser_profiles', data=payload,
                                     headers={'Content-Type': 'application/json',
                                              'Authorization': f'Bearer {auth_token}'})
        return response.json()['browserProfileId']

    def start_browser(self, profile_id: str):
        response = self.session.get(
            f"http://localhost:3001/v1.0/browser_profiles/{profile_id}/start?automation=1").json()
        return response['automation']


class BrowserHSWEngine:
    def __init__(self) -> None:
        self.context = None
        self.page = None
        self.agent = None
        self.frame = None
        self.browser = None
        self.refresh_iter = 0
        self.playwright = None
        self.first_time = True
        self.worker_id = uuid.uuid4()

    async def main(self) -> None:
        print(f"(DEBUG) - Starting Browser Spoofer in HSW mode (Worker ID: {self.worker_id})")
        self.playwright = await async_playwright().start()
        anty = Anty()
        anty_id = anty.create_profile_and_send_id()
        anty_browser = anty.start_browser(anty_id)
        self.browser = await self.playwright.chromium.connect_over_cdp(f"ws://127.0.0.1:{anty_browser['port']}{anty_browser['wsEndpoint']})")
        self.context = self.browser.contexts[0]
        self.page = self.context.pages[0]
        await self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', undefined);
        """)
        await self.visit_discord()
        await self.get_hsw_iframe()

    async def pull_hsw(self, rq_token: str):
        return await self.frame.evaluate(f'hsw("{rq_token}")')

    @staticmethod
    async def handle(route):
        response = await route.fetch()
        json = {
            "captcha_key": [
                "captcha-required"
            ],
            "captcha_sitekey": "4c672d35-0701-42b2-88c3-78380b0db560",
            "captcha_service": "hcaptcha"
        }
        await route.fulfill(status=400, response=response, json=json)

    @staticmethod
    async def handle2(route):
        response = await route.fetch()
        json = {
            "c": {
                "type": "hsw",
                "req": secrets.token_hex(16)
            }
        }
        await route.fulfill(status=200, response=response, json=json)

    async def visit_discord(self) -> None:
        await self.page.route("https://discord.com/api/v9/auth/register**", self.handle)
        await self.page.route("https://hcaptcha.com/checksiteconfig**", self.handle2)
        await self.page.goto('https://discord.com/')
        await self.page.wait_for_load_state('domcontentloaded')
        await self.page.click('[class *= "gtm-click-class-open-button"]')
        await self.page.type('[class *= "username"]', ''.join(random.choice(string.ascii_letters) for _ in range(15)))
        try:
            await self.page.click("[class *= 'checkbox']", timeout=100)
        except Exception:
            pass
        await self.page.click('[class *= "gtm-click-class-register-button"]')

    async def get_hsw_iframe(self) -> None:
        found = False
        while not found:
            await self.page.wait_for_timeout(1000)
            for frame in self.page.frames:
                try:
                    try:
                        await frame.evaluate('document.querySelector("#checkbox").click()')
                    except Exception:
                        pass
                    await frame.evaluate(f"hsw('XD');")
                except Exception as ex:
                    if 'Token is invalid' in str(ex):
                        self.frame = frame
                        print(f"(DEBUG) - Successfully Spoofed (Worker ID: {self.worker_id})")
                        found = True


class Solver:
    def __init__(self, site_key: str, site_url: str, session: tls_client.Session, hsl: bool = False,
                 debug: bool = False) -> None:
        self.solution = None
        self.hsw = None
        self.question = None
        self.task_list = None
        self.key = None
        self.proof_data = None
        self._hsl = hsl
        self.debug = debug
        self.client = session
        self.client2 = httpx.AsyncClient(timeout=900)
        self.client.headers = {'authority': 'hcaptcha.com', 'accept': 'application/json',
                               'accept-language': 'en-US,en;q=0.9', 'content-type': 'text/plain',
                               'origin': 'https://newassets.hcaptcha.com', 'referer': 'https://newassets.hcaptcha.com/',
                               'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site',
                               'sec-gpc': '1',
                               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36', }
        self.site_url = site_url
        self.site_key = site_key

    @staticmethod
    async def create_browser():
        browser = BrowserHSWEngine()
        await browser.main()
        workers.append(browser)

    @staticmethod
    async def setup():
        tasks = []
        for i in range(5):
            tasks.append(asyncio.create_task(Solver.create_browser()))
        for x in tasks:
            await x

    async def get_hsw(self) -> str:
        hsw_dat: str = await random.choice(workers).pull_hsw(self.proof_data['req'])
        return hsw_dat

    async def check_site_config(self) -> typing.Union[str, None]:
        params = {'v': version, 'host': self.site_url, 'sitekey': self.site_key, 'sc': '1', 'swa': '1'}
        response = await self.client.post('https://hcaptcha.com/checksiteconfig', params=params)
        if response.json()['pass']:
            return response.json()['c']
        else:
            return None

    @staticmethod
    @aiomisc.threaded_separate
    def mouse_movement() -> str:
        x_movements = np.random.randint(15, 450, size=50)
        y_movements = np.random.randint(15, 450, size=50)
        times = np.round(time.time(), 0)
        times_list = [times] * len(x_movements)
        movement = np.column_stack((x_movements, y_movements, times_list))
        return str(movement.tolist())

    async def get_captcha(self) -> dict:
        ts = str(round(time.time()))[:8]
        mm_data = await self.mouse_movement()
        self.client.headers['content-type'] = 'application/x-www-form-urlencoded'
        response = await self.client.post(f'https://hcaptcha.com/getcaptcha/{self.site_key}',
                                          data={"v": version, "sitekey": self.site_key, "host": self.site_url,
                                                "hl": "en",
                                                "motionData": '{"st":1672758403488,"mm":mmdata,"mm-mp":19.62389380530976,"md":[[137,60,1672758472219]],"md-mp":0,"mu":[[137,60,1672758472323]],"mu-mp":0,"v":1,"topLevel":{"st":1672758402888,"sc":{"availWidth":1920,"availHeight":1040,"width":1920,"height":1080,"colorDepth":24,"pixelDepth":24,"availLeft":2560,"availTop":360,"onchange":null,"isExtended":true},"nv":{"vendorSub":"","productSub":"20030107","vendor":"Google Inc.","maxTouchPoints":0,"scheduling":{},"userActivation":{},"doNotTrack":null,"geolocation":{},"connection":{},"pdfViewerEnabled":true,"webkitTemporaryStorage":{},"hardwareConcurrency":12,"cookieEnabled":true,"appCodeName":"Mozilla","appName":"Netscape","appVersion":"5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36","platform":"Win32","product":"Gecko","userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36","language":"en-US","languages":["fr-FR","fr","en-US","en"],"onLine":true,"webdriver":false,"bluetooth":{},"clipboard":{},"credentials":{},"keyboard":{},"managed":{},"mediaDevices":{},"storage":{},"serviceWorker":{},"virtualKeyboard":{},"wakeLock":{},"deviceMemory":8,"ink":{},"hid":{},"locks":{},"mediaCapabilities":{},"mediaSession":{},"permissions":{},"presentation":{},"serial":{},"usb":{},"windowControlsOverlay":{},"xr":{},"userAgentData":{"brands":[{"brand":"Not?A_Brand","version":"8"},{"brand":"Chromium","version":"108"},{"brand":"Google Chrome","version":"108"}],"mobile":false,"platform":"Windows"},"plugins":["internal-pdf-viewer","internal-pdf-viewer","internal-pdf-viewer","internal-pdf-viewer","internal-pdf-viewer"]},"dr":"","inv":false,"exec":false,"wn":[],"wn-mp":0,"xy":[],"xy-mp":0,"mm":[[19,459,1672758467748],[271,582,1672758467764],[395,642,1672758467780],[447,666,1672758467796],[452,669,1672758467907],[457,674,1672758467923],[465,681,1672758467939],[472,689,1672758467957],[483,692,1672758467973],[498,693,1672758467989],[525,693,1672758468005],[575,699,1672758468021],[669,720,1672758468037],[797,751,1672758468053],[879,522,1672758471241],[809,527,1672758471257],[742,525,1672758471273],[675,520,1672758471289],[618,513,1672758471305],[564,506,1672758471321],[509,498,1672758471337],[458,491,1672758471353],[413,487,1672758471369],[379,486,1672758471385],[353,486,1672758471401],[39,525,1672758471616],[34,527,1672758471633],[34,529,1672758471736],[39,531,1672758471755],[47,533,1672758471772],[65,534,1672758471789],[90,537,1672758471805],[117,541,1672758471821],[138,544,1672758471838],[150,545,1672758471856],[155,545,1672758471872],[156,545,1672758471924],[158,545,1672758471949],[159,543,1672758471977],[160,542,1672758471995],[161,540,1672758472011],[163,537,1672758472029],[165,535,1672758472051],[166,533,1672758472067]],"mm-mp":21.897983392645333},"session":[],"widgetList":["0e0kbvh77qr"],"widgetId":"0e0kbvh77qr","href":"https://discord.com/","prev":{"escaped":false,"passed":false,"expiredChallenge":false,"expiredResponse":false}}'.replace(
                                                    "16727584", ts).replace('mmdata', mm_data), "n": self.hsw,
                                                "c": json.dumps(self.proof_data)})
        if 'key' not in response.json():
            self.proof_data = response.json()['c']
            return {'error': 'Failed Getting Captcha'}
        return response.json()

    async def post_answers(self) -> typing.Union[str, None]:
        self.client.headers = {'authority': 'hcaptcha.com', 'accept': '*/*', 'accept-language': 'en-US,en;q=0.9',
                               'content-type': 'application/json;charset=UTF-8',
                               'origin': 'https://newassets.hcaptcha.com', 'referer': 'https://newassets.hcaptcha.com/',
                               'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site',
                               'sec-gpc': '1',
                               "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}
        response = await self.client.post(f'https://hcaptcha.com/checkcaptcha/{self.site_key}/{self.key}',
                                          json={'v': version, 'job_mode': 'image_label_binary',
                                                'answers': self.solution,
                                                'serverdomain': self.site_url, 'sitekey': self.site_key,
                                                "motionData": '{"st":1672758607913,"dct":1672758607913,"mm":mmdata,"mm-mp":4.306643952299827,"md":[[351,172,1672758611263],[93,302,1672758612354],[58,166,1672758614414],[80,454,1672758614980],[343,565,1672758615747]],"md-mp":1121,"mu":[[351,172,1672758611356],[93,302,1672758612470],[58,166,1672758614516],[80,454,1672758615042],[343,565,1672758615868]],"mu-mp":1128,"topLevel":{"st":1672758606002,"sc":{"availWidth":1920,"availHeight":1040,"width":1920,"height":1080,"colorDepth":24,"pixelDepth":24,"availLeft":2560,"availTop":360,"onchange":null,"isExtended":true},"nv":{"vendorSub":"","productSub":"20030107","vendor":"Google Inc.","maxTouchPoints":0,"scheduling":{},"userActivation":{},"doNotTrack":null,"geolocation":{},"connection":{},"pdfViewerEnabled":true,"webkitTemporaryStorage":{},"hardwareConcurrency":12,"cookieEnabled":true,"appCodeName":"Mozilla","appName":"Netscape","appVersion":"5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36","platform":"Win32","product":"Gecko","userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36","language":"en-US","languages":["fr-FR","fr","en-US","en"],"onLine":true,"webdriver":false,"bluetooth":{},"clipboard":{},"credentials":{},"keyboard":{},"managed":{},"mediaDevices":{},"storage":{},"serviceWorker":{},"virtualKeyboard":{},"wakeLock":{},"deviceMemory":8,"ink":{},"hid":{},"locks":{},"mediaCapabilities":{},"mediaSession":{},"permissions":{},"presentation":{},"serial":{},"usb":{},"windowControlsOverlay":{},"xr":{},"userAgentData":{"brands":[{"brand":"Not?A_Brand","version":"8"},{"brand":"Chromium","version":"108"},{"brand":"Google Chrome","version":"108"}],"mobile":false,"platform":"Windows"},"plugins":["internal-pdf-viewer","internal-pdf-viewer","internal-pdf-viewer","internal-pdf-viewer","internal-pdf-viewer"]},"dr":"","inv":false,"exec":false,"wn":[[880,924,1,1672758606002]],"wn-mp":0,"xy":[[0,0,1,1672758606003]],"xy-mp":0,"mm":[[879,684,1672758606557],[803,680,1672758606573],[727,674,1672758606589],[660,670,1672758606605],[607,666,1672758606621],[567,661,1672758606637],[541,656,1672758606653],[525,653,1672758606669],[513,651,1672758606687],[501,650,1672758606703],[489,648,1672758606719],[477,648,1672758606735],[463,647,1672758606752],[449,646,1672758606768],[438,644,1672758606784],[427,643,1672758606801],[415,641,1672758606818],[402,640,1672758606835],[387,639,1672758606853],[373,637,1672758606869],[361,635,1672758606885],[345,634,1672758606902],[327,632,1672758606919],[311,629,1672758606935],[298,627,1672758606952],[286,625,1672758606969],[272,622,1672758606986],[260,618,1672758607002],[251,615,1672758607020],[243,611,1672758607037],[230,603,1672758607053],[209,591,1672758607069],[186,576,1672758607085],[168,562,1672758607101],[154,550,1672758607118],[143,536,1672758607134],[125,496,1672758608067],[96,458,1672758614148],[96,419,1672758614164],[407,789,1672758615149],[443,809,1672758615165],[461,820,1672758615182],[470,824,1672758615198],[478,825,1672758615216],[489,826,1672758615232],[501,827,1672758615248],[512,828,1672758615265],[518,827,1672758615282],[520,826,1672758615339],[520,825,1672758615358],[518,822,1672758615376],[517,818,1672758615393],[515,817,1672758615410],[512,814,1672758615429],[507,810,1672758615446],[501,805,1672758615463],[497,802,1672758615479],[494,800,1672758615496],[490,797,1672758615513],[484,793,1672758615530],[477,790,1672758615546]],"mm-mp":13.799079754601225},"v":1}'.replace(
                                                    "1672758", str(round(datetime.now().timestamp()))[:7]).replace(
                                                    'mmdata',
                                                    str(await self.mouse_movement())),
                                                'n': self.hsw, 'c': json.dumps(self.proof_data)}, )
        if 'generated_pass_UUID' in response.json():
            return response.json()['generated_pass_UUID']
        else:
            return None

    @aiomisc.threaded_separate
    def so(self):
        temp_tasks = []
        for u in self.task_list:
            url, task_key = str(u["datapoint_uri"]), str(u["task_key"])
            temp_tasks.append(url)
        clicks = nopecha.Recognition.solve(
            type='hcaptcha',
            task=self.question,
            image_urls=temp_tasks
        )
        return {task['task_key']: str(resp).lower() for task, resp in zip(self.task_list, clicks)}

    @aiomisc.threaded_separate
    def sol_redis(self):
        tiles = [
            Tile(info.get("task_key"), index, (
                httpx.get(info.get("datapoint_uri"), headers={
                    "Accept-Encoding": "gzip"
                })).content)
            for index, info in enumerate(self.task_list)
        ]
        question_hash = hashlib.sha1(self.question.encode()).hexdigest()
        for tile in tiles:
            image_hash = hashlib.sha1(tile.image_content).hexdigest()
            tile.custom_id = f"{(base64.b64encode(b'HCaptcha Enterprise')).decode()}|" \
                             f"{question_hash}|{image_hash}"
            tile.score = int(database.get(tile.custom_id) or 0)
        tiles.sort(
            key=lambda _tile: _tile.score or random.uniform(0, 0.97),
            reverse=True)
        n_answers = max(3,
                        len(list(filter(lambda t: t.score >= 1, tiles))))
        for index in range(n_answers):
            tile = tiles[index]
            tile.selected = True
        solution = {
            tile.image_id: "true" if tile.selected else "false" for tile in tiles
        }
        return solution, tiles

    @aiomisc.threaded_separate
    def update_redis(self, tiles):
        for tile in tiles:
            if not tile.selected:
                continue
            database.incrbyfloat(tile.custom_id, 1)

    @aiomisc.threaded_separate
    def predict(self) -> dict:
        try:
            base64_img = {str(i): base64.b64encode(
                requests.get(str(img["datapoint_uri"]), headers=self.client.headers).content).decode('utf-8') for i, img
                          in enumerate(self.task_list)}
            task = requests.post(f'https://pro.nocaptchaai.com/solve', headers={
                'Content-type': 'application/json',
                'apikey': 'rorm-ec5766a4-b520-ae85-510b-6d240abd7454'
            }, json={
                'images': base64_img,
                'target': self.question,
                'method': 'hcaptcha_base64',
                'sitekey': self.site_key,
                'site': self.site_url
            })
            sol_array = task.json()['solution']
            resp = [i in sol_array for i in range(len(self.task_list))]
            return {task['task_key']: str(resp).lower() for task, resp in zip(self.task_list, resp)}
        except Exception:
            pass

    async def solve(self) -> str:
        self.proof_data = await self.check_site_config()
        if self.proof_data is None:
            return 'Failed Site Check'
        self.hsw = await self.get_hsw()
        captcha = await self.get_captcha()
        if 'error' in captcha:
            pass
        else:
            self.proof_data = captcha['c']
            self.key = captcha['key']
            self.task_list = captcha['tasklist']
            self.question = captcha['requester_question']['en']
        # self.solution, tiles = await self.sol_redis()
        self.solution = await self.predict()
        self.hsw = await self.get_hsw()
        token: str = await self.post_answers()
        if token:
            print(f"[!] Solved: [{token[:42]}]")
            # await self.update_redis(tiles)
            return token
