from selenium import webdriver


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

    def is_adult_page(self):
        self



