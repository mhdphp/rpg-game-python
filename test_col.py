import os
import colorama

convert ='test'
strip = 'test'

if 'PYCHARM_HOSTED' in os.environ:
    convert = False  # in PyCharm, we should disable convert
    strip = False
    print("Hi! You are using PyCharm")
else:
    convert = None
    strip = None

colorama.init(convert=convert, strip=strip)
print(colorama.Fore.GREEN + "hello world-green" + colorama.Fore.RESET)
print(colorama.Fore.RED + "hello world-red" + colorama.Fore.RESET)
print(convert, strip)

