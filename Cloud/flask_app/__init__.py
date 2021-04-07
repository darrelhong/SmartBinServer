import os
from flask import Flask
from sassutils.wsgi import SassMiddleware


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    app.wsgi_app = SassMiddleware(app.wsgi_app, {
        'flask_app': {
            'sass_path': 'static/sass',
            'css_path': 'static/css',
            'wsgi_path': '/static/css',
            'strip_extension': True,
        }
    })

    from flask_app.views import views
    from flask_app.api import api
    app.register_blueprint(views)
    app.register_blueprint(api, url_prefix='/api')

    from . import db
    db.init_app(app)

    return app
