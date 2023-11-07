from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
import flask_sqlalchemy
import flask_marshmallow
from flask import render_template

db = flask_sqlalchemy.SQLAlchemy()
ma = flask_marshmallow.Marshmallow()

app = Flask(__name__, static_url_path='/')
app.config["JWT_SECRET_KEY"] = """
    vmkD0mL:r4ClE"<~D?gu'71Mo4rHi~/HTa@#6|;ddPXj'Wrhj`.&>'~rWLNg,T0
    """
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma.init_app(app)

jwt = JWTManager(app)
api = Api(app, prefix='/api')
