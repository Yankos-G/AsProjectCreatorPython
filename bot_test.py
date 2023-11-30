# import pyautogui as py
# import random
# import string
# import pyautogui as py #Import pyautogui
# import time #Import Time
# ############################################################################
# #BOT MA SZTYWNO WPISANE WARTOŚCI CZEKANIA - WOLNY KOMPUTER = BOT NIE DZIAŁA
# #mozna ewentualnie wykrywać na ekranie rzeczy
# ############################################################################
#
#
# def get_random_string(length):
#     letters = string.ascii_letters
#     result_str = ''.join(random.choice(letters) for i in range(length))
#     return result_str
#
#
# seen = 0
# clicked = 0
# str = get_random_string(2)
# project_name= 'project_bot' + str
# module_name = 'X20CP1584'
#
# while True:
#     py.sleep(1)
#     if not clicked:
#         try:
#             a = py.locateOnScreen('C:/Users/Szkolenie/Desktop/AS/AS.png')
#             print(a)
#             print('widze')
#             seen=1
#
#         except:
#             print('nie widze AS na pulpicie')
#     else:
#         pass
#
#     if seen:
#         py.doubleClick(a.left,a.top)
#         clicked=1
#         py.sleep(5)
#         py.hotkey('CTRL','SHIFT','N')
#         py.sleep(10)
#         py.write(project_name,0.01)
#         py.sleep(0.5)
#         py.hotkey('ENTER')
#         py.sleep(1)
#         py.hotkey('ENTER')
#         py.sleep(2)
#         py.write(module_name,0.01)
#         py.sleep(0.5)
#         py.hotkey('ENTER')
#         print('NEW PROJECT CREATED')
#         seen=0
#         clicked=0;
#         exit()

import pyautogui as py
import random
import string
import pyautogui as py #Import pyautogui
import time #Import Time
############################################################################
#BOT MA SZTYWNO WPISANE WARTOŚCI CZEKANIA - WOLNY KOMPUTER = BOT NIE DZIAŁA
#mozna ewentualnie wykrywać na ekranie rzeczy
############################################################################


def get_random_string(length):
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

str = get_random_string(2)
project_name= 'project_bot' + str
module_name = 'X20CP1584'

state = 'find_icon'

while True:
    match state:
        case 'find_icon':
            try:
                a = py.locateOnScreen('C:/Users/Szkolenie/Desktop/AS/AS.png')
                py.doubleClick(a.left, a.top)
                print('Icon located', a)
                state= 'is_open'
            except:
                print('Cannot find AS icon on desktop')
        case 'is_open':
            try:
                a = py.locateOnScreen('C:/Users/Szkolenie/Desktop/AS/is_open.png')
                print('Program is on',a)
                py.sleep(2)
                py.hotkey('CTRL', 'SHIFT', 'N')
                state = 'type_project_name'
            except:
                print('Waiting for program')
        case 'type_project_name':
            try:
                a = py.locateOnScreen('C:/Users/Szkolenie/Desktop/AS/wizard.png')
                print('Wizard is on',a)
                py.write(project_name, 0.01)
                py.sleep(0.05)
                py.hotkey('enter')
                state = 'choose_config'
            except:
                print('Waiting for wizard')
        case 'choose_config':
            try:
                a = py.locateOnScreen('C:/Users/Szkolenie/Desktop/AS/config.png')
                print('Config is on', a)
                py.sleep(0.05)
                py.hotkey('enter')
                state = 'choose_hardware'
            except:
                print('Waiting for config')
        case 'choose_hardware':
            try:
                a = py.locateOnScreen(r'C:/Users/Szkolenie/Desktop/AS/hardware1.png')
                print('Hardware is on', a)
                py.write(module_name, 0.01)
                py.sleep(0.5)
                py.hotkey('enter')
                state = 'end'
            except:
                print('Waiting for hardware')
        case 'end':
            print('New project created')
            exit()
        case _:
            print('NOT MATCHED STATE')
            exit()
