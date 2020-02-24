import requests
from bs4 import BeautifulSoup as BS

session = requests.Session()

def auth():
	"""
	Функция авторизации
	"""

	url = "https://fix-price.ru/ajax/auth_user.php"
	params = {
	'AUTH_FORM':'Y',
	'TYPE':'AUTH',
	'backurl':'/personal/',
	'login': login,
	'password': password
	}
	session.post(url, data=params)

	return True

login = ''
password = ''

while login == '':
	login = str(input('Введите логин: '))
while password == '':	
	password = str(input('Введите пароль: '))


user_info = [] #контейнер для данных об имени, отчестве, фамилии, емайл, даты рождении
def profile():
	"""
		Парсинг профиля
	"""
	response = session.get('https://fix-price.ru/personal/#profile_data')
	soup = BS(response.content, 'lxml')
	profile_data = soup.find_all('div', class_='personal-data__item')[0] #ищем общие персональные данные


	profile_data_main = profile_data.find_all('input', {'type': 'text'}) #поиск имени,фамилии,отчества,почты, даты рождения
	for info in profile_data_main: 
		user_info.append(info.attrs['value']) # Добавление в список данных об имени, фамилии...

	profile_data_gender = profile_data.find('input', {'checked': 'checked'}).attrs['value']
	user_info.append(profile_data_gender) # поиск пола

	profile_data_sity = soup.find_all('div', class_='personal-data__item')[1].find_all('select')[1].find('option').text
	user_info.append(profile_data_sity) # Добавляем город

	profile_data_oblast = soup.find('option', {'selected': True}).text
	user_info.append(profile_data_oblast) # Добавляем область
		
	profile_data_index = soup.find_all('div', class_='personal-data__item')[1].find('input').attrs['value']
	user_info.append(profile_data_index) # вывод индекса города
	
	profile_data_email = soup.find_all('div', class_='personal-data__item')[1].find('input', {'id': 'emailSubscribe'}).attrs['value']
	user_info.append(profile_data_email) # подписка на емайл 1 - да
	
	profile_data_sms = soup.find_all('div', class_='personal-data__item')[1].find('input', {'id': 'smsSubscribe'}).attrs['value']
	user_info.append(profile_data_sms) # подписка на sms 1 - да

	profile_data_card = soup.find('div', class_='personal-card__number').text
	user_info.append(profile_data_card) # номер скидочной карты

	profile_data_balance = soup.find('div', class_='client-points__active').text
	user_info.append(profile_data_balance) # баланс скидочной карты
	
	return user_info

price = [] # храним все цены
desc = [] # храним все описания товаров
product = [] # храним все товары в избранном
def faviorites():
	"""
	Сохранение избранных товаров
	"""
	response = session.get('https://fix-price.ru/favorites/')
	soup = BS(response.content, 'lxml')
	
	fav_data_price = soup.find_all('div', class_='product-card product-card--md') # цена товара
	for a in fav_data_price:
		b = a.find('span', {'itemprop': 'price'}).attrs['data-price']
		price.append(b) # сохраняем список цен
	
	fav_data_desc = soup.find_all('div', class_='product-card product-card--md') # описание товара
	for a in fav_data_desc:
		b = a.find('div', {'itemprop': 'description'}).text.strip()
		desc.append(b)
	
	fav_data_product = soup.find_all('div', class_='product-card product-card--md') # наименование товара
	for a in fav_data_product:
		b = a.find('a', class_="product-card__title").text.strip()
		product.append(b)

action_time = [] # даты акций
action_title = [] # заголовок акций
action_desc = [] # описание акций
def actions():
	for a in range(1,6):
		response = session.get('https://fix-price.ru/actions/?PAGEN_2='+str(a))
		soup = BS(response.content, 'lxml')
		act_data = soup.find_all('a', {'class': 'action-block__item'})
		for a in act_data:
			act_data_a = a.find('span', class_= 'action-card__footer-date') # даты завершающиеся акции
			if act_data_a != None:
				action_time.append(act_data_a.text)
		for a in act_data:
			act_data_b = a.find('div', class_= 'action-card__date') # даты длинные акции
			if act_data_b != None:
				b = str(act_data_b.text.strip().replace(' ',''))
				if b != 'акциязавершена':
					action_time.append(b)	
	

def writer():
	"""
	Запись информации в файл
	"""
	a = [				#Список ключей для вывода личных данных
		'Фамилия: ', 
		'Имя: ',
		'Отчество: ',
		'e-mail: ',
		'Дата рождения: ', 
		'Пол: ',
		'Город: ',
		'Область: ',
		'Индекс города: ',
		'Подписка на e-mail: ',
		'Подписка на sms: ',
		'Номер скидочной карты: ',
		'Баланс скидочной карты: '
		]
	with open(f'{login}.txt', 'w') as write_file:
		b = dict(zip(a,user_info))
		for key,value in b.items():
			write_file.write('{}{}\n'.format(key,value))
		
		write_file.write('\n\n ----- ТОВАРЫ В ИЗБРАННОМ ----\n\n')
		
		for a in range(len(product)):
			write_file.write(str(a+1)+')'+' '+product[a]+'   ')
			write_file.write(desc[a]+'   ')
			write_file.write('Цена: '+price[a]+'руб\n\n')

	print('Данные записаны в файл - 'f'{login}.txt')


auth()
# profile()
# faviorites()
actions()
# writer()
print(action_time)
