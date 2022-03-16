from datetime import datetime
from . import db


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    #person = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
