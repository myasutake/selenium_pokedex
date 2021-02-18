import logging.config

import pytest
from selenium import webdriver

import misc.logging_config
import steps.pokedex


logging.config.dictConfig(misc.logging_config.config)


@pytest.fixture(scope='function')
def driver():
    d = webdriver.Chrome()
    d.maximize_window()
    steps.pokedex.load_page(driver=d)
    yield d
    d.quit()
    return


def test_search_by_name(driver):
    logging.info("Test begin.")
    steps.pokedex.execute_search_query(driver=driver, query='th')
    steps.pokedex.verify_search_field_results(driver=driver, query='th')
    logging.info("Test passed.")
    return


def test_search_by_number(driver):
    logging.info("Test begin.")
    steps.pokedex.execute_search_query(driver=driver, query='20')
    steps.pokedex.verify_search_field_results(driver=driver, query='20')
    logging.info("Test passed.")
    return


@pytest.mark.xfail
def test_search_fail(driver):
    logging.info("Test begin.")
    steps.pokedex.execute_search_query(driver=driver, query='th')
    steps.pokedex.verify_search_field_results(driver=driver, query='ha')
    logging.info("Test passed.")
    return
