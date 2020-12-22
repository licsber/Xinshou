from flask import Blueprint
from flask import render_template
from flask import request

mod = Blueprint('bind', __name__)


@mod.route('/')
def bind():
    print(request.args)
    print(request.form)
    return render_template('bind.html')
