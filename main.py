from colorama import init, Fore
from dotenv import load_dotenv
import requests
import json
import sys
import os
import re

init(autoreset=True)

load_dotenv()

SEND_NOTE_URL_M = "https://m.note.naver.com/mobile/mobileSendNoteForm.nhn"
SEND_NOTE_URL = "https://note.naver.com/note/sendForm.nhn"

def get_naver_id(member_key):
    req = requests.get(SEND_NOTE_URL_M, params={"targetCafeMemberKey": member_key}, headers=headers)
    pattern = re.compile(r"onload\('([^']+)',\s*'([^']+)'\);")
    matches = pattern.findall(req.text)
    return matches[0][0]

def get_naver_nickname(member_key):
    req = requests.get(SEND_NOTE_URL, params={"targetCafeMemberKey": member_key}, headers=headers)
    pattern = re.compile(r'"targetNickname":\s*({.*?})')
    matches = pattern.findall(req.text)
    return json.loads(matches[0])[member_key]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"{Fore.RED}[!] Usage: python {sys.argv[0]} <member_key>")
        sys.exit(1)

    member_key = sys.argv[1]

    headers = {
        "Cookie": os.getenv("COOKIE")
    }

    print(f"{Fore.GREEN}[{Fore.WHITE}*{Fore.GREEN}] Checking Member Key: {Fore.WHITE}{member_key}\n")

    naver_id = get_naver_id(member_key)
    naver_nickname = get_naver_nickname(member_key)

    print(f"{Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}] {Fore.GREEN}Email: {Fore.WHITE}{naver_id}@naver.com")
    print(f"{Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}] {Fore.GREEN}Nickname: {Fore.WHITE}{naver_nickname}")