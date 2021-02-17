# Intro to Selenium...with Pokémon!
## Objectives
I started this project as a Selenium self-study. Hopefully you can learn something from it too! I am writing this code and documentation with the following objectives in mind, from a Python perspective:
* Installation and setup of Selenium
* Establishment of an effective Selenium Page Object Model
* Learning PyTest basics
* Writing simple and readable tests

### Prerequisites

Knowledge of:
* HTML/XML structure
* Web browser inspectors
* XPath and CSS selectors

## Things to install

Code is written for Python 3.x.

The following packages are required:
* [selenium](https://pypi.python.org/pypi/selenium/) - Automation framework!
* [pytest](http://doc.pytest.org/en/latest/) - Testing framework, way better than Python's included <code>unittests</code> package.

### Verifying Selenium setup

1. Launch Python - <code>python</code> - (whie you're at it, verify you're running 3.x)
1. Import selenium - <code>from selenium import webdriver</code>
1. Launch Chrome - <code>webdriver.Chrome()</code>

If you get an error stating that Selenium can't find the chromedriver executable in your PATH, then do the following:

1. Download [Chromedriver](https://sites.google.com/a/chromium.org/chromedriver/) zip file.
1. Grab the executable from the zip file.
1. Edit your PATH variable to include the directory of the Chromedriver executable.
1. Run through the first three steps again and verify that <code>webdriver.Chrome()</code> does launch a browser.

### Selenium Architecture - Page Object Model / Design Pattern

By far, the most suggested method to architect Selenium code is with the use of the ["Page Object Design Pattern"](http://www.seleniumhq.org/docs/06_test_design_considerations.jsp#page-object-design-pattern) or "Page Object Model. "However, Google searches result in many different implementation styles! This is due to
1. Selenium being available in many languages, each having have their own nuances.
1. A lack of consensus of what a "Page Object" is.

I'll do my best to explain my interpretation of a Page Object, along with the code I've written to implement them, and some tips I'd recommend.

##### What is it?

I'll quote the official Selenium page linked above:

> Page Object is a Design Pattern which has become popular in test automation for enhancing test maintenance and reducing code duplication. A page object is an object-oriented class that serves as an interface to a page of your AUT. The tests then use the methods of this page object class whenever they need to interact with the UI of that page. The benefit is that if the UI changes for the page, the tests themselves don’t need to change, only the code within the page object needs to change. Subsequently all changes to support that new UI are located in one place.
>
> The Page Object Design Pattern provides the following advantages
>
> 1. There is a clean separation between test code and page specific code such as locators (or their use if you’re using a UI Map) and layout.
> 2. There is a single repository for the services or operations offered by the page rather than having these services scattered throughout the tests.
>
> In both cases this allows any modifications required due to UI changes to all be made in one place.

To be a little more specific, Page Objects _themselves_:
* Should contain the majority of the Selenium code (finding elements, clicking things, setting fields).
* Should not test (read: assert) anything.

Conversely, the tests _themselves_:
* Should contain very little Selenium code.
* Should perform the assertions.

##### Scope

How "big" should a given Page Object be?

As an example, let's say we have a page with a search field, a button which executes the search, two toggles, and a bunch of search results. Here are the two implementation extremes:

Put the entire page into one Page Object:

    class TheEntirePage():
        def set_search_field(): ...
        def click_search_button(): ...
        def set_toggle_1(): ...
        def set_toggle_2(): ...
        def click_result_1(): ...
        def get_result_1_url(): ...

As many Page Objects as possible:

    class SearchField():
        def set_search_field(): ...
        def clear_search_field(): ...

    class Searchbutton():
        def click(): ...

    class Toggle1():
        def enable(): ...
        def disable(): ...

    class Toggle2():
        def enable(): ...
        def disable(): ...

    class Result1():
        def click(): ...
        def get_url(): ...

Sorry to give a non-answer, but a Page Object's scope really should depend on a case-by-case basis. It will likely be between the two given extremes. More details included in <code>page_objects/base.py</code>.

##### Locators

One of the things that undergoes frequent changes during website development is an element's locator. Obviously, locators should be a part of the Page Object architecture (i.e. a given locator should be defined in one place, so maintenance is minimized). However, I have seen two types of architecture:

1. All locators defined in one separate file.
1. Locators defined their respective Page Objects (i.e. the locator of the search field should be defined in the Search Page Object).

I strongly recommend the latter.

Yes, the one-file approach makes it easier to find your locator since they're all in one place. Or...does it, though? You still need to organize (read: architect) your locators in a logical way. What if you have two similarly-named Page Objects? Will you be able to differentiate the locators in each object or will you confuse them? When you instead define the locators inside their respective Page Objects, there's no additional architecture needed; you know which locator applies to which object.

### PyTest

PyTest is a very popular testing framework library. I recommend it whether your tests involve Selenium or not. The documentation is good, but extensive. I'll highlight below the mechanisms I've used in these tests.

##### Tests

* Test files are defined as files beginning with 'test\_'.
* Tests can be defined as functions beginning with "test\_" and/or...
* Tests can be defined as class methods beginning with "test\_" inside of a class beginning with "Test".

##### Setup and Teardown

Setup and teardown functions are a common mechanism of unit testing frameworks. Simply, a setup is run before every test, and a teardown is run after every test.

In Pytest, a setup is indicated by a <code>fixture</code> function. If there is a <code>yeild</code> instead of a <code>return</code>, the setup is everything before the <code>yield</code>, and the teardown is everything after.

A fixture can have a scope as well, depending on where it is defined, and if it was given a scope parameter. Obviously, if it is defined in a test file, it can only apply to the tests in that file. Because I wanted the same setup (open a browser) and teardown (close the browser) to apply to more than one file, it is defined in a Pytest-specific file which contains mechanisms which apply to all files in the directory. This file is named _conftest.py_.
