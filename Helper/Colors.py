
class Color:

    @staticmethod
    def print_infos(message):
        print('\033[94m' + message + '\033[0m')

    @staticmethod
    def print_warning(message):
        print('\033[93m' + message + '\033[0m')

    @staticmethod
    def print_error(message):
        print('\033[91m' + message + '\033[0m')

    @staticmethod
    def print_success(message):
        print('\033[92m' + message + '\033[0m')
