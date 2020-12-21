from flask import Blueprint
from flask import current_app

mod = Blueprint('licsber', __name__)


@mod.route('/')
def root():
    access_token = current_app.admin.get_access_token()
    return access_token
