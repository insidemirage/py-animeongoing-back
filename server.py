from aiohttp import web
import sys
from database import AnimevostBase
import asyncio
import json
# Дефолтный запрос к серверу
WEEKDAYS = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье', 'Не стабильный релиз']

async def serverside(request):
    return web.Response(text ='hello')


# Запрос аниме
async def getanime(request):
  name = request.match_info.get('name')
  info = animevost.get_one(name)
  try:
    animeinfo = {'name' : info['name'], 'day' : WEEKDAYS[info['day']], 'epnow' : info['epnow'], 'link' : info['link']}
  # animeinfo = json.dumps(animeinfo)
  except:
    return web.Response(text='Error')

  return web.json_response(animeinfo)


animevost = AnimevostBase('anilibria')
app = web.Application()
app.add_routes([web.get('/', serverside), web.get('/anime/{name}', getanime)])
if __name__ == '__main__':
    web.run_app(app, port=3003)
