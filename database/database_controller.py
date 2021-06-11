from collections import deque


class QueryController:
    def __init__(self, game_dict={}):
        self.game_dict = game_dict

    @staticmethod
    def is_duplicate_data(game_key):
        if game_key != "":
            query = f"SELECT GAME_ID FROM GAMES WHERE GAME_ID='{game_key}'"
            return query
        else:
            return ""

    def game_data_insert(self):
        game_dict = self.game_dict
        if len(game_dict) >= 10:
            # 특수문자 변경
            game_dict['description'] = game_dict['description'].replace("\'", "\"")
            game_dict['game_name'] = game_dict['game_name'].replace("\'", "\"")
            # GAMES insert 문
            insert_sql = f"INSERT IGNORE INTO GAMES (GAME_ID, GAME_NAME, GAME_INFO, LAUNCH_DATE, EVALUATION, IMG_URL, VIDEO_URL, DEV_COMPANY, DISTRIBUTOR) VALUES ('{game_dict['game_id']}','{game_dict['game_name']}', '{game_dict['description']}', '{game_dict['launch_date']}', '{game_dict['evaluation']}', '{game_dict['img_url']}', '{game_dict['video_url']}', '{game_dict['company']}', '{game_dict['distributor']}');"
            return insert_sql
        else:
            print("딕셔너리 크기가 잘못 입력 되었습니다")
            return ""

    def tag_data_insert(self):
        game_dict = self.game_dict

        # TAGS insert 문
        tag_query = "INSERT IGNORE INTO TAGS (TAG_ID, TAG_NAME) VALUES "

        # TAGS insert VALUES 추가
        if len(game_dict) >= 10:
            tags = deque(game_dict['tags'])
            # tags 크기만큼 loop
            while True:
                # 마지막 데이터는 쿼리문을 닫는다.
                if len(tags) > 1:
                    tag = tags.popleft()
                    tag_query = tag_query + f"('{tag[0]}', '{tag[1]}'), "
                else:
                    tag = tags.popleft()
                    tag_query = tag_query + f"('{tag[0]}', '{tag[1]}');"
                    break

            # TAGS insert 문 return
            return tag_query
        else:
            print("딕셔너리 크기가 잘못 입력 되었습니다")
            return ""

    def game_tags_insert(self):
        game_dict = self.game_dict

        # GAME_TAGS 쿼리
        game_tag_query = "INSERT IGNORE INTO GAME_TAGS (GAME_TAGS_KEY, GAME_ID, TAG_ID) VALUES "

        # TAGS insert VALUES 추가
        if len(game_dict) >= 10:
            tags = deque(game_dict['tags'])

            while True:
                if len(tags) > 1:
                    tag = tags.popleft()
                    game_tag_query = game_tag_query + f"('{game_dict['game_id']+tag[0]}', '{game_dict['game_id']}', '{tag[0]}'), "
                else:
                    game_tag_query = game_tag_query + f"('{game_dict['game_id']+tag[0]}','{game_dict['game_id']}', '{tag[0]}');"
                    break

            return game_tag_query
        else:
            print("딕셔너리 크기가 잘못 입력 되었습니다")
            return ""
