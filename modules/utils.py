import json, os, threading, time
from pandas import DataFrame
from selenium_chrome import Browser
stop_event = threading.Event()

def thread( proxy_url, playlist_url ):
    print(f'Proxy Url: {proxy_url}, Playlist URL: {playlist_url}')
    try:
        with open('.\profiles.json', 'r') as f:
                profiles = json.load(f)
                print(" * Opening browsers...")
                threads = []
                for data in profiles['credentials']:
                    threads.append( threading.Thread(target=run, kwargs={ 'username': data['username'], 'password': data['password'], 'playlist_url': playlist_url, 'proxy_url': proxy_url, 'stop_event':stop_event}, daemon=True ) )
                for thread in threads:
                    thread.start()
                    time.sleep(10)
                f.close()
    except:
        raise BaseException('No User Provided!')
        
def run(username, password, playlist_url, proxy_url, stop_event):
    stop_event.clear()
    try:
        with open(".\links.json", 'r') as f:
            links = json.load(f)

        if playlist_url == '' :
            playlist_url = links['playlist']

        if proxy_url == '' :
            proxy_url = links['proxy']
    except:
        raise BaseException('No URL Provided!')
    
    if stop_event.is_set():
        exit()
        

    browser = Browser(username, password, playlist_url, proxy_url)

    print(browser.url)
    browser.browser.get(url=browser.url)
    print('opened the browser!')
    browser.browser.back()
    time.sleep(2)
    browser.browser.forward()
    time.sleep(2)
 
    
    if stop_event.is_set():
        browser.browser.close()
        browser.browser.quit()
        
        
    if stop_event.is_set():
        browser.browser.close()
        browser.browser.quit()
        

    login = browser.login()

    if login:
        print('login successs!')
        browser.play()
    
    print('playing')
    try:
        while not stop_event.is_set():
            name, duration = browser.log()
            #with st.empty():
            #    st.text( f'{browser.username} is playing {name}')
            #duration = duration.split(':')
            #duration = abs( int(duration[0])*60 + int(duration[1]) + 10 )
            time.sleep(47)
    finally:
        print('closing browsers')
        browser.browser.close()
        browser.browser.quit()

def read_profiles():
    try:
        with open('.\profiles.json', 'r') as f:
            profiles = json.load(f)

    except:
        with open('.\profiles.json', 'w+') as f:
            profiles =  {"credentials": []}
            json.dump(profiles, f)
    
    return profiles

def add_user(username, password):
    #check the username
    username = username.strip()
    if username in ['', ' ', None] or password in ['', ' ', None]:
        raise ValueError

    #add_user to json file
    try:    
        f =  open('.\profiles.json', 'r')
        profiles = json.load(f)

        #check if pre-loaded users exists
        try:
            profiles['credentials'].append( {"username": username, "password": password} )
        except:
            profiles['credentials'] =[]
            profiles['credentials'].append( {"username": username, "password": password} )

        f.close()

    except:
        pass

    #write the updated file
    with open('.\profiles.json', 'w+') as f:
        json.dump(profiles, f)

def del_user(username_list:list):
    for username in username_list:
        try:
            log_file = f'.\log\{username}_log.json'
            os.remove(log_file)
        except:
            pass
        try:
            with open('.\profiles.json', 'r') as f:
                profiles = json.load(f)
            for i in range(len(profiles["credentials"])):
                if profiles["credentials"][i]['username'] == username:
                    del profiles["credentials"][i]
                    break
            
            with open('.\profiles.json', 'w+') as f:
                json.dump(profiles, f)

        except:
            pass

def set_defaults(playlist_url, proxy_url):

    try:
        with open('.\links.json', 'r') as f:
            data = json.load(f)
    
    except:
        data =  {"playlist": "", "proxy": "" }
    

    #add link to json file
    if playlist_url != "":
        #check if pre-loaded users exists
        data['playlist'] =  playlist_url
    if proxy_url != "":
        data['proxy'] = proxy_url

    #write the updated file
    with open('.\links.json', 'w+') as f:
        json.dump(data, f)

def delete_defaults(res_playlist_url, res_proxy_url):
    try:
        with open('.\links.json', 'r') as f:
            data = json.load(f)

        if res_playlist_url == True:
            data['playlist'] = ""
        
        if res_proxy_url == True:
            data['proxy'] = ""

    except:
        data =  {"playlist": "", "proxy": "" }

    with open('.\links.json', "w+") as f:
        json.dump(data, f)    

def read_logs():
    recent = {}
    try:
        for log in os.listdir('.\log'):
            
            if log[-4:] =='json':
                with open( f'.\log\{log}', 'r') as f:
                    data = json.load(f)
                    recent[log] = data
    except:
        return None

    return DataFrame( recent )

if __name__ == '__main__':
    pass    