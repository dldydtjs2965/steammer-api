from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

import time


class SteamDataScraping:

    def __init__(self, target_game_url, hide=False):
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

        self.target_game_url = target_game_url

        # 드라이버 생성
        self.driver = webdriver.Chrome("../static/chromedriver.exe", options=options)

    def __del__(self):
        # 자신의 창만 종료
        self.driver.close()

    # 성인게임 판정
    def is_adult_page(self):
        try:
            # 생년월일 탐지
            self.driver.find_element(By.CLASS_NAME, "agegate_birthday_selector")
            # year 콤보 박스 탐지
            select = Select(self.driver.find_element_by_id("ageYear"))
            # 1997년으로 변경
            select.select_by_visible_text("1997")
            # 확인 버튼 이벤트
            self.driver.execute_script("ViewProductPage()")

            time.sleep(1.5)
        except NoSuchElementException:
            pass



