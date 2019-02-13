import unittest
from selenium import webdriver

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("http://google.com")
driver.quit()