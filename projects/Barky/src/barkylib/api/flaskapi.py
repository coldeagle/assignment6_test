import json
from datetime import datetime
from barkylib.api import views
from barkylib import bootstrap
from barkylib.adapters.repository import *
from barkylib.domain import commands

# init from dotenv file
from dotenv import load_dotenv
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    jsonify,
)
from flask_sqlalchemy import SQLAlchemy
from .baseapi import AbstractBookMarkAPI

load_dotenv()

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookmarks.db'
# db = SQLAlchemy(app)
bus = bootstrap.bootstrap()


class FlaskBookmarkAPI(AbstractBookMarkAPI):
    """
    Flask
    """

    def __init__(self) -> None:
        super().__init__()

    # @app.route("/")
    def index(self):
        return f"Barky API"

    # @app.route("/api/one/<id>")
    def one(self, id):
        return self.first('id', id)

    # @app.route("/api/all")
    def all(self):
        cmd = commands.ListBookmarksCommand(
            None
        )
        result = bus.handle(cmd)
        if not result:
            return "not found", 404
        return jsonify(result), 200

    # @app.route("/api/first/<property>/<value>/<sort>")
    def first(self, filter, value):
        print('first')
        id = None
        title = None
        if filter is None or value is None:
            return "invalid input", 404
        if filter == 'id':
            id = int(value)
        elif filter == 'title':
            title = str(value)

        cmd = commands.ListBookmarksCommand(
            id=id,
            title=title,
        )
        print('trying to get result')
        result = bus.handle(cmd)
        print('results')
        print(json.dumps(result))
        if not result:
            return "not found", 404
        return jsonify(result), 200

    def many(self, filter, value, sort):
        pass

    def add(self, bookmark):
        try:

            cmd = commands.AddBookmarkCommand(
                None,
                bookmark.title,
                bookmark.url,
                bookmark.date_added,
                bookmark.date_edited,
                bookmark.notes,
            )
            bus.handle(cmd)
        except ImportError as e:
            print(str(e))
            return {"message": str(e)}, 400

        return f'posted'

    def add_post(self):
        req_json = request.get_json(force=True)
        bookmark = Bookmark(
            req_json.get('id'),
            req_json.get('title'),
            req_json.get('url'),
            req_json.get('date_added'),
            req_json.get('date_edited'),
            req_json.get('notes'),
        )
        return self.add(bookmark)

    def delete(bookmark):
        pass

    def update(bookmark):
        pass


fb = FlaskBookmarkAPI()
bp = Blueprint("flask_bookmark_api", __name__, url_prefix="/api")

# @app.route('/')
bp.add_url_rule("/", "index", fb.index, ["GET"])

# @app.route('/api/one/<id>')
bp.add_url_rule("/one/<id>", "one", fb.one, ["GET"])

# @app.route('/api/all')
bp.add_url_rule("/all", "all", fb.all, ["GET"])


bp.add_url_rule("/add", "add", fb.add_post, methods=["POST"])
