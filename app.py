from flask import Flask, render_template, request, jsonify, redirect, url_for, abort

from scraping.steam_data_scraping import SteamDataScraping

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def main():
    abort(404)
    return "404 Error"


@app.route('/api/gameUrl/<url_key>')
def post_url(url_key):
    url = "https://store.steampowered.com/app/"+str(url_key)
    print(url)
    game_dict = SteamDataScraping().game_data_scraping(url)
    if game_dict["result"]:
        return jsonify({'result': 'success', 'msg': f'success scraping {url}'})
    else:
        return jsonify({'result': 'fail', 'msg': '잘못된 url 입니다'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
