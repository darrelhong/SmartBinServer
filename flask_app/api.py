from flask import Blueprint

# all routes are prefixed with /api
api = Blueprint('api', __name__)


@api.route('/')
def hello():
    return 'Hello API'
