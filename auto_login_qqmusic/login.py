# @Author: allen
# @Date: May 20 15:50 2020
import time

from selenium import webdriver

driver = webdriver.Chrome('../drivers/chromedriver')

driver.set_page_load_timeout(20)
driver.get('https://y.qq.com')
driver.maximize_window()

# time.sleep(10)
#
# for d in driver.find_elements_by_css_selector('#divdialog_0'):
#     d.find_element_by_tag_name('a').click()
#     break

driver.find_element_by_class_name('top_login__link.js_login').click()

# time.sleep(5)
#
# driver.find_element_by_id('switcher_plogin').click()

time.sleep(3)

driver.find_element_by_name('u').send_keys('337657561')
driver.find_element_by_name('p').send_keys('zaiguqingguo')


time.sleep(3)

driver.quit()