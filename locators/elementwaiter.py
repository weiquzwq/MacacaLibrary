# -*- coding: utf-8 -*-

from MacacaLibrary import utils
from robot.api import logger
from macaca import WebElement


class ElementWaiter(object):

    def __init__(self):
        self._strategies = {
            'id': self._wait_by_id,
            'name': self._wait_by_name,
            'xpath': self._wait_by_xpath,
            'class': self._wait_by_class_name,
            'css': self._wait_by_css_selector,
            'link': self._wait_by_link_text,
            'partial link': self._wait_by_partial_link_text,
            'tag name': self._wait_by_tag_name,
            None: self._wait_by_default
        }

    def wait(self, browser, locator, timeout, tag=None):
        assert browser is not None
        assert locator is not None and len(locator) > 0

        (prefix, criteria) = self._parse_locator(locator)
        strategy = self._strategies.get(prefix)
        if strategy is None:
            raise ValueError("Element locator with prefix '" + prefix + "' is not supported")
        (tag, constraints) = self._get_tag_and_constraints(tag)
        return strategy(browser, criteria, tag, constraints, timeout)

    # Strategy routines, private

    def _wait_by_id(self, browser, criteria, tag, constraints, timeout):
        return self._filter_elements(
            browser.wait_for_element_by_id(criteria,timeout),
            tag, constraints)

    def _wait_by_name(self, browser, criteria, tag, constraints, timeout):
        return self._filter_elements(
            browser.wait_for_element_by_name(criteria,timeout),
            tag, constraints)

    def _wait_by_xpath(self, browser, criteria, tag, constraints, timeout):
        return self._filter_elements(
            browser.wait_for_element_by_xpath(criteria, timeout),
            tag, constraints)

    def _wait_by_class_name(self, browser, criteria, tag, constraints, timeout):
        return self._filter_elements(
            browser.wait_for_element_by_class_name(criteria, timeout),
            tag, constraints)

    def _wait_by_css_selector(self, browser, criteria, tag, constraints, timeout):
        return self._filter_elements(
            browser.wait_for_element_by_css_selector(criteria, timeout),
            tag, constraints)

    def _wait_by_link_text(self, browser, criteria, tag, constraints, timeout):
        return self._filter_elements(
            browser.wait_for_element_by_link_text(criteria, timeout),
            tag, constraints)

    def _wait_by_partial_link_text(self, browser, criteria, tag, constraints, timeout):
        return self._filter_elements(
            browser.wait_for_element_by_partial_link_text(criteria, timeout),
            tag, constraints)

    def _wait_by_tag_name(self, browser, criteria, tag, constraints, timeout):
        return self._filter_elements(
            browser.wait_for_element_by_tag_name(criteria, timeout),
            tag, constraints)

    def _wait_by_default(self, browser, criteria, tag, constraints, timeout):
        if criteria.startswith('//'):
            return self._wait_by_xpath(browser, criteria, tag, constraints, timeout)
        return self._wait_by_key_attrs(browser, criteria, tag, constraints, timeout)

    def _get_tag_and_constraints(self, tag):
        if tag is None:
            return None, {}

        tag = tag.lower()
        constraints = {}
        if tag == 'link':
            tag = 'a'
        elif tag == 'image':
            tag = 'img'
        elif tag == 'list':
            tag = 'select'
        elif tag == 'radio button':
            tag = 'input'
            constraints['type'] = 'radio'
        elif tag == 'checkbox':
            tag = 'input'
            constraints['type'] = 'checkbox'
        elif tag == 'text field':
            tag = 'input'
            constraints['type'] = 'text'
        elif tag == 'file upload':
            tag = 'input'
            constraints['type'] = 'file'
        return tag, constraints

    def _element_matches(self, element, tag, constraints):
        if not element.tag_name.lower() == tag:
            return False
        for name in constraints:
            if not element.get_attribute(name) == constraints[name]:
                return False
        return True

    def _filter_elements(self, elements, tag, constraints):
        elements = self._normalize_result(elements)
        if tag is None:
            return elements
        return filter(
            lambda element: self._element_matches(element, tag, constraints),
            elements)

    def _get_attrs_with_url(self, key_attrs, criteria, browser):
        attrs = []
        url = None
        xpath_url = None
        for attr in ['@src', '@href']:
            if attr in key_attrs:
                if url is None or xpath_url is None:
                    url = self._get_base_url(browser) + "/" + criteria
                    xpath_url = utils.escape_xpath_value(url)
                attrs.append("%s=%s" % (attr, xpath_url))
        return attrs

    def _get_base_url(self, browser):
        url = browser.get_current_url()
        if '/' in url:
            url = '/'.join(url.split('/')[:-1])
        return url

    # separation locator to get prefix and criteria
    def _parse_locator(self, locator):
        prefix = None
        criteria = locator
        if not locator.startswith('//'):
            locator_parts = locator.partition('=')
            if len(locator_parts[1]) > 0:
                prefix = locator_parts[0].strip().lower()
                criteria = locator_parts[2].strip()
                if len(criteria) > 2:
                    if criteria.startswith('\"') and criteria.endswith('\"'):
                        criteria = criteria[1:-1]
                    if criteria.startswith('\'') and criteria.endswith('\''):
                        criteria = criteria[1:-1]
        return (prefix, criteria)

    def _normalize_result(self, elements):
        elementlist = []
        if isinstance(elements,type(WebElement(1, 1))):
            elementlist.append(elements)
        elif isinstance(elements, list):
            return elements    
        else:
            logger.debug("WebDriver find returned %s" % elements)    
        return elementlist