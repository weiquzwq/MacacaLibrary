# -*- coding: utf-8 -*-

from MacacaLibrary.locators import ElementFinder
from keywordgroup import KeywordGroup
from robot.api import logger

class _TouchKeywords(KeywordGroup):

    def __init__(self):
        self._element_finder = ElementFinder()

    # Public, element lookups
    def zoom(self, locator, percent="200%", steps=1):
        """
        Zooms in on an element a certain amount.
        """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        driver.zoom(element=element, percent=percent, steps=steps)

    def pinch(self, locator, percent="200%", steps=1):
        """
        Pinch in on an element a certain amount.
        """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        driver.pinch(element=element, percent=percent, steps=steps)

    #def swipe(self, start_x, start_y, end_x, end_y, duration=1000):
    #    """
    #    Swipe from one point to another point, for an optional duration.
    #    """
    #    driver = self._current_application()
    #    logger.write("swip_before", level='INFO', html=False)
    #    driver.swipe(start_x, start_y, end_x, end_y, duration)

    def swipe(self, start_x, start_y, end_x, end_y, duration=2):
        """
        Swipe from one point to another point, for an optional duration.
        """
        driver = self._current_application()
        driver.touch('drag', {'fromX': start_x, 'fromY': start_y, 'toX': end_x, 'toY': end_y, 'duration': duration})


    def scroll(self, start_locator, end_locator):
        """
        Scrolls from one element to another
        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        el1 = self._element_find(start_locator, True, True)
        el2 = self._element_find(end_locator, True, True)
        driver = self._current_application()
        driver.scroll(el1, el2)
        
    def scroll_to(self, locator):
        """Scrolls to element"""
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        driver.execute_script("mobile: scrollTo", {"element": element.id})


    def long_press(self, locator, duration=2):
        """long press the element

        """
        element = self._element_find(locator, True, True)
        element.touch('press', {'duration': duration})

        
    def tap_a_point(self, x, y):
        """ tap on a point """
        driver = self._current_application()
        driver.touch('tap', {'X': x, 'Y': y})

