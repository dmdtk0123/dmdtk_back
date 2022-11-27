import os
from flask import Flask, request, redirect, url_for
from flask import render_template, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='templates')
CORS(app)

@app.route('/upload',  methods={"POST"})
def upload_file():
    file = request.files.getlist("images")
    print(file)
    data = request.form['productDetail']
    return redirect(url_for('test_html', data=data))

@app.route('/test/{file}/{data}')
def test_html():
    return render_template('test.html')

@app.route('/')
def index_html(): # 루트에서는 index.html을 response로 보냄
    return render_template('index.html')

@app.errorhandler(404)
def not_found(e):  # SPA 이므로 404 에러는 index.html을 보냄으로써 해결한다.
    return index_html()

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run(debug = True)