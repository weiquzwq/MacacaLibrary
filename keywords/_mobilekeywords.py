# -*- coding: utf-8 -*-
import sys
import traceback

from keywordgroup import KeywordGroup
#from appium.webdriver.common.touch_action import TouchAction
from time import sleep
from xml.etree import cElementTree as ET

class _MobileKeywords(KeywordGroup):
    """
    _MobileKeywords including the Wrapper Keywords for RFUI Framework specially. 
    Move from the common_lib_mobile.py.
    The following keywords can be add/delete/modify according to the RFUI Framework requirement.
    """
    def __init__(self):
        self._mobile_gen_gif = False


    def Mobile_Set_Gif_Flag(self, mobile_gif_flag="FALSE"):
        """ Set Mobile GIF Generation Flag. (Default: "FALSE" / "TRUE": generate one GIF file for each TestCase)
        设置用例生成GIF开关.(默认设置为"FALSE", 当设置为“TRUE/True”时， 每个用例都会生成一份同名的gif文件)
        This KW will invoke at Library importing, Also Can be invoked during case running.
        | Mobile Set Gif Flag | TRUE | #enable genrate gif for test case |
        | Mobile Set Gif Flag | FALSE | #disable genrate gif for test case  |
        """
        if mobile_gif_flag.upper() == "TRUE":
            self._mobile_gen_gif = True
        else:
            self._mobile_gen_gif = False

    # Public, keywords
    def Mobile_Open_Application(self, myremote_url, myalias=None,  **kwargs):
        """打开Moible(IOS/Android)端APP
        | Mobile Open Application | ${remote_url} | MyIOSapp | platformName=iOS | platformVersion=9.1 | deviceName='iPhone 6' app=${yourapp_path} | 
        """
        myindex = self.open_application(myremote_url, alias=myalias, **kwargs)
        self._info("[>>>]index of open_application: %s" % myindex)
        return myindex

    def Mobile_Close_Application(self):
        """关闭 当前活动的Moible(IOS/Android)端APP
        | Mobile Close Application | |
        """       
        self.close_application()
        self._info("[>>>]close_application!")

    def Mobile_Switch_Application(self, alias_or_index):
        """切换至指定的alias_or_index Moible(IOS/Android)端APP
        | Mobile Switch Application | ${alias_or_index} |
        | Mobile Switch Application | MyIOSapp |
        """
        self.switch_application(alias_or_index)
        self._info("[>>>]switch_application to alias_or_index:%s" % alias_or_index)


    def Mobile_Click_Element(self, locator, target_num=1):
        """点击locator定义的元素， （locator搜索结果为多个元素，默认点击其中第一个，可以设定target_num，点击指定第n元素）
        locator: 同AppiumLibrary里的locator;
        target_num: 指定元素序号.
        [不输入（默认值）:   点击第一个元素]
        [=0 :                点击最后一个元素]
        [=x（>0）:           点击第x个元素]

        | Mobile Click Element | ${locator} |
        Android Native: 
        | Mobile Click Element | identifier=myid |
        | Mobile Click Element | xpath=//android.widget.TextView[@text="文本"] |
        | Mobile Click Element | xpath=//android.widget.lsView/android.widget.RelativeLayout[3] |
        @text表示的是android.widget.TextView的一个text属性，"文本"是该属性的值，用""引起来，是xpath的一种写法
        
        Android WebView: 
        | Mobile Click Element | accessibility_id=公众号名称 |
        | Mobile Click Element | accessibility_id=公众号名称 | 0 |
        
        IOS Native: 
        | Mobile Click Element | identifier=myid |
        | Mobile Click Element | id=public icon normal |
        | Mobile Click Element | xpath=//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIATextField[2] |

        IOS WebView:
        | Mobile Click Element | xpath=//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/UIAStaticText[27] |

        locator 示例:
        | *Strategy*        | *Example*                                                      | *Description*                     |
        | identifier Click Element | identifier=my_element | Matches by @id or @name attribute |
        | id Click Element | id=my_element | Matches by @id attribute |
        | name Click Element | name=my_element | Matches by @name attribute |
        | xpath Click Element | xpath=//UIATableView/UIATableCell/UIAButton | Matches with arbitrary XPath | 
        | class Click Element | class=UIAPickerWheel | Matches by class | 
        | accessibility_id Click Element | accessibility_id=t | Accessibility options utilize. | 
        | android Click Element | android=new UiSelector().description('Apps') | Matches by Android UI Automator   |
        | ios     Click Element | ios=.buttons().withName('Apps')              | Matches by iOS UI Automation      |
        | css     Click Element | css=.green_button                            | Matches by css in webview         |

        """
        target_element = self._get_selected_element(locator, target_num)
        target_element.click()
        

    def Mobile_Click_Text_Button(self, text, target_num=1):
        """点击可以通过按钮内文字定位的Button， （相同文字的按钮如果是多个，默认点击其中第一个，可以设定target_num，点击指定第n元素）
        text: 为按钮内的文字, 比如： 欢迎页－登录  主菜单页－发现／好友／电话／我
        target_num: 指定元素序号
        [不输入（默认值）:   点击第一个元素]
        [=0 :                点击最后一个元素]
        [=x（>0）:           点击第x个元素]
        
        | Mobile Click Text Button | ${text} |
        IOS/Android:
        | Mobile Click Text Button | 登录 |
        | Mobile Click Text Button | ${text} |
        | Mobile Click Text Button | 发送的消息内容 | 0 |
        | Mobile Click Text Button | 发送的消息内容 | 3 |
        """
        if self._is_android():
            #Android example:   xpath=//*[@text="登录"]
            mylocator = 'xpath=//*[@text=' + '"' + text + '"]'
            #mylocator = 'xpath=//android.widget.Button[@text=' + '"' + text + '"]'
        if self._is_ios():
            #iOS example: id=登录 
            #mylocator = 'name=' + text
            #mylocator = 'id=' + text
            mylocator = 'accessibility_id=' + text
        self.Mobile_Click_Element(mylocator, target_num)

    def Mobile_Long_Press(self, locator, target_num=1):
        """长时间按 locator定义的UI元素
        locator: 同AppiumLibrary里的locator
        | Mobile Long Press | ${locator} |
        """
        self.wait_until_page_contains_element(locator)
        self.long_press(locator, target_num)

    def Mobile_Long_Press_Text_Button(self, text, target_num=1):
        """长时间按 可以通过按钮内文字定位的Button
        text: 为按钮内的文字
        | Mobile Long Press Text Button | ${text} |
        | Mobile Long Press Text Button | 发送的消息 |
        """
        if self._is_android():
            # Android example:   xpath=//*[@text="登录"]
            mylocator = 'xpath=//*[@text=' + '"' + text + '"]'
        if self._is_ios():
            # iOS example: id=登录
            mylocator = 'identifier=' + text
        self.Mobile_Long_Press(mylocator, target_num)

    def Mobile_Input_Text(self, locator, text):
        """向文本框中输入文本
        | Mobile Input Text | ${locator} |  ${text} |
        locator: 同AppiumLibrary里的locator
        text: 用户名
        """
        self.wait_until_page_contains_element(locator)
        self.input_text(locator, text)

    def Mobile_Clear_Text(self, locator):
        """清空文本框中的文本
        | Mobile Clear Text | ${locator} |
        locator: 同AppiumLibrary里的locator
        """
        self.wait_until_page_contains_element(locator)
        self.clear_text(locator)

    def Mobile_Capture_Page_Screenshot(self):
        """抓取当前页面截屏图片
        | Mobile Capture Page Screenshot |
        """
        self.capture_page_screenshot() 

    def Mobile_Page_Should_Contain_Text(self, text):
        """验证当前页面是否包含text
        | Mobile Page Should Contain Text | ${text} |
        """
        self.Mobile_Wait_Until_Text_Exist(text)
        self.page_should_contain_text(text)

    def Mobile_Page_Should_Contain_Element(self, locator):
        """验证当前页面是否包含locator定位的元素
        | Mobile Page Should Contain Element | ${locator} |
        """
        self.Mobile_Wait_Until_Element_Exist(locator)
        self.page_should_contain_element(locator)

    def Mobile_Page_Should_Not_Contain_Text(self, text):
        """验证当前页面是否 不包含text
        | Mobile Page Should Not Contain_Text | ${text} |
        """
        self.Mobile_Wait_Until_Text_Vanish(text)
        self.page_should_not_contain_text(text)

    def Mobile_Page_Should_Not_Contain_Element(self, locator):
        """验证当前页面是否 不包含locator定位的元素
        | Mobile Page Should Not Contain_Element | ${locator} |
        """
        self.Mobile_Wait_Until_Element_Vanish(locator)
        self.page_should_not_contain_element(locator)

    # Wait KWs
    def Mobile_Wait_Until_Text_Exist(self, text, timeout=None):
        """timeout时间内，等待至当前页面包含text

        text 页面包含的文本
        timeout 设置等待时间(s)，默认值为库设定值
        | Mobile Wait Until Text Exist| ${text} |
        | Mobile Wait Until Text Exist| Hello! |
        """
        self.wait_until_page_contains(text, timeout)

    def Mobile_Wait_Until_Element_Exist(self, locator, timeout=None):
        """timeout时间内，等待至当前页面包含locator指定的元素

        locator 元素定位
        timeout 设置等待时间(s)，默认值为库设定值
        | Mobile Wait Until Element Exist | ${locator} |
        | Mobile Wait Until Element Exist | id=myid |
        """ 
        self.wait_until_page_contains_element(locator, timeout)

    def Mobile_Wait_Until_Text_Vanish(self, text, timeout=None):
        """timeout时间内，等待至当前页面不包含text

        text 页面不包含的文本
        timeout 设置等待时间(s)，默认值为库设定值
        | Mobile Wait Until Text Vanish | ${text} |
        | Mobile Wait Until Text Vanish | Hello! |
        """
        self.wait_until_page_does_not_contain(text, timeout)

    def Mobile_Wait_Until_Element_Vanish(self, locator, timeout=None):
        """timeout时间内，等待当前页面不包含locator指定的元素

        locator 元素定位
        timeout 设置等待时间(s)，默认值为库设定值
        | Mobile Wait Until Element Vanish  | ${locator} |
        | Mobile Wait Until Element Vanish  | id=myid |
        """ 
        self.wait_until_page_does_not_contain_element(locator, timeout)


    def Mobile_Swipe(self, start_x, start_y, end_x, end_y, duration=1000):
        """定义滑动操作

        添加了1s延迟
        start_x 起始x轴坐标
        start_y 起始y轴坐标
        end_x 结束x轴坐标
        end_y 结束y轴坐标
        duration 操作的时间间隔单位ms
        | Mobile_Swipe | start_x | start_y | end_x | end_y | duration |
        """
        sleep(1)#延迟1s
        self.swipe(start_x, start_y, end_x, end_y, duration)

    def Mobile_Get_Element_Attribute(self, locator, attribute):
        """获取指定位置元素的属性

        locator 元素位置
        attribute 属性：name, value, text...
        | Mobile Get Element Attribute | locator | name |
        | Mobile Get Element Attribute | locator | text |
        """
        self.wait_until_page_contains_element(locator)
        return self.get_element_attribute(locator, attribute)

    def Mobile_Switch_To_Context(self, context):
        """切换native和webview

        context 通常是'NATIVE_APP'和'WEBVIEW_X'两种
        | Mobile Switch To Context | NATIVE_APP |
        | Mobile Switch To Context | WEBVIEW_3 |
        """
        self.switch_to_context(context)


    def Mobile_Click_WebView_TextElement(self, text, target_num=1):
        """用于移动端WebView中的带文本的元素点击操作,支持自动滚屏，可以点击未进入webview屏幕的元素

        | Mobile Click WebView TextElement | 更多游戏 | 
        如果有重复元素，可以用target_num选择第几个
        | Mobile Click WebView TextElement | ${text} | ${target_num}|
        | Mobile Click WebView TextElement | 下载 | 3 |
        """
        if self._is_android():
            textelement = 'accessibility_id=' + text
            #try search elment with ${text}, if failed try search element with ${text}+' Link' (易信内置webview)
            try:
                 self.wait_until_page_contains_element(textelement)
            except Exception:
                 textelement += " Link" 
        if self._is_ios():
            textelement = 'xpath=//UIAStaticText[@name="%s"]' % text
        self.Mobile_Click_WebView_Element(textelement, target_num)

    def Mobile_Click_WebView_Element(self, locator, target_num=1):
        """用于移动端WebView中locator定义的元素点击操作,支持自动滚屏,可以点击未进入webview屏幕的元素

        | Mobile Click WebView Element | accessibility_id=webview_ico_home_games_all_played_2x |
        如果有重复元素，可以用target_num选择第几个
        | Mobile Click WebView Element | ${text}  | 3 |
        """
        self.wait_until_page_contains_element(locator)
        self._click_webview_element_autoswipe(locator, target_num)

    def Mobile_Get_Elements_Num(self, locator):
        """返回符合locator定义的元素的个数 0-n

        | Mobile Get Elements Num | ${locator} |
        | Mobile Get Elements Num | identifier=myid |
        | ${element_num} | Mobile Get Elements Num | identifier=myid |
        """

        try:
            self.wait_until_page_contains_element(locator)
            elements_list = self.get_elements(locator)
            # self._debug("[debug] Mobile_Get_Elements_Num: try step2 elements_list: %d!" % len(elements_list))
            return len(elements_list)
        except Exception:
            # self._debug("[debug] Mobile_Get_Elements_Num: except path!")
            return 0

    def Mobile_Get_Text_Button_Num(self, text):
        """返回匹配‘text’的文本/按钮元素的个数 0-n

        | Mobile Get Text Button Num | ${text} |
        | Mobile Get Text Button Num | 登录 |
        | ${element_num} | Mobile Get Text Button Num| 登录 |
        """
        if self._is_android():
            # Android example:   xpath=//*[@text="登录"]
            mylocator = 'xpath=//*[@text=' + '"' + text + '"]'
        if self._is_ios():
            # iOS example: id=登录
            # mylocator = 'identifier=' + text
            # mylocator = 'name=' + text
            mylocator = 'accessibility_id=' + text
        return self.Mobile_Get_Elements_Num(mylocator)

    def Mobile_Get_Text_Button_Num_By_Source(self, text):
        """iOS only
            由于appium v1.5取消了name定位方式，增加该关键字通过page source获得文本/按钮个数
            只统计visible为true的文本/按钮个数

        | Mobile Get Text Button Num By Source | ${text} |
        | Mobile Get Text Button Num By Source| 登录 |
        | ${element_num} | Mobile Get Text Button Num By Source| 登录 |
        :return: 匹配‘text’的文本/按钮元素的可见个数
        """
        if self._is_ios():
            locator = 'name=' + text
            (prefix, criteria) = self._element_finder._parse_locator(locator)
            return self._locate_elements_from_source(prefix, criteria, predicate_attr='visible',
                                                     predicate_val='true')
        if self._is_android():
            raise ValueError("This keyword does not support Android")

    def Mobile_Press_Keycode(self, keycode):
        """Android Only，向Android系统下发keycode按键事件
        具体按键事件定义，可参考：
        http://developer.android.com/reference/android/view/KeyEvent.html

        | ${KEYCODE_MENU} | Set Variable | 82 |
        | Mobile Press Keycode | ${KEYCODE_MENU} |
        | ${KEYCODE_HOME} | Set Variable | 3 |
        | Mobile Press Keycode | ${KEYCODE_HOME} |
        | ${KEYCODE_BACK} | Set Variable | 4 |
        | Mobile Press Keycode | ${KEYCODE_BACK} |
        """
        self.press_keycode(keycode)

    def Mobile_Long_Press_Keycode(self, keycode):
        """Android Only，向Android系统下发keycode长按键事件
        具体按键事件定义，可参考：
        http://developer.android.com/reference/android/view/KeyEvent.html

        | ${KEYCODE_MENU} | Set Variable | 82 |
        | Mobile Long Press Keycode | ${KEYCODE_MENU} |
        """
        self.long_press_keycode(keycode)

    def Mobile_Swipe_In_Element(self, locator, target_num=1):
        """Android Only Now, 定义元素内滑动操作。在一个元素内滑动，每次上下滑动元素一半可视长度
        locator: 元素定位
        target_num: 指定元素序号
        [不输入（默认值）:   点击第一个元素]
        [=0 :                点击最后一个元素]
        [=x（>0）:           点击第x个元素]

        | Mobile Swipe In Element | identifier=custom_webview_more_action |
        | Mobile Swipe In Element | ${图文页更多菜单栏框体} | 1 |
        """
        self.wait_until_page_contains_element(locator)
        element = self._get_selected_element(locator, target_num)
        size = element.size.values()
        width, height = size[0], size[1]
        loc = element.location.values()
        y, x = loc[0], loc[1]
        self.swipe(x + width / 2, y + height * 0.9, x + width / 2, y + height * 0.1, 1000)

# Private 
    def _click_webview_element_autoswipe(self, target_locator, target_num=1):
        """ swipe loop + element.click on webview pages, such as game platform webview and public webview

            Implemented seperately in Android & iOS
            inputs: target_locator, target_num
            return: none
        """
        #Android 自动滑动
        if self._is_android():
            # get&verify target element with target_num
            # 获取目标元素 和 Webview空间的左边尺寸数据
            target_element = self._get_selected_element(target_locator, target_num)               
            webview_element = self.get_elements('class=android.webkit.WebView', True)          

            # get the swipe-times and swipe action(start-point and swipe-distance)
            # 获取 滑动 操作相关参数
            swipe_times, start_loc_x, start_loc_y, swipe_distance  = self._webview_element_autoswipe_get_swipe_actiondata(webview_element, target_element)
            #self._debug("[debug] autoswipe action data:")
            #self._debug("[debug] swipe_times: %d, start_loc_x:%d, start_loc_y:%d, swipe_distance:%d" % (swipe_times, start_loc_x, start_loc_y, swipe_distance))

            #Click Element with Auto Swipe for Andorid
            # 滑动屏幕 直至（次数限制内）元素出现在Webivew屏显范围内，再进行点击操作
            # Swipe loop(swipe-times and the element still not present in webview)
            #       Do a up/down swipe    
            #       get target element latest location
            # if new location appear in WebView Controller, Click the Elment 
            # else print the failed info and do nothing to the element
            #       else try to Swipe a distance=Webview height
            while (swipe_times > 0 and self._is_element_present_in_webview(webview_element, target_element)==False):                 
                self.swipe(start_loc_x, start_loc_y, start_loc_x, start_loc_y+swipe_distance, 3000)
                #self._debug('[debug] Element not present in Webview now, and do one swipe with swipe_distance: %d' % swipe_distance)
                target_element = self._get_selected_element(target_locator, target_num)
                swipe_times -=1
                sleep(2)
                #self._debug('[debug] Now swipe_times left: %d' % swipe_times)
            if self._is_element_present_in_webview(webview_element, target_element):
                #target_element.click()    
                x=target_element.location.values()[1]+target_element.size.values()[0]/2
                y=target_element.location.values()[0]+target_element.size.values()[1]/2
                self.click_a_point(x,y)
                self._info('[>>>] Click the elment by element.click with locator: %s' % target_locator)
            else:
                self._info('[xxx] Faile to swipe the element %s present in Webview!' % target_locator)

                
        # IOS 自动滑动
        if self._is_ios():
            self._ios_auto_swipe(target_locator, target_num)


    def _ios_auto_swipe(self, target_locator, target_num):
        device_height = self.get_elements('xpath=//UIAWindow[1]', True).size.values()[1]
        webView = self.get_elements('xpath=//UIAWebView[1]', True)
        webView_size = webView.size.values()
        webView_y = webView.location.values()[0]
        width = webView_size[0]
        one_height = webView_size[1]
        # 对游戏平台的特殊WebView特殊处理
        # 如果WebView一次性加载（页面超出device的屏幕），可以不用滑动直接点击
        if one_height > device_height:
            self.Mobile_Click_Element(target_locator, target_num)
            return 
        # 定义划动起始位置，滑动一个WebView的高度（默认WebView底部接屏幕底部）
        mystart_x = width / 2
        mystart_y = webView_y + one_height
        myend_x = mystart_x
        myend_y = webView_y
        # 获取元素起始坐标位置
        elem = self._get_selected_element(target_locator, target_num)
        elem_y = elem.location.values()[0]
        distance = elem_y - webView_y
        # 向上滑
        if elem_y >= 0:
            while elem_y >= device_height:
                self.Mobile_Swipe(mystart_x, mystart_y, myend_x, myend_y)
                elem = self._get_selected_element(target_locator, target_num)
                elem_y = elem.location.values()[0]
        # 向下滑
        else:
            while elem_y < 0:
                self.Mobile_Swipe(myend_x, myend_y, mystart_x, mystart_y)
                elem = self._get_selected_element(target_locator, target_num)
                elem_y = elem.location.values()[0]
        elem.click()
        self._info('[>>>]Click WebView Element "%s"' % target_locator)

    def _webview_element_autoswipe_get_swipe_actiondata(self, webview_element, target_element):
        """ get swipe-actiondata with the webview element &  the target element
            inputs: webview_element, target_element
            return: swipe_times, start_loc_x, start_loc_y, swipe_distance
        """
        #get webview location+size
        webview_location = webview_element.location.values()
        webview_size = webview_element.size.values()
        #get element location+size
        des_loc = target_element.location.values()
        des_size = target_element.size.values()

        des_size_width = des_size[0]
        des_size_height = des_size[1]
        des_loc_y = des_loc[0]
        des_loc_bottom = des_loc_y + des_size_height
        des_loc_x = des_loc[1]
        webview_y = webview_location[0]
        webview_height = webview_size[1]
        webview_bottom = webview_y + webview_height
        self._info('[debug] webview_location: (%d, %d)'%(webview_location[1], webview_y))
        self._info('[debug] webview_size: (%d, %d)' % (webview_size[0], webview_height))
        self._info('[debug] des_loc: (%d, %d)' % (des_loc_x, des_loc_y))
        self._info('[debug] des_size: (%d, %d)' % (des_size_width, des_size_height))

        start_loc_x = des_loc_x + int(des_size_width/2)
        swipe_times = abs(des_loc_bottom - webview_bottom)/webview_height + 2
        if (des_loc_y >= webview_y) :
            # in case the target element is in webview
            start_loc_y = webview_bottom-2
            swipe_distance = 1-webview_height
        else:
            # otherwise the target element is above of the webview
            start_loc_y = webview_y+1
            swipe_distance = webview_height-2
        return swipe_times, start_loc_x, start_loc_y, swipe_distance


    def _is_element_present_in_webview(self, webview_element, target_element):
        """ get swipe-actiondata with the webview element &  the target element
            inputs: webview_element, target_element
            return: boolen value: True or False
        """
        #get webview location+size
        webview_location = webview_element.location.values()
        webview_size = webview_element.size.values()
        webview_top = webview_element.location.values()[0]
        webview_bottom = webview_element.location.values()[0] + webview_element.size.values()[1]
        self._debug('[debug] y of webview_top & webview_bottom: (%d, %d)'%(webview_top, webview_bottom))
        #get element location+size
        target_loc = target_element.location.values()
        target_size = target_element.size.values()
        target_element_top = target_element.location.values()[0]
        target_element_bottom = target_element.location.values()[0] + target_element.size.values()[1]
        self._debug('[debug] y of target_element_top & target_element_bottom: (%d, %d)'%(target_element_top, target_element_bottom))
        if (target_element_bottom <= webview_bottom and target_element_top >= webview_top):
            is_inwebview_flag = True
        else:
            is_inwebview_flag = False
        self._debug('[debug] The Target element is in webview control: %d' % is_inwebview_flag)
        return is_inwebview_flag
        

    def _get_selected_element(self, target_locator, target_num=1):
        """ get&verify target element with target_num
            inputs: target_locator, target_num
            return: target_element
        """
        self.wait_until_page_contains_element(target_locator)
        index = int(target_num) - 1
        elements_ls = self.get_elements(target_locator)
        if index < len(elements_ls):
            return elements_ls[index]
        else:
            self.capture_page_screenshot() 
            raise AssertionError("[xxx]The target_num is '%d', which is out of the length of elements_ls searched by '%s'." % (int(target_num), target_locator))

    def _locate_elements_from_source(self, attr='name', attr_val='查看消息', predicate_attr='visible', predicate_val='true'):
        m = 0
        try:
            page = self.get_source()
            tree = ET.ElementTree(ET.fromstring(page))
            for elem in tree.iter():
                if attr in elem.attrib:
                    # if unicode(attr_val, 'utf-8') == elem.attrib[attr]:
                    #     if unicode(predicate_val, 'utf-8') == elem.attrib[predicate_val]:
                    if attr_val in elem.attrib[attr]:
                        if predicate_val in elem.attrib[predicate_attr]:
                            m += 1
            return m
        except Exception, e:
            self._info('[xxx]: %s ' % traceback.format_exc())
