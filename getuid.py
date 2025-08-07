import random
import re
import os
import traceback
import time

from selenium.common import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

base_dir = os.path.dirname(os.path.abspath(__file__))
########################################################################################################################
uid_file = os.path.join(base_dir, 'uid')
list_file = os.path.join(base_dir, 'list')
iid_file = os.path.join(base_dir, 'iid')
collections = set()
userids = set()

########################################################################################################################
import random

# 匀加速运动位置函数：s = 0.5 * a * t^2
def ease_out_quart(T, a):
    return 0.5 * a * T * T

# 生成从 (x0, y0) 到 (x1, y1) 的匀加速轨迹
def generate_track(x0, y0, x1, y1, steps=60):
    track = []

    dx = x1 - x0
    dy = y1 - y0

    # 随机生成 Y 轴加速度，范围可调
    ay = random.uniform(0.002, 0.01)
    ax = ay * 2

    # 总时间归一化为1，steps是分段数
    for i in range(steps + 1):
        T = i / steps
        sx = ease_out_quart(T, ax)
        sy = ease_out_quart(T, ay)

        xt = x0 + dx * sx / ease_out_quart(1, ax)
        yt = y0 + dy * sy / ease_out_quart(1, ay)

        track.append([xt - x0, yt - y0])  # 相对坐标

    return track



user_data_dir = os.path.join(base_dir, 'User Data')
chrome_binary_path = os.path.join(base_dir, 'chrome-win', 'chrome.exe')
executable_path= os.path.join(base_dir, 'chrome-win', 'chromedriver.exe')

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(f'--user-data-dir={user_data_dir}')
options.binary_location = chrome_binary_path
options.add_argument('--proxy-server="direct://"')
options.add_argument('--proxy-bypass-list=*')
options.add_argument("--disable-gpu")
options.add_argument("--disable-sync")
options.add_argument("disable-cache")
options.add_experimental_option("prefs",
                                {"credentials_enable_service": False, "profile.password_manager_enabled": False})

service = Service(executable_path=executable_path)
driver = webdriver.Chrome(service=service, options=options)

driver.get('https://www.goofish.com/collection')

time.sleep(10)
driver.set_window_size(500, 700)  # 设置浏览器窗口大小（宽度, 高度）
driver.set_window_position(0, 0)  # 左上角坐标为 (0, 0)
#driver.set_window_position(-500, -700)  # 左上角坐标为 (0, 0)





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


with open(iid_file, 'a', encoding='utf-8') as file:
    for collection in collections:
        file.write(collection + '\n')  # 写入每个元素后跟一个换行符
collections = set()


try:
    with open(iid_file, 'r', encoding='utf-8') as file:  # 以读取模式打开文件
        for line in file:
            line = line.strip()  # 去掉行首尾的空白字符
            if line.isdigit():
                collections.add(line)
except Exception as e:
    print(f"无法读取IID文件: {e}")











for collection in collections:
    try:

        driver.get(f'https://www.goofish.com/item?id={collection}')
        try:
            iframe = driver.find_element(By.ID, "baxia-dialog-content")
            print('发现验证码')
            driver.switch_to.frame(iframe)
            slider = driver.find_element(By.ID, 'nc_1_n1z')  # 你的滑块元素
            rect = slider.rect
            x0 = rect['x'] + rect['width'] / 2
            y0 = rect['y'] + rect['height'] / 2
            distance = 500
            jitter = random.uniform(-300, 300)
            track = generate_track(x0, y0, x0 + distance, y0 + jitter)

            # 拖动滑块的 JS 脚本
            drag_script = """
            const element = arguments[0];
            const moves = arguments[1];
            const rect = element.getBoundingClientRect();
            const startX = rect.left + rect.width / 2;
            const startY = rect.top + rect.height / 2;

            const dispatchMouseEvent = (type, x, y) => {
                const event = new MouseEvent(type, {
                    clientX: x,
                    clientY: y,
                    bubbles: true
                });
                element.dispatchEvent(event);
            };

            dispatchMouseEvent('mousedown', startX, startY);

            let i = 0;
            function step() {
                if (i >= moves.length) {
                    dispatchMouseEvent('mouseup', startX + moves[moves.length - 1][0], startY + moves[moves.length - 1][1]);
                    return;
                }
                const [dx, dy] = moves[i];
                dispatchMouseEvent('mousemove', startX + dx, startY + dy);
                i++;
                requestAnimationFrame(step);
            }
            requestAnimationFrame(step);
            """

            driver.execute_script(drag_script, slider, track)
            time.sleep(2)
        except NoSuchElementException as e:
            print('无验证码:', str(e))





        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href*="userId"]'))
        )


        href = element.get_attribute('href')
        match = re.search(r'userId=(\d+)', href)

        if match:
            id_value = match.group(1)
            userids.add(id_value)

        try:
            with open(iid_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            with open(iid_file, 'w', encoding='utf-8') as f:
                for line in lines:
                    if line.strip() != collection:
                        f.write(line)
            print(f"删除UID: {collection}")
        except Exception as e:
            print(f"删除UID时发生错误: {e}")

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


