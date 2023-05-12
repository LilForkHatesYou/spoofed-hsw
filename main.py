import tls_client, json, websocket, random, base64, threading, re, os, time, requests, httpx
from colorama import Fore, Style
from datetime import timedelta
# from libss.solver import Solver, Browser
from libss.solver import Solver
import traceback

config = json.loads(open('config.json', 'r').read())
names = open('input/names.txt', "r", encoding="utf-8").read().splitlines()
proxies = open('input/proxies.txt', "r", encoding="utf-8").read().splitlines()
proxy_pool = []
for proxy in proxies:
    proxy = proxy.rstrip()
    ip, port, user, password = proxy.split(':')
    proxy_pool.append(f'{user}:{password}@{ip}:{port}')
threadList = []
locked, unlocked, total = 0, 0, 0


def updateTitle():
    genStartedAs = time.time()
    while True:
        try:
            delta = timedelta(seconds=round(time.time() - genStartedAs))
            elapsed = str(delta).split(".")[0]
            unlocked_rate = round(unlocked / total * 100, 2)
            upm = round(unlocked / ((time.time() - genStartedAs) / 60))
            os.system(
                f'title UNLOCKED: {unlocked} │ LOCKED: {locked} │ Rate: {unlocked_rate}% │ UPM: {upm} │ Elapsed: {elapsed}')
        except Exception:
            pass
        time.sleep(1)


def split_invite(invite):
    if invite.__contains__("discord.gg"):
        if invite.startswith("https://"):
            return invite.split("/")[3]
        else:
            return invite.split("/")[1]
    else:
        return invite


class Discord():
    def __init__(self) -> None:
        global total
        global locked
        global unlocked
        self.session = tls_client.Session(
            client_identifier="chrome_111",
            random_tls_extension_order=True,
            h2_settings={"HEADER_TABLE_SIZE": 65536, "MAX_CONCURRENT_STREAMS": 1000, "INITIAL_WINDOW_SIZE": 6291456,
                         "MAX_HEADER_LIST_SIZE": 262144},
            h2_settings_order=["HEADER_TABLE_SIZE", "MAX_CONCURRENT_STREAMS", "INITIAL_WINDOW_SIZE",
                               "MAX_HEADER_LIST_SIZE"],
            supported_signature_algorithms=["ECDSAWithP256AndSHA256", "PSSWithSHA256", "PKCS1WithSHA256",
                                            "ECDSAWithP384AndSHA384", "PSSWithSHA384", "PKCS1WithSHA384",
                                            "PSSWithSHA512", "PKCS1WithSHA512", ],
            supported_versions=["GREASE", "1.3", "1.2"],
            key_share_curves=["GREASE", "X25519"],
            cert_compression_algo="brotli",
            pseudo_header_order=[":method", ":authority", ":scheme", ":path"],
            connection_flow=15663105,
            header_order=["accept", "user-agent", "accept-encoding", "accept-language"])
        self.proxy = "http://" + random.choice(proxy_pool)
        self.session.proxies = {"http": self.proxy, "https": self.proxy}
        self.prop = {
            "os": "Windows",
            "browser": "Chrome",
            "device": "",
            "system_locale": "en-US",
            "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "browser_version": "111.0.0.0",
            "os_version": "10",
            "referrer": "",
            "referring_domain": "",
            "referrer_current": "",
            "referring_domain_current": "",
            "release_channel": "stable",
            "client_build_number": self.build_number(),
            "client_event_source": None,
            "design_id": 0
        }
        self.super = base64.b64encode(json.dumps(self.prop, separators=(',', ':')).encode()).decode()

    def build_number(self):
        res = requests.get("https://discord.com/login").text
        file_with_build_num = 'https://discord.com/assets/' + \
                              re.compile(r'assets/+([a-z0-9]+)\.js').findall(res)[-2] + '.js'
        req_file_build = requests.get(file_with_build_num).text
        index_of_build_num = req_file_build.find('buildNumber') + 24
        return int(req_file_build[index_of_build_num:index_of_build_num + 6])

    def getFingerprint(self) -> str:
        response = self.session.get('https://discord.com/api/v9/experiments')
        self.session.cookies.update(response.cookies)
        self.session.cookies.update({"locale": "fr"})
        return response.json()['fingerprint']

    def createAccount(self, captchaKey: str, fingerprint: str) -> str:
        global total
        global locked
        global unlocked
        self.session.headers = {
            'authority': 'discord.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'referer': 'https://discord.com/',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
            'x-fingerprint': fingerprint,
            'x-track': 'eyJvcyI6IkxpbnV4IiwiYnJvd3NlciI6IkZpcmVmb3giLCJkZXZpY2UiOiIiLCJzeXN0ZW1fbG9jYWxlIjoiZW4tVVMiLCJicm93c2VyX3VzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0OyBydjo5MS4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzkxLjAiLCJicm93c2VyX3ZlcnNpb24iOiI5MS4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjk5OTksImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9',
        }
        response = self.session.post('https://discord.com/api/v9/auth/register',
                                     json={
                                         'consent': True,
                                         'fingerprint': fingerprint,
                                         'invite': split_invite(invite),
                                         'username': random.choice(names),
                                         'captcha_key': captchaKey
                                     }
                                     )
        if not 'token' in response.json():
            print(f"({Fore.RED}-{Style.RESET_ALL}) - Rate Limited")
            return None
        return response.json()['token']

    def generate(self) -> None:
        global total
        global locked
        global unlocked
        solver = Solver(siteUrl='discord.com', siteKey='4c672d35-0701-42b2-88c3-78380b0db560', session=self.session)
        captchaKey = solver.solve()
        while captchaKey == None:
            captchaKey = solver.solve()
        self.session.headers = {
            'authority': 'discord.com',
            'accept': '*/*',
            'accept-language': 'en-US,fr;q=0.9',
            'cookie': 'locale=fr',
            'referer': 'https://discord.com/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
            'x-track': 'eyJvcyI6IkxpbnV4IiwiYnJvd3NlciI6IkZpcmVmb3giLCJkZXZpY2UiOiIiLCJzeXN0ZW1fbG9jYWxlIjoiZW4tVVMiLCJicm93c2VyX3VzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0OyBydjo5MS4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzkxLjAiLCJicm93c2VyX3ZlcnNpb24iOiI5MS4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjk5OTksImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9',
        }
        fingerprint = self.getFingerprint()
        self.fingerprint = fingerprint
        token = self.createAccount(captchaKey, fingerprint)
        if token == None:
            return
        self.session.headers.pop('x-track')
        self.session.headers['referer'] = 'https://discord.com/channels/@me'
        self.session.headers.update({
            'x-super-properties': self.super,
            'x-discord-locale': 'fr',
            'x-debug-options': 'bugReporterEnabled',
            'authorization': token
        })
        if self.session.get('https://discord.com/api/v9/users/@me/affinities/users').status_code == 403:
            total += 1
            locked += 1
            print(f"({Fore.RED}-{Style.RESET_ALL}) - Locked [{token[:30]}*************************]")
            return
        total += 1
        self.session.proxies = {"http": self.proxy, "https": self.proxy}
        # self.session.proxies = {"http": None, "https": None}
        ws = websocket.WebSocket()
        ws.connect('wss://gateway.discord.gg/?encoding=json&v=9')
        ws.send(json.dumps({
            "op": 2,
            "d": {
                "token": token,
                "capabilities": 4093,
                "properties": self.prop,
                "presence": {
                    "status": "dnd",
                    "since": 0,
                    "activities": [
                        {
                            "name": "to Lil Fork",
                            "type": 2
                        }
                    ],
                    "afk": False
                },
                "compress": False,
                "client_state": {
                    "guild_versions": {},
                    "highest_last_message_id": "0",
                    "read_state_version": 0,
                    "user_guild_settings_version": -1,
                    "user_settings_version": -1,
                    "private_channels_version": "0",
                    "api_code_version": 0
                }
            }
        }))
        added = ""
        json_data = {'date_of_birth': '2000-12-19', 'avatar': 'data:image/png;base64,' + base64.b64encode(open(
            os.path.join("input/image", random.choice(
                [f for f in os.listdir("input/image") if f.endswith('.jpg') or f.endswith('.png')])),
            'rb').read()).decode('utf-8')}
        added += "Avatar, "
        response = self.session.patch('https://discord.com/api/v9/users/@me', json=json_data)
        if response.status_code == 200:
            added += "BirthDate, "
        response = self.session.post('https://discord.com/api/v9/hypesquad/online',
                                     json={'house_id': random.randint(1, 3)})
        if response.status_code == 204:
            added += "Hypesquad, "
        bio = random.choice(open('input/bios.txt', 'r', encoding="utf-8").read().splitlines())
        response = self.session.patch('https://discord.com/api/v9/users/%40me/profile', json={'bio': bio})
        if response.status_code == 200:
            added += "Bio "
        unlocked += 1
        open('tokens.txt', 'a').write(f'{token}\n')
        ws.close()
        print(f"({Fore.GREEN}+{Style.RESET_ALL}) - Unlocked [{token[:30]}*************************]")
        print(f"({Fore.MAGENTA}~{Style.RESET_ALL}) - Humanized: {added}")


# def setupBrowser() -> None:
#    browser = Browser()
#    browser.setup()
#    browserList.append(browser)

def generate() -> None:
    global total
    global locked
    global unlocked
    while True:
        try:
            discord = Discord()
            discord.generate()
        except Exception as e:
            # traceback.print_exc()
            # print(f"({Fore.RED}-{Style.RESET_ALL}) - Error [{e}")
            pass


if __name__ == "__main__":
    os.system('cls')
    # setupBrowser()
    invite = input(f'({Fore.LIGHTMAGENTA_EX}~{Fore.RESET}) - Invite (Leave Blank For None) → ')
    for i in range(int(input(f'({Fore.LIGHTMAGENTA_EX}~{Fore.RESET}) - Threads → '))):
        threading.Thread(target=generate).start()
    threading.Thread(target=updateTitle).start()
