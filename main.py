import asyncio
import base64
import json
import os
import random
import re
import secrets
import sys
import threading
import time
from datetime import timedelta
from typing import Union

import aiomisc
import requests
import tls_client
import websocket
from colorama import Fore

from solver import Solver

names = open('input/names.txt', "r", encoding="utf-8").read().splitlines()
proxies = open('input/proxies.txt', "r", encoding="utf-8").read().splitlines()
proxy_pool = []
for proxy in proxies:
    proxy = proxy.rstrip()
    ip, port, user, password = proxy.split(':')
    proxy_pool.append(f'{user}:{password}@{ip}:{port}')
threadList = []
locked, unlocked, total = 0, 0, 0


class Nigger(tls_client.Session):
    @aiomisc.threaded_separate
    def execute_request(self, *args, **kwargs):
        for _ in range(100):
            try:
                return super().execute_request(*args, **kwargs)
            except Exception as ex:
                pass


def update_title():
    gen_started_at = time.time()
    while True:
        try:
            unlocked_rate = round(unlocked / total * 100, 2)
            upm = round(unlocked / ((time.time() - gen_started_at) / 60))
            sys.stdout.write(f'\x1b]2;{unlocked} UNLOCKED │ {locked} LOCKED │ {unlocked_rate}% RATE │ {upm} UPM\x07')
            sys.stdout.flush()
        except Exception:
            pass
        time.sleep(1)


def split_invite(__invite__):
    if __invite__.__contains__("discord.gg"):
        if __invite__.startswith("https://"):
            return __invite__.split("/")[3]
        else:
            return __invite__.split("/")[1]
    else:
        return __invite__


def build_number():
    res = requests.get("https://discord.com/login").text
    file_with_build_num = 'https://discord.com/assets/' + \
                          re.compile(r'assets/+([a-z0-9]+)\.js').findall(res)[-2] + '.js'
    req_file_build = requests.get(file_with_build_num).text
    index_of_build_num = req_file_build.find('buildNumber') + 24
    return int(req_file_build[index_of_build_num:index_of_build_num + 6])


version = build_number()


class Discord:
    def __init__(self) -> None:
        global total
        global locked
        global unlocked
        self.fingerprint = None
        self.proxy = "http://" + random.choice(proxy_pool)
        self.session = Nigger(
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
        self.session.proxies = self.proxy
        self.prop = {
            "os": "Windows",
            "browser": "Chrome",
            "device": "",
            "system_locale": "en-US",
            "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "browser_version": "115.0.0.0",
            "os_version": "10",
            "referrer": "",
            "referring_domain": "",
            "referrer_current": "",
            "referring_domain_current": "",
            "release_channel": "stable",
            "client_build_number": version,
            "client_event_source": None,
            "design_id": 0
        }
        self.super = base64.b64encode(json.dumps(self.prop, separators=(',', ':')).encode()).decode()

    async def get_fingerprint(self) -> str:
        response = await self.session.get('https://discord.com/api/v9/experiments')
        self.session.cookies.update(response.cookies)
        self.session.cookies.update({"locale": "fr"})
        return response.json()['fingerprint']

    async def create_account(self, captcha_key: str, fingerprint: str) -> Union[str, None]:
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
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'x-fingerprint': fingerprint,
            'x-track': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExNS4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTE1LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjk5OTksImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9',
        }
        response = await self.session.post('https://discord.com/api/v9/auth/register',
                                           json={
                                               'consent': True,
                                               'fingerprint': fingerprint,
                                               "invite": None,
                                               'username': random.choice(names),
                                               'captcha_key': captcha_key
                                           })
        if 'token' not in response.json():
            return None
        return response.json()['token']

    async def generate(self) -> None:
        global total
        global locked
        global unlocked
        solver = Solver(site_url='discord.com', site_key='4c672d35-0701-42b2-88c3-78380b0db560', session=self.session)
        captcha_key = await solver.solve()
        while captcha_key is None:
            captcha_key = await solver.solve()
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
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'x-track': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExNS4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTE1LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjk5OTksImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9',
        }
        fingerprint = await self.get_fingerprint()
        self.fingerprint = fingerprint
        token = await self.create_account(captcha_key, fingerprint)
        if token is None:
            return
        self.session.headers.pop('x-track')
        self.session.headers['referer'] = 'https://discord.com/channels/@me'
        self.session.headers.update({
            'x-super-properties': self.super,
            'x-discord-locale': 'fr',
            'x-debug-options': 'bugReporterEnabled',
            'authorization': token
        })
        if (await self.session.get('https://discord.com/api/v9/users/@me/affinities/users')).status_code != 200:
            total += 1
            locked += 1
            print(f"{Fore.LIGHTWHITE_EX}[!] {Fore.LIGHTRED_EX}LOCKED{Fore.LIGHTWHITE_EX} {token.split('.')[0]}"
                  f"{Fore.RESET}")
            return
        total += 1
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
                            "name": f"to {secrets.token_urlsafe(6)}",
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
        json_data = {'date_of_birth': '2000-12-18', 'avatar': 'data:image/png;base64,' + base64.b64encode(open(
            os.path.join("input/image", random.choice(
                [f for f in os.listdir("input/image") if f.endswith('.jpg') or f.endswith('.png')])),
            'rb').read()).decode('utf-8')}
        added += "PFP"
        print(f"{Fore.LIGHTWHITE_EX}[!] {Fore.LIGHTMAGENTA_EX}UNLOCKED{Fore.LIGHTWHITE_EX} "
              f"{token.split('.')[0]}{Fore.RESET}")
        response = await self.session.patch('https://discord.com/api/v9/users/@me', json=json_data,
                                            proxy={"http": None, "https": None})
        if response.status_code == 200:
            added += " | DOB"
        response = await self.session.post('https://discord.com/api/v9/hypesquad/online',
                                           json={'house_id': random.randint(1, 3)})
        if response.status_code == 204:
            added += " | HS"
        bio = random.choice(open('input/bios.txt', 'r', encoding="utf-8").read().splitlines())
        response = await self.session.patch('https://discord.com/api/v9/users/%40me/profile', json={'bio': bio})
        if response.status_code == 200:
            added += " | BIO"
        unlocked += 1
        open('tokens.txt', 'a').write(f'{token}\n')
        ws.close()
        token = token.split(".")[0]
        if added:
            print(f"{Fore.LIGHTWHITE_EX}[!] {Fore.LIGHTBLUE_EX}ADDED PROFILE{Fore.LIGHTWHITE_EX} {token} | {added}{Fore.RESET}")

async def generate() -> None:
    while True:
        try:
            discord = Discord()
            await discord.generate()
        except Exception as e:
            pass


async def prepare():
    await Solver.setup()
    for _ in range(20):
        asyncio.create_task(generate())
    await asyncio.sleep(999999)


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    threading.Thread(target=update_title).start()
    asyncio.run(prepare())
