"""
Contains definitions for all base classes and standard HTML elements.

Some pages are small and simple enough to use a single BasePage object
to represent the entire page. However, two very common general
situations warrant multiple objects:
* A page is too big/complex and gets "bigger than your head."
* An element, regardless of complexity, with a given internal structure
  appears in multiple areas. Could be on different pages (e.g. a menu nav)
  or on the same page (e.g. HTML list items).
"""

import logging
import time

from selenium.webdriver.common.by import By


# Base Classes


class BaseDesc:

    def __init__(self, desc=None):
        self._desc = desc
        return

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, value):
        self._desc = value
        return


class Loading(BaseDesc):
    """
    Defines methods for elements with a loading state.

    Not to be instantiated directly.
    """

    def __init__(self, desc='loading element'):
        super().__init__(desc=desc)
        return

    def is_loaded(self):
        """
        Checks to see if the element is loaded.

        :returns bool:
        """
        # Override this method definition in your subclass.
        log_str = 'Subclasses of Loading must override is_loaded().'
        logging.error(log_str)
        raise NotImplementedError(log_str)

    def is_displayed(self):
        """
        See: is_loaded()
        """
        return self.is_loaded()

    def wait_until_loaded(self, time_limit=5.0, must_load=True):
        """
        Waits for the element to load.

        :param number time_limit: Max time to wait for the element to load.
        :param bool must_load: see next line.
        :raises TimeoutError if time_limit elapses AND must_load is True
        :returns None:
        """
        end_time = time.time() + time_limit
        while time.time() < end_time:
            time.sleep(0.5)
            if self.is_loaded():
                return
        log_str = '{} did not load.'.format(self.desc)
        if must_load is True:
            logging.error(log_str)
            raise TimeoutError(log_str)
        else:
            logging.warning(log_str)
            return

    def wait_until_displayed(self, time_limit=5.0, must_display=True):
        """
        See: wait_until_loaded()
        """
        return self.wait_until_loaded(time_limit=time_limit, must_load=must_display)

    def wait_until_closed(self, time_limit=5.0, must_close=True):
        """
        Waits for the element to close.

        :param number time_limit: Max time to wait for the element to close.
        :param bool must_close: see next line.
        :raises TimeoutError if time_limit elapses AND must_close is True
        :returns None:
        """
        end_time = time.time() + time_limit
        while time.time() < end_time:
            time.sleep(0.5)
            if not self.is_loaded():
                return
        log_str = '{} did not close.'.format(self.desc)
        if must_close is True:
            logging.error(log_str)
            raise TimeoutError(log_str)
        else:
            logging.warning(log_str)
            return


class Expanding(BaseDesc):
    """
    Defines methods for elements with expanded/collapsed states.

    Not to be instantiated directly.
    """

    def __init__(self, desc='expanding element'):
        super().__init__(desc=desc)
        return

    def is_expanded(self):
        """
        Checks to see if the element is loaded.

        :returns bool:
        """
        # Override this method definition in your subclass.
        log_str = 'Subclasses of Loading must override is_expanded().'
        logging.error(log_str)
        raise NotImplementedError(log_str)

    def wait_until_expanded(self, time_limit=5.0, must_expand=True):
        """
        Waits for the element to expand.

        :param number time_limit: Max time to wait for the element to expand.
        :param bool must_expand: see next line.
        :raises TimeoutError if time_limit elapses AND must_expand is True
        :returns None:
        """
        end_time = time.time() + time_limit
        while time.time() < end_time:
            time.sleep(0.5)
            if self.is_expanded():
                return
        log_str = '{} did not expand.'.format(self.desc)
        if must_expand is True:
            logging.error(log_str)
            raise TimeoutError(log_str)
        else:
            logging.warning(log_str)
            return

    def wait_until_collapsed(self, time_limit=5.0, must_collapse=True):
        """
        Waits for the element to collapse.

        :param number time_limit: Max time to wait for the element to collapse.
        :param bool must_collapse: see next line.
        :raises TimeoutError if time_limit elapses AND must_collapse is True
        :returns None:
        """
        end_time = time.time() + time_limit
        while time.time() < end_time:
            time.sleep(0.5)
            if not self.is_expanded():
                return
        log_str = '{} did not collapse.'.format(self.desc)
        if must_collapse is True:
            logging.error(log_str)
            raise TimeoutError(log_str)
        else:
            logging.warning(log_str)
            return


class BaseElement(BaseDesc):
    """
    Extends a WebElement object, represents an HTML element.

    This class must be init with either a WebDriver or WebElement.
    * If the class represents a unique element, it may be init with
      either WebDriver or WebElement.
    * If the class represents an element which appears in multiple
      locations, it must be init with WebElement.
    * If init with WebElement, the element must be found first
      via WebDriver.find_element() or WebDriver.find_elements().

    :attribute WebDriver driver:
    :attribute WebElement element:
    :attribute str desc: Description of the element.
    """

    def __init__(self, driver=None, element=None, desc='element'):
        super().__init__(desc=desc)
        if driver is None and element is None:
            log_str = 'Neither a WebDriver nor a WebElement was given to instantiate this object.'
            logging.error(log_str)
            raise TypeError(log_str)
        if driver is None:
            self._driver = element.parent
        else:
            self._driver = driver
        self._element = element
        return

    @property
    def driver(self):
        return self._driver

    @property
    def element(self):
        return self._element

    def is_displayed(self):
        self._verify_element_is_defined()
        return self._element.is_displayed()

    # Highlight

    def highlight(self, duration=3.0):
        """
        Highlights the element. Helpful for debugging locators.

        :param number duration: Duration (in seconds) to highlight the WebElement.
        :returns None:
        """
        self._verify_element_is_defined()
        original_style = self.element.get_attribute('style')
        highlighted_style = "border: 2px solid red; border-style: dashed;"
        self._alternate_styles(original_style, highlighted_style, duration)
        return

    def _alternate_styles(self, style_value_1, style_value_2, duration):
        end_time = time.time() + duration
        while time.time() < end_time:
            # Make sure the flashing ends on the original value, otherwise you end up with
            #   the element permanently highlighted.
            self._set_style(style_value=style_value_2)
            time.sleep(0.2)
            self._set_style(style_value=style_value_1)
            time.sleep(0.2)
        return

    def _set_style(self, style_value):
        self._verify_element_is_defined()
        self.driver.execute_script(
            "arguments[0].setAttribute(arguments[1], arguments[2])",
            self.element,
            "style",
            style_value
        )
        return

    # Misc

    def _verify_element_is_defined(self):
        if self.element is None:
            log_str = 'self.element must be defined before this method can be called.'
            logging.error(log_str)
            raise AttributeError(log_str)


class BaseLoadingElement(Loading, BaseElement):
    """
    Represents a BaseElement with a loading state.
    """

    def __init__(self, driver=None, element=None, desc='base loading element'):
        Loading.__init__(self=self, desc=desc)
        BaseElement.__init__(self=self, driver=driver, element=element, desc=desc)
        return


class BaseExpandingElement(Expanding, BaseElement):
    """
    Represents a BaseElement with expanded/collapsed states.
    """

    def __init__(self, driver=None, element=None, desc='base expanding element'):
        Expanding.__init__(self=self, desc=desc)
        BaseElement.__init__(self=self, driver=driver, element=element, desc=desc)
        return


class BasePage(BaseLoadingElement):
    """
    Extends a WebDriver object, represents an entire page.

    :attribute WebDriver driver:
    :attribute str url: URL which this page represents.
    :attribute str desc: Description of the page.
    """

    def __init__(self, driver, url=None, desc='page'):
        super().__init__(driver=driver, element=None, desc=desc)
        self._url = url
        return

    @property
    def url(self):
        return self._url

    def load(self, time_limit=5.0):
        """
        Directly opens the page, then waits for the page to load.

        :param number time_limit: Max time to wait for the element to load.
            The actual wait time is longer than this, since the driver.get()
            method doesn't return control until the _browser_ thinks the
            page has loaded (i.e. the reload button enables itself). We still
            need to call our own wait_for_load method since there may be
            other elements on the screen that need to be loaded.
        """
        if self._url is None:
            log_str = 'This class has no URL attribute defined.'
            logging.error(log_str)
            raise AttributeError(log_str)
        logging.info('Directly loading {}.'.format(self.desc))
        self.driver.get(self._url)
        self.wait_until_loaded(time_limit=time_limit)
        return


# Standard HTML Elements


# # Input Types


class Input(BaseElement):
    """
    Represents an <input> HTML element.
    """

    def __init__(self, element, desc='input'):
        super().__init__(element=element, desc=desc)
        return

    def is_required(self):
        """
        :returns bool if element has 'required' attribute type.
        """
        if self.element.get_attribute('required') == 'true':
            return True
        return False

    def _verify_type(self, input_type):
        if self.element.tag_name != 'input':
            log_str = "Class initialized with element type '{}'; expected 'input'.".format(self.element.tag_name)
            logging.error(log_str)
            raise ValueError(log_str)
        actual_input = self.element.get_attribute('type')
        if actual_input != input_type:
            log_str = "Class initialized with input type '{}'; expected '{}'.".format(actual_input, input_type)
            logging.error(log_str)
            raise ValueError(log_str)
        return


class Checkbox(Input):
    """
    Represents <input type="checkbox">.
    """

    def __init__(self, element, desc='checkbox'):
        super().__init__(element=element, desc=desc)
        self._verify_type(input_type='checkbox')
        return

    @property
    def selected(self):
        return self.element.is_selected()

    @selected.setter
    def selected(self, value):
        if type(value) is not bool:
            log_str = "Checkbox must be given a bool, got {}.".format(type(value))
            logging.error(log_str)
            raise TypeError(log_str)
        if not self.selected == value:
            logging.info("Clicking '{}'...".format(self.desc))
            self.element.click()
        else:
            if value is True:
                logging.debug("'{}' is already selected; no need to click.".format(self.desc))
            else:
                logging.debug("'{}' is already unselected; no need to click.".format(self.desc))
        return


class Text(Input):
    """
    Represents <input type="text">.
    """

    def __init__(self, element, desc='single-line text field'):
        super().__init__(element=element, desc=desc)
        self._verify_type(input_type='text')
        return

    @property
    def value(self):
        return self.element.get_attribute('value')

    @value.setter
    def value(self, value):
        logging.info("'{}': Clearing field and entering '{}'...".format(self.desc, value))
        self.element.clear()
        self.element.send_keys(value)
        return


# # Other Types


class Dropdown(BaseElement):
    """
    Standard dropdown.
    """

    def __init__(self, element, desc='dropdown'):
        super().__init__(element=element, desc=desc)
        self._locator = dict()
        self._locator['option'] = (By.CSS_SELECTOR, 'option')
        self._locator['option_enabled'] = (By.CSS_SELECTOR, 'option:not([disabled])')
        self._locator['option_disabled'] = (By.CSS_SELECTOR, 'option[disabled]')
        return

    @property
    def selected_option(self):
        """
        Get/set the dropdown value.
        """
        currently_selected = self._find_selected_option_element()
        if currently_selected is None:
            return ''
        text = currently_selected.text
        # Some strings have unnecessary spaces on the left and right. Que???
        return text.lstrip().strip()

    @selected_option.setter
    def selected_option(self, requested_option):
        self._verify_option_exists(requested_option)
        if requested_option in self.disabled_options:
            log_str = "'{}' option '{}' is disabled. Attempting to select anyway...".format(self.desc, requested_option)
            logging.warning(log_str)
        for option in self._find_options_elements():
            if option.text == requested_option:
                logging.info("'{}': selecting '{}'...".format(self.desc, requested_option))
                option.click()
                return

    @property
    def all_options(self):
        """
        :returns list of str of all options.
        """
        return self._get_options('all')

    @property
    def enabled_options(self):
        """
        :returns list of str of all enabled options.
        """
        return self._get_options('enabled')

    @property
    def disabled_options(self):
        """
        :returns list of str of all disabled options.
        """
        return self._get_options('disabled')

    def _verify_option_exists(self, requested_option):
        """
        :param str requested_option: Option to verify.
        :raises ValueError if requested option is invalid.
        """
        if requested_option not in self.all_options:
            log_str = "Dropdown does not contain requested option '{}'. ".format(requested_option)
            log_str += 'Valid options:\n'
            for option in self.all_options:
                log_str += '    {}\n'.format(option)
            logging.error(log_str)
            raise ValueError(log_str)

    @staticmethod
    def _log_duplicate_options(options_list):
        """
        Logs a warning if any duplicates are found.

        :returns None
        """
        options_set = set(options_list)
        if len(options_set) != len(options_list):
            log_str = 'Dropdown has duplicate options:\n'
            for option in options_list:
                log_str += '    {}\n'.format(option)
            logging.warning(log_str)
        return

    def _get_options(self, option_type):
        """
        Returns list of options of the specified type.

        :param str option_type:
        :returns list of str
        """
        option_type = option_type.lower()
        if option_type == 'all':
            locator = self._locator['option']
        elif option_type == 'enabled':
            locator = self._locator['option_enabled']
        elif option_type == 'disabled':
            locator = self._locator['option_disabled']
        else:
            raise ValueError("Invalid dropdown option type requested.")

        options_list = []
        options_elements = self.element.find_elements(*locator)
        for option in options_elements:
            options_list.append(option.text)

        self._log_duplicate_options(options_list)
        return options_list

    def _find_options_elements(self):
        """
        :returns list of WebElements corresponding to each option.
        """
        return self.element.find_elements(*self._locator['option'])

    def _find_selected_option_element(self):
        """
        :returns WebElement for the currently selected option. (Or None.)
        """
        for option in self._find_options_elements():
            if option.is_selected():
                return option
        return None
