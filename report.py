import string
from selenium.common import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import re
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
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









base_dir = os.path.dirname(os.path.abspath(__file__))
########################################################################################################################
uid_file = os.path.join(base_dir, 'uid')
list_file = os.path.join(base_dir, 'list')
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


if not uids:
    print("UID文件中没有可处理的UID，程序退出")
    exit(0)




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

driver.get('https://www.goofish.com/')

driver.set_window_size(500, 700)  # 设置浏览器窗口大小（宽度, 高度）
driver.set_window_position(0, 0)  # 左上角坐标为 (0, 0)
#driver.set_window_position(-500, -700)  # 左上角坐标为 (0, 0)

#time.sleep(1000)


time.sleep(3)

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
        try:
            with open(list_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            with open(list_file, 'w', encoding='utf-8') as f:
                for line in lines:
                    if line.strip() != uid:
                        f.write(line)
            print(f"删除UID: {uid}")
        except Exception as e:
            print(f"删除UID时发生错误: {e}")
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

            element_input_reason.send_keys(str(pagenumber)+str(reasonnumber)+'gdfgff'+''.join(random.choices(string.ascii_letters + string.digits, k=30)))
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
            time.sleep(1.5)


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


        except Exception as e:
            print('操作失败:', str(e))
