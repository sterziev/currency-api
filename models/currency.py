from app import db


class Currency(db.Model):
    __tablename__ = 'currency'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    rate = db.Column(db.Float())
    date = db.Column(db.Date())

    def __init__(self, name, rate, date):
        self.name = name
        self.rate = rate
        self.date = date

    def __repr__(self):
        return '{' + 'id:{}, name:{}, rate:{}, date:{}'.format(self.id, self.name, self.rate, self.date) + '}'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'rate': self.rate,
            'date': self.date
        }
