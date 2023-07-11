import platform


class Logger:
    PREFIXES = {'success': '[+]', 'error': '[-]', 'info': '[~]'}

    COLORS = {
        'success': '\033[1;32m',
        'error': '\033[1;31m',
        'info': '\033[1;34m',
    }

    RESET = '\033[0m'

    def __init__(self, name):
        self.name = name
        self.is_windows = platform.system() == 'Windows'

    def log(self, message, prefix, color):
        if self.is_windows:
            formatted_message = f'{prefix} {message}'
        else:
            formatted_message = f'{color}{prefix}{self.RESET} {message}'
        print(formatted_message)

    def log_message(self, message_type, message):
        prefix = self.PREFIXES.get(message_type, '')
        color = self.COLORS.get(message_type, '')
        self.log(message, prefix, color)

    def success(self, message):
        self.log_message('success', message)

    def error(self, message):
        self.log_message('error', message)

    def info(self, message):
        self.log_message('info', message)
