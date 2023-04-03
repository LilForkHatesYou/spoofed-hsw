from colorama import Fore

class console():
    def info(message):
        print(f'({Fore.MAGENTA}~{Fore.RESET}) - {message}')
    def error(message):
        print(f'({Fore.RED}!{Fore.RESET}) - {message}')
    def success(message):
        print(f'({Fore.GREEN}${Fore.RESET}) - {message}')