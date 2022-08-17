# -*- coding: utf-8 -*-

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver.v2 as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from config import google_login, google_password

import time
import random
import requests
import pickle
import os
import json
import datetime
import emoji
import sys
import keyboard as kb
import win32api as win


class Twitch:

    def __init__(self, google_login, google_password):
        self.google_username = google_login
        self.google_password = google_password
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--profile-directory=Default")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--disable-plugins-discovery")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("user_agent=DN")
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("--window-size=1032,720")
        chrome_options.add_argument("--window-position=0,0")
        # chrome_options.add_argument("--window-position=1940,-657")

        self.driver = uc.Chrome(
            executable_path=r"D:\Programs\Python\Twitch\chromedriver\chromedriver.exe",
            version_main=104,
            options=chrome_options
        )

    def close_driver(self):
        self.driver.close()
        self.driver.quit()

    def folders_create(self):

        if not os.path.exists(f"{os.getcwd()}\\Vids"):
            os.mkdir(f"{os.getcwd()}\\Vids")

        if not os.path.exists(f"{os.getcwd()}\\TXTs"):
            os.mkdir(f"{os.getcwd()}\\TXTs")

        if not os.path.exists(f"{os.getcwd()}\\cookies"):
            os.mkdir(f"{os.getcwd()}\\cookies")

        if not os.path.exists(f"{os.getcwd()}\\TXTs\\all.txt"):
            open(f"{os.getcwd()}\\TXTs\\all.txt", "w")

        if not os.path.exists(f"{os.getcwd()}\\TXTs\\names.txt"):
            open(f"{os.getcwd()}\\TXTs\\names.txt", "w")

        if not os.path.exists(f"{os.getcwd()}\\TXTs\\end_time.txt"):
            open(f"{os.getcwd()}\\TXTs\\end_time.txt", "w")

        if not os.path.exists(f"{os.getcwd()}\\TXTs\\logs.txt"):
            open(f"{os.getcwd()}\\TXTs\\logs.txt", "w")

    # определяет раскладку
    def get_name_layout(self):
        name = win.GetKeyboardLayoutName()
        if name == '00000409':
            return 'en'
        elif name == '00000419':
            return 'ru'

    # меняет раскладку
    def change_layout(self, set_lay, my_bot):
        current_lay = my_bot.get_name_layout()
        if current_lay == set_lay:
            pass
        else:
            print(f'[INFO] Layout changed')
            kb.press_and_release('shift + alt')

    def twitch_parse(self, twitch_link):

        driver = self.driver
        time.sleep(1)

        set_clip_urls = []

        try:
            entry = f'{twitch_link}/clips?filter=clips&range=24hr'
            driver.get(entry)
            time.sleep(5)

            hrefs = driver.find_elements_by_tag_name('a')

            clip_urls = [item.get_attribute('href') for item in hrefs if "/clip/" in item.get_attribute('href')]

            set_clip_urls = set(clip_urls)
            set_clip_urls = list(set_clip_urls)

        except:
            pass

        return set_clip_urls

    def views_count(self, link):
        driver = self.driver
        driver.get(link)
        time.sleep(random.randrange(4, 6))

        num_of_views = driver.find_element_by_xpath(
            # '/html/body/div[1]/div/div[2]/div/main/div[1]/div[3]/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div[1]/div[1]/div[2]/div/div/p[2]'
            '/html/body/div[1]/div/div[2]/div/main/div[1]/div[3]/div/div/div[1]/div[1]/div[2]/div/section/div/div/div[1]/div[1]/div[2]/div/div/p[2]'
        ).text.strip().split(' ')[0]

        name = driver.find_element_by_xpath(
            # '/html/body/div[1]/div/div[2]/div/main/div[1]/div[3]/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div[1]/div[1]/h2'
            '/html/body/div[1]/div/div[2]/div/main/div[1]/div[3]/div/div/div[1]/div[1]/div[2]/div/section/div/div/div[1]/div[1]/h2'
        ).get_attribute("title").strip()

        return num_of_views, link, name

    def ok(self, name):
        m = 0

        # фильтр по названию
        with open(f"{os.getcwd()}\\TXTs\\names.txt") as f:
            names = [row.strip() for row in f]
            for entry in names:
                if name == entry:
                    m = m + 1

        words = [
            "!", "\\", "/", ":", "*", "?", '"', "<", ">", "|",
            "ブ", "ラ", "チ", "シ", "ュ", "キ", "ン", "の", "攻", "撃", "ャ", "丫",
            "嗨", "，", "我", "很", "酷", "肉", "乙",
            "Название отсутствует", "IRL", "стрим", "Стрим", "КАТАЕМСЯ",
            "хуй", "пизд", "дцп", "хохол", "пид", "gay", "геи", "гей", "nig", "негр",
            "еба", "секс", "бляд", "блят"
        ]

        is_ok = True

        if m != 0:
            is_ok = False

        if not len(name) < 85:
            is_ok = False

        for i in words:
            if i.lower() in name.lower():
                is_ok = False

        if ":" in emoji.demojize(name):
            is_ok = False

        return is_ok

    def save_vids(self, link, amount, my_bot):
        driver = self.driver
        success = 0

        if len(os.listdir(os.getcwd() + r'\Vids')) < amount:
            try:
                driver.get(link)
                time.sleep(random.randrange(4, 6))

                author = link.split("/")[3]

                name = driver.find_element_by_xpath(
                    # '/html/body/div[1]/div/div[2]/div/main/div[1]/div[3]/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div[1]/div[1]/h2'
                    '/html/body/div[1]/div/div[2]/div/main/div[1]/div[3]/div/div/div[1]/div[1]/div[2]/div/section/div/div/div[1]/div[1]/h2'
                ).get_attribute("title").strip()

                with open(f'{os.getcwd()}\\TXTs\\all.txt', "a") as all_add:
                    all_add.write(f"{link}\n")
                all_add.close()

                is_ok = my_bot.ok(name=name)

                if is_ok:
                    vid_src = '/html/body/div[1]/div/div[2]/div/main/div[1]/div[3]/div/div/div[2]/div/div[2]/div/div[2]/video'
                    vid_src_url = driver.find_element_by_xpath(vid_src).get_attribute('src')

                    get_vid = requests.get(vid_src_url, stream=True)
                    with open(f"{os.getcwd()}\\Vids\\{name} _ @{author}.mp4", "wb") as video_file:
                        for chunk in get_vid.iter_content(chunk_size=576 * 1024):
                            if chunk:
                                video_file.write(chunk)

                    try:
                        with open(f"{os.getcwd()}\\TXTs\\names.txt", "a") as f:
                            f.write(f"{name}\n")
                        f.close()

                        success = 1
                    except:
                        try:
                            os.remove(f"{os.getcwd()}\\Vids\\{name} _ @{author}.mp4")
                        except:
                            pass
                    """ delete """
                    # success = 1
                else:
                    pass

            except:
                pass
        else:
            pass

        if success == 0:
            return_text = ""
        else:
            num_of_clips = len(os.listdir(f"{os.getcwd()}\\Vids\\"))
            return_text = f'[INFO] {num_of_clips}/{amount} downloaded'

        return return_text

    def google_login(self):

        driver = self.driver
        driver.get(
            r"https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground&prompt=consent&response_type=code&client_id=407408718192.apps.googleusercontent.com&scope=email&access_type=offline&flowName=GeneralOAuthFlow"
        )
        time.sleep(random.randrange(1, 3))
        driver.find_element_by_xpath(
            "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input"
        ).send_keys(str(google_login))
        driver.find_element_by_xpath(
            "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input").send_keys(
            Keys.RETURN)
        time.sleep(random.randrange(5, 10))
        password_input = driver.find_element_by_xpath(
            "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input")
        password_input.clear()
        password_input.send_keys(str(google_password), Keys.ENTER)

        time.sleep(random.randrange(5, 10))

        driver.get("https://www.youtube.com")
        time.sleep(random.randrange(5, 10))
        pickle.dump(driver.get_cookies(), open(f"{os.getcwd()}\\cookies\\{google_login}_cookies", "wb"))

        return "[INFO] Cookies updated successfully"

    def google_auth(self, timer=None, timer_value=None):

        while timer:
            today = datetime.datetime.today()
            date = today + datetime.timedelta(hours=0)
            if str(f"{date.strftime('%H.%M')}") == timer_value:  # 10.30
                break
            else:
                print(str(f"{date.strftime('%H.%M.%S')}"))
                time.sleep(58)

        driver = self.driver
        driver.delete_all_cookies()

        driver.get("https://www.youtube.com")

        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                           'Timed out waiting for PA creation ' +
                                           'confirmation popup to appear.')

            alert = driver.switch_to.alert
            alert.accept()
            driver.get("https://www.youtube.com")
        except TimeoutException:
            pass

        time.sleep(random.randrange(5, 10))
        for cookie in pickle.load(open(f"{os.getcwd()}\\cookies\\{google_login}_cookies", "rb")):
            driver.add_cookie(cookie)

        time.sleep(5)
        driver.refresh()
        time.sleep(10)

    def counter(self):
        files = []
        counter = 0
        list_of_files = os.listdir(os.getcwd() + r'\Vids')
        for item in list_of_files:
            if ".mp4" in item:
                try:
                    files.append(f"{os.getcwd()}\\Vids\\{item}")
                    counter += 1
                except:
                    pass
            else:
                os.remove(f"{os.getcwd()}\\Vids\\{item}")

        return files, counter

    def vid_upload(self, vid_path):

        driver = self.driver

        try:
            try:
                vid_path = vid_path.replace("\n", "")
            except:
                pass

            hashtag = vid_path.split("@")[-1]
            hashtag = hashtag.split(".mp4")[0]
            name = vid_path.split(" _ ")[0]

            description = r'Streamer - https://www.twitch.tv/' + hashtag

            name = name.split("\\")[-1] + ' @' + hashtag
            create_buttons = [
                    '/html/body/ytd-app/div[1]/div/ytd-masthead/div[3]/div[3]/div[2]/ytd-topbar-menu-button-renderer[1]/div/a/yt-icon-button/button/yt-icon', 
                    '/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[3]/div[2]/ytd-topbar-menu-button-renderer[1]/div/a/yt-icon-button/button', 
                    "/html/body/ytd-app/div[1]/div/ytd-masthead/div[3]/div[3]/div[2]/ytd-topbar-menu-button-renderer[1]",
                    '/html/body/ytd-app/div[1]/div/ytd-masthead/div[3]/div[3]/div[2]/ytd-topbar-menu-button-renderer[1]/dom-if',
                    '/html/body/ytd-app/div[1]/div/ytd-masthead/div[3]/div[3]/div[2]/ytd-topbar-menu-button-renderer[1]/div',
                    '/html/body/ytd-app/div[1]/div/ytd-masthead/div[3]/div[3]/div[2]/ytd-topbar-menu-button-renderer[1]/div/a',
                    '/html/body/ytd-app/div[1]/div/ytd-masthead/div[3]/div[3]/div[2]/ytd-topbar-menu-button-renderer[1]/div/a/yt-icon-button',
                    '/html/body/ytd-app/div[1]/div/ytd-masthead/div[3]/div[3]/div[2]/ytd-topbar-menu-button-renderer[1]/div/a/yt-icon-button/button',
                    '/html/body/ytd-app/div[1]/div/ytd-masthead/div[3]/div[3]/div[2]/ytd-topbar-menu-button-renderer[1]/div/a/yt-icon-button/button/yt-icon',
                    '/html/body/ytd-app/div[1]/div/ytd-masthead/div[3]/div[3]/div[2]/ytd-topbar-menu-button-renderer[1]/div/a/yt-icon-button/button/yt-icon/svg',
                    '/html/body/ytd-app/div[1]/div/ytd-masthead/div[3]/div[3]/div[2]/ytd-topbar-menu-button-renderer[1]/div/a/yt-icon-button/button/yt-icon/svg/g',
                    '/html/body/ytd-app/div[1]/div/ytd-masthead/div[3]/div[3]/div[2]/ytd-topbar-menu-button-renderer[1]/div/a/yt-icon-button/button/yt-icon/svg/g/path',
                    '/html/body/ytd-app/div[1]/div/ytd-masthead/div[3]/div[3]/div[2]/ytd-topbar-menu-button-renderer[1]/div/a/yt-icon-button/yt-interaction',
                    '/html/body/ytd-app/div[1]/div/ytd-masthead/div[3]/div[3]/div[2]/ytd-topbar-menu-button-renderer[1]/div/a/yt-icon-button/yt-interaction/div[1]',
                    '/html/body/ytd-app/div[1]/div/ytd-masthead/div[3]/div[3]/div[2]/ytd-topbar-menu-button-renderer[1]/div/a/yt-icon-button/yt-interaction/div[2]',
                    '/html/body/ytd-app/div[1]/div/ytd-masthead/div[3]/div[3]/div[2]/ytd-topbar-menu-button-renderer[1]/div/a/tp-yt-paper-tooltip',
                    ]
            
            add_video_buttons = [
                    '/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/div[3]/div[1]/yt-multi-page-menu-section-renderer/div[2]/ytd-compact-link-renderer[1]/a/tp-yt-paper-item/yt-formatted-string',
                    '/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/div[3]/div[1]/yt-multi-page-menu-section-renderer/div[2]/ytd-compact-link-renderer[1]',
                    '/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/div[3]/div[1]/yt-multi-page-menu-section-renderer/div[2]/ytd-compact-link-renderer[1]/a',
                    '/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/div[3]/div[1]/yt-multi-page-menu-section-renderer/div[2]/ytd-compact-link-renderer[1]/a/tp-yt-paper-item',
                    '/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/div[3]/div[1]/yt-multi-page-menu-section-renderer/div[2]/ytd-compact-link-renderer[1]/a/tp-yt-paper-item/div[1]',
                    '/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/div[3]/div[1]/yt-multi-page-menu-section-renderer/div[2]/ytd-compact-link-renderer[1]/a/tp-yt-paper-item/div[1]/yt-img-shadow',
                    '/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/div[3]/div[1]/yt-multi-page-menu-section-renderer/div[2]/ytd-compact-link-renderer[1]/a/tp-yt-paper-item/div[2]',
                    '/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/div[3]/div[1]/yt-multi-page-menu-section-renderer/div[2]/ytd-compact-link-renderer[1]/a/tp-yt-paper-item/div[2]/yt-formatted-string[1]',
                    '/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/div[3]/div[1]/yt-multi-page-menu-section-renderer/div[2]/ytd-compact-link-renderer[1]/a/tp-yt-paper-item/div[2]/yt-formatted-string[2]',
                    '/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/div[3]/div[1]/yt-multi-page-menu-section-renderer/div[2]/ytd-compact-link-renderer[1]/a/tp-yt-paper-item/yt-icon',
                    '/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/div[3]/div[1]/yt-multi-page-menu-section-renderer/div[2]/ytd-compact-link-renderer[1]/a/tp-yt-paper-item/yt-formatted-string'
                    ]

            try:
                # Создать
                for create_button in create_buttons:
                    try:
                        driver.find_element_by_xpath(
                            create_button).click()
                        break
                    except:
                        pass
                time.sleep(random.randrange(1, 2))

                # Добавить видео
                for add_video_button in add_video_buttons:
                    try:
                        driver.find_element_by_xpath(
                            add_video_button).click()
                        break
                    except:
                        pass
                time.sleep(3)
            except Exception as ex:
                return print(ex)

            time.sleep(5)
            elem = driver.find_element_by_xpath("//input[@type='file']")

            elem.send_keys(vid_path)

            # Name input

            time.sleep(random.randrange(5, 7))
            try:
                name_input = driver.find_element_by_xpath(
                    "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[1]/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input/div"
                )
            except:
                name_input = driver.find_element_by_xpath(
                        "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[1]/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-mention-input/div"
                )
            name_input.clear()
            name_input.send_keys(str(name))
            time.sleep(5)

            # description input

            try:
                description_input = driver.find_element_by_xpath(
                    "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[2]/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input/div"
                )
            except:
                description_input = driver.find_element_by_xpath(
                        "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[2]/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-mention-input/div"
                        )
            description_input.clear()
            description_input.send_keys(str(description))
            time.sleep(5)

            try:
                driver.find_element_by_xpath(
                    "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[1]/div/yt-formatted-string/span[1][contains(text(), 'За день можно загрузить ограниченное число видео. Ваш лимит исчерпан. Вы снова сможете добавлять ролики через 24 часа.')]"
                )
                limit = 1
            except NoSuchElementException:
                limit = 0

            if limit == 0:
                try:
                    driver.find_element_by_xpath(
                        "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[1]/div/yt-formatted-string/span[1][contains(text(), 'You can upload more videos in 24 hours.')]"
                    )
                    limit = 1
                except NoSuchElementException:
                    limit = 0

            if limit == 1:
                print('[INFO] Достигнут лимит')
                driver.find_element_by_xpath(
                    "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/div[1]/div/div/ytcp-icon-button"
                ).click()
                time.sleep(1)
                sys.exit()

            try:
                """ Нет, это видео не для детей """
                try:
                    driver.find_element_by_xpath(
                        "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[5]/ytkc-made-for-kids-select/div[4]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[2]"
                    ).click()
                except:
                    driver.find_element_by_xpath(
                            "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[5]/ytkc-made-for-kids-select/div[4]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[2]/div[2]/ytcp-ve"
                    ).click()
                time.sleep(1)

                # age restrictions
                """ Возрастные ограничения (дополнительно) """

                try:
                    try:
                        driver.find_element_by_xpath(
                            "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[5]/button/h3"
                        ).click()
                    except:
                        driver.find_element_by_xpath(
                                "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[5]/button/h3"
                        ).click()
                    time.sleep(2)
                    """ Видео подходит для зрителей младше 18 """

                    try:
                        driver.find_element_by_xpath(
                            "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[5]/ytcp-age-restriction-select/div/div[3]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[2]"
                        ).click()
                    except:
                        driver.find_element_by_xpath(
                            "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[5]/ytcp-age-restriction-select/div/div[3]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[2]/div[2]/ytcp-ve"
                        ).click()

                    time.sleep(1)
                except Exception as ex:
                    print(ex)

                # hashtags input
                """ Развернуть """

                driver.find_element_by_xpath(
                    "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/div/ytcp-button/div"
                ).click()
                time.sleep(1)

                try:
                    try:
                        tag_input = driver.find_element_by_xpath(
                            "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[3]/ytcp-form-input-container/div[1]/div/ytcp-free-text-chip-bar/ytcp-chip-bar/div/input"
                            )
                    except:
                        tag_input = driver.find_element_by_xpath(
                            "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[4]/ytcp-form-input-container/div[1]/div/ytcp-free-text-chip-bar/ytcp-chip-bar/div/input"
                            )
                    tag_input.clear()
                    tag_input.send_keys(
                        r"twitch,моменты с твича,твитч,топ клипы с твича,топ моменты твича,топ моменты,твич,twitch moments,топ моменты с твич,топ моменты с твича,клипы,топ твич,твичфм,irl,twitchfm,топ моменты с twitch,твич клипы,топ моменты твич,топ твича,irl стрим,twitch tv,топ моменты со стримов,twitch ru,лучшие моменты твича,стрим,лучшие моменты с twitch,топ клипы с twitch,приколы на стриме,top twitch fails,funny,funny twitch moments,twitch fails,livestreamfails,твичру")
                    time.sleep(random.randrange(2, 4))
                except Exception as ex:
                    print(ex)



            except Exception as ex:
                print(ex)

            time.sleep(random.randrange(45, 100))

            try:
                driver.find_element_by_xpath(
                    "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[1]/ytcp-video-upload-progress/span[contains(text(), 'Проверка завершена. Найдена жалоба на нарушение в видео авторских прав.')]")
                exist = 1
            except NoSuchElementException:
                exist = 0

            if exist == 0:
                try:
                    driver.find_element_by_xpath(
                        "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[1]/ytcp-video-upload-progress/span[contains(text(), 'Checks complete. Copyright claim found.')]"
                    )
                    exist = 1
                except NoSuchElementException:
                    exist = 0

            if exist == 0:

                driver.find_element_by_xpath(
                    "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[2]/div"
                ).click()
                time.sleep(2)
                driver.find_element_by_xpath(
                    "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[2]/div"
                ).click()
                time.sleep(2)
                driver.find_element_by_xpath(
                    "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[2]/div"
                ).click()
                time.sleep(2)
                driver.find_element_by_xpath(
                    "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[2]/div[1]/ytcp-video-visibility-select/div[1]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[3]/div[2]"
                ).click()
                time.sleep(2)
                driver.find_element_by_xpath(
                    "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[3]/div"
                ).click()
                time.sleep(3)

                os.remove(vid_path)

                try:
                    driver.find_element_by_xpath(
                        "/html/body/ytcp-video-share-dialog/ytcp-dialog/tp-yt-paper-dialog/div[1]/div/ytcp-icon-button"
                    ).click()
                    time.sleep(10)
                except Exception:
                    pass

                try:
                    WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                                   'Timed out waiting for PA creation ' +
                                                   'confirmation popup to appear.')

                    alert = driver.switch_to.alert
                    alert.accept()
                except TimeoutException:
                    pass



            else:
                print("[INFO] Авторские права")
                os.remove(vid_path)

                try:
                    driver.find_element_by_xpath(
                        "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/div[1]/div/div/ytcp-icon-button"
                    ).click()
                except Exception as ex:
                    print(ex)

                time.sleep(1)
                driver.get("https://www.youtube.com")
                time.sleep(2)

                try:
                    WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                                   'Timed out waiting for PA creation ' +
                                                   'confirmation popup to appear.')

                    alert = driver.switch_to.alert
                    alert.accept()
                except TimeoutException:
                    pass


        except Exception as ex:
            print(ex)

    def main(self, my_bot, write_logs, timer_value, need_to_sort, show_sorted, twitch_links, amount, min_views):

        # creates folders and empty files
        my_bot.folders_create()

        # logs
        if write_logs == 1:
            with open(f"{os.getcwd()}\\TXTs\\logs.txt", "a") as f:
                now = datetime.datetime.now()
                date = datetime.datetime.today()
                f.write(f'----------- {now} -----------\n{date.strftime("%H.%M")}  -  Script started\n')

        # deletes all previous clips
        list_of_files = os.listdir(os.getcwd() + r'\Vids')
        for item in list_of_files:
            os.remove(f"{os.getcwd()}\\Vids\\{item}")

        # adds time to files
        with open(os.getcwd() + r'\TXTs\all.txt', "a") as file:
            now = datetime.datetime.now()
            file.write(str(now) + '\n')
        file.close()

        with open(os.getcwd() + r'\TXTs\names.txt', "a") as file:
            now = datetime.datetime.now()
            file.write(str(now) + '\n')
        file.close()

        # prints time
        print(f'{datetime.datetime.now()}')

        # scrapping clips urls
        urls = []

        for twitch_link in twitch_links:
            clip_links = my_bot.twitch_parse(twitch_link)
            urls.append(clip_links)

        new_urls = []
        for item in urls:
            for i in item:
                new_urls.append(i)

        new_urls = set(new_urls)
        new_urls = list(new_urls)
        #
        delete_entries = []
        with open(f'{os.getcwd()}\\TXTs\\all.txt') as all:
            all_links = [row.strip() for row in all]
            all_links = set(all_links)
            all_links = list(all_links)
            for entry in new_urls:
                for text in all_links:
                    if text == entry:
                        delete_entries.append(entry)

        for link in delete_entries:
            try:
                new_urls.remove(link)
            except:
                print(f'не получилось удалить из списка {link}')
        #

        urls = new_urls

        print(f"[INFO] {len(urls)} urls were added")

        # logs
        if write_logs == 1:
            with open(f"{os.getcwd()}\\TXTs\\logs.txt", "a") as f:
                date = datetime.datetime.today()
                f.write(f'{date.strftime("%H.%M")}  -  Added {len(urls)} urls\n')

        # sort by views
        if need_to_sort == 1:
            # views count
            data = []
            for url in urls:
                try:
                    output = my_bot.views_count(link=url)
                    is_ok = my_bot.ok(name=output[2])
                    if is_ok:
                        if int(output[0]) >= min_views:
                            data.append(
                                {
                                    "link": output[1],
                                    "views": int(output[0]),
                                    "name": output[2]
                                }
                            )
                    else:
                        with open(f'{os.getcwd()}\\TXTs\\all.txt', "a") as all_add:
                            all_add.write(f"{url}\n")
                        all_add.close()
                except:
                    pass

            # sorts clips by views
            new_urls = []
            del_urls = data

            for i in range(1, len(del_urls) + 1):
                max_views = {
                    "link": "",
                    "views": 0,
                    "name": ""
                }
                max_index = 0
                for item in enumerate(del_urls):
                    if item[1]["views"] > max_views["views"]:
                        max_views = item[1]
                        max_index = int(item[0])

                new_urls.append(max_views)
                del_urls.pop(max_index)

            # shows sorted links to clips
            if show_sorted == 1:
                for item in new_urls:
                    print(f'{item["views"]} - {item["name"]}')

            # gets amount of videos with more than 600 views
            big_views_vids = [i for i in new_urls if i['views'] >= 600]
            if len(big_views_vids) > 1:
                amount = len(big_views_vids)
                print(f'Amount of videos changed to {amount}')

            # deletes the "views" values
            urls = [item["link"] for item in new_urls]

            print("[INFO] Clips were sorted by views")
            print(f'[INFO] Amount of links after sorting - {len(urls)}')

            # logs
            if write_logs == 1:
                with open(f"{os.getcwd()}\\TXTs\\logs.txt", "a") as f:
                    date = datetime.datetime.today()
                    f.write(f'{date.strftime("%H.%M")}  -  Clips were sorted by views\n')

        # download clips
        for url in urls:
            download = my_bot.save_vids(link=url, amount=amount, my_bot=my_bot)
            if not download == "":
                print(download)

        # logs
        if write_logs == 1:
            with open(f"{os.getcwd()}\\TXTs\\logs.txt", "a") as f:
                date = datetime.datetime.today()
                f.write(f'{date.strftime("%H.%M")}  -  Clips downloaded\n')

        """ gets needed layout """
        # my_bot.change_layout(my_bot=my_bot, set_lay='en')

        # updates youtube cookies
        cookie_file_path = f"{os.getcwd()}\\cookies\\{google_login}_cookies"
        if os.path.exists(cookie_file_path):
            today = datetime.datetime.ctime(datetime.datetime.today()).split(' ')
            today = [i for i in today if i != ""]
            today_month = str(today[1])
            today_day = int(today[2])
            last_change = str(time.ctime(os.path.getmtime(cookie_file_path))).strip().split(' ')
            last_change = [i for i in last_change if i != '']
            last_change_month = str(last_change[1])
            last_change_day = int(last_change[2])
            if last_change_day != today_day and last_change_month != today_month:
                if today_day == 1 or today_day == 15:
                    print(my_bot.google_login())

                    # logs
                    if write_logs == 1:
                        with open(f"{os.getcwd()}\\TXTs\\logs.txt", "a") as f:
                            date = datetime.datetime.today()
                            f.write(f'{date.strftime("%H.%M")}  -  Cookies updated\n')
        else:
            print(my_bot.google_login())

            # logs
            if write_logs == 1:
                with open(f"{os.getcwd()}\\TXTs\\logs.txt", "a") as f:
                    date = datetime.datetime.today()
                    f.write(f'{date.strftime("%H.%M")}  -  Cookies updated\n')

        # counts amount of clips
        output = my_bot.counter()
        paths = output[0]

        # logs
        if write_logs == 1:
            with open(f"{os.getcwd()}\\TXTs\\logs.txt", "a") as f:
                date = datetime.datetime.today()
                f.write(f'{date.strftime("%H.%M")}  -  Upload started\n')

        # set timer
        if timer_value is None:
            timer = False
        else:
            timer = True

        if need_to_sort != 1:
            """ gets needed layout """
            my_bot.change_layout(my_bot=my_bot, set_lay='en')

        # uploading clips
        first = 1
        for path in paths:

            output = my_bot.counter()
            counter = int(output[1])
            print(f"[INFO] Количество видео для загрузки - {counter}")

            """ auth in google """
            if first == 1:
                my_bot.google_auth(timer=timer, timer_value=timer_value)
            else:
                my_bot.google_auth(timer=False, timer_value=timer_value)

            my_bot.vid_upload(vid_path=path)
            first = 0

            try:
                os.remove(path)
            except:
                pass

        print(f'[INFO] Upload finished')
        print(f'[INFO] Ending time - {datetime.datetime.now().strftime("%H.%M")}')
        print("----------------")

        # end time writing
        with open(f"{os.getcwd()}\\TXTs\\end_time.txt", "a") as f:
            today = datetime.datetime.today()
            date = today + datetime.timedelta(hours=0)
            f.write(f"{str(date.strftime('%H.%M.%S'))}\n")

        # logs
        if write_logs == 1:
            with open(f"{os.getcwd()}\\TXTs\\logs.txt", "a") as f:
                date = datetime.datetime.today()
                f.write(f'{date.strftime("%H.%M")}  -  Upload finished\n')


if __name__ == '__main__':
    """ SETTINGS """

    # write logs  [ 1 - YES | 0 - NO ]
    write_logs = 1

    # set timer
    # timer_value = "10.00"
    timer_value = None

    # sort by views  [ 1 - YES | 0 - NO ]
    need_to_sort = 0

    # show sorted links if sorting is enabled  [ 1 - YES | 0 - NO ]
    show_sorted = 0

    # max amount of clips
    amount = 50

    # min amount of views
    min_views = 50

    # links to get clips
    twitch_links = [
        'https://www.twitch.tv/mibrozzz',
        'https://www.twitch.tv/bratishkinoff',
        'https://www.twitch.tv/razdva',
        'https://www.twitch.tv/mazellovvv',
        'https://www.twitch.tv/gwinglade',
        'https://www.twitch.tv/grpzdc',
        'https://www.twitch.tv/sindicsgo',
        'https://www.twitch.tv/lagoda1337',
        'https://www.twitch.tv/nelyaray',
        'https://www.twitch.tv/karandashaa',
        'https://www.twitch.tv/lomaka',
        'https://www.twitch.tv/pinkbutterflyman',
        'https://www.twitch.tv/muhanjan',
        'https://www.twitch.tv/batyaoffc',
        'https://www.twitch.tv/silazhik',
        'https://www.twitch.tv/t2x2',
        'https://www.twitch.tv/jesusavgn',
        'https://www.twitch.tv/drakeoffc',
        'https://www.twitch.tv/superstas2',
        'https://www.twitch.tv/stintik',
        'https://www.twitch.tv/dinik',
        "https://www.twitch.tv/baragozzers",
        "https://www.twitch.tv/jojohf",
        'https://www.twitch.tv/gaechkatm',
        'https://www.twitch.tv/stanislaw9',
    ]

    # init class
    my_bot = Twitch(google_login=google_login, google_password=google_password)

    # start uploading
    my_bot.main(my_bot=my_bot, write_logs=write_logs, timer_value=timer_value, need_to_sort=need_to_sort,
                show_sorted=show_sorted, twitch_links=twitch_links, amount=amount, min_views=min_views)
