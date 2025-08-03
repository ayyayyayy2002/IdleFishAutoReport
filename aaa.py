import re
import os
import traceback
import subprocess
import time
from dotenv import load_dotenv
import undetected_chromedriver as uc
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


base_dir = os.path.dirname(os.path.abspath(__file__))
########################################################################################################################
uid_file = os.path.join(base_dir, 'uid.txt')
list_file = os.path.join(base_dir, 'list')
log_file = os.path.join(base_dir,'循环记录.txt')
collections = set()
userids = set()
########################################################################################################################


version_main = 121
user_data_dir = os.path.join(base_dir, 'User Data')
chrome_binary_path = os.path.join(base_dir, 'chrome-win', 'chrome.exe')
options = uc.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(f'--user-data-dir={user_data_dir}')
options.binary_location = chrome_binary_path
options.add_argument('--proxy-server="direct://"')
options.add_argument('--proxy-bypass-list=*')
options.add_argument("--disable-gpu")
options.add_argument("--disable-sync")
options.add_argument("disable-cache")  # 禁用缓存
options.add_experimental_option("prefs",{"credentials_enable_service":False,"profile.password_manager_enabled":False})
driver = uc.Chrome(options=options, version_main=version_main,driver_executable_path="chromedriver.exe")
driver.get(f'https://www.goofish.com/collection')

time.sleep(1000)
