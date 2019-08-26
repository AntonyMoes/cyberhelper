from urllib.parse import quote
import aiohttp
from selectolax.parser import HTMLParser

from utils import user_agent

domain = 'https://www.yandex.ru'
weather_request = '/pogoda/search?request='


async def get_weather(location: str) -> str:
    async with aiohttp.request('GET', domain + weather_request + quote(location), headers={'User-Agent': user_agent}) as resp:
        search_text = await resp.text()
        title = HTMLParser(search_text).css_first('title').text()
        possible_href = str(resp.url)

    if title != 'Яндекс.Погода':
        # if we got rerouted to weather
        weather_text = search_text
        exact_location = ''
        for node in HTMLParser(weather_text).css('span.breadcrumbs__title'):
            exact_location += node.text() + ','
        exact_location = exact_location[:-1]
        href = possible_href
    else:
        # if we got location list as we expected
        node = HTMLParser(search_text).css_first('div.grid__cell')
        if node is None:
            return f'По запросу "{location}" ничего не найдено'
        node = node.css_first('li.place-list__item')
        node = node.css_first('a')
        href = domain + node.attributes['href']
        exact_location = node.text()
        async with aiohttp.request('GET', href, headers={'User-Agent': user_agent}) as resp:
            weather_text = await resp.text()

    # parsing weather
    card = HTMLParser(weather_text).css_first('div.content__main').css_first('div.content__row').css_first('div.card')
    temp_info = card.css_first('div.fact__temp-wrap').css_first('a')
    now_temp = temp_info.css_first('div.fact__temp').css_first('span.temp__value').text()
    now_condition = temp_info.css_first('div.fact__feelings').css_first('div.link__condition').text()
    wind_info = card.css_first('div.fact__props').css_first('dl.fact__wind-speed').css_first('dd.term__value')
    now_wind = wind_info.css_first('span.wind-speed').text() + ' ' + wind_info.css_first('span.fact__unit').text()

    day_info = HTMLParser(weather_text).css_first('div.forecast-briefly').css_first('div.swiper-wrapper')
    # print(day_info.html)
    slide = None
    for day in day_info.css('div.swiper-slide'):
        text: str = day.text()
        if text.find('Сегодня') != -1:
            slide = day.css_first('a')

    day_temp = slide.css_first('div.forecast-briefly__temp_day').css_first('span.temp__value').text()
    night_temp = slide.css_first('div.forecast-briefly__temp_night').css_first('span.temp__value').text()
    condition = slide.css_first('div.forecast-briefly__condition').text()

    return f'Место: {exact_location}' \
           f'\n\nCЕЙЧАС:\nТемпература: {now_temp}\nСостояние: {now_condition}\nВетер: {now_wind}' \
           f'\n\nCЕГОДНЯ:\nТемпература днем: {day_temp}\nТемпература ночью: {night_temp}\nСостояние: {condition}'\
           f'\n\nПолный прогноз: {href}'
