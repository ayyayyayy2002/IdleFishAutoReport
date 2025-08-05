import re
import os
import traceback
import time


from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

base_dir = os.path.dirname(os.path.abspath(__file__))
########################################################################################################################
uid_file = os.path.join(base_dir, 'uid.txt')
list_file = os.path.join(base_dir, 'list')
log_file = os.path.join(base_dir,'循环记录.txt')
collections = set()
userids = set()

########################################################################################################################


user_data_dir = os.path.join(base_dir, 'User Data')
chrome_binary_path = os.path.join(base_dir, 'chrome-win', 'chrome.exe')
executable_path= os.path.join(base_dir, 'chrome-win', 'chromedriver.exe')

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(f'--user-data-dir={user_data_dir}')
options.binary_location = chrome_binary_path
options.add_argument('--proxy-server="direct://"')
options.add_argument('--proxy-bypass-list=*')
# options.add_argument("--disable-gpu")
# options.add_argument("--disable-sync")
# options.add_argument("disable-cache")  # 禁用缓存
options.add_experimental_option("prefs",
                                {"credentials_enable_service": False, "profile.password_manager_enabled": False})

service = Service(executable_path=executable_path)
driver = webdriver.Chrome(service=service, options=options)

driver.get('https://www.goofish.com/collection')

time.sleep(10)
driver.set_window_size(500, 700)  # 设置浏览器窗口大小（宽度, 高度）
driver.set_window_position(0, 0)  # 左上角坐标为 (0, 0)





try:
    parent_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,  "/html/body/div[2]/div[2]/div[1]/div[2]/div[2]/div"))
    )


    # 获取该父级元素下的所有同级别子元素
    elements = parent_element.find_elements(By.TAG_NAME, "a")


    for element in elements:

        href = element.get_attribute("href")  # 获取href属性
        if href:
            # 使用正则表达式提取itemid
            match = re.search(r"id=(\d+)", href)
            if match:
                itemid = match.group(1)
                print(f"Extracted itemid: {itemid}")
                collections.add(itemid)
                button_xpath = ".//div[contains(@class, 'wantTo--v1xUeJJj')]"
                button_element = element.find_element(By.XPATH, button_xpath)
                if button_element:
                    # 使用 JavaScript 触发点击
                    driver.execute_script("arguments[0].click();", button_element)



except Exception as e:
    print(e)
    traceback.print_exc()

for collection in collections:
    try:

        driver.get(f'https://www.goofish.com/item?id={collection}')
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href*="userId"]'))
        )


        href = element.get_attribute('href')
        match = re.search(r'userId=(\d+)', href)

        if match:
            id_value = match.group(1)
            userids.add(id_value)
    except Exception:
        print('无法提取用户id')


driver.quit()



with open(list_file, 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        uid = line.strip()
        userids.add(uid)
with open(list_file, 'w', encoding='utf-8') as file:
    for uid in userids:
        file.write(uid + '\n')  # 写入每个元素后跟一个换行符
with open(uid_file, 'w', encoding='utf-8') as file:
    for uid in userids:
        file.write(uid + '\n')  # 写入每个元素后跟一个换行符


print("提取的id集合：", userids)


