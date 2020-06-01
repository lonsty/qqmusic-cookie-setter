import time

from selenium import webdriver
from selenium.webdriver import ActionChains

HOST = 'https://y.qq.com'
WEBDRIVER = '../drivers/chromedriver'
SET_COOKIE_API = 'http://cn.lonsty.me:8179/user/setCookie'
TIMEOUT = 20
SETTINGS = {}


driver = webdriver.Chrome(SETTINGS.get('webdriver', WEBDRIVER))
# Open https://y.qq.com in Chrome
driver.get(HOST)
# Open login page
driver.find_element_by_link_text('登录').click()

# Switch to the top window
driver.switch_to.window(driver.window_handles[-1])

# Switch to the login iframe step by step
while 1:
    try:
        driver.switch_to.frame('frame_tips')  # iframe frame_tips
        break
    except Exception:
        time.sleep(0.5)

while 1:
    try:
        driver.switch_to.frame('ptlogin_iframe')  # iframe ptlogin_iframe
        break
    except Exception:
        time.sleep(0.5)

time.sleep(3)
# Switch to input popup, fill username and password, then login
driver.find_element_by_id('switcher_plogin').click()
driver.find_element_by_name('u').send_keys('919100841')
driver.find_element_by_name('p').send_keys('zaiguqingguo.')
driver.find_element_by_id('login_button').click()

# driver.switch_to.window(driver.window_handles[-1])
# tcaptcha_iframe

while 1:
    try:
        driver.switch_to.frame('tcaptcha_iframe')  # iframe ptlogin_iframe
        break
    except Exception:
        time.sleep(0.5)

# element = driver.find_element_by_id('tcaptcha_drag_thumb')
# element = driver.find_element_by_id('tcaptcha_drag_button')
element = driver.find_element_by_id('slideBlock')
# element = driver.find_element_by_class_name('tc-dragable-icon')
# driver.execute_script("arguments[0].setAttribute('class', 'tc-jpp-img')", element)
print(element.location)
print(element.size)
print(driver.find_element_by_id('slideBg').get_attribute('src'))

# print(element)
# ActionChains(driver).click_and_hold(element).perform()
# time.sleep(5)
# ActionChains(driver).move_by_offset(xoffset=150, yoffset=0).perform()
# # 此处一定要睡，如果不睡的话，可能还没拉到那个位置就直接进行下一步的动作了
# time.sleep(1.5)
# ActionChains(driver).click().perform()
# time.sleep(10)
# ActionChains(driver).click_and_hold(element).perform()
# ActionChains(driver).drag_and_drop_by_offset(element, xoffset=100, yoffset=0).perform()
time.sleep(1)
print('-' * 160, ' start')
ActionChains(driver).click_and_hold(element).move_by_offset(xoffset=450, yoffset=0).pause(1).release().perform()
# ActionChains(driver).drag_and_drop_by_offset(element, 170, 0).perform()
print('-' * 160, ' end')

# driver.find_element_by_id('e_reload').click()

# time.sleep(5)
# ActionChains(driver).move_by_offset(xoffset=150, yoffset=0).perform()

time.sleep(1)

cookies = driver.get_cookies()

cookies = {item.get('name'): item.get('value') for item in cookies}
print(cookies)
# # Check if login is successful by checking cookie value of qm_keyst
# time_cost = 0
# while 1:
#     cookies_list = driver.get_cookies()
#     cookies_dict = {item.get('name'): item.get('value') for item in cookies_list}
#     if cookies_dict.get('qm_keyst'):
#         break
#     if time_cost > TIMEOUT:
#         raise TimeoutError('Login timeout.')
#     time.sleep(0.5)
#     time_cost += 0.5
# driver.quit()