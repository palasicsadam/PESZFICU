from . import db


class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
    image = db.Column(db.Text, nullable=False)


class Person(db.Model):
    person_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text)
    image = db.relationship('Images')
    report = db.relationship('Report')


class Report(db.Model):
    report_id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
    camera = db.Column(db.Text, nullable=False)
    image = db.Column(db.DateTime, nullable=False)
