import cv2
from HandTrackingModule import handDetector#cvzone.HandTrackingModule中handDetector有些地方用不了只能大致修改一个
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller,Key
#默认摄像头
cap=cv2.VideoCapture(0)
#设置窗口分辨率范围
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
cap.set(3, width+600)
cap.set(4, height+200)

detector = handDetector(detectionCon=0.8)#检测器 置信度0.8


keys = [["`~","1!","2@","3#","4$","5%","6^","7&","8*","9(","0)","BACK"],
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P","ENTER"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";:","'\"","Caps"],
        ["Z", "X", "C", "V", "B", "N", "M", ",<", ".>", "/?","Shift"],
        ["[{","]}","=+","-_","\|","TRUN"," "]]


finaltext=""

keyboard = Controller()
#实体框
# def drawall(img,buttonlist):
#
#     for button in buttonlist:
#         x, y = button.pos
#         w, h = button.size
#         cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)  # 紫色方框 要x+w 不能只用w
#         cv2.putText(img, button.text, (x + 20, y + 75), cv2.FONT_HERSHEY_PLAIN, 4,
#                     (255, 255, 255), 4)
#     return img

#使方框透明
def drawALL(img, buttonList):
    imgNew = np.zeros_like(img, np.uint8)
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        if button.text =="Caps"or button.text=="Shift"or button.text=="ENTER"or button.text=="BACK"or button.text=="TRUN":
            cvzone.cornerRect(imgNew, (x, y, w+65, h), 20, rt=0)
            cv2.rectangle(imgNew, button.pos, (x + w+65, y + h), (255, 0, 255), cv2.FILLED)
            cv2.putText(imgNew, button.text, (x + 20, y + 45), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 4)
        elif button.text==" ":
            cvzone.cornerRect(imgNew, (x, y, w + 150, h), 20, rt=0)
            cv2.rectangle(imgNew, button.pos, (x + w + 150, y + h), (255, 0, 255), cv2.FILLED)
            cv2.putText(imgNew, button.text, (x + 20, y + 45), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 4)
        else:
            cvzone.cornerRect(imgNew, (x, y, w , h ), 20, rt=0)
            cv2.rectangle(imgNew, button.pos, (x + w , y + h ), (255, 0, 255), cv2.FILLED)
            cv2.putText(imgNew, button.text, (x + 20, y + 45), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 4)
    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1-alpha, 0)[mask]
    return out


class Button():
    def __init__(self,pos,text,size=[80,80]):
        self.pos=pos
        self.text=text
        self.size=size


buttonlist=[]
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        if key==" ":
            buttonlist.append(Button([100 * j + 115, 100 * i + 50], key))
        else:
            buttonlist.append(Button([100* j + 50, 100 * i + 50], key))

caps=False
shift=False
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)#镜像翻转
    img = detector.findHands(img)  # 找到手
    lmlist, bboxInfo = detector.findPosition(img)  # 手的地址点
    img = drawALL(img, buttonlist)

    if lmlist:
        for button in buttonlist:
            x, y = button.pos
            w, h = button.size

            if x < lmlist[8][1] < x + w and y < lmlist[8][2] < y + h:
                if button.text == "Caps" or button.text == "Shift" or button.text == "ENTER" or button.text == "BACK" or button.text == "TRUN":
                    cv2.rectangle(img, (x - 5, y - 5), (x + w + 65, y + h + 5), (175, 0, 175), cv2.FILLED)  #绿方框 看是否点击
                    cv2.putText(img, button.text, (x + 10, y + 45), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 4)
                    l, _, _ = detector.findDistance(8, 12, img, draw=False)
                    print(l)
                elif button.text==" ":
                    cv2.rectangle(img, (x - 5, y - 5), (x + w + 150, y + h + 5), (175, 0, 175), cv2.FILLED)  # 绿方框 看是否点击
                    cv2.putText(img, button.text, (x + 10, y + 45), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 4)
                    l, _, _ = detector.findDistance(8, 12, img, draw=False)
                    print(l)
                else:
                    cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175),cv2.FILLED)
                    cv2.putText(img, button.text, (x + 10, y + 45), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 4)
                    l, _, _ = detector.findDistance(8, 12, img, draw=False)
                    print(l)
                # 点击时更新文本
                if l <30:
                    if button.text == "BACK":
                        finaltext = finaltext[:-1]
                        sleep(0.5)  #防止删的特别快
                        keyboard.press('\010')
                    elif button.text =="ENTER":
                        keyboard.press('\n')
                        sleep(0.5)
                        continue
                    elif button.text == "Caps":
                        caps = not caps  # 切换大小写状态
                        sleep(1)
                        continue
                    elif button.text == "Shift":
                        shift = not shift
                        sleep(0.5)
                        continue
                    elif button.text == "TURN":
                        keyboard.press(Key.shift_l)
                        sleep(0.5)  # 适当延时，确保按键被正确触发
                        keyboard.release(Key.shift_l)
                        sleep(0.5)
                        continue
                    else:
                        if caps:
                            button_text = button.text
                        else:
                            button_text = button.text.lower()
                        if len(button.text)>1 and shift== True:
                            keyboard.press(button_text[1])
                            finaltext += button_text[1]
                            sleep(0.4)  # 设0.4虽然有点卡 但是胜在不会出现一直打这个字的情况
                        else:
                            keyboard.press(button_text[0])
                            finaltext += button_text[0]
                            sleep(0.4)
                        if len(finaltext)*50>750:
                            finaltext = ""

    cv2.rectangle(img, (50, 650), (1000, 550), (175, 0, 175), cv2.FILLED)  #紫框 文字输出界面
    cv2.putText(img, finaltext, (60, 610), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv2.namedWindow("keyboard", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("keyboard", width+600, height+200)

    cv2.imshow("keyboard", img)
    cv2.waitKey(1)

