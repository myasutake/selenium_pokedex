import logging

import page_objects.pokedex


# Searching


def execute_search_query(driver, query):
    page = page_objects.pokedex.Page(driver)
    search_field = page.find_search_field_text_input_object()
    search_field.value = query
    page.click_execute_search_button()
    page.wait_until_loaded()
    return


def verify_search_field_results(driver, query):
    page = page_objects.pokedex.Page(driver)
    search_results = page.find_search_result_objects()
    for result in search_results:
        if query.lower() not in result.name and query.lower() not in result.number:
            log_str = f"Test failed. Search query '{query}' verification failed for '{result}'."
            logging.error(log_str)
            raise AssertionError(log_str)
    logging.debug(f"Search verification passed. {len(search_results)} total results found.")
    return


# Sorting


def set_sort_method(driver, sort_method):
    page = page_objects.pokedex.Page(driver)
    sort_dropdown = page.find_sort_dropdown_object()
    sort_dropdown.selected_option = sort_method
    return


def verify_sort_method(driver, sort_method):
    ascending_methods = {'lowest number (first)', 'a-z'}
    descending_methods = {'highest number (first)', 'z-a'}
    name_methods = {'a-z', 'z-a'}
    number_methods = {'lowest number (first)', 'highest number (first)'}
    all_methods = ascending_methods.union(descending_methods).union(name_methods).union(number_methods)

    if sort_method.lower() not in all_methods:
        log_str = f"Invalid sort method '{sort_method}' specified."
        logging.error(log_str)
        raise ValueError(log_str)

    page = page_objects.pokedex.Page(driver)

    if sort_method.lower() in name_methods:
        actual_results = page.all_search_results_names_displayed()
    else:
        actual_results = page.all_search_results_numbers_displayed()
    total_results = len(actual_results)

    expected_results = actual_results.copy()
    if sort_method.lower() in ascending_methods:
        expected_results.sort()
    else:
        expected_results.sort(reverse=True)

    if actual_results != expected_results:
        log_str = f"Sort method '{sort_method} verification failed. {total_results} total results found.\n"
        log_str += "\tActual results:\n"
        for i in actual_results:
            log_str += f"\t\t{i}\n"
        log_str += "\tExpected results:\n"
        for i in expected_results:
            log_str += f"\t\t{i}\n"
        log_str = log_str[:-1]
        logging.error(log_str)
        raise AssertionError(log_str)

    logging.info(f"Sort method '{sort_method} verification passed. {total_results} total results found.")
    return


# Misc


def load_page(driver):
    page = page_objects.pokedex.Page(driver=driver)
    page.load()
    page.accept_cookies()
    return
