import httpx, time, random, json, threading
from colorama import Fore, Style
from colored import fg
def spam():
    try:
        ja = random.choice(open('tokens.txt', "r", encoding="utf-8").read().splitlines())
        balls = str(round(time.time()))
        data = {
            "content": f"{message} | Sent at: <t:{balls}:R>",
            "tts": False
        }
        json_payload = json.dumps(data).encode('utf-8')
        content_length = str(len(json_payload))
        headers = {
            "authority": "discord.com",
            "method": "POST",
            "path": f"/api/v9/channels/{channel}/messages",
            "scheme": "https",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "authorization": ja,
            "content-length": content_length,
            "content-type": "application/json",
            "cookie": "__dcfduid=f4eb3de061f611ed94d2c362d4cf7525; __sdcfduid=f4eb3de161f611ed94d2c362d4cf7525c9d19316ef5eed6ec714f638facc263a8d6886b38a0359d0cce29ee7b620f4df; _gcl_au=1.1.623562195.1676410200; locale=en-US; __cfruid=1d7d47c485975f39a9e81e59cc9e0ca97df414d4-1679623723; _gid=GA1.2.525544167.1679964273; _gat_UA-53577205-2=1; _ga=GA1.1.157891939.1668196446; OptanonConsent=isIABGlobal=false&datestamp=Mon+Mar+27+2023+20%3A44%3A32+GMT-0400+(Eastern+Daylight+Time)&version=6.33.0&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1&AwaitingReconsent=false; __cf_bm=LInKRRFt0YPYK8fhtogMr6Mzdi6fqSZtIMpVChRaxhg-1679964273-0-ASlKQYJVTxMpmoSWfBVSDFRWx7acxxTPrcF6KcgsfV6ra2+hSluypOK8uPUGs9p5pehkCT3IF/92S9zfXS2YGHStGtLpPLtP1Rkx1h2uMh3aWKujQQfzPBn0rQI8FekfgQ==; _ga_Q149DFWHT7=GS1.1.1679964272.8.0.1679964277.0.0.0",
            "origin": "https://discord.com",
            "referer": f"https://discord.com/channels/1089635924188594196/{channel}",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.192 Safari/537.36",
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExMC4wLjU0ODEuMTkyIFNhZmFyaS81MzcuMzYiLCJicm93c2VyX3ZlcnNpb24iOiIxMTAuMC41NDgxLjE5MiIsIm9zX3ZlcnNpb24iOiIxMCIsInJlZmVycmVyIjoiIiwicmVmZXJyaW5nX2RvbWFpbiI6IiIsInJlZmVycmVyX2N1cnJlbnQiOiIiLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiIiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoxODQwMzgsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGwsImRlc2lnbl9pZCI6MH0="
        }
        send = httpx.post(f"https://discord.com/api/v9/channels/{channel}/messages", headers=headers, json=data, proxies="http://LilFork:LilFork@142.202.220.242:11889")
        if send.status_code == 429:
            print(f"({Fore.LIGHTMAGENTA_EX}~{Style.RESET_ALL}) [{fg(208)}{ja[:30]}****************{Style.RESET_ALL}] → {Fore.LIGHTMAGENTA_EX}Rate-Limited{Style.RESET_ALL} [{Fore.LIGHTMAGENTA_EX}{channel}{Style.RESET_ALL}]")
        if send.status_code == 200:
            print(f"({Fore.LIGHTMAGENTA_EX}~{Style.RESET_ALL}) [{fg(208)}{ja[:30]}****************{Style.RESET_ALL}] → {Fore.LIGHTMAGENTA_EX}Message{Style.RESET_ALL}: {message} [{Fore.LIGHTMAGENTA_EX}{channel}{Style.RESET_ALL}]")
        if send.status_code != 200:
            print(f"({Fore.RED}-{Style.RESET_ALL}) Error → {send.status_code}")
    except Exception as e:
        print(f"({Fore.RED}-{Style.RESET_ALL}) Request Error → {e}")
        pass

def capter():
    try:
        ja = random.choice(open('tokens.txt', "r", encoding="utf-8").read().splitlines())
        balls = str(round(time.time()))
        with open('image.png', 'rb') as f:
            image_data = f.read()
        data = {
            "file": image_data,
            "tts": False,
            "content": "",
            "filename": "image.png"
        }
        #data = {
        #    "content": f"{message} | Sent at: <t:{balls}:R>",
        #    "tts": False
        #}
        json_payload = json.dumps(data).encode('utf-8')
        content_length = str(len(json_payload))
        headers = {
            "authority": "discord.com",
            "method": "POST",
            "path": f"/api/v9/channels/{channel}/messages",
            "scheme": "https",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "authorization": ja,
            "content-length": content_length,
            "content-type": "application/json",
            "cookie": "__dcfduid=f4eb3de061f611ed94d2c362d4cf7525; __sdcfduid=f4eb3de161f611ed94d2c362d4cf7525c9d19316ef5eed6ec714f638facc263a8d6886b38a0359d0cce29ee7b620f4df; _gcl_au=1.1.623562195.1676410200; locale=en-US; __cfruid=1d7d47c485975f39a9e81e59cc9e0ca97df414d4-1679623723; _gid=GA1.2.525544167.1679964273; _gat_UA-53577205-2=1; _ga=GA1.1.157891939.1668196446; OptanonConsent=isIABGlobal=false&datestamp=Mon+Mar+27+2023+20%3A44%3A32+GMT-0400+(Eastern+Daylight+Time)&version=6.33.0&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1&AwaitingReconsent=false; __cf_bm=LInKRRFt0YPYK8fhtogMr6Mzdi6fqSZtIMpVChRaxhg-1679964273-0-ASlKQYJVTxMpmoSWfBVSDFRWx7acxxTPrcF6KcgsfV6ra2+hSluypOK8uPUGs9p5pehkCT3IF/92S9zfXS2YGHStGtLpPLtP1Rkx1h2uMh3aWKujQQfzPBn0rQI8FekfgQ==; _ga_Q149DFWHT7=GS1.1.1679964272.8.0.1679964277.0.0.0",
            "origin": "https://discord.com",
            "referer": f"https://discord.com/channels/1089635924188594196/{channel}",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.192 Safari/537.36",
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExMC4wLjU0ODEuMTkyIFNhZmFyaS81MzcuMzYiLCJicm93c2VyX3ZlcnNpb24iOiIxMTAuMC41NDgxLjE5MiIsIm9zX3ZlcnNpb24iOiIxMCIsInJlZmVycmVyIjoiIiwicmVmZXJyaW5nX2RvbWFpbiI6IiIsInJlZmVycmVyX2N1cnJlbnQiOiIiLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiIiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoxODQwMzgsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGwsImRlc2lnbl9pZCI6MH0="
        }
        send = httpx.post(f"https://discord.com/api/v9/channels/{channel}/messages", headers=headers, json=data, proxies="http://LilFork:LilFork@142.202.220.242:11889")
        if send.status_code == 429:
            print(f"({Fore.LIGHTMAGENTA_EX}~{Style.RESET_ALL}) [{fg(208)}{ja[:30]}****************{Style.RESET_ALL}] → {Fore.LIGHTMAGENTA_EX}Rate-Limited{Style.RESET_ALL} [{Fore.LIGHTMAGENTA_EX}{channel}{Style.RESET_ALL}]")
        if send.status_code == 200:
            print(f"({Fore.LIGHTMAGENTA_EX}~{Style.RESET_ALL}) [{fg(208)}{ja[:30]}****************{Style.RESET_ALL}] → {Fore.LIGHTMAGENTA_EX}Message{Style.RESET_ALL}: {message} [{Fore.LIGHTMAGENTA_EX}{channel}{Style.RESET_ALL}]")
        if send.status_code != 200:
            print(f"({Fore.RED}-{Style.RESET_ALL}) Error → {send.status_code}")
    except Exception as e:
        print(f"({Fore.RED}-{Style.RESET_ALL}) Request Error → {e}")
        pass

if __name__ == "__main__":
   # print(Colorate.Diagonal(Colors.purple_to_red, Center.XCenter(Ascii.get('Nigga Spam', AsciiType.DOH))))
    message = input(f"({fg('magenta')}+{Style.RESET_ALL}) Message → ")
    channel = input(f"({fg('magenta')}+{Style.RESET_ALL}) Channel ID → ")
    threads = input(f"({fg('magenta')}+{Style.RESET_ALL}) Threads → ")
    print(f"({fg('magenta')}+{Style.RESET_ALL}) Starting...")
    for _ in range(int(threads)):
        threading.Thread(target=spam).start()