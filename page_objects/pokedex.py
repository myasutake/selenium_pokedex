import logging

from selenium.webdriver.common.by import By

from page_objects.base import BaseElement
from page_objects.base import BaseLoadingElement
from page_objects.base import BasePage


class Page(BasePage):

    def __init__(self, driver):
        super().__init__(driver=driver, desc='Pokedex Page', url='https://www.pokemon.com/us/pokedex/')
        self._locators = dict()
        self._locators['loading_indicator'] = (By.CSS_SELECTOR, 'div.loader')
        self._locators['search_result'] = (By.CSS_SELECTOR, 'li.animating')
        return

    # Search Results

    @property
    def number_of_results(self):
        return len(self._find_search_result_objects())

    def _find_search_result_objects(self):
        elements = self.driver.find_elements(*self._locators['search_result'])
        return [SearchResult(i) for i in elements]

    # Misc

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


class SearchResult(BaseElement):

    def __init__(self, element):
        super().__init__(element=element, desc='Search Result')

        self._locators = dict()
        self._locators['name'] = (By.CSS_SELECTOR, 'h5')
        self._locators['number'] = (By.CSS_SELECTOR, 'p.id')

        self.desc = f"Search Result - {self.number} {self.name}"
        return

    @property
    def name(self):
        return self.element.find_element(*self._locators['name']).text

    @property
    def number(self):
        return self.element.find_element(*self._locators['number']).text

    def __str__(self):
        return self.desc


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
