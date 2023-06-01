from colorama import Fore, Back, Style, init

init(autoreset=True, convert=True)


class Logger:
    def __init__(self, name):
        self.name = name

    def success(self, message):
        self._print_message(message, Fore.WHITE, Back.GREEN, '[+]', Fore.WHITE)

    def error(self, message):
        self._print_message(message, Fore.WHITE, Back.RED, '[-]', Fore.WHITE)

    def info(self, message):
        self._print_message(message, Fore.WHITE, Back.BLUE, '[~]', Fore.WHITE)

    def _print_message(
        self, message, fore_color, back_color, prefix, reset_color
    ):
        formatted_message = f'{back_color}{fore_color}{prefix}{Style.RESET_ALL} {message}{reset_color}'
        print(formatted_message)
