from collections import deque
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time


class UrlScraping:
    TOP_GAME_URL = 'https://store.steampowered.com/search/?sort_by=_ASC&filter=topsellers'

    def __init__(self, hide=False):
        options = webdriver.ChromeOptions()

        # 헤드리스 옵션 사용 여부
        if hide:
            options.add_argument("headless")

        # 창의 크기
        options.add_argument("--window-size=1920,1080")

        # 하드웨어 가속 사용 여부
        options.add_argument("disable-gpu")

        # 사용 언어
        options.add_argument("lang=ko_KR")

        # 드라이버 생성
        self.driver = webdriver.Chrome("../static/chromedriver.exe", options=options)

    def __del__(self):
        # 자신의 창만 종료
        self.driver.close()

    @property
    def top_game_url(self):
        # 게임 인기 순위 url
        url = self.TOP_GAME_URL

        try:
            # url 리스트
            url_deque = deque()
            # 드라이버 실행
            self.driver.get(url)
            # 맨 밑까지 스크롤
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            #  대기
            time.sleep(2)
            # html 추출
            html = self.driver.page_source
            # beautifulSoup 형태로 변경
            soup = BeautifulSoup(html, 'html.parser')
            # scraping 할 url 개수 가져오기
            for i in range(1, 6):
                game_url = soup.select_one(f"#search_resultsRows > a:nth-child({i})").get('href')
                url_deque.append(game_url)
            # url 개수만큼 루프
            while url_deque:
                print(url_deque.popleft())

        except Exception as ex:
            logging.error(ex)


if __name__ == "__main__":
    driver = UrlScraping()
    t1 = time.time()
    driver.top_game_url
    print(f"time : {time.time() - t1}")