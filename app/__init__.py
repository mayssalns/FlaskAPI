# CODING: UTF-8 

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://admin:admin@db:5432/Borges'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)

from .routes.authors import author
from .routes.books import book

app.register_blueprint(author)
app.register_blueprint(book)

db.create_all()


@app.route('/')
def index():
    return """
    <p>Author: <a href="http://0.0.0.0:8000/v1/author/">http://0.0.0.0:8000/v1/author/</a></p>
    <p>Book: <a href="http://0.0.0.0:8000/v1/book/">http://0.0.0.0:8000/v1/book/</a></p>
    """



