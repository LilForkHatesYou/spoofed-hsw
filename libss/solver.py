import tls_client, json, asyncio, base64, threading, re, json, time, requests, numpy as np, random, string
from colorama import Fore, Style
from playwright.async_api import async_playwright
from datetime import datetime
from .ais.hcaptcha import core
import urllib

class Solver():
    def __init__(self, siteKey:str, siteUrl:str,session:tls_client.Session, debug:bool=False) -> None:
        self.client =  session
        self.client.headers = {'authority': 'hcaptcha.com','accept': 'application/json','accept-language': 'en-US,en;q=0.9','content-type': 'text/plain','origin': 'https://newassets.hcaptcha.com','referer': 'https://newassets.hcaptcha.com/','sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'same-site','sec-gpc': '1','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',}
        self.version = re.findall(r'v1\/([A-Za-z0-9]+)\/static', self.client.get('https://hcaptcha.com/1/api.js?render=explicit&onload=hcaptchaOnLoad').text)[1]
        self.siteUrl = siteUrl
        self.siteKey = siteKey
        self.ai_submit = []
    def getHsw(self) -> str:
        return requests.get(f"http://127.0.0.1:3030/n?req={self.proofData['req']}", timeout=300).text 
    def checkSiteConfig(self) -> str:
        params = {'v': self.version,'host': self.siteUrl,'sitekey': self.siteKey,'sc': '1','swa': '1',}
        response = self.client.post('https://hcaptcha.com/checksiteconfig', params=params)
        if response.json()['pass']:
            return response.json()['c']
        else:
            return None
    def mouse_movement(self) -> str:
        x_movements = np.random.randint(15, 450, size=50)
        y_movements = np.random.randint(15, 450, size=50)
        times = np.round(time.time(), decimals=0)
        times_list = [times] * len(x_movements)
        movement = np.column_stack((x_movements, y_movements, times_list))
        return str(movement.tolist())
    
    def getCaptcha(self) -> dict:
        self.hsw = self.getHsw()
        ts = str(round(time.time()))[:8]
        mmData = self.mouse_movement()
        self.client.headers['content-type'] = 'application/x-www-form-urlencoded'
        response = self.client.post(f'https://hcaptcha.com/getcaptcha/{self.siteKey}',
            data={"v": self.version,"sitekey": self.siteKey,"host":  self.siteUrl,"hl": "fr","motionData":'{"st":1672758403488,"mm":mmdata,"mm-mp":19.62389380530976,"md":[[137,60,1672758472219]],"md-mp":0,"mu":[[137,60,1672758472323]],"mu-mp":0,"v":1,"topLevel":{"st":1672758402888,"sc":{"availWidth":1920,"availHeight":1040,"width":1920,"height":1080,"colorDepth":24,"pixelDepth":24,"availLeft":2560,"availTop":360,"onchange":null,"isExtended":true},"nv":{"vendorSub":"","productSub":"20030107","vendor":"Google Inc.","maxTouchPoints":0,"scheduling":{},"userActivation":{},"doNotTrack":null,"geolocation":{},"connection":{},"pdfViewerEnabled":true,"webkitTemporaryStorage":{},"hardwareConcurrency":12,"cookieEnabled":true,"appCodeName":"Mozilla","appName":"Netscape","appVersion":"5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36","platform":"Win32","product":"Gecko","userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36","language":"en-US","languages":["fr-FR","fr","en-US","en"],"onLine":true,"webdriver":false,"bluetooth":{},"clipboard":{},"credentials":{},"keyboard":{},"managed":{},"mediaDevices":{},"storage":{},"serviceWorker":{},"virtualKeyboard":{},"wakeLock":{},"deviceMemory":8,"ink":{},"hid":{},"locks":{},"mediaCapabilities":{},"mediaSession":{},"permissions":{},"presentation":{},"serial":{},"usb":{},"windowControlsOverlay":{},"xr":{},"userAgentData":{"brands":[{"brand":"Not?A_Brand","version":"8"},{"brand":"Chromium","version":"108"},{"brand":"Google Chrome","version":"108"}],"mobile":false,"platform":"Windows"},"plugins":["internal-pdf-viewer","internal-pdf-viewer","internal-pdf-viewer","internal-pdf-viewer","internal-pdf-viewer"]},"dr":"","inv":false,"exec":false,"wn":[],"wn-mp":0,"xy":[],"xy-mp":0,"mm":[[19,459,1672758467748],[271,582,1672758467764],[395,642,1672758467780],[447,666,1672758467796],[452,669,1672758467907],[457,674,1672758467923],[465,681,1672758467939],[472,689,1672758467957],[483,692,1672758467973],[498,693,1672758467989],[525,693,1672758468005],[575,699,1672758468021],[669,720,1672758468037],[797,751,1672758468053],[879,522,1672758471241],[809,527,1672758471257],[742,525,1672758471273],[675,520,1672758471289],[618,513,1672758471305],[564,506,1672758471321],[509,498,1672758471337],[458,491,1672758471353],[413,487,1672758471369],[379,486,1672758471385],[353,486,1672758471401],[39,525,1672758471616],[34,527,1672758471633],[34,529,1672758471736],[39,531,1672758471755],[47,533,1672758471772],[65,534,1672758471789],[90,537,1672758471805],[117,541,1672758471821],[138,544,1672758471838],[150,545,1672758471856],[155,545,1672758471872],[156,545,1672758471924],[158,545,1672758471949],[159,543,1672758471977],[160,542,1672758471995],[161,540,1672758472011],[163,537,1672758472029],[165,535,1672758472051],[166,533,1672758472067]],"mm-mp":21.897983392645333},"session":[],"widgetList":["0e0kbvh77qr"],"widgetId":"0e0kbvh77qr","href":"https://discord.com/","prev":{"escaped":false,"passed":false,"expiredChallenge":false,"expiredResponse":false}}'.replace("16727584", ts).replace('mmdata', mmData),"n": self.hsw,"c": json.dumps(self.proofData)}) 
        if 'key' not in response.json():
            self.proofData = response.json()['c']
            return {'error': 'Failed Getting Captcha'}
        return response.json()

    def predict(self) -> dict:
        self.hsw = self.getHsw()
        try:
            start = time.time()
            imgB64 = {str(i): base64.b64encode(requests.get(str(img["datapoint_uri"]), headers=self.client.headers).content).decode('utf-8') for i, img in enumerate(self.taskList)}
            task = requests.post(f'https://pro.nocaptchaai.com/solve', headers={'Content-type': 'application/json','apikey': 'lilfork-3741290e-8fff-3e94-f371-cf9ce642a6eb'},json={'images': imgB64,'target': self.question,'method': 'hcaptcha_base64','sitekey': self.siteKey,'site': self.siteUrl})
            self.solArray = task.json()['solution']
            print(f"({Fore.LIGHTBLUE_EX}!{Fore.RESET}) - Solution: {self.solArray} - {round(time.time()-start,2)}s")
            resp = [i in self.solArray for i in range(len(self.taskList))]
            return {task['task_key']: str(resp).lower() for task, resp in zip(self.taskList, resp)}
        except Exception as e:
            #print(e)
            pass

    def ai(self) -> dict:
        temp_tasks = []
        for u in self.taskList:
            url, task_key = str(u["datapoint_uri"]), str(u["task_key"])
            image = urllib.request.urlopen(url).read()
            temp_tasks.append([image, task_key])
        sex = str(self.question).replace("Please click each image containing an ", "").replace("Please click each image containing a ", "").strip(".")
        hc = core.ArmorCaptcha(label=sex)
        a = hc.challenge(temp_tasks)
        #print(a)
        return a
    
    def postAnswers(self) -> str:
        self.hsw = self.getHsw()
        self.client.headers = {'authority': 'hcaptcha.com','accept': '*/*','accept-language': 'en-US,en;q=0.9','content-type': 'application/json;charset=UTF-8','origin': 'https://newassets.hcaptcha.com','referer': 'https://newassets.hcaptcha.com/','sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'same-site','sec-gpc': '1',"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}
        response = self.client.post(f'https://hcaptcha.com/checkcaptcha/{self.siteKey}/{self.key}',json={'v': self.version,'job_mode': 'image_label_binary','answers': self.solution,'serverdomain': self.siteUrl,'sitekey': self.siteKey,"motionData": '{"st":1672758607913,"dct":1672758607913,"mm":mmdata,"mm-mp":4.306643952299827,"md":[[351,172,1672758611263],[93,302,1672758612354],[58,166,1672758614414],[80,454,1672758614980],[343,565,1672758615747]],"md-mp":1121,"mu":[[351,172,1672758611356],[93,302,1672758612470],[58,166,1672758614516],[80,454,1672758615042],[343,565,1672758615868]],"mu-mp":1128,"topLevel":{"st":1672758606002,"sc":{"availWidth":1920,"availHeight":1040,"width":1920,"height":1080,"colorDepth":24,"pixelDepth":24,"availLeft":2560,"availTop":360,"onchange":null,"isExtended":true},"nv":{"vendorSub":"","productSub":"20030107","vendor":"Google Inc.","maxTouchPoints":0,"scheduling":{},"userActivation":{},"doNotTrack":null,"geolocation":{},"connection":{},"pdfViewerEnabled":true,"webkitTemporaryStorage":{},"hardwareConcurrency":12,"cookieEnabled":true,"appCodeName":"Mozilla","appName":"Netscape","appVersion":"5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36","platform":"Win32","product":"Gecko","userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36","language":"en-US","languages":["fr-FR","fr","en-US","en"],"onLine":true,"webdriver":false,"bluetooth":{},"clipboard":{},"credentials":{},"keyboard":{},"managed":{},"mediaDevices":{},"storage":{},"serviceWorker":{},"virtualKeyboard":{},"wakeLock":{},"deviceMemory":8,"ink":{},"hid":{},"locks":{},"mediaCapabilities":{},"mediaSession":{},"permissions":{},"presentation":{},"serial":{},"usb":{},"windowControlsOverlay":{},"xr":{},"userAgentData":{"brands":[{"brand":"Not?A_Brand","version":"8"},{"brand":"Chromium","version":"108"},{"brand":"Google Chrome","version":"108"}],"mobile":false,"platform":"Windows"},"plugins":["internal-pdf-viewer","internal-pdf-viewer","internal-pdf-viewer","internal-pdf-viewer","internal-pdf-viewer"]},"dr":"","inv":false,"exec":false,"wn":[[880,924,1,1672758606002]],"wn-mp":0,"xy":[[0,0,1,1672758606003]],"xy-mp":0,"mm":[[879,684,1672758606557],[803,680,1672758606573],[727,674,1672758606589],[660,670,1672758606605],[607,666,1672758606621],[567,661,1672758606637],[541,656,1672758606653],[525,653,1672758606669],[513,651,1672758606687],[501,650,1672758606703],[489,648,1672758606719],[477,648,1672758606735],[463,647,1672758606752],[449,646,1672758606768],[438,644,1672758606784],[427,643,1672758606801],[415,641,1672758606818],[402,640,1672758606835],[387,639,1672758606853],[373,637,1672758606869],[361,635,1672758606885],[345,634,1672758606902],[327,632,1672758606919],[311,629,1672758606935],[298,627,1672758606952],[286,625,1672758606969],[272,622,1672758606986],[260,618,1672758607002],[251,615,1672758607020],[243,611,1672758607037],[230,603,1672758607053],[209,591,1672758607069],[186,576,1672758607085],[168,562,1672758607101],[154,550,1672758607118],[143,536,1672758607134],[125,496,1672758608067],[96,458,1672758614148],[96,419,1672758614164],[407,789,1672758615149],[443,809,1672758615165],[461,820,1672758615182],[470,824,1672758615198],[478,825,1672758615216],[489,826,1672758615232],[501,827,1672758615248],[512,828,1672758615265],[518,827,1672758615282],[520,826,1672758615339],[520,825,1672758615358],[518,822,1672758615376],[517,818,1672758615393],[515,817,1672758615410],[512,814,1672758615429],[507,810,1672758615446],[501,805,1672758615463],[497,802,1672758615479],[494,800,1672758615496],[490,797,1672758615513],[484,793,1672758615530],[477,790,1672758615546]],"mm-mp":13.799079754601225},"v":1}'.replace("1672758", str(round(datetime.now().timestamp()))[:7]).replace('mmdata', str(self.mouse_movement())),'n': self.hsw,'c': json.dumps(self.proofData)},)       
        #print(response.text)
        if 'generated_pass_UUID' in response.json():
            return response.json()['generated_pass_UUID']
        else: 
            return None
    def solve(self) -> str:
        startedAs = time.time()
        self.proofData = self.checkSiteConfig()
        if self.proofData == None:
            return 'Failed Site Check'
        #print(f"({Fore.LIGHTBLUE_EX}!{Fore.RESET}) - Passed Check Site Config")
        self.hsw = self.getHsw()
        captcha = self.getCaptcha()
        if 'error' in captcha: 
            pass
            #print(f"({Fore.LIGHTBLUE_EX}!{Fore.RESET}) - Error: {captcha['error']}")
        else:
            self.proofData = captcha['c']
            self.key       = captcha['key']
            self.taskList  = captcha['tasklist']
            self.question  = captcha['requester_question']['en']
        #print(f"({Fore.LIGHTBLUE_EX}!{Fore.RESET}) - Solving: {self.question}")
        #self.solution = self.ai()
        self.solution = self.predict()
        self.hsw = self.getHsw()
        captchaKey = self.postAnswers()
        if captchaKey == None:
            #print(f"({Fore.LIGHTBLUE_EX}!{Fore.RESET}) - Failed Captcha")
            pass
        else:
            print(f"({Fore.LIGHTBLACK_EX}#{Fore.RESET}) - Solved [{round(time.time()-startedAs,2)}s]: [{captchaKey[:42]}]")
            return captchaKey