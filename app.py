from flask import Flask, render_template, request, jsonify, redirect, url_for, abort

app = Flask(__name__)


@app.route('/')
def main():
    abort(404)
    return "404 Error"


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
