import json
import time
import mouse

# 读取轨迹文件
with open('mouse_track.json', 'r') as f:
    events = json.load(f)

if not events:
    print("❌ 轨迹为空")
    exit()

print("🎬 准备回放轨迹（3秒后开始）...")
time.sleep(3)

start_time = events[0]['time']

for i, event in enumerate(events):
    # 等待与上一个事件的间隔
    if i > 0:
        delay = event['time'] - events[i - 1]['time']
        time.sleep(delay)

    x = event['x']
    y = event['y']
    etype = event['type']
    ev = event['event_type']
    button = event['button']

    if etype == 'MoveEvent' and x is not None and y is not None:
        mouse.move(x, y, absolute=True, duration=0)

    elif etype == 'ButtonEvent':
        if ev == 'down':
            mouse.press(button=button)
        elif ev == 'up':
            mouse.release(button=button)

print("✅ 回放完成")
