import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from user import User

TEST_STUDENT = User(username="EWCJ_Student1", password="EWCJ_Student1")

# Get login URL from Bulb RESTful API
d2l_login = requests.get('https://www.blub.tech/auth').text.strip('"')

# Open login page
driver = webdriver.Chrome()
driver.get(d2l_login)


d2l_only = driver.find_element_by_xpath("/html/body/main/div[2]/p[2]/a")
d2l_only.click()

username_input = driver.find_element_by_id("userName")
username_input.send_keys(TEST_STUDENT.username)
password_input = driver.find_element_by_id("password")
password_input.send_keys(TEST_STUDENT.password)

login_btn = driver.find_element_by_xpath('//*[@id="externlLoginForm"]/form/button')
#login_btn.click()


"""
# Click login button
login_btn = driver.find_element_by_id("mun-login")
login_btn.click()

# Fill in mun ID and password
username_input = driver.find_element_by_id("username")
username_input.send_keys(TEST_STUDENT.username)
password_input = driver.find_element_by_id("password")
password_input.send_keys(TEST_STUDENT.password)

# Submit login form
submit_btn = username_input = driver.find_element_by_xpath('//*[@id="fm1"]/div[3]/section/input[4]')
submit_btn.click()
"""

# Get credentials from URL
redirected_url = driver.current_url
TEST_STUDENT.set_token(redirected_url)
print(TEST_STUDENT.redirect_url)
