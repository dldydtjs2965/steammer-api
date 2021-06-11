# steammer-api


## 목표

steammer-webservice와 연계되어 작동하는 api 서버로

steam 웹페이지에 있는 game data를 크롤링 및 스크래핑 하기 위한 falsk 서버.


## features


- game key를 받아서 scraping된 데이터를 data를 DB에 저장.
- 일정 시간이 되면 지정된 Top Seller game들을 crawling 후 DB에 저장


## example


- ### game key 


  ***기존 스팀 웹 url*** : ` https://store.steampowered.com/app/"gamekey"/game_name/ `
 

- ### data scraping 


    http://serverIP:5000/api/gameUrl/"gameKey" 
  

- ### database setting
```json
   {
    "host": "server ip",
    "port": "port number(int)",
    "user": "user id",
    "password": "user password",
    "charset" : "utf8",
    "db": "using schema"
   }
```


## 일정


- 2021-06-04 : Top Seller game url scraping
  

- 2021-06-08 : Steam game data scraping


- 2021-06-09 : data base query module 제작


- 2021-06-11 : steam web scraping api 제작 완료.
