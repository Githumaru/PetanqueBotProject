import pandas as pd
import pickle
import base64
import telebot
from telebot import types


adress = 'C:\\PyProdjects\\Telegram\\Petanque\\DataBase.csv'

class Player:

    list_of_players = []

    @classmethod
    def load_players(cls):
        table = pd.read_csv(adress, sep=';')
        pickled_objs = table['player'].values
        cls.list_of_players = [pickle.loads(base64.b64decode(obj)) for obj in pickled_objs]

    def __init__(self, name):
        self.name = name
        self.score = 1000
        table = pd.read_csv(adress, sep=';')
        table.loc[len(table)] = [base64.b64encode(pickle.dumps(self)).decode(), self.name, self.score]
        table.to_csv(adress, sep=';', index=False)
        Player.list_of_players.append(self)

    def match(self, name, victory):
        victory = float(victory)
        d = abs(self.score - name.score)
        e = 1 / (1 + 10 ** (d / 400))
        self.score += 32 * (victory - e)
        name.score += 32 * (1 - victory - e)
        table = pd.read_csv(adress, sep=';')
        table.iloc[table[table['name'] == self.name].index, 0] = [base64.b64encode(pickle.dumps(self)).decode()]
        table.iloc[table[table['name'] == name.name].index, 0] = [base64.b64encode(pickle.dumps(name)).decode()]
        table.iloc[table[table['name'] == self.name].index, 2] = self.score
        table.iloc[table[table['name'] == name.name].index, 2] = name.score
        table.sort_values('score')
        table.to_csv(adress, sep=';', index=False)


bot = telebot.TeleBot(token=token)


@bot.message_handler(content_types=['text'])
def handle_start(message):
    if message.text == '/help':
        bot.send_message(chat_id=message.chat.id,
                         text='Hello there. I am Mr. Bot for your petang. Please use me. Press "/start"')
    elif message.text == '/start':
        Player.load_players()
        bot.send_message(chat_id=message.chat.id,
                         text='Choose an option: ',
                         reply_markup=create_keyboard())
    elif message.text == '/stop':
        bot.stop_polling()


def create_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="Add a new player",
                                     callback_data='Add a new player')
    button2 = types.InlineKeyboardButton(text="Add match result",
                                     callback_data='Add match result')
    button3 = types.InlineKeyboardButton(text="Show rating",
                                     callback_data='Show rating')
    button4 = types.InlineKeyboardButton(text="Show rank",
                                     callback_data='Show rank')
    keyboard.add(button1, button2).add(button3, button4)
    return keyboard


def create_keyboar():
    keyboar = types.InlineKeyboardMarkup()
    for player in Player.list_of_players:
        keyboar.add(types.InlineKeyboardButton(text=f"{player.name}",
                                               callback_data=f'{player.name}'))
    return keyboar


def create_keyboa():
    keyboa = types.InlineKeyboardMarkup()
    for player in Player.list_of_players:
        keyboa.add(types.InlineKeyboardButton(text=f"{player.name}",
                                              callback_data=f'+{player.name}'))
    return keyboa


def create_keybo():
    keybo = types.InlineKeyboardMarkup()
    for player in Player.list_of_players:
        keybo.add(types.InlineKeyboardButton(text=f"{player.name}",
                                             callback_data=f'{player.name}+'))
    return keybo


def create_keyb():
    keyb = types.InlineKeyboardMarkup()
    keyb.add(types.InlineKeyboardButton(text='Win', callback_data='1'),
             types.InlineKeyboardButton(text='Lose', callback_data='0'),
             types.InlineKeyboardButton(text='Draw', callback_data='0.5'))
    return keyb


def create_player(message):
    player = Player(message.text)
    bot.send_message(chat_id=message.chat.id,
                     text=f'Player {player.name} has been added')
    bot.send_message(chat_id=message.chat.id,
                     text='Choose an option: ', reply_markup=create_keyboard())


@bot.callback_query_handler(func=lambda call: call.data == 'Add a new player')
def add_player_callback(call):
    bot.send_message(chat_id=call.message.chat.id,
                     text='Write the name of the player here:')
    bot.register_next_step_handler(call.message, create_player)


@bot.callback_query_handler(func=lambda call: call.data == 'Add match result')
def add_match_callback(call):
    bot.send_message(chat_id=call.message.chat.id,
                     text='Choose first player:',
                     reply_markup=create_keyboar())


@bot.callback_query_handler(func=lambda call: call.data in map(lambda x: x.name, Player.list_of_players))
def add_first_player(call):
    global list_players
    list_players = [call.data]
    bot.send_message(chat_id=call.message.chat.id,
                     text='Choose second player:',
                     reply_markup=create_keyboa())


@bot.callback_query_handler(func=lambda call: call.data in map(lambda x: f'+{x.name}', Player.list_of_players))
def add_second_player(call):
    list_players.append(call.data[1:])
    global players_class
    players_class = [i for i in Player.list_of_players if i.name in list_players]
    bot.send_message(chat_id=call.message.chat.id,
                     text=f'Choose the result for {players_class[0].name}:',
                     reply_markup=create_keyb())


@bot.callback_query_handler(func=lambda call: call.data in ['1', '0', '0.5'])
def add_score(call):
    players_class[0].match(players_class[1], call.data)
    bot.send_message(chat_id=call.message.chat.id,
                     text='The rating has been changed')
    bot.send_message(chat_id=call.message.chat.id,
                     text='Choose an option: ',
                     reply_markup=create_keyboard())


@bot.callback_query_handler(func=lambda call: call.data == 'Show rating')
def rating_callback(call):
    Player.list_of_players.sort(key=lambda x: x.score, reverse=True)
    for player in Player.list_of_players:
        bot.send_message(chat_id=call.message.chat.id,
                         text=f'{Player.list_of_players.index(player) + 1}. {player.name}: {int(player.score)}')


@bot.callback_query_handler(func=lambda call: call.data == 'Show rank')
def rank_callback(call):
    bot.send_message(chat_id=call.message.chat.id,
                     text='Choose player:',
                     reply_markup=create_keybo())


@bot.callback_query_handler(func=lambda call: call.data in map(lambda x: f'{x.name}+', Player.list_of_players))
def rank(call):
    player = [i for i in Player.list_of_players if i.name == call.data[:-1]][0]
    bot.send_message(chat_id=call.message.chat.id,
                     text=f'{player.name}: {int(player.score)}, {Player.list_of_players.index(player) + 1}')


bot.polling(none_stop=True, interval=0)
