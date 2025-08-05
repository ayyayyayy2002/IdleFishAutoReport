import mouse
import json
import time

recording = False
events = []
start_time = None

def handler(event):
    global recording, events, start_time

    # 如果右键按下，切换开始/停止
    if isinstance(event, mouse.ButtonEvent) and event.button == 'right' and event.event_type == 'down':
        if not recording:
            print("🟢 开始录制鼠标轨迹（再次右键停止）")
            recording = True
            start_time = time.time()
            events.clear()
        else:
            print("🔴 停止录制，保存文件 mouse_track.json")
            recording = False
            mouse.unhook_all()

            # 保存事件数据
            recorded = []
            for e in events:
                recorded.append({
                    'time': e.time - start_time,
                    'type': type(e).__name__,
                    'event_type': getattr(e, 'event_type', None),
                    'button': getattr(e, 'button', None),
                    'x': getattr(e, 'x', None),
                    'y': getattr(e, 'y', None),
                })

            with open('mouse_track.json', 'w') as f:
                json.dump(recorded, f, indent=2)

    # 如果正在录制，则记录所有事件
    if recording:
        events.append(event)

print("💡 右键开始录制，再次右键停止录制")
mouse.hook(handler)

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("手动中断")
    mouse.unhook_all()
