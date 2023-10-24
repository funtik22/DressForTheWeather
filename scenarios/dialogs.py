from dialogic import COMMANDS
from dialogic.cascade import DialogTurn

from dm import csc

import json
import random

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
@csc.add_handler(priority=3, checker=is_new_session)
def hello(turn: DialogTurn):
    text = random.choice(info['hello'])
    text = f'<speaker audio="alice-sounds-game-powerup-1.opus"> <text>{text}</text><voice>{text}</voice>'
    turn.response_text = text
    turn.user_object['last_phrase'] = text


@csc.add_handler(priority=1000, intents=['ability'])
def show_rules(turn: DialogTurn):
    turn.response_text = info['ability']
    turn.user_object['last_phrase'] = info['ability']


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
@csc.add_handler(priority=100, intents=['gender_M'])
def gender_M (turn: DialogTurn):
    turn.user_object['gender'] = "M"

@csc.add_handler(priority=100, intents=['gender_W'])
def gender_W (turn: DialogTurn):
    turn.user_object['gender'] = "W"

