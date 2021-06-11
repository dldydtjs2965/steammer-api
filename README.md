# steammer-api

## 목표

aaaaaaaaaaaawssteammer-webservice와 연계되어 작동하는 api 전용 서버로
steam 웹페이지에 있는 game data를 크롤링 및 스크래핑 하기 위한 falsk 서버.


## features

- game key를 받아서 scraping된 데이터를 data를 DB에 저장.
- 일정 시간이 되면 지정된 Top Seller game들을 crawling 후 DB에 저장


## example

- game key
 https://store.steampowered.com/app/` 1384160 `/game_name/
 
- data scraping
` http://serverIP:5000/api/gameUrl/"gameKey" `
