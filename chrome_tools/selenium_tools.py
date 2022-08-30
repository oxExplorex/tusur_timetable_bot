from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver

from PIL import Image
from io import BytesIO
import asyncio

class Chrome:
    def __init__(self):
        self.driver = None
        self.chrome_options = webdriver.ChromeOptions()

        self.chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.chrome_options.add_experimental_option('useAutomationExtension', False)
        self.chrome_options.add_argument("--log-level=3")
        self.chrome_options.add_argument("--disable-notifications")
        self.chrome_options.add_experimental_option("prefs",
                                                    {"profile.default_content_setting_values.notifications": 2})
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument("--window-size=1920,1080")

    async def get_url(self, find_url):
        try:

            self.driver = webdriver.Chrome(executable_path="chrome_tools/chromedriver/chromedriver.exe",
                                           options=self.chrome_options)
            self.driver.get(find_url)
            return True
        except:
            return False

    async def get_page_source(self):
        return self.driver.page_source

    async def create_table_png(self):
        try:
            target = self.driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[6]/div[2]/div[3]/div/div[2]/ul/li[4]')

            actions = ActionChains(self.driver)
            actions.move_to_element(target)
            actions.perform()

            element = self.driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[6]/div[2]/div[3]/div')

            img = Image.open(BytesIO(element.screenshot_as_png))

            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            return img_byte_arr
        except:
            return False

    async def create_table_png_teacher(self):
        try:
            target = self.driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[6]/div[2]/div[3]/div/ul/li[3]')

            actions = ActionChains(self.driver)
            actions.move_to_element(target)
            actions.perform()

            element = self.driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[6]/div[2]/div[3]/div')

            img = Image.open(BytesIO(element.screenshot_as_png))

            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            return img_byte_arr
        except:
            return False

    async def create_choice_png(self):
        try:
            element = self.driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[6]')

            img = Image.open(BytesIO(element.screenshot_as_png))

            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            return img_byte_arr
        except:
            return False

    async def driver_quit(self):
        self.driver.quit()
