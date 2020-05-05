"""
A script for copying content from websites and pasting the content
into a text file.
"""

import webbrowser
import pyautogui
import pandas as pd
import time
import clipboard
import os

# Put game id numbers into list
filepath = 'game_ids.txt'
col_headers = []

with open(filepath) as fp:
   line = fp.readline()
   while line:
       col_headers.append(line.strip())
       line = fp.readline()

# Using chrome as default browser:
# loop through each url, load website,
# copy all content and paste into txt file,
# then close chrome.
# Mouse pointer must be pointing to a location on
# website where it doesn't click on link.
for x in range(len(col_headers)):
    webbrowser.open('http://www.kki.is/motamal/leikir-og-urslit/motayfirlit/Leikur?league_id=undefined&season_id=109345&game_id=4637' + str(col_headers[x]) + '#mbt:6-400$t&0=1')
    time.sleep(1)
    pyautogui.click(button='left')
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(1)
    s = clipboard.paste() 

    with open('game_data.txt','a', encoding='utf-8') as g:
        g.write(s)
    
    # kill chrome at the end of each loop
    # so we don't end up with hundreds of tabs
    # open
    os.system("taskkill /im chrome.exe /f")
