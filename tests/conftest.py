import pytest
from selenium import webdriver

import steps.pokedex


@pytest.fixture(scope='function')
def load_pokedex_page():
    d = webdriver.Chrome()
    d.maximize_window()
    steps.pokedex.load_page(driver=d)
    yield d
    d.quit()
    return


