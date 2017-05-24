import sys
import inspect
import re

try:
    from decorator import decorator
except SyntaxError:  # decorator module requires Python/Jython 2.4+
    decorator = None
if sys.platform == 'cli':
    decorator = None  # decorator module doesn't work with IronPython 2.6

def _run_on_failure_decorator(method, *args, **kwargs):
    self = args[0]
    try:
        if self._mobile_gen_gif == True:
            # If _web_gen_gif(_mobilekeywords) is setted True, capture the Screen when users do actions(Click/Input/Press/Swipe)
            if(re.search(r'[Cc]lick|[Ii]nput|[Ss]wipe|[Pp]ress',method.__name__)):
                self.capture_page_screenshot_without_html_log()
        return method(*args, **kwargs)
    except Exception, err:
        if hasattr(self, '_run_on_failure'):
            self._run_on_failure()
        raise


class KeywordGroupMetaClass(type):
    def __new__(cls, clsname, bases, dict):
        if decorator:
            for name, method in dict.items():
                if not name.startswith('_') and inspect.isroutine(method):
                    dict[name] = decorator(_run_on_failure_decorator, method)
        return type.__new__(cls, clsname, bases, dict)


class KeywordGroup(object):
    __metaclass__ = KeywordGroupMetaClass
