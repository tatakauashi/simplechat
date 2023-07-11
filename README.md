# simplechat
Simple Chat Web Application by Flask with ChatGPT API.

## How to setup & run 'simplechat'

### Python for Mac
```
use brew -> pyenv  
```
https://prog-8.com/docs/python-env

### Set up venv
```
python -m venv venv  
source ./venv/bin/activate  
pip install -r requirements.txt
```
*\*including install openai library.*

#### How to upgrade requirements.txt
```
pip freeze > requirements.txt  
```

### Preparing DB
```
sqlite3 instance/database.db  
BEGIN TRANSACTION;  
CREATE TABLE IF NOT EXISTS chat_history (seq INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, chat_id TEXT, role TEXT, content TEXT);  
COMMIT;  
```

### Voice Environment (Optional)
Install and Run VOICEVOX  
https://voicevox.hiroshiba.jp/  

### config.py settings
Edit flaskr/config.py

### How to run Flask
#### Prepare
##### Mac (Bash/zsh)
```
source ./venv/bin/activate  
export FLASK_APP=flaskr  
export FLASK_ENV=development  
```

##### Windows
```
.\venv\Scripts\activate.bat  
set FLASK_APP=flaskr  
set FLASK_ENV=development  
```

##### PowerShell (Windows)
```
.\venv\Scro@ts\Activate.ps1  
$env:FLASK_APP="flaskr"  
$env:FLASK_ENV="development"  
```

#### Set Open API Key
##### Mac (Bash/zsh)
```
export OPENAI_API_KEY="OpenAIのAPIキー"  
```

##### Windows
```
set OPENAI_API_KEY="OpenAIのAPIキー"  
```

##### PowerShell (Windows)
```
$env:OPENAI_API_KEY="OpenAIのAPIキー"  
```

#### Run
```
flask run  
```
or  
```
flask run --port=5505  
```
*\*On a Mac, it's likely that Flask's default port might be in use, so we recommend specifying a port.*　　

## Reference Links
【PythonでWebアプリ作成】Flask入門 ！この動画１本でWebアプリが作れちゃう！ 〜 Pythonプログラミング初心者用 〜  
https://www.youtube.com/watch?v=EQIAzH0HvzQ  

【話題の技術】ChatGPTのAPIをPythonから使う方法を解説！APIを使って議事録の要約プログラムを作ってみた！〜人工知能の進化が凄すぎる〜  
https://www.youtube.com/watch?v=kodz6fzbAUA  

【コピペでOK】CSSだけでLINE風の「吹き出し」を作る方法！  
https://stand-4u.com/css/fukidashi.html  

Free Icons | Font Awesome  
https://fontawesome.com/search?o=r&m=free&s=regular&f=classic  

WindowsでPIP Install するとSSLエラーになるのを解消する。  
https://qiita.com/kekosh/items/e96e822bf9cb6ca1aff8  

自然な会話できてすごい / JavaScriptで簡単に作れる  
https://www.youtube.com/watch?v=oOUBvdLKLK4  

ChatGPTとWhisperのAPIを使用して、AIと話せる会話アプリを作ってみた【Python初心者でも使えるコード付きで解説】  
https://www.youtube.com/watch?v=ECwfieE5hDU  
