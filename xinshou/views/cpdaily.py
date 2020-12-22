from flask import Blueprint
from flask import current_app
from flask import render_template
from flask import request

mod = Blueprint('cpdaily', __name__)


@mod.route('/')
def root():
    token = request.args['token']
    open_id = current_app.cpdaily.take_token(token)
    if open_id:
        return render_template('cpdaily.html', token=open_id)
    else:
        return '<h1>Token已过期, 请先关注公众号<心手>, 通过验证后再使用.</h1><br>' * 5


@mod.route('/submit', methods=['POST'])
def submit():
    stu_no = request.form['stu_no']
    passwd = request.form['passwd']
    open_id = request.form['token']
    if current_app.cpdaily.add_user(stu_no, passwd, open_id):
        return '<h1>提交成功.</h1>'
    else:
        return '<h1>密码错误或该微信已绑定账号，如需更改请联系管理员.</h1>'
