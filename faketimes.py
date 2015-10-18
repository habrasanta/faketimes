import random
import hashlib

from flask import Flask, render_template, jsonify, request, flash, abort


# Можете добавить себя сюда, чтобы не вводить каждый раз.
users = [
    [1000000001, 'kafeman', 256.2, 0.0,
     '//hsto.org/getpro/habr/avatars/7bf/80e/da6/7bf80eda638211ca4a38ed48b4058c2d.png'],
    [1000000002, 'negasus', 101.0, 0.0,
     '//hsto.org/getpro/habr/avatars/74a/1b6/c64/74a1b6c647c673df32177e355647ac71.jpg'],
]


app = Flask(__name__)

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key'
))


@app.route('/login')
@app.route('/auth/o/login/')
def login():
    redirect_uri = request.args.get('redirect_uri').split('?', 1)[0]
    return render_template('login.html', redirect_uri=redirect_uri, users=users)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        user_id = random.randint(3, 99999)+1000000000
        username = request.form.get('username')
        avatar = request.form.get('avatar')
        if not avatar:
            avatar = '//hsto.org/storage/habrastock/i/avatars/stub-user-middle.gif'
        karma = float(request.form.get('karma'))
        rating = float(request.form.get('rating'))
        users.append([user_id, username, karma, rating, avatar])
        flash('Готово. Войдите заново, чтобы увидеть нового пользователя в списке.')
    return render_template('add.html')


@app.route('/token', methods=['POST'])
@app.route('/auth/o/access-token/', methods=['POST'])
def token():
    code = request.form.get('code')
    return jsonify(access_token='token%s' % code)


@app.route('/users/me')
@app.route('/api/v1/users/me')
def user():
    access_token = request.headers.get('token')
    for user_id, username, karma, rating, avatar in users:
        if access_token == 'tokenuser%d' % user_id:
            return jsonify(data={
                'id': user_id,
                'login': username,
                'avatar': avatar,
                'score': karma,
                'rating': rating,
                'is_readonly': False
            })
    abort(404)


if __name__ == '__main__':
    app.run(debug=True)
