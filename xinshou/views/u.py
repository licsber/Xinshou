import uuid

from flask import Blueprint
from flask import current_app
from flask import render_template
from flask import request

mod = Blueprint('register', __name__)


def notify(text):
    return f'<h1 align="center" style="color:#5DADE2; font-size:100px">{text}</h1>'


@mod.route('/')
def root():
    token = request.args['token']
    token = uuid.UUID(token)
    oid = current_app.session.get(token, 'register_root')
    if oid:
        token = uuid.uuid4()
        current_app.session.set(token, 'register_form', oid)
        return render_template('register.html', token=token)
    else:
        return notify('此链接不可分享、重入<br>请先关注公众号「心手」<br>重新获取绑定链接')


@mod.route('/submit', methods=['POST'])
def submit():
    token = request.form['token']
    token = uuid.UUID(token)
    oid = current_app.session.get(token, 'register_form')
    if not oid:
        return notify('链接已过期<br>请重新获取')

    no = request.form['stu_no']
    pwd = request.form['passwd']
    if uid := current_app.wisedu.add_account(oid, no, pwd):
        return notify(f"UID: {uid}<br>推荐长按复制保存<br>提交成功<br>请直接按左上角X关闭")
    else:
        return notify('密码错误或异常<br>请重新获取绑定链接')


@mod.route('/checkin', methods=['GET'])
def checkin():
    token = request.args['token']
    token = uuid.UUID(token)
    uid = current_app.session.get(token, 'checkin_root')
    if uid:
        return notify(f"UID：{uid}<br>")
    else:
        return notify('此链接不可重入<br>请先关注公众号「心手」<br>重新获取领Mana链接')
