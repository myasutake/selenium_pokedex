import logging.config

import pytest

import misc.logging_config
import steps.pokedex


logging.config.dictConfig(misc.logging_config.config)


def test_search_by_name(load_pokedex_page):
    logging.info("Test begin.")
    driver = load_pokedex_page
    steps.pokedex.execute_search_query(driver=driver, query='th')
    steps.pokedex.load_all_results(driver=driver)
    steps.pokedex.verify_search_field_results(driver=driver, query='th')
    logging.info("Test passed.")
    return


def test_search_by_number(load_pokedex_page):
    logging.info("Test begin.")
    driver = load_pokedex_page
    steps.pokedex.execute_search_query(driver=driver, query='20')
    steps.pokedex.load_all_results(driver=driver)
    steps.pokedex.verify_search_field_results(driver=driver, query='20')
    logging.info("Test passed.")
    return


@pytest.mark.xfail
def test_search_fail(load_pokedex_page):
    logging.info("Test begin.")
    driver = load_pokedex_page
    steps.pokedex.execute_search_query(driver=driver, query='th')
    steps.pokedex.load_all_results(driver=driver)
    steps.pokedex.verify_search_field_results(driver=driver, query='ha')
    logging.info("Test passed.")
    return
