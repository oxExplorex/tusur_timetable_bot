from chrome_tools.arsenic import browsers
from chrome_tools.arsenic.services import Chromedriver
from chrome_tools.arsenic.actions import Mouse, chain
from chrome_tools.arsenic import get_session

from chrome_tools.fix_log import set_arsenic_log_level

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline import delete_button, update_button_by_url

from utils.times import get_time_update

from data.config import PATH_BINARY

from urllib.parse import unquote
from bs4 import BeautifulSoup

from loguru import logger

import ujson
import os

set_arsenic_log_level()


class Chrome:
    def __init__(self):
        """self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.chrome_options.add_experimental_option('useAutomationExtension', False)
        self.chrome_options.add_experimental_option("prefs",
                                                    {"profile.default_content_setting_values.notifications": 2})"""

        self.chromedriver = Chromedriver(binary=PATH_BINARY)
        self.browser = browsers.Chrome(log_path=os.devnull)
        self.browser.capabilities = {"goog:chromeOptions": {"args": ["--headless", "--window-size=1920,1080",
                                                                     "--disable-dev-shm-usage",
                                                                     "--disable-extensions", "--disable-gpu",
                                                                     "--log-level=3" 
                                                                     "--disable-notifications",
                                                                     "--disable-blink-features=AutomationControlled"]}}

    async def get_table(self, find_url):
        try:
            result_dict = {
                            "photo": "",
                            "caption": "",
                            "caption2": "",
                            "reply_markup": "",
                            "reply_markup2": "",
                            "end_link": "",
                            "last_update": get_time_update()
            }
            async with get_session(self.chromedriver, self.browser) as session:
                await session.get(find_url)
                await session.wait_for_element(30, 'html')
                html = await session.get_page_source()
                end_link = unquote(await session.get_url())
                if "не дал результатов" in html:
                    result_dict['caption'] = 'Парсинг не дал результатов, повторите попытку'
                    result_dict['end_link'] = end_link
                    await session.close()
                    return result_dict
                elif "Результаты поиска" in html:
                    table = await session.get_element(
                        '#wrapper > div:nth-child(9) > div.row')

                    soup = BeautifulSoup(html, "lxml")
                    reply_markup = InlineKeyboardMarkup()
                    temp_button = []
                    for a in soup.find("ul", {"class": "list-inline"}).find_all("a"):
                        group_id = a.text
                        callback_data = 'get_' + a['href']  # faculties/fsu/groups/420-1
                        if len(temp_button) == 3:
                            a, b, c = temp_button
                            reply_markup.add(a, b, c)
                            temp_button = []
                        temp_button.append(InlineKeyboardButton(text=group_id, callback_data=callback_data))
                    if temp_button:
                        ltb = len(temp_button)
                        if ltb == 1:
                            reply_markup.add(temp_button[0])
                        elif ltb == 2:
                            a, b = temp_button
                            reply_markup.add(a, b)
                        elif ltb == 3:
                            a, b, c = temp_button
                            reply_markup.add(a, b, c)

                    reply_markup.add(update_button_by_url(end_link))
                    reply_markup.add(delete_button)

                    result_dict['photo'] = await table.get_screenshot()
                    result_dict['caption'] = "Выберете один их предложенных вариантов"
                    result_dict['reply_markup'] = ujson.loads(reply_markup.as_json())
                    result_dict['end_link'] = end_link
                    await session.close()
                    return result_dict
                elif "Расписание занятий группы" in html:
                    target = await session.get_element(
                        '#wrapper > div:nth-child(9) > div.timetable_wrapper > div:nth-child(3) > div > '
                        'div:nth-child(2) > ul > '
                        'li.training_type_practice.new-training-type-practice.margin-bottom-10')

                    mouse = Mouse()
                    actions = chain(mouse.move_to(target))
                    await session.perform_actions(actions)

                    table = await session.get_element(
                        '#wrapper > div:nth-child(9) > div.timetable_wrapper > div:nth-child(3) > div')

                    soup = BeautifulSoup(html, "lxml")
                    info = soup.find("title").text.split(" — ")[0]
                    more_info = soup.find("div", {"class": "col-md-12"}).text.replace("\n", "")

                    reply_markup = InlineKeyboardMarkup()
                    reply_markup.add(InlineKeyboardButton(text="Schedule link", url=end_link),
                                     update_button_by_url(end_link))
                    reply_markup.add(delete_button)

                    reply_markup2 = InlineKeyboardMarkup()
                    reply_markup2.add(delete_button)

                    caption2 = ""
                    for i in range(1, 8):
                        s = soup.find("tr", {"class": f"lesson_{i}"})
                        span_info = s.find("div", {"class": "hidden for_print"})
                        if span_info:
                            note_info = span_info.find("span", {"class": "note"})
                            if note_info:
                                name_lesson = s.find("abbr").text
                                caption2 += f"{note_info.text} - {name_lesson}\n"


                    result_dict['photo'] = await table.get_screenshot()
                    result_dict['caption'] = f"{info}\n<code>{more_info}</code>"
                    result_dict['caption2'] = caption2
                    result_dict['reply_markup'] = ujson.loads(reply_markup.as_json())
                    result_dict['reply_markup2'] = ujson.loads(reply_markup2.as_json())
                    result_dict['end_link'] = end_link
                    await session.close()
                    return result_dict
                elif "Расписание занятий преподавателя" in html:
                    target = await session.get_element(
                        '#wrapper > div:nth-child(9) > div.timetable_wrapper > div:nth-child(3) > div > ul > '
                        'li.training_type_practice.new-training-type-practice.margin-bottom-10')

                    mouse = Mouse()
                    actions = chain(mouse.move_to(target))
                    await session.perform_actions(actions)

                    table = await session.get_element(
                        '#wrapper > div:nth-child(9) > div.timetable_wrapper > div:nth-child(3) > div')


                    soup = BeautifulSoup(html, "lxml")
                    info = soup.find("title").text.split(" — ")[0]
                    more_info = soup.find("div", {"class": "col-md-12"}).text.replace("\n", "")

                    reply_markup = InlineKeyboardMarkup()
                    reply_markup.add(InlineKeyboardButton(text="Schedule link", url=end_link),
                                     update_button_by_url(end_link))
                    reply_markup.add(delete_button)

                    reply_markup2 = InlineKeyboardMarkup()
                    reply_markup2.add(delete_button)

                    caption2 = ""
                    for i in range(1, 8):
                        s = soup.find("tr", {"class": f"lesson_{i}"})
                        span_info = s.find("div", {"class": "hidden for_print"})
                        if span_info:
                            note_info = span_info.find("span", {"class": "note"})
                            if note_info:
                                name_lesson = s.find("abbr").text
                                caption2 += f"{note_info.text} - {name_lesson}\n"


                    result_dict['photo'] = await table.get_screenshot()
                    result_dict['caption'] = f"{info}\n<code>{more_info}</code>\n"
                    result_dict['caption2'] = caption2
                    result_dict['reply_markup'] = ujson.loads(reply_markup.as_json())
                    result_dict['reply_markup2'] = ujson.loads(reply_markup2.as_json())
                    result_dict['end_link'] = end_link
                    await session.close()
                    return result_dict
                elif "Расписание занятий в аудитории" in html:
                    target = await session.get_element(
                        '#wrapper > div:nth-child(9) > div.timetable_wrapper > '
                        'div:nth-child(3) > div > ul > '
                        'li.training_type_practice.new-training-type-practice.margin-bottom-10')

                    mouse = Mouse()
                    actions = chain(mouse.move_to(target))
                    await session.perform_actions(actions)

                    table = await session.get_element(
                        '#wrapper > div:nth-child(9) > div.timetable_wrapper > div:nth-child(3) > div')


                    soup = BeautifulSoup(html, "lxml")
                    info = soup.find("title").text.split(" — ")[0]
                    more_info = soup.find("div", {"class": "col-md-12"}).text.replace("\n", "")

                    reply_markup = InlineKeyboardMarkup()
                    reply_markup.add(InlineKeyboardButton(text="Schedule link", url=end_link),
                                     update_button_by_url(end_link))

                    reply_markup.add(delete_button)

                    reply_markup2 = InlineKeyboardMarkup()
                    reply_markup2.add(delete_button)

                    caption2 = ""
                    for i in range(1, 8):
                        s = soup.find("tr", {"class": f"lesson_{i}"})
                        span_info = s.find("div", {"class": "hidden for_print"})
                        if span_info:
                            note_info = span_info.find("span", {"class": "note"})
                            if note_info:
                                name_lesson = s.find("abbr").text
                                caption2 += f"{note_info.text} - {name_lesson}\n"


                    result_dict['photo'] = await table.get_screenshot()
                    result_dict['caption'] = f"{info}\n<code>{more_info}</code>"
                    result_dict['caption2'] = caption2
                    result_dict['reply_markup'] = ujson.loads(reply_markup.as_json())
                    result_dict['reply_markup2'] = ujson.loads(reply_markup2.as_json())
                    result_dict['end_link'] = end_link
                    await session.close()
                    return result_dict
                else:

                    result_dict['caption'] = "Неизвестная ошибка, повторите запрос"
                    result_dict['end_link'] = end_link
                    result_dict['error'] = ""
                    await session.close()
                    return result_dict

        except Exception as e:
            logger.error(e)
            return False

