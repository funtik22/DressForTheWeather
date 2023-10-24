import pandas as pd
import random

gender = ''

if gender == 'Мужской':
    man = pd.read_excel("tempman.xlsx")
elif gender == 'Женский':
    man = pd.read_excel("tempwoman.xlsx")
##else:



temp = random.randint(-50, 50)
rain = random.randint(0, 1)
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


if rain:
    turn.response_text = recommendation.loc[recommendation.index[0]][f"Совет {num}"],'\n', if_rain.loc[if_rain.index[0]]["Доп. совет в случае дождя"]
else:
    turn.response_text = recommendation.loc[recommendation.index[0]][f"Совет {num}"]







