import logging.config

import pytest

import misc.logging_config
import steps.pokedex


logging.config.dictConfig(misc.logging_config.config)


def test_sort_lowest_number_first(load_pokedex_page):
    logging.info("Test begin.")
    driver = load_pokedex_page
    steps.pokedex.set_sort_method(driver=driver, sort_method='lowest number (first)')
    steps.pokedex.verify_sort_method(driver=driver, sort_method='lowest number (first)')
    logging.info("Test passed.")
    return


def test_sort_highest_number_first(load_pokedex_page):
    logging.info("Test begin.")
    driver = load_pokedex_page
    steps.pokedex.set_sort_method(driver=driver, sort_method='highest number (first)')
    steps.pokedex.verify_sort_method(driver=driver, sort_method='highest number (first)')
    logging.info("Test passed.")
    return


def test_sort_az(load_pokedex_page):
    logging.info("Test begin.")
    driver = load_pokedex_page
    steps.pokedex.set_sort_method(driver=driver, sort_method='a-z')
    steps.pokedex.verify_sort_method(driver=driver, sort_method='a-z')
    logging.info("Test passed.")
    return


def test_sort_za(load_pokedex_page):
    logging.info("Test begin.")
    driver = load_pokedex_page
    steps.pokedex.set_sort_method(driver=driver, sort_method='z-a')
    steps.pokedex.verify_sort_method(driver=driver, sort_method='z-a')
    logging.info("Test passed.")
    return


@pytest.mark.xfail
def test_sort_az_fail(load_pokedex_page):
    logging.info("Test begin.")
    driver = load_pokedex_page
    steps.pokedex.set_sort_method(driver=driver, sort_method='a-z')
    steps.pokedex.verify_sort_method(driver=driver, sort_method='z-a')
    logging.info("Test passed.")
    return
