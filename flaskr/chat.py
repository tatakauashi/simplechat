from flask import render_template, request, redirect, url_for, jsonify
from . import app, db, voicevox
from .db import ChatHistory
import openai
import json, os

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    chat_id = data['chatId']
    content = data['content']
    audioOn = data['audioOn']
    speaker = data['speaker']
    if not is_positive_integer(speaker):
        speaker = "08"

    systemPrompt = ''
    audioFileName = 'c-' + chat_id + '-audio.wav'
    if os.path.exists('./flaskr/static/audios/' + audioFileName):
        os.remove('./flaskr/static/audios/' + audioFileName)
    else:
        print(f'@@@@@@@@@@ Can''t find file:{audioFileName}')

    # Check if chat_id exists
    if ChatHistory.query.filter_by(chat_id=chat_id).count() == 0:
        # Insert system message
        systemPrompt = readSystemPrompot(app.config['SYSTEM_PROMPT'])
#        system_message = ChatHistory(chat_id=chat_id, role='system', content='You are a helpful assistant.')
        system_message = ChatHistory(chat_id=chat_id, role='system', content=systemPrompt)
        db.session.add(system_message)
        
    # Insert user message
    user_message = ChatHistory(chat_id=chat_id, role='user', content=content)
    db.session.add(user_message)
    
    # Retrieve chat history
    chat_history = ChatHistory.query.filter_by(chat_id=chat_id).order_by(ChatHistory.seq.asc()).all()
    chat_history_list = [{'role': ch.role, 'content': ch.content} for ch in chat_history]

    print(chat_history_list)
    next_messages = []
    history_len = app.config['ACTIVE_CHAT_HISTORY_LENGTH']
    if len(chat_history_list) > (history_len + 1):
        next_messages.append(chat_history_list[0])
        next_messages = next_messages + chat_history_list[-history_len:]
    else:
        next_messages = chat_history_list

    print(f'@@@@@@@@@@ next_messages={next_messages}')

    result = False
    assistant_message_text = ''
    audio_path = None
    try:
        # Call GPT-3 API
        # openai.api_key = 'your-api-key'
        response = openai.ChatCompletion.create(
            model=app.config['CHATGPT_MODEL'],  # gpt-3.5-turbo
            messages=next_messages
        )

        # Insert assistant message
        assistant_message_text = response['choices'][0]['message']['content']
        assistant_message = ChatHistory(chat_id=chat_id, role='assistant', content=assistant_message_text)
        db.session.add(assistant_message)
        db.session.commit()

        print(f'@@@@@@@@@@ OpenAI API Response: {response}')

        # assistant_message_text をオーディオファイルに変換
        if audioOn and speaker != None and speaker != '':
            audio_abs_path = os.path.abspath('./flaskr/static/audios/' + audioFileName)
            voicevoxHost = app.config['VOICEVOX_HOST']
            voicevoxPort = app.config['VOICEVOX_PORT']
            voicevox.generate_wav(assistant_message_text, speaker=speaker, filepath=audio_abs_path, host=voicevoxHost, port=voicevoxPort)
            print(f'@@@@@@@@@@ audio_abs_path={audio_abs_path}')
            audio_path = '/static/audios/' + audioFileName

        result = True

    except Exception as e:
        print(e)
        assistant_message_text = 'ちょっと待ってね。'
        if audioOn and speaker != None and speaker != '':
            audio_path = f'/static/audios/0{speaker}_001_waitaminutes.wav'

    # Return assistant message
    return jsonify(result=result, role='assistant', content=assistant_message_text, audio_path=audio_path)

def readSystemPrompot(promptName):
    f = open(f'./prompts/{promptName}.md', 'r', encoding='UTF-8')
    data = f.read()
    f.close()

    data.replace('{%%%history_summary%%%}', 'None')
    return data

@app.route('/')
def index():
    return render_template(
        'chatgpt.html'
    )

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

import sqlite3
@app.route('/setup')
def setup():
    if True:
        DATABASE = "instance/database.db"
        con = sqlite3.connect(DATABASE)
        # con.execute("CREATE TABLE IF NOT EXISTS books (title, price, arrival_day)")
        # ChatGPT chat history
        con.execute("CREATE TABLE IF NOT EXISTS chat_history (seq INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, chat_id TEXT, role TEXT, content TEXT)")
    #    con.execute("ALTER TABLE chat_history ADD COLUMN response_json TEXT")
        con.close()
    return redirect(url_for('index'))

def is_positive_integer(s):
    return s.isdigit() and len(s) <= 6