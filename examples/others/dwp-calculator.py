# coding=utf-8

from itertools import count
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from random import randint
from time import sleep

useNativeEvents = 1

windowPath = "/AXApplication[@AXTitle='Calculator']/AXWindow[@AXRoleDescription='standard window']"
windowPathByIndex = "/AXApplication[@AXTitle='Calculator']/AXWindow[{}]"
resultGroupPath = windowPath + "/AXGroup[0]"
basicGroupPath = windowPath + "/AXGroup[1]"
basicGroupPath = windowPath + "/AXGroup"
scientificGroupPath = windowPath + "/AXGroup[2]"
programmerGroupPath = windowPath + "/AXGroup[1]"

print 'Starting the WebDriver session'
defaultCookies = [
    {'name': 'loop_delay', 'value': 1.00},
    {'name': 'command_delay', 'value': 0.500},
    {'name': 'implicit_timeout', 'value': 0.100},
    {'name': 'mouse_speed', 'value': 100},
    {'name': 'screen_shot_on_error', 'value': False},
    {'name': 'global_diagnostics_directory', 'value': '~/Desktop/'},
]
desiredCapabilities = {'platformName': 'Mac', 'deviceName': 'Mac', 'cookies': defaultCookies}
driver = webdriver.Remote(command_executor='http://localhost:4723/wd/hub',
                          desired_capabilities=desiredCapabilities)

driver.command_executor._commands['closeApp'] = ('POST', '/session/$sessionId/closeApp')
driver.command_executor._commands['elements'] = ('POST', '/session/$sessionId/elements')


print 'Opening the "Calculator" app'
driver.get("Calculator")

for c in count():
    new_xpath = windowPathByIndex.format(c)
    print "   checking:", new_xpath
    try:
        a_window = driver.find_element_by_xpath(new_xpath)
        print "found window:", a_window
        print
    except NoSuchElementException:
        print "... Nope, didn't find that one, guess we are done!"
        break
print

aboutPath = "/AXApplication[@AXTitle='Calculator']/AXWindow[@AXRoleDescription='dialog']"
about_window = None
try:
    about_window = driver.find_element_by_xpath(aboutPath)
    print "Found about window:", about_window
except:
    print "NO ABOUT WINDOW!"
print


def numToAXPath(num):
    if num == 0:
        return basicGroupPath + "/AXButton[@AXDescription='zero']"
    elif num == 1:
        return basicGroupPath + "/AXButton[@AXDescription='one']"
    elif num == 2:
        return basicGroupPath + "/AXButton[@AXDescription='two']"
    elif num == 3:
        return basicGroupPath + "/AXButton[@AXDescription='three']"
    elif num == 4:
        return basicGroupPath + "/AXButton[@AXDescription='four']"
    elif num == 5:
        return basicGroupPath + "/AXButton[@AXDescription='five']"
    elif num == 6:
        return basicGroupPath + "/AXButton[@AXDescription='six']"
    elif num == 7:
        return basicGroupPath + "/AXButton[@AXDescription='seven']"
    elif num == 8:
        return basicGroupPath + "/AXButton[@AXDescription='eight']"
    elif num == 9:
        return basicGroupPath + "/AXButton[@AXDescription='nine']"
    else:
        return ""


menuBarAXPath = "/AXApplication[@AXTitle='Calculator']/AXMenuBar"


def clickElement(element):
    if useNativeEvents > 0:
        # move and click the mouse like a user
        # actions = ActionChains(driver)
        # actions.click(element)
        # actions.perform()
        ActionChains(driver).click(element).perform()
    else:
        # use the traditional accessibility action
        element.click()


def do_some_calculations_with_clicks():
    print 'Clearing the calculator'
    clickElement(button_clear)
    clickElement(button_clear)

    rand1 = randint(0, 1000)
    rand2 = randint(0, 1000)

    print 'Entering the first number'
    for num in str(rand1):
        n = numToAXPath(int(num))
        print str(num) + ' --> ' + str(n)
        clickElement(driver.find_element_by_xpath(n))

    print 'Clicking the "+" button'
    clickElement(button_plus)

    print 'Entering the second number'
    for num in str(rand2):
        n = numToAXPath(int(num))
        print str(num) + ' --> ' + str(n)
        clickElement(driver.find_element_by_xpath(n))

    print 'Clicking the "=" button'
    clickElement(button_equals)

    print 'Reading result from screen'
    answer = text_result.text

    if int(answer) == (rand1 + rand2):
        print 'Correct Result:', answer
    else:
        print 'Incorect Result:', answer, 'Should be:', rand1 + rand2


def do_scientific_calcs():
    print 'Clearing the calculator'
    ActionChains(driver).send_keys('cc').perform()

    result = text_result.text
    if result != '0':
        print
        print "Expect 0, got:", result


    pie_button.click()
    result = text_result.text
    if not result.startswith('3.14159'):
        print
        print "Expected pi, got:", result

    ActionChains(driver).send_keys('c').perform()
    ActionChains(driver).send_keys('5').perform()
    factorial_button.click()
    result = text_result.text
    if result != '120':
        print
        print 'Expected 120, got:', result

    ActionChains(driver).send_keys('cc').perform()
    # ActionChains(driver).key_up(Keys.SHIFT).send_keys('9').key_down(Keys.SHIFT).send_keys('2+3').key_up(Keys.SHIFT).send_keys('0').key_down(Keys.SHIFT).send_keys('*5=').perform()
    ActionChains(driver).send_keys('(2+3)*5=').perform()
    result = text_result.text
    if result != '25':
        print
        print 'expected 25, got:', result

    ActionChains(driver).send_keys('c').perform()
    ActionChains(driver).send_keys('2+3*5=').perform()
    result = text_result.text
    if result != '17':
        print
        print 'expected 17, got:', result


def do_some_calculations_with_keystrokes():
    print 'Clearing the calculator'
    ActionChains(driver).send_keys('cc').perform()

    rand1 = randint(0, 1000)
    rand2 = randint(0, 1000)

    print 'Typing the first number'
    ActionChains(driver).send_keys(str(rand1)).perform()

    print 'Typing the "+" button'
    ActionChains(driver).send_keys("+").perform()

    print 'Typing the second number'
    ActionChains(driver).send_keys(str(rand2)).perform()

    print 'Typing the "=" button'
    ActionChains(driver).send_keys("=").perform()

    print 'Reading result from screen'
    answer = text_result.text

    if int(answer) == (rand1 + rand2):
        print 'Correct Result: ' + answer
    else:
        print 'Incorect Result: ' + answer, 'Should be:', rand1 + rand2


print 'Finding Some Elements...'


def calculator_mode(mode):
    xpath = "/AXApplication/AXMenuBar/AXMenuBarItem/AXMenu/AXMenuItem[@AXTitle='{}']".format(mode)
    return xpath


view_menu_xpath = "/AXApplication/AXMenuBar/AXMenuBarItem[@AXTitle='View']"
# driver.find_element_by_xpath(view_menu_xpath).click()
# driver.find_element_by_xpath(calculator_mode('Basic')).click()
# sleep(2)
# driver.find_element_by_xpath(view_menu_xpath).click()
# driver.find_element_by_xpath(calculator_mode('Scientific')).click()
# sleep(2)
# driver.find_element_by_xpath(view_menu_xpath).click()
# driver.find_element_by_xpath(calculator_mode('Programmer')).click()
# sleep(2)

print "Now by keys!"

# Command key is a toggle/shift

# ActionChains(driver).key_up(Keys.COMMAND).send_keys("1").key_down(Keys.COMMAND).perform()
# sleep(2)
# ActionChains(driver).key_up(Keys.COMMAND).send_keys("2").key_down(Keys.COMMAND).perform()
# sleep(2)
# ActionChains(driver).key_up(Keys.COMMAND).send_keys("3").key_down(Keys.COMMAND).perform()
# sleep(2)
ActionChains(driver).key_up(Keys.COMMAND).send_keys("2").key_down(Keys.COMMAND).perform()

button_clear = driver.find_element_by_xpath(basicGroupPath + "/AXButton[@AXDescription='clear']")
button_plus = driver.find_element_by_xpath(basicGroupPath + "/AXButton[@AXDescription='add']")
button_equals = driver.find_element_by_xpath(basicGroupPath + "/AXButton[@AXDescription='equals']")
text_result = driver.find_element_by_xpath(resultGroupPath +
                                           "/AXStaticText[@AXDescription='main display']")
calculator_menu = driver.find_element_by_xpath("/AXApplication/AXMenuBar/AXMenuBarItem[1]")
quit_menu_item_xpath = "/AXApplication/AXMenuBar/AXMenuBarItem/AXMenu/" + \
                       "AXMenuItem[@AXTitle='Quit Calculator']"
quit_menu_item = driver.find_element_by_xpath(quit_menu_item_xpath)

pie_button = driver.find_element_by_id('_NS:307')
factorial_button = driver.find_element_by_id('_NS:297')

# print
# print
# print 'Doing calculations with native mouse events...'

# useNativeEvents = 1
# do_some_calculations_with_clicks()

# print
# print
# print 'Doing calculations with accessibility actions...'

# useNativeEvents = 0
# do_some_calculations_with_clicks()

# print
# print
# useNativeEvents = 1
# print 'Doing calculations with native keystrokes...'

# do_some_calculations_with_keystrokes()

do_scientific_calcs()

# quit the webdriver instance
print 'Quitting the WebDriver session'

# driver.find_element_by_xpath(quit_menu_item_xpath).click()
# quit_menu_item.click()
# driver.execute('closeApp')
ActionChains(driver).send_keys(Keys.COMMAND + "q").perform()
driver.quit()



#################

# <AXButton AXDescription="right paren" AXIdentifier="_NS:140">
# <AXButton AXDescription="left paren" AXIdentifier="_NS:150">
# <AXButton AXDescription="inverse" AXIdentifier="_NS:160">
# <AXButton AXDescription="sine" AXIdentifier="_NS:170">
# <AXButton AXDescription="hyperbolic cosine" AXIdentifier="_NS:179">
# <AXButton AXDescription="x squared" AXIdentifier="_NS:188">
# <AXButton AXDescription="square root" AXIdentifier="_NS:197">
# <AXButton AXDescription="cube root" AXIdentifier="_NS:206">
# <AXButton AXDescription="nth root" AXIdentifier="_NS:215">
# <AXButton AXDescription="hyperbolic sine" AXIdentifier="_NS:224">
# <AXButton AXDescription="x to the power of y" AXIdentifier="_NS:233">
# <AXButton AXDescription="x cubed" AXIdentifier="_NS:242">
# <AXButton AXDescription="natural logarithm" AXIdentifier="_NS:251">
# <AXButton AXDescription="log base 10" AXIdentifier="_NS:261">
# <AXButton AXDescription="tangent" AXIdentifier="_NS:270">
# <AXButton AXDescription="hyperbolic tangent" AXIdentifier="_NS:279">
# <AXButton AXDescription="cosine" AXIdentifier="_NS:288">
# <AXButton AXDescription="x factorial" AXIdentifier="_NS:297">
# <AXButton AXDescription="pi" AXIdentifier="_NS:307">
# <AXButton AXDescription="random number" AXIdentifier="_NS:317">
# <AXButton AXDescription="e" AXIdentifier="_NS:326">
# <AXButton AXDescription="EE" AXIdentifier="_NS:333">
# <AXButton AXDescription="radians" AXIdentifier="_NS:343">
# <AXButton AXDescription="10 to the x" AXIdentifier="_NS:351">
# <AXButton AXDescription="secondary functions" AXIdentifier="_NS:357">
# <AXButton AXDescription="memory clear" AXIdentifier="_NS:366">
# <AXButton AXDescription="memory plus" AXIdentifier="_NS:375">
# <AXButton AXDescription="memory minus" AXIdentifier="_NS:384">
# <AXButton AXDescription="memory recall" AXIdentifier="_NS:393">
# <AXButton AXDescription="e to the x" AXIdentifier="_NS:402">
