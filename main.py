from colorama import init, Fore
from dotenv import load_dotenv
import requests
import argparse
import json
import sys
import os
import re

init(autoreset=True)

load_dotenv()

SEND_NOTE_URL_M = "https://m.note.naver.com/mobile/mobileSendNoteForm.nhn"
SEND_NOTE_URL = "https://note.naver.com/note/sendForm.nhn"

def get_naver_id(member_key):
    response = requests.get(SEND_NOTE_URL_M, params={"targetCafeMemberKey": member_key}, headers=headers)
    pattern = re.compile(r"onload\('([^']+)',\s*'([^']+)'\);")
    matches = pattern.findall(response.text)
    return matches[0][0]

def get_naver_nickname(member_key):
    response = requests.get(SEND_NOTE_URL, params={"targetCafeMemberKey": member_key}, headers=headers)
    pattern = re.compile(r'"targetNickname":\s*({.*?})')
    matches = pattern.findall(response.text)
    return json.loads(matches[0])[member_key]

def get_writer_info(cafe_id, article_id):
    response = requests.get(f"https://article.cafe.naver.com/gw/v4/cafes/{cafe_id}/articles/{article_id}", headers=headers)
    data = response.json()
    return {
        "member_key": data["result"]["article"]["writer"]["memberKey"],
        "nickname": data["result"]["article"]["writer"]["nick"]
    }

def get_comment_info(cafe_id, article_id):
    response = requests.get(f"https://article.cafe.naver.com/gw/cafes/{cafe_id}/articles/{article_id}/comments", headers=headers)
    data = response.json()
    result = {}

    result["writer"] = {
        "id": data["article"]["writer"]["id"],
        "nickname": data["article"]["writer"]["nick"]
    }
    result["comments"] = []

    ids = []
    for comment in data["comments"]["items"]:
        if comment["writer"]["id"] in ids: continue

        ids.append(comment["writer"]["id"])
        result["comments"].append({
            "id": comment["writer"]["id"],
            "nickname": comment["writer"]["nick"],
            "member_key": comment["writer"]["memberKey"]
        })
    
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Naver Cafe Osint tool")

    parser.add_argument("--memberkey", 
                        type=str,
                        metavar="MEMBER_KEY")

    parser.add_argument("--article", 
                        nargs=2,
                        type=str, 
                        metavar=("CAFE_ID", "ARTICLE_ID"))

    args = parser.parse_args()

    cookie = os.getenv("COOKIE")
    if not cookie:
        print(f"{Fore.RED}[-] .env 파일에 COOKIE 값이 설정되지 않았습니다.")
        sys.exit(1)
        
    headers = {
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    if args.memberkey:
        member_key = args.memberkey
        print(f"{Fore.GREEN}[{Fore.WHITE}*{Fore.GREEN}] Checking Member Key: {Fore.WHITE}{member_key}\n")
        
        try:
            naver_id = get_naver_id(member_key)
            naver_nickname = get_naver_nickname(member_key)
            
            print(f"{Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}] {Fore.GREEN}Email: {Fore.WHITE}{naver_id}@naver.com")
            print(f"{Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}] {Fore.GREEN}Nickname: {Fore.WHITE}{naver_nickname}")
            print(f"{Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}] {Fore.GREEN}Member Key: {Fore.WHITE}{member_key}")

        except Exception as e:
            print(f"{Fore.RED}[-] 멤버 키 조회 중 오류 발생: {e}")
            print(f"{Fore.YELLOW}   (Cookie가 만료되었거나 member_key가 잘못되었을 수 있습니다.)")

    elif args.article:
        cafe_id = args.cafe[0]
        article_id = args.cafe[1]
        print(f"{Fore.GREEN}[{Fore.WHITE}*{Fore.GREEN}] Checking Cafe Article: {Fore.WHITE}{cafe_id} / {article_id}\n")

        try:
            writer_info = get_writer_info(cafe_id, article_id)
            comment_info = get_comment_info(cafe_id, article_id)

            if writer_info and comment_info:
                print(f"{Fore.CYAN}--- Article Writer ---")
                print(f"{Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}] {Fore.GREEN}Email: {Fore.WHITE}{get_naver_id(writer_info["member_key"])}@naver.com")
                print(f"{Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}] {Fore.GREEN}Cafe Nickname: {Fore.WHITE}{writer_info["nickname"]}")
                print(f"{Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}] {Fore.GREEN}Nickname: {Fore.WHITE}{get_naver_nickname(writer_info["member_key"])}")
                print(f"{Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}] {Fore.GREEN}Member Key: {Fore.WHITE}{writer_info["member_key"]}")

                if comment_info["comments"]:
                    print(f"\n{Fore.CYAN}--- Comments ({len(comment_info["comments"])}) ---")
                    for i, comment in enumerate(comment_info["comments"]):
                        writer_message = ""
                        if writer_info["member_key"] == comment["member_key"]: writer_message = f" {Fore.YELLOW}(Writer){Fore.WHITE}"
                        print(f"  {Fore.WHITE}Comment {i+1}{writer_message}:")
                        print(f"    {Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}] {Fore.GREEN}Email: {Fore.WHITE}{comment["id"]}@naver.com")
                        print(f"    {Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}] {Fore.GREEN}Cafe Nickname: {Fore.WHITE}{comment["nickname"]}")
                        print(f"    {Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}] {Fore.GREEN}Nickname: {Fore.WHITE}{get_naver_nickname(comment["member_key"])}")
                        print(f"    {Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}] {Fore.GREEN}Member Key: {Fore.WHITE}{comment["member_key"]}\n")

        except Exception as e:
            print(f"{Fore.RED}[-] 게시글 정보 조회 중 오류 발생: {e}")
            print(f"{Fore.YELLOW}   (Cookie가 만료되었거나 cafe_id, article_id가 잘못되었을 수 있습니다.)")

    else:
        print(f"{Fore.RED}[-] 실행할 옵션을 입력해주세요.")
        parser.print_help()
        sys.exit(1)