import time

from selenium import webdriver
from selenium.webdriver import ActionChains

driver = webdriver.Chrome('../drivers/chromedriver')
driver.get('https://jqueryui.com/resources/demos/sortable/connect-lists.html')


draggable = driver.find_element_by_xpath("//ul[@id='sortable1']/li[1]")
droppable = driver.find_element_by_xpath("//ul[@id='sortable2']/li[1]")

ActionChains(driver).drag_and_drop(draggable, droppable).perform()


draggable2 = driver.find_element_by_xpath("//ul[@id='sortable1']/li[1]")
ActionChains(driver).drag_and_drop_by_offset(draggable2, 150, 0).perform()


draggable3 = driver.find_element_by_xpath("//ul[@id='sortable1']/li[1]")
ActionChains(driver).click_and_hold(draggable3).move_by_offset(150, 0).pause(2).release().perform()