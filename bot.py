from parser_city import main, list_of_cities
from check_city import check_this_city
import telebot

TOKEN = ""
bot = telebot.TeleBot(TOKEN)
game_over = False #глобальная переменная проверки на то, закончилась ли игра

@bot.message_handler(commands=['start'])
def send_welcome(message):
    hello = "Привет!\nЯ бот для игры в Города.\n\nЕсли хотите начать игру, пришлите мне команду /newgame!"
    bot.reply_to(message, hello)


@bot.message_handler(commands=['newgame'])
def new_game(message):
    global game_over
    game_over = False
    list_of_cities.clear() #список городов
    bot.reply_to(message, "Назовите любой город!")

@bot.message_handler(content_types=['text'])
def get_city(message):
    global game_over
    """
    Я перевожу все города в нижний регистр для того, чтоб сохранять их в список и удобнее
    сравнивать с теми, что уже были. Из-за этого нет привязки у тому, как пользователь напишет название: 
    с большой буквы, капсом и т.д.
    """
    print(message.from_user.first_name)
    print(message.text)

    if game_over:
        bot.reply_to(message, "Если хотите начать новую игру, используйте специальную команду /newgame")
        return

    if message.text.lower() == "не знаю":
        bot.reply_to(message, "Тогда я выиграл!")
        game_over = True
        return
    
    #помещаю в нижний кейс слово юзера для проверки
    users_word = message.text.lower()

    if list_of_cities:
        letter = ''
        if list_of_cities[-1][-1] == "ь" or list_of_cities[-1][-1] == "ъ":
            letter = list_of_cities[-1][-2]
        else:
            letter = list_of_cities[-1][-1]

        if users_word[0] != letter:
            bot.reply_to(message, "Введите название города, которое начинается на \"" + letter.upper() + "\"")
            return


    checking_the_city = check_this_city(users_word)

    if not checking_the_city:
        bot.reply_to(message, "Введите корректное название города!")
        return
        
    for i in list_of_cities:
        if i == users_word:
            bot.reply_to(message, "Этот город уже был назван!")
            return
            
    #помещаю город, названный пользователем в список
    list_of_cities.append(users_word)
    print(list_of_cities)

    if message.text[-1].upper() == "Ь" or message.text[-1].upper() == "Ъ":
        city = main(message.text[-2].upper())
    else:
        city = main(message.text[-1].upper())

    if city == None:
        bot.reply_to(message, "Я не знаю больше городов, вы выиграли!")
        game_over = True
        return
    
    bot.reply_to(message, city)

bot.polling()