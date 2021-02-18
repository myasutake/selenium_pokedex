import logging

import page_objects.pokedex


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
