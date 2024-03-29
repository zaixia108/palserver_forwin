import ctypes
import os.path
import time

from PIL import Image, ImageTk

from th_pool import thread_control, stop
import win32api
import win32con
import win32gui
import tkinter as tk
from tkinter import ttk, messagebox


root = tk.Tk()
submit = thread_control.submit
RUN = None
check_update = tk.BooleanVar()
check_update.set(True)

if os.path.exists(r"mem\memreduct.exe"):
    print('内存整理器存在')
else:
    print('内存整理器不存在')
    ctypes.windll.user32.MessageBoxW(0, "内存整理器不存在", "错误", 0)
    exit(0)


def mem_clean():
    try:
        os.system('taskkill /f /im memreduct.exe')
    except:
        pass
    os.popen(r"mem\memreduct.exe")
    time.sleep(0.5)
    print('开始内存整理')
    hwnd = win32gui.FindWindow(r'#32770', "Mem Reduct")
    print(hwnd)
    #
    button = win32gui.FindWindowEx(hwnd, 0, "Button", "清理内存")
    print(button)

    # 点击按钮
    win32gui.SendMessage(button, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)

    time.sleep(0.05)
    # 释放按钮
    win32gui.SendMessage(button, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)
    print('内存整理完成')
    os.system('taskkill /f /im memreduct.exe')


def loop_clean():
    mem_clean()
    time.sleep(300)


def change_settings():
    if os.path.exists(r"st\steamapps\common\PalServer\Pal\Saved\Config\WindowsServer\PalWorldSettings.ini"):
        print('配置文件存在')
    else:
        print('配置文件不存在')
        ctypes.windll.user32.MessageBoxW(0, "配置文件不存在", "错误", 0)
        return None
    os.popen(r"start st\steamapps\common\PalServer\Pal\Saved\Config\WindowsServer\PalWorldSettings.ini")


def start_server():
    global RUN
    if os.path.exists(r"st\steamapps\common\PalServer\PalServer.exe"):
        print('服务器存在')
    else:
        print('服务器不存在')
        ctypes.windll.user32.MessageBoxW(0, "服务器不存在", "错误", 0)
        return None
    if check_update:
        cmd = "st\steamcmd.exe +login anonymous +app_update 2394010 validate +quit"
        os.system(cmd)
    else:
        pass
    os.popen(r"start st\steamapps\common\PalServer\PalServer.exe port=8211")
    #开始loop清理内存
    RUN = submit(func=loop_clean, name='loop_clean', state=True, error_stop=False)


def stop_server():
    global RUN
    if RUN is None:
        print('服务器未启动')
        ctypes.windll.user32.MessageBoxW(0, "服务器未启动", "错误", 0)
        return None
    if RUN.alive():
        RUN.stop()
        print('停止loop清理内存')
    os.system('taskkill /f /im PalServer.exe')
    time.sleep(1)
    stop()


def set_update():
    global check_update
    state = check_update.get()
    if state:
        check_update.set(True)
    else:
        check_update.set(False)


root.title('Pal服务器一键启动')
root.geometry('460x460')
root.resizable(False, False)
ico = ImageTk.PhotoImage(Image.open('108.ico'))
root.iconphoto(False, ico)

pic = ImageTk.PhotoImage(Image.open('pal.png'))
label = tk.Label(root, image=pic)
label.grid(row=0, column=0, padx=10, pady=10)

button_settings = ttk.Button(root, text='修改配置', command=change_settings, width=60)
button_settings.grid(row=3, column=0, padx=10, pady=10)

button_start = ttk.Button(root, text='启动服务器', command=start_server, width=60)
button_start.grid(row=1, column=0, padx=10, pady=10)

check_box = ttk.Checkbutton(root, text='检查更新', variable=check_update, onvalue=True, offvalue=False, command=set_update)
check_box.grid(row=2, column=0, padx=10, pady=10)

button_stop = ttk.Button(root, text='停止服务器', command=stop_server, width=60)
button_stop.grid(row=4, column=0, padx=10, pady=10)

label = tk.Label(root, text='powerd by 在下108', font=('微软雅黑', 10))
label.grid(row=5, column=0, padx=10, pady=10)

root.mainloop()