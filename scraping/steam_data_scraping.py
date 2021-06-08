from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import re


class SteamDataScraping:

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
        self.driver = webdriver.Chrome("D:\\steammer-api\\static\\chromedriver.exe", options=options)

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

    def is_package_page(self):
        # 패키지 게임 확인
        try:
            self.driver.find_element(By.XPATH, "/html/body/div[1]/div[7]/div[4]/div[1]/div[2]/div/div[2]/div[4]").click()
        except NoSuchElementException:
            pass

    def game_id_scraping(self):
        # 링크에서 game_id 추출
        steam_link = self.driver.current_url
        steam_link = steam_link.replace("https://store.steampowered.com/app/", "")
        game_list = steam_link.split("/")
        game_id = game_list[0]

        return game_id

    def game_data_scraping(self, target_game_url):
        try:
            self.driver.get(target_game_url)

            # 한국어 선택
            self.driver.find_element(By.ID, "language_pulldown").click()
            self.driver.find_element(By.XPATH, '//*[@id="language_dropdown"]/div/a[4]').click()
            time.sleep(1.5)

            # 성인 게임 판정
            self.is_adult_page()

            # 패키지 게임 판정
            self.is_package_page

            # 태그 클릭
            self.driver.find_element(By.CLASS_NAME, 'add_button').click()

            # 태그 div 대기
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                'body > div.responsive_page_frame.with_header > div.responsive_page_content > div.responsive_page_template_content > div.game_page_background.game > div.page_content_ctn > div.page_title_area.game_title_area.page_content > div.apphub_HomeHeaderContent > div > div.apphub_AppName'))
            )

            # html 추출
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # 해당게임 링크
            game_id = self.game_id_scraping()

            # 게임 정보
            if soup.find("div", class_="game_description_snippet") is None:
                game_description = ""
            else:
                game_description = soup.find("div", class_="game_description_snippet").get_text()
            game_description = game_description.strip()

            # 비디오 url
            video_url = soup.find("video", class_="highlight_player_item highlight_movie").get("src")

            # 이미지 url
            img_url = soup.find("img", class_="game_header_image_full").get("src")

            # 게임 평가
            if soup.select_one(
                    "#game_highlights > div.rightcol > div > div.glance_ctn_responsive_left > div > div.user_reviews_summary_row > div.summary.column > span.game_review_summary") is not None:
                evaluation = soup.select_one(
                    "#game_highlights > div.rightcol > div > div.glance_ctn_responsive_left > div > div.user_reviews_summary_row > div.summary.column > span.game_review_summary").get_text()
            else:
                evaluation = "사용자 평가 없음"

            # 출시일
            launch_date = soup.find("div", class_="date").get_text()
            launch_date = re.compile('[|가-힣]+').sub("", launch_date)
            launch_date = launch_date.replace(" ", "-")

            # 개발사
            company = soup.select_one("#developers_list > a").get_text()

            # 배급사
            distributor = soup.select_one("div.summary.column > a").get_text()

            tag_info = []
            # 태그정보 append
            for tag in soup.find_all(class_="app_tag_control popular"):
                if tag is not None:
                    tag_info.append([tag.get('data-tagid'), tag.find("a").get_text()])

            return {"result": True, "game_id": game_id, "description": game_description, "video_url": video_url, "img_url": img_url, "evaluation": evaluation, "launch_date": launch_date, "company": company, "distributor": distributor, "tags": tag_info}
        except Exception as ex:
            print("잘못된 url 입니다.", ex)
            return {"result": False}







