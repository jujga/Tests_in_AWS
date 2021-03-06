# не смог одолеть проблему циклического импорта,
# потому все пейжобжекты поместил в один файл

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.utilities.utils import DriverForAllure
from tests.utilities import utils
import allure
import datetime


class BasePage(object):
    # базовая страница. типа абстрактный класс
    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(5)
        self.wait = WebDriverWait(driver, 10)

    @allure.step('Go back')
    def click_browser_back_button(self):
        self.driver.back()
        do_allure_screenshot(f'Previous page')

    @staticmethod
    def good_name_text(web_item):
        return web_item.find_element(
            By.XPATH, './/span[@data-qaid="product_name"]').text

    @property
    def sign_in_link(self):
        return self.driver.find_element(By.XPATH,
                                        '//button[@data-qaid="sign-in"]')

    @property
    def email_button(self):
        return self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//div[@data-qaid="email_btn"]')))

    @property
    def email_field(self):
        return self.driver.find_element(By.XPATH,
                                        '//input[@id="email_field"]')

    @property
    def next_button(self):
        return self.driver.find_element(By.XPATH,
                                        '//button[@id="emailConfirmButton"]')

    @property
    def password_field(self):
        return self.driver.find_element(By.XPATH,
                                        '//input[@id="enterPassword"]')

    @property
    def submit_button(self):
        return self.driver.find_element(
            By.XPATH, '//button[@id="enterPasswordConfirmButton"]')

    def submit_button_click(self):
        self.submit_button.click()

    def go_logined_page(self):
        return LoginedPage(self.driver)

    @staticmethod
    @allure.step('Clicking on a heart button on the goods with index {1}')
    def click_goods_heart_button(web_item_list, goods_index):
        web_item_list[goods_index].find_element(By.XPATH, './/span[@data-qaid="add_favorite"]').click()
        do_allure_screenshot(f'After clicking on the {goods_index}-th goods/s heart button')


class MainPage(BasePage):
    # основная страница до логина
    def __init__(self, driver):
        super().__init__(driver)

    @property
    def goods_list(self):
        # эксплисит ждет, пока не появится список товаров
        return self.wait.until(EC.visibility_of_any_elements_located(
            (By.XPATH, '//div[@data-qaid="product_block"]')))


class LoginedPage(MainPage):
    # страница, когда залогинены
    def __init__(self, driver):
        super().__init__(driver)

    @property
    def fav_page_button(self):
        return self.driver.find_element(
            By.XPATH, '//button[@data-qaid = "favorite_cabinet_button"]')

    @allure.step('Jump to favorite page')
    def click_fav_page_button(self):
        self.fav_page_button.click()
        do_allure_screenshot('Favorite page')
        return FavoritePage(self.driver)

    @allure.step('Enter into goods details by clicking on the goods with index {1}')
    def click_on_goods(self, i):
        self.goods_list[i].click()
        do_allure_screenshot('Goods details')
        return GoodsDetail(self.driver)

    @property
    def fav_button_counter_text(self):
        return self.driver.find_element(By.XPATH,
                                        '//div[@data-qaid="counter"]').text

    @allure.step('Clicking on a heart button on the goods with index {2}')
    def click_goods_heart_button(self, web_item_list, goods_index):
        time_to_press_heart_button = 5

        def is_heart_picked():
            heart_button = operable_goods.find_element(By.XPATH, './/span[@data-qaid="add_favorite"]')
            heart_dom_attrs = heart_button.get_dom_attribute('data-tg-clicked')
            return False if ':"off",' in heart_dom_attrs else True

        def is_heart_state_changed(is_prev_heart_state):
            """Do REST POST request to make sure goods is added/removed to the favorites"""
            import requests
            url = "https://my.prom.ua/cabinet/user/graphql"
            headers = {
                'Cookie': '; '.join([cookie['name'] + '=' + cookie['value'] for cookie in self.driver.get_cookies()]),
                'x-requested-with': 'XMLHttpRequest',
                'Content-Type': 'application/json'}
            response = requests.request("POST", url, headers=headers, data=utils.payload)
            is_in_fav = True if BasePage.good_name_text(operable_goods) in response.text else False
            return is_in_fav ^ is_prev_heart_state

        operable_goods = web_item_list[goods_index]
        is_heart_picked_prev = is_heart_picked()
        click_time = datetime.datetime.now().timestamp()
        operable_goods.find_element(By.XPATH, './/span[@data-qaid="add_favorite"]').click()
        # while not is_heart_state_changed(is_heart_picked_prev):
        #     if datetime.datetime.now().timestamp() - click_time > time_to_press_heart_button:
        #         do_allure_screenshot(f'Time out ({time_to_press_heart_button}s) after clicking on the heart button')
        #         raise ConnectionError('Global problem about adding/removing goods to/from favorites.'
        #                               'Please check internet connection or accessibility of site')
        do_allure_screenshot(f'After clicking on the {goods_index}-th goods/s heart button')


class FavoritePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    @property
    def fav_button_counter_text(self):
        return self.driver.find_element(
            By.XPATH, '//div[@data-qaid="counter"]//span').text

    @property
    def del_favs_button(self):
        return self.driver.find_elements(By.XPATH,
                                         '//span[@data-qaid="delete_icon"]')

    @property
    def fav_list(self):
        return self.driver.find_elements(By.XPATH,
                                         '//a[@data-qaid="product_name"]')


class GoodsDetail(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    @property
    def fav_add_button(self):
        return self.driver.find_element(By.XPATH,
                                        '//span[@data-qaid="add_favorite"]')

    @allure.step("Clicking on a heart button on the goods's detail")
    def click_fav_add_button(self):
        self.fav_add_button.click()
        do_allure_screenshot(f'After clicking on the heart button')

    @property
    def good_code_text(self):
        return self.driver.find_element(
            By.XPATH, '//span[@data-qaid="product-sku"]').text

    @property
    def good_name_txt(self):
        return self.driver.find_element(
            By.XPATH, '//h1[@data-qaid="product_name"]').text


# HELPERS
def do_allure_screenshot(name):
    allure.attach(DriverForAllure.driver.get_screenshot_as_png(),
                  name=name,
                  attachment_type=allure.attachment_type.PNG)
