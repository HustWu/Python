# coding = utf-8
import win32api
import win32gui
import win32con
import win32clipboard as clipboard
import time
from PIL import Image
from io import BytesIO #python3,新增字节流
import requests
from lxml import etree

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                         ' AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/79.0.3945.117 Safari/537.36' }

###############################
#  微信发送（文本及图片）
###############################

#定义指定图片文件复制到剪贴板函数##########
def pic_ctrl_c(pathfile):
    img = Image.open(pathfile)
    output = BytesIO()#如是StringIO分引起TypeError: string argument expected, got 'bytes'
    img.convert("RGB").save(output, "BMP")# 以BMP格式保存流
    data = output.getvalue()[14:]#bmp文件头14个字节丢弃
    output.close()
    clipboard.OpenClipboard() #打开剪贴板
    clipboard.EmptyClipboard() #先清空剪贴板
    clipboard.SetClipboardData(win32con.CF_DIB, data)  #将图片放入剪贴板
    clipboard.CloseClipboard()
    return

def send_m():
    # 以下为“CTRL+V”组合键,回车发送，（方法一）
    win32api.keybd_event(17, 0, 0, 0)  # 有效，按下CTRL
    time.sleep(1)  # 需要延时
    win32gui.SendMessage(win, win32con.WM_KEYDOWN, 86, 0)  # V
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)  # 放开CTRL
    time.sleep(1)  # 缓冲时间
    win32gui.SendMessage(win, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)  # 回车发送
    return

def txt_ctrl_v(txt_str):
    #定义文本信息,将信息缓存入剪贴板
    clipboard.OpenClipboard()
    clipboard.EmptyClipboard()
    clipboard.SetClipboardData(win32con.CF_UNICODETEXT,txt_str)
    clipboard.CloseClipboard()
    return

def day_english():
    #获取金山词霸每日一句
    url = 'http://open.iciba.com/dsapi'
    r = requests.get(url)
    content = r.json()['content']
    note = r.json()['note']
    print(content+note)
    return  content+note

def dujitang():#毒鸡汤
    url = 'https://8zt.cc/'
    res = requests.get(url=url, headers=headers, timeout=10)
    selector = etree.HTML(res.text)
    # content = selector.xpath('//section/div/*/text()')[0]
    content = selector.xpath('//div[@class="main-wrapper"]//span[@id="sentence"]/text()')[0]
    #text = str(content)
    return content

#######################发送过程=================
#查找微信窗口，如果最小化则还原（需要固定位置）
title_name="张三"#需要单独打开张三的对话框，好友名称
win = win32gui.FindWindow('ChatWnd',title_name)
print("找到句柄：%x" % win)
if win!=0:
    left, top, right, bottom = win32gui.GetWindowRect(win)
    print(left, top, right, bottom)#最小化为负数
    print("nothe")
    #
    #最小化时点击还原，下面为单个窗口
    if top<0:
        #鼠标点击，还原窗口
        win32api.SetCursorPos([190, 1040])  # 鼠标定位到(190,1040)
        # 执行左单键击，若需要双击则延时几毫秒再点击一次即可
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        ######点击完成一次
    time.sleep(0.5)
    left, top, right, bottom = win32gui.GetWindowRect(win)#取数
    #
    #最小时点击还原窗口，下面一节为多个窗口，依次点击打开。
    k=1040#最小化后的纵坐标，横坐标约为190
    while top<0 and k>800:#并设定最多6次，防止死循环
        time.sleep(1)
        win32api.SetCursorPos([180, k-40])  # 鼠标定位菜单第一个
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        ######点击完成一次
        time.sleep(1)#等待窗口出现
        left, top, right, bottom = win32gui.GetWindowRect(win)#取数
        if top>0 :#判断是否还原
            break
        else:
            k-=40#菜单上移一格
            win32api.SetCursorPos([190, 1040])  # 重新打开菜单
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32gui.SetForegroundWindow(win)#获取控制
    time.sleep(0.5)
else:
    print('请注意：找不到【%s】这个人（或群），请激活窗口！'%title_name)
#
##开始发送图片
#pic_ctrl_c(r'C:\Users\Pictures\1.png')#第一张图片
#time.sleep(1)
#send_m()
#pic_ctrl_c(r'C:\Users\Pictures\2.png')#第二张图片
#time.sleep(1)
#send_m()
#pic_ctrl_c(r'C:\Users\Pictures\3.png')#第三张图片
#time.sleep(1)
#send_m()
#开始发送文本
# str=day_english()
# txt_ctrl_v(str)
# send_m()
str2=dujitang()
txt_ctrl_v(str2)
send_m()
str2=dujitang()
txt_ctrl_v(str2)
send_m()
#############################微信发送结束================

#############################其它备注====================
#
# #模拟键盘CTRL+V，方法二
# keyboard.press(Key.ctrl)
# keyboard.press('v')#大写不行列
# keyboard.release('v')
# keyboard.release(Key.ctrl)
#
##鼠标操作可忽略
# in_xy=[right-50,bottom-50]
# win32api.SetCursorPos(in_xy)
# mouse.press(Button.left)
# mouse.release(Button.left)
#
#from pynput.mouse import Button, Controller as mController
#from pynput.keyboard import Key, Controller as kController
#mouse = mController()
#keyboard = kController()
#print(type(keyboard))
# keyboard.type(str1) # 发送消息,需要pip install pynput
# time.sleep(1)#缓冲时间
#
# title_name='微信'#这个不分对象，瞎发。
# win = win32gui.FindWindow('WeChatMainWndForPC',title_name)