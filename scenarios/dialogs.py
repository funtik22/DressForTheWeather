from dialogic import COMMANDS
from dialogic.cascade import DialogTurn

from dm import csc

from get_temperature import *
import json
import random
import pandas as pd


with open('info.json', encoding='utf-8') as f:
    info = json.load(f)

def is_single_pass(turn: DialogTurn) -> bool:
    """ Check that a command is passed when the skill is activated """
    if not turn.ctx.yandex:
        return False
    if not turn.ctx.yandex.session.new:
        return False
    return bool(turn.ctx.yandex.request.command)


def is_new_session(turn: DialogTurn):
    return turn.ctx.session_is_new() or not turn.text


@csc.add_handler(priority=10, regexp='(hello|hi|привет|здравствуй)')
@csc.add_handler(priority=1000, checker=is_new_session)
def hello(turn: DialogTurn):
    text = random.choice(info['hello'])
    text = f'<speaker audio="alice-sounds-game-powerup-1.opus"> <text>{text}</text><voice>{text}</voice>'
    turn.response_text = text
    turn.user_object["last_phrase"] = text


@csc.add_handler(priority=5, regexp='(что|надеть|одеть|одеться|выбрать)')
def drees_for_dress(turn: DialogTurn):
    if len(turn.ctx.yandex.request.nlu.entities)!=0:
        city = str(turn.ctx.yandex.request.nlu.entities[0].value.get('city'))
    else:
        city = ''
    if city!=None and city!='':
       turn.user_object['city'] = city
       if turn.user_object.get('gender'):
           text = get_advice(turn)
           turn.response_text = text
           turn.user_object["last_phrase"] = text
       else:
           text = "Назови свой пол, пожалуйста"
           turn.response_text = text
           turn.user_object["last_phrase"] = text
    else:
       text = "Город не найден!"
       turn.response_text = text
       turn.user_object["last_phrase"] = text


@csc.add_handler(priority=1000, intents=['ability'])
def show_rules(turn: DialogTurn):
    text = random.choice(info['ability'])
    turn.response_text = text
    turn.user_object['last_phrase'] = text


@csc.add_handler(priority=1000, intents=['repeat_phrase'])
def repeat_phrase(turn: DialogTurn):
    turn.response_text = turn.user_object['last_phrase']

@csc.add_handler(priority=0)  # use it as a fallback scenario
def mistake(turn: DialogTurn):
    count_mistakes = turn.user_object.get('mistakes')
    if count_mistakes == None:
        count_mistakes = 0
    if count_mistakes == 0:
        count_mistakes += 1
        turn.response_text = random.choice(info['mistakes'])
    elif count_mistakes == 1:
        count_mistakes += 1
        turn.response_text = random.choice(info['mistakes_1']) + turn.user_object['last_phrase']
    else:
        turn.response_text = random.choice(info['mistakes_2'])
        turn.suggests.append('Помощь')
    turn.user_object['mistakes'] = count_mistakes

@csc.add_handler(priority=10, intents=['total_exit'])
def total_exit(turn: DialogTurn):
    turn.response_text = info['goodbye']
    turn.commands.append(COMMANDS.EXIT)


@csc.add_handler(priority=10000000, intents=['ping'])
def ping_pong(turn: DialogTurn):
    turn.response_text = 'pong'

@csc.add_handler(priority=1000, intents=['help'])
def alice_help(turn: DialogTurn):
    turn.response_text = 'Чтобы получить мой совет о том, как одеться по погоде, назови свой город, в котором находишься или ближайший крупный населённый пункт!'


@csc.add_handler(priority=100, intents=['gender_M'])
def gender_M (turn: DialogTurn):
    turn.user_object['gender'] = "Мужской"
    turn.response_text = get_advice(turn)


@csc.add_handler(priority=100, intents=['gender_W'])
def gender_W (turn: DialogTurn):
    turn.user_object['gender'] = "Женский"
    turn.response_text = get_advice(turn)


def get_advice(turn):

    gender = turn.user_object['gender']

    if gender == 'Мужской':
        man = pd.read_excel("tempman.xlsx")
    elif gender == 'Женский':
        man = pd.read_excel("tempwoman.xlsx")
    temp = get_temperature(turn.user_object['city'])
    rain = is_precipitation(turn.user_object['city'])
    num = random.randint(1, 3)

    title = ["от 0 до +5", "от +5 до +10", "от +10 до +15", "от +15 до +20", \
             "от +20 до +25", "от +25 до +30", "от +30 до +35", "от +35 до +40", \
             "от +40 до +45", "от -45 до -40", "от -40 до -35", \
             "от -35 до -30", "от -30 до -25", "от -25 до -20", "от -20 до -15", \
             "от -15 до -10", "от -10 до -5", "от -5 до 0"]

    if temp > 45:
        recommendation = man[man["Температура"] == ">45"][[f"Совет {num}"]].head()
        if_rain = man[man["Температура"] == ">45"][["Доп. совет в случае дождя"]].head()
    elif temp < -45:
        recommendation = man[man["Температура"] == "<-45"][[f"Совет {num}"]].head()
        if_rain = man[man["Температура"] == "<-45"][["Доп. совет в случае дождя"]].head()
    else:
        recommendation = man[man["Температура"] == title[temp//5]][[f"Совет {num}"]].head()
        if_rain = man[man["Температура"] == title[temp//5]][["Доп. совет в случае дождя"]].head()
    if temp>0:
        str_temp = "+"+str(temp)
    else:
        str_temp = str(temp)
    if rain:
        return  random.choice(info['temp'])+str_temp+"\n"+recommendation.loc[recommendation.index[0]][f"Совет {num}"]+'\n'+if_rain.loc[if_rain.index[0]]["Доп. совет в случае дождя"]
    else:
        return  random.choice(info['temp'])+str_temp+"\n"+recommendation.loc[recommendation.index[0]][f"Совет {num}"]
