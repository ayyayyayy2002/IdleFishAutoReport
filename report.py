import random
import string
import subprocess
from dotenv import load_dotenv
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import time
import re
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
########################################################################################################################
uid_file = os.path.join(base_dir, 'uid.txt')
uids = []


########################################################################################################################


try:
    with open(uid_file, 'r', encoding='utf-8') as file:  # 以读取模式打开文件
        for line in file:
            line = line.strip()  # 去掉行首尾的空白字符
            if line.isdigit():
                uids.append(line)
except Exception as e:
    print(f"无法读取UID文件: {e}")
    exit(0)

if not uids:
    print("uid.txt 文件中没有可处理的UID，程序退出")
    exit(0)
"""
version_main = 121
user_data_dir = os.path.join(base_dir, 'User Data')
chrome_binary_path = os.path.join(base_dir, 'chrome-win', 'chrome.exe')
options = uc.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(f'--user-data-dir={user_data_dir}')
options.binary_location = chrome_binary_path
options.add_argument('--proxy-server="direct://"')
options.add_argument('--proxy-bypass-list=*')
#options.add_argument("--disable-gpu")
#options.add_argument("--disable-sync")
#options.add_argument("disable-cache")  # 禁用缓存
options.add_experimental_option("prefs",
                                {"credentials_enable_service": False, "profile.password_manager_enabled": False})

driver = uc.Chrome(options=options, version_main=version_main, driver_executable_path="chromedriver.exe")
options.add_experimental_option("prefs",
                                {"credentials_enable_service": False, "profile.password_manager_enabled": False})
driver.get(f'https://www.goofish.com/collection')
"""
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# 假设这两行在你代码里已定义，无需改动也不赋值
user_data_dir = os.path.join(base_dir, 'User Data')
chrome_binary_path = os.path.join(base_dir, 'chrome-win', 'chrome.exe')

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

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

driver.get('https://www.goofish.com/collection')

driver.set_window_size(500, 700)  # 设置浏览器窗口大小（宽度, 高度）
driver.set_window_position(0, -10)  # 左上角坐标为 (0, 0)

#time.sleep(1000)

try:
    WebDriverWait(driver, 5).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "alibaba-login-box"))  # 根据 ID 切换到 iframe
    )

    password_login_tab = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "password-login-tab-item"))  # 根据 class 定位
    )
    password_login_tab.click()

    fm_login_id = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "fm-login-id"))  # 根据 ID 定位输入框
    )
    fm_login_id.send_keys(id)

    fm_login_password = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "fm-login-password"))  # 根据 ID 定位输入框
    )
    fm_login_password.send_keys("aaa")

    command = 'KeymouseGo_v5_2-win.exe 登录验证码.json5'
    subprocess.run(command, shell=True)
    time.sleep(3)
except Exception as e:
    print(e)

for uid in uids:
    itemids = set()
    try:
        with open(uid_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        with open(uid_file, 'w', encoding='utf-8') as f:
            for line in lines:
                if line.strip() != uid:
                    f.write(line)
        print(f"删除UID: {uid}")
    except Exception as e:
        print(f"删除UID时发生错误: {e}")

    driver.get(f'https://www.goofish.com/personal?&userId={uid}')

    try:
        elements = WebDriverWait(driver, 3).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'cardWarp--dZodM57A'))
        )
        for element in elements:
            # 查找元素中的 href 属性包含 id 的 a 标签
            a_tag = element.find_element(By.XPATH, './/a[contains(@href, "id")]')
            href = a_tag.get_attribute('href')

            # 使用正则表达式匹配 id 值
            match = re.search(r'id=(\d+)', href)
            if match:
                itemids.add(match.group(1))
        print(itemids)
    except Exception as e:
        print('无商品')
        continue

    for itemid in itemids:


        print(itemid)
        urls = {
            1: [
                f"https://h5.m.goofish.com/wow/moyu/moyu-project/cro-report-center/pages/report-form?titleVisible=false&useCusFont=true&pageSourceCode=itemDetail&reportSubjectTypeCode=ITEM&reportSubjectId={itemid}&reportTypeCode=PROHIBIT&formId=PROHIBIT_ITEM&spm=a2170.29608093.0.0",
                6],
            2: [
                f"https://h5.m.goofish.com/wow/moyu/moyu-project/cro-report-center/pages/report-form?titleVisible=false&useCusFont=true&pageSourceCode=itemDetail&reportSubjectTypeCode=ITEM&reportSubjectId={itemid}&reportTypeCode=PROHIBIT&formId=PROHIBIT_POLITICS_ITEM&spm=a2170.29608093.0.0",
                2],
            3: [
                f"https://h5.m.goofish.com/wow/moyu/moyu-project/cro-report-center/pages/report-form?titleVisible=false&useCusFont=true&pageSourceCode=itemDetail&reportSubjectTypeCode=ITEM&reportSubjectId={itemid}&reportTypeCode=PROHIBIT&formId=PROHIBIT_BAD_INFO_ITEM&spm=a2170.29608093.0.0",
                6],
            4: [
                f"https://h5.m.goofish.com/wow/moyu/moyu-project/cro-report-center/pages/report-form?titleVisible=false&useCusFont=true&pageSourceCode=itemDetail&reportSubjectTypeCode=ITEM&reportSubjectId={itemid}&reportTypeCode=FAKE_COMMODITY&formId=FAKE_COMMODITY_ITEM&spm=a2170.29608093.0.0",
                3],
            5: [
                f"https://h5.m.goofish.com/wow/moyu/moyu-project/cro-report-center/pages/report-form?titleVisible=false&useCusFont=true&pageSourceCode=itemDetail&reportSubjectTypeCode=ITEM&reportSubjectId={itemid}&reportTypeCode=RENT_HOUSE_REPORT&formId=RENT_HOUSE_ITEM&spm=a2170.29608093.0.0",
                6],
            6: [
                f"https://h5.m.goofish.com/wow/moyu/moyu-project/cro-report-center/pages/report-form?titleVisible=false&useCusFont=true&pageSourceCode=itemDetail&reportSubjectTypeCode=ITEM&reportSubjectId={itemid}&reportTypeCode=LANFA_COMMODITY&formId=OTHER_ITEM&spm=a2170.29608093.0.0",
                3],

        }
        #pagenumber = random.randint(1, 6)
        pagenumber = 6
        url = urls[pagenumber]

        reasonnumber = random.randint(1, url[1])

        driver.get(url[0])
        xpaths = {
            1: '/html/body/div/div/div[4]/div/div[1]/div/div[1]/div/div[2]/div[1]/div/div[1]',
            2: '//*[@id="root"]/div/div[4]/div/div[1]/div/div[1]/div/div[2]/div[1]/div/div[2]',
            3: '/html/body/div/div/div[4]/div/div[1]/div/div[1]/div/div[2]/div[2]/div/div[1]',
            4: '/html/body/div/div/div[4]/div/div[1]/div/div[1]/div/div[2]/div[2]/div/div[2]',
            5: '/html/body/div/div/div[4]/div/div[1]/div/div[1]/div/div[2]/div[3]/div/div[1]',
            6: '/html/body/div/div/div[4]/div/div[1]/div/div[1]/div/div[2]/div[3]/div/div[2]',
        }

        try:
            # 选择理由
            element_choose_reason = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable(
                    (By.XPATH, xpaths[reasonnumber]))
            )
            element_choose_reason.click()
            print('选择理由')


            element_input_reason = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div/div/div[4]/div/div[1]/div/div[2]/div/div[2]/textarea'))
            )

            element_input_reason.send_keys(str(pagenumber)+str(reasonnumber)+'站外微信引流诈骗，骗取钱财，色情网站推广'+''.join(random.choices(string.ascii_letters + string.digits, k=30)))
            print('输入文字')

            # 允许消息
            element_allow_message = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[4]/div/div[1]/div/div[3]/img'))
            )
            element_allow_message.click()
            print('允许消息')

            # 提交举报
            element_submit_report = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[4]/div/div[2]/div'))
            )
            element_submit_report.click()
            print('提交表单')
            time.sleep(2)
            max_attempts = 10
            attempts = 0

            while attempts < max_attempts:
                try:
                    element = driver.find_element(By.XPATH, '//*[@id="baxia-dialog-content"]')
                    if element.is_displayed():
                        print('发现验证码')
                        #time.sleep(1000)

                        random_number = random.randint(1, 5)
                        command = f'KeymouseGo_v5_2-win.exe 表单验证码{str(random_number)}.json5'
                        subprocess.run(command, shell=True)

                        attempts += 1
                        time.sleep(2)  # 可选：给验证码处理一点反应时间
                    else:
                        print("元素不可见")
                        break
                except Exception:
                    print("未找到验证码元素")
                    break
            else:
                print("达到最大尝试次数，停止处理验证码")
                exit(200)














        except Exception as e:
            print('操作失败:', str(e))
