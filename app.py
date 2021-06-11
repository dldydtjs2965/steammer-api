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
    # mysql 커서
    cur = conn.cursor()
    # 중복 데이터 체크 쿼리
    q = QueryController.is_duplicate_data(url_key)
    # 중복 데이터 인지 체크
    if cur.execute(q) != 0:
        return jsonify({'result': 'fail', 'msg': '이미 존재하는 url 입니다.'})

    # 드라이버 생성
    driver = SteamDataScraping()
    # steam game url
    url = "https://store.steampowered.com/app/"+str(url_key)
    # steam game scraping data
    game_dict = driver.game_data_scraping(url)

    # data가 제대로 scraping 되었는지 확인.
    if game_dict["result"]:
        game_query = QueryController(game_dict).game_data_insert()
        tag_query = QueryController(game_dict).tag_data_insert()
        game_tags_query = QueryController(game_dict).game_tags_insert()

        try:
            # game_data query
            cur.execute(game_query)
            # tag_data query
            cur.execute(tag_query)
            # game_tags query
            cur.execute(game_tags_query)
            # commit
            conn.commit()
            # 커서 종료
            cur.close()
        except Exception as ex:
            print(ex)
            return jsonify({'result': 'Error', 'msg': 'data base Error'})

        return jsonify({'result': 'success', 'msg': f'success scraping {url}'})
    else:
        return jsonify({'result': 'fail', 'msg': '잘못된 url 입니다'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
