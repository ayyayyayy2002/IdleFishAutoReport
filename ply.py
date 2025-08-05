import json
import time
import mouse

def replay_mouse_track(filename: str, start_x: int = 100, start_y: int = 100):
    # 读取轨迹文件
    try:
        with open(filename, 'r') as f:
            events = json.load(f)
    except Exception as e:
        print(f"❌ 无法读取文件 {filename}：{e}")
        return

    if not events:
        print("❌ 轨迹为空")
        return

    print("🎬 准备回放轨迹（3秒后开始）...")
    time.sleep(3)

    # 找到第一个有效的 MoveEvent 作为基准点
    dx = dy = 0
    for event in events:
        if event['type'] == 'MoveEvent' and event['x'] is not None and event['y'] is not None:
            dx = event['x'] - start_x
            dy = event['y'] - start_y
            break
    else:
        print("❌ 找不到有效的鼠标移动坐标")
        return

    print(f"📐 起始坐标偏移：dx={dx}, dy={dy}")

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
            new_x = x - dx
            new_y = y - dy
            mouse.move(new_x, new_y, absolute=True, duration=0)

        elif etype == 'ButtonEvent':
            if ev == 'down':
                mouse.press(button=button)
            elif ev == 'up':
                mouse.release(button=button)

    print("✅ 回放完成")


if __name__ == '__main__':
    # 示例：播放 mouse_track.json 到 (100, 100) 起始位置
    replay_mouse_track('mouse_track.json', 100, 100)
