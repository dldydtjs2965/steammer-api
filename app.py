from flask import Flask, render_template, request, jsonify, redirect, url_for, abort

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def main():
    abort(404)
    return "404 Error"


@app.route('/api/gameUrl/<url>')
def post_url(url):
    scraping_result = True

    if scraping_result:
        return jsonify({'result': 'success', 'msg': f'success scraping {url}'})
    else:
        return jsonify({'result': 'fail', 'msg': '잘못된 url 입니다'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
