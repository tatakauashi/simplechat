from . import db

class ChatHistory(db.Model):
    __tablename__ = 'chat_history'

    seq = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chat_id = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
