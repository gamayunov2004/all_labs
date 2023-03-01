import requests

s_city = "Moscow,RU"
appid  = "014668d9f9f89dcf0d8c5d84aff4cd86"

res = requests.get("http://api.openweathermap.org/data/2.5/weather?lat=55.751244&lon=37.618423&appid=014668d9f9f89dcf0d8c5d84aff4cd86",
                   params={'q':s_city,'units':'metric','lang':'ru','APPID':appid})
data = res.json()

print("Город:", s_city)
print("Прогноз погоды на сегодня:")
print("Погодные условия:", data['weather'][0]['description'])
print("Температура:", data['main']['temp'])
print("Минимальная температура:", data['main']['temp_min'])
print("Максимальная температура", data['main']['temp_max'])
print("Скорость ветра:", data['wind']['speed'])
print("Видимость:", data['visibility'])

res2=requests.get("http://api.openweathermap.org/data/2.5/forecast?lat=55.751244&lon=37.618423&appid=014668d9f9f89dcf0d8c5d84aff4cd86",
                  params={'q':s_city,'units':'metric','lang':'ru','APPID':appid})
data2=res2.json()
print("\nПрогноз погоды на неделю:")
for i in data2['list']:
    print("Дата <", i['dt_txt'], ">"
        " \r\nПогодные условия <", i['weather'][0]['description'], ">"
        " \r\nТемпература <", '{0:+3.0f}'.format(i['main']['temp']), ">"
        " \r\nСкорость ветра <", i['wind']['speed'], ">"
        " \r\nВидимость <", i['visibility'], ">")
    print("____________________________")
