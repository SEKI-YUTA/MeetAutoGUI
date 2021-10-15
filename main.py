import PySimpleGUI as sg
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time
import re
import sys
import os
import functions

webclassId = ""
webclassPass = ""
googleId = ""
googlePass = ""
sandaiDomain = "@ge.osaka-sandai.ac.jp"
configFileExists = functions.configFileExists()
options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#これがエラーをなくすコードです。ブラウザ制御コメントを非表示化しています
options.use_chromium = True
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--start-maximized')
options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 1,
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 0,
    "profile.default_content_setting_values.notifications": 1
})

def meetAutomation():
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.dirname(__file__)
        return os.path.join(base_path, relative_path)
    browser = webdriver.Chrome(executable_path=resource_path('./chromedriver'),options=options)
    
    browser.delete_all_cookies()
    def luhchChrome():
        browser.get('https://j29-plw.osaka-sandai.ac.jp/cas/login?service=https%3A%2F%2Fed24lb.osaka-sandai.ac.jp%2Fwebclass%2Flogin.php%3Fauth_mode%3DCAS')
        time.sleep(1)

    def webClass():
        userIdBox = browser.find_element_by_css_selector("input[name='username']")
        userPassBox = browser.find_element_by_css_selector("input[name='password']")
        loginBtn = browser.find_element_by_css_selector("input[name='submit']")
        userIdBox.send_keys(webclassId)
        userPassBox.send_keys(webclassPass)
        time.sleep(1)
        loginBtn.click()
        time.sleep(1)
        courcesContainer = browser.find_element_by_css_selector('ul.courseTree.courseLevelOne > li:last-child')
        cources = courcesContainer.find_elements_by_class_name("course-title")
        syogakusoron = cources[0].find_element_by_tag_name('a')
        syogakusoron.click()
        time.sleep(1)
        timeLineItem = browser.find_element_by_css_selector('.cl-contentsList_contentInfo');
        joinPageLink = timeLineItem.find_element_by_tag_name('a')
        joinPageLink.click()
        time.sleep(1)
        browser.get('https://meet.google.com/rax-ozng-ndo')
        time.sleep(3)

    def googleLogin():
        send_command = ('POST', '/session/$sessionId/chromium/send_command')
        browser.command_executor._commands['SEND_COMMAND'] = send_command
        browser.execute('SEND_COMMAND', dict(cmd='Network.clearBrowserCache', params={}))
        emailInput = browser.find_element_by_css_selector("input[type='email']")
        emailSubmit = browser.find_element_by_css_selector("button.VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.qIypjc.TrZEUc.lw1w4b")
        emailInput.send_keys(googleId + sandaiDomain)
        emailSubmit.click()
        time.sleep(3)
        passwordInput = browser.find_element_by_css_selector("input[type='password']")
        passwordSubmit = browser.find_element_by_css_selector("button.VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.qIypjc.TrZEUc.lw1w4b")
        passwordInput.send_keys(googlePass)
        passwordSubmit.click()
        time.sleep(5)

    def turnOffMicCam():
        time.sleep(1)
        mikeToggle = browser.find_element_by_css_selector('.U26fgb.JRY2Pb.mUbCce.kpROve.yBiuPb.y1zVCf.HNeRed.M9Bg4d').click()
        browser.implicitly_wait(3000)
        videoToggle = browser.find_element_by_css_selector('.U26fgb.JRY2Pb.mUbCce.kpROve.yBiuPb.y1zVCf.HNeRed.M9Bg4d').click()
        browser.implicitly_wait(3000)

    def joinMeet():
        joinButton = browser.find_element_by_css_selector('span.l4V7wb.Fxmcue').click()
        browser.implicitly_wait(3000)
        print('joinMeet')
        print(joinButton)
    print('\n')
    luhchChrome()
    print('finished lunchChrome')
    webClass()
    print('finished webClass')
    googleLogin()
    print('finished googleLogin')
    turnOffMicCam()
    print('finished turnOffMicCam')
    joinMeet()
    print('finished joinMeet')


layout = [
    
]
if configFileExists:
    layout = [
        [sg.Text('設定ファイルがあります')],
        [sg.Button('settings'),sg.Button('Open Chrome')]
    ]
    configs = functions.readConfigFile()
    googleId = configs[0].replace('\n','')
    googlePass = configs[1].replace('\n','')
    webclassId = configs[2].replace('\n','')
    webclassPass = configs[3].replace('\n','')
else:
    layout = [
        [sg.Text('設定画面')],
        [sg.Text('gooleEmail'),sg.In(key='googleEmail')],
        [sg.Text('goolePass'),sg.In(key='googlePass')],
        [sg.Text('webclassId'),sg.In(key='webclassId')],
        [sg.Text('webclassPass'),sg.In(key='webclassPass')],
    ]

window = sg.Window('授業さぼろー',layout)

while True:
    event, values = window.read()
    # print('event=',event,'values=', values)
    # print('入力値=',values['-IN-'])
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event=='Clear':
        window['-OUTPUT-'].update('')
    if event=='Go':
        window['-OUTPUT-'].update(values['-IN-'])
    if event == "Open Chrome":
        print("Open Chrome")
        meetAutomation()
        


window.close()