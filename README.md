# DreamStorm  [![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php)

Automated Website Analyzer and Intelligence Collection

目前支援功能 : 
1. 基本的爬蟲功能
2. CSRF 注入 detection
3. 檢查伺服器版本自動搜尋相關漏洞 ( 用 searchsploit )
4. tor 匿名連線
5. 分散式架構

## Version

now is on version 2.0

## Dependency

### BeautifulSoup ( https://www.crummy.com/software/BeautifulSoup/bs4/doc/ )

```
sudo apt-get install python-bs4
```

### Tor ( https://www.torproject.org/ )

```
sudo apt-get install tor
```

### searchsploit ( https://www.exploit-db.com/searchsploit/ )

Kali linux 有內建

## Usage

edit config.json and missions.json

config.json is the global setting

you can assign multiple missions in missions.json

```
./DreamStorm.py
```

and just run it...
