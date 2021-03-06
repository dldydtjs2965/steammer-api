from collections import deque
from threading import Thread
from pyvirtualdisplay import Display
from selenium import webdriver
from bs4 import BeautifulSoup
from queue import Queue

import logging
import time


class UrlScraping:
    TOP_GAME_URL = 'https://store.steampowered.com/search/?sort_by=_ASC&filter=topsellers'

    def __init__(self, url_count, hide=False):
        options = webdriver.ChromeOptions()

        # 헤드리스 옵션 사용 여부
        if hide:
            options.add_argument("headless")

        # 가상 웹브라우저 설정
        display = Display(visible=0, size=(1024, 768))

        # 가상 웹브라우저 실행
        display.start()

        # 하드웨어 가속 사용 여부
        options.add_argument("disable-gpu")

        # 사용 언어
        options.add_argument("lang=ko_KR")

        # # 드라이버 생성
        # self.driver = webdriver.Chrome("D:\\steammer-api\\static\\chromedriver.exe", options=options)

        # 드라이버 생성
        self.driver = webdriver.Chrome("/home/ubuntu/steammer-api/static/chromedriver", options=options)

        self.url_count = url_count

        # url 리스트
        self.url_queue = Queue()

    def __del__(self):
        # 자신의 창만 종료
        self.driver.close()

    def url_scraping(self, soup, index):
        try:
            game_url = soup.select_one(f"#search_resultsRows > a:nth-child({index})").get('href')
            self.url_queue.put(game_url)
        except Exception as ex:
            print(ex)
            return "scraping error"

    @property
    def top_game_url(self):
        # 게임 인기 순위 url
        url = self.TOP_GAME_URL

        try:
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

            t_list = deque()

            # scraping 할 url 개수 가져오기
            for i in range(1, self.url_count + 1):
                t = Thread(target=self.url_scraping, args=(soup, i))
                t_list.append(t)

            [t.start() for t in t_list]

            [t.join() for t in t_list]

            return self.url_queue

        except Exception as ex:
            logging.error(ex)
