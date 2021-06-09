from flask import Flask, render_template, request, jsonify, redirect, url_for, abort
from scraping.steam_data_scraping import SteamDataScraping
from database.database_controller import QueryController
import pymysql
import json
import time

with open('./database_property.json') as db_info:
    db = json.load(db_info)


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

conn = pymysql.connect(host=db['host'], port=db['port'], user=db['user'], password=db['password'], charset=db['charset'], db=db['db'])
cur = conn.cursor()


@app.route('/')
def main():
    abort(404)
    return "404 Error"


@app.route('/api/gameUrl/<url_key>')
def post_url(url_key):
    url = "https://store.steampowered.com/app/"+str(url_key)
    t1 = time.time()
    print(url)
    game_dict = SteamDataScraping().game_data_scraping(url)
    print(f"time: {time.time() - t1}")
    if game_dict["result"]:
        game_query = QueryController(game_dict).game_data_insert()
        tag_query = QueryController(game_dict).game_tags_insert()
        game_tags_query = QueryController(game_dict).game_tags_insert()

        print(game_query, tag_query, game_tags_query, sep="\n")
        return jsonify({'result': 'success', 'msg': f'success scraping {url}'})
    else:
        return jsonify({'result': 'fail', 'msg': '잘못된 url 입니다'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
