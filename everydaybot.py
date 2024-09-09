import telebot
import datetime
import threading
import json


API_TOKEN = "7032022212:AAHKybjdIEjDYA-_woGbsFuSJlB89o_Wf1w"
bot = telebot.TeleBot(API_TOKEN)


tasks = "E:\\Python\\Everydaybot\\tasks.json"
@bot.message_handler(commands=['start'])
def start(message):
	bot.send_message(message.chat.id, "Здравствуйте! Я - телеграммбот, который поможет вам не забыть о каких-либо делах, список продуктов. Проще говоря: Ваш верный помощник!\n \n /help - помощь вам =)")

@bot.message_handler(commands=['help'])
def help(message):
	bot.send_message(message.chat.id, "/start - перезапуск бота \n /reminder - установить напоминание \n /add 'имя задачи' - Добавить задачу \n /list - Просмотреть задачи \nПриятного использования!")

@bot.message_handler(commands=['reminder'])
def reminder_name(message):
	bot.send_message(message.chat.id, "Установите название для напоминания: ")
	bot.register_next_step_handler(message, set_reminder)


def set_reminder(message):
	user_data = {}
	user_data[message.chat.id] = {'reminder_name': message.text}
	bot.send_message(message.chat.id, "Введите дату и время в формате ГГ - ММ-ДД чч:мм")
	bot.register_next_step_handler(message, reminder, user_data)

def reminder(message,user_data):
	try:
		reminder_time = datetime.datetime.strptime(message.text,"%Y-%m-%d %H:%M")
		now = datetime.datetime.now()
		delta = reminder_time - now
		if delta.total_seconds() <= 0:
			bot.send_message(message.chat.id, "Вы ввели дату/время, которая уже истекла. Попробуйте заново")
		else:
			reminder_name = user_data[message.chat.id]['reminder_name']
			bot.send_message(message.chat.id, "Напоминание {} установлено!".format(reminder_name))
			reminder_timer = threading.Timer(delta.total_seconds(),send_reminder,[message.chat.id,reminder_name])
			reminder_timer.start()
	except ValueError:
		bot.send_message(message.chat.id,"Вы ввели некорректную дату/время. Попробуйте заново")

def send_reminder(chat_id,reminder_name):
	bot.send_message(chat_id, "Пришло время выполнить: {}!".format(reminder_name))
	

def load_tasks():
	try:
		with open("E:\\Python\\Everydaybot\\tasks.json","r") as f:
			return json.load(f)
	except FileNotFoundError:
		return {}

def save_tasks(tasks):
	try:
		with open("E:\\Python\\Everydaybot\\tasks.json","w") as f:
			json.dump(tasks,f)
	except IOError as e:
		print(f" ошибка {e}")

def add_task(user_id, task_text):
	tasks = load_tasks()
	if user_id not in tasks:
		tasks[str(user_id)] = []
	tasks[str(user_id)].append(task_text)
	save_tasks(tasks)

@bot.message_handler(commands=['add'])
def handle_add_task(message):
	try:
		task_text = message.text.split(maxsplit=1)[1]
		user_id = message.from_user.id
		add_task(str(user_id),task_text)
		bot.send_message(message.chat.id, "Задача добавлена!")
	except IndexError:
		bot.send_message(message.chat.id, "У тебя нет задач")


def list_tasks(user_id):
  tasks = load_tasks()
  if str(user_id) not in tasks:
  	return "У вас пока нет задач!"
  task_list = ""
  for i,task in enumerate(tasks[str(user_id)],1):
  	task_list += f"{i}.{task}\n"
  return task_list


@bot.message_handler(commands=['list'])
def handle_list_task(message):
	user_id = message.from_user.id
	task_list = list_tasks(user_id)
	bot.send_message(message.chat.id, task_list)

def handle_all_message(message):
	bot.send_message(message.chat.id, "Твоя моя не понимать. Для напоминание введите /reminder")

bot.polling(none_stop=True)


