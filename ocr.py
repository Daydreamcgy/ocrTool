import screenshot_tool
import ocr_recognition
import tkinter as tk
from tkinter import messagebox
import keyboard  # 导入 keyboard 库

def show_ocr_result(text):
    def copy_to_clipboard():
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()  # 现在它在剪贴板上

    root = tk.Tk()
    root.title("OCR 结果")
    
    text_box = tk.Text(root, wrap='word', height=15, width=50)
    text_box.pack(padx=10, pady=10)
    text_box.insert('1.0', text)
    text_box.config(state='disabled')  # 设置为只读

    copy_button = tk.Button(root, text="复制", command=copy_to_clipboard)
    copy_button.pack(pady=10)

    root.mainloop()

def take_screenshot_and_ocr():
    # 截图并获取截图路径
    screenshot_path = screenshot_tool.take_screenshot()
    if screenshot_path:
        # 进行OCR识别
        ocr_result = ocr_recognition.ocr_recognition(screenshot_path)
        if ocr_result:
            show_ocr_result(ocr_result)

def main():
    # 提示用户按 Alt+R 键进行截图并进行 OCR 识别
    print("Press Alt+R to take a screenshot and perform OCR.")
    # 绑定快捷键 Alt+R 到 take_screenshot_and_ocr 函数
    keyboard.add_hotkey('alt+r', take_screenshot_and_ocr)
    # 等待用户按 Esc 键退出程序
    print("Press Esc to exit.")
    keyboard.wait('esc')

if __name__ == "__main__":
    main()