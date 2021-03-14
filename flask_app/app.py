from flask import Flask, render_template
from sassutils.wsgi import SassMiddleware

from api import api

app = Flask(__name__)
app.wsgi_app = SassMiddleware(app.wsgi_app, {
    'app': {
        'sass_path': 'static/sass',
        'css_path': 'static/css',
        'wsgi_path': '/static/css',
        'strip_extension': True,
    }
})
app.register_blueprint(api, url_prefix='/api')


@app.route('/')
def hello():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
