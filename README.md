# -Описание-

### Кейлоггер может:
- Сохранять логи в случайно названный файл 
- Отправлять логи в телеграм бота
- Отправлять скриншоты в телеграм бота
### При отправке в телеграм также показываются:
- IP-адрес 
- Имя машины
- Имя пользователя

![2](https://user-images.githubusercontent.com/56086653/106382940-ed92c400-63d3-11eb-8908-2b1b982d2b6a.PNG)
![1](https://user-images.githubusercontent.com/56086653/106382935-e66bb600-63d3-11eb-83f3-a3c1ed66ef11.PNG)


# -Установка-

### Кейлоггер имеет следующие зависимости:
- Pillow
- requests
- pyperclip
- pythoncom  
- pyHook

Все они ставятся без проблем, кроме [pyHook](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyhook).
Беда в том, что официальный модуль имеет много багов, которые не позволяют полноценно использовать кейлоггер, поэтому я использую доработанную версию - https://github.com/Answeror/pyhook_py3k (которая тоже имеет критические баги, но более юзабельна)

Для установки pyhook_py3k:
- Скачайте pyhook_py3k
- Скачайте swig.exe http://www.swig.org/download.html и запомните путь, например у меня он такой: C:\swig.exe
- Скачайте VS C++ build tools https://visualstudio.microsoft.com/ru/visual-cpp-build-tools/
- Перейдите в папку с pyhook_py3k и пропишите в консоли:
```
python setup.py build_ext --swig=C:\swig.exe
pip install .
```
### Готово! Осталось настроить кейлоггер.







