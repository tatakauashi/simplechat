# 使用するChatGPTのモデル
CHATGPT_MODEL='gpt-3.5-turbo'

# 使用するシステムプロンプトファイル（拡張子 .md を除く）
SYSTEM_PROMPT = 'fumika'
# APIを実行する際にサーバーに渡す会話の履歴の数。冒頭のシステムプロンプトは常に付加するため、それ以外の直近の会話の数を指定する。
# 最新の会話は直近のユーザーの入力がそれにあたる。
ACTIVE_CHAT_HISTORY_LENGTH = 9

# VOICEVOX information
VOICEVOX_HOST = 'localhost'
VOICEVOX_PORT = 50021