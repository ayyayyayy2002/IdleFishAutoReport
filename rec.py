import mouse
import json
import time
import os

recording = False
events = []
start_time = None

def handler(event):
    global recording, events, start_time

    if isinstance(event, mouse.ButtonEvent) and event.button == 'right' and event.event_type == 'down':
        if not recording:
            print("🟢 开始录制鼠标轨迹（再次右键停止）")
            recording = True
            start_time = time.time()
            events.clear()
        else:
            print("🔴 停止录制，保存文件到 rec 文件夹")
            recording = False
            mouse.unhook_all()

            # 构建保存目录和文件名
            timestamp = int(time.time())
            os.makedirs("rec", exist_ok=True)
            file_path = os.path.join("rec", f"{timestamp}.json")

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

            with open(file_path, 'w') as f:
                json.dump(recorded, f, indent=2)

            print(f"✅ 已保存到 {file_path}")

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
