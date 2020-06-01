from app import db


class CurrencySync(db.Model):
    __tablename__ = 'currencysync'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date())
    isSynced = db.Column(db.Boolean())

    def __init__(self, date, isSynced):
        self.date = date
        self.isSynced = isSynced

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.date,
            'rate': self.isSynced
        }
