from selenium import webdriver
from time import sleep
import pickle
import json
from pathlib import Path
import os
import dotenv
from selenium.webdriver.common.keys import Keys
import threading


dotenv_file = os.path.join(Path(__file__).resolve().parent, '.env')
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)
else:
    exit()


class InstagramInfo():
    DRIVER_PATH = 'tools/chromedriver'

    def __init__(self, headless=False):
        self.total_followers = 0
        self.total_followings = 0
        self.all_followers = set()
        self.all_followings = set()

        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.headless = headless
        self.driver = webdriver.Chrome(executable_path=self.DRIVER_PATH, options=self.chrome_options)

        with open('dataFile.json') as data_file:
            data = json.load(data_file)

        self.are_cookies_saved = data['initialized']

    def login(self, username, password):
        if self.are_cookies_saved:
            self.load_cookies()
            print('cookies loaded\n')
            return
        
        try:
            self.driver.get("https://www.instagram.com/")
            sleep(3)

            self.driver.find_element_by_xpath('//input[@name = \"username\"]').send_keys(username)
            self.driver.find_element_by_xpath('//input[@name = \"password\"]').send_keys(password)
            self.driver.find_element_by_xpath('//button[@type = \"submit\"]').click()
            sleep(5)

            self.save_cookies()

            jsonData = {'initialized': True}

            with open('dataFile.json', 'w') as f:
                json.dump(jsonData, f, indent=2)

        except Exception as e:
            print(e)
            exit()

    def save_cookies(self):
        pickle.dump(self.driver.get_cookies(), open("cookies.txt", "wb"))

    def load_cookies(self):
        try:
            cookies = pickle.load(open("cookies.txt", "rb"))
            self.driver.delete_all_cookies()

            # have to be on a page before you can add any cookies, any page - does not matter which
            self.driver.get("https://instagram.com")
            for cookie in cookies:

                # Checks if the instance expiry a float
                if isinstance(cookie.get('expiry'), float):

                    # It converts expiry cookie to a int
                    cookie['expiry'] = int(cookie['expiry'])
                self.driver.add_cookie(cookie)

        except:
            print(
                'heeeeeeeere'
            )
            print(
                'heeeeeeeere'
            )
            print(
                'heeeeeeeere'
            )
            print(
                'heeeeeeeere'
            )
            return False

    def scroll_to_bottom(self, target_class_name):
        before_scroll_window_height = -2 
        after_scroll_window_height = -1

        while before_scroll_window_height != after_scroll_window_height:
            before_scroll_window_height = self.driver.execute_script(f'return document.getElementsByClassName("{target_class_name}")[0].scrollHeight')
            self.driver.execute_script(f'''
            target_window = document.getElementsByClassName("{target_class_name}")[0];
            window_scroll_height = target_window.scrollHeight;
            target_window.scrollTo(0, window_scroll_height);
            ''')
            sleep(0.5)
            after_scroll_window_height = self.driver.execute_script(f'return document.getElementsByClassName("{target_class_name}")[0].scrollHeight')
    
    def followings(self):
        
        self.driver.get('https://www.instagram.com/piyu5hkumar/following/')
        sleep(5)
        
        self.scroll_to_bottom(target_class_name='_aano')

        divs = self.driver.find_elements_by_class_name('_ab8y._ab94._ab97._ab9f._ab9k._ab9p._abcm')

        for div in divs:
            name = div.get_attribute('innerHTML')
            self.all_followings.add(name)
        
        self.total_followings = len(self.all_followings)


    def followers(self):

        self.driver.get('https://www.instagram.com/piyu5hkumar/followers/')
        sleep(5)
        
        self.scroll_to_bottom(target_class_name='_aano')

        divs = self.driver.find_elements_by_class_name('_ab8y._ab94._ab97._ab9f._ab9k._ab9p._abcm')

        for div in divs:
            name = div.get_attribute('innerHTML')
            self.all_followers.add(name)

        self.total_followers = len(self.all_followers)
    
    def close(self):
        self.driver.close()


instagram_info_followings = InstagramInfo()
instagram_info_followings_thread_login = threading.Thread(target=instagram_info_followings.login, args=[os.environ.get('USER_NAME'), os.environ.get('PASSWORD')])
instagram_info_followings_thread_login.start()

instagram_info_followers = InstagramInfo()
instagram_info_followers_thread_login = threading.Thread(target=instagram_info_followers.login, args=[os.environ.get('USER_NAME'), os.environ.get('PASSWORD')])
instagram_info_followers_thread_login.start()

instagram_info_followings_thread_login.join()
followings_thread = threading.Thread(target=instagram_info_followings.followings)
followings_thread.start()

instagram_info_followers_thread_login.join()
followers_thread = threading.Thread(target=instagram_info_followers.followers)
followers_thread.start()

followings_thread.join()
followers_thread.join()

instagram_info_followings.close()
instagram_info_followers.close()

not_following_back = instagram_info_followings.all_followings - instagram_info_followers.all_followers

print('not following back - ')
for follow in not_following_back:
    print(follow)

print('\nI am not following back - ')
m_not_following_back =  instagram_info_followers.all_followers - instagram_info_followings.all_followings
for follow in m_not_following_back:
    print(follow)