from flask import Flask, render_template, request, jsonify, redirect, url_for, abort
from scraping.steam_data_scraping import SteamDataScraping
from database.database_controller import QueryController
import pymysql
import json

with open('./database_property.json') as db_info:
    db = json.load(db_info)


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

conn = pymysql.connect(host=db['host'], port=db['port'], user=db['user'], password=db['password'], charset=db['charset'], db=db['db'])

@app.route('/')
def main():
    abort(404)
    return "404 Error"


@app.route('/api/gameUrl/<url_key>')
def post_url(url_key):
    # 드라이버 생성
    driver = SteamDataScraping()
    # mysql 커서
    cur = conn.cursor()
    # 중복 데이터 체크 쿼리
    q = QueryController.is_duplicate_data(url_key)
    # 중복 데이터 인지 체크
    if cur.execute(q) != 0:
        return jsonify({'result': 'fail', 'msg': '이미 존재하는 url 입니다.'})
    # steam game url
    url = "https://store.steampowered.com/app/"+str(url_key)

    try:
        # steam game scraping data
        game_dict = driver.game_data_scraping(url)
        query = QueryController(game_dict)
        # GAMES insert
        game_insert = query.game_data_insert()
        cur.execute(game_insert)
        # TAGS insert
        tag_insert = query.tag_data_insert()
        cur.execute(tag_insert)
        # GAME_TAGS insert
        game_tag_insert = query.tag_data_insert()
        cur.execute(game_tag_insert)

        conn.commit()

        # data가 제대로 scraping 되었는지 확인.
        if game_dict["result"]:
            return jsonify({'result': 'success', 'msg': 'success'})
        else:
            return jsonify({'result': 'fail', 'msg': game_dict["msg"]})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'result': 'fail', 'msg': f"Error: {e}"})
    finally:
        # 커서 종료
        cur.close()


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
