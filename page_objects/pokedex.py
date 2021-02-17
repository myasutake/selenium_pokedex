import logging

from selenium.webdriver.common.by import By

from page_objects.base import BasePage
from page_objects.base import BaseLoadingElement


class Page(BasePage):

    def __init__(self, driver):
        super().__init__(driver=driver, desc='Pokedex Page', url='https://www.pokemon.com/us/pokedex/')
        self._locators = dict()
        self._locators['loading_indicator'] = (By.CSS_SELECTOR, 'div.loader')
        return

    def accept_cookies(self):
        cookie_modal = CookieModal(driver=self.driver)

        if not cookie_modal.is_loaded():
            logging.debug(f"{cookie_modal.desc} is not displayed. No action needed.")
            return

        cookie_modal.click_ok_button()
        cookie_modal.wait_until_closed()
        return

    def loading_indicator_is_displayed(self):
        elements = self.driver.find_elements(*self._locators['loading_indicator'])
        if len(elements) == 0:
            return False
        else:
            return elements[0].is_displayed()

    def is_loaded(self):
        return not self.loading_indicator_is_displayed()


class CookieModal(BaseLoadingElement):

    def __init__(self, driver):
        super().__init__(driver=driver, desc="Cookie Modal")
        self._locators = dict()
        self._locators['cookie_modal'] = (By.CSS_SELECTOR, 'div.ot-sdk-container')
        self._locators['ok_button'] = (By.CSS_SELECTOR, '#onetrust-accept-btn-handler')
        return

    def click_ok_button(self):
        button = self.driver.find_element(*self._locators['ok_button'])
        logging.info(f"Clicking 'OK' on {self.desc}")
        button.click()
        return

    def is_loaded(self):
        elements = self.driver.find_elements(*self._locators['cookie_modal'])
        if len(elements) == 0:
            return False
        else:
            return elements[0].is_displayed()
