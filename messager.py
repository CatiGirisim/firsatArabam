"""
This module makes predictions from sklearn model.
23.01.2021
ÇatıGirişim
"""

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pyperclip
import time
from config import CHROME_PROFILE_PATH
import os
import shutil


def send_message(fle):
    filepath = fle
    newPath = fle.replace("dones", "sent")
    ilan_no = os.path.split(filepath)[-1].split(".")[0]
    # whatsapp mesajı gönderilmek üzere ilan linki oluşturuluyor
    ilan_link = "www.sahibinden.com/{}".format(ilan_no)
    options = webdriver.ChromeOptions()
    options.add_argument(CHROME_PROFILE_PATH)
    browser = webdriver.Chrome(executable_path="C:\\chromedriver\\chromedriver.exe", options=options)
    browser.maximize_window()
    browser.get('https://web.whatsapp.com/')
    with open('contacts.txt', 'r', encoding='utf8') as f:
        contact_list = [group.strip() for group in f.readlines()]

    msg = ilan_link
    # contacts.txt'de yer alan her kullanıcıya ilan linki gönderiliyor
    for contact in contact_list:
        search_xpath = '//div[@contenteditable="true"][@data-tab="3"]'

        search_box = WebDriverWait(browser, 500).until(
            EC.presence_of_element_located((By.XPATH, search_xpath))
        )
        search_box.clear()
        time.sleep(1)
        pyperclip.copy(contact)
        search_box.send_keys(Keys.SHIFT, Keys.INSERT)  # Keys.CONTROL + "v"
        time.sleep(2)

        group_xpath = f'//span[@title="{contact}"]'
        group_title = browser.find_element_by_xpath(group_xpath)
        group_title.click()
        time.sleep(1)

        try:
            input_xpath = '// *[ @ id = "main"] / footer / div[1] / div[2] / div / div[2]'
            input_box = browser.find_element_by_xpath(input_xpath)
            pyperclip.copy(msg)
            input_box.send_keys(Keys.SHIFT, Keys.INSERT)  # Keys.CONTROL + "v"
            input_box.send_keys(Keys.ENTER)
        except:
            print('Error sending sahibinden.com link !')

        time.sleep(2)
        try:
            attachment_box = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[1]/div[2]/div')
            attachment_box.click()
            # ilan linkinin ardından hazırlanan ilan fotoğrafı attachment olarak gönderiliyor
            image_box = browser.find_element_by_css_selector('#main > footer > div._3SvgF._1mHgA.copyable-area > div._3qpzV.rN1v9 > div.bDS3i > div > span > div > div > ul > li:nth-child(1) > button > input[type=file]')
            image_box.send_keys(filepath)
            time.sleep(2)
            send_btn = browser.find_element_by_css_selector('#app > div > div > div._3Bog7 > div.i5ly3._2l_Ww > span > div > span > div > div > div._1RHZR.b-lt8 > span > div > div > span')
            send_btn.click()
        except:
            print('Error sending attachment!')

        shutil.move(filepath, newPath)
        time.sleep(3)
        browser.close()


if __name__ == "__main__":
    send_message(r"C:\ilan_photos\dones\867309186.png")



