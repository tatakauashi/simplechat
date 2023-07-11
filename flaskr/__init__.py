from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

# ルーティングをインポート
from . import chat

# 生成してあったwavファイルを削除する
import glob, os
for filename in  glob.glob('./flaskr/static/audios/c-*.wav'):
    os.remove(filename)