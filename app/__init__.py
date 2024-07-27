import os
import random
from flask import Flask, render_template, request, Response
from docx import Document
from werkzeug.utils import secure_filename

from jinja2 import Template as Jinja2_Template
from jinja2 import Environment, DictLoader

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "fortifydemoapp.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return render_template('index.html')

    # register the database commands
    from . import db

    db.init_app(app)

    # apply the blueprints to the app
    from . import auth
    from . import products
    from . import insecure

    app.register_blueprint(auth.bp)
    app.register_blueprint(products.bp)
    app.register_blueprint(insecure.bp)

    # make url_for('index') == url_for('shop.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    #app.add_url_rule("/", endpoint="index")

    return app