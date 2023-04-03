import traceback
import threading
from bs4 import BeautifulSoup
import tls_client
import random
from console import console
from funny_email_verify.email import emailfucker
import string
import random

class discordVerify():
    def __init__(self, token):
        self.session = tls_client.Session(
            client_identifier="chrome_111",
            random_tls_extension_order=True,
            h2_settings={"HEADER_TABLE_SIZE": 65536,"MAX_CONCURRENT_STREAMS": 1000,"INITIAL_WINDOW_SIZE": 6291456,"MAX_HEADER_LIST_SIZE": 262144},
            h2_settings_order=["HEADER_TABLE_SIZE","MAX_CONCURRENT_STREAMS","INITIAL_WINDOW_SIZE","MAX_HEADER_LIST_SIZE"],
            supported_signature_algorithms=["ECDSAWithP256AndSHA256","PSSWithSHA256","PKCS1WithSHA256","ECDSAWithP384AndSHA384","PSSWithSHA384","PKCS1WithSHA384","PSSWithSHA512","PKCS1WithSHA512",],
            supported_versions=["GREASE", "1.3", "1.2"],
            key_share_curves=["GREASE", "X25519"],
            cert_compression_algo="brotli",
            pseudo_header_order=[":method",":authority",":scheme",":path"],
            connection_flow=15663105,
            header_order=["accept","user-agent","accept-encoding","accept-language"]
        )
        self.password = ''.join(random.choices(string.ascii_uppercase +string.digits, k=13))
        self.token = token
        self.proxy = "http://" + random.choice(open('input/proxies.txt').read().splitlines())
        self.session.proxies = {"http": self.proxy,"https": self.proxy}
        self.mailClient = emailfucker()
        self.address = self.mailClient.createAddress()
        console.info(f'New Mail --> {self.address}')

    def submitToken(self, emailToken):
        headers = {
            'authority': 'discord.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'referer': 'https://discord.com/verify',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'en-US',
            #'x-fingerprint': '1091911245021581322.YJ_I2pis8mFP4CPLKDkEVP6Sf5Y',
            'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExMS4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTExLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjE4NTgzMiwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0=',
        }

        json_data = {
            'token': emailToken,
            'captcha_key': None,
        }

        response = self.session.post('https://discord.com/api/v9/auth/verify', headers=headers, json=json_data)
        if response.status_code == 200:
            console.success(f'Verified Token --> {self.token}')
            with open('verified.txt', 'a') as f:
                newToken = response.json()["token"]
                f.write(f'{self.address}:{self.password}:{newToken}\n')

    def addMail(self):
        self.session.get('https://discord.com')
        headers = {
            'authority': 'discord.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': self.token,
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'referer': 'https://discord.com/channels/@me',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'fr',
            'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExMS4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTExLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjE4NTgzMiwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbCwiZGVzaWduX2lkIjowfQ==',
        }

        json_data = {
            'email': self.address,
            'password': self.password,
        }

        response = self.session.patch('https://discord.com/api/v9/users/@me', headers=headers, json=json_data)
        self.token = response.json()["token"]
        if response.status_code == 200:
            console.info(f'Added Mail --> {self.token}')
            return True
        else:return False
    
    def verifyToken(self):
        try:
            res = self.addMail()
            if res == True:
                self.email = self.mailClient.waitForEmail()
                console.success(f'Got Mail --> {self.address}')
                emailBody = self.email[0]["Body"]
                soup = BeautifulSoup(emailBody, 'html.parser')
                link = soup.find_all('a')[1].get('href')
                verifyToken = str(self.session.get(link, allow_redirects=True).url).split('#')[1].replace('token=', '')
                self.submitToken(verifyToken)
            else:return False
        except:
            #traceback.print_exc()
            pass


for token in open('input/tokens.txt').read().splitlines():
    while True:
        if threading.active_count()<=50:
            threading.Thread(target=discordVerify(token).verifyToken).start()
            break