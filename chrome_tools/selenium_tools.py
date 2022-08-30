from arsenic import browsers
from arsenic.services import Chromedriver
from arsenic.actions import Mouse, chain
from arsenic import get_session

from bs4 import BeautifulSoup


class Chrome:
    def __init__(self):
        """self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.chrome_options.add_experimental_option('useAutomationExtension', False)
        self.chrome_options.add_experimental_option("prefs",
                                                    {"profile.default_content_setting_values.notifications": 2})"""

        path_binary = r"C:\My_project\timetable_tusur\chrome_tools\chromedriver\chromedriver.exe"
        self.chromedriver = Chromedriver(binary=path_binary)
        self.browser = browsers.Chrome()
        self.browser.capabilities = {"goog:chromeOptions": {"args": ["--headless", "--window-size=1920,1080",
                                                                     "--disable-dev-shm-usage",
                                                                     "--disable-extensions", "--disable-gpu",
                                                                     "--log-level=3", "--disable-notifications",
                                                                     "--disable-blink-features=AutomationControlled"]}}

    async def get_table(self, find_url):
        try:
            async with get_session(self.chromedriver, self.browser) as session:
                await session.get(find_url)
                await session.wait_for_element(20, 'html')
                html = await session.get_page_source()

                if "не дал результатов" in html:
                    return {"photo": "", "caption": "Парсинг не дал результатов, повторите попытку"}
                elif "Результаты поиска" in html:
                    table = await session.get_element(
                        '#wrapper > div:nth-child(9) > div.row')
                    return {"photo": await table.get_screenshot(),
                            "caption": "Повторите запрос одним из предложенных вариантов"}
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

                    return {"photo": await table.get_screenshot(), "caption": f"{info}\n<code>{more_info}</code>"}
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

                    return {"photo": await table.get_screenshot(), "caption": f"{info}\n<code>{more_info}</code>"}
                else:
                    return {"photo": "", "caption": "Неизвестная ошибка"}
        except Exception as e:
            print(e)
            return False

