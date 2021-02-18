import logging
import time

from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.by import By

from page_objects.base import BaseElement
from page_objects.base import BaseLoadingElement
from page_objects.base import BasePage
from page_objects.base import TextInput


class Page(BasePage):

    def __init__(self, driver):
        super().__init__(driver=driver, desc='Pokedex Page', url='https://www.pokemon.com/us/pokedex/')
        self._locators = dict()
        self._locators['execute_search_button'] = (By.CSS_SELECTOR, 'input.button-search')
        self._locators['loading_indicator'] = (By.CSS_SELECTOR, 'div.loader')
        self._locators['no_results'] = (By.CSS_SELECTOR, 'div.no-results')
        self._locators['search_field'] = (By.CSS_SELECTOR, '#searchInput')
        self._locators['search_result'] = (By.CSS_SELECTOR, 'li.animating')
        self._locators['sort_dropdown'] = (By.CSS_SELECTOR, 'section.overflow-visible > div > div > div.custom-select-menu')
        return

    # Basic Filters

    def click_execute_search_button(self):
        element = self.driver.find_element(*self._locators['execute_search_button'])
        logging.info("Clicking execute search button.")
        element.click()
        return

    def find_search_field_text_input_object(self):
        element = self.driver.find_element(*self._locators['search_field'])
        return TextInput(element)

    def find_sort_dropdown_object(self):
        element = self.driver.find_element(*self._locators['sort_dropdown'])
        return SortDropdown(element=element)

    # Search Results

    def all_search_results_names_displayed(self):
        results = self.find_search_result_objects()
        return [i.name for i in results]

    def all_search_results_numbers_displayed(self):
        results = self.find_search_result_objects()
        return [i.number for i in results]

    def no_results_found(self):
        return self.driver.find_element(*self._locators['no_results']).is_displayed()

    @property
    def number_of_results(self):
        return len(self.find_search_result_objects())

    def find_search_result_objects(self):
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


class SortDropdown(BaseElement):

    def __init__(self, element):
        super().__init__(element=element, desc='Sort Dropdown')
        self._locators = dict()
        self._locators['current_option'] = (By.CSS_SELECTOR, 'label')
        self._locators['option'] = (By.CSS_SELECTOR, 'li')
        return

    # Displaying Options

    def click_dropdown(self):
        logging.info(f"Clicking {self.desc}.")
        self.element.click()
        time.sleep(0.1)
        return

    def display_options(self):
        if self.options_are_displayed():
            logging.debug('Options are already displayed. No action needed.')
            return
        self.click_dropdown()
        return

    def options_are_displayed(self):
        label_element = self.element.find_element(*self._locators['current_option'])
        return 'opened' in label_element.get_attribute('class')

    def _verify_options_are_displayed(self):
        if not self.options_are_displayed():
            log_str = "Options are not displayed."
            logging.error(log_str)
            raise ElementNotVisibleException(log_str)
        return

    # Setting/Getting Options

    def click_option(self, option):
        self._verify_options_are_displayed()
        self._verify_option_exists(option)

        element = self._find_option_element(option=option)
        logging.info(f"Clicking sort option '{option}'.")
        element.click()
        return

    def _find_option_element(self, option):
        self._verify_options_are_displayed()

        elements = self.element.find_elements(*self._locators['option'])
        for i in elements:
            if option.lower() == i.text.lower():
                return i

        log_str = f"Invalid option '{option}' specified."
        logging.error(log_str)
        raise ValueError(log_str)

    @property
    def selected_option(self):
        return self.element.find_element(*self._locators['current_option']).text

    @selected_option.setter
    def selected_option(self, option):
        self.display_options()
        self._verify_option_exists(option=option)
        self.click_option(option=option)
        return

    def _verify_option_exists(self, option):
        self._find_option_element(option=option)
        return


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
