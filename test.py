import hfuck
class SolveCaptcha(object):
    def init():
        captcha_key = hfuck.Solver('9d4ce4a4e4;us;session_10830325:329508a720@datacenter.proxyempire.io:9000', "4c672d35-0701-42b2-88c3-78380b0db560", "https://discord.com/").solve_captcha()
        if "P0_" in captcha_key:
            return captcha_key
        else:
            return False
print(SolveCaptcha.init())