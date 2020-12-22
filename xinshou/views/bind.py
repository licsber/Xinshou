from flask import Blueprint

mod = Blueprint('bind', __name__)


@mod.route('/')
def bind():
    pass
