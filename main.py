import time
from datetime import datetime as dt
import requests
from bs4 import BeautifulSoup as bs
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
import os
import json


def show_news(t):
	print(f'{t} новостей на сегодня:')
	URL_TEMPLATE = "https://habr.com/ru/news" # https://habr.com/ru/news/top/daily/
	r = requests.get(URL_TEMPLATE)
	html_doc = r.text
	soup = bs(html_doc, 'html.parser')

	x = 0
	for i in soup.find_all("a", class_="tm-article-snippet__title-link"):
		x += 1
		print('-' * (len(i.span.text) + 4))
		print('|', i.span.text, '|')
		print('|', f'Подробнее: habr.com{i.get("href")}', end='')
		print(' ' * (len(i.span.text) - len(f'Подробнее: habr.com{i.get("href")}')), "|")
		print('-' * (len(i.span.text) + 4))
		print()
		if x == t:
			break


def weather(c):
	owm = OWM('48de1d399cdd9181e5832ed10dc1d75f')
	mgr = owm.weather_manager()
	observation = mgr.weather_at_place(c)
	w = observation.weather
	print(f"Погода сейчас {w.detailed_status},")
	print(f"темпиратура: {w.temperature('celsius')['temp']}")


def os_info():
	OS_NAME = f"{os.uname().sysname} { ''.join([i if i.isalpha() else '' for i in os.uname().release]).lower()}"
	USERNAME = os.getlogin()
	MACHINE = os.uname().machine
	HOST_NAME = os.uname().nodename
	NOW_TIME = dt.now().strftime("%A %d-%B-%y %H:%M:%S")

	b = {
    'OS': OS_NAME,
    'name': USERNAME,
    'machine': MACHINE,
    'host name':HOST_NAME,
    'time': NOW_TIME
    }

	x = 0

	for bb in b.items():
		print(f"\033[1;32;231m{bb[0]}\033[0;0m: {bb[1]}")
		x += 1


def reg():
	json_fil = open('names.json', 'r', encoding='utf-8')
	str_json = json_fil.read()
	data = json.loads(str_json)
	# print(data)
	if not data['name']:
		data['name'] = input('Как я могу к тебе обращаться? ')
	uname = data['name']
	if not data['city']:
		data['city'] = input('Где ты живешь? (город) ')
	town = data['city']
	print(data)
	json_fil.close()
	json_fil2 = open('names.json', 'w', encoding='utf-8')
	json.dump(data, json_fil2)
	json_fil2.close()
	return (uname, town)


def clear_data():
	json_fil = open('names.json', 'r', encoding='utf-8')
	str_json = json_fil.read()
	data = json.loads(str_json)
	# print(data)
	print(data)
	data['name'] = None
	data['city'] = None
	print(data)
	json_fil.close()
	json_fil2 = open('names.json', 'w', encoding='utf-8')
	json.dump(data, json_fil2)
	json_fil2.close()


def your_info():
	print('Привет, меня зовут neko-alice-chan')
	print('Я могу помогать тебе с компом, а так же могу тебя потдержать')
	print('Для потдержки просто напиши "Потдержи меня"')
	print('ня')


def main():
	uname, town = reg()

	# ---------------------------------------
	#fil = open('username.txt', 'a+', encoding='utf-8')
	#fil.seek(0)
	#if fil.readline() == '':
	#	name = input('Как я могу к тебе обращаться? ')
	#	fil.write(f'{name}\n')
	#	town = input('Где ты живешь? ')
	#	fil.write(town)
	#fil.seek(0)
	#uname = fil.readline()
	#fil.seek(1)
	#your_city = fil.readline()
	#fil.close()
	# ---------------------------------------------

	print(f"Привет, {uname}")
	print('Точное время:', dt.now().strftime("%A %d-%B-%y %H:%M:%S"))
	print()
	weather(town)
	show_news(6)
	os_info()
	print()
	print("Я могу помогать тебе с компом, так что, если что-то нужно будет, пиши сюда")
	while True:
		inn = input('> ')
		if inn == 'пока' or inn == 'exit':
			print('Пока')
			break
		elif 'news' in inn or 'новости' in inn:
			show_news(int(inn.split()[1]))
		elif inn.lower() == 'time' or inn.lower() == 'время' or inn.lower() == 'сколько времени':
			print('|', f"Точное время: {dt.now().strftime('%A %d-%B-%y %H:%M:%S')}", '|')
		elif inn == 'os info' or inn == 'osinfo':
			os_info()
		elif inn == 'weather' or inn == 'погода':
			weather(town)
		elif inn == 'myinfo' or inn == 'Я':
			print(f'Тебя зовут {uname}', f'Ты живешь в {town}', sep='\n')
		elif inn == 'clear my data' or inn == 'relog':
			inn = input('вы хотите удалить свои данные и зарегестрироваться снова? (y/N)')
			if inn.lower() == 'y' or inn.lower() == 'yes':
				clear_data()
				uname, town = reg()
			elif inn.lower() == 'n' or inn.lower() == 'no':
				pass
			elif inn == 'asd':
				clear_data()
		elif inn == 'Кто ты' or inn == 'Your info':
			your_info()
		elif inn == 'Потдержи меня' or inn == "I'm sed":
			print('Я с тобой')
			print('Ня')

if __name__ == '__main__':
	main()
