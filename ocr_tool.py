import pyautogui
import keyboard
import time
from datetime import datetime
from tkinter import Tk, Canvas
import os

def select_region():
    root = Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-alpha", 0.3)
    canvas = Canvas(root, cursor="cross")
    canvas.pack(fill="both", expand=True)

    region = []
    rect = None

    def on_mouse_down(event):
        nonlocal rect
        region.append((event.x, event.y))
        rect = canvas.create_rectangle(event.x, event.y, event.x, event.y, outline='red')

    def on_mouse_move(event):
        nonlocal rect
        if rect:
            canvas.coords(rect, region[0][0], region[0][1], event.x, event.y)

    def on_mouse_up(event):
        region.append((event.x, event.y))
        root.quit()

    canvas.bind("<ButtonPress-1>", on_mouse_down)
    canvas.bind("<B1-Motion>", on_mouse_move)
    canvas.bind("<ButtonRelease-1>", on_mouse_up)

    root.mainloop()
    root.destroy()

    if len(region) == 2:
        x1, y1 = region[0]
        x2, y2 = region[1]
        # 确保坐标是正确的
        x1, x2 = sorted([x1, x2])
        y1, y2 = sorted([y1, y2])
        return (x1, y1, x2 - x1, y2 - y1)
    else:
        return None

def take_screenshot():
    print("请拖动鼠标选择截图区域...")
    region = select_region()
    if region:
        screenshot = pyautogui.screenshot(region=region)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        os.makedirs('pix', exist_ok=True)
        screenshot_path = f'pix/screenshot_{timestamp}.png'
        screenshot.save(screenshot_path)
        print(f'Screenshot saved as {screenshot_path}')
        return screenshot_path
    else:
        print("未选择区域，截图取消。")
        return None

def main():
    print("Press Alt+R to take a screenshot.")
    keyboard.add_hotkey('alt+r', take_screenshot)
    keyboard.wait('esc')

if __name__ == "__main__":
    main()