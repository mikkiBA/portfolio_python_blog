from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('testapp3.config')

db = SQLAlchemy(app)
from .models import sns_db

import testapp3.views