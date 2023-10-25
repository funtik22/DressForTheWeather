from natasha import (
    Segmenter,
    NewsEmbedding,
    NewsNERTagger,
    Doc
)
#Библиотека для распознования именнованных сущностей

segmenter = Segmenter()
emb = NewsEmbedding()
ner_tagger = NewsNERTagger(emb)

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
    turn.user_object["last_phrase"] = text


@csc.add_handler(priority=1000, regexp='что (надеть|одеть|одеться|выбрать)')
def drees_for_dress(turn: DialogTurn):
    text = (turn.text).title()
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_ner(ner_tagger)
    print(text)
    if doc.spans:
       turn.response_text = str(doc.spans[0].text)
    else:
       turn.response_text = "Город не найден!"


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

