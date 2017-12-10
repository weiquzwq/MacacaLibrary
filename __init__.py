import os
from keywords import *
from version import VERSION
from utils import LibraryListener
from robot.libraries.BuiltIn import BuiltIn


__version__ = VERSION


class MacacaLibrary(
    _LoggingKeywords,
    _RunOnFailureKeywords,
    _ElementKeywords,
    _ScreenshotKeywords,
    _ApplicationManagementKeywords,
    _WaitingKeywords,
    _TouchKeywords,
    _KeyeventKeywords,
    _AndroidUtilsKeywords,
    _MobileKeywords,
    _BrowserManagementKeywords,

):
    """MacacaLibrary is a App testing library for Robot Framework.

    *Locating elements*

    All keywords in MacacaLibrary that need to find an element on the app
    take an argument, `locator`. By default, when a locator value is provided,
    it is matched against the key attributes of the particular element type.
    For example, `id` and `name` are key attributes to all elements, and
    locating elements is easy using just the `id` as a `locator`. For example:

    ``Click Element  my_element``

    Macaca additionally supports some of the _Mobile JSON Wire Protocol_
    (https://code.google.com/p/selenium/source/browse/spec-draft.md?repo=mobile) locator strategies
    It is also possible to specify the approach AppiumLibrary should take
    to find an element by specifying a lookup strategy with a locator
    prefix. Supported strategies are:

    | *Strategy*        | *Example*                                                      | *Description*                     |
    | identifier        | Click Element `|` identifier=my_element                        | Matches by @id or @name attribute |
    | id                | Click Element `|` id=my_element                                | Matches by @id attribute          |
    | name              | Click Element `|` name=my_element                              | Matches by @name attribute        |
    | xpath             | Click Element `|` xpath=//UIATableView/UIATableCell/UIAButton  | Matches with arbitrary XPath      |
    | link              | Click Element `|` link=My Link                                 | Webview only Matches anchor elements by their link text      |
    | partial link      | Click Element `|` partial link=My Link                         | Webveiw only Matches anchor elements by their partial link text |
    | class             | Click Element `|` class=UIAPickerWheel                         | Matches by class                  |
    | accessibility_id  | Click Element `|` accessibility_id=t                           | Accessibility options utilize.    |
    | android           | Click Element `|` android=new UiSelector().description('Apps') | Matches by Android UI Automator   |
    | ios               | Click Element `|` ios=.buttons().withName('Apps')              | Matches by iOS UI Automation      |
    | css               | Click Element `|` css=.green_button                            | Matches by css in webview         |



    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self, timeout=5, run_on_failure='Capture Page Screenshot',mobile_gif='False'):
        """MacacaLibrary can be imported with optional arguments.

        `timeout` is the default timeout used to wait for all waiting actions.
        It can be later set with `Set Appium Timeout`.

        `run_on_failure` specifies the name of a keyword (from any available
        libraries) to execute when a AppiumLibrary keyword fails. By default
        `Capture Page Screenshot` will be used to take a screenshot of the current page.
        Using the value `No Operation` will disable this feature altogether. See
        `Register Keyword To Run On Failure` keyword for more information about this
        functionality.
        `mobile_gif` Enable/Disable gif generation for each Test Case, Defalut setting is False/FALSE

        Examples:
        | Library | MacacaLibrary | 10 | # Sets default timeout to 10 seconds                                                                             |
        | Library | MacacaLibrary | timeout=10 | run_on_failure=No Operation | # Sets default timeout to 10 seconds and does nothing on failure           |
        | Library | MacacaLibrary | timeout=10 | mobile_gif=TRUE             | # Sets default timeout to 10 seconds and enable gif file generation for each case |
        """
        for base in MacacaLibrary.__bases__:
            base.__init__(self)
        self.set_macaca_timeout(timeout)
        self.register_keyword_to_run_on_failure(run_on_failure)

        self.Mobile_Set_Gif_Flag(mobile_gif)
        if self._mobile_gen_gif == True:
            self.ROBOT_LIBRARY_LISTENER = LibraryListener()
