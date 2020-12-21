from flask import Blueprint

mod = Blueprint('cpdaliy', __name__)


@mod.route('/')
def root():
    return 'Test.'
