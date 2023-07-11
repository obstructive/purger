from colorama import Fore, Back, Style, init

init(autoreset=True, convert=True)

class Logger:
    def __init__(self, name):
        self.name = name

    def log(self, message, prefix, fore_color, back_color):
        formatted_message = f'{back_color}{fore_color}{prefix}{Style.RESET_ALL} {message}'
        print(formatted_message)

    def success(self, message):
        self.log(message, '[+]', Fore.WHITE, Back.GREEN)

    def error(self, message):
        self.log(message, '[-]', Fore.WHITE, Back.RED)

    def info(self, message):
        self.log(message, '[~]', Fore.WHITE, Back.BLUE)
