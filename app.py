import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(config.DevelopmentConfig())
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from controller.controller import controller
from exceptions.errorHandler import error

app.register_blueprint(controller, url_prefix='/api/v1')
app.register_blueprint(error)

if __name__ == '__main__':
    app.run()


class Person:
  def __init__(self, name=None, age=None):
    self.name = name
    self.age = age

p1 = Person("John", 36)
p2 = Person()
