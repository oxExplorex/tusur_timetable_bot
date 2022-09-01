from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from chrome_tools.arsenic import browsers
from chrome_tools.arsenic.services import Chromedriver
from chrome_tools.arsenic.actions import Mouse, chain
from chrome_tools.arsenic import get_session

from bs4 import BeautifulSoup

from chrome_tools.fix_log import set_arsenic_log_level

import os

set_arsenic_log_level()


class Chrome:
    def __init__(self):
        """self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.chrome_options.add_experimental_option('useAutomationExtension', False)
        self.chrome_options.add_experimental_option("prefs",
                                                    {"profile.default_content_setting_values.notifications": 2})"""


        path_binary = r"C:\My_project\timetable_tusur\chrome_tools\chromedriver\chromedriver.exe"
        self.chromedriver = Chromedriver(binary=path_binary)
        self.browser = browsers.Chrome(log_path=os.devnull)
        self.browser.capabilities = {"goog:chromeOptions": {"args": [ "--headless", "--window-size=1920,1080",
                                                                     "--disable-dev-shm-usage",
                                                                     "--disable-extensions", "--disable-gpu",
                                                                     "--log-level=3" 
                                                                     "--disable-notifications",
                                                                     "--disable-blink-features=AutomationControlled"]}}

    async def get_table(self, find_url):
        try:
            async with get_session(self.chromedriver, self.browser) as session:
                await session.get(find_url)
                await session.wait_for_element(20, 'html')
                html = await session.get_page_source()
                end_link = await session.get_url()
                if "не дал результатов" in html:
                    return {"photo": "", "caption": "Парсинг не дал результатов, повторите попытку"}
                elif "Результаты поиска" in html:
                    table = await session.get_element(
                        '#wrapper > div:nth-child(9) > div.row')

                    soup = BeautifulSoup(html, "lxml")
                    reply_markup = InlineKeyboardMarkup()
                    temp_button = []
                    for a in soup.find("ul", {"class": "list-inline"}).find_all("a"):
                        group_id = a.text
                        callback_data = 'get_https://timetable.tusur.ru' + a['href']  # faculties/fsu/groups/420-1
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

                    reply_markup.add(InlineKeyboardButton(text="✖️", callback_data="delete_message"))

                    return {"photo": await table.get_screenshot(),
                            "caption": "Выберете один их предложенных вариантов",
                            "reply_markup": reply_markup}
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
                    reply_markup.add(InlineKeyboardButton(text="Schedule link", url=end_link))
                    reply_markup.add(InlineKeyboardButton(text="✖️", callback_data="delete_message"))

                    reply_markup2 = InlineKeyboardMarkup()
                    reply_markup2.add(InlineKeyboardButton(text="✖️", callback_data="delete_message"))

                    caption2 = ""
                    for i in range(1, 8):
                        s = soup.find("tr", {"class": f"lesson_{i}"})
                        span_info = s.find("div", {"class": "hidden for_print"})
                        if span_info:
                            note_info = span_info.find("span", {"class": "note"})
                            if note_info:
                                name_lesson = s.find("abbr").text
                                caption2 += f"{note_info.text} - {name_lesson}\n"

                    return {"photo": await table.get_screenshot(),
                            "caption": f"{info}\n<code>{more_info}</code>",
                            "caption2": caption2,
                            "reply_markup": reply_markup,
                            "reply_markup2": reply_markup2}
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
                    reply_markup.add(InlineKeyboardButton(text="Schedule link", url=end_link))
                    reply_markup.add(InlineKeyboardButton(text="✖️", callback_data="delete_message"))

                    reply_markup2 = InlineKeyboardMarkup()
                    reply_markup2.add(InlineKeyboardButton(text="✖️", callback_data="delete_message"))

                    caption2 = ""
                    for i in range(1, 8):
                        s = soup.find("tr", {"class": f"lesson_{i}"})
                        span_info = s.find("div", {"class": "hidden for_print"})
                        if span_info:
                            note_info = span_info.find("span", {"class": "note"})
                            if note_info:
                                name_lesson = s.find("abbr").text
                                caption2 += f"{note_info.text} - {name_lesson}\n"

                    return {"photo": await table.get_screenshot(),
                            "caption": f"{info}\n<code>{more_info}</code>\n{end_link}",
                            "caption2": caption2,
                            "reply_markup": reply_markup,
                            "reply_markup2": reply_markup2}
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
                    reply_markup.add(InlineKeyboardButton(text="Schedule link", url=end_link))
                    reply_markup.add(InlineKeyboardButton(text="✖️", callback_data="delete_message"))

                    reply_markup2 = InlineKeyboardMarkup()
                    reply_markup2.add(InlineKeyboardButton(text="✖️", callback_data="delete_message"))

                    caption2 = ""
                    for i in range(1, 8):
                        s = soup.find("tr", {"class": f"lesson_{i}"})
                        span_info = s.find("div", {"class": "hidden for_print"})
                        if span_info:
                            note_info = span_info.find("span", {"class": "note"})
                            if note_info:
                                name_lesson = s.find("abbr").text
                                caption2 += f"{note_info.text} - {name_lesson}\n"

                    return {"photo": await table.get_screenshot(),
                            "caption": f"{info}\n<code>{more_info}</code>",
                            "caption2": caption2,
                            "reply_markup": reply_markup,
                            "reply_markup2": reply_markup2}
                else:
                    return {"photo": "", "caption": "Неизвестная ошибка"}
        except Exception as e:
            print(e)
            return False

