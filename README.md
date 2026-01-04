# Naver Cafe Osint

<!--["main"](/images/main.png)-->

---

This project is a Python-based OSINT tool designed to retrieve information about Naver Cafe members.

It can identify a member's real **Naver ID** and **Nickname** by leveraging internal Naver APIs, specifically the one associated with the 'note' (private message) feature.

> [!WARNING]  
> This tool is intended for educational and research purposes only. The author assumes no liability and is not responsible for any misuse or damage caused by this program. **Use this tool responsibly and ethically.**

## Getting Started

### Requirements
- Python 3.8+
- A Naver account

### Installation
1. Clone the repository:
```
git clone https://github.com/simnple/Naver-Cafe-Osint.git
cd Naver-Cafe-Osint
```

2. Install the required Python packages:
```
pip install -r requirements.txt
```

3. Enter your Naver cookie in `.env`
```
COOKIE="YOUR_NAVER_COOKIE"
```

## Usage
To retrieve member information using a `member_key`:
```
$ py main.py --memberkey (member_key)
```

To retrieve member information from a cafe post (using `cafe_id` and `article_id`):
```
$ py main.py --article (cafe_id) (article_id)
```

For a detailed explanation of the arguments, use the help command:
```
$ py main.py --help
usage: main.py [-h] [--memberkey MEMBER_KEY]
               [--article CAFE_ID ARTICLE_ID]

Naver Cafe Osint tool

options:
  -h, --help            show this help message and exit
  --memberkey MEMBER_KEY
  --article CAFE_ID ARTICLE_ID
```

## Reference
- [네이버 카페 멤버 아이디 알아내기 — 다락방](https://simnple.tistory.com/18)

## License
This project is licensed under the [MIT License](https://github.com/simnple/Naver-Cafe-Osint/blob/main/LICENSE).
