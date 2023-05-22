import multiprocessing
import sys
import threading
import traceback

import tls_client

from libss.solver import Solver


def t():
    while 1:
        try:
            sess = tls_client.Session("chrome_108")
            sess.proxies = "socks5://jew:jew@localhost:1080"
            solver = Solver(hsl=True, site_url='discord.com', site_key='4c672d35-0701-42b2-88c3-78380b0db560')
            xd = solver.solve()
            if not xd:
                sys.stdout.write("failed 1 captcha...\n")
                sys.stdout.flush()
        except Exception:
            pass


def b():
    for i in range(62):
        threading.Thread(target=t).start()


if __name__ == '__main__':
    b()
