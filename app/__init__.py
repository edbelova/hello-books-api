from flask import Flask
from .db import db, migrate
from .models import book
from .routes.book_routes import bp as book_routes
from .routes.author_routes import bp as author_routes
import os

def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(book_routes)
    app.register_blueprint(author_routes)
    
    return app