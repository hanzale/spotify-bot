from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support.ui import WebDriverWait
import json, time, os
from modules.spotify import xpaths
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

class Browser():
    def __init__(self, user_name, password, url, proxy_url):
        self.browser = self.__set_browser__( proxy_url=proxy_url)
        self.wait = WebDriverWait(self.browser, 35)
        self.username = user_name       
        self.password = password
        self.url = url
        self.last_song=''
    
    def __set_browser__(self, proxy_url):

        options = Options()
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popups")
        options.add_argument("use-fake-ui-for-media-stream")
        options.add_experimental_option('excludeSwitches', ['enable-logging', "--block-new-web-content", "enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

       
        try:
            #if headless:
            #    options.add_argument('--headless')
            if proxy_url != None or proxy_url != "":
                
               #options.add_argument( f'--proxy-server={proxy_url}' )
                chrome_capabilities = webdriver.DesiredCapabilities().CHROME
                chrome_proxies = webdriver.Proxy()
                chrome_proxies.ssl_proxy = proxy_url
                chrome_proxies.add_to_capabilities(chrome_capabilities)

        except:
            pass
        
        browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options, desired_capabilities=chrome_capabilities)
        #browser = Chrome(executable_path='.\chromedriver\chromedriver' options=options)
        
        try:
            return browser
        except:
            raise [WebDriverException, ConnectionRefusedError, BaseException("Check Proxy!")]
    def login(self):
        
        # Login with given credentials
        try:
            login_button = self.wait.until( expected_conditions.element_to_be_clickable( (by.XPATH, xpaths['login_button']) ) )
            login_button.click()
            
            user_form = self.wait.until(expected_conditions.element_to_be_clickable((by.XPATH, xpaths["user_form"])))
            user_form.send_keys(self.username)
            pass_form = self.wait.until(expected_conditions.element_to_be_clickable((by.XPATH, xpaths["pass_form"])))
            pass_form.send_keys(self.password)
            submit_button = self.wait.until(expected_conditions.element_to_be_clickable((by.XPATH, xpaths["submit_button"])))
            submit_button.click()
            return True
        
        except:
            raise "Login Error! Check the Credentials or the Internet Connection"
        
    def play(self):
        #shuffle_button = wait.until(selEc.element_to_be_clickable((selBy.XPATH, xpaths["shuffle_button"])))
        
        time.sleep(1)
        try:
            cookie_check = self.wait.until(expected_conditions.element_to_be_clickable((by.XPATH, xpaths["cookie_check"])))
            cookie_check.click()
        except:
            pass

            
        repeat_button = self.wait.until(expected_conditions.element_to_be_clickable((by.XPATH, xpaths['repeat_button'])))
        
        # Start playing the list
        play_button = self.wait.until(expected_conditions.element_to_be_clickable((by.XPATH, xpaths["playlist_button"])))
        play_button.click()
        time.sleep(5)
        
        # Set repeat button to playlist repeat
        if repeat_button.get_attribute("aria-checked") == 'true':
            pass

        elif repeat_button.get_attribute("aria-checked") == 'mixed':
            time.sleep(0.7)
            repeat_button.click()
            time.sleep(2)
            repeat_button.click()
            
        elif repeat_button.get_attribute("aria-checked") == 'false':
            time.sleep(0.8)
            repeat_button.click()

        volume_button = self.wait.until(expected_conditions.element_to_be_clickable( (by.XPATH, xpaths['volume_button'])))
        if volume_button.get_attribute("aria-checked") != 'Volume off':
            volume_button.click()
            time.sleep(1.2)


        #self.browser.minimize_window()


    def write_to_file(self, username:str, song_name:str):
        try:
            with open(f'.\log\{username}_log.json', 'r') as f:
                logs = json.load(f)

            if song_name in logs.keys():
                logs[song_name] += 1
            else:
                logs[song_name] = 1
        except:
            logs = {}
            logs[f'{song_name}'] = 1
        
        with open(f'.\log\{username}_log.json', 'w+') as f:
            json.dump(logs, f)  

    def log(self) :
        
        song_name = self.wait.until(expected_conditions.presence_of_element_located((by.XPATH, xpaths["song_name"]))).text
        #time_track = self.wait.until(expected_conditions.presence_of_element_located((by.XPATH, xpaths["time_track"]))).text
        song_duration = self.wait.until(expected_conditions.presence_of_element_located((by.XPATH, xpaths["song_duration"]))).text

        if self.last_song != song_name:
            self.last_song = song_name
            
            self.write_to_file(username=self.username, song_name=song_name)
        
        elif self.last_song == '':
            self.write_to_file(username=self.username, song_name=song_name)
            self.last_song = song_name
        
        return song_name , song_duration
        
        
if __name__ == '__main__':
    pass